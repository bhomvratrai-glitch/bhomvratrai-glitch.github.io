# Active Project Memory — TheBhom (`thebhom.in`)

## 1. Project Vision & Architecture
- **Primary Domain**: `thebhom.in` / `www.thebhom.in`
- **Hosting Platform**: Cloudflare Pages (`thebhom`, `thebhom.pages.dev`)
- **Git Repo**: `https://github.com/bhomvratrai-glitch/thebhom-landing.git` (branch `main`)
- **Direct Deploy Command**:
  ```bash
  npx -y wrangler pages deploy . --project-name=thebhom --commit-dirty=true
  ```
- **Edge Cache Purge**:
  ```bash
  curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CLOUDFLARE_DNS_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{"purge_everything":true}'
  ```

---

## 2. Site Architecture Cleanup (October 18, 2026)
- **Active Core Structure**:
  - **Main Landing Site**: Root (`/`) at `https://www.thebhom.in/` featuring Deals Hub & Universal Video Downloader.
  - **Deals Store**: Subdirectory (`/deals/`) at `https://www.thebhom.in/deals/`.
  - **Universal Video Downloader**: Subdirectory (`/downloader/`) at `https://www.thebhom.in/downloader/`.
- **Obsolete Sections Removed & 301 Redirected to Root**:
  - `/tools/`, `/imgpdf/`, `/wallpapers`, `/ebooks`, `/magazines`, `/templates`, `/cards`, `/news/`.
- **Preserved Tags & Verification System**:
  - Google AdSense: `ca-pub-4674566886677472` (Script & Account meta + `ads.txt`).
  - Google Tag Manager: `GTM-K2B22XSW`.
  - Google Analytics 4: `G-GHVNZWFVQV`.
  - Pinterest Domain Verification: `027b813eb55f730989b6236aea44ed88`.
  - Google Search Console Verification: `googlec324d892b7f2bbf5`.
- **Sitemap & SEO**:
  - `sitemap.xml` streamlined to 35 high-priority canonical URLs.
  - `robots.txt` updated to allow `/`, `/deals/`, `/downloader/` and disallow removed sections.


---

## 2. Google AdSense & SEO Audit (Fixed on October 5, 2026)
### AdSense Account & Status
- **Publisher ID**: `ca-pub-4674566886677472`
- **Current Status**: **"Getting ready — Getting your site ready to show ads" (Review Requested)**
- **Previous Rejection Reason**: "Low value content" (Thin content, crawler timeout, and canonical mismatch).

### Root Causes Diagnosed & Fixed
1. **Deferred AdSense Loader Timeout**:
   - *Problem*: AdSense snippet was loaded after a 7-second timer or mousemove/scroll event (`loadAdSense()`). The Google AdSense review crawler does not simulate human mouse movements and times out after 3-5 seconds, causing Google's bot to see 0 ads or script tags.
   - *Fix*: Replaced with official standard `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4674566886677472" crossorigin="anonymous"></script>` in `<head>`.
2. **Cloudflare 308 Redirect vs Canonical Mismatch**:
   - *Problem*: Cloudflare Pages automatically strips `.html` via 308 Permanent Redirect (e.g. `/wallpapers.html` -> `/wallpapers`). However, `<link rel="canonical">` pointed back to `.html`, creating an infinite redirect confusion loop for Googlebot.
   - *Fix*: Standardized all canonical URLs and internal links across the entire site to extensionless clean URLs (e.g., `https://www.thebhom.in/wallpapers`).
3. **Thin Content De-indexation (184 Affiliate Product Pages)**:
   - *Problem*: Auto-generated deal pages in `/deals/p/*.html` constituted over 50% of the site's indexable pages, triggering "Scraped / Thin Affiliate Content" filters.
   - *Fix*: Marked all 184 product deal pages with `<meta name="robots" content="noindex, follow"/>` and disallowed bot crawling in `robots.txt`. The deals hub remains accessible to human users.
4. **Trademark & Copyright Guardrails**:
   - *Problem*: Pages mentioning commercial copyrighted brands or uncurated magazines/cartoons (e.g. Marvel wallpapers, cartoon voice clones) triggered Google policy scanners.
   - *Fix*: Added `noindex, nofollow` to `/marvel/`, `/cartoon/`, `/voices/` and disallowed them in `robots.txt`. Replaced hyperbolic claims ("1 Crore books, Forbes, NatGeo") with realistic educational/public domain descriptions.
5. **Sanitized Navigation & Sitemaps**:
   - *Problem*: Header/Footer navigation contained broken tool anchor links and an "Admin Panel" link. Sitemap was bloated with 1,220 redirecting or thin URLs.
   - *Fix*: Cleaned `shared.js` navigation links to only verified working tools. Regenerated `sitemap.xml` with 54 high-quality, 200 OK canonical URLs.
6. **Hardened `robots.txt`**:
   - Disallowed non-public and low-value directories: `/deals/p/`, `/admin/`, `/marvel/`, `/cartoon/`, `/voices/`, `/pricing.html`, `/checkout.html`, `/dashboard.html`.

