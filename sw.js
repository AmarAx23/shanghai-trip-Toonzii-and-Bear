// Offline support for the trip page.
// The page itself is fetched network-first, so an installed iPhone/Android app always shows the newest
// version when online and falls back to the saved copy when offline. Photos, fonts and Leaflet are cache-first.
const CACHE_NAME = 'sh-trip-v202611242322';
const URLS_TO_CACHE = [
  './',
  './index.html',
  './tour.html',
  './present.html',
  './manifest.json',
  './icon-180.png',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './icon.svg',
  './favicon.ico',
  './favicon-32.png',
  './vendor/leaflet/leaflet.js',
  './vendor/leaflet/leaflet.css',
  './vendor/maplibre/maplibre-gl.js',
  './vendor/maplibre/maplibre-gl.css',
  './img/canton8.jpg',
  './img/chef-fei.jpg',
  './img/cocina19.jpg',
  './img/grandmas-home.jpg',
  './img/lailai.jpg',
  './img/long-time-ago.jpg',
  './img/maotou.jpg',
  './img/new-sukiyaki.jpg',
  './img/pane.jpg',
  './img/pushing.jpg',
  './img/hd/adventure-1280.webp',
  './img/hd/adventure-640.webp',
  './img/hd/agedbeef-1280.webp',
  './img/hd/agedbeef-640.webp',
  './img/hd/anfu-1280.webp',
  './img/hd/anfu-640.webp',
  './img/hd/bagel-1280.webp',
  './img/hd/bagel-640.webp',
  './img/hd/bkk-1280.webp',
  './img/hd/bkk-640.webp',
  './img/hd/bund-1280.webp',
  './img/hd/bund-640.webp',
  './img/hd/bundday-1280.webp',
  './img/hd/bundday-640.webp',
  './img/hd/butterful-1280.webp',
  './img/hd/butterful-640.webp',
  './img/hd/castle-1280.webp',
  './img/hd/castle-640.webp',
  './img/hd/citygod-1280.webp',
  './img/hd/citygod-640.webp',
  './img/hd/disney-1280.webp',
  './img/hd/disney-640.webp',
  './img/hd/dongsheng-1280.webp',
  './img/hd/dongsheng-640.webp',
  './img/hd/fireworks-1280.webp',
  './img/hd/fireworks-640.webp',
  './img/hd/hero-1920.webp',
  './img/hd/hero-960.webp',
  './img/hd/huaihai-1280.webp',
  './img/hd/huaihai-640.webp',
  './img/hd/ifc-1280.webp',
  './img/hd/ifc-640.webp',
  './img/hd/jade-1280.webp',
  './img/hd/jade-640.webp',
  './img/hd/jingan-1280.webp',
  './img/hd/jingan-640.webp',
  './img/hd/ljznight-1280.webp',
  './img/hd/ljznight-640.webp',
  './img/hd/luneurs-1280.webp',
  './img/hd/luneurs-640.webp',
  './img/hd/m50-1280.webp',
  './img/hd/m50-640.webp',
  './img/hd/marzo-1280.webp',
  './img/hd/marzo-640.webp',
  './img/hd/nanjing-1280.webp',
  './img/hd/nanjing-640.webp',
  './img/hd/njnight-1280.webp',
  './img/hd/njnight-640.webp',
  './img/hd/no1dept-1280.webp',
  './img/hd/no1dept-640.webp',
  './img/hd/northbund-1280.webp',
  './img/hd/northbund-640.webp',
  './img/hd/peoples-1280.webp',
  './img/hd/peoples-640.webp',
  './img/hd/peoplespark-1280.webp',
  './img/hd/peoplespark-640.webp',
  './img/hd/pvg-1280.webp',
  './img/hd/pvg-640.webp',
  './img/hd/rockbund-1280.webp',
  './img/hd/rockbund-640.webp',
  './img/hd/skywalk-1280.webp',
  './img/hd/skywalk-640.webp',
  './img/hd/spring-1280.webp',
  './img/hd/spring-640.webp',
  './img/hd/superbrand-1280.webp',
  './img/hd/superbrand-640.webp',
  './img/hd/sz-fish-1280.webp',
  './img/hd/sz-fish-640.webp',
  './img/hd/sz-garden-1280.webp',
  './img/hd/sz-garden-640.webp',
  './img/hd/sz-noodle-1280.webp',
  './img/hd/sz-noodle-640.webp',
  './img/hd/sz-pingjiang-1280.webp',
  './img/hd/sz-pingjiang-640.webp',
  './img/hd/sz-shantang-1280.webp',
  './img/hd/sz-shantang-640.webp',
  './img/hd/sz-shstation-1280.webp',
  './img/hd/sz-shstation-640.webp',
  './img/hd/sz-station-1280.webp',
  './img/hd/sz-station-640.webp',
  './img/hd/sz-train-1280.webp',
  './img/hd/sz-train-640.webp',
  './img/hd/tianzifang-1280.webp',
  './img/hd/tianzifang-640.webp',
  './img/hd/treasure-1280.webp',
  './img/hd/treasure-640.webp',
  './img/hd/waibaidu-1280.webp',
  './img/hd/waibaidu-640.webp',
  './img/hd/westbund-1280.webp',
  './img/hd/westbund-640.webp',
  './img/hd/wnanjing-1280.webp',
  './img/hd/wnanjing-640.webp',
  './img/hd/wukang-1280.webp',
  './img/hd/wukang-640.webp',
  './img/hd/xintiandi-1280.webp',
  './img/hd/xintiandi-640.webp',
  './img/hd/xmas-1280.webp',
  './img/hd/xmas-640.webp',
  './img/hd/yu-1280.webp',
  './img/hd/yu-640.webp',
  './img/hd/yuxingji-1280.webp',
  './img/hd/yuxingji-640.webp',
  './img/hd/zhujiajiao-1280.webp',
  './img/hd/zhujiajiao-640.webp',
  './img/hd/zongzi-1280.webp',
  './img/hd/zongzi-640.webp',
  './img/hd/zootopia-1280.webp',
  './img/hd/zootopia-640.webp',
  './fonts/kanit-latin-600-normal.woff2',
  './fonts/kanit-thai-600-normal.woff2',
  './fonts/noto-sans-thai-latin-400-normal.woff2',
  './fonts/noto-sans-thai-latin-700-normal.woff2',
  './fonts/noto-sans-thai-thai-400-normal.woff2',
  './fonts/noto-sans-thai-thai-700-normal.woff2'
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(URLS_TO_CACHE)));
  self.skipWaiting();
});

