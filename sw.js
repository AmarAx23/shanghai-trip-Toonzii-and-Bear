// Bump this version string whenever index.html changes, so returning
// offline visitors get the fresh copy instead of a stale cached one.
const CACHE_NAME = 'hk-trip-cache-v16';
const URLS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './vendor/leaflet/leaflet.js',
  './vendor/leaflet/leaflet.css',
  './icon-192.png',
  './icon-512.png',
  './img/adventure-isle.jpg',
  './img/bkk.jpg',
  './img/bund.jpg',
  './img/canton8.jpg',
  './img/castle.jpg',
  './img/chef-fei.jpg',
  './img/disneyland.jpg',
  './img/fireworks.jpg',
  './img/grandmas-home.jpg',
  './img/hero.jpg',
  './img/huaihai-road.jpg',
  './img/lailai.jpg',
  './img/long-time-ago.jpg',
  './img/nanjing-road.jpg',
  './img/new-sukiyaki.jpg',
  './img/peoples-square.jpg',
  './img/pvg.jpg',
  './img/superbrand.jpg',
  './img/treasure-cove.jpg',
  './img/wukang-road.jpg',
  './img/xintiandi.jpg',
  './img/yu-garden.jpg',
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