---

## 3. TheBhom Real-Time News & Viral Stories Engine (Added October 5, 2026)
- **Subpath**: `/news/` (`https://www.thebhom.in/news/`)
- **Automated Generator**: `python3 scripts/news_engine.py`
  - Fetches live RSS from Google News India, Space/ISRO, Tech/AI, Viral Science.
  - Automatically synthesizes rich, human-touch articles with key highlights, background analysis, source attribution, and Schema.org `NewsArticle` JSON-LD.
  - Generates individual `news/[slug].html` pages.
  - Generates Google Publisher Center RSS feed (`/feed.xml` & `/news/rss.xml`).
  - Generates Google News Sitemap (`/sitemap-news.xml`).
  - Automatically injects live trending articles into Homepage (`/index.html`) under section `#live-news-section` for instant Googlebot internal link discovery.
  - Updates master `sitemap.xml` (currently tracking 240+ canonical URLs).

---

## 4. Automated Hourly Publishing & Traffic Pipeline (Active)
- **Hourly Cron Daemon**: `in.thebhom.news-hourly` LaunchAgent running every 3600 seconds (1 hour) via macOS `launchd`. Runs automatically on boot/wake.
- **Hourly Workflow**:
  1. `news_engine.py`: Scrapes top trending Google News India, ISRO/Space, Tech/AI, Viral Science, synthesizes full SEO articles with Schema.org `NewsArticle` JSON-LD.
  2. Injects trending stories into `index.html` homepage `#live-news-section`.
  3. Updates `feed.xml` (RSS 2.0 with media enclosures).
  4. Updates `sitemap-news.xml` and `sitemap.xml`.
  5. Commits and pushes changes to GitHub `main` branch.
  6. Deploys to Cloudflare Pages via Wrangler (`npx -y wrangler pages deploy . --project-name=thebhom`).
  7. Purges Cloudflare Edge Cache via Cloudflare API.
  8. Submits newly generated URLs to IndexNow (`api.indexnow.org` and `bing.com/indexnow`) with HTTP 200 instant crawl triggers.
  9. Runs `traffic_booster.py` for multi-platform distribution.

---

## 5. Google Search Console & Indexing Status
- **Domain Property**: `sc-domain:thebhom.in`
- **Sitemaps Submitted**:
  - `https://thebhom.in/sitemap.xml` (Status: Success, 254 discovered URLs)
  - `https://www.thebhom.in/sitemap.xml` (Status: Success, 254 discovered URLs)
  - `https://thebhom.in/sitemap-news.xml` (Submitted & Queued)
  - `https://thebhom.in/thebhom-indexnow-key-2024.txt` (Verified HTTP 200 on live edge)
- **Live URL Priority Indexing**:
  - `https://thebhom.in/news/` submitted to Google's Priority Crawl Queue via Search Console CDP automation.
- **Pinterest Integration**:
  - RSS feeds actively auto-publishing Pins to boards (@bhomvrat).
  - `thebhom.in/pinterest-feed.xml` -> Loot Deals board
  - `thebhom.in/feed.xml` -> Active feed

---

## 6. Active Production Verification
- Live site returns HTTP 200 on all canonical clean URLs.
- AdSense script executes synchronously on page load (`pub-4674566886677472`).
- Cloudflare Pages deployment verified live.
- Cloudflare Edge Cache purge API verified (`{"success":true}`).

---

## 7. Community Traffic & Instant Telegram Deals Pipeline (October 5, 2026)
### Quora Live Backlinks
- **Answer 1**: *How do I compress PDF files online for free?*
  - Live URL: `https://www.quora.com/How-do-I-compress-PDF-files-online-for-free/answer/Bhomvrat-Rai`
  - Backlinks to: `https://www.thebhom.in/imgpdf/compress-pdf-online` and `https://www.thebhom.in/imgpdf/merge-pdf`
- **Answer 2**: *How do I merge PDF files for free?*
  - Live URL: `https://www.quora.com/How-do-I-merge-PDF-files-for-free/answer/Bhomvrat-Rai`
  - Backlinks to: `https://www.thebhom.in/imgpdf/merge-pdf` and `https://www.thebhom.in/imgpdf/compress-pdf-online`

### Telegram Deals & News Broadcaster
- **Bot**: `@thebhom_live_bot` ("TheBhom News and Deals", ID `8866349662`)
- **Target Channel**: `@thebhom_deals`
- **User Telegram Account**: `bhom1207` (ID `1063182415`)
- **Broadcaster Script**: `scripts/telegram_broadcaster.py`
  - Auto-extracts top verified deals from `deals/p/*.html`
  - Sends high-resolution product cards with bold discount pricing and direct store affiliate links (`fktr.in` / Amazon tag `bhom120704-21`).
  - Integrated into hourly autonomous cron via `scripts/traffic_booster.py`.
