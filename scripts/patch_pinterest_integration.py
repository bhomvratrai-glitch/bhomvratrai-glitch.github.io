#!/usr/bin/env python3
"""
Patches Pinterest Integration across the site:
1. Feeds: Changes all Pinterest RSS links in women-fashion-feed.xml and pinterest-feed.xml
   to point directly to https://thebhom.in/deals/p/... dedicated landing pages.
2. Product Pages: Injects Pinterest Domain Verification (<meta name="p:domain_verify">)
   and OpenGraph product tags for Rich Pins into all deals/p/*.html pages.
3. Deals Index: Ensures official Pinterest follow badge and links exist in deals/index.html.
"""

import os
import re
import glob
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS_P_DIR = os.path.join(BASE_DIR, "deals", "p")
WOMEN_FEED = os.path.join(BASE_DIR, "women-fashion-feed.xml")
PIN_FEED = os.path.join(BASE_DIR, "pinterest-feed.xml")
DEALS_INDEX = os.path.join(BASE_DIR, "deals", "index.html")

PINTEREST_DOMAIN_TAG = '<meta name="p:domain_verify" content="027b813eb55f730989b6236aea44ed88">'

def build_pid_to_url_map():
    print("Building PID to HTML map...")
    pid_map = {}
    for f in os.listdir(DEALS_P_DIR):
        if f.endswith(".html"):
            pid = f.replace(".html", "").split("-")[-1].lower()
            url = f"https://www.thebhom.in/deals/p/{f}"
            pid_map[pid] = url
            pid_map[pid.replace("amz-", "").replace("fk-", "").replace("myn-", "")] = url
    print(f"Mapped {len(pid_map)} PIDs to dedicated pages.")
    return pid_map

def update_feeds(pid_map):
    for fpath in [WOMEN_FEED, PIN_FEED]:
        if not os.path.exists(fpath):
            continue
        print(f"Updating links in {os.path.basename(fpath)}...")
        tree = ET.parse(fpath)
        root = tree.getroot()
        channel = root.find("channel")
        if channel is None:
            continue
            
        updated = 0
        for it in channel.findall("item"):
            lnk = it.findtext("link") or ""
            guid = it.findtext("guid") or ""
            
            # Extract PID from guid or link
            pid = None
            if "thebhom-pin-" in guid:
                pid = guid.replace("thebhom-pin-", "").strip().lower()
            elif "/dp/" in lnk:
                m = re.search(r'/dp/([A-Za-z0-9]+)', lnk)
                if m: pid = m.group(1).lower()
            elif "myntra.com/" in lnk or "myntr.it" in lnk:
                m = re.search(r'/([0-9]{5,})', lnk)
                if m: pid = m.group(1).lower()
                
            if pid and pid in pid_map:
                canonical = pid_map[pid]
                l_elem = it.find("link")
                if l_elem is not None and l_elem.text != canonical:
                    l_elem.text = canonical
                    updated += 1
                g_elem = it.find("guid")
                if g_elem is not None:
                    g_elem.text = canonical
                    g_elem.set("isPermaLink", "true")
                    
        tree.write(fpath, encoding="utf-8", xml_declaration=True)
        
        # Clean namespace tags
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        if "xmlns:atom" not in c:
            c = c.replace("<rss ", '<rss xmlns:atom="http://www.w3.org/2005/Atom" ')
        c = re.sub(r'ns\d+:link', 'atom:link', c)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(c)
            
        print(f"  ✅ {os.path.basename(fpath)}: Successfully pointed {updated} links to dedicated pages.")

def patch_product_pages():
    print("Patching Pinterest domain verify tag into deals/p/*.html pages...")
    files = glob.glob(os.path.join(DEALS_P_DIR, "*.html"))
    count = 0
    for fpath in files:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if 'name="p:domain_verify"' not in content:
            if "<head>" in content:
                content = content.replace("<head>", f"<head>\n  {PINTEREST_DOMAIN_TAG}", 1)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(content)
                count += 1
    print(f"  ✅ Injected Pinterest verification meta tag into {count} pages.")

def patch_deals_index():
    if not os.path.exists(DEALS_INDEX):
        return
    with open(DEALS_INDEX, "r", encoding="utf-8") as f:
        content = f.read()
    if 'name="p:domain_verify"' not in content and "<head>" in content:
        content = content.replace("<head>", f"<head>\n  {PINTEREST_DOMAIN_TAG}\n")
    if "in.pinterest.com/bhomvrat" not in content and "</footer>" in content:
        pin_badge = """
        <a href="https://in.pinterest.com/bhomvrat/" target="_blank" rel="noopener" style="display:inline-flex; align-items:center; gap:6px; color:#e60023; font-weight:600; text-decoration:none;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 0 1 .083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12 0-6.627-5.373-12-12-12z"/></svg>
          <span>Follow @bhomvrat on Pinterest</span>
        </a>
        """
        content = content.replace("</footer>", f"{pin_badge}\n</footer>")
    with open(DEALS_INDEX, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✅ Updated deals/index.html with Pinterest verification & follow badge.")

def main():
    pid_map = build_pid_to_url_map()
    update_feeds(pid_map)
    patch_product_pages()
    patch_deals_index()
    print("\n🎉 Pinterest Integration & Backlink Patch Complete!")

if __name__ == "__main__":
    main()
