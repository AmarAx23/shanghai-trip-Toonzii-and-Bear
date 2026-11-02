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
  // Jump to the first activity of the shown day, just below the sticky day tabs
  function toFirst() {
    requestAnimationFrame(function () {
      var tl = $('.day.active .tl'), ev = tl && tl.querySelector('.ev'), bar = $('#dtabs'); if (!ev) return;
      var stuck = bar.offsetHeight + (parseFloat(getComputedStyle(bar).top) || 0);
      var y = tl.getBoundingClientRect().top + window.pageYOffset + ev.offsetTop - stuck - 6;
      window.scrollTo({ top: Math.max(0, y), behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    });
  }
  function pick(n) { showDay(n); toFirst(); }
  tabs.forEach(function (t) { t.addEventListener('click', function () { pick(t.getAttribute('data-day')); }); });
  function cur() { var a = $('.dtab.active'); return a ? parseInt(a.getAttribute('data-day'), 10) : 1; }
  document.addEventListener('keydown', function (e) {
    if (e.target && /input|textarea/i.test(e.target.tagName)) return;
    if (e.key === 'ArrowRight' && cur() < N_DAYS) pick(cur() + 1);
    if (e.key === 'ArrowLeft' && cur() > 1) pick(cur() - 1);
  });
  (function () {
    var box = $('.days'), sx = 0, sy = 0;
    if (!box) return;
    box.addEventListener('touchstart', function (e) { sx = e.changedTouches[0].clientX; sy = e.changedTouches[0].clientY; }, { passive: true });
    box.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
      if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
      if (dx < 0 && cur() < N_DAYS) pick(cur() + 1);
      if (dx > 0 && cur() > 1) pick(cur() - 1);
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
        msg.textContent = n ? '🎄 วันที่ ' + n + ' ของทริป ขอให้เที่ยวสนุก!' : (new Date() < new Date(TRIP_END + 'T23:59:00+08:00') ? '✈️ ออกเดินทางแล้ว ขอให้เที่ยวสนุก!' : '🎉 จบทริปแล้ว ขอบคุณที่เที่ยวด้วยกัน');
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
        var tx = el('text', {}, grp); tx.textContent = p.hotel ? '🏨' : String(++n);
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
      var n = fig.querySelector('.mnote'); if (n) n.textContent = 'แผนผังคร่าว ๆ (' + why + ') · 🏨 = ที่พัก';
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
        var label = p.hotel ? '🏨' : String(++n);
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
    var sel = '.sec-h, .wx, .days, .passw, details.more, #budget .card, #prep .card, .taxi, .phrases, .sos-grid, .tips, .install, .ev';
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


  // ================= Motion set 2 =================
  // 4 · Flip boarding passes (links inside still work)
  $$('.passw').forEach(function (w) {
    function flip() { var on = w.classList.toggle('on'); w.querySelector('.pass-back').setAttribute('aria-hidden', on ? 'false' : 'true'); w.querySelector('.pass').setAttribute('aria-hidden', on ? 'true' : 'false'); }
    w.addEventListener('click', function (e) { if (e.target.closest('a')) return; flip(); });
    w.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flip(); } });
  });

  // 5 · Timeline line fills as you scroll; dots light up
  (function () {
    if (REDUCE) return;
    var raf = 0;
    function upd() {
      raf = 0;
      var tl = $('.day.active .tl'); if (!tl) return;
      var r = tl.getBoundingClientRect(), mid = innerHeight * 0.62;
      var p = Math.max(0, Math.min(1, (mid - r.top - 10) / Math.max(1, r.height - 20)));
      tl.style.setProperty('--tlp', p.toFixed(3));
      $$('.ev', tl).forEach(function (ev) { var d = ev.querySelector('.dot'); ev.classList.toggle('lit', d.getBoundingClientRect().top < mid); });
    }
    function q() { if (!raf) raf = requestAnimationFrame(upd); }
    addEventListener('scroll', q, { passive: true }); addEventListener('resize', q);
    document.addEventListener('daychange', function () { setTimeout(upd, 30); });
    upd();
  })();

  // 6 · Budget total counts up, bars grow
  (function () {
    var card = $('#budget .btotal'); if (!card) return; card = card.parentNode;
    var b = $('.btotal b', card), N = +b.getAttribute('data-n');
    if (REDUCE || !('IntersectionObserver' in window) || !N) return;
    card.classList.add('bgrow');
    $$('.bbar i', card).forEach(function (i, k) { i.style.setProperty('--bd', (0.15 + k * 0.12) + 's'); });
    b.textContent = '0 ฿';
    new IntersectionObserver(function (es, o) {
      if (!es[0].isIntersecting) return; o.disconnect();
      card.classList.add('go');
      var t0 = performance.now();
      (function step(t) { var k = Math.min(1, (t - t0) / 1300), e = 1 - Math.pow(1 - k, 3); b.textContent = Math.round(N * e).toLocaleString('en-US') + ' ฿'; if (k < 1) requestAnimationFrame(step); })(t0);
    }, { threshold: 0.4 }).observe(card);
  })();

  // 10 · Photo curtain reveal
  (function () {
    if (REDUCE || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('open'); io.unobserve(e.target); } });
    }, { threshold: 0.35 });
    $$('.day .ph').forEach(function (f) { f.classList.add('cur'); io.observe(f); });
    document.addEventListener('daychange', function () {
      $$('.day.active .ph').forEach(function (f) { if (f.classList.contains('open')) return; io.unobserve(f); io.observe(f); });
    });
  })();

  // 9 · Fireworks over the hero on special days (departure, Disney, last day) — or tap the title 3×
  (function () {
    var c = $('#fw'), x = c && c.getContext && c.getContext('2d'); if (!x || REDUCE) return;
    var parts = [], run = false, dpr = Math.min(2, window.devicePixelRatio || 1);
    var COLS = ['#F3DDA2', '#E26871', '#FFFFFF', '#8EC0E2', '#FFB36B', '#E8C877'];
    function loop() {
      x.globalCompositeOperation = 'destination-out'; x.fillStyle = 'rgba(0,0,0,.22)'; x.fillRect(0, 0, c.width, c.height);
      x.globalCompositeOperation = 'lighter';
      parts = parts.filter(function (p) { return p.l-- > 0; });
      parts.forEach(function (p) {
        p.vy += 0.045 * dpr; p.vx *= 0.975; p.vy *= 0.975; p.x += p.vx; p.y += p.vy;
        x.globalAlpha = Math.min(1, p.l / 40); x.fillStyle = p.c; x.beginPath(); x.arc(p.x, p.y, 1.6 * dpr, 0, 7); x.fill();
      });
      x.globalAlpha = 1;
      if (parts.length) requestAnimationFrame(loop); else { run = false; x.clearRect(0, 0, c.width, c.height); }
    }
    function burst(n) {
      c.width = c.clientWidth * dpr; c.height = c.clientHeight * dpr;
      for (var b = 0; b < n; b++) (function (b) {
        setTimeout(function () {
          var cx = c.width * (0.15 + Math.random() * 0.7), cy = c.height * (0.12 + Math.random() * 0.38), col = COLS[(Math.random() * COLS.length) | 0], m = 56;
          for (var i = 0; i < m; i++) { var a = Math.PI * 2 * i / m, s = (1.6 + Math.random() * 3) * dpr; parts.push({ x: cx, y: cy, vx: Math.cos(a) * s, vy: Math.sin(a) * s, l: 55 + Math.random() * 35, c: col }); }
          if (!run) { run = true; loop(); }
        }, b * 420);
      })(b);
    }
    var today = shNow().date, dis = $('.day .tag.gold') && $('.day .tag.gold').closest('.day');
    var special = [TRIP_START, TRIP_END, dis ? dis.getAttribute('data-date') : ''];
    if (special.indexOf(today) >= 0 || /[?&]fw=1/.test(location.search)) setTimeout(function () { burst(5); }, 900);
    var taps = 0, tt = 0, h = $('#hero-title');
    if (h) h.addEventListener('click', function () { taps++; clearTimeout(tt); tt = setTimeout(function () { taps = 0; }, 600); if (taps >= 3) { taps = 0; burst(4); } });
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
    function icon(c) { return c <= 1 ? '☀️' : c <= 3 ? '⛅' : c <= 48 ? '🌫️' : c <= 57 ? '🌦️' : c <= 67 ? '🌧️' : c <= 77 ? '🌨️' : c <= 82 ? '🌦️' : '⛈️'; }
    function label(iso) { var d = new Date(iso + 'T00:00:00Z'); return DOW[d.getUTCDay()] + ' ' + d.getUTCDate(); }
    // fallback: averages from the day headers
    wx.innerHTML = $$('.wxb').map(function (b) {
      var t = b.textContent, ic = t.split(' ')[0], tmp = t.replace(/^\S+\s*/, '').replace('กลางคืน', '').trim();
      return '<div class="trip"><div class="d">' + label(b.getAttribute('data-date')) + '</div><div class="i">' + ic + '</div><div class="t">' + tmp + '</div></div>';
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
        if (trip) $$('.wxb[data-date="' + t + '"]').forEach(function (b) { b.textContent = ic + ' ' + lo + '–' + hi + '°C (พยากรณ์)'; });
        return '<div' + (trip ? ' class="trip"' : '') + '><div class="d">' + label(t) + '</div><div class="i">' + ic + '</div><div class="t">' + hi + '° <small>' + lo + '°</small></div></div>';
      }).join('');
      note.innerHTML = inRange ? 'พยากรณ์จริงช่วงทริป' : 'พยากรณ์ 7 วันข้างหน้า<small>ใกล้ทริปจะเปลี่ยนเป็นวันเที่ยวเอง</small>';
    }).catch(function () {});
  })();

  // ---- Lightbox ----
  (function () {
    var ov = $('#lightbox-overlay'), im = $('#lightbox-img');
    var from = null, busy = false;
    // Transform that puts the big image exactly over the thumbnail (cover-cropped via clip-path)
    function overThumb(t) {
      var F = im.getBoundingClientRect(), T = t.getBoundingClientRect();
      if (!F.width || !T.width) return null;
      var k = Math.max(T.width / F.width, T.height / F.height);
      var vw = T.width / k, vh = T.height / k, ix = (F.width - vw) / 2, iy = (F.height - vh) / 2, r = 14 / k;
      var dx = (T.left + T.width / 2) - (F.left + F.width / 2), dy = (T.top + T.height / 2) - (F.top + F.height / 2);
      return { tf: 'translate(' + dx + 'px,' + dy + 'px) scale(' + k + ')', cp: 'inset(' + iy + 'px ' + ix + 'px round ' + r + 'px)' };
    }
    function set(tf, cp, anim) { im.style.transition = anim ? '' : 'none'; im.style.transform = tf; im.style.clipPath = im.style.webkitClipPath = cp; }
    $$('.thumb').forEach(function (img) { img.addEventListener('click', function () {
      if (busy) return;
      var src = img.currentSrc || img.src, big = src.replace(/-640\.webp$/, '-1280.webp');
      im.alt = img.alt; from = img;
      if (REDUCE) { im.src = big; ov.classList.add('active'); return; }
      im.src = src; ov.classList.add('active', 'zoom');
      var go = function () {
        var o = overThumb(img); if (!o) { ov.classList.add('open'); return; }
        set(o.tf, o.cp, false); img.style.visibility = 'hidden'; void im.offsetWidth;
        requestAnimationFrame(function () { ov.classList.add('open'); set('none', 'inset(0px 0px round 12px)', true); });
        if (big !== src) { var pre = new Image(); pre.onload = function () { if (from === img) im.src = big; }; pre.src = big; }
      };
      if (im.complete && im.naturalWidth) go(); else im.onload = function () { im.onload = null; go(); };
    }); });
    function close() {
      if (!ov.classList.contains('active') || busy) return;
      var t = from, o = (!REDUCE && t && ov.classList.contains('zoom')) ? overThumb(t) : null;
      function done() { ov.classList.remove('active', 'zoom', 'open'); set('', '', false); im.removeAttribute('src'); if (t) t.style.visibility = ''; from = null; busy = false; }
      if (!o) { done(); return; }
      busy = true; ov.classList.remove('open'); set(o.tf, o.cp, true); setTimeout(done, 460);
    }
    ov.addEventListener('click', function (e) { if (e.target === ov || e.target.id === 'lightbox-close') close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  })();

  // ---- Speak Chinese ----
  function say(t, lang) {
    try { speechSynthesis.cancel(); var u = new SpeechSynthesisUtterance(t); u.lang = lang || 'zh-CN'; u.rate = lang === 'th-TH' ? 0.95 : 0.85; speechSynthesis.speak(u); } catch (e) {}
  }
  $$('[data-say]').forEach(function (b) { b.addEventListener('click', function () { say(b.getAttribute('data-say')); }); });

  // ---- Translator Thai <-> Chinese ----
  (function () {
    var box = $('#tr'); if (!box) return;
    var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    var st = $('#tr-status'), log = $('#tr-log'), form = $('#tr-form'), inp = $('#tr-in'), dirB = $('#tr-dir'), clr = $('#tr-clear');
    var big = $('#tr-big'), KEY = 'hkTripTrLog', from = 'th', rec = null, items = [];
    var LANG = { th: { sr: 'th-TH', tts: 'th-TH', g: 'th', mm: 'th-TH' }, zh: { sr: 'zh-CN', tts: 'zh-CN', g: 'zh-CN', mm: 'zh-CN' } };
    function other(l) { return l === 'th' ? 'zh' : 'th'; }
    function status(t, err) { st.textContent = t || ''; st.classList.toggle('err', !!err); }
    function setDir(l) { from = l; dirB.textContent = l === 'th' ? 'ไทย → 中文' : '中文 → ไทย'; inp.placeholder = l === 'th' ? 'หรือพิมพ์ไทยตรงนี้ (กดไมค์บนคีย์บอร์ดก็ได้)' : '请在这里输入中文'; inp.lang = LANG[l].sr; }
    dirB.addEventListener('click', function () { setDir(other(from)); });
    function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    function withTimeout(url, ms) {
      var ac = window.AbortController ? new AbortController() : null, tm = setTimeout(function () { if (ac) ac.abort(); }, ms);
      return fetch(url, ac ? { signal: ac.signal } : {}).then(function (r) { clearTimeout(tm); if (!r.ok) throw new Error(r.status); return r.json(); });
    }
    // Google first (best quality, but blocked on Chinese networks) → MyMemory (works in China)
    function translate(text, f) {
      var t = other(f);
      var g = 'https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&dt=rm&sl=' + LANG[f].g + '&tl=' + LANG[t].g + '&q=' + encodeURIComponent(text);
      return withTimeout(g, 3500).then(function (j) {
        var rows = j[0] || [], out = '', py = '';
        rows.forEach(function (r) { if (r[0]) out += r[0]; else if (r[2]) py = r[2]; });
        if (!out) throw new Error('empty');
        return { text: out, py: t === 'zh' ? py : '' };
      }).catch(function () {
        var m = 'https://api.mymemory.translated.net/get?langpair=' + LANG[f].mm + '|' + LANG[t].mm + '&q=' + encodeURIComponent(text.slice(0, 480));
        return withTimeout(m, 9000).then(function (j) {
          var out = j && j.responseData && j.responseData.translatedText;
          if (!out || /MYMEMORY WARNING|QUERY LENGTH LIMIT/i.test(out)) throw new Error('mm');
          return { text: out, py: '' };
        });
      });
    }

    function save() { store(KEY, JSON.stringify(items.slice(-30))); clr.hidden = !items.length; }
    function bubble(it, i) {
      var t = other(it.f);
      return '<div class="tb ' + (it.f === 'th' ? 'me' : 'them') + (it.wait ? ' wait' : '') + '" data-i="' + i + '">'
        + '<div class="src" lang="' + LANG[it.f].sr + '">' + (it.f === 'th' ? '🇹🇭 ' : '🇨🇳 ') + esc(it.src) + '</div>'
        + '<div class="dst" lang="' + LANG[t].sr + '">' + esc(it.dst || '') + '</div>'
        + (it.py ? '<div class="py">' + esc(it.py) + '</div>' : '')
        + (it.dst ? '<div class="acts"><button type="button" data-a="say">🔊 ฟัง</button>' + (t === 'zh' ? '<button type="button" data-a="big">⛶ ยื่นให้ดู</button>' : '') + '</div>' : '')
        + '</div>';
    }
    function render() { log.innerHTML = items.map(bubble).reverse().join(''); }
    log.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-a]'); if (!b) return;
      var it = items[+b.closest('.tb').getAttribute('data-i')]; if (!it) return;
      if (b.getAttribute('data-a') === 'say') say(it.dst, LANG[other(it.f)].tts); else showBig(it);
    });
    clr.addEventListener('click', function () { items = []; save(); render(); status(''); });

    function run(text, f) {
      text = (text || '').trim(); if (!text) return;
      if (navigator.onLine === false) { status('ตอนนี้ไม่มีเน็ต ใช้ประโยคสำเร็จรูปด้านล่างแทนก่อนนะ', true); return; }
      var it = { f: f, src: text, dst: '', py: '', wait: true }; items.push(it); render(); status('');
      translate(text, f).then(function (r) {
        it.dst = r.text; it.py = r.py; delete it.wait; save(); render();
        say(r.text, LANG[other(f)].tts);
      }).catch(function () {
        items.splice(items.indexOf(it), 1); render();
        status('แปลไม่สำเร็จ ลองอีกครั้ง หรือเช็กอินเทอร์เน็ต', true);
      });
    }
    form.addEventListener('submit', function (e) { e.preventDefault(); var v = inp.value; inp.value = ''; inp.blur(); run(v, from); });
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit')); } });

    // Voice input
    function unlockTTS() { try { var u = new SpeechSynthesisUtterance(' '); u.volume = 0; speechSynthesis.speak(u); } catch (e) {} }
    function stop() { if (rec) { try { rec.stop(); } catch (e) {} } }
    function listen(l, btn) {
      unlockTTS();
      if (rec) { stop(); return; }
      if (!SR) {
        setDir(l); inp.focus();
        status(l === 'th' ? 'เครื่องนี้ใช้ไมค์ในเว็บไม่ได้ กดปุ่มไมค์ 🎤 บนคีย์บอร์ดแล้วพูดแทนได้เลย' : '请点键盘上的 🎤 说中文 · ให้พนักงานกดไมค์บนคีย์บอร์ด');
        return;
      }
      var r = new SR(), finalT = '', interim = '';
      r.lang = LANG[l].sr; r.interimResults = true; r.continuous = false; r.maxAlternatives = 1;
      r.onresult = function (e) {
        interim = '';
        for (var i = e.resultIndex; i < e.results.length; i++) { if (e.results[i].isFinal) finalT += e.results[i][0].transcript; else interim += e.results[i][0].transcript; }
        status('“' + (finalT + interim) + '”');
      };
      r.onerror = function (e) {
        var m = { 'not-allowed': 'ยังไม่ได้อนุญาตให้ใช้ไมค์ ไปที่ตั้งค่าเพื่ออนุญาต หรือพิมพ์แทน', 'service-not-allowed': 'เครื่องนี้ใช้ไมค์ในเว็บไม่ได้ กดไมค์บนคีย์บอร์ดแทน', 'no-speech': 'ไม่ได้ยินเสียง ลองกดแล้วพูดใหม่อีกครั้ง', 'network': 'ระบบฟังเสียงต่อเน็ตไม่ได้ ลองกดไมค์บนคีย์บอร์ดแทน' }[e.error];
        if (m) status(m, true);
      };
      r.onend = function () {
        btn.classList.remove('rec'); rec = null;
        var t = (finalT || interim).trim();
        if (t) run(t, l); else if (!st.classList.contains('err')) status('');
      };
      try { r.start(); rec = r; btn.classList.add('rec'); status(l === 'th' ? 'พูดภาษาไทยได้เลย…' : '请说中文…'); }
      catch (e) { status('เริ่มฟังไม่ได้ ลองอีกครั้ง', true); }
    }
    $$('.tr-mic', box).forEach(function (b) { b.addEventListener('click', function () { listen(b.getAttribute('data-lang'), b); }); });

    // Big "show the staff" view
    var cur = null;
    function showBig(it) {
      cur = it; $('#tb-zh').textContent = it.dst; $('#tb-py').textContent = it.py || ''; $('#tb-th').textContent = it.src;
      big.hidden = false; document.documentElement.style.overflow = 'hidden';
    }
    function hideBig() { big.hidden = true; document.documentElement.style.overflow = ''; }
    $('#tb-x').addEventListener('click', hideBig);
    $('#tb-say').addEventListener('click', function () { if (cur) say(cur.dst, 'zh-CN'); });
    $('#tb-reply').addEventListener('click', function () { hideBig(); box.scrollIntoView({ block: 'start' }); listen('zh', $('.tr-mic.zh', box)); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !big.hidden) hideBig(); });

    try { items = JSON.parse(store(KEY) || '[]').filter(function (x) { return x && x.dst; }); } catch (e) { items = []; }
    setDir('th'); render(); clr.hidden = !items.length;
  })();

  // ---- Currency (CNY -> THB) ----
  (function () {
    var input = $('#cny-input'), result = $('#thb-result'), meta = $('#currency-meta'), RATE_KEY = 'hkTripCnyThbRate', rate = null;
    function render() {
      var v = parseFloat(input.value);
      var str = (isNaN(v) || rate === null) ? '0.00' : (v * rate).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      odo(str);
    }
    var odoEl = null, odoStr = '';
    function odo(str) {
      if (REDUCE) { result.textContent = '= ' + str + ' ฿'; return; }
      if (!odoEl || str.length !== odoStr.length) {
        result.innerHTML = '= <span class="odo" aria-hidden="true"></span> ฿<span class="vh"></span>';
        odoEl = result.querySelector('.odo');
        odoEl.innerHTML = str.split('').map(function (ch) {
          return /\d/.test(ch) ? '<span class="col">' + '0123456789'.split('').map(function (d) { return '<span>' + d + '</span>'; }).join('') + '</span>' : '<span>' + ch + '</span>';
        }).join('');
        void odoEl.offsetWidth;
      }
      var k = 0;
      str.split('').forEach(function (ch, i) { var c = odoEl.children[i]; if (c && c.className === 'col') { c.style.transitionDelay = (k++ * 35) + 'ms'; c.style.transform = 'translateY(-' + (+ch * 1.25) + 'em)'; } });
      result.querySelector('.vh').textContent = str + ' บาท';
      odoStr = str;
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
    function upd() {
      var n = boxes.filter(function (b) { return b.checked; }).length;
      fill.style.width = (n / boxes.length * 100) + '%';
      count.textContent = n + '/' + boxes.length;
    }
    boxes.forEach(function (cb) {
      var k = cb.getAttribute('data-key');
      if (saved[k]) { cb.checked = true; cb.closest('.packing-item').classList.add('checked'); }
      cb.addEventListener('change', function () {
        saved[k] = cb.checked; store(KEY, JSON.stringify(saved));
        cb.closest('.packing-item').classList.toggle('checked', cb.checked); upd();
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
  function copy(btn) { if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { flash(btn, '✅ คัดลอกแล้ว'); }); }
  $('#share-btn').addEventListener('click', function () {
    var b = this, data = { title: document.title, text: 'แผนเที่ยวเซี่ยงไฮ้ 8 วัน 7 คืน ธันวาคม 2026', url: location.href };
    if (navigator.share) navigator.share(data).catch(function () {}); else copy(b);
  });
  // ---- Poster summaries (one picture per day, drawn on canvas) ----
  (function () {
    var ov = $('#pst'), grid = $('#pst-grid'), stEl = $('#pst-st'), saveB = $('#pst-save'), files = [], shots = [], busy = false;
    var W = 1080, RED = '#B0242E', NAVY = '#0F3A54', GOLD = '#C79A3F', CREAM = '#FBF4E4', INK = '#1B2730', MUTED = '#6B7680';
    var HEAD = "600 {s}px Kanit, 'Noto Sans Thai', 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', 'Microsoft YaHei', sans-serif", BODY = "{w} {s}px 'Noto Sans Thai', 'PingFang SC', 'Hiragino Sans GB', 'Noto Sans SC', 'Microsoft YaHei', sans-serif", LANG = 'th';
    var WD = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    function zhDate(iso) { var d = new Date(iso + 'T00:00:00Z'); return (d.getUTCMonth() + 1) + '月' + d.getUTCDate() + '日 ' + WD[d.getUTCDay()]; }
    var EMO = { fly: '✈️', stay: '🏨', food: '🍜', see: '📍', shop: '🛍️', go: '🚇' };
    function fH(s) { return HEAD.replace('{s}', s); } function fB(s, w) { return BODY.replace('{s}', s).replace('{w}', w || 400); }
    function rr(x, y, w, h, r, c) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
    var seg = window.Intl && Intl.Segmenter ? new Intl.Segmenter('th', { granularity: 'word' }) : null;
    function pieces(t) { if (seg) return Array.from(seg.segment(t), function (x) { return x.segment; }); return t.match(/[฀-๿][ัิ-ฺ็-๎]*|[　-鿿＀-￯]|[^\s฀-๿　-鿿＀-￯]+\s*|\s/g) || []; }
    function wrap(c, t, maxW, maxL) {
      var out = [], line = '';
      pieces(t).forEach(function (p) {
        if (out.length >= maxL) return;
        if (c.measureText(line + p).width <= maxW || !line) line += p;
        else { out.push(line.trim()); line = p.replace(/^\s+/, ''); }
      });
      if (line && out.length < maxL) out.push(line.trim());
      var used = out.join('').replace(/\s/g, '').length, all = t.replace(/\s/g, '').length;
      if (used < all && out.length) { var l = out[out.length - 1]; while (l && c.measureText(l + '…').width > maxW) l = l.slice(0, -1); out[out.length - 1] = l.replace(/[\s·,]+$/, '') + '…'; }
      return out;
    }
    function img(src) { return new Promise(function (ok) { if (!src) return ok(null); var i = new Image(); i.onload = function () { ok(i); }; i.onerror = function () { ok(null); }; i.src = src; }); }
    function cover(c, im, x, y, w, h) { var k = Math.max(w / im.width, h / im.height), sw = w / k, sh = h / k; c.drawImage(im, (im.width - sw) / 2, (im.height - sh) / 2, sw, sh, x, y, w, h); }
    function lantern(c, x, y, s) {
      c.save(); c.translate(x, y); c.scale(s, s);
      c.strokeStyle = '#E8C877'; c.lineWidth = 2; c.beginPath(); c.moveTo(20, -40); c.lineTo(20, 18); c.stroke();
      c.fillStyle = '#E8C877'; rr(12, 16, 16, 6, 2, c); c.fill(); rr(12, 64, 16, 5, 2, c); c.fill();
      c.fillStyle = '#C2303A'; c.beginPath(); c.ellipse(20, 44, 17, 22, 0, 0, 7); c.fill();
      c.fillStyle = 'rgba(255,179,107,.55)'; c.beginPath(); c.ellipse(20, 44, 11, 15, 0, 0, 7); c.fill();
      c.strokeStyle = 'rgba(138,26,34,.6)'; c.lineWidth = 1.4; c.beginPath(); c.ellipse(20, 44, 10, 22, 0, 0, 7); c.stroke(); c.beginPath(); c.ellipse(20, 44, 4, 22, 0, 0, 7); c.stroke();
      c.strokeStyle = '#E8C877'; c.lineWidth = 1.6; [[17, 16], [20, 20], [23, 24]].forEach(function (a) { c.beginPath(); c.moveTo(a[0], 69); c.lineTo(a[1], 87); c.stroke(); });
      c.restore();
    }
    function cloud(c, x, y, s, a) {
      c.save(); c.translate(x, y); c.scale(s, s); c.globalAlpha = a; c.strokeStyle = GOLD; c.lineWidth = 3; c.lineCap = 'round';
      c.beginPath(); c.arc(30, 30, 16, Math.PI * 0.9, Math.PI * 1.9); c.arc(58, 22, 20, Math.PI * 1.1, Math.PI * 1.95); c.arc(86, 32, 13, Math.PI * 1.3, Math.PI * 0.5); c.lineTo(22, 45); c.arc(22, 37, 8, Math.PI * 0.5, Math.PI * 1.3); c.stroke();
      c.beginPath(); c.arc(48, 34, 7, 0, Math.PI * 1.6); c.stroke();
      c.restore();
    }
    function background(c, H) {
      var g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, CREAM); g.addColorStop(1, '#F3E3C6'); c.fillStyle = g; c.fillRect(0, 0, W, H);
      for (var yy = 620, k = 0; yy < H; yy += 260, k++) { cloud(c, k % 2 ? 860 : 20, yy, 1.6, 0.18); cloud(c, k % 2 ? 30 : 900, yy + 130, 1.1, 0.12); }
    }
    function header(c, hero, top, big, title, sub, pill) {
      var h = 560; c.save(); rr(0, -60, W, h + 60, 70, c); c.clip();
      if (hero) cover(c, hero, 0, 0, W, h); else { c.fillStyle = NAVY; c.fillRect(0, 0, W, h); }
      var g = c.createLinearGradient(0, 0, 0, h); g.addColorStop(0, 'rgba(10,38,58,.78)'); g.addColorStop(.6, 'rgba(12,44,66,.86)'); g.addColorStop(1, 'rgba(120,26,34,.92)'); c.fillStyle = g; c.fillRect(0, 0, W, h);
      c.restore();
      lantern(c, 800, 30, 1.25); lantern(c, 880, 36, 1.5); lantern(c, 970, 26, 1.15);
      c.textAlign = 'left'; c.fillStyle = '#EBCB82'; c.font = fH(34); c.fillText(top, 70, 130);
      c.fillStyle = '#fff'; c.font = fH(big ? 96 : 52);
      if (big) { c.fillText(big, 70, 245); }
      c.font = fH(big ? 60 : 72); var lines = wrap(c, title, W - 140, 2), y = big ? 330 : 240;
      lines.forEach(function (l) { c.fillText(l, 70, y); y += big ? 72 : 84; });
      c.font = fB(32); c.fillStyle = 'rgba(255,255,255,.88)'; if (sub) c.fillText(sub, 70, y + 4);
      if (pill) { c.font = fB(32, 700); var pw = c.measureText(pill).width + 64; c.fillStyle = 'rgba(255,255,255,.16)'; rr(70, h - 120, pw, 68, 34, c); c.fill(); c.strokeStyle = 'rgba(255,255,255,.35)'; c.lineWidth = 2; c.stroke(); c.fillStyle = '#fff'; c.fillText(pill, 102, h - 74); }
      // ribbon
      c.save(); rr(-10, h + 26, W + 20, 34, 0, c); c.clip(); c.fillStyle = RED; c.fillRect(0, h + 26, W, 34); c.fillStyle = 'rgba(255,255,255,.9)';
      for (var x = -40; x < W + 40; x += 56) { c.beginPath(); c.moveTo(x, h + 60); c.lineTo(x + 22, h + 26); c.lineTo(x + 40, h + 26); c.lineTo(x + 18, h + 60); c.fill(); }
      c.restore();
      return h + 110;
    }
    function footer(c, y, tip) {
      if (tip) {
        c.font = fB(30); var ls = wrap(c, tip, W - 240, 4), bh = 60 + ls.length * 44;
        c.fillStyle = '#FFF6DF'; rr(60, y, W - 120, bh, 36, c); c.fill(); c.strokeStyle = GOLD; c.lineWidth = 3; c.stroke();
        c.font = fB(46); c.fillText('⭐', 92, y + 70);
        c.fillStyle = '#5A4515'; c.font = fB(30); ls.forEach(function (l, i) { c.fillText(l, 160, y + 64 + i * 44); }); y += bh + 50;
      }
      c.textAlign = 'center'; c.fillStyle = NAVY; c.font = fH(34); c.fillText('🐻 Toonzii & Bear · Shanghai 5–12 ธ.ค. 2026 🎄', W / 2, y + 10);
      c.fillStyle = MUTED; c.font = fB(22); c.fillText('ภาพสถานที่จาก Wikimedia Commons ตามสัญญาอนุญาต Creative Commons', W / 2, y + 52);
      c.textAlign = 'left';
      return y + 90;
    }
    function card(c, y, e, i, pic, measureOnly) {
      var col = i % 2 ? '#1D5C82' : RED, x = 60, w = W - 120, tx = x + (pic ? 350 : 250), tw = x + w - 36 - tx;
      c.font = fH(44); var tl = wrap(c, e.title, tw, 2); c.font = fB(28); var nl = e.note ? wrap(c, e.note, tw, 2) : [];
      var th = tl.length * 54 + (nl.length ? 12 + nl.length * 40 : 0), h = Math.max(pic ? 240 : 200, th + 96);
      if (measureOnly) return h;
      c.fillStyle = '#fff'; rr(x, y, w, h, 44, c); c.fill(); c.strokeStyle = col; c.lineWidth = 6; c.stroke();
      // time pill
      c.font = fH(40); var pw = c.measureText(e.time).width + 70;
      c.fillStyle = col; rr(W / 2 - pw / 2, y - 34, pw, 66, 33, c); c.fill(); c.strokeStyle = '#fff'; c.lineWidth = 5; c.stroke();
      c.fillStyle = '#fff'; c.textAlign = 'center'; c.fillText(e.time, W / 2, y + 12); c.textAlign = 'left';
      var iy = y + (h - (pic ? 170 : 150)) / 2 + 12;
      if (pic) { c.save(); rr(x + 34, iy, 290, 170, 26, c); c.clip(); cover(c, pic, x + 34, iy, 290, 170); c.restore(); }
      else { c.fillStyle = i % 2 ? '#E7F0F7' : '#FBEDEE'; c.beginPath(); c.arc(x + 125, iy + 75, 75, 0, 7); c.fill(); c.font = fB(72); c.textAlign = 'center'; c.fillText(EMO[e.kind] || '📍', x + 125, iy + 100); c.textAlign = 'left'; }
      var ty = y + (h - th) / 2 + 52;
      c.fillStyle = NAVY; c.font = fH(44); tl.forEach(function (l) { c.fillText(l, tx, ty); ty += 54; });
      c.fillStyle = MUTED; c.font = fB(28); ty += 4; nl.forEach(function (l) { c.fillText(l, tx, ty); ty += 40; });
      return h;
    }
    function toBlob(cv) { return new Promise(function (ok) { cv.toBlob(function (b) { ok(b); }, 'image/jpeg', 0.92); }); }
    function cleanTitle(h) { var x = h.cloneNode(true); $$('.tag', x).forEach(function (t) { t.remove(); }); return x.textContent.trim(); }
    function firstSentence(t) { t = (t || '').replace(/\s+/g, ' ').trim(); var p = t.split(' · '); return p.slice(0, 2).join(' · '); }

    function dayData(sec) {
      var p = $('.dh-txt p', sec).textContent.split('·');
      return {
        n: sec.getAttribute('data-day'), iso: sec.getAttribute('data-date'), zh: sec.getAttribute('data-zh') || '', title: cleanTitle($('.dh-txt h3', sec)), date: p[0].trim(), wx: (p[1] || '').trim(), icon: $('.dicon', sec).textContent.trim(),
        disney: !!$('.dh-txt .tag', sec), tip: ($('.note', sec) ? $('.note', sec).textContent.replace('⭐', '').trim() : ''),
        evs: $$('.ev', sec).map(function (ev) { var im = $('img.thumb', ev), n = $('.evb > p', ev); var o = { time: $('time', ev).textContent.trim(), kind: ev.getAttribute('data-kind'), title: cleanTitle($('h3', ev)), note: n ? firstSentence(n.textContent) : '', src: im ? im.getAttribute('src') : '' }, z = ev.getAttribute('data-zh');
          if (LANG === 'zh' && z) { o.note = o.title; o.title = z; }
          return o; })
      };
    }
    function drawDay(d, hero) {
      var pics = d.evs.map(function (e) { return img(e.src); });
      return Promise.all(pics).then(function (pics) {
        var cv = document.createElement('canvas'), c = cv.getContext('2d'); cv.width = W; cv.height = 10;
        var hs = d.evs.map(function (e, i) { return card(c, 0, e, i, pics[i], true); });
        c.font = fB(30); var tipH = d.tip ? 60 + wrap(c, d.tip, W - 240, 4).length * 44 + 50 : 0;
        var H = 670 + hs.reduce(function (a, b) { return a + b + 86; }, 0) + tipH + 120;
        cv.height = H; background(c, H);
        var zh = LANG === 'zh';
        var y = header(c, hero, (zh ? '上海之旅 2026 · SHANGHAI TRIP' : 'SHANGHAI TRIP 2026') + (d.disney ? ' · DISNEY DAY' : ''), null, zh ? '第' + d.n + '天 • ' + (d.zh || d.title) : 'DAY ' + d.n + ' • ' + d.title, zh ? d.title : null, '📅 ' + (zh ? '2026年' + zhDate(d.iso) : d.date + ' 2026') + (d.wx ? '  ·  ' + d.wx.replace(/[\u0E00-\u0E7F]+/g, '').trim() : ''));
        y += 20;
        d.evs.forEach(function (e, i) {
          if (i) { c.fillStyle = GOLD; for (var k = 0; k < 4; k++) { c.beginPath(); c.arc(W / 2, y - 76 + k * 14, 4, 0, 7); c.fill(); } }
          y += card(c, y, e, i, pics[i]) + 86;
        });
        footer(c, y - 20, d.tip);
        return toBlob(cv);
      });
    }
    function drawCover(days, hero) {
      var cv = document.createElement('canvas'), c = cv.getContext('2d'), H = 670 + days.length * 150 + 330 + 160;
      cv.width = W; cv.height = H; background(c, H);
      var zh = LANG === 'zh';
      var y = zh ? header(c, hero, 'SHANGHAI · 2026年12月', '上海', '8天7晚', '2026年12月5日–12日 · เซี่ยงไฮ้ 8 วัน 7 คืน', '🏨 亚朵X酒店 · 淮海中路1329号')
                 : header(c, hero, 'SHANGHAI · DECEMBER 2026', 'เซี่ยงไฮ้', '8 วัน 7 คืน', '5–12 ธ.ค. 2026 · ไฟคริสต์มาส The Bund · Disneyland', '🏨 Atour X Hotel · Huaihai Rd');
      y += 10;
      days.forEach(function (d, i) {
        var col = i % 2 ? '#1D5C82' : RED;
        c.fillStyle = '#fff'; rr(60, y, W - 120, 126, 63, c); c.fill(); c.strokeStyle = col; c.lineWidth = 4; c.stroke();
        c.fillStyle = col; c.beginPath(); c.arc(126, y + 63, 46, 0, 7); c.fill();
        c.fillStyle = '#fff'; c.font = fH(48); c.textAlign = 'center'; c.fillText(d.n, 126, y + 80); c.textAlign = 'left';
        c.fillStyle = MUTED; c.font = fB(26); c.fillText((zh ? zhDate(d.iso) + ' · ' + d.title : d.date + (d.disney ? ' · DISNEY DAY' : '')), 200, y + 48);
        c.fillStyle = NAVY; c.font = fH(40); var t = wrap(c, zh && d.zh ? d.zh : d.title, W - 120 - 140 - 130, 1)[0]; c.fillText(t, 200, y + 98);
        c.font = fB(60); c.textAlign = 'right'; c.fillText(d.icon, W - 96, y + 86); c.textAlign = 'left';
        y += 150;
      });
      // flights
      var fl = $$('.passw .pass').map(function (p) { var ap = $$('.route .ap b', p).map(function (b) { return b.textContent; }), tm = $$('.times span', p).map(function (s) { return s.textContent; }); return $('.stub b', p).textContent + '  ' + ap[0] + ' ' + tm[0] + ' → ' + ap[1] + ' ' + tm[1]; });
      c.fillStyle = NAVY; rr(60, y + 10, W - 120, 250, 40, c); c.fill();
      c.fillStyle = '#EBCB82'; c.font = fH(34); c.fillText('✈️ Spring Airlines', 100, y + 70);
      c.fillStyle = '#fff'; c.font = fH(40); if (fl[0]) c.fillText((zh ? '去程 ' : 'ไป  ') + fl[0], 100, y + 140); if (fl[1]) c.fillText((zh ? '回程 ' : 'กลับ ') + fl[1], 100, y + 210);
      footer(c, y + 330, '');
      return toBlob(cv);
    }
    function addFig(blob, name, cap) {
      var url = URL.createObjectURL(blob), f = document.createElement('figure');
      f.innerHTML = '<button type="button" class="pst-th" data-i="' + shots.length + '" aria-label="ขยายภาพ ' + cap + '"><img alt="' + cap + '" src="' + url + '"></button><figcaption>' + cap + '</figcaption>';
      grid.appendChild(f); files.push(new File([blob], name, { type: 'image/jpeg' })); shots.push({ url: url, name: name, cap: cap });
    }
    function generate() {
      if (busy || files.length) return; busy = true; grid.innerHTML = ''; saveB.disabled = true;
      var secs = $$('.day'), days = secs.map(dayData), n = 0, total = days.length + 1, sfx = LANG === 'zh' ? '-zh' : '', myLang = LANG;
      function prog() { stEl.textContent = 'กำลังทำภาพ ' + n + '/' + total + '…'; }
      prog();
      var fontsReady = document.fonts && document.fonts.load ? Promise.all([document.fonts.load(fH(40), 'กขABC'), document.fonts.load(fB(30), 'กขABC'), document.fonts.load(fB(30, 700), 'กขABC')]).catch(function () {}) : Promise.resolve();
      fontsReady.then(function () { return img('img/hd/hero-960.webp'); }).then(function (hero) {
        var chain = drawCover(days, hero).then(function (b) { if (myLang !== LANG) return; n++; prog(); addFig(b, 'shanghai-trip-00-overview' + sfx + '.jpg', 'ภาพรวมทริป'); });
        days.forEach(function (d) {
          chain = chain.then(function () { return myLang === LANG ? drawDay(d, hero) : null; }).then(function (b) { if (!b || myLang !== LANG) return; n++; prog(); addFig(b, 'shanghai-trip-day' + d.n + sfx + '.jpg', 'วันที่ ' + d.n + ' · ' + d.date); });
        });
        return chain;
      }).then(function () {
        busy = false; if (myLang !== LANG) { generate(); return; } saveB.disabled = false;
        stEl.textContent = 'เสร็จแล้ว ' + total + ' ภาพ · แตะที่ภาพเพื่อดูขยาย ปัดซ้าย-ขวาดูภาพถัดไป';
      }).catch(function () { busy = false; stEl.textContent = 'ทำภาพไม่สำเร็จ ลองใหม่อีกครั้ง'; });
    }
    function open() { ov.hidden = false; document.documentElement.style.overflow = 'hidden'; generate(); }
    function close() { pv.hidden = true; ov.hidden = true; document.documentElement.style.overflow = ''; }
    $$('.pst-lang button').forEach(function (b) { b.addEventListener('click', function () {
      var l = b.getAttribute('data-lang'); if (l === LANG) return; LANG = l;
      $$('.pst-lang button').forEach(function (x) { var on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-checked', on ? 'true' : 'false'); });
      files = []; shots = []; grid.innerHTML = ''; saveB.disabled = true; if (!busy) generate();
    }); });
    $('#print-btn').addEventListener('click', open);
    $('#pst-x').addEventListener('click', close);
    // On phones the second button shares the pictures instead of printing
    var MOBILE = window.matchMedia('(pointer: coarse)').matches && !!navigator.share, printB = $('#pst-print');
    function canFiles(fs) { try { return !!(navigator.canShare && navigator.canShare({ files: fs })); } catch (e) { return false; } }
    function share(fs) {
      if (canFiles(fs)) return navigator.share({ files: fs, title: 'แผนเที่ยวเซี่ยงไฮ้' }).catch(function () {});
      return navigator.share({ title: document.title, url: location.href.split('#')[0].split('?')[0] }).catch(function () {});
    }
    if (MOBILE) { printB.innerHTML = '📤 แชร์'; printB.setAttribute('aria-label', 'แชร์ภาพสรุป'); $('#pv-sh').hidden = false; }
    printB.addEventListener('click', function () {
      if (MOBILE) { if (files.length) share(files); else share([]); return; }
      close(); setTimeout(function () { window.print(); }, 100);
    });
    // Full-screen viewer: tap a picture, scroll to read, swipe or ‹ › for the next one
    var pv = $('#pv'), pvImg = $('#pv-img'), pvSc = $('#pv-sc'), at = 0;
    function show(i, dir) {
      if (i < 0 || i >= shots.length) return;
      at = i; $('#pv-n').textContent = (i + 1) + ' / ' + shots.length + ' · ' + shots[i].cap;
      $('#pv-prev').disabled = i === 0; $('#pv-next').disabled = i === shots.length - 1;
      if (dir && !REDUCE) { pvImg.className = dir > 0 ? 'out-l' : 'out-r'; setTimeout(function () { pvImg.src = shots[i].url; pvImg.alt = shots[i].cap; pvSc.scrollTop = 0; pvImg.className = dir > 0 ? 'out-r' : 'out-l'; void pvImg.offsetWidth; pvImg.className = ''; }, 180); }
      else { pvImg.src = shots[i].url; pvImg.alt = shots[i].cap; pvSc.scrollTop = 0; }
    }
    grid.addEventListener('click', function (e) { var b = e.target.closest('.pst-th'); if (!b) return; pv.hidden = false; show(+b.getAttribute('data-i')); });
    $('#pv-x').addEventListener('click', function () { pv.hidden = true; });
    $('#pv-sh').addEventListener('click', function () { if (files[at]) share([files[at]]); });
    $('#pv-prev').addEventListener('click', function () { show(at - 1, -1); });
    $('#pv-next').addEventListener('click', function () { show(at + 1, 1); });
    (function () {
      var sx = 0, sy = 0, multi = false;
      pvSc.addEventListener('touchstart', function (e) { multi = e.touches.length > 1; sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
      pvSc.addEventListener('touchend', function (e) {
        if (multi || (window.visualViewport && visualViewport.scale > 1.05)) return;
        var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
        if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
        show(at + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
      }, { passive: true });
    })();
    document.addEventListener('keydown', function (e) {
      if (!pv.hidden) { if (e.key === 'Escape') pv.hidden = true; if (e.key === 'ArrowRight') show(at + 1, 1); if (e.key === 'ArrowLeft') show(at - 1, -1); return; }
      if (e.key === 'Escape' && !ov.hidden) close();
    });
    saveB.addEventListener('click', function () {
      if (navigator.canShare && navigator.canShare({ files: files })) { navigator.share({ files: files, title: 'แผนเที่ยวเซี่ยงไฮ้' }).catch(function () {}); return; }
      shots.forEach(function (sh, i) { setTimeout(function () { var a = document.createElement('a'); a.href = sh.url; a.download = sh.name; document.body.appendChild(a); a.click(); a.remove(); }, i * 350); });
    });
    window.__posters = { open: open };
  })();
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
      btn.textContent = done ? '✅ เก็บแผนที่ครบแล้ว · อัปเดตอีกครั้ง' : '💾 เก็บแผนที่ไว้ใช้ออฟไลน์';
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
        else { show(ok, 'เก็บแผนที่ของทั้ง 8 วันไว้ในเครื่องแล้ว เปิดได้แม้ไม่มีเน็ต'); toast('✅ เก็บแผนที่ครบ ' + ok + ' ชิ้นแล้ว', null, 2200); }
      }).catch(function () { busy = false; btn.disabled = false; show(ok, 'เก็บแผนที่ไม่สำเร็จ ลองใหม่อีกครั้ง'); });
    });
  })();

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
      if (m && m[1] > BUILD) toast('✨ มีเวอร์ชันใหม่ <b>แตะเพื่ออัปเดต</b>', function () { location.reload(); });
    }).catch(function () {});
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden) checkNewer(); });
  setTimeout(checkNewer, 4000);
})();
