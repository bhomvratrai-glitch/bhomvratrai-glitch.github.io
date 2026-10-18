#!/usr/bin/env python3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.utcnow().strftime('%Y-%m-%d')

urls = [
    ('https://www.thebhom.in/', '1.0', 'daily'),
    ('https://www.thebhom.in/deals/', '0.95', 'daily'),
    ('https://www.thebhom.in/downloader/', '0.95', 'daily'),
    ('https://www.thebhom.in/downloader/youtube-video-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/youtube-shorts-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/youtube-song-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/instagram-reels-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/instagram-story-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/tiktok-video-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/facebook-video-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/twitter-video-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/pinterest-video-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/downloader/reddit-video-downloader.html', '0.90', 'daily'),
    ('https://www.thebhom.in/about', '0.7', 'monthly'),
    ('https://www.thebhom.in/contact', '0.7', 'monthly'),
    ('https://www.thebhom.in/privacy-policy', '0.6', 'monthly'),
    ('https://www.thebhom.in/terms', '0.6', 'monthly'),
    ('https://www.thebhom.in/disclaimer', '0.6', 'monthly'),
]

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for url, pri, freq in urls:
    xml_lines.append(f'  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><changefreq>{freq}</changefreq><priority>{pri}</priority></url>')

xml_lines.append('</urlset>\n')

sitemap_main_path = os.path.join(BASE_DIR, 'sitemap-main.xml')
with open(sitemap_main_path, 'w', encoding='utf-8') as out:
    out.write('\n'.join(xml_lines))

print(f"Generated {sitemap_main_path} successfully with {len(urls)} canonical URLs.")
