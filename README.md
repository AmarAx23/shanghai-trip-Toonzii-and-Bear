# แผนเที่ยวเซี่ยงไฮ้ · Toonzii & Bear (5–12 ธ.ค. 2026)

เว็บแผนทริปเซี่ยงไฮ้ 8 วัน 7 คืน เปิดได้ที่ https://amarax23.github.io/shanghai-trip-Toonzii-and-Bear/
ติดตั้งเป็นแอปบนมือถือได้ และใช้งานได้แม้ไม่มีเน็ต

## โครงสร้าง

| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `src/build.py` | ข้อมูลทริปทั้งหมด (แผนรายวัน งบ เช็กลิสต์ เบอร์ฉุกเฉิน พิกัด) และสร้าง `index.html` |
| `src/site.css` | หน้าตาเว็บ |
| `src/site.js` | การทำงานของเว็บ (นับถอยหลัง แผนที่ อากาศ แปลงเงิน ฯลฯ) |
| `src/tiles.py` | คำนวณชิ้นแผนที่ที่ต้องเก็บไว้ใช้ออฟไลน์ |
| `src/mksw.py` | สร้าง `sw.js` (ระบบออฟไลน์และอัปเดตแอป) |
| `index.html`, `sw.js` | ไฟล์ที่สร้างอัตโนมัติ อย่าแก้ตรง ๆ |
| `img/`, `img/hd/` | รูปภาพ (`img/hd/credits.json` = เครดิตรูปจาก Wikimedia Commons) |
| `fonts/`, `vendor/leaflet/` | ฟอนต์และไลบรารีแผนที่ที่เก็บไว้ในเว็บเอง (ใช้ในจีนได้) |
| `icons/` | ไอคอนเส้นที่ใช้ในเว็บ |

## แก้เว็บ

1. แก้ไฟล์ใน `src/`
2. รัน `./build.sh` (หรือ `python3 src/build.py && python3 src/mksw.py`)
3. commit แล้ว push ขึ้น `main` — GitHub Pages อัปเดตเองภายใน 1–2 นาที แอปบนมือถือจะขึ้น "มีเวอร์ชันใหม่"

## เครดิต

- รูปสถานที่จาก Wikimedia Commons ตามสัญญาอนุญาต Creative Commons (รายชื่อใน `img/hd/credits.json`)
- แผนที่ © OpenStreetMap contributors · Leaflet (BSD-2-Clause)
- ฟอนต์ Kanit และ Noto Sans Thai (SIL Open Font License)
