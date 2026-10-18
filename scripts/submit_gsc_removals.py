import asyncio
import json
import websockets
import base64
import urllib.request

async def get_gsc_ws_url():
    resp = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json").read())
    for target in resp:
        if "search.google.com/search-console/removals" in target.get("url", ""):
            return target["webSocketDebuggerUrl"]
    return None

async def run_removal_flow(urls_to_remove):
    ws_url = await get_gsc_ws_url()
    if not ws_url:
        print("ERROR: GSC Removals tab not found in Chrome!")
        return

    print(f"Connecting to CDP: {ws_url}")
    async with websockets.connect(ws_url) as ws:
        msg_id = 0
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            cur_id = msg_id
            payload = {"id": cur_id, "method": method}
            if params:
                payload["params"] = params
            await ws.send(json.dumps(payload))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == cur_id:
                    return msg

        for url in urls_to_remove:
            print(f"\n--- Submitting Removal for: {url} ---")
            # Step 1: Ensure on page or close any stray modal
            # Check if modal is open; if not open, click NEW REQUEST
            step1_js = '''
            (() => {
                const modal = document.querySelector('.g3VIld');
                if (modal) {
                    const cancel = Array.from(modal.querySelectorAll('button, div[role="button"], span')).find(b => b.innerText && b.innerText.trim() === 'CANCEL');
                    if (cancel) cancel.click();
                }
                return 'READY';
            })()
            '''
            await call("Runtime.evaluate", {"expression": step1_js})
            await asyncio.sleep(1)

            # Click NEW REQUEST
            click_new_js = '''
            (() => {
                const newBtn = Array.from(document.querySelectorAll('button, div[role="button"], span')).find(b => b.innerText && b.innerText.trim() === 'NEW REQUEST');
                if (newBtn) {
                    newBtn.click();
                    return 'CLICKED_NEW_REQUEST';
                }
                return 'NEW_REQUEST_NOT_FOUND';
            })()
            '''
            r = await call("Runtime.evaluate", {"expression": click_new_js, "returnByValue": True})
            print("Step 1 (New Request):", r.get("result", {}).get("result", {}).get("value"))
            await asyncio.sleep(1.5)

            # Step 2: Fill input and select prefix
            fill_js = f'''
            (() => {{
                const input = Array.from(document.querySelectorAll('input[placeholder="Enter URL"]')).find(i => i.offsetParent !== null);
                if (!input) return 'INPUT_NOT_FOUND';
                input.focus();
                input.value = '{url}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));

                const labels = Array.from(document.querySelectorAll('label'));
                const prefixLabel = labels.find(l => l.innerText && l.innerText.includes('Remove all URLs with this prefix'));
                if (prefixLabel) {{
                    prefixLabel.click();
                }}

                return {{
                    inputId: input.id,
                    inputValue: input.value,
                    prefixSelected: !!prefixLabel
                }};
            }})()
            '''
            r = await call("Runtime.evaluate", {"expression": fill_js, "returnByValue": True})
            print("Step 2 (Fill & Prefix):", r.get("result", {}).get("result", {}).get("value"))
            await asyncio.sleep(1)

            # Step 3: Click Next
            next_js = '''
            (() => {
                const nextBtn = Array.from(document.querySelectorAll('button, div[role="button"]')).find(b => b.innerText && b.innerText.trim() === 'Next');
                if (nextBtn) {
                    nextBtn.click();
                    return 'CLICKED_NEXT';
                }
                return 'NEXT_NOT_FOUND';
            })()
            '''
            r = await call("Runtime.evaluate", {"expression": next_js, "returnByValue": True})
            print("Step 3 (Next):", r.get("result", {}).get("result", {}).get("value"))
            await asyncio.sleep(2)

            # Step 4: Click SUBMIT REQUEST
            submit_js = '''
            (() => {
                const submitBtn = Array.from(document.querySelectorAll('button, div[role="button"], span')).find(b => b.innerText && b.innerText.trim() === 'SUBMIT REQUEST');
                if (submitBtn) {
                    submitBtn.click();
                    return 'CLICKED_SUBMIT_REQUEST';
                }
                return 'SUBMIT_NOT_FOUND';
            })()
            '''
            r = await call("Runtime.evaluate", {"expression": submit_js, "returnByValue": True})
            print("Step 4 (Submit):", r.get("result", {}).get("result", {}).get("value"))
            await asyncio.sleep(3)

        # Final step: Capture screenshot of the removals table
        print("\n--- Capturing Final Screenshot of GSC Removals Table ---")
        shot_res = await call("Page.captureScreenshot", {"format": "png"})
        shot_data = shot_res.get("result", {}).get("data")
        if shot_data:
            out_path = "/Users/bhomvratrai/.gemini/antigravity-ide/brain/4e665a7e-2f89-4642-95cf-22b5f08af84b/gsc_all_removals_live_verified.png"
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(shot_data))
            print(f"Screenshot successfully saved to: {out_path}")

urls = [
    "https://www.thebhom.in/articles/",
    "https://toolnest.thebhom.in/",
    "https://imgpdf.thebhom.in/"
]

asyncio.run(run_removal_flow(urls))
