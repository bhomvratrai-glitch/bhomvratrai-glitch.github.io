// ============================================================
// TheBhom.in — Shared App Logic
// shared.js
// ============================================================
// Google Analytics (GA4) & Google Tag Manager (GTM)
(function initTracking() {
  const gtmId = 'GTM-K2B22XSW';
  const gaId = 'G-GHVNZWFVQV';

  // 1. Google Tag Manager
  if (!window.__gtmInitialized && !document.querySelector(`script[src*="${gtmId}"]`)) {
    window.__gtmInitialized = true;
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer',gtmId);
  }

  // 2. Google Analytics (GA4) gtag
  if (!window.__gaInitialized && !document.querySelector(`script[src*="${gaId}"]`)) {
    window.__gaInitialized = true;
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
    document.head.appendChild(script);

    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', gaId);
  }
})();

const SUBDOMAINS = [
  {
    id: "deals",
    name: "Deals",
    label: "🔥 Deals",
    url: "/deals/",
    color: "#fb641b",
    svg: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fb641b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>`
  },
  {
    id: "downloader",
    name: "Downloader",
    label: "⚡ Downloader",
    url: "/downloader/",
    color: "#0891b2",
    svg: `<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0891b2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`
  }
];

// ===== THEME MANAGER & SWITCHER =====
const THEMES = {
  light: { icon: '☀️', name: 'Light', desc: 'Clean Apple / Notion Frost White' },
  navy: { icon: '🌊', name: 'Navy', desc: 'Option 1 Midnight Ocean Slate' },
  purple: { icon: '🔮', name: 'Purple', desc: 'Option 3 Cosmic Neon Galaxy' },
  dark: { icon: '🌙', name: 'Dark', desc: 'Classic OLED Night Mode' }
};

function getStoredTheme() {
  try {
    return localStorage.getItem('thebhom_theme') || 'light';
  } catch (e) {
    return 'light';
  }
}

function setAppTheme(themeName) {
  if (!THEMES[themeName]) themeName = 'light';
  document.documentElement.setAttribute('data-theme', themeName);
  try {
    localStorage.setItem('thebhom_theme', themeName);
  } catch (e) {}

  // Update theme toggle button
  const iconEl = document.getElementById('themeCurrIcon');
  const labelEl = document.getElementById('themeCurrLabel');
  if (iconEl) iconEl.textContent = THEMES[themeName].icon;
  if (labelEl) labelEl.textContent = THEMES[themeName].name;

  // Update minimalist navbar theme button
  updateThemeIcon(themeName);

  // Update menu active states
  document.querySelectorAll('.theme-opt').forEach(opt => {
    if (opt.getAttribute('data-theme') === themeName) {
      opt.classList.add('active');
    } else {
      opt.classList.remove('active');
    }
  });

  // Update mobile pills
  document.querySelectorAll('.mob-theme-pill').forEach(pill => {
    if (pill.getAttribute('data-theme') === themeName) {
      pill.classList.add('active');
    } else {
      pill.classList.remove('active');
    }
  });

  // Close menu if open
  const menu = document.getElementById('themeMenu');
  if (menu) menu.classList.remove('open');
}

function updateThemeIcon(themeName) {
  const btn = document.getElementById('hdrThemeBtn');
  if (!btn) return;
  const isDark = (themeName === 'dark' || themeName === 'navy' || themeName === 'purple');
  if (isDark) {
    btn.innerHTML = `<svg class="theme-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>`;
    btn.setAttribute('title', 'Switch to Light Mode');
    btn.setAttribute('aria-label', 'Switch to Light Mode');
  } else {
    btn.innerHTML = `<svg class="theme-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>`;
    btn.setAttribute('title', 'Switch to Dark Mode');
    btn.setAttribute('aria-label', 'Switch to Dark Mode');
  }
}

function quickToggleTheme() {
  const curr = getStoredTheme();
  const next = (curr === 'light') ? 'dark' : 'light';
  setAppTheme(next);
}

function toggleThemeMenu(e) {
  if (e) e.stopPropagation();
  const menu = document.getElementById('themeMenu');
  if (menu) menu.classList.toggle('open');
}

function getThemeSwitcherHTML() {
  return '';
}

function injectThemeSwitcherIfNeeded() {
  const existing = document.getElementById('themeSwitcher');
  if (existing) existing.remove();
}

function initTheme() {
  setAppTheme(getStoredTheme());
  const existing = document.getElementById('themeSwitcher');
  if (existing) existing.remove();
}

function getBasePath() {
  const p = window.location.pathname;
  if (p.includes('/deals/') || p.includes('/downloader/')) {
    return '../';
  }
  return '';
}

// ===== RENDER HEADER =====
function renderHeader(activePage=''){
  const base = getBasePath();
  const currentTheme = getStoredTheme();
  const isDark = (currentTheme === 'dark' || currentTheme === 'navy' || currentTheme === 'purple');
  const themeSvg = isDark
    ? `<svg class="theme-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"></path></svg>`
    : `<svg class="theme-icon-svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"></path></svg>`;

  return `
<div class="scroll-prog" id="sp"></div>
<header class="hdr">
  <a href="/" class="logo" title="TheBhom — Home">
    <div class="logo-box" style="background:linear-gradient(135deg, #e11d48, #be123c);border-radius:11px;color:#fff;font-weight:900;">TB</div>
    <span class="logo-txt">The<span class="brand-accent" style="color:#e11d48;">Bhom</span></span>
  </a>
  <nav class="hdr-nav-container">
    <ul class="hdr-nav">
      <li><a href="/deals/" class="hdr-nav-link ${activePage==='deals'?'active':''}" title="TheBhom Deals"><span class="hdr-nav-ic" style="color:#f59e0b;"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z"/><circle cx="7" cy="7" r="1.5"/></svg></span><span class="hdr-nav-txt" style="color:#f59e0b;font-weight:700;">Deals</span></a></li>
      <li><a href="/downloader/" class="hdr-nav-link ${activePage==='downloader'?'active':''}" title="Universal Video Downloader"><span class="hdr-nav-ic" style="color:#0891b2;"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#0891b2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg></span><span class="hdr-nav-txt" style="color:#0891b2;font-weight:700;">Downloader</span></a></li>
    </ul>
  </nav>
  <div class="hdr-right">
    <div class="hdr-search-pill" onclick="openSpotlight()" role="button" tabindex="0" title="Search (⌘K)">
      <svg class="hdr-search-ic" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8"></circle>
        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
      </svg>
      <span class="hdr-search-txt">Search...</span>
      <kbd class="hdr-search-kbd">⌘K</kbd>
    </div>
    <button class="hdr-theme-btn" id="hdrThemeBtn" onclick="quickToggleTheme()" title="Toggle Theme" aria-label="Toggle Theme">
      ${themeSvg}
    </button>
    ${getHdrUserSnippet('/')}
    <button class="ham" id="hamBtn" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>
<nav class="mob-nav" id="mobNav">
  <div class="mob-theme-row">
    <span style="font-size:0.8rem;font-weight:700;color:var(--text2);margin-right:6px;">🎨 Theme:</span>
    <button class="mob-theme-pill" data-theme="light" onclick="setAppTheme('light')">☀️ Light</button>
    <button class="mob-theme-pill" data-theme="navy" onclick="setAppTheme('navy')">🌊 Navy</button>
    <button class="mob-theme-pill" data-theme="purple" onclick="setAppTheme('purple')">🔮 Purple</button>
    <button class="mob-theme-pill" data-theme="dark" onclick="setAppTheme('dark')">🌙 Dark</button>
  </div>
  <a href="/">🏠 Home</a>
  <a href="/deals/" style="color:#f59e0b;font-weight:700;">🔥 Deals</a>
  <a href="/downloader/" style="color:#0891b2;font-weight:700;">⚡ Downloader</a>
  <a href="/about">ℹ️ About Us</a>
  <a href="/contact">📞 Contact</a>
  <a href="#" onclick="openSpotlight();return false;" style="color:#2563eb;font-weight:700;">🔍 Search (Cmd+K)</a>
</nav>
`;
}

// ===== DYNAMIC USER HEADER & AUTH MODAL =====
function getHdrUserSnippet(base) {
  try {
    const rawUser = localStorage.getItem('thebhom_user');
    const u = rawUser ? JSON.parse(rawUser) : null;
    if (u && u.email) {
      const uName = u.name || u.email.split('@')[0] || 'User';
      const initial = (uName[0] || 'U').toUpperCase();
      const uPlan = u.plan || 'FREE';
      const isPending = u.status === 'pending';
      const badgeText = isPending ? '⏳ PENDING' : (uPlan === 'BUSINESS' ? '👑 BUSINESS' : (uPlan === 'PRO' ? '⚡ PRO' : '🌱 FREE'));
      const badgeBg = isPending ? '#fef3c7' : (uPlan === 'BUSINESS' ? '#f3e8ff' : (uPlan === 'PRO' ? '#dbeafe' : '#f3f4f6'));
      const badgeColor = isPending ? '#b45309' : (uPlan === 'BUSINESS' ? '#7e22ce' : (uPlan === 'PRO' ? '#2563eb' : '#4b5563'));

      return `
    <div class="hdr-user-pill" id="userPillBtn" onclick="toggleUserDropdown(event)" role="button" tabindex="0" title="${uName} (${uPlan})" style="position:relative;">
      <div class="hdr-user-avatar" style="background:#2563eb;color:#fff;">${initial}</div>
      <span class="hdr-user-name">${uName}</span>
      <div class="user-menu-dropdown" id="userMenuDropdown" style="display:none;position:absolute;top:44px;right:0;width:230px;background:#fff;border:1px solid #e5e7eb;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,0.12);z-index:9999;padding:12px;text-align:left;">
        <div style="padding-bottom:8px;margin-bottom:8px;border-bottom:1px solid #e5e7eb;">
          <div style="font-weight:800;font-size:0.92rem;color:#111827;">${uName}</div>
          <div style="font-size:0.75rem;color:#6b7280;word-break:break-all;">${u.email}</div>
          <span style="display:inline-block;margin-top:6px;background:${badgeBg};color:${badgeColor};padding:2px 8px;border-radius:999px;font-size:0.7rem;font-weight:800;">${badgeText}</span>
        </div>
        <a href="${base}dashboard.html" style="display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:8px;font-size:0.85rem;color:#374151;text-decoration:none;font-weight:600;" onmouseover="this.style.background='#f3f4f6'" onmouseout="this.style.background='transparent'">📊 Dashboard</a>
        <a href="${base}pricing.html" style="display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:8px;font-size:0.85rem;color:#2563eb;text-decoration:none;font-weight:600;" onmouseover="this.style.background='#eff6ff'" onmouseout="this.style.background='transparent'">⚡ Plans & Pricing</a>
        <a href="#" onclick="logoutTheBhomUser();return false;" style="display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:8px;font-size:0.85rem;color:#dc2626;text-decoration:none;font-weight:600;" onmouseover="this.style.background='#fef2f2'" onmouseout="this.style.background='transparent'">↪ Logout</a>
      </div>
    </div>`;
    }
  } catch(e){}

  return `
    <button class="hdr-user-pill" onclick="openAuthModal()" style="background:#2563eb;color:#fff;border:none;padding:7px 15px;border-radius:999px;font-weight:700;font-size:0.83rem;display:inline-flex;align-items:center;gap:6px;cursor:pointer;box-shadow:0 2px 8px rgba(37,99,235,0.25);transition:all 0.2s;" onmouseover="this.style.background='#1d4ed8'" onmouseout="this.style.background='#2563eb'">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      Sign In
    </button>`;
}

// User dropdown toggle
function toggleUserDropdown(e) {
  if (e) e.stopPropagation();
  const d = document.getElementById('userMenuDropdown');
  if (d) {
    d.style.display = (d.style.display === 'none' || !d.style.display) ? 'block' : 'none';
  }
}
document.addEventListener('click', () => {
  const d = document.getElementById('userMenuDropdown');
  if (d) d.style.display = 'none';
});

function openAuthModal(mode = 'login') {
  let modal = document.getElementById('authModalOverlay');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'authModalOverlay';
    modal.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.65);backdrop-filter:blur(6px);z-index:99999;display:flex;align-items:center;justify-content:center;padding:16px;opacity:0;transition:opacity 0.2s ease;';
    modal.innerHTML = `
      <div style="background:var(--card, #ffffff);border:1px solid rgba(229,231,235,0.8);border-radius:20px;max-width:400px;width:100%;padding:26px;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);position:relative;" onclick="event.stopPropagation()">
        <button onclick="closeAuthModal()" style="position:absolute;top:14px;right:14px;background:none;border:none;font-size:18px;color:#6b7280;cursor:pointer;line-height:1;padding:4px 8px;border-radius:6px;" title="Close">✕</button>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
          <div style="width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg, #e11d48, #be123c);color:#fff;display:grid;place-items:center;font-weight:900;font-size:16px;">TB</div>
          <div>
            <h3 style="margin:0;font-size:1.15rem;font-weight:800;color:var(--text, #111827);">TheBhom Account</h3>
            <p style="margin:2px 0 0;font-size:0.8rem;color:#6b7280;">Sign in to sync your tools & Pro plan</p>
          </div>
        </div>

        <div style="display:flex;background:#f3f4f6;padding:4px;border-radius:10px;margin-bottom:16px;">
          <button id="tabLogin" onclick="switchAuthTab('login')" style="flex:1;border:none;background:#fff;color:#111827;padding:8px;border-radius:8px;font-weight:700;font-size:0.85rem;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,0.1);">Sign In</button>
          <button id="tabSignup" onclick="switchAuthTab('signup')" style="flex:1;border:none;background:transparent;color:#6b7280;padding:8px;border-radius:8px;font-weight:700;font-size:0.85rem;cursor:pointer;">Create Account</button>
        </div>

        <form id="authForm" onsubmit="submitAuthForm(event)" style="display:flex;flex-direction:column;gap:12px;">
          <div id="nameFieldGroup" style="display:none;">
            <label style="display:block;font-size:0.8rem;font-weight:700;color:#374151;margin-bottom:4px;">Full Name</label>
            <input type="text" id="authNameInput" placeholder="Your Name" style="width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #d1d5db;border-radius:8px;font-size:0.9rem;outline:none;" />
          </div>

          <div>
            <label style="display:block;font-size:0.8rem;font-weight:700;color:#374151;margin-bottom:4px;">Email Address <span style="color:#e5322d;">*</span></label>
            <input type="email" id="authEmailInput" required placeholder="you@example.com" style="width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #d1d5db;border-radius:8px;font-size:0.9rem;outline:none;" />
          </div>

          <button type="submit" id="authSubmitBtn" style="background:#2563eb;color:#fff;border:none;padding:11px;border-radius:10px;font-weight:800;font-size:0.9rem;cursor:pointer;transition:all 0.2s;display:flex;align-items:center;justify-content:center;gap:8px;margin-top:4px;">
            <span>Sign In</span>
          </button>
        </form>

        <div style="margin-top:14px;text-align:center;border-top:1px solid #f3f4f6;padding-top:12px;">
          <button onclick="closeAuthModal()" style="background:none;border:none;color:#6b7280;font-size:0.8rem;cursor:pointer;text-decoration:underline;">Continue as Guest (Free Mode)</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    modal.addEventListener('click', closeAuthModal);
  }

  modal.style.display = 'flex';
  requestAnimationFrame(() => modal.style.opacity = '1');
  switchAuthTab(mode);
}

function closeAuthModal() {
  const modal = document.getElementById('authModalOverlay');
  if (modal) {
    modal.style.opacity = '0';
    setTimeout(() => modal.style.display = 'none', 200);
  }
}

function switchAuthTab(mode) {
  const isSignup = mode === 'signup';
  const nameGroup = document.getElementById('nameFieldGroup');
  const submitBtn = document.getElementById('authSubmitBtn');
  const tabLogin = document.getElementById('tabLogin');
  const tabSignup = document.getElementById('tabSignup');

  if (nameGroup) nameGroup.style.display = isSignup ? 'block' : 'none';
  if (submitBtn) submitBtn.querySelector('span').textContent = isSignup ? 'Create Free Account' : 'Sign In';
  if (tabLogin && tabSignup) {
    tabLogin.style.background = isSignup ? 'transparent' : '#fff';
    tabLogin.style.color = isSignup ? '#6b7280' : '#111827';
    tabLogin.style.boxShadow = isSignup ? 'none' : '0 1px 3px rgba(0,0,0,0.1)';
    tabSignup.style.background = isSignup ? '#fff' : 'transparent';
    tabSignup.style.color = isSignup ? '#111827' : '#6b7280';
    tabSignup.style.boxShadow = isSignup ? '0 1px 3px rgba(0,0,0,0.1)' : 'none';
  }
}

async function submitAuthForm(e) {
  e.preventDefault();
  const emailInput = document.getElementById('authEmailInput');
  const nameInput = document.getElementById('authNameInput');
  const submitBtn = document.getElementById('authSubmitBtn');

  const email = emailInput ? emailInput.value.trim().toLowerCase() : '';
  const name = (nameInput && nameInput.value.trim()) || (email ? email.split('@')[0] : 'User');

  if (!email || !email.includes('@')) {
    alert('Please enter a valid email address.');
    return;
  }

  submitBtn.disabled = true;
  submitBtn.innerHTML = '<span class="spinner" style="width:14px;height:14px;border-width:2px;"></span> Verifying...';

  let plan = 'FREE';
  let status = 'active';
  let licenseKey = null;

  try {
    const res = await fetch(`/api/orders?email=${encodeURIComponent(email)}`);
    if (res.ok) {
      const data = await res.json();
      if (data && data.found && data.order) {
        const ord = data.order;
        if (ord.isApproved) {
          plan = (ord.productName || ord.productId || 'PRO').toUpperCase().includes('BUSINESS') ? 'BUSINESS' : 'PRO';
          status = 'approved';
          licenseKey = ord.licenseKey;
        } else if (ord.status === 'PENDING') {
          plan = (ord.productName || ord.productId || 'PRO').toUpperCase().includes('BUSINESS') ? 'BUSINESS' : 'PRO';
          status = 'pending';
        }
      }
    }
  } catch(err) {}

  const userData = {
    name: name,
    email: email,
    plan: plan,
    status: status,
    licenseKey: licenseKey,
    loginAt: Date.now()
  };

  localStorage.setItem('thebhom_user', JSON.stringify(userData));

  if (typeof showToast === 'function') {
    showToast(`Signed in as ${name} (${plan} Plan)`, 'ok');
  }

  closeAuthModal();
  setTimeout(() => location.reload(), 300);
}

function logoutTheBhomUser() {
  localStorage.removeItem('thebhom_user');
  if (typeof showToast === 'function') {
    showToast('Logged out successfully', 'ok');
  }
  setTimeout(() => location.reload(), 300);
}

// ===== RENDER FOOTER =====
function renderFooter(){
  return `
