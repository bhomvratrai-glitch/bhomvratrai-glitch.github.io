const fs = require('fs');
const path = require('path');

const dir = 'downloader';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && f !== 'video-to-mp3-converter.html' && f !== 'index.html');

files.forEach(filename => {
  const filePath = path.join(dir, filename);
  let content = fs.readFileSync(filePath, 'utf8');

  // 1. Add video-to-mp3-converter.html to tool-switcher-nav if not present
  if (!content.includes('video-to-mp3-converter.html')) {
    content = content.replace(
      '<a href="/downloader/" class="tool-pill">⚡ All-in-One</a>',
      '<a href="/downloader/" class="tool-pill">⚡ All-in-One</a>\n      <a href="/downloader/video-to-mp3-converter.html" class="tool-pill" style="font-weight:800;">🎧 Video to MP3</a>'
    );
  }

  // 2. Add language container in hdr-right if not present
  if (!content.includes('thebhom-lang-container')) {
    content = content.replace(
      '<button class="hdr-theme-btn"',
      '<div class="thebhom-lang-container" style="display:inline-flex;align-items:center;margin-right:4px;"></div>\n      <button class="hdr-theme-btn"'
    );
    content = content.replace(
      /<a href="\/"\s*>🏠 Home<\/a>/,
      '<div class="thebhom-lang-container" style="padding:10px 0;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--dl-border);"><span style="font-size:0.8rem;font-weight:700;color:var(--text2);">🌐 Language:</span></div>\n    <a href="/">🏠 Home</a>'
    );
  }

  // 3. Add i18n.js script tag if not present
  if (!content.includes('i18n.js')) {
    content = content.replace(
      '<script src="../shared.js',
      '<script src="i18n.js?v=20261024_v1"></script>\n  <script src="../shared.js'
    );
  }

  fs.writeFileSync(filePath, content, 'utf8');
  console.log(`Updated ${filename}`);
});
