#!/usr/bin/env python3
"""
Batch Regenerate all dedicated product pages in deals/p/ with the new Flipshope-Style template.
Iterates across all products in deals/data/catalog.json, attaches affiliate tracking,
and generates high-converting price history tracker pages.
"""

import os
import sys
import json
import time

# Add scripts directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

from generate_flipshope_style_page import generate_flipshope_html
from auto_hourly_deals_bot import build_affiliate_link

CATALOG_PATH = os.path.join(PROJECT_DIR, "deals", "data", "catalog.json")
DEALS_P_DIR = os.path.join(PROJECT_DIR, "deals", "p")

def run_batch_regeneration():
    print("==================================================")
    print("🚀 Batch Regenerating All Product Pages (Flipshope Style)")
    print("==================================================")
    
    if not os.path.exists(CATALOG_PATH):
        print(f"❌ Error: Catalog file not found at {CATALOG_PATH}")
        return 0
        
    os.makedirs(DEALS_P_DIR, exist_ok=True)
    
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    total = len(catalog)
    print(f"📦 Total products loaded from catalog.json: {total:,}")
    
    start_time = time.time()
    generated_count = 0
    updated_catalog = False
    
    for idx, prod in enumerate(catalog, start=1):
        # Ensure affiliate profitLink is attached
        if not prod.get("profitLink"):
            prod["profitLink"] = build_affiliate_link(prod.get("url", ""), prod.get("store", "Amazon"))
            updated_catalog = True
            
        fname, canonical_url, html = generate_flipshope_html(prod)
        filepath = os.path.join(DEALS_P_DIR, fname)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
            
        prod["dedicatedPage"] = canonical_url
        prod["slug"] = fname.replace(".html", "")
        generated_count += 1
        
        if idx % 1000 == 0 or idx == total:
            elapsed = time.time() - start_time
            print(f"  ✓ Processed {idx:,} / {total:,} pages ({round(idx/total*100, 1)}%) in {round(elapsed, 1)}s")
            
    # Save back updated catalog with any fixed profitLinks
    if updated_catalog:
        with open(CATALOG_PATH, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
        print("💾 Updated catalog.json with verified profitLinks.")
        
    total_elapsed = round(time.time() - start_time, 2)
    print(f"\n🎉 Successfully regenerated {generated_count:,} dedicated Flipshope-style pages in {total_elapsed} seconds!")
    return generated_count

if __name__ == "__main__":
    run_batch_regeneration()