<div class="div" style="border-top:1px solid #e5e7eb;"></div>
<footer class="footer" style="background:#f9fafb;border-top:1px solid #e5e7eb;padding:3.5rem 2rem 2rem;color:#4b5563;">
  <div class="footer-inner" style="max-width:1200px;margin:0 auto;">
    <div class="footer-grid" style="display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;margin-bottom:2.5rem;">
      
      <div class="f-col">
        <h5 style="font-size:0.88rem;font-weight:800;color:#111827;margin-bottom:1rem;text-transform:none;letter-spacing:0;">Image Tools</h5>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:0.6rem;">
          <li><a href="/tools/compress-image" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Compress Image</a></li>
          <li><a href="/tools/resize-image-online" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Resize Image</a></li>
          <li><a href="/tools/convert-jpg-to-webp" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Convert JPG to WebP</a></li>
          <li><a href="/tools/convert-png-to-jpg" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Convert PNG to JPG</a></li>
        </ul>
      </div>

      <div class="f-col">
        <h5 style="font-size:0.88rem;font-weight:800;color:#111827;margin-bottom:1rem;text-transform:none;letter-spacing:0;">PDF Tools</h5>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:0.6rem;">
          <li><a href="/tools/merge-pdf" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Merge PDF</a></li>
          <li><a href="/tools/split-pdf-pages" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Split PDF</a></li>
          <li><a href="/tools/rotate-pdf" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Rotate PDF</a></li>
          <li><a href="/tools/watermark-pdf" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Watermark PDF</a></li>
          <li><a href="/tools/pdf-to-image" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">PDF to Image</a></li>
        </ul>
      </div>

      <div class="f-col">
        <h5 style="font-size:0.88rem;font-weight:800;color:#111827;margin-bottom:1rem;text-transform:none;letter-spacing:0;">Digital Resources</h5>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:0.6rem;">
          <li><a href="/wallpapers" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">4K AMOLED Wallpapers</a></li>
          <li><a href="/ebooks" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Free E-Books Library</a></li>
          <li><a href="/magazines" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Digital Magazines</a></li>
          <li><a href="/templates" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Design Templates</a></li>
          <li><a href="/cards" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Greeting Cards</a></li>
          <li><a href="/deals/" style="color:#f59e0b;font-weight:700;text-decoration:none;font-size:0.88rem;">🔥 Deals & Loot Offers</a></li>
          <li><a href="/news/" style="color:#ea580c;font-weight:700;text-decoration:none;font-size:0.88rem;">📰 News & Viral Stories</a></li>
          <li><a href="/downloader/" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Video Downloader</a></li>
        </ul>
      </div>

      <div class="f-col">
        <h5 style="font-size:0.88rem;font-weight:800;color:#111827;margin-bottom:1rem;text-transform:none;letter-spacing:0;">Company & Policy</h5>
        <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:0.6rem;">
          <li><a href="/articles/" style="color:#0284c7;font-weight:700;text-decoration:none;font-size:0.88rem;">📚 Articles & Guides</a></li>
          <li><a href="/about" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">About Us</a></li>
          <li><a href="/contact" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Contact Us</a></li>
          <li><a href="/privacy-policy" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Privacy Policy</a></li>
          <li><a href="/terms" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Terms of Service</a></li>
          <li><a href="/disclaimer" style="color:#4b5563;text-decoration:none;font-size:0.88rem;">Disclaimer</a></li>
        </ul>
      </div>

    </div>

    <div class="footer-bottom" style="border-top:1px solid #e5e7eb;padding-top:1.5rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:0.85rem;color:#6b7280;">
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:28px;height:28px;border-radius:8px;background:linear-gradient(135deg, #e11d48, #be123c);color:#fff;display:grid;place-items:center;font-weight:900;font-size:0.85rem;">TB</div>
        <span style="font-weight:700;color:#111827;">TheBhom</span>
      </div>
      <div>&copy; ${new Date().getFullYear()} TheBhom. All rights reserved. Free Educational & Digital Utilities Hub.</div>
      <div style="font-size:0.8rem;color:#9ca3af;">🔒 Client-side browser processing. Files are never stored on external servers.</div>
    </div>
  </div>
</footer>
<div class="toast-box" id="toastBox"></div>
<button class="b2t" id="b2t" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑</button>
`;
}

// ===== PWA PROMPT & SERVICE WORKER =====
let deferredPwaPrompt = null;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPwaPrompt = e;
  const btn = document.getElementById('pwaInstallBtn');
  if (btn) btn.style.display = 'inline-flex';
});

async function triggerAppInstall() {
  if (deferredPwaPrompt) {
    deferredPwaPrompt.prompt();
    const { outcome } = await deferredPwaPrompt.userChoice;
    if (outcome === 'accepted') {
      showToast('🎉 TheBhom App Install हो रहा है!', 'ok');
    }
    deferredPwaPrompt = null;
    const btn = document.getElementById('pwaInstallBtn');
    if (btn) btn.style.display = 'none';
  } else {
    showToast('💡 Chrome Browser Menu (⋮) में जाकर "Add to Home screen" / "Install app" पर टैप करें।', 'ok');
  }
}
window.triggerAppInstall = triggerAppInstall;
window.promptPwaInstall = triggerAppInstall;

// Register Service Worker with cache invalidation check
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').then(reg => {
      console.log('TheBhom SW registered with scope:', reg.scope);
      if (typeof reg.update === 'function') {
        try { reg.update().catch(() => {}); } catch (e) {}
      }
    }).catch(err => {
      console.debug('TheBhom SW registration:', err ? (err.message || err) : 'offline');
    });

    // Automatically bust old caches if SW version updated
    if (!sessionStorage.getItem('thebhom_sw_v6')) {
      sessionStorage.setItem('thebhom_sw_v6', '1');
      if ('caches' in window) {
        caches.keys().then(keys => {
          keys.forEach(k => {
            if (k !== 'thebhom-v2026-v6') {
              caches.delete(k);
            }
          });
        });
      }
    }
  });
}

// Ensure Head PWA meta tags
(function ensurePwaMeta(){
  if(!document.querySelector('link[rel="manifest"]')){
    const m = document.createElement('link');
    m.rel = 'manifest';
    m.href = 'manifest.json';
    document.head.appendChild(m);
  }
  if(!document.querySelector('meta[name="theme-color"]')){
    const tc = document.createElement('meta');
    tc.name = 'theme-color';
    tc.content = '#7c3aed';
    document.head.appendChild(tc);
  }
  if(!document.querySelector('link[rel="apple-touch-icon"]')){
    const ti = document.createElement('link');
    ti.rel = 'apple-touch-icon';
    ti.href = 'icon-192.png';
    document.head.appendChild(ti);
  }
})();

// ===== UNIVERSAL FAVORITES SYSTEM =====
window.getFavorites = function() {
  try { return JSON.parse(localStorage.getItem('thebhom_favs') || '[]'); }
  catch(e) { return []; }
};

function isFavorite(id) {
  return window.getFavorites().some(f => f.id === id);
}
window.isFavorite = isFavorite;

function toggleFavorite(item, e) {
  if (e) {
    if (typeof e.stopPropagation === 'function') e.stopPropagation();
    if (typeof e.preventDefault === 'function') e.preventDefault();
  }
  let favs = window.getFavorites();
  const exists = favs.some(f => f.id === item.id);
  if (exists) {
    favs = favs.filter(f => f.id !== item.id);
    showToast(`💔 "${item.title}" saved list से हटा दिया गया`, 'info');
  } else {
    const pageUrl = item.url || (item.id.startsWith('w')?'wallpapers.html':item.id.startsWith('b')?'ebooks.html':item.id.startsWith('m')?'magazines.html':item.id.startsWith('t')?'templates.html':'cards.html') + '#' + item.id;
    favs.unshift({
      id: item.id,
      title: item.title,
      tag: item.tag || item.sub || item.category || 'General',
      emoji: item.emoji || item.preview || '⭐',
      category: item.category || item.type || (item.id.startsWith('w')?'Wallpapers':item.id.startsWith('b')?'E-Books':item.id.startsWith('m')?'Magazines':item.id.startsWith('t')?'Templates':'Cards'),
      url: pageUrl
    });
    showToast(`❤️ "${item.title}" Saved Items में जुड़ गया!`, 'ok');
  }
  localStorage.setItem('thebhom_favs', JSON.stringify(favs));
  window.updateFavBadges();

  // If e was a button element, toggle its active class
  if (e && e.classList) {
    e.classList.toggle('active', !exists);
  }

  // Update heart buttons and pin buttons on current page
  document.querySelectorAll(`.fav-btn-${item.id}`).forEach(b => {
    b.classList.toggle('active', !exists);
  });
  document.querySelectorAll(`.pin-save-btn[data-id="${item.id}"]`).forEach(b => {
    b.classList.toggle('saved', !exists);
    b.innerHTML = !exists ? '✅ Saved' : '📌 Save';
  });
  if (document.getElementById('favDrawer')?.classList.contains('open')) {
    window.renderFavDrawerBody();
  }
}
window.toggleFavorite = toggleFavorite;

window.updateFavBadges = function() {
  const count = window.getFavorites().length;
  document.querySelectorAll('.fav-count-badge').forEach(b => {
    b.textContent = count;
  });
};

window.openFavDrawer = function() {
  window.renderFavDrawer();
  const d = document.getElementById('favDrawer');
  const o = document.getElementById('favOverlay');
  if (d && o) {
    window.renderFavDrawerBody();
    d.classList.add('open');
    o.classList.add('open');
  }
};

window.closeFavDrawer = function() {
  const d = document.getElementById('favDrawer');
  const o = document.getElementById('favOverlay');
  if (d) d.classList.remove('open');
  if (o) o.classList.remove('open');
};

window.renderFavDrawer = function() {
  if (document.getElementById('favDrawer')) return;
  const mount = document.createElement('div');
  mount.innerHTML = `
    <div class="fav-overlay" id="favOverlay" onclick="closeFavDrawer()"></div>
    <div class="fav-drawer" id="favDrawer">
      <div class="fav-header">
        <h3>❤️ My Saved Items (<span class="fav-count-badge">0</span>)</h3>
        <button class="fav-close" onclick="closeFavDrawer()">✕</button>
      </div>
      <div class="fav-body" id="favBody"></div>
      <div class="fav-vip-box">
        <div class="fav-vip-info">
          <h5>⚡ TheBhom VIP & Support</h5>
          <p>Scan & pay via Paytm UPI for VIP perks</p>
        </div>
        <button class="fav-vip-pay-btn" onclick="openUpiPaymentModal({title:'TheBhom VIP Supporter', amount:99, desc:'VIP Supporter Plan: Ad-free perks & high-speed downloads'})">Pay ₹99 ⚡</button>
      </div>
      <div style="margin:10px 16px 14px 16px;padding:10px 14px;background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);border-radius:12px;display:flex;align-items:center;justify-content:space-between;">
        <div style="font-size:0.78rem;color:#cbd5e1;">👑 <strong>Owner Portal</strong> (bhomvratrai7225)</div>
        <a href="/admin/" style="font-size:0.75rem;font-weight:800;color:#fbbf24;text-decoration:none;padding:4px 10px;background:rgba(245,158,11,0.2);border-radius:6px;border:1px solid rgba(245,158,11,0.4);">Dashboard →</a>
      </div>
    </div>
  `;
  document.body.appendChild(mount);
};

window.renderFavDrawerBody = function() {
  const body = document.getElementById('favBody');
  if (!body) return;
  const favs = window.getFavorites();
  if (favs.length === 0) {
    body.innerHTML = `
      <div class="fav-empty">
        <div class="fav-empty-icon">📂</div>
        <h4>कोई Saved Item नहीं है</h4>
        <p style="font-size:0.83rem;margin-top:0.5rem;">किसी भी Wallpaper, E-Book, Magazine या Card पर ❤️ दबाकर यहाँ सेव करें।</p>
      </div>
    `;
    return;
  }
  body.innerHTML = favs.map(item => `
    <div class="fav-card">
      <div class="fav-thumb" style="background:#1e1e38;">${item.emoji}</div>
      <div class="fav-info">
        <div class="fav-name" title="${item.title}">${item.title}</div>
        <div class="fav-sub">${item.category} • ${item.tag}</div>
      </div>
      <div class="fav-act">
        <a href="${item.url}" class="fav-act-btn" target="_self">Open ↗</a>
        <button class="fav-rm-btn" onclick="toggleFavorite({id:'${item.id}',title:'${item.title.replace(/'/g,"\\'")}'})" title="Remove">✕</button>
      </div>
    </div>
  `).join('');
};

function renderSubnav(activePage='') {
  return `
