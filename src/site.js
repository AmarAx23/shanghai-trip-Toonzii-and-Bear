(function () {
  'use strict';
  var TRIP_START = '2026-12-05', TRIP_END = '2026-12-12', N_DAYS = 8;
  var DEPART = new Date('2026-12-05T16:45:00+07:00');
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  // Date/time in Shanghai
  function shNow() {
    var p = {}; new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    return { date: p.year + '-' + p.month + '-' + p.day, hm: p.hour + ':' + p.minute };
  }
  function dayIndexFor(iso) {
    var d = (Date.parse(iso + 'T00:00:00Z') - Date.parse(TRIP_START + 'T00:00:00Z')) / 864e5;
    return (d >= 0 && d < N_DAYS) ? d + 1 : 0;
  }

  // ---- Day tabs ----
  var tabs = $$('.dtab'), panels = $$('.day');
  function showDay(n, scrollTab) {
    n = String(n);
    panels.forEach(function (p) { p.classList.toggle('active', p.getAttribute('data-day') === n); });
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-day') === n;
      t.classList.toggle('active', on); t.setAttribute('aria-selected', on ? 'true' : 'false');
      if (on && scrollTab !== false) { var bar = t.parentNode; bar.scrollTo({ left: t.offsetLeft - (bar.clientWidth - t.offsetWidth) / 2, behavior: 'smooth' }); }
    });
  }
  tabs.forEach(function (t) { t.addEventListener('click', function () { showDay(t.getAttribute('data-day')); }); });
  function cur() { var a = $('.dtab.active'); return a ? parseInt(a.getAttribute('data-day'), 10) : 1; }
  document.addEventListener('keydown', function (e) {
    if (e.target && /input|textarea/i.test(e.target.tagName)) return;
    if (e.key === 'ArrowRight' && cur() < N_DAYS) showDay(cur() + 1);
    if (e.key === 'ArrowLeft' && cur() > 1) showDay(cur() - 1);
  });
  (function () {
    var box = $('.days'), sx = 0, sy = 0;
    if (!box) return;
    box.addEventListener('touchstart', function (e) { sx = e.changedTouches[0].clientX; sy = e.changedTouches[0].clientY; }, { passive: true });
    box.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
      if (dx < 0 && cur() < N_DAYS) showDay(cur() + 1);
      if (dx > 0 && cur() > 1) showDay(cur() - 1);
    }, { passive: true });
  })();

  // ---- Today mode ----
  function todayMode() {
    var now = shNow(), n = dayIndexFor(now.date), note = $('#today-note');
    $$('.dtab.today').forEach(function (t) { t.classList.remove('today'); });
    $$('.ev.next, .ev.past').forEach(function (e) { e.classList.remove('next', 'past'); });
    if (!n) { if (note) note.textContent = 'ปัดซ้าย-ขวาเพื่อเปลี่ยนวัน'; return 0; }
    var tab = $('.dtab[data-day="' + n + '"]'); if (tab) tab.classList.add('today');
    if (note) note.textContent = 'วันนี้: วันที่ ' + n;
    var found = false;
    $$('#day-' + n + ' .ev').forEach(function (e) {
      var t = e.getAttribute('data-t');
      if (!t) return;
      if (!found && t >= now.hm) { e.classList.add('next'); found = true; }
      else if (!found) e.classList.add('past');
    });
    return n;
  }
  var tn = todayMode();
  showDay(tn || 1, false);
  setInterval(todayMode, 60000);

  function IC(name, cls) { return '<svg class="ic' + (cls ? ' ' + cls : '') + '" aria-hidden="true"><use href="#i-' + name + '"/></svg>'; }
  var REDUCE = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Countdown (flip board) ----
  (function () {
    var msg = $('#cd-msg'), cd = $('#cd'), names = ['วัน', 'ชม.', 'นาที', 'วินาที'];
    cd.innerHTML = names.map(function (n) {
      return '<div class="unit"><div class="digits"><div class="fc"><i class="t"></i><i class="b"></i><i class="ft"></i><i class="fb"></i></div><div class="fc"><i class="t"></i><i class="b"></i><i class="ft"></i><i class="fb"></i></div></div><span>' + n + '</span></div>';
    }).join('');
    var cards = $$('.fc', cd);
    function setDigit(card, v) {
      // Classic split-flap: top half (old) folds down, then bottom half (new) falls into place.
      var t = card.children[0], b = card.children[1], ft = card.children[2], fb = card.children[3];
      if (t.textContent === v) return;
      var old = t.textContent;
      clearTimeout(card._done);
      if (!old || REDUCE || document.hidden) { t.textContent = b.textContent = v; card.classList.remove('go'); return; }
      t.textContent = v; ft.textContent = old; fb.textContent = v; b.textContent = old;
      card.classList.remove('go'); void card.offsetWidth; card.classList.add('go');
      card._done = setTimeout(function () { b.textContent = v; card.classList.remove('go'); }, 640);
    }
    function tick() {
      var diff = DEPART - new Date();
      if (diff <= 0) {
        cd.style.display = 'none';
        var n = dayIndexFor(shNow().date);
        msg.innerHTML = n ? IC('tree-pine') + ' วันที่ ' + n + ' ของทริป ขอให้เที่ยวสนุก!' : (new Date() < new Date(TRIP_END + 'T23:59:00+08:00') ? IC('plane') + ' ออกเดินทางแล้ว ขอให้เที่ยวสนุก!' : IC('party-popper') + ' จบทริปแล้ว ขอบคุณที่เที่ยวด้วยกัน');
        return;
      }
      var v = [Math.min(99, Math.floor(diff / 864e5)), Math.floor(diff % 864e5 / 36e5), Math.floor(diff % 36e5 / 6e4), Math.floor(diff % 6e4 / 1e3)];
      var s = v.map(function (n) { return String(n).padStart(2, '0'); }).join('');
      cards.forEach(function (c, i) { setDigit(c, s[i]); });
      cd.setAttribute('aria-label', 'อีก ' + v[0] + ' วัน ' + v[1] + ' ชั่วโมง ' + v[2] + ' นาที ถึงวันเดินทาง');
    }
    // Tick exactly on each second boundary so every flip starts at the same moment.
    (function loop() { tick(); setTimeout(loop, 1000 - (Date.now() % 1000) + 5); })();
  })();

  // ---- Day maps: schematic route drawn from approximate coordinates ----
  var drawMap = (function () {
    var NS = 'http://www.w3.org/2000/svg';
    // Rough line of the Huangpu River, just for orientation
    var RIVER = [[31.330,121.505],[31.290,121.522],[31.262,121.508],[31.248,121.494],[31.240,121.491],[31.231,121.495],[31.221,121.500],[31.210,121.495],[31.199,121.484],[31.185,121.470],[31.168,121.466],[31.150,121.472],[31.122,121.458],[31.095,121.425],[31.06,121.36],[31.02,121.25]];
    function el(tag, attrs, parent) { var n = document.createElementNS(NS, tag); for (var k in attrs) n.setAttribute(k, attrs[k]); if (parent) parent.appendChild(n); return n; }
    return function (fig) {
      var svg = fig.querySelector('.msvg'), w = svg.clientWidth, h = svg.clientHeight;
      if (!w) return;
      var g; try { g = JSON.parse(fig.getAttribute('data-geo')); } catch (e) { return; }
      var pts = g.route.map(function (p) { return p.hotel ? { lat: g.hotel.lat, lng: g.hotel.lng, hotel: 1 } : p; });
      var lat0 = pts.reduce(function (a, p) { return a + p.lat; }, 0) / pts.length, k = Math.cos(lat0 * Math.PI / 180);
      var xs = pts.map(function (p) { return p.lng * k; }), ys = pts.map(function (p) { return -p.lat; });
      var minX = Math.min.apply(null, xs), maxX = Math.max.apply(null, xs), minY = Math.min.apply(null, ys), maxY = Math.max.apply(null, ys);
      var spanX = Math.max(maxX - minX, 0.012), spanY = Math.max(maxY - minY, 0.008), pad = 30;
      var s = Math.min((w - pad * 2) / spanX, (h - pad * 2) / spanY);
      var cx = (minX + maxX) / 2, cy = (minY + maxY) / 2;
      function P(lat, lng) { return [w / 2 + (lng * k - cx) * s, h / 2 + (-lat - cy) * s]; }
      svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var rv = RIVER.map(function (r) { return P(r[0], r[1]); });
      el('polyline', { 'class': 'river', points: rv.map(function (p) { return p[0].toFixed(1) + ',' + p[1].toFixed(1); }).join(' ') }, svg);
      var lab = rv.filter(function (p) { return p[0] > 20 && p[0] < w - 60 && p[1] > 14 && p[1] < h - 10; })[0];
      if (lab) { var t = el('text', { 'class': 'rlabel', x: lab[0] + 8, y: lab[1] }, svg); t.textContent = 'แม่น้ำหวงผู่'; }
      var xy = pts.map(function (p) { return P(p.lat, p.lng); });
      var d = xy.map(function (p, i) {
        if (!i) return 'M' + p[0].toFixed(1) + ' ' + p[1].toFixed(1);
        var q = xy[i - 1], mx = (q[0] + p[0]) / 2, my = (q[1] + p[1]) / 2, dx = p[0] - q[0], dy = p[1] - q[1];
        return 'Q' + (mx - dy * 0.18).toFixed(1) + ' ' + (my + dx * 0.18).toFixed(1) + ' ' + p[0].toFixed(1) + ' ' + p[1].toFixed(1);
      }).join(' ');
      // the trip back to the hotel is drawn lighter so the day's order stays readable
      var segs = d.split(' Q'), back = null;
      if (pts.length > 2 && pts[pts.length - 1].hotel && !pts[0].hotel === false) {
        var last = segs.pop(), prev = xy[xy.length - 2];
        back = el('path', { 'class': 'path back', d: 'M' + prev[0].toFixed(1) + ' ' + prev[1].toFixed(1) + ' Q' + last }, svg);
        d = segs.join(' Q');
      }
      var path = el('path', { 'class': 'path', d: d }, svg);
      if (!REDUCE) {
        var len = Math.ceil(path.getTotalLength());
        path.style.strokeDasharray = len; path.style.setProperty('--len', len); path.classList.add('draw');
        path.addEventListener('animationend', function () { path.style.strokeDasharray = ''; path.classList.remove('draw'); }, { once: true });
      }
      var n = 0, seenHotel = false;
      pts.forEach(function (p, i) {
        if (p.hotel) { if (seenHotel) return; seenHotel = true; }
        var grp = el('g', { 'class': 'pin' + (p.hotel ? ' home' : ''), transform: 'translate(' + xy[i][0].toFixed(1) + ' ' + xy[i][1].toFixed(1) + ')' }, svg);
        grp.style.animationDelay = (REDUCE ? 0 : 0.15 + i * 0.12) + 's';
        el('circle', { r: p.hotel ? 12 : 11 }, grp);
        if (p.hotel) el('use', { href: '#i-hotel', x: -7, y: -7, width: 14, height: 14, 'class': 'hic' }, grp);
        else { var tx = el('text', {}, grp); tx.textContent = String(++n); }
        if (!p.hotel) { var tt = el('title', {}, grp); tt.textContent = p.t + ' ' + p.name; grp.addEventListener('click', function () { goTo(p.id); }); }
      });
    };
  })();
  function goTo(id) {
    var ev = document.getElementById(id); if (!ev) return;
    ev.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth', block: 'center' });
    ev.classList.remove('flash'); void ev.offsetWidth; ev.classList.add('flash');
  }
  $$('.mleg').forEach(function (b) { b.addEventListener('click', function () { goTo(b.getAttribute('data-go')); }); });

  // ---- Real maps: Leaflet + OpenStreetMap tiles, falling back to the schematic when tiles can't load ----
  var realMap = (function () {
    var state = 'idle', waiters = [], failed = false;
    // OpenStreetMap tiles (no key needed); colours are softened / inverted with CSS to match the theme
    function tileUrl() { return 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'; }
    function loadLeaflet(cb) {
      if (window.L) return cb(true);
      waiters.push(cb);
      if (state === 'loading') return;
      state = 'loading';
      var sc = document.createElement('script');
      sc.src = 'vendor/leaflet/leaflet.js';
      sc.onload = function () { state = 'ready'; waiters.splice(0).forEach(function (f) { f(true); }); };
      sc.onerror = function () { state = 'error'; waiters.splice(0).forEach(function (f) { f(false); }); };
      document.head.appendChild(sc);
    }
    function curve(a, b) {
      var mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[1] - a[1], dy = b[0] - a[0];
      var c = [mx + dx * 0.15, my - dy * 0.15], out = [];
      for (var t = 0; t <= 1.0001; t += 0.05) {
        var u = 1 - t; out.push([u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1]]);
      }
      return out;
    }
    function fallback(fig, why) {
      fig.classList.remove('real');
      var n = fig.querySelector('.mnote'); if (n) n.innerHTML = 'แผนผังคร่าว ๆ (' + why + ') · ' + IC('hotel') + ' = ที่พัก';
      drawMap(fig);
    }
    function build(fig) {
      var g; try { g = JSON.parse(fig.getAttribute('data-geo')); } catch (e) { return fallback(fig, 'ข้อมูลผิดพลาด'); }
      var box = fig.querySelector('.lmap');
      fig.classList.add('real');
      var map = L.map(box, { zoomControl: true, attributionControl: true, scrollWheelZoom: false, dragging: !L.Browser.mobile, tap: false, zoomSnap: 1,
        minZoom: g.minZoom || 3, maxZoom: g.maxZoom || 16, maxBounds: g.view ? L.latLngBounds(g.view).pad(0.6) : null, maxBoundsViscosity: 0.8 });
      map.attributionControl.setPrefix(false);
      var layer = L.tileLayer(tileUrl(), { maxZoom: 19, crossOrigin: true,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors' });
      var loaded = false, errors = 0;
      layer.on('tileload', function () { loaded = true; });
      var why = function () { return navigator.onLine === false ? 'ออฟไลน์ และยังไม่ได้เก็บแผนที่ไว้' : 'โหลดแผนที่ไม่ได้'; };
      layer.on('tileerror', function () { if (!loaded && ++errors >= 3) { failed = navigator.onLine !== false; map.remove(); fig._map = null; fallback(fig, why()); } });
      layer.addTo(map);
      setTimeout(function () { if (!loaded && fig._map) { failed = navigator.onLine !== false; map.remove(); fig._map = null; fallback(fig, why()); } }, 6000);
      var pts = g.route.map(function (p) { return p.hotel ? { lat: g.hotel.lat, lng: g.hotel.lng, hotel: 1 } : p; });
      var ll = pts.map(function (p) { return [p.lat, p.lng]; });
      var backLeg = pts.length > 2 && pts[pts.length - 1].hotel && pts[0].hotel;
      var main = [], i;
      for (i = 1; i < ll.length - (backLeg ? 1 : 0); i++) main = main.concat(curve(ll[i - 1], ll[i]));
      var route = L.polyline(main, { className: 'lroute', interactive: false }).addTo(map);
      if (backLeg) L.polyline(curve(ll[ll.length - 2], ll[ll.length - 1]), { className: 'lroute back', interactive: false }).addTo(map);
      var n = 0, seenHotel = false;
      pts.forEach(function (p, k) {
        if (p.hotel) { if (seenHotel) return; seenHotel = true; }
        var label = p.hotel ? IC('hotel') : String(++n);
        var icon = L.divIcon({ className: '', html: '<div class="lpin' + (p.hotel ? ' home' : '') + '" style="animation-delay:' + (REDUCE ? 0 : 0.2 + k * 0.12) + 's">' + label + '</div>', iconSize: p.hotel ? [28, 28] : [24, 24], iconAnchor: p.hotel ? [14, 14] : [12, 12] });
        var m = L.marker([p.lat, p.lng], { icon: icon, title: p.hotel ? 'ที่พัก' : p.t + ' ' + p.name, keyboard: true }).addTo(map);
        if (!p.hotel) m.on('click', function () { goTo(p.id); });
      });
      fig._map = map; fig._layer = layer; fig._bounds = L.latLngBounds(ll).pad(0.12); fig._route = route;
      map.fitBounds(fig._bounds, { padding: [24, 24], maxZoom: g.maxZoom || 15 });
      animateRoute(fig);
    }
    function animateRoute(fig) {
      var el = fig._route && fig._route.getElement && fig._route.getElement();
      if (!el || REDUCE) { if (el) el.classList.add('dash'); return; }
      var len = Math.ceil(el.getTotalLength());
      el.classList.remove('dash');
      el.style.transition = 'none'; el.style.strokeDasharray = len; el.style.strokeDashoffset = len;
      void el.getBoundingClientRect();
      el.style.transition = 'stroke-dashoffset 1.4s cubic-bezier(.4,0,.2,1)'; el.style.strokeDashoffset = '0';
      setTimeout(function () { el.style.transition = ''; el.style.strokeDasharray = ''; el.style.strokeDashoffset = ''; el.classList.add('dash'); }, 1500);
    }
    return {
      show: function (fig) {
        if (failed) return fallback(fig, 'โหลดแผนที่ไม่ได้');
        if (fig._map) { fig.classList.add('real'); fig._map.invalidateSize(); fig._map.fitBounds(fig._bounds, { padding: [24, 24], maxZoom: fig._map.getMaxZoom() }); animateRoute(fig); return; }
        loadLeaflet(function (ok) { if (!ok) { failed = true; return fallback(fig, 'โหลดแผนที่ไม่ได้'); } build(fig); });
      },
      retheme: function () {}
    };
  })();
  new MutationObserver(function () { realMap.retheme(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  function drawActiveMap() { var f = $('.day.active .dmap'); if (f) realMap.show(f); }
  var _show = showDay;
  showDay = function (n, sc) { _show(n, sc); requestAnimationFrame(drawActiveMap); document.dispatchEvent(new Event('daychange')); };
  window.addEventListener('resize', function () { clearTimeout(drawActiveMap._t); drawActiveMap._t = setTimeout(function () { var f = $('.day.active .dmap'); if (!f) return; if (f._map) f._map.invalidateSize(); else drawMap(f); }, 150); });
  drawActiveMap();

  // ---- Scroll reveal ----
  (function () {
    if (REDUCE || !('IntersectionObserver' in window)) return;
    var sel = '.sec-h, .wx, .days, .pass, details.more, #budget .card, #prep .card, .taxi, .phrases, .sos-grid, .tips, .install, .ev';
    var items = $$(sel);
    document.documentElement.classList.add('rv');
    var io = new IntersectionObserver(function (es) {
      var batch = 0;
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.style.setProperty('--rd', (batch++ * 0.07) + 's');
        e.target.classList.add('in'); io.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
    items.forEach(function (it) { it.classList.add('reveal'); io.observe(it); });
    // events in a newly opened day: replay the rise
    document.addEventListener('daychange', function () {
      $$('.day.active .ev').forEach(function (ev, i) { io.unobserve(ev); ev.classList.remove('in'); ev.style.setProperty('--rd', (i * 0.06) + 's'); void ev.offsetWidth; ev.classList.add('in'); });
    });
  })();

  // ---- Install-as-app card ----
  (function () {
    var box = $('#install'); if (!box) return;
    var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone;
    if (standalone || store('hkTripInstallDismissed') === '1') return;
    var ua = navigator.userAgent, ios = /iphone|ipad|ipod/i.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
    var deferred = null;
    function show() { box.hidden = false; }
    if (ios) { $('#ins-ios').hidden = false; show(); }
    window.addEventListener('beforeinstallprompt', function (e) {
      e.preventDefault(); deferred = e; $('#ins-btn').hidden = false; show();
    });
    $('#ins-btn').addEventListener('click', function () {
      if (!deferred) return; deferred.prompt();
      deferred.userChoice.then(function () { box.hidden = true; deferred = null; });
    });
    window.addEventListener('appinstalled', function () { box.hidden = true; });
    $('#ins-x').addEventListener('click', function () { box.hidden = true; store('hkTripInstallDismissed', '1'); });
  })();

  // ---- Plane flying along each boarding-pass route ----
  (function () {
    var routes = $$('.mid.fly');
    function fit(m) {
      var w = m.clientWidth, h = m.clientHeight, d = 'M 6 ' + (h - 18) + ' Q ' + (w / 2) + ' ' + (-h * 0.55) + ' ' + (w - 6) + ' ' + (h - 18);
      m.querySelector('svg').setAttribute('viewBox', '0 0 ' + w + ' ' + h);
      m.querySelector('path').setAttribute('d', d);
      m.querySelector('.plane').style.offsetPath = 'path("' + d + '")';
    }
    function progress(m) {
      var now = Date.now(), dep = Date.parse(m.getAttribute('data-dep')), arr = Date.parse(m.getAttribute('data-arr'));
      if (now <= dep) return null;
      return Math.min(1, (now - dep) / (arr - dep));
    }
    function fly(m) {
      var p = progress(m), plane = m.querySelector('.plane');
      if (p === null) { m.classList.add('landed'); plane.style.offsetDistance = ''; }
      else { m.classList.remove('landed'); plane.style.offsetDistance = (p * 100).toFixed(1) + '%'; }
    }
    routes.forEach(fit);
    window.addEventListener('resize', function () { routes.forEach(fit); });
    if (REDUCE || !('IntersectionObserver' in window)) { routes.forEach(function (m) { m.querySelector('.plane').style.transition = 'none'; fly(m); }); return; }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { fly(e.target); io.unobserve(e.target); } });
    }, { threshold: 0.6 });
    routes.forEach(function (m) { io.observe(m); m.addEventListener('click', function () {
      var plane = m.querySelector('.plane'); m.classList.remove('landed'); plane.style.offsetDistance = '0%';
      void plane.offsetWidth; setTimeout(function () { plane.style.offsetDistance = ''; fly(m); }, 60);
    }); });
    setInterval(function () { routes.forEach(function (m) { if (progress(m) !== null) fly(m); }); }, 60000);
  })();

  // ---- Snow ----
  (function () {
    var c = $('#snow'), btn = $('#snow-btn'), x = c.getContext && c.getContext('2d');
    if (!x) return;
    var saved = store('hkTripSnow'), on = saved ? saved === 'on' : !REDUCE, flakes = [], w = 0, h = 0, running = false;
    function size() {
      var r = window.devicePixelRatio || 1; w = innerWidth; h = innerHeight;
      c.width = w * r; c.height = h * r; x.setTransform(r, 0, 0, r, 0, 0);
    }
    function make() {
      flakes = [];
      var n = Math.round(Math.min(70, w * h / 12000));
      for (var i = 0; i < n; i++) flakes.push({ x: Math.random() * w, y: Math.random() * h, r: 1 + Math.random() * 2.4, s: 0.3 + Math.random() * 0.8, p: Math.random() * 6 });
    }
    function frame() {
      x.clearRect(0, 0, w, h);
      if (!on) { running = false; return; }
      var dark = document.documentElement.getAttribute('data-theme') === 'dark';
      x.fillStyle = dark ? 'rgba(255,255,255,.4)' : 'rgba(110,145,175,.45)';
      for (var i = 0; i < flakes.length; i++) {
        var f = flakes[i]; f.y += f.s; f.p += 0.01; f.x += Math.sin(f.p) * 0.3;
        if (f.y > h + 4) { f.y = -4; f.x = Math.random() * w; }
        x.beginPath(); x.arc(f.x, f.y, f.r, 0, 6.283); x.fill();
      }
      requestAnimationFrame(frame);
    }
    function start() { if (!running && on) { running = true; requestAnimationFrame(frame); } }
    function setOn(v) { on = v; btn.setAttribute('aria-pressed', v ? 'true' : 'false'); btn.title = v ? 'ปิดหิมะ' : 'เปิดหิมะ'; store('hkTripSnow', v ? 'on' : 'off'); start(); }
    size(); make();
    window.addEventListener('resize', function () { size(); make(); });
    btn.addEventListener('click', function () { setOn(!on); });
    btn.setAttribute('aria-pressed', on ? 'true' : 'false'); btn.title = on ? 'ปิดหิมะ' : 'เปิดหิมะ';
    start();
  })();

  // ---- Weather (Open-Meteo, falls back to December averages) ----
  (function () {
    var wx = $('#wx'), note = $('#wx-note');
    var DOW = ['อา.', 'จ.', 'อ.', 'พ.', 'พฤ.', 'ศ.', 'ส.'];
    function icon(c) { return c <= 1 ? 'sun' : c <= 3 ? 'cloud-sun' : c <= 48 ? 'cloud-fog' : c <= 57 ? 'cloud-drizzle' : c <= 67 ? 'cloud-rain' : c <= 77 ? 'cloud-snow' : c <= 82 ? 'cloud-rain' : 'cloud-lightning'; }
    function label(iso) { var d = new Date(iso + 'T00:00:00Z'); return DOW[d.getUTCDay()] + ' ' + d.getUTCDate(); }
    // fallback: averages from the day headers
    wx.innerHTML = $$('.wxb').map(function (b) {
      var tmp = (b.querySelector('.wxt') || b).textContent.replace('กลางคืน', '').trim();
      return '<div class="trip"><div class="d">' + label(b.getAttribute('data-date')) + '</div><div class="i">' + IC(b.getAttribute('data-ic') || 'cloud') + '</div><div class="t">' + tmp + '</div></div>';
    }).join('');
    var today = shNow().date;
    var daysToTrip = (Date.parse(TRIP_START) - Date.parse(today)) / 864e5;
    var inRange = daysToTrip <= 14 && today <= TRIP_END;
    var url = 'https://api.open-meteo.com/v1/forecast?latitude=31.21&longitude=121.45&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=Asia%2FShanghai'
      + (inRange ? '&start_date=' + (today > TRIP_START ? today : TRIP_START) + '&end_date=' + TRIP_END : '&forecast_days=7');
    fetch(url).then(function (r) { return r.json(); }).then(function (j) {
      var d = j && j.daily; if (!d || !d.time) return;
      wx.innerHTML = d.time.map(function (t, i) {
        var hi = Math.round(d.temperature_2m_max[i]), lo = Math.round(d.temperature_2m_min[i]), ic = icon(d.weathercode[i]);
        var trip = t >= TRIP_START && t <= TRIP_END;
        if (trip) $$('.wxb[data-date="' + t + '"]').forEach(function (b) { b.setAttribute('data-ic', ic); b.innerHTML = IC(ic) + '<span class="wxt">' + lo + '–' + hi + '°C (พยากรณ์)</span>'; });
        return '<div' + (trip ? ' class="trip"' : '') + '><div class="d">' + label(t) + '</div><div class="i">' + IC(ic) + '</div><div class="t">' + hi + '° <small>' + lo + '°</small></div></div>';
      }).join('');
      note.textContent = inRange ? 'พยากรณ์จริงช่วงทริป' : 'พยากรณ์ 7 วันข้างหน้า · ใกล้วันเดินทางจะเปลี่ยนเป็นช่วงทริปเอง';
    }).catch(function () {});
  })();

  // ---- Lightbox ----
  (function () {
    var ov = $('#lightbox-overlay'), im = $('#lightbox-img');
    $$('.thumb').forEach(function (img) { img.addEventListener('click', function () { im.src = img.src; im.alt = img.alt; ov.classList.add('active'); }); });
    function close() { ov.classList.remove('active'); im.src = ''; }
    ov.addEventListener('click', function (e) { if (e.target === ov || e.target.id === 'lightbox-close') close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  })();

  // ---- Speak Chinese ----
  function say(t) {
    try { speechSynthesis.cancel(); var u = new SpeechSynthesisUtterance(t); u.lang = 'zh-CN'; u.rate = 0.85; speechSynthesis.speak(u); } catch (e) {}
  }
  $$('[data-say]').forEach(function (b) { b.addEventListener('click', function () { say(b.getAttribute('data-say')); }); });

  // ---- Currency (CNY -> THB) ----
  (function () {
    var input = $('#cny-input'), result = $('#thb-result'), meta = $('#currency-meta'), RATE_KEY = 'hkTripCnyThbRate', rate = null;
    function render() {
      var v = parseFloat(input.value);
      if (isNaN(v) || rate === null) { result.textContent = '= 0.00 ฿'; return; }
      result.textContent = '= ' + (v * rate).toLocaleString('th-TH', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' ฿';
    }
    function applyRate(r, src, date) { rate = r; meta.textContent = '1 ¥ ≈ ' + r.toFixed(3) + ' ฿ · ' + src + (date ? ' (' + date + ')' : ''); render(); }
    try { var c = JSON.parse(store(RATE_KEY) || 'null'); if (c && c.rate) applyRate(c.rate, 'เรทล่าสุดที่บันทึกไว้', c.date); } catch (e) {}
    function save(r, d) { store(RATE_KEY, JSON.stringify({ rate: r, date: d })); }
    fetch('https://api.frankfurter.app/latest?from=CNY&to=THB').then(function (r) { return r.json(); }).then(function (d) {
      if (d && d.rates && d.rates.THB) { applyRate(d.rates.THB, 'อัปเดตล่าสุด', d.date); save(d.rates.THB, d.date); return; }
      throw new Error('no rate');
    }).catch(function () {
      return fetch('https://open.er-api.com/v6/latest/CNY').then(function (r) { return r.json(); }).then(function (d) {
        if (d && d.rates && d.rates.THB) { var dt = d.time_last_update_utc ? new Date(d.time_last_update_utc).toISOString().slice(0, 10) : ''; applyRate(d.rates.THB, 'อัปเดตล่าสุด', dt); save(d.rates.THB, dt); return; }
        throw new Error('no rate');
      });
    }).catch(function () { if (rate === null) meta.textContent = 'โหลดเรทไม่ได้ ลองใหม่เมื่อมีอินเทอร์เน็ต'; });
    input.addEventListener('input', render);
    $$('.cny-chip').forEach(function (c) { c.addEventListener('click', function () { input.value = c.getAttribute('data-v'); render(); }); });
  })();

  // ---- Packing checklist (same storage key as before, ticks are kept) ----
  (function () {
    var KEY = 'hkTripPackingChecklist', saved = {};
    try { saved = JSON.parse(store(KEY) || '{}') || {}; } catch (e) { saved = {}; }
    var boxes = $$('.packing-item input'), fill = $('#pack-bar-fill'), count = $('#pack-count');
    var doneBox = $('#pack-done');
    function upd(byUser) {
      var n = boxes.filter(function (b) { return b.checked; }).length, all = n === boxes.length;
      fill.style.width = (n / boxes.length * 100) + '%';
      count.textContent = n + '/' + boxes.length;
      if (doneBox) {
        var was = !doneBox.hidden; doneBox.hidden = !all;
        if (all && byUser && !was) { doneBox.classList.remove('pop'); void doneBox.offsetWidth; doneBox.classList.add('pop'); celebrate(doneBox); }
      }
    }
    boxes.forEach(function (cb) {
      var k = cb.getAttribute('data-key');
      if (saved[k]) { cb.checked = true; cb.closest('.packing-item').classList.add('checked'); }
      cb.addEventListener('change', function () {
        saved[k] = cb.checked; store(KEY, JSON.stringify(saved));
        cb.closest('.packing-item').classList.toggle('checked', cb.checked); upd(true);
      });
    });
    upd();
  })();

  // ---- Bottom nav highlight ----
  (function () {
    var links = $$('.bnav a'), secs = links.map(function (a) { return document.getElementById(a.getAttribute('data-sec')); });
    function onScroll() {
      var y = window.scrollY + window.innerHeight * 0.35, idx = -1;
      secs.forEach(function (s, i) { if (s && s.offsetTop <= y) idx = i; });
      links.forEach(function (a, i) { a.classList.toggle('on', i === idx); });
    }
    window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  })();

  // ---- Share / print / QR ----
  function flash(btn, txt) { toast(txt, null, 1800); }
  function copy(btn) { if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { flash(btn, IC('circle-check') + ' คัดลอกลิงก์แล้ว'); }); }
  $('#share-btn').addEventListener('click', function () {
    var b = this, data = { title: document.title, text: 'แผนเที่ยวเซี่ยงไฮ้ 8 วัน 7 คืน ธันวาคม 2026', url: location.href };
    if (navigator.share) navigator.share(data).catch(function () {}); else copy(b);
  });
  $('#print-btn').addEventListener('click', function () { window.print(); });
  (function () {
    var ov = $('#qr-modal-overlay'), md = $('#qr-modal');
    function open() {
      $('#qr-modal-img').src = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(location.href);
      $('#qr-modal-url').textContent = location.href; ov.classList.add('active'); md.classList.add('active');
    }
    function close() { ov.classList.remove('active'); md.classList.remove('active'); }
    $('#qr-btn').addEventListener('click', open); $('#qr-modal-close').addEventListener('click', close); ov.addEventListener('click', close);
    $('#qr-copy-btn').addEventListener('click', function () { copy(this); });
  })();

  // ---- Dark mode toggle ----
  (function () {
    var btn = $('#theme-toggle-btn'), root = document.documentElement;
    function apply(t) { if (t === 'dark') { root.setAttribute('data-theme', 'dark'); btn.classList.add('on'); } else { root.removeAttribute('data-theme'); btn.classList.remove('on'); } }
    apply(root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');
    btn.addEventListener('click', function () { var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; apply(next); store('hkTripTheme', next); });
  })();

  // ---- Offline maps: save every day's OpenStreetMap tiles into the same cache the service worker serves from ----
  (function () {
    var box = $('#offmap'); if (!box || !('caches' in window)) { if (box) box.hidden = true; return; }
    var TILE_CACHE = 'sh-tiles-v1', BASE = 'https://tile.openstreetmap.org/';
    var tiles; try { tiles = JSON.parse(box.getAttribute('data-tiles')); } catch (e) { tiles = []; }
    var btn = $('#om-btn'), fill = $('#om-fill'), status = $('#om-status'), busy = false;
    function show(n, msg) {
      fill.style.width = Math.round(n / tiles.length * 100) + '%';
      if (msg) status.textContent = msg;
      var done = n >= tiles.length;
      box.classList.toggle('done', done);
      btn.innerHTML = done ? IC('circle-check') + ' เก็บแผนที่ครบแล้ว · อัปเดตอีกครั้ง' : IC('download') + ' เก็บแผนที่ไว้ใช้ออฟไลน์';
    }
    function countCached() {
      return caches.open(TILE_CACHE).then(function (c) { return c.keys(); }).then(function (keys) {
        var have = {}; keys.forEach(function (r) { have[r.url] = 1; });
        return tiles.filter(function (t) { return have[BASE + t + '.png']; }).length;
      });
    }
    countCached().then(function (n) {
      show(n, n >= tiles.length ? 'เก็บแผนที่ของทั้ง 8 วันไว้ในเครื่องแล้ว เปิดได้แม้ไม่มีเน็ต' : (n ? 'เก็บไว้แล้ว ' + n + '/' + tiles.length + ' ชิ้น กดเพื่อเก็บให้ครบ' : null));
    }).catch(function () {});
    btn.addEventListener('click', function () {
      if (busy) return;
      if (navigator.onLine === false) { toast('ต่อเน็ตก่อนแล้วค่อยกดเก็บแผนที่', null, 2200); return; }
      busy = true; btn.disabled = true;
      var refresh = box.classList.contains('done'), i = 0, ok = 0, fail = 0;
      caches.open(TILE_CACHE).then(function (cache) {
        function next() {
          if (i >= tiles.length) return Promise.resolve();
          var url = BASE + tiles[i++] + '.png';
          return (refresh ? Promise.resolve(null) : cache.match(url)).then(function (hit) {
            if (hit) { ok++; return; }
            return fetch(url, { mode: 'cors', credentials: 'omit' }).then(function (r) {
              if (!r.ok) throw new Error(r.status);
              return cache.put(url, r).then(function () { ok++; });
            }).catch(function () { fail++; });
          }).then(function () { show(ok, 'กำลังเก็บแผนที่ ' + ok + '/' + tiles.length + '…'); return next(); });
        }
        // a few at a time, to be gentle with the OpenStreetMap servers
        return Promise.all([next(), next(), next()]);
      }).then(function () {
        busy = false; btn.disabled = false;
        if (fail) show(ok, 'เก็บได้ ' + ok + '/' + tiles.length + ' ชิ้น บางส่วนโหลดไม่สำเร็จ ลองกดอีกครั้ง');
        else { show(ok, 'เก็บแผนที่ของทั้ง 8 วันไว้ในเครื่องแล้ว เปิดได้แม้ไม่มีเน็ต'); toast(IC('circle-check') + ' เก็บแผนที่ครบ ' + ok + ' ชิ้นแล้ว', null, 2200); }
      }).catch(function () { busy = false; btn.disabled = false; show(ok, 'เก็บแผนที่ไม่สำเร็จ ลองใหม่อีกครั้ง'); });
    });
  })();

  // ---- Mascot: splash, hero bear, celebration ----
  (function () {
    var sp = $('#splash');
    if (sp) {
      var hide = function () { sp.classList.add('out'); setTimeout(function () { sp.remove(); }, 450); };
      if (document.documentElement.classList.contains('nosplash')) sp.remove();
      else { var t0 = Date.now(); window.addEventListener('load', function () { setTimeout(hide, Math.max(0, 700 - (Date.now() - t0))); }); setTimeout(hide, 1600); }
    }
    var hb = $('#hero-bear');
    if (hb) hb.addEventListener('click', function () {
      var days = Math.ceil((DEPART - Date.now()) / 864e5), n = dayIndexFor(shNow().date);
      var lines = n ? ['วันที่ ' + n + ' แล้ว เที่ยวให้สนุกนะ!', 'อย่าลืมถ่ายรูปเยอะ ๆ', 'หนาวไหม ใส่ผ้าพันคอด้วยนะ'] :
        days > 0 ? ['อีก ' + days + ' วันเจอกันที่เซี่ยงไฮ้!', 'เก็บแผนที่ออฟไลน์แล้วหรือยัง?', 'อย่าลืมกรอกบัตรขาเข้าออนไลน์ก่อนบิน 3 วันนะ', 'power bank ต้องมีโลโก้ 3C นะ', 'ตั้งค่า Alipay ไว้ก่อนไปด้วยนะ']
        : ['ขอบคุณที่พาไปเที่ยวนะ!'];
      hb.classList.remove('hop'); void hb.offsetWidth; hb.classList.add('hop');
      toast('<svg class="tb" aria-hidden="true"><use href="#bear"/></svg>' + lines[Math.floor(Math.random() * lines.length)], null, 2600);
    });
  })();
  function celebrate(anchor) {
    toast('<svg class="tb" aria-hidden="true"><use href="#bear"/></svg>เตรียมของครบแล้ว เย้!', null, 2600);
    if (REDUCE) return;
    var c = $('#confetti'), x = c && c.getContext && c.getContext('2d'); if (!x) return;
    var r = anchor.getBoundingClientRect(), ps = [], cols = ['#B0242E', '#C79A3F', '#E8C877', '#1D5C82', '#ffffff'];
    c.width = innerWidth; c.height = innerHeight;
    for (var i = 0; i < 110; i++) ps.push({ x: r.left + r.width / 2, y: r.top + 30, vx: (Math.random() - .5) * 11, vy: -5 - Math.random() * 9, a: Math.random() * 6, va: (Math.random() - .5) * .4, c: cols[i % 5], l: 150 });
    (function f() {
      x.clearRect(0, 0, c.width, c.height);
      ps = ps.filter(function (p) { return p.l-- > 0 && p.y < c.height + 20; });
      ps.forEach(function (p) { p.vy += .25; p.x += p.vx; p.y += p.vy; p.a += p.va; x.save(); x.translate(p.x, p.y); x.rotate(p.a); x.fillStyle = p.c; x.fillRect(-4, -2, 8, 4); x.restore(); });
      if (ps.length) requestAnimationFrame(f); else x.clearRect(0, 0, c.width, c.height);
    })();
  }

  // ---- Toast ----
  function toast(html, onTap, ms) {
    var t = $('#toast'); if (!t) return;
    t.innerHTML = html; t.classList.add('show'); t.onclick = onTap || null; t.style.cursor = onTap ? 'pointer' : '';
    clearTimeout(t._h); if (ms) t._h = setTimeout(function () { t.classList.remove('show'); }, ms);
  }

  // ---- Offline + auto-update (matters most for the app installed on the iPhone home screen) ----
  var BUILD = (document.querySelector('meta[name="build"]') || {}).content || '';
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('sw.js', { updateViaCache: 'none' }).then(function (reg) {
        document.addEventListener('visibilitychange', function () { if (!document.hidden) reg.update().catch(function () {}); });
      }).catch(function () {});
    });
  }
  // iOS keeps a home-screen app alive in the background, so check for a newer page whenever it comes back.
  function checkNewer() {
    if (!BUILD || navigator.onLine === false) return;
    fetch('index.html?check=' + Date.now(), { cache: 'no-store' }).then(function (r) { return r.ok ? r.text() : ''; }).then(function (html) {
      var m = html.match(/<meta name="build" content="(\d+)"/);
      if (m && m[1] > BUILD) toast(IC('sparkles') + ' มีเวอร์ชันใหม่ <b>แตะเพื่ออัปเดต</b>', function () { location.reload(); });
    }).catch(function () {});
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden) checkNewer(); });
  setTimeout(checkNewer, 4000);
})();
