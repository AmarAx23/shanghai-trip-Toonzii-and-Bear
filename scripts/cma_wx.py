"""Fetch Shanghai 15-day forecast from 中国天气网 (weather.com.cn) and write data/cma-wx.json.
Runs on GitHub Actions; the site reads the JSON from its own origin."""
import json, re, sys, urllib.request, datetime

UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148"
URLS = {
    "m15": "https://m.weather.com.cn/mweather15d/101020100.shtml",
    "w15": "http://www.weather.com.cn/weather15d/101020100.shtml",
    "w7": "http://www.weather.com.cn/weather/101020100.shtml",
}


def get(u, ref="http://www.weather.com.cn/"):
    r = urllib.request.Request(u, headers={"User-Agent": UA, "Referer": ref})
    with urllib.request.urlopen(r, timeout=30) as f:
        return f.read().decode("utf-8", "replace")


raw = {}
URLS = {k: v for k, v in URLS.items() if k in ("m15", "w7")}
for k, u in URLS.items():
    try:
        raw[k] = get(u)
    except Exception as e:  # keep going, record the error
        raw[k] = "ERR " + repr(e)

if "--debug" in sys.argv:  # kept for troubleshooting only
    for k, v in raw.items():
        open(f"data/cma-debug-{k}.html", "w").write(v)


def parse_m15(h):
    """Mobile 15-day page: <li class="h15li"> … <p class="h15listdayp2">11/21</p> … <p>晴</p> … <div class="h15listtem …">15/7℃</div>"""
    out = []
    for li in re.split(r'<li class="h15li"', h)[1:]:
        md = re.search(r'class="h15listdayp2">\s*(\d{1,2})/(\d{1,2})', li)
        tp = re.search(r'class="h15listtem[^"]*"[^>]*>\s*(-?\d+)\s*/\s*(-?\d+)', li)
        wx = re.search(r'housr_icons[^>]*></i>\s*(?:<i[^>]*></i>\s*)?<p>([^<]+)</p>', li)
        if md and tp:
            hi, lo = sorted([int(tp.group(1)), int(tp.group(2))], reverse=True)
            out.append({"m": int(md.group(1)), "d": int(md.group(2)), "wx": wx.group(1).strip() if wx else "", "hi": hi, "lo": lo})
    return out


def parse_w7(h):
    """Desktop 7-day page: <h1>22日（明天）</h1> … <p title="多云转阴" class="wea"> … <span>17</span>/<i>12℃</i>"""
    out = []
    for li in re.split(r'<li class="sky', h)[1:]:
        dd = re.search(r"<h1>(\d{1,2})日", li)
        wx = re.search(r'title="([^"]+)" class="wea"', li)
        hi = re.search(r'class="tem">\s*<span>(-?\d+)</span>', li)
        lo = re.search(r"<i>(-?\d+)℃</i>", li)
        if dd and lo:
            out.append({"d": int(dd.group(1)), "wx": wx.group(1) if wx else "", "hi": int(hi.group(1)) if hi else None, "lo": int(lo.group(1))})
    return out


days = []
if not raw["m15"].startswith("ERR"):
    days = parse_m15(raw["m15"])

now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
res = []
for x in days:
    y = now.year + (1 if x["m"] < now.month else 0)
    res.append({"date": f"{y}-{x['m']:02d}-{x['d']:02d}", "wx": x["wx"], "hi": x["hi"], "lo": x["lo"]})
if not res and not raw["w7"].startswith("ERR"):
    m, y = now.month, now.year
    prev = 0
    for x in parse_w7(raw["w7"]):
        if x["d"] < prev:
            m, y = (1, y + 1) if m == 12 else (m + 1, y)
        prev = x["d"]
        if x["hi"] is not None:
            res.append({"date": f"{y}-{m:02d}-{x['d']:02d}", "wx": x["wx"], "hi": x["hi"], "lo": x["lo"]})
res.sort(key=lambda r: r["date"])
if not res:  # parsing failed: keep the last good file instead of wiping it
    print("no forecast parsed; status:", {k: v[:80] for k, v in raw.items()})
    sys.exit(0)

json.dump({"source": "中国天气网 weather.com.cn", "updated": now.strftime("%Y-%m-%d %H:%M"), "days": res,
           "status": {k: ("ok" if not v.startswith("ERR") else v[:200]) for k, v in raw.items()}},
          open("data/cma-wx.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False)[:1500])