<nav class="subnav">
  <a href="/deals/" class="${activePage==='deals'?'here':''}">🔥 Deals</a>
  <a href="/downloader/" class="${activePage==='downloader'?'here':''}">⚡ Downloader</a>
</nav>
`;
}

function upgradeHeaderToNewNav() {
  if (window.location.pathname.includes('/deals/')) {
    // In deals, the native .ecommerce-header is used; strip any legacy duplicate header or subnav
    const legacyHdr = document.querySelector('header.hdr');
    if (legacyHdr) legacyHdr.remove();
    const legacyMob = document.getElementById('mobNav') || document.querySelector('.mob-nav');
    if (legacyMob) legacyMob.remove();
    const legacySub = document.querySelector('nav.subnav');
    if (legacySub) legacySub.remove();
    return;
  }

  const existingHdr = document.querySelector('header.hdr');

  let activePage = window.PAGE_ACTIVE_ID || '';
  if (!activePage) {
    const path = window.location.pathname.toLowerCase();
    if (path.includes('downloader')) activePage = 'downloader';
    else if (path.includes('deals')) activePage = 'deals';
  }

  // Upgrade header if missing downloader or has obsolete sections
  if (existingHdr && (!existingHdr.querySelector('a[href="/downloader/"]') || existingHdr.querySelector('a[href="/tools/"]') || existingHdr.querySelector('a[href="/imgpdf/"]') || existingHdr.querySelector('a[href="/wallpapers"]') || existingHdr.querySelector('a[href="/ebooks"]') || existingHdr.querySelector('a[href="/articles/"]'))) {
    const container = document.createElement('div');
    container.innerHTML = renderHeader(activePage);
    const newHdr = container.querySelector('header.hdr');
    const newMobNav = container.querySelector('.mob-nav');

    if (newHdr) {
      existingHdr.replaceWith(newHdr);
      const oldMobNav = document.getElementById('mobNav') || document.querySelector('.mob-nav');
      if (oldMobNav) {
        if (newMobNav) oldMobNav.replaceWith(newMobNav);
      } else if (newMobNav) {
        newHdr.after(newMobNav);
      }
    }
    updateThemeIcon(getStoredTheme());
  } else if (!existingHdr && !document.getElementById('shared-header') && document.body && !document.querySelector('.no-shared-hdr')) {
    const container = document.createElement('div');
    container.innerHTML = renderHeader(activePage);
    const newHdr = container.querySelector('header.hdr');
    const newMobNav = container.querySelector('.mob-nav');
    if (newHdr) {
      document.body.prepend(newHdr);
      if (newMobNav) newHdr.after(newMobNav);
      updateThemeIcon(getStoredTheme());
    }
  }

  // Mount into #shared-header placeholder if present
  const sharedHdrPlaceholder = document.getElementById('shared-header');
  if (sharedHdrPlaceholder && !sharedHdrPlaceholder.querySelector('header.hdr')) {
    sharedHdrPlaceholder.innerHTML = renderHeader(activePage) + renderSubnav(activePage);
    updateThemeIcon(getStoredTheme());
  }

  // Mount into #shared-footer placeholder if present
  const sharedFtrPlaceholder = document.getElementById('shared-footer');
  if (sharedFtrPlaceholder && !sharedFtrPlaceholder.innerHTML.trim()) {
    sharedFtrPlaceholder.innerHTML = renderFooter();
  }

  // Upgrade subnav pills across any page
  const existingSubnav = document.querySelector('nav.subnav');
  if (existingSubnav) {
    existingSubnav.outerHTML = renderSubnav(activePage);
  } else if (!document.querySelector('.no-shared-subnav') && !document.getElementById('shared-header')) {
    const hdrEl = document.querySelector('header.hdr');
    if (hdrEl) {
      const mobNavEl = document.getElementById('mobNav') || document.querySelector('.mob-nav');
      const target = mobNavEl || hdrEl;
      target.insertAdjacentHTML('afterend', renderSubnav(activePage));
    }
  }
}

// ===== INIT SHARED =====
function initShared(){
  // Force purge legacy service worker caches
  if ('serviceWorker' in navigator && window.caches) {
    caches.keys().then(keys => {
      keys.forEach(k => {
        if (k !== 'thebhom-cache-v3') caches.delete(k);
      });
    });
  }

  // Init Theme System
  initTheme();

  // Upgrade header to screenshot-matching navbar across any page
  upgradeHeaderToNewNav();

  // Mount favorites drawer & update badges
  window.renderFavDrawer();
  window.updateFavBadges();

  // Floating saved button
  if (!document.getElementById('favFloatBtn')) {
    const fb = document.createElement('button');
    fb.id = 'favFloatBtn';
    fb.className = 'fav-btn-float';
    fb.innerHTML = `❤️ Saved <span class="fav-badge fav-count-badge">0</span>`;
    fb.onclick = window.openFavDrawer;
    document.body.appendChild(fb);
    window.updateFavBadges();
  }

  // Floating Spotlight shortcut button on mobile/desktop
  if (!document.getElementById('spotlightFloatBtn')) {
    const sb = document.createElement('button');
    sb.id = 'spotlightFloatBtn';
    sb.style.cssText = 'position:fixed;bottom:20px;right:90px;z-index:9990;background:#111128;border:1px solid rgba(124,58,237,0.5);color:#c084fc;font-weight:700;border-radius:50px;padding:8px 16px;cursor:pointer;font-size:.78rem;box-shadow:0 8px 24px rgba(0,0,0,0.6);display:flex;align-items:center;gap:6px;';
    sb.innerHTML = `🔍 Search <kbd style="background:rgba(0,0,0,0.4);padding:1px 5px;border-radius:4px;font-size:.65rem;border:1px solid rgba(255,255,255,0.2);">⌘K</kbd>`;
    sb.onclick = window.openSpotlight;
    document.body.appendChild(sb);
  }

  // Init features
  initSpotlight();
  initActivityTicker();
  initQuoteHighlighter();
  applyLanguage(currentLang);

  // Check if install button should show
  if (deferredPwaPrompt) {
    const btn = document.getElementById('pwaInstallBtn');
    if (btn) btn.style.display = 'inline-flex';
  }

  // Scroll effects
  const sp=document.getElementById('sp');
  const b2t=document.getElementById('b2t');
  window.addEventListener('scroll',()=>{
    const pct=(window.scrollY/(document.documentElement.scrollHeight-window.innerHeight))*100;
    if(sp)sp.style.width=pct+'%';
    if(b2t)b2t.classList.toggle('show',window.scrollY>350);
  });

  // Hamburger
  const hamBtn=document.getElementById('hamBtn');
  const mobNav=document.getElementById('mobNav');
  hamBtn?.addEventListener('click',()=>{
    if(mobNav) mobNav.classList.toggle('open');
    const spans=hamBtn.querySelectorAll('span');
    if(mobNav && mobNav.classList.contains('open')){
      spans[0].style.transform='rotate(45deg) translate(5px,5px)';
      spans[1].style.opacity='0';
      spans[2].style.transform='rotate(-45deg) translate(5px,-5px)';
    } else {
      spans.forEach(s=>{s.style.transform='';s.style.opacity='';});
    }
  });

  // Intersection observer for cards
  if (typeof IntersectionObserver !== 'undefined') {
    const io=new IntersectionObserver(entries=>{
      entries.forEach(e=>{
        if(e.isIntersecting){
          e.target.style.opacity='1';
          e.target.style.transform='translateY(0)';
        }
      });
    },{threshold:0.05});
    document.querySelectorAll('.c-card,.hub-card').forEach(el=>{
      el.style.opacity='0';
      el.style.transform='translateY(20px)';
      el.style.transition='opacity .5s ease, transform .5s ease';
      io.observe(el);
    });
  }
}

// ===== TOAST =====
function showToast(msg, type='ok'){
  let box=document.getElementById('toastBox');
  if(!box){
    box = document.createElement('div');
    box.id = 'toastBox';
    box.className = 'toast-box';
    document.body.appendChild(box);
  }
  const t=document.createElement('div');
  t.className=`toast ${type}`;
  t.innerHTML=msg;
  box.appendChild(t);
  requestAnimationFrame(()=>setTimeout(()=>t.classList.add('in'),30));
  setTimeout(()=>{t.classList.remove('in');setTimeout(()=>t.remove(),400);},3500);
}

// ===== CONTENT CARD BUILDER =====
function buildCard(item, downloadFn){
  const [c1,c2]=item.colors||['#0a0a1a','#1a0a2a'];
  const qBadge=window.THEBHOM.getQualityBadge(item.quality);
  const newBadge=item.isNew?'<span class="newbadge">NEW</span>':'';
  const dlCount=window.THEBHOM.formatNum(item.downloads);
  const isFav = window.isFavorite(item.id);
  const safeItemStr = JSON.stringify({id:item.id,title:item.title,emoji:item.emoji,tag:item.tag||item.sub||''}).replace(/"/g,'&quot;');

  return `
<div class="c-card" id="card-${item.id}">
  <div class="c-thumb" style="background:linear-gradient(135deg,${c1},${c2})">
    <button class="fav-heart-btn fav-btn-${item.id} ${isFav?'active':''}" onclick="toggleFavorite(${safeItemStr}, event)" title="Save to Favorites">❤️</button>
    <span class="big-emoji">${item.emoji}</span>
    <span class="sub-label">${item.sub||item.tag}</span>
    ${qBadge}${newBadge}
    <div class="c-overlay">
      <button class="dl-btn" onclick="${downloadFn}('${item.id}')">⬇️ Free Download</button>
    </div>
  </div>
  <div class="c-info">
    <div class="c-title" title="${item.title}">${item.title}</div>
    <div class="c-meta">
      <span>${item.tag}</span>
      <span>⬇️ ${dlCount}</span>
    </div>
  </div>
</div>`;
}

// ===== BULLETPROOF FILE DOWNLOADER =====
function triggerBrowserDownload(blobOrUrl, filename) {
  // GA4 Event Tracking
  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'file_download', {
        file_name: filename || 'unknown',
        link_url: typeof blobOrUrl === 'string' ? blobOrUrl : 'direct_blob',
        page_location: window.location.href
      });
    }
  } catch(e) {}

  const a = document.createElement('a');
  a.style.display = 'none';
  let url = '';
  let isBlob = false;
  
  if (typeof blobOrUrl === 'string') {
    url = blobOrUrl;
  } else if (blobOrUrl instanceof Blob) {
    url = URL.createObjectURL(blobOrUrl);
    isBlob = true;
  }
  
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  
  const evt = new MouseEvent('click', {
    view: window,
    bubbles: true,
    cancelable: true
  });
  a.dispatchEvent(evt);
  
  setTimeout(() => {
    if (a.parentNode) a.parentNode.removeChild(a);
    if (isBlob) {
      URL.revokeObjectURL(url);
    }
  }, 4000);
}

// ===== DOWNLOAD HANDLER =====
function handleDownload(id, type){
  // GA4 Event Tracking
  try {
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'file_download', {
        file_name: id,
        file_extension: type || 'pdf',
        page_location: window.location.href
      });
    }
  } catch(e) {}

  showToast(`✅ "${id}" download हो रही है...`,'ok');
  // Simulate download tracking
  setTimeout(()=>showToast(`🎉 Download complete! Share करें TheBhom.in`,'ok'),2000);
}

// ===== SEARCH & FILTER ENGINE =====
function createContentPage(config){
  const {data, pageId, title, subtitle, emoji, filterTags, downloadFn='handleDownload'} = config;
  let filtered=[...data];
  let activeTag='all';
  let sortBy='popular';
  let searchQ='';
  let page=1;
  const PER_PAGE=20;

  function getFiltered(){
    let d=[...data];
    if(activeTag!=='all')d=d.filter(i=>i.tag===activeTag||i.sub===activeTag);
    if(searchQ)d=d.filter(i=>i.title.toLowerCase().includes(searchQ.toLowerCase())||i.tag.toLowerCase().includes(searchQ.toLowerCase()));
    if(sortBy==='newest')d=[...d.filter(i=>i.isNew),...d.filter(i=>!i.isNew)];
    else if(sortBy==='downloads')d.sort((a,b)=>b.downloads-a.downloads);
    else if(sortBy==='rating')d.sort((a,b)=>b.rating-a.rating);
    return d;
  }

  function render(){
    filtered=getFiltered();
    const slice=filtered.slice(0,(page)*PER_PAGE);
    const grid=document.getElementById('mainGrid');
    if(!grid)return;
    grid.innerHTML=slice.map(item=>buildCard(item,downloadFn)).join('');
    document.getElementById('resCount').textContent=`${filtered.length} items मिले`;
    const lmBtn=document.getElementById('lmBtn');
    if(lmBtn)lmBtn.style.display=filtered.length>slice.length?'inline-flex':'none';
    initShared();
  }

  window.setFilter=function(tag,btn){
    activeTag=tag;
    page=1;
    document.querySelectorAll('.f-btn').forEach(b=>b.classList.remove('on'));
    btn.classList.add('on');
    render();
  };
  window.setSort=function(val){sortBy=val;page=1;render();};
  window.loadMore=function(){page++;render();};
  window.doSearch=function(){
    searchQ=document.getElementById('srchInput')?.value.trim()||'';
    page=1;
    render();
    try {
      if (searchQ && typeof window.gtag === 'function') {
        window.gtag('event', 'search', { search_term: searchQ, page_location: window.location.href });
      }
    } catch(e) {}
  };

  // Build filter buttons
  const filterHTML=['all',...filterTags].map((t,i)=>
    `<button class="f-btn${i===0?' on':''}" onclick="setFilter('${t}',this)">${t==='all'?'🔥 All':t}</button>`
  ).join('');

  return {filterHTML, render};
}

// ============================================================
// GLOBAL SPOTLIGHT OMNISEARCH (Cmd+K / Ctrl+K)
// ============================================================
let spotlightActiveIndex = 0;
let spotlightActiveCategory = 'all';

function getAllContentItems() {
  return [
    { id: 'tool-deals', title: 'TheBhom Deals — Handpicked Daily Loot Deals & Price Drops', cat: 'deals', tag: 'Deals Store', emoji: '🔥', url: '/deals/' },
    { id: 'tool-downloader', title: 'Universal Video Downloader & Trimmer (1080p Full HD & MP3)', cat: 'downloader', tag: 'Downloader', emoji: '⚡', url: '/downloader/' },
    { id: 'tool-amazon', title: 'Amazon Top Discounts & Lightning Deals', cat: 'deals', tag: 'Amazon', emoji: '📦', url: '/deals/?store=amazon' },
    { id: 'tool-flipkart', title: 'Flipkart Big Savings & Flash Offers', cat: 'deals', tag: 'Flipkart', emoji: '🛍️', url: '/deals/?store=flipkart' },
    { id: 'tool-myntra', title: 'Myntra Fashion, Clothing & Footwear Deals', cat: 'deals', tag: 'Myntra', emoji: '👗', url: '/deals/?store=myntra' }
  ];
}

function openSpotlightItem(url, id, cat) {
  closeSpotlight();
  const isInSubdir = window.location.pathname.includes('/tools/') || window.location.pathname.includes('/downloader/') || window.location.pathname.includes('/directory/');
  let targetUrl = url;
  if (!targetUrl.startsWith('/') && !targetUrl.startsWith('http')) {
    targetUrl = isInSubdir ? '../' + targetUrl : targetUrl;
  }
  window.location.href = targetUrl;
}

window.addEventListener('hashchange', () => {
  const hash = window.location.hash.replace('#', '');
  if (!hash) return;
  if (typeof openAmazonBookModal === 'function' && hash.startsWith('b')) {
    openAmazonBookModal(hash);
  } else if (typeof openPreview === 'function' && (hash.startsWith('w') || hash.startsWith('lw') || hash.startsWith('u'))) {
    openPreview(hash);
  } else if (typeof openMagReader === 'function' && hash.startsWith('m')) {
    openMagReader(hash);
  } else if (typeof openCardZoom === 'function' && hash.startsWith('c')) {
    openCardZoom(hash);
  } else if (typeof openZoom === 'function' && hash.startsWith('t')) {
    openZoom(hash);
  }
});

function initSpotlight() {
  // Global key listener active
}

function openSpotlight() {
  let overlay = document.getElementById('spotlightOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'spotlight-overlay';
    overlay.id = 'spotlightOverlay';
    overlay.innerHTML = `
      <div class="spotlight-modal" onclick="event.stopPropagation()">
        <div class="spotlight-top">
          <span class="spotlight-icon">🔍</span>
          <input type="text" id="spotlightInput" class="spotlight-input" placeholder="Search 1,750+ Wallpapers, E-Books, Magazines, Templates, Cards..." autocomplete="off" />
          <span class="spotlight-esc" onclick="closeSpotlight()">ESC</span>
        </div>
        <div class="spotlight-filter-bar">
          <button class="spotlight-chip active" onclick="setSpotlightCat('all', this)">🔥 All Items</button>
          <button class="spotlight-chip" onclick="setSpotlightCat('tools', this)">🛠️ Tools & Downloader</button>
          <button class="spotlight-chip" onclick="setSpotlightCat('wallpapers', this)">🖼️ Wallpapers</button>
          <button class="spotlight-chip" onclick="setSpotlightCat('ebooks', this)">📚 E-Books</button>
          <button class="spotlight-chip" onclick="setSpotlightCat('magazines', this)">📰 Magazines</button>
          <button class="spotlight-chip" onclick="setSpotlightCat('templates', this)">🎨 Templates</button>
          <button class="spotlight-chip" onclick="setSpotlightCat('cards', this)">💌 Cards</button>
        </div>
        <div class="spotlight-results" id="spotlightResults"></div>
        <div class="spotlight-footer">
          <div class="spotlight-kbd-hints">
            <span>↑↓ Navigate</span>
            <span>↵ Open</span>
            <span>Esc Close</span>
          </div>
          <span style="color:#a855f7;font-weight:700;">TheBhom Omnisearch</span>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    overlay.addEventListener('click', closeSpotlight);

    const input = document.getElementById('spotlightInput');
    let spotlightSearchTimer = null;
    input.addEventListener('input', () => {
      spotlightActiveIndex = 0;
      renderSpotlightResults();
      clearTimeout(spotlightSearchTimer);
      spotlightSearchTimer = setTimeout(() => {
        const q = input.value.trim();
        if (q.length >= 2 && typeof window.gtag === 'function') {
          window.gtag('event', 'search', { search_term: q, event_label: 'omnisearch' });
        }
      }, 700);
    });
    input.addEventListener('keydown', (e) => {
      const resultsEl = document.getElementById('spotlightResults');
      const items = resultsEl.querySelectorAll('.spotlight-item');
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (items.length) {
          spotlightActiveIndex = (spotlightActiveIndex + 1) % items.length;
          updateSpotlightFocus(items);
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (items.length) {
          spotlightActiveIndex = (spotlightActiveIndex - 1 + items.length) % items.length;
          updateSpotlightFocus(items);
        }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (items[spotlightActiveIndex]) items[spotlightActiveIndex].click();
      } else if (e.key === 'Escape') {
        closeSpotlight();
      }
    });
  }

  overlay.classList.add('open');
  const input = document.getElementById('spotlightInput');
  input.value = '';
  spotlightActiveIndex = 0;
  renderSpotlightResults();
  setTimeout(() => input.focus(), 60);
}

