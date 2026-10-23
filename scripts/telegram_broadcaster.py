#!/usr/bin/env python3
"""
TheBhom Telegram Broadcaster & Instant Click Pipeline
Autonomous Telegram channel broadcast engine for Breaking News & Hot Deals.
Supports @thebhom_deals, @thebhom_official, and @thebhom_news.
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED_FILE = os.path.expanduser('~/.gemini/config/credentials.env')
STATE_FILE = os.path.join(BASE_DIR, 'scripts', 'telegram_posted.json')
SITE_URL = "https://thebhom.in"

def load_credentials():
    creds = {
        'TELEGRAM_BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN', '8866349662:AAEYDu8ENkAL-um1OCeKwPxZ4MvM9CqfYY0'),
        'TELEGRAM_CHANNEL_ID': os.environ.get('TELEGRAM_CHANNEL_ID', '-1004358353540')
    }
    if os.path.exists(CRED_FILE):
        with open(CRED_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('export '):
                    line = line[7:]
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    v = v.strip().strip('"').strip("'")
                    creds[k.strip()] = v
    return creds

def get_posted_ids():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_posted_ids(posted):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(posted)[-500:], f, indent=2)

def telegram_api(token, method, payload):
    import ssl
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore')
        return e.code, body
    except Exception as e:
        return 0, str(e)

def verify_bot(token):
    s, r = telegram_api(token, "getMe", {})
    if s == 200 and isinstance(r, dict) and r.get('ok'):
        bot = r.get('result', {})
        print(f"[✅ Telegram] Bot connected: @{bot.get('username')} ({bot.get('first_name')})")
        return True, bot
    print(f"[❌ Telegram] Bot token invalid or network error: HTTP {s} - {r}")
    return False, None

def get_latest_deals():
    deals_dir = os.path.join(BASE_DIR, 'deals', 'p')
    deals = []
    if not os.path.exists(deals_dir):
        return deals
    
    files = [os.path.join(deals_dir, f) for f in os.listdir(deals_dir) if f.endswith('.html')]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    for fpath in files[:30]:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            name_m = re.search(r'"name"\s*:\s*"([^"]+)"', html)
            price_m = re.search(r'"price"\s*:\s*([0-9.]+)', html)
            store_url_m = re.search(r'"url"\s*:\s*"(https://[^"]+)"', html)
            img_m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            desc_m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
            
            slug = os.path.basename(fpath).replace('.html', '')
            name = name_m.group(1).strip() if name_m else slug
            price = price_m.group(1).strip() if price_m else ''
            store_url = store_url_m.group(1).strip() if store_url_m else f"{SITE_URL}/deals/p/{slug}.html"
            img = img_m.group(1).strip() if img_m else f"{SITE_URL}/assets/og-default.jpg"
            desc = desc_m.group(1).strip() if desc_m else ''
            
            deals.append({
                'id': f"deal_{slug}",
                'type': 'deal',
                'title': name,
                'price': price,
                'store_url': store_url,
                'page_url': f"{SITE_URL}/deals/p/{slug}.html",
                'desc': desc,
                'image': img
            })
        except Exception:
            continue
    return deals

def get_latest_news():
    news_dir = os.path.join(BASE_DIR, 'news')
    articles = []
    if not os.path.exists(news_dir):
        return articles
    
    files = [os.path.join(news_dir, f) for f in os.listdir(news_dir) if f.endswith('.html') and f != 'index.html']
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    for fpath in files[:15]:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            title_m = re.search(r'<title>([^<]+)</title>', content)
            desc_m = re.search(r'<meta name="description" content="([^"]+)"', content)
            img_m = re.search(r'<meta property="og:image" content="([^"]+)"', content)
            slug = os.path.basename(fpath).replace('.html', '')
            
            title = title_m.group(1).replace(' — TheBhom News', '').strip() if title_m else slug
            desc = desc_m.group(1).strip() if desc_m else ''
            img = img_m.group(1).strip() if img_m else f"{SITE_URL}/assets/og-default.jpg"
            
            articles.append({
                'id': f"news_{slug}",
                'type': 'news',
                'title': title,
                'desc': desc,
                'image': img,
                'url': f"{SITE_URL}/news/{slug}.html"
            })
        except Exception:
            continue
    return articles

def broadcast_deal(token, channel, deal):
    title = deal['title']
    price_str = f"₹{deal['price']}" if deal['price'] else "Great Price Drop"
    desc = deal['desc'][:200] + '...' if len(deal['desc']) > 200 else deal['desc']
    store_url = deal['store_url']
    page_url = deal['page_url']
    img = deal['image']
    
    caption = (
        f"🔥 *LOOT DEAL ALERT | THEBHOM*\n\n"
        f"🛍️ *{title}*\n"
        f"💰 *Deal Price: {price_str}*\n\n"
        f"⚡ {desc}\n\n"
        f"👉 [लूट डील यहाँ से खरीदें]({store_url})\n"
        f"🌐 [TheBhom Deals पर और ऑफर्स देखें]({SITE_URL}/deals/)"
    )
    
    buttons = [
        [{"text": f"🔥 Buy Now at {price_str}", "url": store_url}],
        [{"text": "🛍️ All Today's Deals (TheBhom)", "url": f"{SITE_URL}/deals/"}]
    ]
    
    photo_payload = {
        "chat_id": channel,
        "photo": img,
        "caption": caption,
        "parse_mode": "Markdown",
        "reply_markup": {"inline_keyboard": buttons}
    }
    
    status, resp = telegram_api(token, "sendPhoto", photo_payload)
    if status == 200:
        print(f"[✅ Telegram Sent Deal] {title[:40]} -> {channel}")
        return True
    
    # Fallback to sendMessage
    text_payload = {
        "chat_id": channel,
        "text": caption,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
        "reply_markup": {"inline_keyboard": buttons}
    }
    status2, resp2 = telegram_api(token, "sendMessage", text_payload)
    if status2 == 200:
        print(f"[✅ Telegram Sent Text Deal] {title[:40]} -> {channel}")
        return True
    else:
        print(f"[❌ Telegram Failed Deal] HTTP {status2}: {resp2}")
        return False

def broadcast_news(token, channel, art):
    title = art['title']
    desc = art['desc'][:220] + '...' if len(art['desc']) > 220 else art['desc']
    url = art['url']
    img = art['image']
    
    caption = (
        f"🚨 *BREAKING NEWS | THEBHOM*\n\n"
        f"*{title}*\n\n"
        f"{desc}\n\n"
        f"👉 [पूरी खबर यहाँ पढ़ें]({url})\n"
        f"🌐 [TheBhom.in पर ताज़ा अपडेट्स]({SITE_URL}/news/)"
    )
    
    buttons = [
        [{"text": "📰 पूरी खबर पढ़ें (Click Here)", "url": url}],
        [{"text": "⚡ ताज़ा खबरें (TheBhom News)", "url": f"{SITE_URL}/news/"}]
    ]
    
    photo_payload = {
        "chat_id": channel,
        "photo": img,
        "caption": caption,
        "parse_mode": "Markdown",
        "reply_markup": {"inline_keyboard": buttons}
    }
    
    status, resp = telegram_api(token, "sendPhoto", photo_payload)
    if status == 200:
        print(f"[✅ Telegram Sent News] {title[:40]} -> {channel}")
        return True
    
    text_payload = {
        "chat_id": channel,
        "text": caption,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
        "reply_markup": {"inline_keyboard": buttons}
    }
    status2, resp2 = telegram_api(token, "sendMessage", text_payload)
    if status2 == 200:
        print(f"[✅ Telegram Sent Text News] {title[:40]} -> {channel}")
        return True
    else:
        print(f"[❌ Telegram Failed News] HTTP {status2}: {resp2}")
        return False

def run_broadcast(max_items=2):
    creds = load_credentials()
    token = creds.get('TELEGRAM_BOT_TOKEN')
    channel = creds.get('TELEGRAM_CHANNEL_ID', '@thebhom_deals')
    
    if not token:
        print("[⚠️ Telegram Broadcaster] TELEGRAM_BOT_TOKEN not configured in credentials.env")
        return False
    
    ok, _ = verify_bot(token)
    if not ok:
        return False
    
    posted = get_posted_ids()
    mode = creds.get('TELEGRAM_BROADCAST_MODE', 'deals').lower()
    is_deals_channel = mode == 'deals' or 'deal' in channel.lower() or channel == "-1004358353540"
    
    sent_count = 0
    consecutive_failures = 0
    if is_deals_channel:
        deals = get_latest_deals()
        for deal in deals:
            if deal['id'] in posted:
                continue
            success = broadcast_deal(token, channel, deal)
            if success:
                posted.add(deal['id'])
                sent_count += 1
                consecutive_failures = 0
                time.sleep(3)
            else:
                consecutive_failures += 1
                if consecutive_failures >= 2:
                    print(f"[⚠️ Telegram] Channel {channel} unreachable. Verify that the channel exists and @thebhom_live_bot is an Admin.")
                    break
            if sent_count >= max_items:
                break
    else:
        news_items = get_latest_news()
        for art in news_items:
            if art['id'] in posted:
                continue
            success = broadcast_news(token, channel, art)
            if success:
                posted.add(art['id'])
                sent_count += 1
                consecutive_failures = 0
                time.sleep(3)
            else:
                consecutive_failures += 1
                if consecutive_failures >= 2:
                    print(f"[⚠️ Telegram] Channel {channel} unreachable. Verify that the channel exists and @thebhom_live_bot is an Admin.")
                    break
            if sent_count >= max_items:
                break
                
    save_posted_ids(posted)
    print(f"[🚀 Telegram Broadcast Complete] Sent {sent_count} items to {channel}.")
    return True

if __name__ == '__main__':
    run_broadcast()
