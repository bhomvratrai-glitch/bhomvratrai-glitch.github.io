#!/usr/bin/env python3
"""
TheBhom Autonomous WhatsApp Deals Broadcaster
Formats verified lowest-price loot deals with 1-click affiliate links,
price history tracking links, and channel syndication.
"""

import os
import sys
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CATALOG_PATH = os.path.join(BASE_DIR, "deals", "data", "catalog.json")
STATE_FILE = os.path.join(BASE_DIR, "scripts", "whatsapp_posted.json")
SITE_URL = "https://thebhom.in"
DEFAULT_WA_CHANNEL = "https://whatsapp.com/channel/0029Vb9DmoaEKyZLLKtLdc2I"

def get_posted_ids():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_posted_ids(posted):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(posted)[-500:], f, indent=2)

def get_top_loot_deals(limit=5):
    if not os.path.exists(CATALOG_PATH):
        return []
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            items = json.load(f)
        
        # Sort by highest genuine discount percentage
        items_sorted = sorted(items, key=lambda x: (int(x.get("discountNum", 0) or 0)), reverse=True)
        posted = get_posted_ids()
        
        deals = []
        for it in items_sorted:
            pid = it.get("id") or it.get("asin")
            if not pid or pid in posted:
                continue
            
            title = it.get("title", "").strip()
            price = str(it.get("price", "")).strip()
            mrp = str(it.get("mrp", "")).strip()
            discount = it.get("discountNum", 0)
            store = it.get("store", "Store").strip()
            direct_url = it.get("profitLink") or it.get("url", "")
            
            # Ensure Amazon affiliate tag
            if "amazon.in" in direct_url and "tag=" not in direct_url:
                sep = "&" if "?" in direct_url else "?"
                direct_url = f"{direct_url}{sep}tag=bhom120704-21"
            
            page_url = it.get("dedicatedPage") or f"{SITE_URL}/deals/"
            img = it.get("cleanImage") or it.get("image") or f"{SITE_URL}/assets/og-default.jpg"
            
            deals.append({
                "id": pid,
                "title": title,
                "price": price,
                "mrp": mrp,
                "discount": discount,
                "store": store,
                "store_url": direct_url,
                "page_url": page_url,
                "image": img
            })
            if len(deals) >= limit:
                break
        return deals
    except Exception as e:
        print(f"[⚠️ Error reading catalog]: {e}")
        return []

def format_whatsapp_deal_message(deal, channel_link=DEFAULT_WA_CHANNEL):
    title = deal["title"]
    price = deal.get("price", "")
    mrp = deal.get("mrp", "")
    discount = deal.get("discount", 0)
    store = deal.get("store", "Store")
    store_url = deal["store_url"]
    page_url = deal["page_url"]
    
    price_str = f"₹{price}" if price else "Loot Price"
    mrp_str = f" ~₹{mrp}~" if mrp and mrp != price else ""
    disc_str = f" (🔥 *{discount}% OFF*)" if discount else ""
    
    msg = (
        f"🔥 *LOOT DEAL ALERT | THEBHOM*\n\n"
        f"🛍️ *{title}*\n\n"
        f"💰 *Deal Price: {price_str}*{mrp_str}{disc_str}\n"
        f"🏪 *Store:* {store}\n\n"
        f"⚡ *1-Click Direct Store Purchase:*\n"
        f"👉 {store_url}\n\n"
        f"🌐 *Check Price History on TheBhom:*\n"
        f"👉 {page_url}\n\n"
        f"📢 *Join WhatsApp Channel for Instant Drops:*\n"
        f"👉 {channel_link}"
    )
    return msg

def main():
    deals = get_top_loot_deals(limit=2)
    if not deals:
        print("[ℹ️ WhatsApp Broadcaster] No new unposted loot deals found.")
        return
    
    posted = get_posted_ids()
    print(f"[🚀 WhatsApp Broadcaster] Prepared {len(deals)} verified loot deals for broadcast:")
    for d in deals:
        text = format_whatsapp_deal_message(d)
        print("-----------------------------------------")
        print(text)
        print("-----------------------------------------")
        posted.add(d["id"])
    
    save_posted_ids(posted)
    print(f"[✅ WhatsApp Broadcaster] {len(deals)} deals staged and state recorded in whatsapp_posted.json")

if __name__ == "__main__":
    main()
