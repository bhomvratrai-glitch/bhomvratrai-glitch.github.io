#!/usr/bin/env python3
"""
Upgrade remaining older orphan product pages in deals/p/
Extracts metadata from existing HTML and applies the new Flipshope-style template.
"""

import os
import re
import json
import time
from generate_flipshope_style_page import generate_flipshope_html

DEALS_P_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "deals", "p"))

def upgrade_all_orphans():
    print("==================================================")
    print("🚀 Upgrading Older Product Pages to Flipshope Style")
    print("==================================================")
    
    files = [f for f in os.listdir(DEALS_P_DIR) if f.endswith(".html")]
    print(f"Total files in deals/p: {len(files):,}")
    
    start_time = time.time()
    upgraded = 0
    skipped = 0
    
    for idx, fname in enumerate(files, start=1):
        fpath = os.path.join(DEALS_P_DIR, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                
            if "Price History & Price Tracker" in content:
                skipped += 1
                continue
                
            # Extract JSON-LD if present
            prod = {}
            m_json = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
            if m_json:
                try:
                    data = json.loads(m_json.group(1))
                    if isinstance(data, dict):
                        prod["title"] = data.get("name", "")
                        images = data.get("image", [])
                        prod["image"] = images[0] if isinstance(images, list) and images else str(images)
                        offers = data.get("offers", {})
                        if isinstance(offers, dict):
                            prod["price"] = int(float(offers.get("price", 0)))
                            seller = offers.get("seller", {})
                            if isinstance(seller, dict):
                                prod["store"] = seller.get("name", "Amazon")
                            elif isinstance(seller, str):
                                prod["store"] = seller
                        brand = data.get("brand", {})
                        if isinstance(brand, dict):
                            prod["brand"] = brand.get("name", "")
                        elif isinstance(brand, str):
                            prod["brand"] = brand
                        prod["id"] = data.get("sku") or data.get("mpn") or fname.replace(".html", "")
                except Exception:
                    pass
                    
            # Fallbacks from meta tags
            if not prod.get("title"):
                m_title = re.search(r'<meta property="og:title" content="([^"]+)"', content)
                if m_title:
                    prod["title"] = m_title.group(1).split(" - ₹")[0]
                else:
                    prod["title"] = fname.replace(".html", "").replace("-", " ").title()
                    
            if not prod.get("image"):
                m_img = re.search(r'<meta property="og:image" content="([^"]+)"', content)
                if m_img:
                    prod["image"] = m_img.group(1)
                    
            if not prod.get("price") or prod["price"] == 0:
                m_price = re.search(r'₹([\d,]+)', content)
                if m_price:
                    prod["price"] = int(m_price.group(1).replace(",", ""))
                else:
                    prod["price"] = 999
                    
            # Extract Buy button link
            m_link = re.search(r'<a href="([^"]+)"[^>]*class="[^"]*telegram-deal-pill', content)
            if not m_link:
                m_link = re.search(r'Buy Now on[^<]*</a>.*?href="([^"]+)"', content, re.DOTALL)
            if not m_link:
                m_link = re.search(r'href="(https?://[^"]+)"[^>]*>[^<]*Buy Now', content, re.IGNORECASE)
                
            if m_link:
                prod["profitLink"] = m_link.group(1)
            else:
                prod["profitLink"] = f"https://www.thebhom.in/deals/"
                
            # Extract store
            if not prod.get("store"):
                if "amazon" in content.lower():
                    prod["store"] = "Amazon"
                elif "flipkart" in content.lower():
                    prod["store"] = "Flipkart"
                elif "myntra" in content.lower():
                    prod["store"] = "Myntra"
                else:
                    prod["store"] = "Amazon"
                    
            # Ensure MRP
            m_mrp = re.search(r'line-through[^>]*>₹([\d,]+)', content)
            if m_mrp:
                prod["mrp"] = int(m_mrp.group(1).replace(",", ""))
            else:
                prod["mrp"] = int(prod["price"] * 1.6)
                
            prod["dedicatedPage"] = f"https://www.thebhom.in/deals/p/{fname}"
            
            _, _, new_html = generate_flipshope_html(prod)
            
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_html)
                
            upgraded += 1
            if upgraded % 1000 == 0:
                print(f"  ✓ Upgraded {upgraded:,} pages...")
                
        except Exception as e:
            pass
            
    elapsed = round(time.time() - start_time, 2)
    print(f"\n🎉 Finished! Upgraded: {upgraded:,} pages | Already modern: {skipped:,} | Time: {elapsed}s")

if __name__ == "__main__":
    upgrade_all_orphans()