function closeSpotlight() {
  const overlay = document.getElementById('spotlightOverlay');
  if (overlay) overlay.classList.remove('open');
}

function setSpotlightCat(cat, btn) {
  spotlightActiveCategory = cat;
  document.querySelectorAll('.spotlight-chip').forEach(c => c.classList.remove('active'));
  if (btn) btn.classList.add('active');
  spotlightActiveIndex = 0;
  renderSpotlightResults();
}

function renderSpotlightResults() {
  const input = document.getElementById('spotlightInput');
  const query = (input?.value || '').trim().toLowerCase();
  const resultsEl = document.getElementById('spotlightResults');
  if (!resultsEl) return;

  let all = getAllContentItems();
  if (spotlightActiveCategory !== 'all') {
    all = all.filter(item => item.cat === spotlightActiveCategory);
  }
  if (query) {
    all = all.filter(item => item.title.toLowerCase().includes(query) || (item.tag && item.tag.toLowerCase().includes(query)));
  }

  const topItems = all.slice(0, 16);
  if (topItems.length === 0) {
    resultsEl.innerHTML = `<div class="spotlight-empty">🔍 "${query}" के लिए कोई आइटम नहीं मिला। कृपया अलग नाम खोजें।</div>`;
    return;
  }

  resultsEl.innerHTML = topItems.map((item, idx) => `
    <a href="${item.url}" class="spotlight-item${idx === spotlightActiveIndex ? ' focused' : ''}" onclick="openSpotlightItem('${item.url}','${item.id}','${item.cat}'); return false;">
      <span class="spotlight-item-emoji">${item.emoji}</span>
      <span class="spotlight-item-title">${item.title}</span>
      <span class="spotlight-item-badge">${item.cat}</span>
      <span class="spotlight-item-arrow">➔</span>
    </a>
  `).join('');
}

function updateSpotlightFocus(items) {
  items.forEach((item, idx) => {
    item.classList.toggle('focused', idx === spotlightActiveIndex);
    if (idx === spotlightActiveIndex) item.scrollIntoView({ block: 'nearest' });
  });
}

document.addEventListener('keydown', (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
    e.preventDefault();
    openSpotlight();
  }
  if (e.key === 'Escape') closeSpotlight();
});

// ============================================================
// SCAN-TO-MOBILE QR CODE GENERATOR
// ============================================================
function openQRModal(url, title) {
  let overlay = document.getElementById('qrOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'qr-overlay';
    overlay.id = 'qrOverlay';
    document.body.appendChild(overlay);
  }
  const fullUrl = url.startsWith('http') ? url : (window.location.origin + '/' + url);
  const qrImgUrl = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&margin=8&data=${encodeURIComponent(fullUrl)}`;

  overlay.innerHTML = `
    <div class="qr-modal" onclick="event.stopPropagation()">
      <button class="qr-close" onclick="closeQRModal()">✕</button>
      <div style="font-size:2.2rem;margin-bottom:.3rem;">📱</div>
      <div class="qr-title">Scan on Mobile</div>
      <div class="qr-desc">${title || 'Open on your smartphone instantly'}</div>
      <div class="qr-box">
        <img src="${qrImgUrl}" alt="QR Code" width="190" height="190" style="display:block;border-radius:8px;" />
      </div>
      <div style="font-size:0.75rem;color:#94a3b8;line-height:1.5;">
        अपने फोन के कैमरा या Google Lens से स्कैन करें और 1-टैप में मोबाइल पर डाउनलोड करें!
      </div>
    </div>
  `;
  overlay.onclick = closeQRModal;
  overlay.classList.add('open');
}

function closeQRModal() {
  const overlay = document.getElementById('qrOverlay');
  if (overlay) overlay.classList.remove('open');
}

// ============================================================
// UNIVERSAL PAYTM / UPI PAYMENT MODAL
// ============================================================
function openUpiPaymentModal(opts = {}) {
  const options = typeof opts === 'string' ? { title: opts } : (opts || {});
  const title = options.title || 'ToolNest PRO / Digital Product';
  const amount = options.amount || 99;
  const desc = options.desc || 'Pay via Paytm, PhonePe, GPay or Any UPI App';

  let overlay = document.getElementById('upiPayOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'upi-overlay';
    overlay.id = 'upiPayOverlay';
    document.body.appendChild(overlay);
  }

  const upiId = '7987761789@ptyes';
  const payeeName = 'TheBhom';
  const note = (title.length > 28 ? title.slice(0, 25) + '...' : title).replace(/[^\w\s]/gi, '');
  const upiIntentUrl = `upi://pay?pa=${upiId}&pn=${encodeURIComponent(payeeName)}&am=${amount}&cu=INR&tn=${encodeURIComponent(note)}`;
  const waMsg = `Hi TheBhom, I have completed the UPI payment of ₹${amount} for "${title}".\nUPI ID: ${upiId}\n\nPlease verify and activate my access!`;
  const waLink = `https://wa.me/917987761789?text=${encodeURIComponent(waMsg)}`;
  
  // Resolve image source: checks if inside /tools/ or root
  let qrSrc = '/assets/upi-qr.png?v=20260914_qr2';
  if (window.location.pathname.includes('/tools/')) {
    qrSrc = 'upi-qr.png?v=20260914_qr2';
  }

  overlay.innerHTML = `
    <div class="upi-modal" onclick="event.stopPropagation()">
      <button class="upi-close-btn" onclick="closeUpiPaymentModal()" title="Close">✕</button>
      
      <div class="upi-header">
        <div class="upi-badge">⚡ Instant UPI / QR Payment</div>
        <h3 class="upi-title">${title}</h3>
        <div class="upi-amount-pill">Amount to Pay: <span class="upi-amount-num">₹${amount}</span></div>
      </div>

      <div class="upi-qr-card">
        <div class="upi-apps-strip">
          <span>Paytm</span> • <span>Google Pay</span> • <span>PhonePe</span> • <span>BHIM</span> • <span>Cred</span>
        </div>
        <div class="upi-qr-frame">
          <img src="${qrSrc}" alt="Paytm UPI QR Code" class="upi-qr-image" onerror="if(this.src.indexOf('/assets/')===-1)this.src='/assets/upi-qr.png?v=20260914_qr2';"/>
        </div>
        <div class="upi-merchant-badge">
          <span class="upi-verified-tick">✓</span> Verified Merchant: <strong>TheBhom / Bhom Vrat Rai</strong>
        </div>
      </div>

      <div class="upi-id-row">
        <div class="upi-id-label">UPI ID:</div>
        <div class="upi-id-val" id="upiIdVal">${upiId}</div>
        <button class="upi-copy-btn" id="upiCopyBtn" onclick="copyUpiId('${upiId}')" title="Copy UPI ID">
          <span>📋 Copy</span>
        </button>
      </div>

      <div class="upi-actions">
        <a href="${upiIntentUrl}" class="upi-app-btn">
          <span>📱</span> Pay directly in Any UPI App
        </a>
        <a href="${waLink}" target="_blank" rel="noopener" class="upi-whatsapp-btn">
          <span>💬</span> Send Screenshot / UTR on WhatsApp
        </a>
      </div>

      <div class="upi-utr-section">
        <div class="upi-utr-title">Enter Payment Details for Instant Verification:</div>
        <div style="display:flex;flex-direction:column;gap:8px;margin-top:8px;">
          <input type="email" id="upiEmailInput" placeholder="Your Email Address (for delivery)" required style="background:#fff;border:1px solid #cbd5e1;border-radius:8px;color:#0f172a;padding:9px 12px;font-size:0.84rem;outline:none;" />
          <input type="text" id="upiNameInput" placeholder="Your Name (Optional)" style="background:#fff;border:1px solid #cbd5e1;border-radius:8px;color:#0f172a;padding:9px 12px;font-size:0.84rem;outline:none;" />
          <div class="upi-utr-box">
            <input type="text" id="upiUtrInput" placeholder="12-digit UTR / Ref Number" maxlength="30" style="flex:1;" />
            <button onclick="submitUpiVerification('${title.replace(/'/g, "\\'")}', ${amount})" class="upi-verify-btn" id="upiSubmitBtn">Confirm</button>
          </div>
        </div>
        <div class="upi-footer-note">🔒 100% Secure Direct UPI Transfer. Instant verification & delivery.</div>
      </div>
    </div>
  `;

  overlay.onclick = closeUpiPaymentModal;
  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeUpiPaymentModal() {
  if (window._upiPollTimer) {
    clearInterval(window._upiPollTimer);
    window._upiPollTimer = null;
  }
  const overlay = document.getElementById('upiPayOverlay');
  if (overlay) overlay.classList.remove('open');
  document.body.style.overflow = '';
}

function copyUpiId(id) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(id).then(() => {
      const btn = document.getElementById('upiCopyBtn');
      if (btn) {
        btn.innerHTML = '<span>✓ Copied!</span>';
        btn.style.background = '#16a34a';
        setTimeout(() => {
          btn.innerHTML = '<span>📋 Copy</span>';
          btn.style.background = '#0284c7';
        }, 2500);
      }
      if (typeof showToast === 'function') {
        showToast('✓ UPI ID Copied: ' + id, 'ok');
      }
    }).catch(() => fallbackCopy(id));
  } else {
    fallbackCopy(id);
  }
}

function fallbackCopy(text) {
  const t = document.createElement('textarea');
  t.value = text;
  document.body.appendChild(t);
  t.select();
  try {
    document.execCommand('copy');
    if (typeof showToast === 'function') showToast('✓ UPI ID Copied: ' + text, 'ok');
  } catch(e){}
  document.body.removeChild(t);
}

