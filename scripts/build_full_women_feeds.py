#!/usr/bin/env python3
"""
Populates women-fashion-feed.xml and deals/rss-women.xml with all available
Women's Fashion products from deals/data/catalog.json (4,150+ products).

Applies:
- Clean titles (Zero promo words)
- Surgical categorization (26 categories)
- Rich Pinterest SEO descriptions & hashtags
- Valid landing page links (deals/p/{slug}.html) & high-res image enclosures
"""

import os
import re
import html
import json
import datetime
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

BASE_DIR = "/Users/bhomvratrai/Documents/GitHub/thebhom-landing"
CATALOG_PATH = os.path.join(BASE_DIR, "deals", "data", "catalog.json")
WOMEN_FEED_PATH = os.path.join(BASE_DIR, "women-fashion-feed.xml")
RSS_WOMEN_PATH = os.path.join(BASE_DIR, "deals", "rss-women.xml")

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scripts.reindex_all_feeds_seo import TAXONOMY, FALLBACK_CATEGORY, clean_title, categorize_product, generate_seo_description

def load_women_products():
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
        
    women_prods = []
    seen_ids = set()
    
    women_kws = [
        'women', "women's", 'womens', 'saree', 'sari', 'kurti', 'kurta', 'lehenga', 
        'choli', 'anarkali', 'chikankari', 'dupatta', 'dress', 'gown', 'skirt', 
        'heels', 'jhumka', 'jewellery', 'jewelry', 'handbag', 'tote bag', 'sling bag', 
        'peplum', 'crop top', 'tank top', 'blouse', 'palazzo', 'trousers', 'denim'
    ]
    
    for item in catalog:
        pid = str(item.get('id') or item.get('asin') or '')
        if not pid or pid in seen_ids:
            continue
            
        title = str(item.get('title', '')).strip()
        img = str(item.get('image', '')).strip()
        link = str(item.get('dedicatedPage', '') or item.get('profitLink', '') or item.get('url', '')).strip()
        dept = str(item.get('department', '')).lower()
        cat = str(item.get('category', '')).lower()
        
        if not title or not img or not link:
            continue
            
        is_women = (dept == 'women') or (cat in ['fashion', 'footwear'] and any(k in title.lower() for k in women_kws))
        if is_women:
            seen_ids.add(pid)
            women_prods.append(item)
            
    print(f"Total Unique Women Fashion Products Loaded: {len(women_prods)}")
    return women_prods

def build_rss_xml(products, channel_title, channel_link, channel_desc, output_path, max_items=3000):
    """Build standards-compliant, high-performance RSS 2.0 feed."""
    now_rfc822 = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/">',
        '  <channel>',
        f'    <title>{escape(channel_title)}</title>',
        f'    <link>{escape(channel_link)}</link>',
        f'    <description>{escape(channel_desc)}</description>',
        '    <language>en-in</language>',
        f'    <lastBuildDate>{now_rfc822}</lastBuildDate>',
        f'    <atom:link href="{escape(channel_link)}" rel="self" type="application/rss+xml" />',
        '    <image>',
        '      <url>https://thebhom.in/logo.png</url>',
        '      <title>TheBhom Women Fashion</title>',
        '      <link>https://thebhom.in</link>',
        '    </image>'
    ]
    
    count = 0
    cat_distribution = {}
    
    for prod in products[:max_items]:
        raw_title = prod.get('title', '')
        clean_name = clean_title(raw_title)
        
        # Categorize
        cat_key, cat_info = categorize_product(clean_name)
        cat_distribution[cat_key] = cat_distribution.get(cat_key, 0) + 1
        
        # SEO Description
        seo_desc = generate_seo_description(clean_name, cat_info)
        
        # Links
        prod_link = prod.get('dedicatedPage')
        if not prod_link or not prod_link.startswith('http'):
            slug = prod.get('slug')
            pid = prod.get('id') or prod.get('asin')
            if slug:
                prod_link = f"https://www.thebhom.in/deals/p/{slug}.html"
            else:
                prod_link = prod.get('profitLink') or prod.get('url') or "https://thebhom.in/deals/"
                
        # Image
        img_url = prod.get('cleanImage') or prod.get('image') or ''
        # Ensure https
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
            
        pid = prod.get('id') or prod.get('asin') or f"prod-{count}"
        pub_date = now_rfc822
        
        item_xml = [
            '    <item>',
            f'      <title>{escape(clean_name)}</title>',
            f'      <link>{escape(prod_link)}</link>',
            f'      <guid isPermaLink="true">{escape(prod_link)}</guid>',
            f'      <description>{escape(seo_desc)}</description>',
            f'      <category>{escape(cat_info["category_name"])}</category>',
            f'      <pubDate>{pub_date}</pubDate>',
            f'      <enclosure url="{escape(img_url)}" type="image/jpeg" length="500000" />',
            f'      <media:content url="{escape(img_url)}" medium="image" width="1000" height="1500" />',
            f'      <media:thumbnail url="{escape(img_url)}" />',
            '    </item>'
        ]
        xml_lines.extend(item_xml)
        count += 1
        
    xml_lines.extend(['  </channel>', '</rss>'])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_lines))
        
    print(f"\nWritten {count} items to {output_path}")
    print("Category Breakdown:")
    for k, v in sorted(cat_distribution.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  • {k}: {v} items")

def main():
    women_products = load_women_products()
    
    # 1. Update women-fashion-feed.xml (Top 3,000 Women Fashion products)
    build_rss_xml(
        products=women_products,
        channel_title="Women's Fashion & Ethnic Wear India | TheBhom",
        channel_link="https://thebhom.in/women-fashion-feed.xml",
        channel_desc="Curated Indian ethnic wear, designer sarees, chikankari kurtis, lehenga cholis, western dresses, korean trousers, heels and aesthetic fashion lookbooks.",
        output_path=WOMEN_FEED_PATH,
        max_items=3500
    )
    
    # 2. Update deals/rss-women.xml (Top 3,500 Women Fashion products)
    build_rss_xml(
        products=women_products,
        channel_title="Aesthetic Women's Fashion & Outfit Inspo | TheBhom",
        channel_link="https://thebhom.in/deals/rss-women.xml",
        channel_desc="Curated Indian ethnic wear, sarees, chikankari kurtis, aesthetic dresses, Korean trousers, and daily outfit inspiration lookbooks.",
        output_path=RSS_WOMEN_PATH,
        max_items=3500
    )

if __name__ == "__main__":
    main()
