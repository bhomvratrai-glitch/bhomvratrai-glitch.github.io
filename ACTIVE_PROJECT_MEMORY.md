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
- **Active Core Structure**:
  - **Main Landing Site**: Root (`/`) at `https://www.thebhom.in/` featuring Deals Hub, Universal Video Downloader, and Knowledge Hub.
  - **Deals Store**: Subdirectory (`/deals/`) at `https://www.thebhom.in/deals/` featuring curated daily loot deals, price drop tracking, and direct affiliate links.
  - **Universal Video Downloader**: Subdirectory (`/downloader/`) at `https://www.thebhom.in/downloader/` supporting 40+ platforms with zero watermarks.
  - **Knowledge Hub**: In-depth creator & SEO guides in `/articles/` (13 verified high-quality canonical guides).
- **Completely Eradicated Sections (301 Permanent Redirects to `/`)**:
  - Web Tools (`/tools/`)
  - ImgPDF (`/imgpdf/`, `pricing.html`, `checkout.html`, `dashboard.html`, `payment.html`)
  - Wallpapers (`/wallpapers`)
  - E-Books (`/ebooks`)
  - Magazines (`/magazines`)
  - Templates (`/templates`)
  - Cards (`/cards`)
  - News Portal (`/news/`)
- **Preserved Tags & Verification System (100% Retained)**:
  - Google AdSense: `ca-pub-4674566886677472` (Script & Account meta + `ads.txt`).
  - Google Tag Manager: `GTM-K2B22XSW`.
  - Google Analytics 4: `G-GHVNZWFVQV`.
  - Pinterest Domain Verification: `027b813eb55f730989b6236aea44ed88`.
  - Google Search Console Verification: `googlec324d892b7f2bbf5`.
- **Sitemap & SEO**:
  - `sitemap.xml` streamlined to 22 high-priority canonical URLs (Root, Deals, Downloader, 5 Policy pages, 13 Articles, Articles Hub).
  - `robots.txt` cleaned and optimized for Googlebot, Mediapartners-Google, and AdsBot-Google.

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
- [x] Universal Video Downloader Zero-Fail Engine deployed live:
  - Local companion daemon running persistently on Mac Apple Silicon (`localhost:8085`) via LaunchAgent `com.thebhom.downloader.plist`.
  - Cloudflare Pages serverless engine (`functions/api/parse.js`) updated with instant oEmbed fallback & format synthesizer.
  - Zero-blank screen guarantee: `#resultCard` always renders with video title, channel, duration, high-res thumbnail, inline interactive embed player, and 6 full format cards (1080p, 720p, 480p, 360p, 320k MP3, 128k MP3).
  - 10 specialized tool subpages synchronized and deployed live to `thebhom.in`.
- [x] Cloudflare Pages deployed and cache purged.
