# Active Project Memory — TheBhom (`thebhom.in`)

## 1. Project Vision & Architecture
- **Primary Domain**: `thebhom.in` / `www.thebhom.in`
- **Hosting Platform**: Cloudflare Pages (`thebhom`, `thebhom.pages.dev`)
- **Git Repo**: `https://github.com/bhomvratrai-glitch/thebhom-landing.git` (branch `main`)
- **Direct Deploy Command**:
  ```bash
  env -u CLOUDFLARE_API_KEY CLOUDFLARE_ACCOUNT_ID="$CLOUDFLARE_ACCOUNT_ID" CLOUDFLARE_API_TOKEN="$CLOUDFLARE_PAGES_TOKEN" npx -y wrangler pages deploy . --project-name=thebhom --commit-dirty=true
  ```
- **Edge Cache Purge**:
  ```bash
  curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CLOUDFLARE_PURGE_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"purge_everything":true}'
  ```

---

## 2. Active Core Structure & Cleaned Ecosystem (October 18, 2026)
- **Active Core Structure (Ultra-Clean Focus)**:
  - **Main Landing Site**: Root (`/`) at `https://www.thebhom.in/` featuring Deals Hub and Universal Video Downloader.
  - **Deals Store**: Subdirectory (`/deals/`) at `https://www.thebhom.in/deals/` featuring curated daily loot deals, price drop tracking, and direct affiliate links.
  - **Universal Video Downloader**: Subdirectory (`/downloader/`) at `https://www.thebhom.in/downloader/` supporting 40+ platforms with zero watermarks.
  - **Company & Policies**: Clean `/about`, `/contact`, `/privacy-policy`, `/terms`, `/disclaimer`.
- **Completely Eradicated Thin Content Sections (301 Permanent Redirects to `/` or `/deals/`)**:
  - Articles & Guides (`/articles/` - all 13 articles permanently purged, 301 redirect to `/deals/`)
  - Image Tools (`/tools/`, compress-image, resize, etc. - 301 redirect to `/`)
  - Subdomains: `https://toolnest.thebhom.in/` and `https://imgpdf.thebhom.in/` (All GSC prefix removals active)
  - HVAC Programmatic Doorway Directory (`/directory/` - 1,159 pages deleted, GSC prefix removal active)
  - Old verticals: `/wallpapers`, `/ebooks`, `/magazines`, `/templates`, `/cards`, `/news/`
- **Google Search Console Removals Submitted & Active (Oct 18, 2026)**:
  - `Starts with: https://imgpdf.thebhom.in/` (Processing request)
  - `Starts with: https://toolnest.thebhom.in/` (Processing request)
  - `Starts with: https://www.thebhom.in/articles/` (Processing request)
  - `Starts with: https://www.thebhom.in/directory/` (Processing request)
  - `https://thebhom.in/product/` (Processing request)
- **Footer Cleanliness**:
  - Completely eliminated "Knowledge Hub" and "Image Tools" blocks.
  - Retained strictly: Downloader, Deals & Categories, Popular Deals & Tags, Company & Policy.
- **Sitemap & SEO**:
  - `sitemap-main.xml` streamlined down to 18 clean canonical URLs (Root, Deals, 11 Downloader pages, 5 Policy pages).
  - Deployed to Cloudflare Pages (`https://7822da79.thebhom.pages.dev` / `thebhom.in`).
  - Edge cache completely purged.

---

## 3. Telegram Deals Pipeline
- **Bot**: `@thebhom_live_bot` ("TheBhom News and Deals", ID `8866349662`)
- **Target Channel**: `@thebhom_deals`
- **User Telegram Account**: `bhom1207` (ID `1063182415`)
- **Broadcaster Script**: `scripts/telegram_broadcaster.py`
  - Sends high-resolution product cards with bold discount pricing and direct store affiliate links (`fktr.in` / Amazon tag `bhom120704-21`).

---

## 4. Production Verification Checklist
- [x] All 8 obsolete sections completely purged from repository, navigation, and sitemaps.
- [x] Zero leftover files for tools, imgpdf, wallpapers, ebooks, magazines, templates, cards, news.
- [x] Canonical `sitemap.xml` regenerated with 22 clean, 200 OK URLs.
- [x] All monetization, GTM, GA4, AdSense, and Pinterest tags intact.
- [x] Cloudflare 301 redirects active for all old URLs.
- [x] Universal Video Downloader SEO & Google Indexing completed:
  - All 11 Downloader URLs (`/downloader/` + 10 specialized tool subpages) registered in canonical `sitemap-main.xml`.
  - Rich Schema.org structured data (`WebApplication`, `HowTo`, `FAQPage`) embedded on each page.
  - Sitemaps verified in Google Search Console with Status: **Success**.
  - Automated Chrome CDP batch inspection executed: Live tests completed and Indexing Requested on Google Search Console for all target downloader pages.