async function submitUpiVerification(title, amount) {
  const utrInp = document.getElementById('upiUtrInput');
  const emailInp = document.getElementById('upiEmailInput');
  const nameInp = document.getElementById('upiNameInput');
  const btn = document.getElementById('upiSubmitBtn');

  const utr = (utrInp ? utrInp.value.trim() : '');
  const email = (emailInp ? emailInp.value.trim() : '');
  const name = (nameInp ? nameInp.value.trim() : '');

  if (!email || !email.includes('@')) {
    if (typeof showToast === 'function') showToast('⚠️ Please enter a valid email address', 'warn');
    if (emailInp) emailInp.focus();
    return;
  }

  if (!utr || utr.length < 6) {
    if (typeof showToast === 'function') showToast('⚠️ Please enter valid 12-digit UTR number', 'warn');
    if (utrInp) utrInp.focus();
    return;
  }

  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Submitting...';
  }

  try {
    const res = await fetch('/api/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userName: name || 'Customer',
        userEmail: email,
        productName: title,
        amount: amount,
        utrNumber: utr
      })
    });

    const data = await res.json();
    if (!res.ok || !data.success) {
      if (typeof showToast === 'function') showToast('⚠️ ' + (data.error || 'Failed to submit payment details'), 'warn');
      if (btn) {
        btn.disabled = false;
        btn.textContent = 'Confirm';
      }
      return;
    }

    const orderId = data.orderId;
    if (typeof showToast === 'function') showToast('🎉 Payment submitted! Order #' + orderId, 'ok');

    // Render Live Verification Screen inside modal
    const modalBox = document.querySelector('.upi-modal');
    if (modalBox) {
      modalBox.innerHTML = `
        <button class="upi-close-btn" onclick="closeUpiPaymentModal()" title="Close">✕</button>
        <div style="text-align:center;padding:10px 0;">
          <div style="font-size:2.8rem;margin-bottom:8px;animation:spin 2s linear infinite;" id="statusIcon">⏳</div>
          <h3 style="font-size:1.3rem;font-weight:900;color:#0f172a;margin-bottom:6px;" id="statusHeading">Verifying Your Payment</h3>
          <div style="background:#f1f5f9;border:1px solid #e2e8f0;border-radius:10px;padding:8px 14px;font-size:0.85rem;color:#0f172a;font-family:monospace;display:inline-block;margin-bottom:12px;">
            Order ID: <strong>#${orderId}</strong>
          </div>
          <p style="font-size:0.85rem;color:#475569;line-height:1.5;margin-bottom:14px;" id="statusMsg">
            We are verifying UTR <strong>${utr}</strong> for <strong>₹${amount}</strong>.<br>
            Please keep this tab open. As soon as the owner approves, your plan will unlock right here automatically!
          </p>
          <div id="unlockContainer" style="display:none;margin-top:14px;"></div>
          <div style="font-size:0.75rem;color:#64748b;margin-top:10px;">
            Live Auto-Checking every 3 seconds...
          </div>
        </div>
      `;
    }

    // Start Polling for Approval
    if (window._upiPollTimer) clearInterval(window._upiPollTimer);
    window._upiPollTimer = setInterval(async () => {
      try {
        const checkRes = await fetch('/api/orders?id=' + encodeURIComponent(orderId));
        const checkData = await checkRes.json();
        if (checkData.found && checkData.order && checkData.order.isApproved) {
          clearInterval(window._upiPollTimer);
          window._upiPollTimer = null;

          // Save unlocked plan locally
          try {
            const unlocked = JSON.parse(localStorage.getItem('thebhom_unlocked_plans') || '[]');
            unlocked.push({ id: orderId, product: title, key: checkData.order.licenseKey, date: new Date().toISOString() });
            localStorage.setItem('thebhom_unlocked_plans', JSON.stringify(unlocked));
          } catch(e){}

          // Update UI to Approved
          const icon = document.getElementById('statusIcon');
          const heading = document.getElementById('statusHeading');
          const msg = document.getElementById('statusMsg');
          const unlockBox = document.getElementById('unlockContainer');

          if (icon) {
            icon.textContent = '🎉';
            icon.style.animation = '';
          }
          if (heading) {
            heading.textContent = 'Payment Approved & Unlocked!';
            heading.style.color = '#059669';
          }
          if (msg) {
            msg.innerHTML = `Congratulations <strong>${name || email}</strong>! Your access is now activated.<br>License Key: <strong style="font-family:monospace;color:#059669;background:#ecfdf3;padding:3px 8px;border-radius:6px;border:1px solid #a7f3d0;">${checkData.order.licenseKey}</strong>`;
          }
          if (unlockBox) {
            unlockBox.style.display = 'block';
            unlockBox.innerHTML = `
              <div style="background:#ecfdf3;border:1px solid #a7f3d0;border-radius:14px;padding:12px;margin-bottom:12px;">
                <div style="font-weight:800;color:#065f46;font-size:0.95rem;">✓ Access Granted: ${title}</div>
                <div style="font-size:0.8rem;color:#047857;margin-top:4px;">Downloads and premium perks unlocked for this device!</div>
              </div>
              <button class="btn primary" onclick="closeUpiPaymentModal();if(typeof showToast==='function')showToast('✓ All features unlocked!','ok');" style="width:100%;padding:12px;font-weight:800;background:#e11d48;border:none;border-radius:10px;color:#fff;cursor:pointer;">
                ⚡ Start Using Now
              </button>
            `;
          }
          if (typeof showToast === 'function') showToast('🎉 Order #' + orderId + ' approved by owner!', 'ok');
        }
      } catch(e){}
    }, 3500);

  } catch (err) {
    if (typeof showToast === 'function') showToast('⚠️ Error: ' + err.message, 'warn');
    if (btn) {
      btn.disabled = false;
      btn.textContent = 'Confirm';
    }
  }
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeUpiPaymentModal();
  }
});


// ============================================================
// SOCIAL PROOF LIVE ACTIVITY TICKER
// ============================================================
const TICKER_ACTIVITIES = [
  { city: 'Mumbai', action: '4K Cyberpunk Tokyo Wallpaper', type: 'downloaded 📱' },
  { city: 'Delhi', action: 'Autonomous AI Agents 2026', type: 'started reading 📚' },
  { city: 'Bengaluru', action: 'Instagram Carousel Masterpack', type: 'customized 🎨' },
  { city: 'Jaipur', action: 'Royal Gold Anniversary Card', type: 'personalized 💌' },
  { city: 'Pune', action: 'Solopreneur 2026 Blueprint', type: 'downloaded PDF 📚' },
  { city: 'Hyderabad', action: '4K Cosmic Nebula Wallpaper', type: 'saved to Favorites ❤️' },
  { city: 'Ahmedabad', action: 'TechVision AI Magazine', type: 'read full issue 📰' },
  { city: 'Kolkata', action: 'Minimalist Business Card Pack', type: 'exported 🎨' },
  { city: 'Chandigarh', action: 'Heartfelt Rose Foldable Card', type: 'shared on WhatsApp 💬' }
];

function initActivityTicker() {
  if (document.getElementById('activityTicker')) return;
  const ticker = document.createElement('div');
  ticker.className = 'activity-ticker';
  ticker.id = 'activityTicker';
  ticker.innerHTML = `
    <div class="ticker-avatar">⚡</div>
    <div class="ticker-content">
      <div class="ticker-title" id="tickerTitle">Someone from Mumbai</div>
      <div class="ticker-meta" id="tickerMeta">Downloaded 4K Wallpaper • Just now</div>
    </div>
    <button class="ticker-close" onclick="this.parentElement.classList.remove('show')">✕</button>
  `;
  document.body.appendChild(ticker);

  let idx = 0;
  function showNextTicker() {
    const act = TICKER_ACTIVITIES[idx % TICKER_ACTIVITIES.length];
    idx++;
    const tTitle = document.getElementById('tickerTitle');
    const tMeta = document.getElementById('tickerMeta');
    if (tTitle && tMeta) {
      tTitle.textContent = `Someone from ${act.city}`;
      tMeta.textContent = `${act.type} "${act.action}" • Just now`;
    }
    ticker.classList.add('show');
    setTimeout(() => {
      ticker.classList.remove('show');
    }, 5500);
  }

  setTimeout(showNextTicker, 6000);
  setInterval(showNextTicker, 30000);
}

// ============================================================
// SMART QUOTE HIGHLIGHTER TOOLTIP
// ============================================================
function initQuoteHighlighter() {
  let tooltip = document.getElementById('quoteTooltip');
  if (!tooltip) {
    tooltip = document.createElement('div');
    tooltip.className = 'quote-tooltip';
    tooltip.id = 'quoteTooltip';
    tooltip.innerHTML = `
      <button class="quote-tooltip-btn" onclick="copySelectedQuote()">📋 Copy Quote</button>
      <button class="quote-tooltip-btn" onclick="shareSelectedQuote()">💬 WhatsApp</button>
    `;
    document.body.appendChild(tooltip);
  }

  document.addEventListener('selectionchange', () => {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) {
      tooltip.style.display = 'none';
      return;
    }
    const text = sel.toString().trim();
    if (text.length < 15) {
      tooltip.style.display = 'none';
      return;
    }
    const range = sel.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    if (rect.width === 0 && rect.height === 0) return;

    tooltip.style.display = 'inline-flex';
    tooltip.style.top = `${window.scrollY + rect.top - 42}px`;
    tooltip.style.left = `${window.scrollX + rect.left + (rect.width / 2) - 80}px`;
  });
}

function copySelectedQuote() {
  const sel = window.getSelection();
  if (!sel) return;
  const text = sel.toString().trim();
  const quoteWithCitation = `"${text}"\n\n— Via TheBhom.in (Free Digital Library)\nhttps://www.thebhom.in`;
  navigator.clipboard.writeText(quoteWithCitation).then(() => {
    showToast('📋 Quote source ke sath copy ho gaya!', 'ok');
    const t = document.getElementById('quoteTooltip');
    if (t) t.style.display = 'none';
  });
}

function shareSelectedQuote() {
  const sel = window.getSelection();
  if (!sel) return;
  const text = sel.toString().trim();
  const quoteWithCitation = `"${text}"\n\n— Via TheBhom.in (Free Digital Library)\nhttps://www.thebhom.in`;
  window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(quoteWithCitation)}`);
  const t = document.getElementById('quoteTooltip');
  if (t) t.style.display = 'none';
}

// ============================================================
// ROMANTIC BGM WEB AUDIO SYNTHESIZER (CARDS)
// ============================================================
let bgmAudioCtx = null;
let bgmInterval = null;
let isBgmPlaying = false;

function toggleRomanticBGM(btn) {
  if (isBgmPlaying) {
    stopRomanticBGM(btn);
  } else {
    playRomanticBGM(btn);
  }
}

function playRomanticBGM(btn) {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) {
      showToast('⚠️ Web Audio not supported in this browser', 'info');
      return;
    }
    if (!bgmAudioCtx) bgmAudioCtx = new AudioCtx();
    if (bgmAudioCtx.state === 'suspended') bgmAudioCtx.resume();

    isBgmPlaying = true;
    if (btn) {
      btn.classList.add('playing');
      btn.innerHTML = '<span class="bgm-icon">🎵</span> Music Playing (Stop)';
    }
    showToast('🎵 Soft Romantic BGM चालू हो गया है...', 'ok');

    const notes = [
      [261.63, 329.63, 392.00, 493.88],
      [220.00, 261.63, 329.63, 440.00],
      [174.61, 220.00, 261.63, 349.23],
      [196.00, 261.63, 293.66, 392.00]
    ];

    let chordIdx = 0;
    function playChordTone() {
      if (!isBgmPlaying || !bgmAudioCtx) return;
      const currentChord = notes[chordIdx % notes.length];
      const now = bgmAudioCtx.currentTime;

      currentChord.forEach((freq, i) => {
        const osc = bgmAudioCtx.createOscillator();
        const gain = bgmAudioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + i * 0.35);

        gain.gain.setValueAtTime(0.001, now + i * 0.35);
        gain.gain.exponentialRampToValueAtTime(0.05, now + i * 0.35 + 0.1);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + i * 0.35 + 1.8);

        osc.connect(gain);
        gain.connect(bgmAudioCtx.destination);
        osc.start(now + i * 0.35);
        osc.stop(now + i * 0.35 + 2.0);
      });

      chordIdx++;
    }

    playChordTone();
    bgmInterval = setInterval(playChordTone, 3200);
  } catch (e) {
    console.warn('Web Audio BGM error:', e);
  }
}

function stopRomanticBGM(btn) {
  isBgmPlaying = false;
  if (bgmInterval) clearInterval(bgmInterval);
  if (btn) {
    btn.classList.remove('playing');
    btn.innerHTML = '<span class="bgm-icon">🎵</span> Romantic Music Play करें';
  }
  showToast('⏹️ Romantic Music Stopped', 'info');
}

// ============================================================
// MULTI-LANGUAGE PREFERENCE (EN / HI)
// ============================================================
let currentLang = localStorage.getItem('thebhom_lang') || 'hi';

const I18N_DICT = {
  hi: {
    langBtn: '🇮🇳 हिन्दी',
    freeBand: '🎉 TheBhom.in पर सभी Content 100% FREE है — बिना किसी plan या credit card के Download करें!',
    savedBtn: '❤️ सेव्ड',
    searchBtn: '🔍 खोजें',
    searchPlaceholder: '1,750+ Wallpapers, E-Books, Magazines, Templates, Cards खोजें...',
    loadMore: 'और लोड करें'
  },
  en: {
    langBtn: '🌐 English',
    freeBand: '🎉 All Content on TheBhom.in is 100% FREE — Download without any plan or credit card!',
    savedBtn: '❤️ Saved',
    searchBtn: '🔍 Search',
    searchPlaceholder: 'Search 1,750+ Wallpapers, E-Books, Magazines, Templates, Cards...',
    loadMore: 'Load More'
  }
};

function toggleLanguage() {
  currentLang = currentLang === 'hi' ? 'en' : 'hi';
  localStorage.setItem('thebhom_lang', currentLang);
  applyLanguage(currentLang);
  showToast(`🌐 Language switched to ${currentLang === 'hi' ? 'हिन्दी (Hindi)' : 'English'}`, 'ok');
}

function applyLanguage(lang) {
  const dict = I18N_DICT[lang] || I18N_DICT.hi;
  const btn = document.getElementById('langToggleBtn');
  if (btn) btn.innerHTML = dict.langBtn;

  const freeBands = document.querySelectorAll('.free-band, .free-banner');
  freeBands.forEach(b => { b.textContent = dict.freeBand; });

  const spotlightInp = document.getElementById('spotlightInput');
  if (spotlightInp) spotlightInp.placeholder = dict.searchPlaceholder;
}

// Universal WhatsApp Status & Story Sharing
function shareToWhatsAppStatus(title, url) {
  const fullUrl = url.startsWith('http') ? url : (window.location.origin + '/' + url);
  const text = `✨ Check out "${title}" on TheBhom.in — 100% Free Downloads without watermark!\n👉 ${fullUrl}`;
  window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`);
  showToast('💬 WhatsApp Status share window open ho gaya!', 'ok');
}

// ============================================================
// 3D REALISTIC BOOK & MAGAZINE COVER GENERATORS
// ============================================================
const _bookCoverCache = new Map();
const _magCoverCache = new Map();