const TILE_CACHE = 'sh-tiles-v1'; // OpenStreetMap tiles saved for offline use (kept across versions)
const OFM_CACHE = 'sh-ofm-v1';   // OpenFreeMap style, vector tiles, fonts, sprites for the tour (kept across versions)

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME && k !== TILE_CACHE && k !== OFM_CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function isPage(req) {
  const path = new URL(req.url).pathname;
  return req.mode === 'navigate' || path.endsWith('/') || path.endsWith('/index.html') ||
    (req.headers.get('accept') || '').includes('text/html');
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'tile.openstreetmap.org') {
    // map tiles: saved copy first (works offline / in China without VPN), otherwise fetch and keep it
    event.respondWith(
      caches.open(TILE_CACHE).then((c) => c.match(req.url).then((hit) => hit || fetch(req).then((res) => {
        if (res && res.ok) c.put(req.url, res.clone());
        return res;
      })))
    );
    return;
  }
  if (url.hostname === 'tiles.openfreemap.org') {
    // tour map: style/tilejson newest when online, tiles/fonts/sprites saved copy first
    const isJson = /\/styles\/|\/planet$|\.json$/.test(url.pathname) && !/sprite/.test(url.pathname);
    event.respondWith(caches.open(OFM_CACHE).then((c) => {
      const net = () => fetch(req).then((res) => { if (res && res.ok) c.put(req.url, res.clone()); return res; });
      return isJson ? net().catch(() => c.match(req.url)) : c.match(req.url).then((hit) => hit || net());
    }));
    return;
  }
  if (url.origin !== self.location.origin) return; // weather, rates: straight to network

  if (isPage(req)) {
    event.respondWith(
      fetch(req, { cache: 'no-store' })
        .then((res) => {
          if (res && res.ok) { const copy = res.clone(); const key = url.pathname.endsWith('tour.html') ? './tour.html' : url.pathname.endsWith('present.html') ? './present.html' : './index.html'; caches.open(CACHE_NAME).then((c) => c.put(key, copy)); }
          return res;
        })
        .catch(() => caches.match(url.pathname.endsWith('tour.html') ? './tour.html' : url.pathname.endsWith('present.html') ? './present.html' : './index.html').then((r) => r || caches.match('./')))
    );
    return;
  }

  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then((cached) => cached || fetch(req).then((res) => {
      if (res && res.ok) { const copy = res.clone(); caches.open(CACHE_NAME).then((c) => c.put(req, copy)); }
      return res;
    }))
  );
});
