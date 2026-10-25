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
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED_FILE = os.path.expanduser('~/.gemini/config/credentials.env')
STATE_FILE = os.path.join(BASE_DIR, 'scripts', 'telegram_posted.json')
SITE_URL = "https://thebhom.in"

def sync_to_whatsapp(item):
    """
    Simultaneously syndicates the exact same item to WhatsApp Official Channel
    """
    wa_script = os.path.join(BASE_DIR, 'scripts', 'wa_cloud', 'send_broadcast.mjs')
    if not os.path.exists(wa_script):
        return False
    try:
        payload = json.dumps(item)
        res = subprocess.run(
            ['node', wa_script, '--json', payload],
            cwd=os.path.join(BASE_DIR, 'scripts', 'wa_cloud'),
            capture_output=True,
            text=True,
            timeout=30
        )
        if res.returncode == 0:
            print(f"[✅ WhatsApp Synced] {item.get('title', '')[:40]} -> WhatsApp Channel")
            return True
        else:
            err = res.stderr.strip() or res.stdout.strip()
            print(f"[⚠️ WhatsApp Sync Notice]: {err}")
            return False
    except Exception as e:
        print(f"[⚠️ WhatsApp Sync Error]: {e}")
        return False

def load_credentials():
    creds = {
        'TELEGRAM_BOT_TOKEN': os.environ.get('TELEGRAM_BOT_TOKEN', ''),
        'TELEGRAM_CHANNEL_ID': os.environ.get('TELEGRAM_CHANNEL_ID', '')
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
    catalog_path = os.path.join(BASE_DIR, 'deals', 'data', 'catalog.json')
    deals = []
    if os.path.exists(catalog_path):
        try:
            with open(catalog_path, 'r', encoding='utf-8') as f:
                items = json.load(f)
            
            # Prioritize high discount verified loot drops
            items_sorted = sorted(items, key=lambda x: (int(x.get('discountNum', 0) or 0)), reverse=True)
            
            for it in items_sorted[:120]:
                title = it.get('title', '').strip()
                price = str(it.get('price', '')).strip()
                mrp = str(it.get('mrp', '')).strip()
                discount = it.get('discountNum', 0)
                store = it.get('store', 'Store').strip()
                direct_url = it.get('profitLink') or it.get('url', '')
                
                # Enforce Amazon affiliate tag
                if 'amazon.in' in direct_url and 'tag=' not in direct_url:
                    sep = '&' if '?' in direct_url else '?'
                    direct_url = f"{direct_url}{sep}tag=bhom120704-21"
                
                page_url = it.get('dedicatedPage') or f"{SITE_URL}/deals/"
                img = it.get('cleanImage') or it.get('image') or f"{SITE_URL}/assets/og-default.jpg"
                pid = it.get('id') or it.get('asin') or re.sub(r'[^a-zA-Z0-9]', '', title)[:20]
                
                deals.append({
                    'id': f"deal_{pid}",
                    'type': 'deal',
                    'title': title,
                    'price': price,
                    'mrp': mrp,
                    'discount': discount,
                    'store': store,
                    'store_url': direct_url,
                    'page_url': page_url,
                    'image': img
                })
            return deals
        except Exception as e:
            print(f"[⚠️ Error loading catalog.json]: {e}")
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
    price = deal.get('price', '')
    mrp = deal.get('mrp', '')
    discount = deal.get('discount', 0)
    store = deal.get('store', 'Store')
    store_url = deal['store_url']
    page_url = deal['page_url']
    img = deal['image']
    
    price_str = f"₹{price}" if price else "Loot Price"
    mrp_str = f" ~₹{mrp}~" if mrp and mrp != price else ""
    disc_str = f" (🔥 {discount}% OFF)" if discount else ""
    
    caption = (
        f"🔥 *LOOT DEAL ALERT | THEBHOM*\n\n"
        f"🛍️ *{title}*\n\n"
        f"💰 *Deal Price: {price_str}*{mrp_str}{disc_str}\n"
        f"🏪 *Store:* {store}\n\n"
        f"⚡ *1-Click Direct Store Purchase:*\n"
        f"👉 [⚡ Buy Directly on {store}]({store_url})\n\n"
        f"🌐 *Check Price History & Tracker:*\n"
        f"👉 [View on TheBhom Site]({page_url})\n\n"
        f"📢 *Join Group:* [Loot Deals India](https://t.me/+UhSD6hAJe7NhODM1)"
    )
    
    buttons = [
        [{"text": f"⚡ Buy on {store} ({price_str})", "url": store_url}],
        [{"text": "🌐 Check Price History on TheBhom", "url": page_url}],
        [{"text": "📢 Join TheBhom Deals Channel", "url": "https://t.me/+UhSD6hAJe7NhODM1"}]
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
                sync_to_whatsapp(deal)
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
                sync_to_whatsapp(art)
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
