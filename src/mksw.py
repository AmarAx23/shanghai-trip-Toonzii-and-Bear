# Writes sw.js: network-first for the page (always newest when online), cache-first for static files.
import os, sys, time
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ver = sys.argv[1] if len(sys.argv) > 1 else time.strftime("v%Y%m%d%H%M")
files=['./','./index.html','./manifest.json','./icon-180.png','./icon-192.png','./icon-512.png','./icon-maskable-512.png','./icon.svg','./favicon.ico','./favicon-32.png','./vendor/leaflet/leaflet.js','./vendor/leaflet/leaflet.css']
files+=['./img/'+f for f in sorted(os.listdir('img')) if f.endswith('.jpg')]
files+=['./img/hd/'+f for f in sorted(os.listdir('img/hd')) if f.endswith('.webp')]
files+=['./fonts/'+f for f in sorted(os.listdir('fonts')) if f.endswith('.woff2')]
lst=',\n'.join("  '%s'"%f for f in files)
open('sw.js','w').write(f"""// Offline support for the trip page.
// The page itself is fetched network-first, so an installed iPhone/Android app always shows the newest
// version when online and falls back to the saved copy when offline. Photos, fonts and Leaflet are cache-first.
const CACHE_NAME = 'sh-trip-{ver}';
const URLS_TO_CACHE = [
{lst}
];

self.addEventListener('install', (event) => {{
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(URLS_TO_CACHE)));
  self.skipWaiting();
}});

const TILE_CACHE = 'sh-tiles-v1'; // OpenStreetMap tiles saved for offline use (kept across versions)

self.addEventListener('activate', (event) => {{
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME && k !== TILE_CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
}});

function isPage(req) {{
  const path = new URL(req.url).pathname;
  return req.mode === 'navigate' || path.endsWith('/') || path.endsWith('/index.html') ||
    (req.headers.get('accept') || '').includes('text/html');
}}

self.addEventListener('fetch', (event) => {{
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'tile.openstreetmap.org') {{
    // map tiles: saved copy first (works offline / in China without VPN), otherwise fetch and keep it
    event.respondWith(
      caches.open(TILE_CACHE).then((c) => c.match(req.url).then((hit) => hit || fetch(req).then((res) => {{
        if (res && res.ok) c.put(req.url, res.clone());
        return res;
      }})))
    );
    return;
  }}
  if (url.origin !== self.location.origin) return; // weather, rates: straight to network

  if (isPage(req)) {{
    event.respondWith(
      fetch(req, {{ cache: 'no-store' }})
        .then((res) => {{
          if (res && res.ok) {{ const copy = res.clone(); caches.open(CACHE_NAME).then((c) => c.put('./index.html', copy)); }}
          return res;
        }})
        .catch(() => caches.match('./index.html').then((r) => r || caches.match('./')))
    );
    return;
  }}

  event.respondWith(
    caches.match(req, {{ ignoreSearch: true }}).then((cached) => cached || fetch(req).then((res) => {{
      if (res && res.ok) {{ const copy = res.clone(); caches.open(CACHE_NAME).then((c) => c.put(req, copy)); }}
      return res;
    }}))
  );
}});
""")
print(len(files),'files')
