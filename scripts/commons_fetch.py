"""One-off helper run on GitHub Actions: search Wikimedia Commons for freely licensed photos
and save candidates (1280px) with license/author metadata into _commons/ for review."""
import json, os, re, time, urllib.parse, urllib.request

UA = "TripPhotoBot/0.2 (https://github.com/AmarAx23/shanghai-trip-Toonzii-and-Bear)"
API = "https://commons.wikimedia.org/w/api.php"
QUERIES = {
    "suzhou-garden": "Humble Administrator's Garden Suzhou",
    "pingjiang": "Pingjiang Road Suzhou",
    "shantang": "Shantang Street Suzhou",
    "hanfu": "Hanfu Suzhou garden",
    "suzhou-noodle": "Suzhou noodles",
    "squirrel-fish": "Squirrel-shaped mandarin fish",
    "suzhou-station": "Suzhou railway station",
    "shanghai-station": "Shanghai railway station building",
    "crh-train": "CR400AF Shanghai",
}
OK_LIC = re.compile(r"^(CC0|Public domain|CC BY(-SA)? [0-9.]+)", re.I)


def get(params):
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json"))
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30) as f:
                return json.load(f)
        except Exception as e:
            print("retry", i, e)
            time.sleep(5 * (i + 1))
    return {}


def clean(html):
    return re.sub(r"<[^>]+>", "", html or "").strip()


os.makedirs("_commons", exist_ok=True)
summary = {}
for key, q in QUERIES.items():
    res = get({"action": "query", "generator": "search", "gsrsearch": q + " filetype:bitmap", "gsrnamespace": 6,
               "gsrlimit": 12, "prop": "imageinfo", "iiprop": "url|size|extmetadata", "iiurlwidth": 1280})
    pages = sorted((res.get("query") or {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
    got = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata") or {}
        lic = clean(md.get("LicenseShortName", {}).get("value"))
        if not OK_LIC.match(lic) or ii.get("width", 0) < 1000 or ii.get("width", 0) < ii.get("height", 1):
            continue
        name = p["title"].replace("File:", "")
        fn = f"_commons/{key}-{len(got) + 1}.jpg"
        try:
            with urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers={"User-Agent": UA}), timeout=60) as f:
                open(fn, "wb").write(f.read())
        except Exception as e:
            print("dl fail", name, e)
            continue
        got.append({"file": fn, "name": name, "license": lic, "author": clean(md.get("Artist", {}).get("value"))[:120],
                    "desc": clean(md.get("ImageDescription", {}).get("value"))[:200]})
        time.sleep(1.5)
        if len(got) >= 4:
            break
    summary[key] = got
    print(key, len(got))
    time.sleep(3)
json.dump(summary, open("_commons/meta.json", "w"), ensure_ascii=False, indent=1)
