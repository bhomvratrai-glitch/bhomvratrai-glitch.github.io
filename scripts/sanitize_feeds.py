#!/usr/bin/env python3
"""
Sanitizes women-fashion-feed.xml and pinterest-feed.xml:
- Converts all legacy deal-spam titles and descriptions into 100% clean, high-ranking Pinterest SEO copy.
- Removes banned non-fashion items (grippers, laptops, idols, etc.).
- Preserves high-res enclosures, links, and pubDates.
"""

import os
import re
import xml.etree.ElementTree as ET
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "scripts"))
from auto_hourly_deals_bot import generate_pinterest_seo

BANNED_KW = [
    "gripper", "gym", "dumbbell", "exercise", "equipment", "fitness", "wrist",
    "laptop", "oled", "ssd", "ram", "intel", "processor", "tablet", "mouse",
    "keyboard", "cable", "charger", "earbuds", "headphone", "speaker", "tv",
    "idol", "murti", "brass", "shiva", "ganesha", "pooja", "god", "mandir",
    "beard", "shaving", "trimmer", "drill", "drain"
]

def is_banned(text):
    text_lower = text.lower()
    if any(b in text_lower for b in BANNED_KW):
        return True
    # Only treat as male if female keywords are absent
    has_male = bool(re.search(r'\b(men|men\'s|mens|male|boys)\b', text_lower))
    has_female = bool(re.search(r'\b(women|women\'s|womens|female|girl|girls)\b', text_lower))
    if has_male and not has_female:
        return True
    return False

def clean_legacy_item(it, store_hint="Amazon"):
    raw_title = it.findtext("title") or ""
    raw_desc = it.findtext("description") or ""
    link = it.findtext("link") or ""
    
    combined = raw_title + " " + raw_desc
    if is_banned(combined):
        return None # drop non-fashion / men-only items
        
    # Check if this item already has clean SEO format
    is_spammy = any(x in raw_desc for x in ["Deal Price", "Savings:", "Loot Deal", "% OFF% OFF", "👉 Buy Now:"]) or \
                any(x in raw_title for x in ["Under ₹", "% Off", "% OFF", "Loot", "Deal Price", "👰", "✨", "🌸", "🛍️", "⚡"])

    if not is_spammy and len(raw_title) > 20:
        return it # already clean

    # Extract real product title from description if available
    first_line = raw_desc.strip().split("\n")[0]
    real_title = first_line.split("—")[0].split(" - Perfect")[0].strip()
    
    # If first_line is generic, look into title tag or link slug
    if len(real_title) < 15 or "amazon sale" in real_title.lower() or "deal" in real_title.lower():
        # Try from title tag stripped of emojis
        cand_t = re.sub(r'[^\w\s\-\,\.]', '', raw_title).strip()
        if len(cand_t) >= 15 and "amazon sale" not in cand_t.lower():
            real_title = cand_t
        else:
            # Try from URL slug
            slug_match = re.search(r'/deals/p/([^/]+)\.html', link)
            if slug_match:
                slug_text = slug_match.group(1).rsplit("-", 1)[0].replace("-", " ").title()
                if len(slug_text) >= 15:
                    real_title = slug_text

    # Extract brand if mentioned
    brand = ""
    brand_match = re.search(r'🏷️ Brand:\s*([^\n\r]+)', raw_desc)
    if brand_match:
        brand = brand_match.group(1).strip()
    if not brand:
        store_match = re.search(r'Available on ([A-Za-z]+)', raw_desc)
        if store_match:
            brand = store_match.group(1).strip()

    store = "Myntra" if "myntr" in link else ("Flipkart" if "fkrt" in link or "flipkart" in link else "Amazon")

    prod_dummy = {
        "title": real_title if len(real_title) >= 10 else raw_title,
        "brand": brand,
        "store": store
    }
    
    seo_title, seo_desc = generate_pinterest_seo(prod_dummy)
    
    t_elem = it.find("title")
    if t_elem is not None:
        t_elem.text = seo_title
    d_elem = it.find("description")
    if d_elem is not None:
        d_elem.text = seo_desc
        
    return it

def sanitize_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    print(f"Sanitizing {os.path.basename(filepath)}...")
    tree = ET.parse(filepath)
    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        return
        
    items = channel.findall("item")
    total_before = len(items)
    cleaned_items = []
    
    for it in items:
        cleaned = clean_legacy_item(it)
        if cleaned is not None:
            cleaned_items.append(cleaned)
            
    # Remove existing items from channel and re-append cleaned
    for it in list(channel.findall("item")):
        channel.remove(it)
    for it in cleaned_items:
        channel.append(it)
        
    tree.write(filepath, encoding="utf-8", xml_declaration=True)
    
    # Fix XML namespace tags
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if "xmlns:atom" not in content:
        content = content.replace("<rss ", '<rss xmlns:atom="http://www.w3.org/2005/Atom" ')
    content = re.sub(r'ns\d+:link', 'atom:link', content)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"  ✅ {os.path.basename(filepath)}: Before={total_before}, After={len(cleaned_items)} (Removed {total_before - len(cleaned_items)} non-fashion/spam)")

def main():
    women_feed = os.path.join(BASE_DIR, "women-fashion-feed.xml")
    pin_feed = os.path.join(BASE_DIR, "pinterest-feed.xml")
    sanitize_file(women_feed)
    sanitize_file(pin_feed)

if __name__ == "__main__":
    main()
