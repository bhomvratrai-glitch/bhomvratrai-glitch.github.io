#!/usr/bin/env python3
"""
Sync all products in deals/data/catalog.json to their exact dedicatedPage HTML files.
Guarantees 100% of catalog items have working dedicated pages on deals site (zero 404s).
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from generate_flipshope_style_page import generate_flipshope_html

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(WORKSPACE, "deals", "data", "catalog.json")
PAGES_DIR = os.path.join(WORKSPACE, "deals", "p")

def main():
    print(f"Loading catalog from {CATALOG_PATH}...")
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    os.makedirs(PAGES_DIR, exist_ok=True)
    disk_files = {f.lower(): f for f in os.listdir(PAGES_DIR) if f.endswith(".html")}

    token_to_file = {}
    for fl, f in disk_files.items():
        for t in re.findall(r"[a-z0-9]{6,}", fl):
            token_to_file[t] = f

    matched = 0
    generated = 0

    for i, p in enumerate(catalog):
        raw_id = (p.get("id") or "").lower()
        asin = (p.get("asin") or "").lower()
        slug = (p.get("slug") or "").lower()
        dp = p.get("dedicatedPage")

        found_file = None

        # 1. Existing dedicatedPage
        if dp:
            dp_file = dp.split("/")[-1].lower()
            if dp_file in disk_files:
                found_file = disk_files[dp_file]

        # 2. Direct slug
        if not found_file and slug:
            slug_file = (slug if slug.endswith(".html") else slug + ".html").lower()
            if slug_file in disk_files:
                found_file = disk_files[slug_file]

        # 3. ID / ASIN tokens
        if not found_file:
            tokens = re.findall(r"[a-z0-9]{6,}", raw_id) + re.findall(r"[a-z0-9]{6,}", asin)
            for t in tokens:
                if t in token_to_file:
                    found_file = token_to_file[t]
                    break

        if found_file:
            matched += 1
            p["dedicatedPage"] = f"https://www.thebhom.in/deals/p/{found_file}"
            p["slug"] = found_file.replace(".html", "")
        else:
            fname, curl, html = generate_flipshope_html(p)
            filepath = os.path.join(PAGES_DIR, fname)
            with open(filepath, "w", encoding="utf-8") as out:
                out.write(html)
            disk_files[fname.lower()] = fname
            for t in re.findall(r"[a-z0-9]{6,}", fname.lower()):
                token_to_file[t] = fname
            p["dedicatedPage"] = curl
            p["slug"] = fname.replace(".html", "")
            generated += 1

    print(f"Sync complete: {matched} matched existing files, {generated} generated new files.")
    print(f"Writing updated catalog back to {CATALOG_PATH}...")
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print("✅ Catalog successfully saved with 100% dedicatedPage coverage!")

if __name__ == "__main__":
    main()