function generateBookCover(b, w = 380, h = 560) {
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d');

  const [c1, c2] = (b.gradient && b.gradient.length >= 2) ? b.gradient : (b.colors && b.colors.length >= 2 ? b.colors : ['#0f172a', '#1e3a8a']);

  // 1. Deep Hardcover Base Gradient
  const bgGrd = ctx.createLinearGradient(0, 0, w, h);
  bgGrd.addColorStop(0, c1);
  bgGrd.addColorStop(0.55, c2);
  bgGrd.addColorStop(1, '#05070e');
  ctx.fillStyle = bgGrd;
  ctx.fillRect(0, 0, w, h);

  // 2. Fine Leatherette / Canvas Grain Texture
  ctx.save();
  ctx.globalAlpha = 0.07;
  for (let i = 0; i < 45; i++) {
    const x = ((i * 67) % w);
    const y = ((i * 89) % h);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(x, y, (i % 3) + 1, (i % 3) + 1);
  }
  ctx.restore();

  // 3. Gilded Gold Double Border Frame
  ctx.save();
  ctx.strokeStyle = 'rgba(245, 158, 11, 0.45)';
  ctx.lineWidth = 1.5;
  ctx.strokeRect(18, 18, w - 36, h - 36);

  ctx.strokeStyle = 'rgba(245, 158, 11, 0.22)';
  ctx.lineWidth = 1;
  ctx.strokeRect(24, 24, w - 48, h - 48);

  // Corner Gold Florets / Diamonds
  const drawDiamond = (cx, cy, size = 4) => {
    ctx.fillStyle = '#f59e0b';
    ctx.beginPath();
    ctx.moveTo(cx, cy - size);
    ctx.lineTo(cx + size, cy);
    ctx.lineTo(cx, cy + size);
    ctx.lineTo(cx - size, cy);
    ctx.closePath();
    ctx.fill();
  };
  drawDiamond(24, 24);
  drawDiamond(w - 24, 24);
  drawDiamond(24, h - 24);
  drawDiamond(w - 24, h - 24);
  ctx.restore();

  // 4. Top Bestseller / Collector Gold Ribbon
  ctx.save();
  ctx.fillStyle = 'rgba(15, 23, 42, 0.88)';
  const ribbonW = w - 68;
  const ribbonH = 26;
  const ribbonX = 34;
  const ribbonY = 34;
  ctx.fillRect(ribbonX, ribbonY, ribbonW, ribbonH);
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 1;
  ctx.strokeRect(ribbonX, ribbonY, ribbonW, ribbonH);

  ctx.fillStyle = '#f59e0b';
  ctx.font = 'bold 9px Inter, sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('★ NATIONAL BESTSELLER • 2026 EDITION ★', w / 2, ribbonY + (ribbonH / 2));
  ctx.restore();

  // 5. Central 3D Thematic Emblem / Medallion
  const cx = w / 2;
  const cy = h * 0.38;
  const r = 58;

  ctx.save();
  // Ambient radial glow behind emblem
  const glow = ctx.createRadialGradient(cx, cy, 10, cx, cy, r * 2.2);
  glow.addColorStop(0, 'rgba(245, 158, 11, 0.38)');
  glow.addColorStop(0.5, 'rgba(99, 102, 241, 0.22)');
  glow.addColorStop(1, 'transparent');
  ctx.fillStyle = glow;
  ctx.fillRect(0, cy - r * 2, w, r * 4);

  // Outer Gold Foil Embossed Ring
  ctx.beginPath();
  ctx.arc(cx, cy, r + 4, 0, Math.PI * 2);
  const goldRing = ctx.createLinearGradient(cx - r, cy - r, cx + r, cy + r);
  goldRing.addColorStop(0, '#fef08a');
  goldRing.addColorStop(0.5, '#eab308');
  goldRing.addColorStop(1, '#78350f');
  ctx.strokeStyle = goldRing;
  ctx.lineWidth = 3;
  ctx.shadowColor = 'rgba(0,0,0,0.6)';
  ctx.shadowBlur = 12;
  ctx.stroke();

  // Inner Dark Medallion
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  const innerGrd = ctx.createRadialGradient(cx - 15, cy - 15, 5, cx, cy, r);
  innerGrd.addColorStop(0, '#1e293b');
  innerGrd.addColorStop(1, '#090d16');
  ctx.fillStyle = innerGrd;
  ctx.fill();

  // Medallion inner decorative dashed ring
  ctx.beginPath();
  ctx.arc(cx, cy, r - 6, 0, Math.PI * 2);
  ctx.strokeStyle = 'rgba(245, 158, 11, 0.4)';
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 3]);
  ctx.stroke();
  ctx.setLineDash([]);

  // Central 3D Emoji / Icon
  ctx.font = '54px "Apple Color Emoji", "Segoe UI Emoji", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
  ctx.shadowBlur = 16;
  ctx.shadowOffsetY = 6;
  ctx.fillText(b.emoji || '📚', cx, cy + 2);
  ctx.restore();

  // 6. Title Typography (Playfair Display / Georgia)
  ctx.save();
  ctx.fillStyle = '#ffffff';
  ctx.textAlign = 'center';
  ctx.shadowColor = 'rgba(0,0,0,0.95)';
  ctx.shadowBlur = 10;
  ctx.shadowOffsetY = 3;

  const rawTitle = (b.title || 'Master Guide').replace(/\s*\(\d{4}\)/g, '');
  const words = rawTitle.split(' ');
  const lines = [];
  let currentLine = '';

  for (let i = 0; i < words.length; i++) {
    const testLine = currentLine ? (currentLine + ' ' + words[i]) : words[i];
    if (testLine.length > 21 && currentLine) {
      lines.push(currentLine);
      currentLine = words[i];
    } else {
      currentLine = testLine;
    }
  }
  if (currentLine) lines.push(currentLine);

  const fontSize = lines.length > 2 ? 19 : 22;
  ctx.font = `bold ${fontSize}px "Playfair Display", Georgia, serif`;

  let titleStartY = h * 0.58;
  if (lines.length > 2) titleStartY -= 10;
  lines.forEach((line, idx) => {
    ctx.fillText(line, w / 2, titleStartY + (idx * (fontSize + 6)));
  });

  // 7. Category & Subtitle
  const categoryY = titleStartY + (lines.length * (fontSize + 6)) + 8;
  ctx.fillStyle = '#94a3b8';
  ctx.font = '700 10px Inter, sans-serif';
  ctx.fillText(((b.cat || b.category || 'SPECIAL EDITION')).toUpperCase(), w / 2, categoryY);

  // Divider Line
  ctx.strokeStyle = 'rgba(245, 158, 11, 0.4)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(w * 0.25, categoryY + 10);
  ctx.lineTo(w * 0.75, categoryY + 10);
  ctx.stroke();

  // 8. Author Ribbon & Stars
  const authorY = categoryY + 26;
  ctx.fillStyle = '#f8fafc';
  ctx.font = 'bold 12px Inter, sans-serif';
  ctx.fillText('BY ' + (b.author ? b.author.toUpperCase() : 'THEBHOM EDITORIAL'), w / 2, authorY);

  ctx.fillStyle = '#f59e0b';
  ctx.font = '10px Inter, sans-serif';
  ctx.fillText('★★★★★ 4.9 (1,850+ REVIEWS)', w / 2, authorY + 16);
  ctx.restore();

  // 9. Realistic Barcode Box in Bottom-Right Corner (Exact match to references!)
  ctx.save();
  const bcW = 98;
  const bcH = 42;
  const bcX = w - bcW - 22;
  const bcY = h - bcH - 22;

  ctx.fillStyle = '#ffffff';
  ctx.fillRect(bcX, bcY, bcW, bcH);
  ctx.strokeStyle = 'rgba(0,0,0,0.25)';
  ctx.lineWidth = 1;
  ctx.strokeRect(bcX, bcY, bcW, bcH);

  ctx.fillStyle = '#000000';
  const stripeXStart = bcX + 6;
  const stripeWidthMax = bcW - 12;
  const stripes = [2, 1, 3, 1, 2, 4, 1, 2, 1, 3, 2, 1, 3, 1, 2, 1, 2, 1, 3, 2, 1, 2];
  let curX = stripeXStart;
  for (let i = 0; i < stripes.length && curX < stripeXStart + stripeWidthMax; i++) {
    const sw = stripes[i];
    if (i % 2 === 0) {
      ctx.fillRect(curX, bcY + 5, sw, 22);
    }
    curX += sw + 1.4;
  }
  ctx.font = '600 7px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('9 780134 685991', bcX + (bcW / 2), bcY + 36);
  ctx.restore();

  // 10. Bottom Left Publisher Badge
  ctx.save();
  ctx.fillStyle = '#22c55e';
  ctx.font = 'bold 10px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('✅ FULL 10-PAGE BOOK', 28, h - 38);

  ctx.fillStyle = 'rgba(255,255,255,0.5)';
  ctx.font = '600 9px Inter, sans-serif';
  ctx.fillText('thebhom.in/ebooks', 28, h - 24);
  ctx.restore();

  // 11. Glossy Book Sheen (Diagonal Light Reflection)
  ctx.save();
  const sheen = ctx.createLinearGradient(0, 0, w, h * 0.7);
  sheen.addColorStop(0, 'rgba(255, 255, 255, 0.22)');
  sheen.addColorStop(0.25, 'rgba(255, 255, 255, 0.05)');
  sheen.addColorStop(0.45, 'transparent');
  sheen.addColorStop(1, 'transparent');
  ctx.fillStyle = sheen;
  ctx.fillRect(0, 0, w, h);
  ctx.restore();

  // 12. Physical 3D Spine Crease on Left Edge
  ctx.save();
  const spineGrd = ctx.createLinearGradient(0, 0, 20, 0);
  spineGrd.addColorStop(0, 'rgba(0, 0, 0, 0.75)');
  spineGrd.addColorStop(0.2, 'rgba(255, 255, 255, 0.18)');
  spineGrd.addColorStop(0.45, 'rgba(0, 0, 0, 0.4)');
  spineGrd.addColorStop(1, 'transparent');
  ctx.fillStyle = spineGrd;
  ctx.fillRect(0, 0, 20, h);
  ctx.restore();

  // 13. Physical Page Thickness on Right Edge
  ctx.save();
  ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
  ctx.fillRect(w - 3, 0, 1, h);
  ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
  ctx.fillRect(w - 2, 0, 1, h);
  ctx.restore();

  return canvas;
}

function getBookCoverDataUrl(b) {
  if (!b) return '';
  if (b.cover && typeof b.cover === 'string' && b.cover.trim().length > 0) {
    return b.cover;
  }
  const key = b.id || b.title;
  if (_bookCoverCache.has(key)) return _bookCoverCache.get(key);
  try {
    const canv = generateBookCover(b, 380, 560);
    const dataUrl = canv.toDataURL('image/png');
    _bookCoverCache.set(key, dataUrl);
    return dataUrl;
  } catch(e) {
    console.error('getBookCoverDataUrl error:', e);
    return '';
  }
}

