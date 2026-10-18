// ============================================================
// TheBhom.in — Progressive Web App (PWA) Service Worker
// Cache Version: v2026.09.14
// ============================================================

const CACHE_NAME = 'thebhom-cache-v6';
const PRECACHE_ASSETS = [
  '/',
  '/index.html',
  '/shared.css?v=20261018_v1',
  '/shared.js?v=20261018_v1',
  '/icon-192.png',
  '/icon-512.png',
  '/manifest.json'
];

// 1. Install Event: Cache Core App Shell & Skip Waiting
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('Pre-caching non-fatal warning:', err);
      });
    })
  );
});

// 2. Activate Event: Clean up old caches & Claim Clients Immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            console.log('Deleting legacy cache:', name);
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Fetch Event: Network-First for HTML, Scripts, Styles; Cache-First for static media
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Ignore non-GET, analytics, ads, and /deals (deals has dynamic shopping catalog)
  if (req.method !== 'GET') return;
  if (url.origin.includes('google') || url.origin.includes('gstatic') || url.origin.includes('pagead2')) return;
  if (url.pathname.startsWith('/deals')) return;

  // For HTML documents, JS scripts, and CSS: Always Network-First so updates reflect immediately
  const isDocument = req.headers.get('accept') && req.headers.get('accept').includes('text/html');
  const isCodeAsset = req.destination === 'script' || req.destination === 'style' || url.pathname.endsWith('.js') || url.pathname.endsWith('.css');

  if (isDocument || isCodeAsset) {
    event.respondWith(
      fetch(req)
        .then((networkRes) => {
          if (networkRes && networkRes.status === 200) {
            const resClone = networkRes.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, resClone));
          }
          return networkRes;
        })
        .catch(() => caches.match(req).then((cachedRes) => cachedRes || (isDocument ? caches.match('/index.html') : null)))
    );
    return;
  }

  // For static media (images, fonts, icons): Stale-while-revalidate
  event.respondWith(
    caches.match(req).then((cached) => {
      const fetchPromise = fetch(req)
        .then((networkRes) => {
          if (networkRes && networkRes.status === 200) {
            const resClone = networkRes.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, resClone));
          }
          return networkRes;
        })
        .catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
