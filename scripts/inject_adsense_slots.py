#!/usr/bin/env python3
"""
Injects Google AdSense tags and responsive advertisement spaces into all deals/p/*.html pages:
1. Head: Ensures client ca-pub-4674566886677472 script is present.
2. Slot 1 (Top Responsive Display): Placed right below breadcrumbs (slot 5470514139).
3. Slot 2 (Bottom In-Article Responsive): Placed before </main> (slot 9101298657).
"""

import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEALS_P_DIR = os.path.join(BASE_DIR, "deals", "p")

ADSENSE_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4674566886677472" crossorigin="anonymous"></script>'

TOP_AD_SLOT = """
    <!-- AdSense Top Responsive Display Slot -->
    <div style="margin: 0 0 20px 0; padding: 8px; background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; text-align: center;">
      <span style="display: block; font-size: 10px; font-weight: 700; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.5px; margin-bottom: 4px;">Advertisement</span>
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-4674566886677472"
           data-ad-slot="5470514139"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({});
      </script>
    </div>
"""

BOTTOM_AD_SLOT = """
    <!-- AdSense Bottom In-Article Responsive Slot -->
    <div style="margin: 24px 0 0 0; padding: 16px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
      <span style="display: block; font-size: 10px; font-weight: 700; text-transform: uppercase; color: #94a3b8; letter-spacing: 0.5px; margin-bottom: 6px;">Sponsored Deal Alert</span>
      <ins class="adsbygoogle"
           style="display:block; text-align:center;"
           data-ad-layout="in-article"
           data-ad-format="fluid"
           data-ad-client="ca-pub-4674566886677472"
           data-ad-slot="9101298657"></ins>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({});
      </script>
    </div>
"""

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Skip if ad slots are already injected
    if 'data-ad-slot="5470514139"' in content:
        return False

    modified = False

    # 1. Ensure head script exists
    if "ca-pub-4674566886677472" not in content and "<head>" in content:
        content = content.replace("<head>", f"<head>\n  {ADSENSE_SCRIPT}", 1)
        modified = True

    # 2. Insert Top Ad Slot after </nav>
    if "</nav>" in content:
        content = content.replace("</nav>", f"</nav>\n{TOP_AD_SLOT}", 1)
        modified = True

    # 3. Insert Bottom Ad Slot before </main>
    if "</main>" in content:
        content = content.replace("</main>", f"{BOTTOM_AD_SLOT}\n  </main>", 1)
        modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

def main():
    print("Injecting Google AdSense spaces into deals/p/*.html pages...")
    files = glob.glob(os.path.join(DEALS_P_DIR, "*.html"))
    total = len(files)
    patched = 0
    
    for i, fpath in enumerate(files):
        if process_file(fpath):
            patched += 1
        if (i + 1) % 1000 == 0 or (i + 1) == total:
            print(f"  Processed {i + 1}/{total} pages ({patched} patched)...")

    print(f"\n🎉 Successfully injected AdSense ad units into {patched}/{total} product pages!")

if __name__ == "__main__":
    main()