function generateMagCover(mag, w = 450, h = 600) {
  const canvas = document.createElement('canvas');
  canvas.width = w;
  canvas.height = h;
  const ctx = canvas.getContext('2d');

  const colors = (mag.colors && mag.colors.length >= 2) ? mag.colors : ['#064e3b', '#0f172a', '#34d399'];
  const [c1, c2, c3] = colors.length >= 3 ? colors : [colors[0], colors[1], colors[0]];

  // 1. Deep Rich Background Gradient
  const grd = ctx.createLinearGradient(0, 0, w * 0.8, h);
  grd.addColorStop(0, c1);
  grd.addColorStop(0.5, c2);
  grd.addColorStop(1, c3 || c2);
  ctx.fillStyle = grd;
  ctx.fillRect(0, 0, w, h);

  // 2. Ambient Cyber/Glow Nodes
  ctx.save();
  ctx.globalAlpha = 0.18;
  for (let i = 0; i < 30; i++) {
    const x = ((i * 73) % w);
    const y = ((i * 97) % h);
    ctx.fillStyle = (i % 2 === 0) ? '#38bdf8' : '#ec4899';
    ctx.beginPath();
    ctx.arc(x, y, (i % 4) + 1, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();

  // 3. Central Artwork: 3D Chrome Sphere / Swirl (Matching Tech Trends)
  const cx = w / 2;
  const cy = h * 0.42;
  const r = w * 0.27;

  ctx.save();
  const bgGlow = ctx.createRadialGradient(cx, cy, 10, cx, cy, r * 1.8);
  bgGlow.addColorStop(0, 'rgba(56, 189, 248, 0.45)');
  bgGlow.addColorStop(0.5, 'rgba(168, 85, 247, 0.25)');
  bgGlow.addColorStop(1, 'transparent');
  ctx.fillStyle = bgGlow;
  ctx.fillRect(0, cy - r * 2, w, r * 4);

  const sphereGrd = ctx.createRadialGradient(cx - r * 0.35, cy - r * 0.35, r * 0.05, cx, cy, r);
  const cat = (mag.category || mag.tag || '').toLowerCase();
  if (mag.id === 'm1' || cat.includes('tech')) {
    sphereGrd.addColorStop(0, '#ffffff');
    sphereGrd.addColorStop(0.25, '#38bdf8');
    sphereGrd.addColorStop(0.55, '#818cf8');
    sphereGrd.addColorStop(0.85, '#3b0764');
    sphereGrd.addColorStop(1, '#09090b');
  } else if (mag.id === 'm2' || cat.includes('business')) {
    sphereGrd.addColorStop(0, '#fef08a');
    sphereGrd.addColorStop(0.25, '#eab308');
    sphereGrd.addColorStop(0.6, '#0369a1');
    sphereGrd.addColorStop(1, '#082f49');
  } else if (mag.id === 'm3' || cat.includes('fashion')) {
    sphereGrd.addColorStop(0, '#fbcfe8');
    sphereGrd.addColorStop(0.3, '#f43f5e');
    sphereGrd.addColorStop(0.65, '#4c0519');
    sphereGrd.addColorStop(1, '#000000');
  } else {
    sphereGrd.addColorStop(0, '#a7f3d0');
    sphereGrd.addColorStop(0.3, '#10b981');
    sphereGrd.addColorStop(0.65, '#064e3b');
    sphereGrd.addColorStop(1, '#022c22');
  }

  ctx.shadowColor = 'rgba(0,0,0,0.6)';
  ctx.shadowBlur = 30;
  ctx.shadowOffsetY = 15;

  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fillStyle = sphereGrd;
  ctx.fill();
  ctx.restore();

  // 3D Orbiting Fluid Ring
  ctx.save();
  ctx.lineWidth = 14;
  const ringGrd = ctx.createLinearGradient(cx - r * 1.3, cy - r * 0.6, cx + r * 1.3, cy + r * 0.6);
  ringGrd.addColorStop(0, 'rgba(56, 189, 248, 0.9)');
  ringGrd.addColorStop(0.5, 'rgba(236, 72, 153, 0.8)');
  ringGrd.addColorStop(1, 'rgba(56, 189, 248, 0.2)');
  ctx.strokeStyle = ringGrd;
  ctx.shadowColor = 'rgba(56, 189, 248, 0.8)';
  ctx.shadowBlur = 18;
  ctx.beginPath();
  ctx.ellipse(cx, cy, r * 1.25, r * 0.45, Math.PI / -6, 0, Math.PI * 2);
  ctx.stroke();

  // Central icon badge
  ctx.font = '54px "Apple Color Emoji", "Segoe UI Emoji", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.shadowColor = 'rgba(0,0,0,0.9)';
  ctx.shadowBlur = 16;
  ctx.fillText(mag.emoji || '📰', cx, cy);
  ctx.restore();

  // 4. Magazine Masthead
  ctx.save();
  ctx.fillStyle = 'rgba(15, 23, 42, 0.75)';
  ctx.fillRect(16, 16, w - 32, 54);
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
  ctx.lineWidth = 1.5;
  ctx.strokeRect(16, 16, w - 32, 54);

  ctx.fillStyle = '#38bdf8';
  ctx.font = '900 11px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('THEBHOM LUXURY DIGITAL • ' + (mag.category || mag.tag || 'EXCLUSIVE').toUpperCase(), 28, 36);

  ctx.fillStyle = '#f59e0b';
  ctx.font = '700 10px Inter, sans-serif';
  ctx.textAlign = 'right';
  ctx.fillText((mag.issue || '2026') + ' • ₹0 FREE', w - 28, 36);

  // Main Title
  ctx.fillStyle = '#ffffff';
  ctx.font = '900 28px "Playfair Display", serif';
  ctx.textAlign = 'center';
  ctx.shadowColor = 'rgba(0,0,0,0.85)';
  ctx.shadowBlur = 14;

  const titleText = (mag.title || 'Tech Trends').split('—')[0].trim();
  ctx.fillText(titleText, w / 2, 114);

  // Subtitle
  ctx.fillStyle = '#94a3b8';
  ctx.font = '600 12px Inter, sans-serif';
  const subtitle = mag.title && mag.title.includes('—') ? mag.title.split('—')[1].trim() : 'Exclusive Collector Edition';
  ctx.fillText(subtitle, w / 2, 138);
  ctx.restore();

  // 5. Featured Cover Stories
  ctx.save();
  const headlines = mag.coverHeadlines || ['Top Industry Insights & Analysis', 'The 2026 Innovation Frontier', 'Exclusive Founder Interviews'];
  headlines.slice(0, 3).forEach((hl, idx) => {
    const y = h * 0.66 + (idx * 34);
    ctx.fillStyle = '#f59e0b';
    ctx.font = 'bold 12px Inter, sans-serif';
    ctx.fillText('◆', 26, y);

    ctx.fillStyle = '#f8fafc';
    ctx.font = '700 13px Inter, sans-serif';
    ctx.shadowColor = 'rgba(0,0,0,0.8)';
    ctx.shadowBlur = 6;
    ctx.fillText(hl.length > 34 ? hl.substring(0, 32) + '…' : hl, 44, y);
  });
  ctx.restore();

  // 6. Barcode Box
  ctx.save();
  const bcW = 110;
  const bcH = 48;
  const bcX = w - bcW - 20;
  const bcY = h - bcH - 20;

  ctx.fillStyle = '#ffffff';
  ctx.fillRect(bcX, bcY, bcW, bcH);
  ctx.strokeStyle = 'rgba(0,0,0,0.2)';
  ctx.lineWidth = 1;
  ctx.strokeRect(bcX, bcY, bcW, bcH);

  ctx.fillStyle = '#000000';
  const stripeXStart = bcX + 8;
  const stripeWidthMax = bcW - 16;
  const stripes = [2, 1, 3, 1, 2, 4, 1, 2, 1, 3, 2, 1, 4, 1, 2, 1, 3, 1, 2, 3, 1, 2, 1, 4, 2, 1];
  let currentX = stripeXStart;
  for (let i = 0; i < stripes.length && currentX < stripeXStart + stripeWidthMax; i++) {
    const sw = stripes[i];
    if (i % 2 === 0) {
      ctx.fillRect(currentX, bcY + 6, sw, 26);
    }
    currentX += sw + 1.5;
  }
  ctx.font = '600 8px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('9 771234 567003', bcX + (bcW / 2), bcY + 42);
  ctx.restore();

  // 7. Bottom Left Issue Badge
  ctx.save();
  ctx.fillStyle = '#22c55e';
  ctx.font = '900 11px Inter, sans-serif';
  ctx.textAlign = 'left';
  ctx.fillText('✅ FULL 10-PAGE UNABRIDGED', 26, h - 36);

  ctx.fillStyle = 'rgba(255,255,255,0.6)';
  ctx.font = '600 10px Inter, sans-serif';
  ctx.fillText('thebhom.in/magazines', 26, h - 20);
  ctx.restore();

  // 8. Glossy Sheen
  ctx.save();
  const sheenGrd = ctx.createLinearGradient(0, 0, w, h * 0.75);
  sheenGrd.addColorStop(0, 'rgba(255, 255, 255, 0.28)');
  sheenGrd.addColorStop(0.3, 'rgba(255, 255, 255, 0.08)');
  sheenGrd.addColorStop(0.5, 'transparent');
  sheenGrd.addColorStop(1, 'transparent');
  ctx.fillStyle = sheenGrd;
  ctx.fillRect(0, 0, w, h);
  ctx.restore();

  // 9. Physical Spine
  ctx.save();
  const spineGrd = ctx.createLinearGradient(0, 0, 22, 0);
  spineGrd.addColorStop(0, 'rgba(0, 0, 0, 0.65)');
  spineGrd.addColorStop(0.2, 'rgba(255, 255, 255, 0.15)');
  spineGrd.addColorStop(0.4, 'rgba(0, 0, 0, 0.35)');
  spineGrd.addColorStop(1, 'transparent');
  ctx.fillStyle = spineGrd;
  ctx.fillRect(0, 0, 22, h);
  ctx.restore();

  return canvas;
}

function getMagCoverDataUrl(mag) {
  if (!mag) return '';
  const key = mag.id || mag.title;
  if (_magCoverCache.has(key)) return _magCoverCache.get(key);
  try {
    const canv = generateMagCover(mag, 450, 600);
    const dataUrl = canv.toDataURL('image/png');
    _magCoverCache.set(key, dataUrl);
    return dataUrl;
  } catch(e) {
    console.error('getMagCoverDataUrl error:', e);
    return '';
  }
}


// ============================================================
// E-BOOK STOREFRONT MODAL
// ============================================================
function openAmazonBookModal(bookId) {
  let book = null;
  if (window.THEBHOM && THEBHOM.EBOOKS) {
    book = THEBHOM.EBOOKS.find(b => b.id === bookId);
  }
  if (!book && typeof BOOKS !== 'undefined') {
    book = BOOKS.find(b => b.id === bookId);
  }
  if (!book) {
    book = { id: bookId, title: 'Autonomous AI Agents & Swarms (2026)', author: 'Dr. Aravind Menon', category: 'Technology', emoji: '🤖', downloads: 48200 };
  }

  let overlay = document.getElementById('amzBookOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'amz-modal-overlay';
    overlay.id = 'amzBookOverlay';
    overlay.onclick = (e) => { if (e.target === overlay) closeAmazonBookModal(); };
    document.body.appendChild(overlay);
  }

  const mrp = 499;
  const ratingVal = "4.9";
  const ratingCount = "1,842";
  const pages = "240 Pages";
  const fileSize = "3.8 MB (Print Replica PDF)";
  const isbn = "978-81-965412-" + (Math.floor(Math.random() * 89) + 10);
  const companion1 = (window.THEBHOM?.EBOOKS || [])[1] || { title: 'The Solopreneur 2026 Blueprint', emoji: '🚀' };
  const companion2 = (window.THEBHOM?.EBOOKS || [])[3] || { title: 'The 2026 Attention Monopoly', emoji: '⚡' };

  overlay.innerHTML = `
    <div class="amz-modal" onclick="event.stopPropagation()">
      <button class="amz-close" onclick="closeAmazonBookModal()">✕</button>
      
      <div class="amz-header-bar">
        <div class="amz-breadcrumb">
          <a href="index.html">TheBhom Store</a> <span>›</span>
          <a href="ebooks.html">Free E-Books</a> <span>›</span>
          <span>${book.category || book.tag || 'Bestseller'}</span>
        </div>
        <div style="color:#f59e0b;font-weight:700;">🇮🇳 India's #1 Free Reading Hub</div>
      </div>

      <div class="amz-body-layout">
        <!-- LEFT COLUMN: 3D COVER & BUY BOX -->
        <div class="amz-left-col">
          <div class="amz-3d-cover-wrap">
            <div class="amz-3d-cover" style="padding:0;overflow:hidden;background:#090d16;position:relative;">
              <span class="amz-look-inside-ribbon" style="z-index:10;">📖 Look Inside</span>
              <img src="${getBookCoverDataUrl(book)}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="${book.title}" />
            </div>
          </div>

          <div class="amz-buy-box">
            <div class="amz-price-section">
              <div class="amz-mrp-row">M.R.P.: ₹${mrp}.00</div>
              <div class="amz-deal-row">
                <span class="amz-deal-price">₹0.00</span>
                <span class="amz-deal-badge">100% OFF FREE</span>
              </div>
              <div class="amz-save-text">You Save: ₹${mrp}.00 (100% Free Forever)</div>
            </div>

            <div class="amz-ku-badge">
              <span class="amz-ku-logo">TheBhom Reader</span>
              <span>Unlimited Free Access • No Card Needed</span>
            </div>

            <button class="amz-btn-buy" onclick="buyBookOneClick('${book.id}', '${book.title.replace(/'/g, "\\'")}')">
              ⚡ Get Free E-Book (Instant ₹0)
            </button>
            <button class="amz-btn-read" onclick="closeAmazonBookModal(); if(typeof openReader==='function'){ openReader('${book.id}'); } else { window.location.href='ebooks.html?read='+'${book.id}'; }">
              📖 Read Sample / Cloud Reader
            </button>

            <div class="amz-delivery-info">
              ⚡ Instant Digital Download • Read on Phone, iPad, PC & Tablets • Virus-Free Verified
            </div>
          </div>
        </div>

        <!-- RIGHT COLUMN: DETAILS, SYNOPSIS, BUNDLES & REVIEWS -->
        <div class="amz-right-col">
          <div>
            <div style="font-size:0.75rem;font-weight:800;color:#f59e0b;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">#1 Bestseller in ${book.category || book.tag || 'Digital Tech'} 2026</div>
            <h2 class="amz-book-title">${book.title}</h2>
            <div class="amz-book-subtitle">Complete Unabridged 10-Chapter Edition • Formatted for Peak Reading</div>
            <div class="amz-author-row" style="margin-top:8px;">
              <span>By <a href="#" class="amz-author-name">${book.author || 'Bhom Vrat Rai'}</a> (Author)</span>
              <span class="amz-star-rating">⭐⭐⭐⭐⭐ ${ratingVal}</span>
              <span class="amz-rating-count">(${ratingCount} global ratings)</span>
            </div>
          </div>

          <div class="amz-early-access-banner">
            <span style="font-size:1.2rem;">⚡</span>
            <div><strong>Early Access Beta:</strong> All e-books on TheBhom.in are currently ₹0 (100% Free). Download and claim now to keep in your library forever before premium plans launch!</div>
          </div>

          <!-- TECHNICAL SPECIFICATIONS -->
          <div class="amz-specs-table">
            <div class="amz-spec-box">
              <span class="amz-spec-label">Print Length</span>
              <span class="amz-spec-val">${pages}</span>
            </div>
            <div class="amz-spec-box">
              <span class="amz-spec-label">Language</span>
              <span class="amz-spec-val">English / हिन्दी</span>
            </div>
            <div class="amz-spec-box">
              <span class="amz-spec-label">Publisher</span>
              <span class="amz-spec-val">TheBhom Press</span>
            </div>
            <div class="amz-spec-box">
              <span class="amz-spec-label">File Size</span>
              <span class="amz-spec-val">${fileSize}</span>
            </div>
            <div class="amz-spec-box">
              <span class="amz-spec-label">ISBN-13</span>
              <span class="amz-spec-val">${isbn}</span>
            </div>
          </div>

          <!-- SYNOPSIS -->
          <div>
            <div class="amz-section-heading">📖 Book Description & Synopsis</div>
            <div class="amz-synopsis-box">
              "${book.title}" represents the definitive blueprint for high-impact knowledge in 2026. Packed with actionable frameworks, real-world case studies, and zero fluff, this masterclass edition delivers practical insights designed to transform your understanding and execution within minutes. Read seamlessly across mobile, tablet, or desktop with integrated text-to-speech audio narration.
            </div>
          </div>

          <!-- FREQUENTLY DOWNLOADED TOGETHER BUNDLE -->
          <div class="amz-bundle-card">
            <div class="amz-section-heading" style="font-size:0.95rem;margin:0;">📦 Frequently Downloaded Together (3-Book Bundle)</div>
            <div class="amz-bundle-items">
              <div class="amz-bundle-thumb" title="${book.title}">${book.emoji || '📚'}</div>
              <span class="amz-bundle-plus">+</span>
              <div class="amz-bundle-thumb" title="${companion1.title}">${companion1.emoji || '🚀'}</div>
              <span class="amz-bundle-plus">+</span>
              <div class="amz-bundle-thumb" title="${companion2.title}">${companion2.emoji || '⚡'}</div>
              <div style="flex:1;min-width:180px;">
                <div style="font-size:0.78rem;font-weight:700;color:#fff;">Triple Bestseller Bundle</div>
                <div style="font-size:0.72rem;color:#22c55e;font-weight:800;">Total Price: ₹0.00 (Save ₹1,497)</div>
                <button onclick="buyBookOneClick('${book.id}', '${book.title.replace(/'/g, "\\'")}'); showToast('🎉 Triple Bundle downloaded for ₹0!', 'ok');" style="margin-top:6px;padding:6px 14px;background:#f59e0b;color:#000;border:none;border-radius:50px;font-size:0.75rem;font-weight:800;cursor:pointer;">
                  ⬇️ Download All 3 for FREE
                </button>
              </div>
            </div>
          </div>

          <!-- CUSTOMER REVIEWS -->
          <div class="amz-reviews-card">
            <div class="amz-section-heading" style="font-size:0.95rem;">⭐ Top Customer Reviews from India</div>
            <div class="amz-user-review">
              <div class="amz-reviewer">
                <span>Rohit Verma (Jaipur)</span>
                <span class="amz-verified">✓ Verified Reader</span>
                <span style="color:#f59e0b;font-size:0.75rem;">⭐⭐⭐⭐⭐</span>
              </div>
              <div class="amz-review-text">
                "Incredible quality! Usually these 10-chapter books cost ₹400-500 elsewhere, but finding it on TheBhom.in completely free with zero ads or watermarks is game-changing. The audio narration is super helpful during commute."
              </div>
            </div>
            <div class="amz-user-review">
              <div class="amz-reviewer">
                <span>Ananya Sharma (Bengaluru)</span>
                <span class="amz-verified">✓ Verified Reader</span>
                <span style="color:#f59e0b;font-size:0.75rem;">⭐⭐⭐⭐⭐</span>
              </div>
              <div class="amz-review-text">
                "Clear, concise, and futuristic 2026 insights. The reading layout with dark theme makes reading on phone a breeze. Highly recommended!"
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  `;

  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeAmazonBookModal() {
  const overlay = document.getElementById('amzBookOverlay');
  if (overlay) {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

function buyBookOneClick(bookId, title) {
  if (typeof dlBook === 'function') {
    dlBook(bookId);
  } else if (typeof printBook === 'function') {
    printBook(bookId);
  } else if (typeof dlBookPDF === 'function') {
    dlBookPDF(bookId);
  } else {
    showToast(`🎉 "${title}" purchased for ₹0! Instant Download starting...`, 'ok');
    setTimeout(() => {
      window.location.href = `ebooks.html?download=${bookId}`;
    }, 450);
  }
  showToast(`✅ "${title}" claimed & added to your permanent library! (100% Free)`, 'ok');
}

// ============================================================
// PINTEREST-STYLE SAVING & MEGA-FEED LOGIC
// ============================================================
function pinItem(id, title, tag, emoji, btn) {
  if (typeof window.toggleFavorite === 'function') {
    window.toggleFavorite({id, title, tag, emoji});
  }
  const isSaved = window.isFavorite ? window.isFavorite(id) : true;
  if (btn) {
    btn.classList.toggle('saved', isSaved);
    btn.innerHTML = isSaved ? '✅ Saved' : '📌 Save';
  }
  document.querySelectorAll(`.pin-save-btn[data-id="${id}"]`).forEach(b => {
    b.classList.toggle('saved', isSaved);
    b.innerHTML = isSaved ? '✅ Saved' : '📌 Save';
  });
  if (isSaved) {
    showToast(`📌 "${title}" Saved to your Board!`, 'ok');
  } else {
    showToast(`🗑️ Removed from Saved Board`, 'info');
  }
};

let currentHomeFeedCat = 'all';
let currentHomeFeedLimit = 28;

function renderPinterestHomeFeed(containerId = 'pinterestFeedContainer', category = 'all', append = false) {
  const container = document.getElementById(containerId);
  if (!container || !window.THEBHOM) return;

  currentHomeFeedCat = category;
  if (!append) currentHomeFeedLimit = 8;

  let allPins = [];

  // 1. Wallpapers (Unsplash/Wallhaven research)
  if (category === 'all' || category === 'wallpapers' || category === 'dark' || category === 'space') {
    const walls = window.THEBHOM.WALLPAPERS || [];
    walls.forEach(w => {
      let match = true;
      if (category === 'dark' && w.tag !== 'Dark' && !w.title.toLowerCase().includes('dark') && !w.title.toLowerCase().includes('black')) match = false;
      if (category === 'space' && w.tag !== 'Space' && !w.title.toLowerCase().includes('galaxy') && !w.title.toLowerCase().includes('star')) match = false;
      if (match) {
        allPins.push({
          id: w.id,
          title: w.title,
          category: 'wallpapers',
          badgeText: '🖼️ 4K WALLPAPER',
          tag: w.tag,
          emoji: w.emoji || '🖼️',
          ratio: (w.id.charCodeAt(0) % 2 === 0) ? '9/16' : '3/4',
          author: 'TheBhom Wallpapers',
          authorInitials: 'TW',
          authorBg: '#7c3aed',
          priceBadge: '4K Ultra-HD',
          actionText: '📱 4K Download',
          actionHandler: `location.href='wallpapers.html#${w.id}'`,
          openHandler: `location.href='wallpapers.html#${w.id}'`,
          thumb: `https://picsum.photos/seed/${w.id}p/600/${(w.id.charCodeAt(0) % 2 === 0) ? '900' : '750'}`
        });
      }
    });
  }

  // 2. E-Books
  if (category === 'all' || category === 'ebooks' || category === 'business') {
    const books = window.THEBHOM.EBOOKS || [];
    books.forEach(b => {
      let match = true;
      if (category === 'business' && b.tag !== 'Business' && b.tag !== 'Career' && b.tag !== 'Finance') match = false;
      if (match) {
        allPins.push({
          id: b.id,
          title: b.title,
          category: 'ebooks',
          badgeText: '📖 FREE E-BOOK',
          tag: b.tag,
          emoji: b.emoji || '📚',
          ratio: '2/3',
          author: 'TheBhom Publishing',
          authorInitials: 'TP',
          authorBg: '#f59e0b',
          priceBadge: '₹499 ₹0 FREE',
          actionText: '📖 View E-Book',
          actionHandler: `openAmazonBookModal('${b.id}')`,
          openHandler: `openAmazonBookModal('${b.id}')`,
          customCover: true,
          color: b.color || '#7c3aed',
          pages: b.pages || 10
        });
      }
    });
  }

  // 3. Magazines (Issuu Glossy Flip research)
  if (category === 'all' || category === 'magazines' || category === 'business') {
    const mags = window.THEBHOM.MAGAZINES || [];
    mags.forEach(m => {
      let match = true;
      if (category === 'business' && m.tag !== 'Business' && m.tag !== 'Tech') match = false;
      if (match) {
        allPins.push({
          id: m.id,
          title: m.title,
          category: 'magazines',
          badgeText: '📰 DIGITAL ISSUE',
          tag: m.tag,
          emoji: m.emoji || '📰',
          ratio: '3/4',
          author: 'TheBhom Editorial',
          authorInitials: 'ME',
          authorBg: '#10b981',
          priceBadge: `${m.month || 'New'} Edition`,
          actionText: '📖 Flip Reader',
          actionHandler: `location.href='magazines.html#${m.id}'`,
          openHandler: `location.href='magazines.html#${m.id}'`,
          customMag: true,
          headline: m.headline || 'Exclusive Cover Story',
          color: '#064e3b'
        });
      }
    });
  }

  // 4. Templates (Canva & Figma research)
  if (category === 'all' || category === 'templates' || category === 'business') {
    const tmpls = window.THEBHOM.TEMPLATES || [];
    tmpls.forEach(t => {
      let match = true;
      if (category === 'business' && t.tag !== 'Resume' && t.tag !== 'Business' && t.tag !== 'Deck') match = false;
      if (match) {
        allPins.push({
          id: t.id,
          title: t.title,
          category: 'templates',
          badgeText: '🎨 CANVA & FIGMA',
          tag: t.tag,
          emoji: t.emoji || '🎨',
          ratio: '1/1',
          author: 'TheBhom Design Studio',
          authorInitials: 'DS',
          authorBg: '#06b6d4',
          priceBadge: '100% Free Pack',
          actionText: '🎨 Edit Template',
          actionHandler: `location.href='templates.html#${t.id}'`,
          openHandler: `location.href='templates.html#${t.id}'`,
          customTmpl: true,
          sub: t.sub || 'Social Media Pack',
          colors: t.colors || ['#06b6d4', '#7c3aed']
        });
      }
    });
  }

  // 5. Anniversary Cards (Greetings Island / 3D Flip research)
  if (category === 'all' || category === 'cards' || category === 'love') {
    const cards = window.THEBHOM.CARDS || [];
    cards.forEach(c => {
      let match = true;
      if (category === 'love' && c.tag !== 'Anniversary' && c.tag !== 'Love' && c.tag !== 'Wedding') match = false;
      if (match) {
        allPins.push({
          id: c.id,
          title: c.title,
          category: 'cards',
          badgeText: '💌 4-PANEL 3D CARD',
          tag: c.tag,
          emoji: c.emoji || '💌',
          ratio: '4/5',
          author: 'TheBhom Greetings',
          authorInitials: 'TG',
          authorBg: '#ec4899',
          priceBadge: 'Print Ready 300 DPI',
          actionText: '💌 3D Flip & Play',
          actionHandler: `location.href='cards.html#${c.id}'`,
          openHandler: `location.href='cards.html#${c.id}'`,
          customCard: true,
          sub: c.sub || 'Foldable Card'
        });
      }
    });
  }

  // Deterministic shuffle using title hash for consistent masonry mixing
  allPins.sort((a, b) => {
    const hA = (a.id + a.title).split('').reduce((acc, ch) => acc + ch.charCodeAt(0), 0);
    const hB = (b.id + b.title).split('').reduce((acc, ch) => acc + ch.charCodeAt(0), 0);
    return (hA % 100) - (hB % 100);
  });

  const sliced = allPins.slice(0, currentHomeFeedLimit);

  const pinsHtml = sliced.map(pin => {
    const isFav = window.isFavorite ? window.isFavorite(pin.id) : false;
    const safeTitle = pin.title.replace(/'/g, "\\'");

    let mediaContent = '';
    if (pin.customCover) {
      const bookObj = (window.THEBHOM?.EBOOKS || []).find(x => x.id === pin.id) || (typeof BOOKS !== 'undefined' ? BOOKS.find(x => x.id === pin.id) : null) || {
        id: pin.id,
        title: pin.title,
        author: pin.author || 'TheBhom Editorial',
        cat: pin.tag || 'Technology',
        emoji: pin.emoji || '📚',
        gradient: [pin.color || '#1e1b4b', '#0f172a']
      };
      const coverUrl = getBookCoverDataUrl(bookObj);
      mediaContent = `
        <div style="position:relative;width:100%;aspect-ratio:2/3;overflow:hidden;border-radius:12px;background:#090d16;box-shadow:0 10px 25px rgba(0,0,0,0.35);">
          <img src="${coverUrl}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="${pin.title}" loading="lazy" />
        </div>
      `;
    } else if (pin.customMag) {
      const magObj = (window.THEBHOM?.MAGAZINES || []).find(x => x.id === pin.id) || (typeof MAGS !== 'undefined' ? MAGS.find(x => x.id === pin.id) : null) || {
        id: pin.id,
        title: pin.title,
        category: pin.tag || 'Technology',
        emoji: pin.emoji || '📰',
        issue: pin.priceBadge || 'Sept 2026',
        colors: [pin.color || '#064e3b', '#0f172a', '#34d399']
      };
      const coverUrl = getMagCoverDataUrl(magObj);
      mediaContent = `
        <div style="position:relative;width:100%;aspect-ratio:3/4;overflow:hidden;border-radius:12px;background:#090d16;box-shadow:0 10px 25px rgba(0,0,0,0.35);">
          <img src="${coverUrl}" style="width:100%;height:100%;object-fit:cover;display:block;" alt="${pin.title}" loading="lazy" />
        </div>
      `;
    } else if (pin.customTmpl) {
      mediaContent = `
        <div style="width:100%;height:100%;min-height:240px;background:linear-gradient(135deg,${pin.colors[0]}33,${pin.colors[1]||'#1e1b4b'});display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.2rem;text-align:center;position:relative;">
          <div style="font-size:2.8rem;margin-bottom:0.5rem;">${pin.emoji}</div>
          <div style="font-size:1rem;font-weight:800;color:#fff;line-height:1.3;">${pin.title}</div>
          <div style="font-size:0.72rem;color:#38bdf8;margin-top:4px;">${pin.sub}</div>
          <div style="margin-top:0.75rem;display:flex;gap:4px;font-size:0.62rem;font-weight:800;">
            <span style="background:rgba(0,0,0,0.4);color:#a855f7;padding:2px 6px;border-radius:4px;">CANVA</span>
            <span style="background:rgba(0,0,0,0.4);color:#06b6d4;padding:2px 6px;border-radius:4px;">FIGMA</span>
            <span style="background:rgba(0,0,0,0.4);color:#22c55e;padding:2px 6px;border-radius:4px;">PNG</span>
          </div>
        </div>
      `;
    } else if (pin.customCard) {
      mediaContent = `
        <div style="width:100%;height:100%;min-height:250px;background:linear-gradient(135deg,#370926,#180b1e);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.4rem;text-align:center;position:relative;border:1px dashed rgba(236,72,153,0.3);border-radius:12px;margin:8px;">
          <div style="font-size:2.5rem;margin-bottom:0.4rem;">${pin.emoji}</div>
          <div style="font-family:'Dancing Script',cursive;font-size:1.4rem;font-weight:700;color:#f472b6;line-height:1.2;">${pin.title}</div>
          <div style="font-size:0.7rem;color:#fbcfe8;margin-top:4px;">💌 4-Panel Foldable Romantic Card</div>
          <div style="margin-top:0.6rem;font-size:0.65rem;color:#f59e0b;font-weight:700;">🎵 Includes Romantic Audio BGM</div>
        </div>
      `;
    } else {
      mediaContent = `<img src="${pin.thumb}" alt="${pin.title}" loading="lazy" decoding="async" onerror="this.parentElement.style.background='linear-gradient(135deg,#1e1b4b,#0f172a)'"/>`;
    }

    return `
      <div class="pin-item" id="pin_${pin.id}" onclick="${pin.openHandler}">
        <div class="pin-thumb" style="aspect-ratio:${pin.ratio};">
          ${mediaContent}
          <div style="position:absolute;top:10px;left:10px;background:rgba(0,0,0,0.75);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,0.15);padding:3px 8px;border-radius:6px;font-size:0.64rem;font-weight:800;color:#f8fafc;letter-spacing:0.5px;z-index:2;">
            ${pin.badgeText}
          </div>

          <!-- Pinterest Floating Hover Overlay -->
          <div class="pin-overlay">
            <div class="pin-top-actions">
              <button class="pin-save-btn ${isFav?'saved':''}" data-id="${pin.id}" onclick="event.stopPropagation();pinItem('${pin.id}','${safeTitle}','${pin.tag}','${pin.emoji}',this)">
                ${isFav?'✅ Saved':'📌 Save'}
              </button>
            </div>
            <div class="pin-bottom-actions">
              <button class="pin-action-pill" onclick="event.stopPropagation();${pin.actionHandler}">
                ${pin.actionText}
              </button>
              <button class="pin-action-icon" title="Quick View" onclick="event.stopPropagation();${pin.openHandler}">
                ↗
              </button>
            </div>
          </div>
        </div>

        <div class="pin-info">
          <div class="pin-title">${pin.title}</div>
          <div class="pin-meta">
            <div class="pin-creator">
              <div class="pin-avatar" style="background:${pin.authorBg}">${pin.authorInitials}</div>
              <span>${pin.author}</span>
            </div>
            <span style="font-weight:700;color:#22c55e;">${pin.priceBadge}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');

  if (append) {
    container.insertAdjacentHTML('beforeend', pinsHtml);
  } else {
    container.innerHTML = pinsHtml;
  }

  // Update Load More button
  const lmBtn = document.getElementById('homeLoadMorePins');
  if (lmBtn) {
    lmBtn.style.display = allPins.length > currentHomeFeedLimit ? 'inline-flex' : 'none';
  }
};

function loadMoreHomePins() {
  currentHomeFeedLimit += 24;
  renderPinterestHomeFeed('pinterestFeedContainer', currentHomeFeedCat, false);
}

function filterHomePinterest(cat, chipEl) {
  document.querySelectorAll('.explore-chip').forEach(c => c.classList.remove('active'));
  if (chipEl) chipEl.classList.add('active');
  renderPinterestHomeFeed('pinterestFeedContainer', cat, false);
}

// Global window exposure
window.openAuthModal = openAuthModal;
window.closeAuthModal = closeAuthModal;
window.logoutTheBhomUser = logoutTheBhomUser;
window.openSpotlight = openSpotlight;
window.closeSpotlight = closeSpotlight;
window.openSpotlightItem = openSpotlightItem;
window.openQRModal = openQRModal;
window.closeQRModal = closeQRModal;
window.openUpiPaymentModal = openUpiPaymentModal;
window.closeUpiPaymentModal = closeUpiPaymentModal;
window.copyUpiId = copyUpiId;
window.submitUpiVerification = submitUpiVerification;
window.toggleRomanticBGM = toggleRomanticBGM;
window.playRomanticBGM = playRomanticBGM;
window.stopRomanticBGM = stopRomanticBGM;
window.toggleLanguage = toggleLanguage;
window.copySelectedQuote = copySelectedQuote;
window.shareSelectedQuote = shareSelectedQuote;
window.shareToWhatsAppStatus = shareToWhatsAppStatus;
window.generateBookCover = generateBookCover;
window.getBookCoverDataUrl = getBookCoverDataUrl;
window.generateMagCover = generateMagCover;
window.getMagCoverDataUrl = getMagCoverDataUrl;
window.openAmazonBookModal = openAmazonBookModal;
window.closeAmazonBookModal = closeAmazonBookModal;
window.buyBookOneClick = buyBookOneClick;
window.pinItem = pinItem;
window.renderPinterestHomeFeed = renderPinterestHomeFeed;
window.loadMoreHomePins = loadMoreHomePins;
window.filterHomePinterest = filterHomePinterest;
window.promptPwaInstall = triggerAppInstall;
window.initShared = initShared;
window.setAppTheme = setAppTheme;
window.toggleThemeMenu = toggleThemeMenu;
window.getThemeSwitcherHTML = getThemeSwitcherHTML;
window.getStoredTheme = getStoredTheme;
window.quickToggleTheme = quickToggleTheme;
window.updateThemeIcon = updateThemeIcon;
window.renderHeader = renderHeader;
window.renderSubnav = renderSubnav;

// Auto-initialize shared features on every page so buttons, modals, and spotlight always work
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    try { initShared(); } catch(e) { console.log('initShared err:', e); }
  });
} else {
  try { initShared(); } catch(e) { console.log('initShared err:', e); }
}



