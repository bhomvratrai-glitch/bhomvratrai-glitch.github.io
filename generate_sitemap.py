#!/usr/bin/env python3
import os
import glob
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.utcnow().strftime('%Y-%m-%d')

urls = []

# 1. Main Landing Pages & Subdomains (Cleaned: Root, Deals, Downloader, Policy pages)
main_pages = [
    ('/', '1.0', 'daily'),
    ('/deals/', '0.95', 'daily'),
    ('/downloader/', '0.9', 'daily'),
    ('/about', '0.8', 'monthly'),
    ('/contact', '0.8', 'monthly'),
    ('/privacy-policy', '0.7', 'monthly'),
    ('/terms', '0.7', 'monthly'),
    ('/disclaimer', '0.7', 'monthly'),
]
for path, priority, freq in main_pages:
    urls.append((f'https://www.thebhom.in{path}', priority, freq))

# 2. High-Value Guide Articles (SEO & AdSense Quality Content)
for f in sorted(glob.glob(os.path.join(BASE_DIR, 'articles', '*.html'))):
    b = os.path.basename(f)
    slug = b[:-5]
    if slug == 'index':
        urls.append(('https://www.thebhom.in/articles/', '0.95', 'daily'))
    else:
        urls.append((f'https://www.thebhom.in/articles/{slug}', '0.85', 'weekly'))

# Remove duplicates while preserving order
seen = set()
unique_urls = []
for u, pri, freq in urls:
    if u not in seen:
        seen.add(u)
        unique_urls.append((u, pri, freq))

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url, pri, freq in unique_urls:
    xml_lines.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>')

xml_lines.append('</urlset>\n')

sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(xml_lines))

print(f"Generated {sitemap_path} successfully with {len(unique_urls)} canonical URLs.")
