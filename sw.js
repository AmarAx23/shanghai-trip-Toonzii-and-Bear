// Bump this version string whenever index.html changes, so returning
// offline visitors get the fresh copy instead of a stale cached one.
const CACHE_NAME = 'hk-trip-cache-v21';
const URLS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './vendor/leaflet/leaflet.js',
  './vendor/leaflet/leaflet.css',
  './img/canton8.jpg',
  './img/chef-fei.jpg',
  './img/grandmas-home.jpg',
  './img/lailai.jpg',
  './img/long-time-ago.jpg',
  './img/new-sukiyaki.jpg',
  './img/hd/adventure-1280.webp',
  './img/hd/adventure-640.webp',
  './img/hd/bkk-1280.webp',
  './img/hd/bkk-640.webp',
  './img/hd/bund-1280.webp',
  './img/hd/bund-640.webp',
  './img/hd/castle-1280.webp',
  './img/hd/castle-640.webp',
  './img/hd/citygod-1280.webp',
  './img/hd/citygod-640.webp',
  './img/hd/disney-1280.webp',
  './img/hd/disney-640.webp',
  './img/hd/fireworks-1280.webp',
  './img/hd/fireworks-640.webp',
  './img/hd/hero-1920.webp',
  './img/hd/hero-960.webp',
  './img/hd/huaihai-1280.webp',
  './img/hd/huaihai-640.webp',
  './img/hd/jade-1280.webp',
  './img/hd/jade-640.webp',
  './img/hd/m50-1280.webp',
  './img/hd/m50-640.webp',
  './img/hd/nanjing-1280.webp',
  './img/hd/nanjing-640.webp',
  './img/hd/peoples-1280.webp',
  './img/hd/peoples-640.webp',
  './img/hd/pvg-1280.webp',
  './img/hd/pvg-640.webp',
  './img/hd/superbrand-1280.webp',
  './img/hd/superbrand-640.webp',
  './img/hd/tianzifang-1280.webp',
  './img/hd/tianzifang-640.webp',
  './img/hd/treasure-1280.webp',
  './img/hd/treasure-640.webp',
  './img/hd/wukang-1280.webp',
  './img/hd/wukang-640.webp',
  './img/hd/xintiandi-1280.webp',
  './img/hd/xintiandi-640.webp',
  './img/hd/yu-1280.webp',
  './img/hd/yu-640.webp',
  './img/hd/zhujiajiao-1280.webp',
  './img/hd/zhujiajiao-640.webp',
  './fonts/kanit-latin-600-normal.woff2',
  './fonts/kanit-thai-600-normal.woff2',
  './fonts/noto-sans-thai-latin-400-normal.woff2',
  './fonts/noto-sans-thai-latin-700-normal.woff2',
  './fonts/noto-sans-thai-thai-400-normal.woff2',
  './fonts/noto-sans-thai-thai-700-normal.woff2'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(URLS_TO_CACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const network = fetch(event.request)
        .then((response) => {
          if (response && response.status === 200 && event.request.method === 'GET') {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => cached || caches.match('./index.html'));
      return cached || network;
    })
  );
});
