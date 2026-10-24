const fs = require('fs');

const srcPath = 'downloader/youtube-song-downloader.html';
const destPath = 'downloader/video-to-mp3-converter.html';

let src = fs.readFileSync(srcPath, 'utf8');

// Replace Title and Meta
src = src.replace(/<title>.*?<\/title>/, '<title>Video to MP3 Converter — Extract 320kbps Audio from Any Video Free | TheBhom</title>');
src = src.replace(/<meta name="description" content=".*?" \/>/, '<meta name="description" content="Free online Video to MP3 Converter. Extract crystal-clear 320kbps MP3 audio, background music, and songs from YouTube, Instagram Reels, TikTok, Twitter, Facebook, and Reddit." />');
src = src.replace(/<meta name="keywords" content=".*?" \/>/, '<meta name="keywords" content="video to mp3 converter, extract audio from video, convert video to mp3 online free, youtube to mp3, instagram reel audio download, tiktok audio download, audio extractor 320kbps, video se audio kaise nikale, video to mp3 converter online" />');

// Replace OG and Canonical
src = src.replace(/<meta property="og:title" content=".*?" \/>/, '<meta property="og:title" content="Video to MP3 Converter — Extract 320kbps Audio Free | TheBhom" />');
src = src.replace(/<meta property="og:description" content=".*?" \/>/, '<meta property="og:description" content="Extract crystal-clear 320kbps MP3 audio tracks, background music, and podcasts from any video link free online." />');
src = src.replace(/<meta property="og:url" content=".*?" \/>/, '<meta property="og:url" content="https://www.thebhom.in/downloader/video-to-mp3-converter.html" />');

const canonicalBlock = `<link rel="canonical" href="https://www.thebhom.in/downloader/video-to-mp3-converter.html" />
  <link rel="alternate" hreflang="x-default" href="https://www.thebhom.in/downloader/video-to-mp3-converter.html" />
  <link rel="alternate" hreflang="en" href="https://www.thebhom.in/downloader/video-to-mp3-converter.html" />
  <link rel="alternate" hreflang="hi" href="https://www.thebhom.in/downloader/video-to-mp3-converter.html?lang=hi" />
  <link rel="alternate" hreflang="es" href="https://www.thebhom.in/downloader/video-to-mp3-converter.html?lang=es" />
  <link rel="alternate" hreflang="pt" href="https://www.thebhom.in/downloader/video-to-mp3-converter.html?lang=pt" />
  <link rel="alternate" hreflang="id" href="https://www.thebhom.in/downloader/video-to-mp3-converter.html?lang=id" />`;
src = src.replace(/<link rel="canonical" href=".*?" \/>/, canonicalBlock);

// Replace WebApp schema
src = src.replace(/"name": "YouTube Song Downloader \(Convert Video to 320kbps MP3\)"/, '"name": "Video to MP3 Converter (Extract Audio from Any Video)"');
src = src.replace(/"url": "https:\/\/www\.thebhom\.in\/downloader\/youtube-song-downloader\.html"/, '"url": "https://www.thebhom.in/downloader/video-to-mp3-converter.html"');

// Replace Hero & Badge
src = src.replace(/<div class="badge">.*?<\/div>/, '<div class="badge" data-i18n="badge">🎧 Universal Video to MP3 Converter</div>');
src = src.replace(/<h1>.*?<\/h1>/, '<h1 data-i18n="heroTitle">Video to MP3 Converter (Extract 320kbps Audio from 40+ Sites)</h1>');
src = src.replace(/<p class="subtitle">.*?<\/p>/, '<p class="subtitle" data-i18n="heroSubtitle">Paste any video or reels URL from YouTube, Instagram, TikTok, Facebook, Twitter/X, or Reddit to extract crystal-clear 320kbps MP3 audio tracks and background music instantly.</p>');

// Add Language selector to header
src = src.replace(/<button class="hdr-theme-btn"/, '<div class="thebhom-lang-container" style="display:inline-flex;align-items:center;margin-right:4px;"></div>\n      <button class="hdr-theme-btn"');

// Add Language selector to mobNav
src = src.replace(/<a href="\/"\s*>🏠 Home<\/a>/, '<div class="thebhom-lang-container" style="padding:10px 0;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--dl-border);"><span style="font-size:0.8rem;font-weight:700;color:var(--text2);">🌐 Language:</span></div>\n    <a href="/">🏠 Home</a>');

// Tool Switcher Nav
const toolNav = `<nav class="tool-switcher-nav" aria-label="Specialized Platform Downloaders">
      <a href="/downloader/" class="tool-pill">⚡ All-in-One</a>
      <a href="/downloader/video-to-mp3-converter.html" class="tool-pill active" style="font-weight:800;">🎧 Video to MP3</a>
      <a href="/downloader/youtube-video-downloader.html" class="tool-pill">▶ YouTube Video</a>
      <a href="/downloader/youtube-shorts-downloader.html" class="tool-pill">⚡ YouTube Shorts</a>
      <a href="/downloader/youtube-song-downloader.html" class="tool-pill">🎵 YouTube Song / MP3</a>
      <a href="/downloader/instagram-reels-downloader.html" class="tool-pill">📸 Instagram Reels</a>
      <a href="/downloader/instagram-story-downloader.html" class="tool-pill">📖 Instagram Story</a>
      <a href="/downloader/tiktok-video-downloader.html" class="tool-pill">🎵 TikTok (No Watermark)</a>
      <a href="/downloader/facebook-video-downloader.html" class="tool-pill">🌐 Facebook</a>
      <a href="/downloader/twitter-video-downloader.html" class="tool-pill">🐦 Twitter / X</a>
      <a href="/downloader/pinterest-video-downloader.html" class="tool-pill">📌 Pinterest</a>
      <a href="/downloader/reddit-video-downloader.html" class="tool-pill">👾 Reddit</a>
    </nav>`;
src = src.replace(/<nav class="tool-switcher-nav" aria-label="Specialized Platform Downloaders">[\s\S]*?<\/nav>/, toolNav);

// Input Placeholder & Buttons
src = src.replace(/placeholder="Paste YouTube music or video link to extract MP3 song\.\.\."/, 'placeholder="Paste any video link (YouTube, Instagram, TikTok, Twitter...) to extract MP3 audio..." data-i18n-placeholder="inputPlaceholder"');
src = src.replace(/<span>Paste<\/span>/, '<span data-i18n="pasteBtn">Paste</span>');
src = src.replace(/<span>🔍 Analyze URL<\/span>/, '<span data-i18n="analyzeBtn">🔍 Analyze URL</span>');

// Add i18n script include
src = src.replace(/<script src="\.\.\/shared\.js\?v=20261018_v1"><\/script>/, '<script src="i18n.js?v=20261024_v1"></script>\n  <script src="../shared.js?v=20261018_v1"></script>');

fs.writeFileSync(destPath, src, 'utf8');
console.log('Successfully created ' + destPath);
