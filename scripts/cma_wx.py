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
for k, u in URLS.items():
    try:
        raw[k] = get(u)
    except Exception as e:  # keep going, record the error
        raw[k] = "ERR " + repr(e)

if "--debug" in sys.argv:
    for k, v in raw.items():
        open(f"data/cma-debug-{k}.html", "w").write(v)


def parse(h):
    """Each forecast day is an <li> holding a date, weather words and two temperatures."""
    out = []
    for li in re.findall(r"<li[^>]*>(.*?)</li>", h, re.S):
        t = re.sub(r"<[^>]+>", " ", li)
        t = re.sub(r"\s+", " ", t).strip()
        md = re.search(r"(\d{1,2})月(\d{1,2})日|(\d{1,2})/(\d{1,2})", t)
        tp = re.findall(r"(-?\d+)\s*[°℃]", t)
        if md and len(tp) >= 2:
            m = int(md.group(1) or md.group(3))
            d = int(md.group(2) or md.group(4))
            wx = [w for w in re.findall(r"[晴阴云雨雪雾霾沙尘转多小中大暴阵雷冻夹]+", t) if any(c in w for c in "晴阴云雨雪雾霾")]
            hi, lo = sorted([int(tp[0]), int(tp[1])], reverse=True)
            out.append({"m": m, "d": d, "wx": wx[0] if wx else "", "hi": hi, "lo": lo})
    return out


days = []
for k in ("m15", "w15", "w7"):
    if not raw[k].startswith("ERR"):
        have = {(x["m"], x["d"]) for x in days}
        days += [x for x in parse(raw[k]) if (x["m"], x["d"]) not in have]

now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
res = []
for x in days:
    y = now.year + (1 if x["m"] < now.month else 0)
    res.append({"date": f"{y}-{x['m']:02d}-{x['d']:02d}", "wx": x["wx"], "hi": x["hi"], "lo": x["lo"]})
res.sort(key=lambda r: r["date"])

json.dump({"source": "中国天气网 weather.com.cn", "updated": now.strftime("%Y-%m-%d %H:%M"), "days": res,
           "status": {k: ("ok" if not v.startswith("ERR") else v[:200]) for k, v in raw.items()}},
          open("data/cma-wx.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False)[:1500])