- [x] Cloudflare Pages deployed and cache purged.
- [x] AdSense "Low Value Content" root-cause fixes applied & verified:
  - Completely purged prompt leaks and comments across all 11 downloader pages.
  - Replaced dead footer navigation in `shared.js` with active Downloader tools.
  - Added `Disallow: /directory/` to `robots.txt` under `Mediapartners-Google` and `AdsBot-Google` to block 1,159 thin programmatic pages.
  - Edge cache purged and live verified.
- [x] High-Volume Tool SEO & Google Discover Optimization (Oct 18, 2026):
  - Updated all 11 Downloader tools with highest-volume exact search queries and CTR meta tags.
  - Injected mandatory `<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">` across all pages for Google Discover eligibility.
  - Replaced outdated news feeds with verified, high-res Deals Feed (`feed.xml` & `rss.xml`) featuring 1200px images, `media:content`, and price drop alerts.
  - Injected RSS autodiscovery tags into `index.html` and `deals/index.html`.
  - Injected Schema.org `ItemList` with `Product` and `Offer` price snippets into `deals/index.html`.
  - Deployed to Cloudflare Pages (`https://1f1ae057.thebhom.pages.dev` / `thebhom.in`) and purged edge cache.
  - Pinged IndexNow API for instant crawling by Bing, Yahoo, and Yandex.

---

## 5. Autonomous Hourly Women's Clothing Deals Bot (`scripts/auto_hourly_deals_bot.py`)
- **Direct Flipshope API (`/api/prices/getrecentpricedrop`)**:
  - Connects to: `https://flipshope.com/deals?subcategory=dresses-leggings-maternity_wear-women_ethnicwear-women_jackets-women_jeans-women_shorts-women_topwear-women_winterwear-makeup`
  - Targets subcategories: Dresses (`301`), Leggings (`304`), Maternity (`305`), Skirts (`315`), Ethnicwear (`316`), Innerwear/Nightwear (`317`), Jackets (`318`), Jeans (`319`), Shorts (`320`), Topwear (`321`), Winterwear (`322`), Heels (`504`), Jewellery (`505`), Ethnic Footwear (`514`), Sandals (`515`), Shoes (`516`), Makeup (`804`).
  - Ingests 32-64 live women's clothing & beauty deals per call with zero bot blocks.
- **Affiliate Tagging Gate**:
  - Amazon: Direct `tag=bhom120704-21` (100% direct bank payout).
  - Flipkart/Myntra/Ajio: EK Affiliate / EarnKaro shortlinks (`5610321` via `affiliaters.in` API).
- **Dedicated SEO Landing Pages**:
  - Automatically generates `/deals/p/{slug}-{pid}.html` for every product.
  - Embedded with Schema.org `Product` JSON-LD, GA4 analytics (`G-GHVNZWFVQV`), AdSense, and responsive affiliate Buy buttons.
- **Pinterest Organic SEO Formatting (Strict Non-Spam Directives)**:
  - Title: Full, clean, natural product name (zero "Loot", "% OFF", "Price Drop", or price prefixes).
  - Description: Rich organic fashion copy detailing fabric, silhouette, occasions (festivals, wedding functions, casual outings, office wear), pairing/styling tips, and targeted Pinterest category hashtags (`#WomensFashion #EthnicWear #KurtiDesign #SareeLove #LehengaCholi #OOTD #FashionInspo`).
  - Feeds: Syndicates to `women-fashion-feed.xml` and `pinterest-feed.xml`.
- **Self-Healing Verification Audit Engine (`verify_and_self_heal`)**:
  - Runs at the end of every bot execution:
    1. Audits dedicated HTML pages existence & size (>500B); auto-regenerates missing ones on the fly.
    2. Verifies affiliate tracking parameters (`bhom120704-21` / `5610321`).
    3. Validates XML syntax for all 5 feed/sitemap files via `ElementTree`; auto-repairs namespace mismatches.
    4. Guarantees 0 spam words in Pinterest feeds.
    5. Confirms image and link reachability.
    6. Submits new URLs to IndexNow API (202 OK).
- **Cloud Automation**: Runs 24/7 on GitHub Actions (`.github/workflows/hourly_deals_bot.yml`) on cron `0 * * * *`.


