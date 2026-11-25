import re
# Builds index.html for the Shanghai trip site.
import sys, html
from urllib.parse import quote

import os as _osroot
_ROOT = _osroot.path.dirname(_osroot.path.dirname(_osroot.path.abspath(__file__)))
_HERE = _osroot.path.dirname(_osroot.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else _osroot.path.join(_ROOT, "index.html")
E = html.escape

HOTEL_Q = "Atour X Hotel, 1329 Huaihai Middle Road, Shanghai"

def apple(q):
    return "https://maps.apple.com/?q=" + quote(q)

def apple_dir(dest, mode="r", src=HOTEL_Q):
    return f"https://maps.apple.com/?saddr={quote(src)}&daddr={quote(dest)}&dirflg={mode}"

SUZHOU_KW = ("苏州", "拙政园", "平江路", "山塘街")
def amap(kw):
    city = "苏州" if any(k in kw for k in SUZHOU_KW) else "上海"
    return f"https://uri.amap.com/search?keyword={quote(kw)}&city={quote(city)}&src=shanghaitrip&callnative=1"

def gmap(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(q)

QUEUE_LINK = [("🎫 วิธีกดคิว", "#queue-card")]
PANE_LINK = [("👟 การ์ดยื่นพนักงาน", "#pane-card")]
def L(apple_q=None, amap_kw=None, extra=None):
    out = []
    if apple_q: out.append(("🍎 Apple Maps", apple(apple_q)))
    if amap_kw: out.append(("🧭 Amap 高德", amap(amap_kw)))
    if extra: out += extra
    return out


def ev(t, kind, title, note="", img=None, links=None, tag=None, data_t=None, html_note=False):
    return dict(t=t, kind=kind, title=title, note=note, img=img, links=links or [], tag=tag,
                data_t=data_t or (t if t[:2].isdigit() else ""), html_note=html_note)

DAYS = [
 dict(n=1, iso="2026-12-05", dow="ส.", date="เสาร์ 5 ธ.ค.", title="เดินทางไปเซี่ยงไฮ้", icon="✈️", wx="🌙 ~8°C กลางคืน",
  events=[
   ev("13:45", "fly", "เช็คอินสนามบินสุวรรณภูมิ", "เผื่อเวลา 3 ชม. ก่อนบิน · ชั่งกระเป๋าถือไม่เกิน 10 กก. · Spring Airlines เป็นโลว์คอสต์ ไม่มีอาหารฟรีบนเครื่อง", "bkk",
      [("📍 Google Maps", gmap("Suvarnabhumi Airport"))], data_t="14:45"),
   ev("16:45", "fly", "บิน BKK → PVG · 9C7284", "บินประมาณ 4 ชม. 20 น. · เวลาจีนเร็วกว่าไทย 1 ชม.", data_t="17:45"),
   ev("22:05", "fly", "ถึงสนามบินผู่ตง", "ผ่าน ตม. รับกระเป๋า แล้วเรียก Didi หรือต่อคิวแท็กซี่ · ยื่นการ์ดที่อยู่ภาษาจีนให้คนขับดูได้เลย", "pvg",
      L("Shanghai Pudong International Airport Terminal 2", "浦东国际机场2号航站楼"), tag="อาคาร 2"),
   ev("23:45", "stay", "เช็คอิน Atour X Hotel",
      'ชั้น 1 และ 6–11 อาคาร Yunhai, 1329 Huaihai Middle Road เขต Xuhui · เดิน ~160 ม. ถึง MRT Changshu Road (สาย 1, 7) · โทร <a href="tel:+8615002128856">+86 150 0212 8856</a>, <a href="tel:+862133561052">+86 21 3356 1052</a>',
      None, L(HOTEL_Q, "淮海中路1329号"), tag="ที่พัก", html_note=True),
  ], note="เครื่องลงค่ำ ถึงที่พักราว 23:45 (เช็คอินได้ตั้งแต่ 14:00 มาดึกได้) พักให้เต็มที่ พรุ่งนี้เริ่มสายได้"),

 dict(n=2, iso="2026-12-06", dow="อา.", date="อาทิตย์ 6 ธ.ค.", title="เที่ยวเบา ๆ + The Bund", icon="🌉", wx="⛅ 5–10°C",
  events=[
   ev("11:00", "go", "ออกจากที่พัก ไป People's Square", "รถไฟฟ้าสาย 1 จาก Changshu Road ไป People's Square ~15 นาที หรือเรียก Didi",
      None, [("🧭 เส้นทางจากที่พัก", apple_dir("People's Square, Shanghai"))]),
   ev("11:30", "food", "Lai Lai Xiao Long Bao (莱莱小笼)", "เสี่ยวหลงเปาไข่ปู Michelin Bib Gourmand · 506 Tianjin Road ใกล้ People's Square · วันอาทิตย์คิวยาว มาก่อนเที่ยงดีกว่า · ถ้าสาขานี้ปิด มีสาขา Jing'an ที่ 1726 Beijing West Road ใกล้ที่พัก (เปิด 8:00–14:00, 15:00–20:00)",
      "lailai", L("Lai Lai Xiao Long Bao, 506 Tianjin Road, Shanghai", "莱莱小笼 天津路", QUEUE_LINK), tag="มื้อกลางวัน"),
   ev("13:30", "shop", "No.1 Shopping Center (第一百货商业中心)", "ห้างเก่าแก่หัวมุม Nanjing Road ฝั่ง People's Square (南京东路830号) · เดินจาก Lai Lai ~10 นาที · เดินห้าง พักขา เข้าห้องน้ำ แล้วออกประตูฝั่ง Nanjing Road เดินต่อไปทาง The Bund ได้เลย · เวลาเปิด-ปิดเช็กใน Amap ก่อน", None, L("Shanghai No.1 Shopping Center, 830 East Nanjing Road", "第一百货商业中心 南京东路830号"), tag="ช้อป"),
    ev("14:30", "shop", "Nanjing Road Pedestrian Street", "ถนนช้อปปิ้งหลัก เดินดูห้างและร้านแบรนด์จีนแบบไม่รีบ ไฟคริสต์มาสตามห้าง · ยาว ~1.2 กม. เดินสุดถนนก็ถึง The Bund", "nanjing-road", L("Nanjing Road Pedestrian Street, Shanghai", "南京路步行街")),
  ev("15:45", "see", "The Bund ถ่ายรูปตอนกลางวัน", "ได้รูปตึกเก่าสไตล์ยุโรปตอนฟ้าสว่าง · แดดเย็นช่วงก่อนพระอาทิตย์ตก (~16:50) แสงสวยที่สุด · เดินขึ้นเหนือไป Rockbund (外滩源) ต่อได้เลย · 19:00 กลับมาดูอีกรอบตอนเปิดไฟ", None, L("The Bund, Shanghai", "外滩"), tag="ถ่ายรูป"),
   ev("16:15", "see", "Rockbund ย่านตึกเก่า (外滩源)", "ย่านอาคารยุค 1920–30 ที่บูรณะแล้ว ปลายเหนือของ The Bund ระหว่างถนน Yuanmingyuan Road (圆明园路) กับ Huqiu Road (虎丘路) · ตึกอิฐ ตึกอาร์ตเดโค ร้านเก๋ ถ่ายรูปสวยช่วงแดดเย็น · เดินจาก The Bund ~5 นาที · ⚠️ ช่วงตลาดคริสต์มาส (25 พ.ย.–27 ธ.ค.) ถนน Yuanmingyuan Road เป็นพื้นที่ตลาด วันอาทิตย์เปิด 12:00 อาจต้องซื้อบัตรเข้าช่วงนั้น เดินถนน Huqiu Road และรอบ ๆ ได้ฟรี · ดูพระอาทิตย์ตก ~16:50 บนสะพาน Waibaidu แล้วข้ามไป Rei Flower", None, L("Rockbund, Yuanmingyuan Road, Shanghai", "外滩源 圆明园路"), tag="ถ่ายรูป"),
  ev("17:00", "food", "Rei Flower Coffee Bar (汭REi·FLOWER COFFEE BAR)", "คาเฟ่ริมคลอง Suzhou Creek ย่าน North Bund · พักขาก่อนไป Manner North Bund · ลองลาเต้ดอกหอมหมื่นลี้ (桂花拿铁) ไอศกรีมมะพร้าว · ~¥55/คน · 234 North Suzhou Road (北苏州路234号) ใกล้สถานี Tiantong Road ทางออก 3 · จากปลาย Nanjing Road เดินข้ามสะพาน Waibaidu Bridge ไม่กี่นาที · เปิด 10:30–01:00 (ตาม Trip.com) · โทร +86 175 2118 7929", None, L("Rei Flower Coffee Bar, 234 North Suzhou Road, Shanghai", "汭REi FLOWER COFFEE BAR 北苏州路234号"), tag="คาเฟ่"),
   ev("18:00", "food", "Manner Coffee สาขา North Bund ริมแม่น้ำ", "ร้านกระจกใส 3 ด้าน ริมแม่น้ำหวงผู่ หันตรงหอไข่มุก · ท่าเรือสำราญนานาชาติ North Bund (北外滩国客中心码头) ใกล้ Dongdaming Road / Taiping Road เขต Hongkou · จาก Rei Flower เดินเลียบคลอง ~1.5 กม. (~20 นาที) หรือ Didi ~5 นาที · ช่วงนี้ฟ้ามืดแล้ว หอไข่มุกเปิดไฟ วิวสวยที่สุด · วันอาทิตย์คนเยอะ อาจต้องรอที่นั่งริมกระจก · เปิด 07:30–22:00 (ตาม Trip.com) · ร้านอยู่ริมแม่น้ำ ห่างตึก International Port Affairs Building (国际港务大厦) ไปทางใต้ ~60 ม. · แล้ว Didi/เดินข้ามสะพาน Waibaidu ไป The Bund ~10 นาที", None, L("Manner Coffee North Bund International Cruise Terminal, Shanghai", "MANNER 北外滩国客中心滨江店"), tag="คาเฟ่"),
  ev("19:00", "see", "The Bund ชมวิวแม่น้ำหวงผู่", "ตึกฝั่ง Lujiazui เปิดไฟยามค่ำ ธันวาคมมีไฟประดับสวยเป็นพิเศษ · ฟรี · คืนวันอาทิตย์คนแน่น ระวังกระเป๋า", "bund", L("The Bund, Shanghai", "外滩")),
  ev("20:00", "food", "Dongsheng Self-service Cuisine (东盛自助料理) บุฟเฟต์", "บุฟเฟต์ชื่อดัง เรตติ้ง 4.6 ติดอันดับในแอป Amap · ชั้น 5 ห้าง Mosaic Plaza (悦荟广场) 南京东路353号 · ~¥129 ต่อคน · เปิด 10:30–22:30 · จาก The Bund เดิน ~10 นาที · ช่วงค่ำคิวยาว กดคิวล่วงหน้าตอนอยู่ The Bund · ใน Amap/Dianping มีดีลกลุ่ม (团购) ราคาถูกกว่าหน้าร้าน · กลับที่พัก: รถไฟฟ้าสาย 2 สถานี East Nanjing Road ไป People's Square ต่อสาย 1 ไป Changshu Road ~25 นาที หรือ Didi ~20 นาที", None, L("Dongsheng Self-service Cuisine, Mosaic Plaza, 353 East Nanjing Road, Shanghai", "东盛自助料理 悦荟广场店", QUEUE_LINK), tag="มื้อเย็น"),
  ], note="ธันวาคมเซี่ยงไฮ้หนาว 4–11°C กลางคืนอาจต่ำกว่านั้น ใส่โค้ท ผ้าพันคอ และถุงมือ"),

 dict(n=3, iso="2026-12-07", dow="จ.", date="จันทร์ 7 ธ.ค.", title="Shanghai Disneyland", icon="🏰", wx="☁️ 4–8°C", disney=True,
  events=[
   ev("07:00", "go", "ออกจากที่พัก ไป Disney", "เรียก Didi ~45–60 นาที (~¥100–150) หรือรถไฟฟ้าต่อสาย 11 ไปสถานี Disney Resort ~1 ชม. · สวนเปิดประมาณ 08:30 เช็กเวลาในแอป Shanghai Disney Resort",
      "disneyland", [("🧭 เส้นทางจากที่พัก", apple_dir("Shanghai Disneyland")), ("🧭 Amap 高德", amap("上海迪士尼乐园"))]),
   ev("08:30", "see", "Enchanted Storybook Castle", "ปราสาทใหญ่ที่สุดในบรรดาดิสนีย์แลนด์ทั่วโลก ถ่ายรูปก่อนคนเยอะ", "castle"),
   ev("10:00", "see", "Zootopia + Tomorrowland", "Zootopia: Hot Pursuit และ TRON คิวยาว · ซื้อ Premier Access ในแอปหลังเข้าสวน ~¥140–180 ต่อเครื่องเล่น"),
   ev("13:00", "see", "Adventure Isle", "Roaring Rapids และโซนผจญภัย", "adventure-isle"),
   ev("15:00", "see", "Treasure Cove", "โซนโจรสลัด Pirates of the Caribbean: Battle for the Sunken Treasure", "treasure-cove"),
   ev("18:00", "food", "มื้อเย็นในสวน", "กินก่อนไปหาที่ดูโชว์ หน้าปราสาทคนเริ่มแน่นตั้งแต่ 20:00", tag="มื้อเย็น"),
   ev("21:15", "see", "Illuminate! + พลุ Magic All Around", "โชว์แสงสีฉายบนปราสาท 21:15 ต่อด้วยพลุฉลองครบ 10 ปี 21:30 · วันธรรมดามีรอบเดียว · ที่ดูแบบจองต้องซื้อ Premier Access ¥299", "fireworks"),
   ev("22:00", "go", "กลับที่พัก", "รถไฟฟ้าสาย 11 เที่ยวสุดท้ายออกจากสถานี Disney Resort ประมาณ 22:30 · Didi หลัง 22:00 ราคาขึ้น 2–3 เท่า (~¥300)"),
  ], note="วันจันทร์คนน้อยกว่าเสาร์-อาทิตย์ ตั๋ววันธรรมดาถูกกว่า (ประมาณ ¥499–539 ต่อคน เช็กราคาวันที่ 7 ธ.ค. อีกครั้งตอนซื้อ) · ถ้าวันนี้ฝนตกหนัก สลับกับวันที่ 4 ได้ · ต่อแถวกลางแจ้งนาน ใส่เสื้อหนา · ปีนี้ฉลองครบ 10 ปี มีโชว์และขบวนพาเหรดพิเศษ"),

 dict(n=4, iso="2026-12-08", dow="อ.", date="อังคาร 8 ธ.ค.", title="Wukang Road + Jing'an + West Nanjing Road", icon="🌳", wx="🌥️ 4–9°C",
  events=[
   ev("09:45", "food", "Grandma's Home (奶奶家) สาขา Wukang Road", "ร้านอาหารเซี่ยงไฮ้ชื่อดัง · ไปถึงก่อน 10:00 เพื่อได้คิวรอบแรก · ร้านอาจเปิดราว 10:30–11:00 เช็กเวลาใน Dianping/Amap ก่อน และกดคิวล่วงหน้าได้ (ดู 🎫 วิธีกดคิว) · กินเสร็จเดินไป Wukang Mansion ~5 นาที", "grandmas-home", L("Grandma's Home Wukang Road, Shanghai", "奶奶家 武康路", QUEUE_LINK), tag="มื้อกลางวัน"),
   ev("11:00", "see", "เดินเล่น Wukang Road", "ตึก Wukang Mansion (武康大楼) ตึกยุโรปเก่า ถนนต้นไม้ร่มรื่น คาเฟ่ถ่ายรูปสวย · เดินเสร็จต่อไป 13DE MARZO ที่หัวถนน Anfu Road ~10 นาที", "wukang-road", L("Wukang Mansion, Shanghai", "武康大楼")),
   ev("12:00", "food", "13DE MARZO คาเฟ่หมีแฟลกชิป 🧸", "ร้านหลักของแบรนด์ · 安福路322号 (322 Anfu Road) ช่วงปลายถนนฝั่ง Wukang Road · เครื่องดื่ม ~¥26–39 ทุกแก้วได้ตุ๊กตาหมี · ซื้อกลับเท่านั้น ไม่มีที่นั่ง · คิวยาวที่สุดในบรรดาสาขา บางช่วงเกิน 1 ชม. (วันธรรมดาช่วงเช้ารอ ~20 นาที) · ช่วงเที่ยงคิวอาจยาวขึ้น สั่งล่วงหน้าผ่านมินิโปรแกรม 13DE MARZO ใน Alipay/WeChat ระหว่างเดิน Wukang Road ~11:40 ไปถึงรับได้เลย · ยังไม่ยืนยันเวลาเปิด เช็กใน Amap ก่อนไป · เสร็จแล้ว Didi ไปวัด Jing'an ~10 นาที", None, L("13DE MARZO, 322 Anfu Road, Shanghai", "13DE MARZO 安福路322号"), tag="คาเฟ่"),
   ev("13:00", "see", "วัด Jing'an (静安寺)", "วัดพุทธเก่าแก่กว่า 1,700 ปี หลังคาทองกลางเมือง ตัดกับตึกสูงรอบ ๆ ถ่ายรูปสวย · ค่าเข้า ~¥50 · เปิดราว 07:30–17:00 · ใช้เวลา ~1 ชม. · จาก 13DE MARZO Didi ~10 นาที · อยู่ติดสถานี Jing'an Temple (สาย 2, 7, 14)", None, L("Jing'an Temple, Shanghai", "静安寺")),
   ev("14:00", "shop", "รองเท้า Pane สาขา Yongyuan Road", "แฟลกชิปสโตร์แรกของแบรนด์ ขายดีที่สุด สต๊อกคนละร้านกับ TX Huaihai · เลขที่ 22 Yongyuan Road (永源路22号) เขต Jing'an ระหว่าง Nanjing West Road กับ Yuyuan Road · เปิดเมื่อ มิ.ย. 2025 · ยังไม่ได้ยืนยันเวลาเปิด (ร้านแนวนี้ปกติราว 10:00–22:00) เช็กใน Amap/Dianping ก่อนไป · จากวัด Jing'an เดิน ~10 นาที · เสร็จแล้วเดินกลับมาเริ่ม West Nanjing Road ฝั่งวัด", "pane", L("PANE, 22 Yongyuan Road, Jing'an, Shanghai", "PANE 永源路22号", PANE_LINK), tag="ช้อป"),
   ev("15:00", "shop", "เดินเล่น West Nanjing Road (南京西路)", "ถนนช้อปปิ้งหรูสายหลัก เดินจากวัด Jing'an ไปทางตะวันออก ~1.5 กม. · ผ่าน Jing'an Kerry Centre, Plaza 66, HKRI Taikoo Hui · ช่วงธันวาคมห้างแถวนี้มักตกแต่งต้นคริสต์มาสใหญ่ ถ่ายรูปได้ · แวะคาเฟ่/พักในห้างได้ · ปลายทางคือ Butterful ที่ Wujiang Road แล้วต่อ 818 Plaza ใกล้ถนน Shimen Yi Road", None, L("West Nanjing Road, Jing'an, Shanghai", "南京西路 静安"), tag="ช้อป"),
   ev("16:45", "food", "Butterful & Creamorous (黄油与面包) แฟลกชิป 🥐", "เบเกอรี่ดังที่สุดตอนนี้ของเซี่ยงไฮ้ คนต่อคิวเยอะ · สาขาแฟลกชิป 吴江路289-291号 (Wujiang Road ใกล้ Taixing Road) ซอยขนานกับ West Nanjing Road · เมนูแนะนำ: ชาบัตตาเม็ดมะม่วงพริกเสฉวน ครัวซองต์ช็อกโกแลต ไส้กรอกชีสลาวา นโปเลียนเบอร์รี่ · เริ่ม ~¥12 · เปิด 12:00–22:00 (ตามรีวิว) · ซื้อกลับไปกินคืนนี้/พรุ่งนี้เช้าได้ · เดินไป Long Time Ago 818 ~5 นาที", None, L("Butterful & Creamorous, 289 Wujiang Road, Shanghai", "黄油与面包 吴江路289号"), tag="ของหวาน"),
   ev("17:30", "food", "Long Time Ago Mutton Shashlik (很久以前羊肉串) สาขา 818 Plaza", "ร้านเนื้อแกะเสียบไม้ย่างสไตล์มองโกเลีย บรรยากาศสนุก · 南京西路818号 818广场 (818 West Nanjing Road ใกล้ Shimen Yi Road) · ไม้ละ ~¥6 ชุด 6 ไม้ ~¥35 · คนละ ~¥100–130 · คิวยาวช่วงค่ำ ไปเร็ว 17:30 หรือกดคิวล่วงหน้า · ลองมะเขือยาวย่าง ข้าวผัดไข่ · กลับที่พัก: รถไฟฟ้าสาย 2 สถานี West Nanjing Road หรือ Didi ~15 นาที", "long-time-ago", L("Long Time Ago Mutton Shashlik, 818 West Nanjing Road, Shanghai", "很久以前羊肉串 南京西路818广场店", QUEUE_LINK), tag="มื้อเย็น"),
  ], note="ถ้าวัน Disney (วันที่ 3) ฝนตก สลับกับวันนี้ได้ · ทุกที่ในวันนี้เปิดวันอังคารตามปกติ"),

 dict(n=5, iso="2026-12-09", dow="พ.", date="พุธ 9 ธ.ค.", title="Canton 8 + West Bund + Xintiandi", icon="🏭", wx="☀️ 3–9°C",
  events=[
   ev("09:45", "food", "Pushing Coffee คาเฟ่น้องหมา", "สาขาถนน Maoming Road (茂名路) ช่วงตัดกับ Huaihai Middle Road · มีน้องหมาประจำร้านหลายตัว นั่งเก้าอี้หน้าร้านเล่นกับน้องหมาได้ · เช้าวันธรรมดาคนน้อย · ให้น้องหมาเดินมาหาก่อนค่อยลูบ ไม่ใช้แฟลช · Didi จากที่พัก ~5 นาที หรือเดิน ~20 นาที · ราว 10:50 เรียก Didi ไป Canton 8 ~15 นาที · ร้านอยู่ซอยเดียวกับ Uniqlo บนถนน Huaihai · เปิด 09:00–20:00 (ตามรีวิว) · ⚠️ ปี 2026 เซี่ยงไฮ้คุมเข้มเรื่องหมาในร้านอาหาร ก่อนไปเช็กรีวิวล่าสุดใน Dianping/Xiaohongshu ว่าน้องหมายังอยู่ไหม", "pushing", L("Pushing Coffee Maoming Road, Shanghai", "Pushing Coffee 茂名路"), tag="คาเฟ่"),
   ev("11:15", "food", "Canton 8 (喜粤8号) สาขา Runan Street", "ร้านอาหารกวางตุ้งชื่อดัง ติดมิชลิน · ติ่มซำ ห่านย่าง · ร้านเปิด ~11:00 ไปตอนเปิดคิวสั้น · จาก Pushing Coffee Didi ~15 นาที", "canton8", L("Canton 8 Runan Street, Shanghai", "喜粤8号"), tag="มื้อกลางวัน"),
   ev("13:00", "see", "Gate M West Bund Dream Center (西岸梦中心)", "โรงงานปูนซีเมนต์เก่าริมแม่น้ำหวงผู่ ปรับเป็นย่านคาเฟ่ ร้านอาหาร ร้านค้า ตึกอินดัสเทรียลถ่ายรูปสวย · ทางเดินริมน้ำ 800 ม. · 2266 Longteng Avenue · จาก Canton 8 Didi ~15 นาที · ริมน้ำลมแรง ใส่เสื้อกันลม · ฤดูหนาวที่แล้วมีลานสเก็ตน้ำแข็งริมแม่น้ำ (ปีนี้ยังไม่ยืนยัน)", None, L("Gate M West Bund Dream Center, 2266 Longteng Avenue, Shanghai", "西岸梦中心"), tag="ถ่ายรูป"),
   ev("16:00", "see", "Xintiandi (新天地)", "ตรอกอิฐแดงสไตล์ Shikumen ผสมจีน-ยุโรป · คาเฟ่ ร้านบูติก · จาก Gate M Didi ~20 นาที · เดินเล่นช่วงเย็นตอนไฟเปิด ร้านอาหาร บาร์ คาเฟ่เยอะ · ธันวาคมมักตกแต่งคริสต์มาส · แล้วแวะ New York Bagelous ใน Xintiandi Style", "xintiandi", L("Xintiandi, Shanghai", "新天地")),
   ev("16:45", "food", "New York Bagelous Museum 🥯", "ร้านเบเกิลดังในห้าง Xintiandi Style เฟส 2 ชั้น 1 ห้อง L111 (马当路245号 新天地时尚购物中心2期 L111) · เนื้อขนมนุ่มหนึบ ใกล้ขนมปังนมผสมเพรทเซลมากกว่าเบเกิลแท้ · Original ~¥13, พริกฮาลาเปโญ ~¥26, แซลมอนรมควัน ~¥56 · ร้านเล็ก คิวต่อเนื่อง · เปิด 11:00–19:00 (ตามรีวิว เช็กอีกครั้ง) · เดินจาก Xintiandi ได้ แล้วไป Pane ที่ TX Huaihai ต่อ ~10 นาที", None, L("New York Bagelous Museum, Xintiandi Style, 245 Madang Road, Shanghai", "新天地时尚 马当路245号 贝果"), tag="ของหวาน"),
   ev("17:30", "shop", "รองเท้า Pane ที่ TX Huaihai", "แบรนด์รองเท้าผ้าใบเซี่ยงไฮ้ · ชั้น L1 ห้าง TX Huaihai, 523 Huaihai Middle Road (淮海中路523号 TX淮海) · เดินจาก Xintiandi ได้ · เปิด 10:00–22:00 · รุ่นยอดนิยม Aria, Zephyr Training · บางไซซ์หมดบ่อย · จาก Xintiandi เดิน ~10 นาที · ออกจากร้านราว 18:15 แล้วเดินไป New Sukiyaki (淮海中路755号) ~10 นาที · ถ้าไซซ์หมด วันที่ 7 แวะร้านนี้ซ้ำได้ (วันที่ 4 ได้ดูสาขา Yongyuan Road มาแล้ว)", "pane", L("TX Huaihai, 523 Middle Huaihai Road, Shanghai", "TX淮海 淮海中路523号", PANE_LINK), tag="ช้อป"),
   ev("18:30", "food", "New Sukiyaki (牛New寿喜烧) สาขา Huaihai Middle Road", "บุฟเฟต์สุกี้ยากี้ญี่ปุ่นชื่อดัง เนื้อไม่อั้น · ชั้น 3 ตึก Huaihai 755 (淮海中路755号 淮海755大厦3楼) ใกล้ถนน Ruijin 2nd Road · ราคาราว ¥118 / 158 / 208 ต่อคน ตามระดับเนื้อ · เปิด 16:30–22:00 (ตามรีวิว เช็กอีกครั้ง) · กินเสร็จเดินถนน Huaihai กลับที่พัก", "new-sukiyaki", L("Niu New Sukiyaki, 755 Huaihai Middle Road, Shanghai", "牛New寿喜烧 淮海中路755号", QUEUE_LINK), tag="มื้อเย็น"),
   ev("20:00", "shop", "เดินถนน Huaihai Road กลับที่พัก", "กินเสร็จเดินต่อไปทางตะวันตกตามถนน Huaihai Middle Road (淮海中路) ร้านแบรนด์ ห้าง ไฟประดับช่วงธันวาคม · จากร้านถึงที่พัก (淮海中路1329号) ~2.5 กม. เดินช้า ๆ ~40 นาที · ผ่านสถานี South Shaanxi Road กลางทาง ถ้าเมื่อยขึ้นรถไฟฟ้าสาย 1 ไป Changshu Road ได้", None, L("Huaihai Middle Road, Shanghai", "淮海中路"), tag="ช้อป"),
  ], note="เช้านี้เริ่มสบาย ๆ ที่คาเฟ่น้องหมาใกล้ที่พัก · Gate M ริมแม่น้ำลมแรง เตรียมเสื้อกันลม"),

 dict(n=6, iso="2026-12-10", dow="พฤ.", date="พฤหัส 10 ธ.ค.", title="ซูโจวเต็มวัน + ชุดฮั่นฝู", icon="🏯", wx="⛅ 4–10°C",
  events=[
   ev("08:00", "go", "ไปสถานีรถไฟเซี่ยงไฮ้ (上海站)", "รถไฟฟ้าสาย 1 จาก Changshu Road ไป Shanghai Railway Station ตรง ~20 นาที · จองตั๋วรถไฟความเร็วสูงล่วงหน้าในแอป Trip.com ใช้พาสปอร์ต · ไปถึงก่อนรถออก ~30 นาที (ตรวจพาสปอร์ต + สแกนกระเป๋า)", None,
      [("🧭 เส้นทางจากที่พัก", apple_dir("Shanghai Railway Station", "r")), ("🧭 Amap 高德", amap("上海站"))]),
   ev("08:40", "go", "รถไฟความเร็วสูง ไปซูโจว (苏州站)", "ราว 25–30 นาที · ตั๋วราว ¥30–40 ต่อเที่ยว · ถึงแล้ว Didi ไปสวน ~10 นาที", None, L("Suzhou Railway Station", "苏州站")),
   ev("09:30", "see", "Humble Administrator's Garden (拙政园)", "สวนจีนที่ใหญ่และสวยที่สุดของซูโจว มรดกโลก UNESCO · เดินชมราว 1.5 ชม. · ตั๋วราว ¥70–90 ต้องจองล่วงหน้าแบบใช้ชื่อจริง (พาสปอร์ต) · ไปเช้าคนน้อย · ข้าง ๆ คือ Suzhou Museum ออกแบบโดย I.M. Pei (เข้าฟรีแต่ต้องจอง) ถ้ามีเวลา", None, L("Humble Administrator's Garden, Suzhou", "拙政园")),
   ev("11:00", "see", "เช่าชุดฮั่นฝู + ถ่ายรูป Pingjiang Road (平江路)", "ถนนเก่าริมคลอง บ้านกำแพงขาวหลังคาดำ · ร้านเช่าชุดฮั่นฝู (汉服) พร้อมแต่งหน้าทำผมเรียงกันเยอะ ราว ¥150–300 ต่อคน แล้วแต่แพ็กเกจ (มีช่างภาพตามถ่ายแพงขึ้น) · ควรจองร้านล่วงหน้า · เดือนธันวาคมหนาว เลือกชุดที่มีเสื้อคลุมบุขน · เดินจากสวน ~10 นาที", None, L("Pingjiang Road, Suzhou", "平江路 汉服"), tag="ถ่ายรูป"),
   ev("13:00", "food", "บะหมี่ซูโจว (苏式汤面)", "บะหมี่น้ำใสสไตล์ซูโจว · Yuxingji (裕兴记) ร้านต้นตำรับจากซูโจว มีบะหมี่มันปู (蟹黄面) · หรือร้านบะหมี่แถว Pingjiang Road · ใส่ชุดฮั่นฝูไปกินได้", None, L("Yuxingji noodles, Suzhou", "裕兴记 苏州"), tag="มื้อกลางวัน"),
   ev("15:00", "see", "Shantang Street (山塘街)", "คืนชุดแล้ว Didi ~15 นาที · ถนนริมคลองเก่าแก่กว่า 1,000 ปี แขวนโคมแดง ร้านขนมและของฝาก · นั่งเรือในคลองได้ · อยู่ถึงช่วงค่ำ ตอนไฟโคมเปิด (~17:00) สวยที่สุด", None, L("Shantang Street, Suzhou", "山塘街"), tag="ถ่ายรูป"),
   ev("18:00", "food", "มื้อเย็นอาหารซูโจว", "ลองปลากระรอกราดซอส (松鼠桂鱼) เมนูขึ้นชื่อของซูโจว · มีร้านอาหารซูโจวแถว Shantang Street และ Guanqian Street (观前街)", None, L("Suzhou cuisine restaurant, Shantang Street", "山塘街 苏帮菜"), tag="มื้อเย็น"),
   ev("19:30", "go", "รถไฟกลับเซี่ยงไฮ้", "Didi ไปสถานีซูโจว ~10 นาที · รถไฟ ~30 นาที ถึงสถานีรถไฟเซี่ยงไฮ้ ~20:15 · ต่อรถไฟฟ้าสาย 1 กลับ Changshu Road ~20 นาที · จองตั๋วขากลับไว้ด้วย เผื่อรอบค่ำเต็ม", None, L("Shanghai Railway Station", "上海站")),
  ], note="จองล่วงหน้าก่อนไป: ① ตั๋วรถไฟไป–กลับ (เปิดขาย 26 พ.ย.) ② ตั๋วสวน 拙政园 (เปิดจอง 3 ธ.ค.) ③ ร้านเช่าชุดฮั่นฝู · ถ้าวันนี้ฝนตก สลับกับวันพรุ่งนี้ได้",
  guide=("🎫 วิธีจองตั๋วรถไฟ + ตั๋วสวน 拙政园", """
<h4>🚄 ตั๋วรถไฟ เซี่ยงไฮ้ ⇄ ซูโจว</h4>
<ul>
<li><b>เปิดขาย พฤ. 26 พ.ย.</b> ทั้งขาไปและขากลับ (รถไฟจีนขายล่วงหน้า 15 วันนับรวมวันเดินทาง) · เวลาเปิดขายแต่ละสถานีไม่เท่ากัน ดูในแอป 12306</li>
<li><b>Trip.com</b> (แนะนำ) ภาษาอังกฤษ จ่ายบัตรไทยได้ กรอกชื่อ + เลขพาสปอร์ตให้ตรงเล่ม · หรือแอป <b>12306</b> (ทางการ ถูกกว่านิดหน่อย ต้องสมัครด้วยพาสปอร์ต + ยืนยันอีเมลก่อน)</li>
<li>ขาไป 08:40 เลือก <b>上海站 (สถานีเซี่ยงไฮ้)</b> ไม่ใช่ 上海虹桥 (หงเฉียว อยู่อีกฝั่งเมือง) · ปลายทาง <b>苏州站</b> ใกล้สวนกว่า 苏州北</li>
<li>วันเดินทางใช้พาสปอร์ตเล่มที่จองสแกนเข้าประตู ไม่ต้องปริ้น · ไปถึงก่อน 30–60 นาที (ตรวจกระเป๋า) · นั่ง ~25–40 นาที</li>
</ul>
<h4>🎫 ตั๋วสวน 拙政园 (Humble Administrator's Garden)</h4>
<ul>
<li><b>เปิดจอง ~พฤ. 3 ธ.ค.</b> (จองล่วงหน้าได้ 1–7 วัน ชื่อจริง แบ่งรอบเวลา ขายจนหมด)</li>
<li><b>Trip.com</b> ใช้พาสปอร์ตได้ เลือกรอบ <b>09:00–10:00</b> ตรงกับแผน · หรือมินิโปรแกรมใน WeChat (ภาษาจีน)</li>
<li>ธันวาคมโลว์ซีซั่น ~70 หยวน · เปิด 07:30–17:00 · วันธรรมดาตั๋วไม่น่าหมด แต่จองวันที่เปิดดีกว่า</li>
<li>เปลี่ยนวัน = ยกเลิกแล้วจองใหม่ (ยกเลิกก่อนเที่ยงคืนวันก่อน) · เข้าประตูแสดงพาสปอร์ตเล่มที่จอง</li>
</ul>
<p class="g-note">ข้อมูลสวนมาจากเว็บท่องเที่ยว/ข่าวท้องถิ่นซูโจว ราคากับเวลาเปิดต่างกันเล็กน้อย เช็กในหน้าจองอีกที</p>""")),

 dict(n=7, iso="2026-12-11", dow="ศ.", date="ศุกร์ 11 ธ.ค.", title="The Bund brunch + Lujiazui", icon="🙏", wx="🌤️ 5–11°C",
  events=[
   ev("10:00", "food", "Cocina 19 ร้านอาหารสเปน ริม The Bund", "มื้อสาย ร้านเปิด 10:00 · 19 Fuzhou Road หัวมุมถนน Zhongshan East 1st Road (The Bund) · ตึกวิลล่าเก่า โต๊ะริมหน้าต่างวิวหอไข่มุก มีระเบียง · เมนูเด่น paella ซีฟู้ด · จองโต๊ะริมหน้าต่างล่วงหน้าได้ · กินแล้วเดินไป Luneurs ~10–15 นาที", "cocina19", L("Cocina 19, 19 Fuzhou Road, Shanghai", "Cocina 19西班牙餐厅 外滩"), tag="มื้อสาย"),
   ev("12:00", "food", "Luneurs Boulanger & Glacier สาขาแฟลกชิป 🍦", "ร้านเบเกอรี่และไอศกรีมดัง · 圆明园路133号 (133 Yuanmingyuan Road) ย่าน The Bund ฝั่งเหนือ ใกล้สะพาน Waibaidu · จาก Cocina 19 เดิน ~10–15 นาที · ห้ามพลาดไอศกรีมคาราเมลเค็ม ลองรสพิสตาชิโอ เกาลัด ดาร์กช็อกโกแลต · ขนมฝรั่งเศส ครัวซองต์ ทาร์ตแอปเปิล ทาร์ตเลมอน · มีที่นั่งด้านนอก · เปิด 08:00–22:00 (ตามรีวิว) · บางแหล่งเขียนเลขที่ 115 เช็กใน Amap ก่อนไป · กินเสร็จเดินเล่น The Bund ต่อได้", None, L("Luneurs, 133 Yuanmingyuan Road, Shanghai", "Luneurs 圆明园路133号"), tag="ของหวาน"),
   ev("13:30", "shop", "แวะ Pane ที่ TX Huaihai (สำรอง)", "เฉพาะถ้าวันที่ 5 ยังไม่ได้ไซซ์ที่อยากได้ · 523 Huaihai Middle Road · จาก Luneurs Didi ~15 นาที · ออกจากร้านไม่เกิน 14:30 แล้ว Didi กลับไปตลาดคริสต์มาส ~15 นาที · ถามพนักงานวันที่ 4 ได้ว่าของจะเข้าวันไหน · ถ้าไม่ต้องแวะ เดินเล่น The Bund ต่อได้เลย", "pane", L("TX Huaihai, 523 Middle Huaihai Road, Shanghai", "TX淮海 淮海中路523号", PANE_LINK), tag="ถ้ายังไม่ได้ไซซ์"),
   ev("16:30", "shop", "Superbrand Mall (正大广场)", "ห้างใหญ่ฝั่ง Lujiazui · จาก TX Huaihai Didi ~20 นาที · ซื้อของฝากรอบสุดท้าย · ตอนค่ำออกมาดูวิว The Bund จากฝั่ง Pudong ได้ · ร้านมื้อเย็นอยู่ย่านเดียวกัน", "superbrand", L("Superbrand Mall, Shanghai", "正大广场")),
   ev("17:30", "see", "เดินถ่ายรูป Lujiazui ตอนเปิดไฟ", "สะพานลอยวงกลม Lujiazui (陆家嘴环形天桥) มุมหอไข่มุก · หน้าห้าง IFC Mall (上海国金中心) · ตึก Jin Mao (金茂大厦) คู่ Shanghai Tower ถ่ายจากถนนด้านล่าง · ทั้งหมดเดินถึงกันจาก Superbrand · พระอาทิตย์ตก ~16:50 ตอนนี้ตึกเปิดไฟแล้ว", None, L("Lujiazui Circular Pedestrian Bridge, Shanghai", "陆家嘴环形天桥"), tag="ถ่ายรูป"),
   ev("18:30", "food", "Chef Fei (费大厨)", "ร้านพริกผัดหมูชื่อดัง (辣椒炒肉) รสจัดจ้านสไตล์หูหนาน · สาขา Lujiazui เดินจากจุดถ่ายรูปได้ · ช่วงค่ำคิวยาว กดคิวล่วงหน้า", "chef-fei", L("Chef Fei Lujiazui, Shanghai", "费大厨 陆家嘴", QUEUE_LINK), tag="มื้อเย็น"),
   ev("20:00", "see", "ตลาดคริสต์มาส Christkindlmarkt on the Bund 🎄 บรรยากาศกลางคืน", "ตลาดคริสต์มาสสไตล์เยอรมัน ร้านไม้ 45+ ร้าน ไวน์อุ่น (Glühwein) ไซเดอร์แอปเปิลร้อน ช็อกโกแลตร้อน ไส้กรอก ราเคล็ต ของขวัญทำมือ · ถนน Yuanmingyuan Road เส้นเดียวกับ Luneurs (北京东路99号 圆明园路步行街) · 🌙 ปิดท้ายทริปตอนไฟประดับเปิดเต็มที่ · วันศุกร์เปิดถึง 22:00 · ค่าเข้า ¥30 ซื้อล่วงหน้า / ¥40 หน้างาน (มินิโปรแกรม SmTk ใน WeChat หรือแอป SmartShanghai) · จาก Chef Fei Didi ข้ามแม่น้ำ ~15 นาที · กลับที่พัก Didi ~20 นาที", None, L("Christkindlmarkt on the Bund, Yuanmingyuan Road, Shanghai", "外滩源 圣诞市集 圆明园路"), tag="ช้อป"),
   ev("21:45", "stay", "เก็บกระเป๋า", "ชั่งกระเป๋า โหลดไม่เกิน 20 กก. ถือขึ้นไม่เกิน 10 กก."),
  ], note="พรุ่งนี้บิน 12:05 ต้องออกจากที่พัก 8:00 · เก็บกระเป๋าและชั่งน้ำหนักให้เสร็จคืนนี้ ตั้งนาฬิกาปลุก"),

 dict(n=8, iso="2026-12-12", dow="ส.", date="เสาร์ 12 ธ.ค.", title="เดินทางกลับ", icon="✈️", wx="🌤️ 5–11°C",
  events=[
   ev("07:30", "stay", "เช็คเอาท์ Atour X Hotel", "ชั่งกระเป๋าอีกรอบ โหลดรวมไม่เกิน 20 กก. ถือขึ้น 1 ชิ้นไม่เกิน 10 กก. · ไปกินมื้อเช้าที่สนามบิน"),
   ev("08:00", "fly", "ไปสนามบินผู่ตงด้วยรถไฟแม่เหล็ก Maglev 🚄", "เดินไปสถานี Changshu Road (~160 ม.) → รถไฟใต้ดินสาย 7 ไป Longyang Road (龙阳路) ~30 นาที → เปลี่ยนขึ้น Maglev (磁浮) วิ่งราว 8 นาที ความเร็วสูงสุดหลายร้อย กม./ชม. → ลงสถานีสนามบินผู่ตง เดินไปอาคาร 2 ~10 นาที · Maglev ออกทุก ~20 นาที (07:00–21:20) · ตั๋ว ¥50 หรือ ¥40 ถ้าแสดงตั๋วเครื่องบินวันเดียวกัน ซื้อที่ตู้/เคาน์เตอร์หน้าทางเข้า · รวม ~1 ชม. ถึงราว 9:00 · เช้าวันเสาร์รถไฟไม่แน่น ลากกระเป๋าได้ · สำรอง: Didi ~1 ชม.", None,
      [("🧭 เส้นทางจากที่พัก", apple_dir("Shanghai Pudong International Airport Terminal 2", "d")), ("🧭 Amap 高德", amap("浦东国际机场2号航站楼"))]),
   ev("09:00", "food", "เช็คอิน + มื้อเช้าที่สนามบิน", "เช็คอินและโหลดกระเป๋าก่อน แล้วค่อยกินข้าวหลังผ่าน ตม. · เคาน์เตอร์ปิดก่อนบินราว 45–60 นาที"),
   ev("12:05", "fly", "บิน PVG → BKK · 9C7283", "บินประมาณ 4 ชม. 40 น. ถึงสุวรรณภูมิ 15:45 (เวลาไทย)"),
  ], note="ขากลับมีของฝาก ชั่งกระเป๋าก่อนออกจากที่พัก"),
]

BUDGET = [("ตั๋วเครื่องบิน Spring Airlines ไป-กลับ", 13330, "✈️"), ("ที่พัก 7 คืน Atour X Hotel", 6565, "🏨"), ("ค่าอาหาร", 5000, "🍜"),
          ("ตั๋ว Disney + คูปอง 30 หยวน", 2208, "🏰"), ("ค่าเดินทางในเมือง", 1000, "🚇"), ("ค่าเดินทางไป-กลับสนามบิน", 800, "🚕"),
          ("e-SIM", 632, "📱"), ("ประกันการเดินทาง", 325, "🛡️")]
TOTAL = sum(b[1] for b in BUDGET)
assert TOTAL == 29860

BOOK = [("bk-disney", "🏰", "ตั๋ว Disney 7 ธ.ค."), ("bk-train", "🚄", "ตั๋วรถไฟไป-กลับซูโจว (เปิดขาย 26 พ.ย.)"),
        ("bk-garden", "🎫", "ตั๋วสวน 拙政园 (เปิดจอง 3 ธ.ค.)"), ("bk-hanfu", "👘", "จองร้านเช่าชุดฮั่นฝู"),
        ("bk-didi", "🚕", "แอป Didi ผูกบัตร"), ("bk-insure", "🛡️", "ประกันเดินทาง"),
        ("bk-arrival", "🛂", "China Arrival Card ออนไลน์ ทั้ง 2 คน (s.nia.gov.cn · ฟรี)")]
PACK = [("sim", "📱", "ซิม / eSIM จีน"), ("pay", "💳", "Alipay ผูกบัตร"), ("passport", "🛂", "Passport + สำเนา"),
        ("powerbank", "🔋", "แบตสำรอง 3C"), ("meds", "💊", "ยาแก้แพ้ / แก้ปวด"), ("plug", "🔌", "หัวแปลงปลั๊ก"),
        ("coat", "🧣", "เสื้อหนาว ผ้าพันคอ"), ("booking", "📄", "ปริ้น Booking"), ("vpn", "🌐", "VPN สำหรับ LINE"),
        ("shoes", "👟", "รองเท้าเดินสบาย"), ("cash", "💴", "เงินสดหยวน"), ("lipbalm", "💧", "ลิปมัน / โลชั่น"),
        ("motionsick", "🤢", "ยาแก้เมารถ"), ("luggage", "⚖️", "กระเป๋า 20/10 กก."), ("umbrella", "☂️", "ร่มพับ / กันลม"),
        ("maps", "🗺️", "แอป Amap"),
        ("offmap", "⬇️", "กดเก็บแผนที่ออฟไลน์ (ปุ่มเดียวได้ทั้งหมด)")]

SOS = [("110", "👮", "ตำรวจ", "มีสายด่วนรองรับภาษาอังกฤษ", "110"), ("120", "🚑", "รถพยาบาล", "เหตุฉุกเฉินทางการแพทย์", "120"),
       ("119", "🚒", "ดับเพลิง", "ไฟไหม้ / เหตุฉุกเฉินอื่น ๆ", "119"),
       ("+862164390630", "🌐", "สายด่วนช่วยเหลือชาวต่างชาติ", "ศูนย์บริการข้อมูลเซี่ยงไฮ้", "+86 21 6439 0630"),
       ("+862152609899", "🇹🇭", "สถานกงสุลใหญ่ไทย ณ เซี่ยงไฮ้", "เวลาทำการ จ.–ศ. 09:30–12:00, 13:30–17:30 (ปิด จ. 7 ธ.ค.) · 18 Wanshan Road เขต Changning · ยื่นคนขับ: 长宁区万山路18号 泰国总领事馆", "+86 21 5260 9899"),
       ("+8618516268776", "🆘", "สายด่วนฉุกเฉินคนไทย (กงสุลเซี่ยงไฮ้)", "นอกเวลาทำการ / เหตุด่วน · เบอร์จากประกาศปี 2022 ควรเช็กอีกครั้งก่อนไป", "+86 185 1626 8776"),
       ("+862122163999", "🏥", "รพ. United Family (Changning)", "ห้องฉุกเฉิน 24 ชม. หมอพูดอังกฤษ · 699 Pingtang Rd · Didi ~20–30 นาที", "+86 21 2216 3999"),
       ("+862162483986", "🏥", "รพ. Huashan 华山医院", "ใกล้ที่พักที่สุด ~1.5 กม. · 12 Middle Wulumuqi Rd · แผนกต่างชาติพูดอังกฤษ จ.–ศ. 8:00–17:00", "+86 21 6248 3986")]

PHRASES = [("多少钱？", "duō shǎo qián", "เท่าไหร่ครับ/คะ"), ("不要辣", "bú yào là", "ไม่เอาเผ็ด"), ("少辣", "shǎo là", "เผ็ดน้อย"),
           ("洗手间在哪里？", "xǐ shǒu jiān zài nǎ lǐ", "ห้องน้ำอยู่ไหน"), ("可以用支付宝吗？", "kě yǐ yòng zhī fù bǎo ma", "จ่าย Alipay ได้ไหม"),
           ("这个", "zhè ge", "อันนี้ (ชี้ที่เมนู)"), ("买单", "mǎi dān", "เช็กบิล"), ("谢谢", "xiè xie", "ขอบคุณ")]

TIPS = [("🛂", "วีซ่า", "พาสปอร์ตไทยเข้าจีนแบบ Free Visa อยู่ได้สูงสุด 30 วัน (ไม่เกิน 90 วันใน 180 วัน) · ไทย-จีนยกเว้นวีซ่าให้กันแบบถาวรตั้งแต่ 1 มี.ค. 2024 · ⚠️ แต่ต้องกรอก China Arrival Card (บัตรขาเข้า) ออนไลน์ฟรีที่ s.nia.gov.cn ก่อนบิน ทุกคน คนละใบ"),
        ("🛂", "พาสปอร์ตหาย ทำ 3 ขั้นตอน", "1) แจ้งความที่สถานีตำรวจ (派出所) ขอใบรับแจ้งความ 报案回执 · 2) ไปสำนักงานตรวจคนเข้าเมือง (出入境) ขอหนังสือรับรองการแจ้งพาสปอร์ตหาย 护照报失证明 และวีซ่าออกนอกประเทศ อาจใช้เวลาหลายวันทำการ · 3) ติดต่อสถานกงสุลใหญ่ไทย ณ เซี่ยงไฮ้ ขอเอกสารเดินทางฉุกเฉิน (ETD) กลับไทย · ถ่ายรูปหน้าพาสปอร์ตเก็บไว้ในมือถือและอีเมลก่อนเดินทาง"),
        ("🔋", "แบตสำรองขึ้นเครื่องในจีน", "ต้องมีตรา 3C (CCC) และตัวเลขความจุ (mAh หรือ Wh) พิมพ์ชัด ไม่ลอก ไม่งั้นถูกยึดที่จุดตรวจ · ใส่กระเป๋าถือเท่านั้น ห้ามโหลด · ไม่เกิน 100Wh (~27,000mAh) ไม่ต้องขออนุญาต · ห้ามใช้ชาร์จบนเครื่อง · ถ้าแบตไม่มี 3C ซื้อใหม่ในจีนก่อนวันกลับได้ (ร้านสะดวกซื้อ/ห้าง)"),
        ("🧻", "พกทิชชูติดตัว", "ห้องน้ำสาธารณะหลายที่ไม่มีกระดาษให้ บางที่เป็นแบบนั่งยอง · พกทิชชูแบบห่อเล็กกับเจลล้างมือ · ห้องน้ำในห้าง ร้านกาแฟ และสถานีใหญ่สะอาดกว่า"),
        ("📷", "สแกนเมนูด้วยมือถือ", "เมนูส่วนใหญ่เป็นภาษาจีนล้วน · iPhone: เปิดกล้องแล้วกดไอคอนข้อความ หรือแอป Translate โหมดกล้อง · Android: Google Lens (ต้องเปิด VPN) · แอปที่ใช้ได้ไม่ต้อง VPN: Alipay มีฟังก์ชันแปลในตัว · ร้านที่สั่งผ่าน QR บนโต๊ะ เปิดในมือถือแล้วแปลหน้าเว็บได้"),
        ("🗺️", "แผนที่ในจีน", "Google Maps ใช้ไม่ได้ถ้าไม่เปิด VPN · ลิงก์ในเว็บนี้ใช้ Apple Maps (ใช้ได้ในจีน) และ Amap 高德 ซึ่งคนท้องถิ่นใช้กัน"),
        ("📱", "จ่ายเงิน", "โหลด Alipay / WeChat Pay ผูกบัตรต่างชาติไว้ล่วงหน้า ร้านส่วนใหญ่ไม่รับเงินสด"),
        ("🚇", "รถไฟฟ้า", "ใช้ QR ในแอป Alipay หรือ Shanghai Public Transportation Card ครอบคลุมเกือบทุกจุดเที่ยว"),
        ("🌐", "อินเทอร์เน็ต", "Google / Facebook / LINE ใช้ไม่ได้ในจีน โหลด VPN หรือใช้ WeChat แทนก่อนเดินทาง"),
        ("🧥", "อากาศ", "หนาว 4–11°C ใส่เสื้อแบบหลายชั้น เพราะในห้างและร้านเปิดฮีตเตอร์ร้อน"),
        ("🎡", "Disneyland ครบ 10 ปี", "ปีนี้มีแคมเปญ \"With You, It's Magic+\" โชว์หน้าปราสาทใหม่และขบวนพาเหรดพิเศษ · ซื้อตั๋วล่วงหน้าในเว็บหรือแอปทางการ"),
        ("🎄", "คริสต์มาส", "ธันวาคมมีไฟประดับตามห้างและ The Bund สวยเป็นพิเศษ")]

KIND_DOT = {"fly": "var(--red)", "stay": "var(--gold)", "food": "#D86A2B", "see": "var(--navy-2)", "shop": "#7F77DD", "go": "var(--muted)"}

def links_html(links):
    if not links: return ""
    out = []
    for label, url in links:
        ext = "" if url.startswith("#") else ' target="_blank" rel="noopener"'
        out.append(f'<a href="{E(url)}"{ext}>{E(label)}</a>')
    return '<div class="links">' + "".join(out) + "</div>"


# Approximate coordinates for the day maps (schematic, no map tiles: works offline and in China)
HOTEL_LL = (31.2162, 121.4458)   # 1329 Middle Huaihai Rd, ~160 m from Changshu Rd station
PVG_LL = (31.1525, 121.8018)
GEO = {
 (4, "14:00"): ((31.2222, 121.4347), "Pane Yongyuan"),
 (5, "16:45"): ((31.2185, 121.4706), "Bagelous"), (4, "16:45"): ((31.2318, 121.4552), "Butterful"),
 (5, "09:45"): ((31.2180, 121.4568), "Pushing Coffee"),
 (5, "17:30"): ((31.2245, 121.4680), "Pane TX Huaihai"),
 (5, "20:00"): ((31.2175, 121.4545), "Huaihai Road"),
 (5, "11:15"): ((31.2065, 121.4743), "Canton 8"), (5, "13:00"): ((31.1749, 121.4574), "Gate M West Bund"), (5, "16:00"): ((31.2219, 121.4704), "Xintiandi"), (5, "18:30"): ((31.2208, 121.4600), "New Sukiyaki Huaihai"),
 (4, "13:00"): ((31.2253, 121.4407), "วัด Jing'an"), (4, "15:00"): ((31.2300, 121.4505), "West Nanjing Road"), (4, "17:30"): ((31.2341, 121.4572), "Long Time Ago 818"),
 (6, "08:00"): ((31.2527, 121.4460), "สถานีรถไฟเซี่ยงไฮ้"), (6, "08:40"): ((31.3325, 120.6058), "สถานีซูโจว"), (6, "09:30"): ((31.3264, 120.6258), "拙政园"), (6, "11:00"): ((31.3177, 120.6303), "Pingjiang Road"), (6, "13:00"): ((31.3243, 120.6222), "บะหมี่ซูโจว"), (6, "15:00"): ((31.3185, 120.6040), "Shantang Street"), (6, "18:00"): ((31.3190, 120.6060), "มื้อเย็นซูโจว"), (6, "19:30"): ((31.3325, 120.6058), "สถานีซูโจว"),
 (1, "22:05"): (PVG_LL, "สนามบินผู่ตง T2"),
 (2, "11:30"): ((31.2381, 121.4726), "Lai Lai"), (2, "13:30"): ((31.2368, 121.4702), "No.1 Shopping Center"),
 (2, "14:30"): ((31.2395, 121.4745), "Nanjing Road"), (2, "15:45"): ((31.2401, 121.4866), "The Bund (กลางวัน)"), (2, "16:15"): ((31.2430, 121.4830), "Rockbund"), (2, "17:00"): ((31.2465, 121.4835), "Rei Flower"), (2, "18:00"): ((31.2500, 121.4940), "Manner North Bund"), (2, "19:00"): ((31.2422, 121.4861), "The Bund"), (2, "20:00"): ((31.2386, 121.4780), "Dongsheng Buffet"),
 (4, "09:45"): ((31.2068, 121.4352), "Grandma's Home"), (4, "12:00"): ((31.2160, 121.4376), "13DE MARZO"), (4, "11:00"): ((31.2063, 121.4337), "Wukang Mansion"),





 (3, "08:30"): ((31.1456, 121.6536), "Disneyland"), (3, "10:00"): ((31.1456, 121.6536), "Disneyland"), (3, "13:00"): ((31.1456, 121.6536), "Disneyland"), (3, "15:00"): ((31.1456, 121.6536), "Disneyland"), (3, "18:00"): ((31.1456, 121.6536), "Disneyland"), (3, "21:15"): ((31.1456, 121.6536), "Disneyland"),

 (7, "10:00"): ((31.2392, 121.4863), "Cocina 19"), 
 (7, "12:00"): ((31.2428, 121.4838), "Luneurs"), (7, "20:00"): ((31.2416, 121.4842), "Christmas Market"), (7, "16:30"): ((31.2387, 121.4947), "Superbrand Mall"), (7, "17:30"): ((31.2401, 121.4961), "สะพานลอยวงกลม"), (7, "18:30"): ((31.2392, 121.4956), "Chef Fei"),
 (8, "08:00"): (PVG_LL, "สนามบินผู่ตง T2"),
}
import json
import sys as _sys, os as _os2; _sys.path.insert(0, _os2.path.dirname(_os2.path.abspath(__file__)))
from tiles import plan as tile_plan
ALL_TILES = []

import math as _m
def wgs2gcj(lat, lng):
    """WGS-84 -> GCJ-02 (the shifted coordinates Amap uses inside China)."""
    a, ee = 6378245.0, 0.00669342162296594323
    x, y = lng - 105.0, lat - 35.0
    dlat = -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*x*y + 0.2*_m.sqrt(abs(x)) + (20.0*_m.sin(6.0*x*_m.pi) + 20.0*_m.sin(2.0*x*_m.pi))*2.0/3.0 + (20.0*_m.sin(y*_m.pi) + 40.0*_m.sin(y/3.0*_m.pi))*2.0/3.0 + (160.0*_m.sin(y/12.0*_m.pi) + 320*_m.sin(y*_m.pi/30.0))*2.0/3.0
    dlng = 300.0 + x + 2.0*y + 0.1*x*x + 0.1*x*y + 0.1*_m.sqrt(abs(x)) + (20.0*_m.sin(6.0*x*_m.pi) + 20.0*_m.sin(2.0*x*_m.pi))*2.0/3.0 + (20.0*_m.sin(x*_m.pi) + 40.0*_m.sin(x/3.0*_m.pi))*2.0/3.0 + (150.0*_m.sin(x/12.0*_m.pi) + 300.0*_m.sin(x/30.0*_m.pi))*2.0/3.0
    rad = lat/180.0*_m.pi; magic = 1 - ee*_m.sin(rad)**2; sq = _m.sqrt(magic)
    dlat = (dlat*180.0)/((a*(1-ee))/(magic*sq)*_m.pi); dlng = (dlng*180.0)/(a/sq*_m.cos(rad)*_m.pi)
    return lat + dlat, lng + dlng
def _mk(t): return re.sub(r"[,|&#]", " ", t).strip()
def day_all_links(stops, n):
    hotel = {"lat": HOTEL_LL[0], "lng": HOTEL_LL[1]}
    pts = [dict(hotel, label="ที่พัก 海玥名庭酒店")] + [dict(s, label=f'{k+1} {s["zh"] or s["name"]}') for k, s in enumerate(stops)]
    if n == 8: pts = pts  # still show hotel as the start
    mk = "|".join(f'{g[1]:.6f},{g[0]:.6f},{_mk(p["label"])}' for p in pts[:10] for g in [wgs2gcj(p["lat"], p["lng"])])
    amap_url = "https://uri.amap.com/marker?markers=" + quote(mk, safe=",|") + "&src=shanghai-trip&callnative=1"
    seq = [hotel] + stops + ([] if n in (1, 8) else [hotel])
    if n == 1: seq = stops + [hotel]
    o, dst, way = seq[0], seq[-1], seq[1:-1]
    g_url = (f'https://www.google.com/maps/dir/?api=1&origin={o["lat"]},{o["lng"]}&destination={dst["lat"]},{dst["lng"]}'
             + (("&waypoints=" + quote("|".join(f'{w["lat"]},{w["lng"]}' for w in way[:9]), safe=",")) if way else ""))
    return (f'<div class="mall"><a class="mall-a" href="{E(amap_url)}" target="_blank" rel="noopener">🧭 ทุกจุดใน Amap</a>'
            f'<a class="mall-g" href="{E(g_url)}" target="_blank" rel="noopener">🗺️ เส้นทาง Google</a></div>')

def day_geo(d):
    stops = []
    for i, e in enumerate(d["events"]):
        g = GEO.get((d["n"], e["t"]))
        if g:
            e["eid"] = f"e{d['n']}-{i}"
            stops.append({"id": e["eid"], "lat": g[0][0], "lng": g[0][1], "name": g[1], "t": e["t"], "zh": e.get("zh", "")})
    if not stops: return ""
    route = stops[:]
    if d["n"] == 1: route = stops + [{"hotel": 1}]
    elif d["n"] == 8: route = [{"hotel": 1}] + stops
    else: route = [{"hotel": 1}] + stops + [{"hotel": 1}]
    data = {"hotel": {"lat": HOTEL_LL[0], "lng": HOTEL_LL[1]}, "route": route}
    pts = [HOTEL_LL if p.get("hotel") else (p["lat"], p["lng"]) for p in route]
    tp = tile_plan(pts)
    data.update(minZoom=tp["minZoom"], maxZoom=tp["maxZoom"], view=tp["bounds"])
    for t in tp["tiles"]:
        if t not in ALL_TILES: ALL_TILES.append(t)
    legend = "".join(f'<button type="button" class="mleg" data-go="{s["id"]}" title="{E(s["name"])}"><b>{k+1}</b><span>{E(s["name"])}</span></button>' for k, s in enumerate(stops))
    return (f'<figure class="dmap" data-geo="{E(json.dumps(data, ensure_ascii=False))}">'
            f'<button type="button" class="mfs" aria-label="ดูแผนที่ทั้งวันเต็มจอ"><span class="mfs-o">⛶ เต็มจอ</span><span class="mfs-c">✕ ปิด</span></button>'
            f'<div class="lmap" aria-label="แผนที่เส้นทางวันที่ {d["n"]}"></div>'
            f'<svg class="msvg" role="img" aria-label="แผนผังเส้นทางวันที่ {d["n"]}"></svg>'
            f'<figcaption><span class="mlegs">{legend}</span>{day_all_links(stops, d["n"]) if len(stops) > 1 else ""}<small class="mnote">แตะหมุดเพื่อดูกิจกรรม · 🏨 = ที่พัก</small></figcaption></figure>')

# HD photos from Wikimedia Commons (see img/hd/credits.json): old image name or (day, time) -> key
import os as _os
_CRED = {r[0]: r for r in json.load(open(_os.path.join(_os.path.dirname(OUT) or ".", "img/hd/credits.json"), encoding="utf-8"))}
HD_BY_OLD = {"bkk": "bkk", "peoples-square": "peoples", "nanjing-road": "nanjing", "bund": "bund", "wukang-road": "wukang",
             "xintiandi": "xintiandi", "yu-garden": "yu", "disneyland": "disney", "castle": "castle", "adventure-isle": "adventure",
             "treasure-cove": "treasure", "pvg": "pvg", "fireworks": "fireworks", "superbrand": "superbrand", "huaihai-road": "huaihai"}
HD_BY_SLOT = {(2, "20:00"): "dongsheng", (4, "16:45"): "butterful", (5, "16:45"): "bagel", (5, "20:00"): "huaihai", (5, "13:00"): "westbund", (4, "15:00"): "wnanjing", (4, "13:00"): "jingan", (6, "08:00"): "sz-shstation", (6, "08:40"): "sz-train", (6, "09:30"): "sz-garden", (6, "11:00"): "sz-pingjiang", (6, "13:00"): "sz-noodle", (6, "15:00"): "sz-shantang", (6, "18:00"): "sz-fish", (6, "19:30"): "sz-station", (2, "16:15"): "rockbund", (2, "13:30"): "no1dept", (2, "17:00"): "waibaidu", (2, "18:00"): "northbund", (3, "10:00"): "zootopia", (1, "16:45"): "spring", (8, "12:05"): "spring", (7, "17:30"): "ljznight", (8, "08:00"): "pvg", (2, "15:45"): "bundday", (4, "12:00"): "marzo", (7, "12:00"): "luneurs", (7, "20:00"): "xmas",}
for _d in DAYS:
    for _e in _d["events"]:
        _e["hd"] = HD_BY_SLOT.get((_d["n"], _e["t"])) or HD_BY_OLD.get(_e["img"] or "")
def commons_page(name):
    return "https://commons.wikimedia.org/wiki/File:" + quote(name.replace(" ", "_"))
def credit_html(key):
    r = _CRED[key]
    if not r[3]:
        return ""
    return (f'<small class="credit">ภาพ: {E(r[5])} · <a href="{E(commons_page(r[3]))}" target="_blank" rel="noopener">{E(r[4])}</a></small>')


# Chinese names for the summary pictures (ไทย / 中文 switch)
ZH_DAY = {1: "出发去上海", 2: "人民广场 + 外滩", 4: "武康路 + 静安寺 + 南京西路", 5: "喜粤8号 + 西岸 + 新天地", 3: "上海迪士尼乐园", 6: "苏州一日游 · 拙政园 + 平江路 + 山塘街", 7: "Cocina 19 + 外滩 + 陆家嘴", 8: "回国"}
SKIP = {
 (2, "17:00"): "คาเฟ่ 2 ร้านติดกัน เลือกไปร้านเดียวก็พอ",
 (2, "18:00"): "คาเฟ่ 2 ร้านติดกัน เลือกไปร้านเดียวก็พอ",


 (7, "13:30"): "แวะเฉพาะถ้ายังไม่ได้ไซซ์",
 (7, "20:00"): "คืนสุดท้าย ถ้าเหนื่อยกลับไปเก็บกระเป๋าก่อน",
}

ZH_EV = {
 (4, "14:00"): "PANE 球鞋（永源路22号）",
 (5, "16:45"): "New York Bagelous Museum（新天地时尚 L111）", (4, "16:45"): "黄油与面包 Butterful & Creamorous（吴江路289号）",
 (5, "09:45"): "Pushing Coffee 狗狗咖啡（茂名路）",
 (5, "17:30"): "PANE 球鞋（TX淮海 淮海中路523号）",
 (5, "20:00"): "淮海中路 散步回酒店",
 (5, "11:15"): "喜粤8号（汝南街）", (5, "13:00"): "西岸梦中心", (5, "16:00"): "新天地", (5, "18:30"): "牛New寿喜烧（淮海中路755号 3楼）",
 (4, "13:00"): "静安寺", (4, "15:00"): "南京西路 逛街", (4, "17:30"): "很久以前羊肉串（南京西路818广场店）",
 (6, "08:00"): "去上海站", (6, "08:40"): "高铁去苏州站", (6, "09:30"): "拙政园", (6, "11:00"): "平江路 · 租汉服拍照", (6, "13:00"): "苏式汤面（裕兴记）", (6, "15:00"): "山塘街 · 坐船", (6, "18:00"): "苏帮菜 · 松鼠桂鱼", (6, "19:30"): "高铁回上海",
 (1, "13:45"): "曼谷素万那普机场 值机", (1, "16:45"): "航班 9C7284 曼谷 → 上海浦东", (1, "22:05"): "抵达浦东国际机场 2号航站楼", (1, "23:45"): "入住 海玥名庭酒店 淮海中路",
 (2, "11:00"): "从酒店出发 去人民广场", (2, "11:30"): "莱莱小笼（天津路）", (2, "13:30"): "第一百货商业中心（南京东路830号）", (2, "14:30"): "南京路步行街", (2, "15:45"): "外滩 · 白天拍照", (2, "16:15"): "外滩源（圆明园路 · 虎丘路）", (2, "17:00"): "汭REi·FLOWER COFFEE BAR（北苏州路234号）", (2, "18:00"): "MANNER 咖啡（北外滩国客中心滨江店）", (2, "19:00"): "外滩 · 黄浦江夜景", (2, "20:00"): "东盛自助料理（悦荟广场店 南京东路353号 5楼）",
 (4, "12:00"): "13DE MARZO 小熊咖啡（安福路322号）", (4, "09:45"): "奶奶家（武康路店）", (4, "11:00"): "武康路 · 武康大楼",

 (3, "07:00"): "从酒店出发 去上海迪士尼", (3, "08:30"): "奇幻童话城堡", (3, "10:00"): "疯狂动物城 + 明日世界", (3, "13:00"): "探险岛", (3, "15:00"): "宝藏湾",
 (3, "18:00"): "园内晚餐", (3, "21:15"): "点亮奇梦 + 烟花表演", (3, "22:00"): "回酒店",

 (7, "10:00"): "Cocina 19 西班牙餐厅（外滩 福州路19号）", (7, "12:00"): "Luneurs 面包冰淇淋（圆明园路133号）", (7, "20:00"): "外滩源 圣诞市集 夜景", (7, "13:30"): "PANE（TX淮海）备选", (7, "16:30"): "正大广场（陆家嘴）", (7, "17:30"): "陆家嘴环形天桥 · 国金中心 · 金茂大厦 拍照", (7, "18:30"): "费大厨辣椒炒肉（陆家嘴）", (7, "21:45"): "整理行李",
 (8, "07:30"): "海玥名庭酒店 退房", (8, "08:00"): "去浦东国际机场 2号航站楼", (8, "09:00"): "机场 值机 + 早餐", (8, "12:05"): "航班 9C7283 上海浦东 → 曼谷",
}
for _d in DAYS:
    _d["zh"] = ZH_DAY.get(_d["n"], "")
    for _e in _d["events"]:
        _e["zh"] = ZH_EV.get((_d["n"], _e["t"]), "")
        _e["skip"] = SKIP.get((_d["n"], _e["t"]), "")


def event_html(e, go=None):
    tag = f' <span class="tag">{E(e["tag"])}</span>' if e["tag"] else ""
    note = e["note"] if e["html_note"] else E(e["note"])
    if e.get("hd"):
        k = e["hd"]
        img = (f'<figure class="ph"><img class="thumb" src="img/hd/{k}-640.webp" srcset="img/hd/{k}-640.webp 640w, img/hd/{k}-1280.webp 1280w" '
               f'sizes="(max-width: 640px) calc(100vw - 110px), 520px" alt="{E(e["title"])}" loading="lazy" decoding="async">{credit_html(k)}</figure>')
    else:
        img = (f'<figure class="ph"><img class="thumb" src="img/{e["img"]}.jpg" alt="{E(e["title"])}" loading="lazy" decoding="async"></figure>' if e["img"] else "")
    eid = f' id="{e["eid"]}"' if e.get("eid") else ""
    gat = f' data-go="{go[0]}|{go[1]}"' if go else ""
    return (f'<li class="ev"{eid}{gat} data-t="{e["data_t"]}" data-kind="{e["kind"]}" data-zh="{E(e.get("zh", ""))}" style="--dot:{KIND_DOT[e["kind"]]}">'
            f'<time>{E(e["t"])}</time><span class="dot" aria-hidden="true"></span>'
            f'<div class="evb">{img}<h3>{E(e["title"])}{tag}</h3>'
            + (f'<div class="skip">😮‍💨 ข้ามได้ถ้าเหนื่อย <small>· {E(e["skip"])}</small></div>' if e.get("skip") else "")
            + (f'<p>{note}</p>' if note else "") + links_html(e["links"]) + '</div></li>')

# what to have in the bag the next morning (shown on the "Tomorrow" card the evening before)
BRING_DEFAULT = "พาสปอร์ต · Alipay/WeChat Pay · พาวเวอร์แบงก์ · ซิม/eSIM"
BRING = {
    1: "พาสปอร์ต · ตั๋วเครื่องบิน 9C7284 · เงินหยวนสำรอง · ซิม/eSIM · แบตสำรอง (ถือขึ้นเครื่อง)",
    3: "ตั๋ว Disney (QR ในแอป) · พาสปอร์ตตัวจริง (ใช้เข้าสวน) · พาวเวอร์แบงก์ · ผ้าพันคอ/ถุงมือ (ดูพลุตอนค่ำหนาว)",
    6: "พาสปอร์ตตัวจริง (ขึ้นรถไฟ + เข้าสวน 拙政园) · ตั๋วรถไฟไป–กลับ · ตั๋วสวน · พาวเวอร์แบงก์",
    7: "พาสปอร์ต · Alipay · พาวเวอร์แบงก์ · คืนนี้เริ่มเก็บกระเป๋า",
    8: "พาสปอร์ต · ตั๋วเครื่องบิน 9C7283 · เช็คเอาท์ 07:30 · ของฝากโหลดใต้เครื่อง · ของเหลวไม่เกิน 100 ml",
}

def day_route(d):
    """pins, route and how each leg is travelled (shared by the plan page and the tour)"""
    import re as _r
    n = d["n"]
    evs = d["events"]
    pts = [(e["t"], GEO[(n, e["t"])][0]) for e in evs if (n, e["t"]) in GEO]
    suzhou = any(ll[1] < 121.0 for _, ll in pts)
    if suzhou:
        pts = [(t, ll) for t, ll in pts if ll[1] < 121.0]
    pins, idx = [], {}
    for t, ll in pts:
        key = (round(ll[0], 3), round(ll[1], 3))
        if key not in idx:
            idx[key] = len(pins) + 1; pins.append([ll[0], ll[1]])
        idx[t] = idx[key]
    if not pins or n == len(DAYS):
        return dict(pins=pins, idx=idx, suzhou=suzhou, route=[], segs=[], first_ev={})
    route = ([] if suzhou else [list(HOTEL_LL)]) + pins
    if n == 1:
        route = pins + [list(HOTEL_LL)]
    # how each leg is travelled: read the destination's note, fall back to distance
    first_ev = {}
    for e in evs:
        k = idx.get(e["t"])
        if k and k not in first_ev:
            first_ev[k] = e
    def km(a, b):
        import math
        la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
        h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
        return 6371 * 2 * math.asin(math.sqrt(h))
    KW = [("🚄", r"รถไฟความเร็วสูง|高铁|Maglev"), ("🚕", r"Didi|แท็กซี่"), ("🚇", r"รถไฟฟ้า|Metro|สาย \d"), ("🚶", r"เดิน")]
    segs = []
    for i in range(len(route) - 1):
        A, B = route[i], route[i + 1]; dist = km(A, B)
        if dist < 0.15:
            continue
        dest = None
        if B in pins:
            dest = first_ev.get(pins.index(B) + 1)
        note = (dest or {}).get("note", "") if dest else ""
        mode, mins = None, None
        # only trust phrases that describe arriving here: "จาก <place> <mode> ~N นาที"
        for ph in _r.findall(r"จาก[^·]{0,60}", note):
            for ic, rx in KW:
                m = _r.search(rx, ph)
                if m:
                    mode = ic
                    mm = _r.search(r"(\d+)\s*นาที", ph[m.start():])
                    mins = int(mm.group(1)) if mm else None
                    break
            if mode:
                break
        if mode is None:
            mode = "🚶" if dist < 1.2 else "🚕"
        if mins is None:
            mins = {"🚶": dist * 13, "🚇": 8 + dist * 2.2, "🚄": 30}.get(mode, (5 + dist * 2.6) if dist < 15 else (10 + dist * 1.2))
            mins = max(5, int(round(mins / 5.0) * 5))
        segs.append({"a": A, "b": B, "m": mode, "min": mins})
    return dict(pins=pins, idx=idx, suzhou=suzhou, route=route, segs=segs, first_ev=first_ev)

def arrivals(d):
    """{event time: (mode, minutes)} for the leg that ends at that event"""
    r = day_route(d); out = {}
    for g in r["segs"]:
        if g["b"] in r["pins"]:
            ev = r["first_ev"].get(r["pins"].index(g["b"]) + 1)
            if ev: out[ev["t"]] = (g["m"], g["min"])
    return out

DAY_COVER = {1: "spring", 2: "bund", 4: "wukang", 5: "xintiandi", 3: "castle", 6: "sz-garden", 7: "ljznight", 8: "pvg"}
def day_html(d):
    disney = ' <span class="tag gold">DISNEY DAY</span>' if d.get("disney") else ""
    mp = day_geo(d)
    arr = arrivals(d)
    evs = "".join(event_html(e, arr.get(e["t"])) for e in d["events"])
    g = d.get("guide")
    guide = f'<details class="tip day-guide"><summary>{E(g[0])}</summary><div class="dg">{g[1]}</div></details>' if g else ""
    return f'''
    <section class="day" id="day-{d["n"]}" data-day="{d["n"]}" data-date="{d["iso"]}" data-zh="{E(d.get("zh", ""))}" data-cover="img/hd/{DAY_COVER.get(d["n"], "hero")}-640.webp" data-bring="{E(BRING.get(d["n"], BRING_DEFAULT))}" aria-label="วันที่ {d["n"]}">
      <div class="dayhead">
        <div class="num">{d["n"]}</div>
        <div class="dh-txt"><h3>{E(d["title"])}{disney}</h3><p>{E(d["date"])} · <span class="wxb" data-date="{d["iso"]}">{E(d["wx"])}</span></p></div>
        <div class="dicon" aria-hidden="true">{d["icon"]}</div>
      </div>
      {mp}
      <ol class="tl">{evs}</ol>
      <div class="note"><span aria-hidden="true">⭐</span><span>{E(d["note"])}</span></div>{guide}
    </section>'''

LANTERN_SVG = ('<svg viewBox="0 0 40 92" aria-hidden="true"><line x1="20" y1="0" x2="20" y2="18" stroke="#E8C877" stroke-width="2"/>'
  '<rect x="12" y="16" width="16" height="6" rx="2" fill="#E8C877"/><ellipse cx="20" cy="44" rx="17" ry="22" fill="#C2303A"/>'
  '<ellipse class="glow" cx="20" cy="44" rx="12" ry="16" fill="#FFB36B"/><g stroke="#8A1A22" stroke-width="1.4" fill="none" opacity=".6">'
  '<ellipse cx="20" cy="44" rx="10" ry="22"/><ellipse cx="20" cy="44" rx="4" ry="22"/></g><rect x="12" y="64" width="16" height="5" rx="2" fill="#E8C877"/>'
  '<g stroke="#E8C877" stroke-width="1.6"><line x1="17" y1="69" x2="16" y2="86"/><line x1="20" y1="69" x2="20" y2="89"/><line x1="23" y1="69" x2="24" y2="86"/></g></svg>')
LANTERNS = '<div class="lanterns" aria-hidden="true">' + "".join(f'<span class="lan l{i}">{LANTERN_SVG}</span>' for i in range(3)) + '</div>'

tabs = tabs = "".join(f'<button type="button" class="dtab" data-day="{d["n"]}" aria-controls="day-{d["n"]}"><b>{d["n"]}</b><span>{d["dow"]} {d["iso"][-2:].lstrip("0")}</span></button>' for d in DAYS)
days = "".join(day_html(d) for d in DAYS)

bmax = max(b[1] for b in BUDGET)
budget_rows = "".join(f'<li><span class="bi" aria-hidden="true">{i}</span><span class="bl">{E(l)}</span><span class="ba">{a:,} ฿</span><span class="bbar"><i style="width:{a/bmax*100:.1f}%"></i></span></li>' for l, a, i in BUDGET)

CHECK_SVG = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5"/></svg>'
def _pack_li(k, ic, t):
    return f'<li class="packing-item" id="pack-{k}"><label><input type="checkbox" data-key="{k}"><span class="pack-box">{CHECK_SVG}</span><span class="packing-txt">{ic} {E(t)}</span></label></li>'
book_rows = "".join(_pack_li(*x) for x in BOOK)
pack_rows = "".join(_pack_li(*x) for x in PACK)

sos_rows = "".join(f'<a class="sos" href="tel:{tel}"><span class="si" aria-hidden="true">{ic}</span><span><b>{E(n)}</b><small>{E(sub)}</small><em>{E(num)}</em></span></a>' for tel, ic, n, sub, num in SOS)

phr_rows = "".join(f'<button type="button" class="phr" data-say="{E(zh)}"><span><span class="zh">{E(zh)}</span><span class="th">{E(th)} · {E(py)}</span></span><span class="spk" aria-hidden="true">🔊</span></button>' for zh, py, th in PHRASES)

PANE_SIZES = [str(x) for x in range(35, 47)]
PANE_PHR = [
 ("你好，请问这款有 {s} 码吗？", "สวัสดี รุ่นนี้มีไซซ์ {s} ไหม"),
 ("可以试穿吗？", "ขอลองใส่ได้ไหม"),
 ("还有别的颜色吗？", "มีสีอื่นไหม"),
 ("有大一码 / 小一码的吗？", "มีไซซ์ใหญ่ขึ้น / เล็กลงหนึ่งเบอร์ไหม"),
 ("什么时候到货？", "ของจะเข้าวันไหน"),
 ("其他门店有货吗？（TX淮海 / 永源路）", "สาขาอื่นมีของไหม (TX Huaihai / Yongyuan Road)"),
 ("可以帮我留一双吗？我们 {d} 来拿。", "ช่วยเก็บไว้ให้ 1 คู่ได้ไหม เราจะมารับ{dt}"),
 ("可以用支付宝吗？", "จ่ายด้วย Alipay ได้ไหม"),
]
PANE_DAYS = [("12月8日", "วันที่ 8 ธ.ค."), ("12月9日", "วันที่ 9 ธ.ค."), ("12月11日", "วันที่ 11 ธ.ค.")]
def _pane_phr(zh, th):
    z = zh.replace("{s}", '<b class="pn-s">40</b>').replace("{d}", '<b class="pn-d">12月11日</b>')
    t = th.replace("{s}", '<b class="pn-s">40</b>').replace("{dt}", '<b class="pn-dt">วันที่ 10 ธ.ค.</b>')
    say = zh.replace("{s}", "40").replace("{d}", "12月11日").replace(" ", "")
    return (f'<button type="button" class="phr pn-phr" data-tpl="{E(zh)}" data-say="{E(say)}"><span><span class="zh">{z}</span>'
            f'<span class="th">{t}</span></span><span class="spk" aria-hidden="true">🔊</span></button>')
pane_rows = "".join(_pane_phr(z, t) for z, t in PANE_PHR)
pane_size_opts = "".join(f'<option value="{x}"{" selected" if x == "40" else ""}>{x}</option>' for x in PANE_SIZES)
pane_day_opts = "".join(f'<option value="{z}" data-th="{E(t)}"{" selected" if z == "12月11日" else ""}>{E(t)}</option>' for z, t in PANE_DAYS)
QUEUE_PHR = [
 ("你好，我们两位，要排队吗？", "สวัสดี มา 2 คน ต้องต่อคิวไหม"),
 ("请问在哪里取号？", "รับบัตรคิวที่ไหน"),
 ("大概要等多久？", "ต้องรอประมาณนานเท่าไร"),
 ("我们的号是 …", "คิวของเราเบอร์ … (ยื่นหน้าจอให้ดู)"),
 ("过号了，还可以进吗？", "เลยคิวไปแล้ว ยังเข้าได้ไหม"),
]
queue_rows = "".join(f'<button type="button" class="phr" data-say="{E(z.replace(" …", ""))}"><span><span class="zh">{E(z)}</span><span class="th">{E(t)}</span></span><span class="spk" aria-hidden="true">🔊</span></button>' for z, t in QUEUE_PHR)
QUEUE_SHOPS = [("วันที่ 2 · 11:30", "Lai Lai", "莱莱小笼"), ("วันที่ 2 · 20:00", "Dongsheng Buffet", "东盛自助料理 悦荟广场"),
               ("วันที่ 4 · 09:45", "Grandma's Home", "奶奶家 武康路"), ("วันที่ 4 · 17:30", "Long Time Ago (818 Plaza)", "很久以前羊肉串 南京西路818"), ("วันที่ 7 · 18:30", "Chef Fei", "费大厨 陆家嘴")]
queue_shops = "".join(f'<li><b>{E(d)}</b> {E(n)} · ค้นว่า <span class="q-zh" lang="zh-CN">{E(z)}</span></li>' for d, n, z in QUEUE_SHOPS)
tips_rows = "".join(f'<details class="tip"><summary><span aria-hidden="true">{ic}</span>{E(h)}</summary><p>{E(t)}</p></details>' for ic, h, t in TIPS)

import datetime as _dt
BUILD = _dt.datetime.now(_dt.timezone(_dt.timedelta(hours=7)))
BUILD_ID = BUILD.strftime('%Y%m%d%H%M%S')
_TH_MON = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
BUILD_TH = f"{BUILD.day} {_TH_MON[BUILD.month-1]} {BUILD.year} {BUILD:%H:%M}"
CSS = open(sys.argv[2] if len(sys.argv) > 2 else _osroot.path.join(_HERE, "site.css"), encoding="utf-8").read()
JS = open(sys.argv[3] if len(sys.argv) > 3 else _osroot.path.join(_HERE, "site.js"), encoding="utf-8").read()

# ---- A4 print document (shown only when printing) ----
def _plain(t):
    return re.sub(r"<[^>]+>", "", t or "").replace("&amp;", "&")
def _short(t, n=2):
    parts = [x.strip() for x in _plain(t).split(" · ") if x.strip()]
    return " · ".join(parts[:n])
KIND_EMO = {"fly": "✈️", "stay": "🏨", "food": "🍜", "see": "📍", "shop": "🛍️", "go": "🚇"}
def _ev_src(e):
    if e.get("hd"): return f'img/hd/{e["hd"]}-640.webp'
    if e.get("img"): return f'img/{e["img"]}.jpg'
    return ""
def _pr_day(d):
    rows = []
    cnt = len(d["events"])
    keep = 2 if cnt >= 10 or d["n"] == 1 else 3 if cnt >= 7 else 5 if cnt >= 5 else 7
    for i, e in enumerate(d["events"]):
        tag = f' <span class="p-tag">{E(e["tag"])}</span>' if e["tag"] else ""
        note = _short(e["note"], keep)
        src = _ev_src(e)
        pic = f'<img class="p-pic" data-psrc="{src}" alt="">' if src else f'<span class="p-pic p-emo">{KIND_EMO.get(e["kind"], "📍")}</span>'
        zh = e.get("zh", "")
        rows.append(f'<div class="p-ev {"alt" if i % 2 else ""}"><span class="p-time">{E(e["t"])}</span>{pic}<div class="p-body"><b>{E(e["title"])}</b>{tag}'
                    + (f'<div class="p-n">{E(note)}</div>' if note else "") + (f'<div class="p-zh" lang="zh-CN">{E(zh)}</div>' if zh else "") + '</div></div>')
    disney = " · DISNEY DAY" if d.get("disney") else ""
    return (f'<section class="p-day p-d{d["n"]}" style="--n:{cnt}"><h3><span class="p-num">{d["n"]}</span><span class="p-dt"><small>{E(d["date"])} 2026{disney} · {E(d["wx"])}</small>{E(d["title"])}</span><span class="p-dzh" lang="zh-CN">{E(d.get("zh", ""))}</span></h3>'
            f'<div class="p-evs">{"".join(rows)}</div>'
            + (f'<p class="p-tip">⭐ {E(_plain(d["note"]))}</p>' if d.get("note") else "") + '</section>')
_pr_over = "".join(f'<tr><td class="p-t">{d["n"]}</td><td>{E(d["date"])}</td><td><b>{E(d["title"])}</b></td><td class="p-zh" lang="zh-CN">{E(d.get("zh", ""))}</td></tr>' for d in DAYS)
_pr_budget = "".join(f'<tr><td>{E(l)}</td><td class="p-r">{a:,} ฿</td></tr>' for l, a, i in BUDGET)
_pr_sos = "".join(f'<tr><td><b>{E(n)}</b><div class="p-n">{E(sub)}</div></td><td class="p-r p-mono">{E(num)}</td></tr>' for tel, ic, n, sub, num in SOS)
_pr_phr = "".join(f'<tr><td class="p-zh" lang="zh-CN">{E(zh)}</td><td class="p-n">{E(py)}</td><td>{E(th)}</td></tr>' for zh, py, th in PHRASES)
_pr_pack = "".join(f'<li>☐ {E(t)}</li>' for k, ic, t in BOOK + PACK)
PRINTDOC = f"""
<div id="printdoc" aria-hidden="true">
  <header class="p-head"><img class="p-hero" data-psrc="img/hd/hero-960.webp" alt=""><div class="p-hin"><small>SHANGHAI · DECEMBER 2026 · Toonzii &amp; Bear</small><h1>แผนเที่ยวเซี่ยงไฮ้ 8 วัน 7 คืน</h1><p>เสาร์ 5 – เสาร์ 12 ธันวาคม 2026 · พิมพ์จากเว็บ อัปเดต {BUILD_TH}</p></div></header>
  <div class="p-grid">
    <div class="p-box"><h4>✈️ เที่ยวบิน Spring Airlines</h4><table class="p-tbl"><tbody>
      <tr><td><b>ขาไป</b> ส. 5 ธ.ค.</td><td class="p-mono">9C7284</td><td>BKK 16:45 → PVG 22:05</td></tr>
      <tr><td><b>ขากลับ</b> ส. 12 ธ.ค.</td><td class="p-mono">9C7283</td><td>PVG 12:05 → BKK 15:45</td></tr></tbody></table>
      <div class="p-n">กระเป๋า: ถือขึ้น 1 ชิ้น ≤10 กก. (55×40×20 ซม.) · โหลด 20 กก. · ไม่มีอาหารฟรี</div></div>
    <div class="p-box"><h4>🏨 ที่พัก 7 คืน</h4><b>Atour X Hotel · Huaihai Middle Road</b><div lang="zh-CN" class="p-zh">海玥名庭酒店（上海静安寺淮海中路店）· 上海市徐汇区淮海中路1329号云海大厦</div>
      <div class="p-n">ใกล้ MRT Changshu Road (สาย 1, 7) · โทร +86 150 0212 8856, +86 21 3356 1052 · เช็คอิน 14:00 เช็คเอาท์ 12:00</div></div>
  </div>
  <h2>ภาพรวม 8 วัน</h2>
  <table class="p-tbl p-over"><tbody>{_pr_over}</tbody></table>
  <h2>แผนรายวัน</h2>
  {"".join(_pr_day(d) for d in DAYS)}
  <section class="p-help">
    <h2>ยื่นให้คนขับ · 请带我去</h2>
    <div class="p-grid">
      <div class="p-taxi"><small>ไปที่พัก</small><div lang="zh-CN">上海市徐汇区<br>淮海中路1329号 云海大厦<br>海玥名庭酒店</div></div>
      <div class="p-taxi"><small>ไปสนามบิน (ขากลับ)</small><div lang="zh-CN">浦东国际机场<br>2号航站楼</div></div>
    </div>
    <div class="p-grid">
      <div><h2>เบอร์ฉุกเฉิน</h2><table class="p-tbl"><tbody>{_pr_sos}</tbody></table></div>
      <div><h2>ประโยคที่ใช้บ่อย</h2><table class="p-tbl"><tbody>{_pr_phr}</tbody></table>
        <h2>งบต่อคน</h2><table class="p-tbl"><tbody>{_pr_budget}<tr><td><b>รวม</b></td><td class="p-r"><b>{TOTAL:,} ฿</b></td></tr></tbody></table></div>
    </div>
    <h2>เช็กลิสต์ก่อนออกเดินทาง</h2><ul class="p-pack">{_pr_pack}</ul>
  </section>
</div>"""

page = f'''<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="เซี่ยงไฮ้ 2026">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#0F3A54">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" sizes="180x180" href="icon-180.png">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="icon" href="favicon-32.png" type="image/png" sizes="32x32">
<meta name="build" content="{BUILD_ID}">
<link rel="preload" href="fonts/noto-sans-thai-thai-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="vendor/leaflet/leaflet.css" media="print" onload="this.media='all'">
<link rel="preload" href="fonts/kanit-thai-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<title>แผนเที่ยวเซี่ยงไฮ้ 8 วัน 7 คืน ธันวาคม 2026</title>
<script>try{{var t=localStorage.getItem('hkTripTheme');if(t==='dark'||(!t&&matchMedia('(prefers-color-scheme: dark)').matches))document.documentElement.setAttribute('data-theme','dark')}}catch(e){{}}</script>
<script>if(navigator.standalone)document.documentElement.classList.add('ios-app')</script>
<style>
{CSS}
</style>
</head>
<body>
<canvas id="snow" aria-hidden="true"></canvas>
<main class="wrap">

  <header class="hero" id="top">
    <canvas class="fw" id="fw" aria-hidden="true"></canvas>
    {LANTERNS}
    <button class="snow-btn" id="snow-btn" type="button" aria-pressed="true" aria-label="ปิดเปิดหิมะ">❄️</button>
    <button class="theme-toggle-btn" id="theme-toggle-btn" type="button" aria-label="สลับโหมดมืด"><span class="tt-stars">✦ ✧ ✦</span><span class="tt-cloud">☁️</span><span class="tt-knob"></span></button>
    <div class="eyebrow">SHANGHAI · DECEMBER 2026</div>
    <h1 id="hero-title">เซี่ยงไฮ้ 8 วัน 7 คืน</h1>
    <p class="sub">5–12 ธ.ค. 2026 · ไฟคริสต์มาส The Bund · Disneyland</p>
    <div class="cd" id="cd" role="timer" aria-label="นับถอยหลังถึงวันเดินทาง"></div>
    <p class="cd-msg" id="cd-msg"></p>
    <div class="chips"><span class="chip"><i aria-hidden="true">🏨</i><span>Atour X Huaihai</span></span><span class="chip"><i aria-hidden="true">💰</i><span>{TOTAL:,} ฿/คน</span></span><span class="chip"><i aria-hidden="true">🚇</i><span>Metro + Didi</span></span></div>
    <div class="hero-actions">
      <button type="button" class="hbtn" id="share-btn"><span aria-hidden="true">🔗</span>แชร์</button>
      <button type="button" class="hbtn" id="qr-btn"><span aria-hidden="true">📱</span>QR</button>
      <button type="button" class="hbtn" id="print-btn"><span aria-hidden="true">🖨️</span>แพลนเที่ยว + ปริ้น</button>
      <div class="hero-row2"><a class="hbtn hbtn-tour" href="tour.html"><span aria-hidden="true">🎬</span>ดูทริปแบบแอนิเมชัน</a><a class="hbtn hbtn-tour" href="present.html"><span aria-hidden="true">🖥️</span>นำเสนอ</a></div>
    </div>
  </header>

  <aside class="card install" id="install" hidden>
    <button type="button" class="ins-x" id="ins-x" aria-label="ปิด">&times;</button>
    <div class="ins-h"><img src="icon-192.png" alt="" width="44" height="44"><div><b>ติดตั้งเป็นแอปบนมือถือ</b><span>เปิดจากหน้าจอโฮมได้เลย ใช้ได้แม้ไม่มีเน็ต</span></div></div>
    <ol class="ins-ios" id="ins-ios" hidden>
      <li>กดปุ่มแชร์ <span class="kbd"><svg viewBox="0 0 24 24" width="15" height="15" aria-hidden="true"><path d="M12 3v12M8 7l4-4 4 4M5 11v9h14v-9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span> ใน Safari</li>
      <li>เลื่อนลงแล้วเลือก <b>เพิ่มไปยังหน้าจอโฮม</b> (Add to Home Screen)</li>
      <li>กด <b>เพิ่ม</b> มุมขวาบน</li>
    </ol>
    <button type="button" class="btn" id="ins-btn" hidden>📲 ติดตั้งแอป</button>
  </aside>

  <section class="sec" id="weather" aria-labelledby="wx-h">
    <div class="sec-h"><h2 id="wx-h">🌤️ อากาศเซี่ยงไฮ้</h2><span class="sec-note" id="wx-note">ค่าเฉลี่ยช่วงเดือนธันวาคม</span></div>
    <div class="wx" id="wx"></div>
  </section>

  <section class="sec" id="plan" aria-labelledby="plan-h">
    <div class="sec-h"><h2 id="plan-h">🗓️ แผนรายวัน</h2><span class="sec-note" id="today-note"></span></div>
    <div class="dtabs" id="dtabs" role="tablist">{tabs}</div>
    <div class="card days">{days}
    </div>
  </section>

  <section class="sec" id="flights" aria-labelledby="fl-h">
    <div class="sec-h"><h2 id="fl-h">✈️ ตั๋วเครื่องบิน Spring Airlines</h2></div>
    <div class="passw" tabindex="0" role="button" aria-label="พลิกตั๋วดูรายละเอียด"><div class="pass-in">
    <div class="pass">
      <div class="pm">
        <span class="tag">ขาไป · เสาร์ 5 ธ.ค. 2026</span>
        <div class="route"><div class="ap"><b>BKK</b><span>สุวรรณภูมิ</span></div><div class="mid fly" data-dep="2026-12-05T16:45:00+07:00" data-arr="2026-12-05T22:05:00+08:00"><svg aria-hidden="true"><path/></svg><span class="plane" aria-hidden="true">✈️</span><span class="dur">4 ชม. 20 น.</span></div><div class="ap r"><b>PVG</b><span>ผู่ตง อาคาร 2</span></div></div>
        <div class="times"><span>16:45</span><span>22:05</span></div>
        <div class="links"><a href="https://www.flightradar24.com/data/flights/9c7284" target="_blank" rel="noopener">🛫 FR24</a><a href="https://www.flightaware.com/live/flight/CQH7284" target="_blank" rel="noopener">🛫 FlightAware</a><button type="button" class="fly-ip" data-fly="9C7284">📱 iPhone</button></div>
      </div>
      <div class="stub"><small>FLIGHT</small><b>9C7284</b><span class="flip-hint">แตะพลิก ↻</span></div>
      </div>
      <div class="pass-back" aria-hidden="true"><div class="pbk"><span class="tag">9C7284 · ข้อมูลเพิ่มเติม</span><ul><li><b>🧳 กระเป๋า (ต่อคน)</b>ถือขึ้นเครื่อง 1 ชิ้น ≤ 10 กก. · 55×40×20 ซม.</li><li><b>🧳 โหลด</b>รวม 20 กก. · แต่ละชิ้นไม่เกิน 100×60×40 ซม.</li><li><b>🍱 บนเครื่อง</b>ไม่มีอาหารฟรี กินก่อนขึ้นหรือซื้อบนเครื่อง</li><li><b>🛬 ถึง PVG</b>22:05 เวลาจีน · ไปที่พักด้วย Didi ~1 ชม.</li></ul><small>แตะเพื่อพลิกกลับ ↻</small></div></div>
    </div></div>
    <div class="passw back" tabindex="0" role="button" aria-label="พลิกตั๋วดูรายละเอียด"><div class="pass-in">
    <div class="pass back">
      <div class="pm">
        <span class="tag gold">ขากลับ · เสาร์ 12 ธ.ค. 2026</span>
        <div class="route"><div class="ap"><b>PVG</b><span>ผู่ตง อาคาร 2</span></div><div class="mid fly" data-dep="2026-12-12T12:05:00+08:00" data-arr="2026-12-12T15:45:00+07:00"><svg aria-hidden="true"><path/></svg><span class="plane" aria-hidden="true">✈️</span><span class="dur">4 ชม. 40 น.</span></div><div class="ap r"><b>BKK</b><span>สุวรรณภูมิ</span></div></div>
        <div class="times"><span>12:05</span><span>15:45</span></div>
        <div class="links"><a href="https://www.flightradar24.com/data/flights/9c7283" target="_blank" rel="noopener">🛬 FR24</a><a href="https://www.flightaware.com/live/flight/CQH7283" target="_blank" rel="noopener">🛬 FlightAware</a><button type="button" class="fly-ip" data-fly="9C7283">📱 iPhone</button></div>
      </div>
      <div class="stub"><small>FLIGHT</small><b>9C7283</b><span class="flip-hint">แตะพลิก ↻</span></div>
      </div>
      <div class="pass-back" aria-hidden="true"><div class="pbk"><span class="tag gold">9C7283 · ข้อมูลเพิ่มเติม</span><ul><li><b>🧳 กระเป๋า (ต่อคน)</b>ถือขึ้นเครื่อง 1 ชิ้น ≤ 10 กก. · 55×40×20 ซม.</li><li><b>🧳 โหลด</b>รวม 20 กก. · แต่ละชิ้นไม่เกิน 100×60×40 ซม.</li><li><b>⏰ ออกจากที่พัก</b>8:00 ให้ถึงสนามบินราว 9:00 ก่อนบิน 3 ชม.</li><li><b>🍱 บนเครื่อง</b>ไม่มีอาหารฟรี · ชั่งกระเป๋าถือเข้ม</li></ul><small>แตะเพื่อพลิกกลับ ↻</small></div></div>
    </div></div>
    <details class="card more">
      <summary>กระเป๋า เวลาออกจากที่พัก และวิธีเช็กไฟลท์</summary>
      <ul class="facts">
        <li><b>🧳 กระเป๋า (ต่อคน ทั้งไปและกลับ)</b>ถือขึ้นเครื่อง 1 ชิ้น ไม่เกิน 10 กก. ขนาดไม่เกิน 55×40×20 ซม. · โหลดรวม 20 กก. ขนาดแต่ละชิ้นไม่เกิน 100×60×40 ซม. · Spring Airlines ชั่งกระเป๋าถือค่อนข้างเข้ม และไม่มีอาหารฟรีบนเครื่อง</li>
        <li><b>⏰ ขากลับ</b>บิน 12:05 · ออกจากที่พักไปสนามบิน 8:00 (นั่งรถ ~1 ชม.) ให้ถึงก่อนบิน 3 ชม.</li>
        <li><b>📱 เช็กไฟลท์บน iPhone</b>เปิดแอป Notes หรือ iMessage พิมพ์ <b class="mono">Fly 9C7284</b> หรือ <b class="mono">Fly 9C7283</b> แล้วกดค้างที่รหัสที่มีเส้นใต้ เลือก Preview Flight</li>
      </ul>
    </details>
  </section>

  <section class="sec" id="budget" aria-labelledby="bd-h">
    <div class="sec-h"><h2 id="bd-h">💰 งบประมาณต่อคน</h2></div>
    <div class="card">
      <div class="btotal"><span>รวมทั้งหมด</span><b data-n="{TOTAL}">{TOTAL:,} ฿</b></div>
      <ul class="blist">{budget_rows}</ul>
    </div>
    <div class="card fx">
      <h3>💱 แปลงเงินหยวน → บาท</h3>
      <div class="fx-row">
        <div class="fl-field"><span class="fl-yen" aria-hidden="true">¥</span><input type="number" inputmode="decimal" class="currency-input" id="cny-input" placeholder=" "><label for="cny-input">จำนวนหยวน</label></div>
        <div class="currency-result" id="thb-result">= 0.00 ฿</div>
      </div>
      <div class="cny-chips"><button type="button" class="cny-chip" data-v="50">¥50</button><button type="button" class="cny-chip" data-v="100">¥100</button><button type="button" class="cny-chip" data-v="500">¥500</button><button type="button" class="cny-chip" data-v="1000">¥1,000</button></div>
      <div class="currency-meta" id="currency-meta">กำลังโหลดเรทล่าสุด...</div>
    </div>
  </section>

  <section class="sec" id="prep" aria-labelledby="pk-h">
    <div class="sec-h"><h2 id="pk-h">🎒 สิ่งที่ต้องเตรียม</h2><span class="sec-note" id="pack-count">0/{len(BOOK) + len(PACK)}</span></div>
    <div class="card">
      <div class="pack-bar"><i id="pack-bar-fill"></i></div>
      <h3 class="pack-h">จองก่อนไป</h3>
      <ul class="pack">{book_rows}</ul>
      <h3 class="pack-h">ของที่ต้องพก</h3>
      <ul class="pack">{pack_rows}</ul>
    </div>
    <div class="card offmap" id="offmap" data-tiles="{E(json.dumps(ALL_TILES))}">
      <div class="om-h"><span class="om-i" aria-hidden="true">🗺️</span><div><b>แผนที่ออฟไลน์</b><span id="om-status">กดครั้งเดียว เก็บทั้งแผนที่รายวัน แผนที่ทัวร์ เส้นทาง และรูป ไว้ในเครื่อง เปิดได้แม้ไม่มีเน็ตหรือไม่ได้เปิด VPN</span></div></div>
      <div class="om-bar" aria-hidden="true"><i id="om-fill"></i></div>
      <button type="button" class="btn" id="om-btn">💾 เก็บแผนที่ทั้งหมดไว้ใช้ออฟไลน์</button>
      <small class="om-note">ทำตอนอยู่ไทยและต่อ Wi-Fi · ใช้เน็ตราว 20–40 MB · แผนที่ © OpenStreetMap contributors</small>
    </div>
  </section>

  <section class="sec" id="sos" aria-labelledby="sos-h">
    <div class="sec-h"><h2 id="sos-h">🆘 ช่วยเหลือในจีน</h2></div>
    <details class="drop t-taxi" open><summary class="sub-h">🚕 ยื่นให้คนขับ <small>ที่พัก / สนามบิน</small></summary>
    <div class="taxis">
    <div class="taxi" id="taxi">
      <div class="tx-en">🏨 ที่พัก · 请带我去</div>
      <div class="tx-zh">上海市徐汇区<br>淮海中路1329号<br>云海大厦<br><span>海玥名庭酒店</span></div>
      <div class="tx-en">Atour X Hotel · 1329 Huaihai Middle Rd · ใกล้ MRT Changshu Road</div>
      <button type="button" class="btn" data-say="请带我去上海市徐汇区淮海中路1329号，云海大厦，海玥名庭酒店">🔊 พูดจีน</button>
    </div>
    <div class="taxi alt" id="taxi-pvg">
      <div class="tx-en">✈️ สนามบินขากลับ · 请带我去</div>
      <div class="tx-zh">浦东国际机场<br>2号航站楼</div>
      <div class="tx-en">Pudong Airport T2 · 9C7283 ออก 12:05</div>
      <button type="button" class="btn" data-say="请带我去浦东国际机场2号航站楼">🔊 พูดจีน</button>
    </div>
    </div>
    <p class="hint tx-hint">แตะที่อยู่เพื่อขยายเต็มจอให้คนขับดู</p>
    </details>
    <details class="drop t-pane" id="pane-card"><summary class="sub-h">👟 ยื่นให้พนักงานร้าน Pane <small>เลือกไซซ์ · กดเพื่อฟังเสียง</small></summary>
    <div class="pane-card">
      <div class="pn-sel">
        <label>ไซซ์ <select id="pn-size" aria-label="ไซซ์รองเท้า">{pane_size_opts}</select></label>
        <label>มารับ <select id="pn-day" aria-label="วันที่จะมารับ">{pane_day_opts}</select></label>
      </div>
      <div class="tx-en">请给店员看 · ยื่นให้พนักงานดู</div>
      <div class="phrases">{pane_rows}</div>
    </div>
    </details>
    <details class="drop t-queue" id="queue-card"><summary class="sub-h">🎫 วิธีกดรับบัตรคิวร้านดัง <small>Dianping / หน้าร้าน</small></summary>
    <div class="queue-card">
      <ol class="q-steps">
        <li><b>ก่อนออกจากที่พัก</b> เปิดแอป <b>大众点评 Dianping</b> (หรือ <b>美团 Meituan</b>) ล็อกอินด้วย WeChat หรือ Alipay จะง่ายกว่าเบอร์ไทย ซึ่งบางครั้งไม่ได้รับ SMS</li>
        <li>ค้นชื่อร้านภาษาจีนตามรายการด้านล่าง เลือกสาขาให้ถูก แล้วหาปุ่ม <b>排队 / 取号</b> (ต่อคิว / รับบัตรคิว) ถ้ามีจะเห็นจำนวนคิวและเวลารอโดยประมาณ</li>
        <li>เลือกจำนวนคน <b>2位</b> (โต๊ะเล็กมักเป็นคิวกลุ่ม A / 小桌) แล้วกดรับคิว ทุกร้านไม่ได้เปิดคิวออนไลน์ และบางร้านเปิดให้กดเฉพาะตอนอยู่ใกล้ร้าน</li>
        <li>เปิดการแจ้งเตือนของแอปไว้ ไปถึงร้านก่อนเลขคิวถึงสักหน่อย ถ้าเลยคิว (过号) ส่วนใหญ่ต้องกดคิวใหม่</li>
        <li><b>ถ้ากดในแอปไม่ได้</b> ไปที่หน้าร้าน มักมีตู้กดบัตรคิวหรือ QR ให้สแกนด้วย WeChat หรือยื่นประโยคด้านล่างให้พนักงานดู</li>
      </ol>
      <ul class="q-shops">{queue_shops}</ul>
      <div class="tx-en">ยื่นให้พนักงาน · 请给店员看</div>
      <div class="phrases">{queue_rows}</div>
      <p class="hint">ทดลองเปิดแอปและล็อกอินตั้งแต่อยู่ไทย จะได้ไม่ติดตอนหน้าร้าน</p>
    </div>
    </details>
    <details class="drop t-tr" id="tr-drop"><summary class="sub-h" id="tr-h">🗣️ ล่ามแปล ไทย ⇄ จีน <small>กดไมค์แล้วพูด</small></summary>
    <div class="card tr" id="tr">
      <div class="tr-mics">
        <button type="button" class="tr-mic th" data-lang="th"><i aria-hidden="true">🎙️</i><b>พูดไทย</b><small>แปลเป็นจีนให้พนักงาน</small></button>
        <button type="button" class="tr-mic zh" data-lang="zh"><i aria-hidden="true">🎙️</i><b>说中文</b><small>ให้พนักงานพูด แปลเป็นไทย</small></button>
      </div>
      <div class="tr-status" id="tr-status" aria-live="polite"></div>
      <form class="tr-form" id="tr-form">
        <button type="button" class="tr-dir" id="tr-dir" aria-label="สลับทิศทางการแปล">ไทย → 中文</button>
        <textarea id="tr-in" rows="2" placeholder="หรือพิมพ์ตรงนี้ (กดไมค์บนคีย์บอร์ดก็ได้)" enterkeyhint="send"></textarea>
        <button type="submit" class="btn tr-go">แปล</button>
      </form>
      <div class="tr-log" id="tr-log"></div>
      <div class="tr-foot"><small id="tr-eng">ต้องต่ออินเทอร์เน็ต · ถ้าไม่มีเน็ตใช้ประโยคสำเร็จรูปด้านล่าง</small><button type="button" class="tr-clear" id="tr-clear" hidden>ล้างประวัติ</button></div>
    </div>
    </details>
    <details class="drop t-phr"><summary class="sub-h">💬 ประโยคที่ใช้บ่อย <small>กดเพื่อฟังเสียง</small></summary>
    <div class="phrases">{phr_rows}</div>
    </details>
    <details class="drop t-sos"><summary class="sub-h">📞 เบอร์ฉุกเฉิน <small>แตะเพื่อโทร</small></summary>
    <div class="sos-grid">{sos_rows}</div>
    <p class="hint">แนะนำแคปหน้านี้เก็บไว้ เผื่อไม่มีเน็ต</p>
    </details>
    <details class="drop t-tip"><summary class="sub-h">💡 เคล็ดลับเที่ยวเซี่ยงไฮ้ 2026</summary>
    <div class="tips">{tips_rows}</div>
    </details>
  </section>

  <footer class="foot">🎄 Merry Christmas & Happy Shanghai Trip 🦌
    <small class="ver">อัปเดตล่าสุด {BUILD_TH}</small>
    <small>ภาพสถานที่จาก Wikimedia Commons ตามสัญญาอนุญาต Creative Commons · ภาพหัวเว็บ: {E(_CRED["hero"][5])} · <a href="{E(commons_page(_CRED["hero"][3]))}" target="_blank" rel="noopener">{E(_CRED["hero"][4])}</a> · แผนที่ © OpenStreetMap contributors</small></footer>
</main>
{PRINTDOC}
<div id="pstprint" aria-hidden="true"></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>

<nav class="bnav" aria-label="เมนูหลัก">
  <a href="#plan" data-sec="plan"><i aria-hidden="true">🗓️</i>แผน</a>
  <a href="#flights" data-sec="flights"><i aria-hidden="true">✈️</i>ตั๋ว</a>
  <a href="#budget" data-sec="budget"><i aria-hidden="true">💰</i>งบ</a>
  <a href="#prep" data-sec="prep"><i aria-hidden="true">🎒</i>เตรียมของ</a>
  <a href="#sos" data-sec="sos"><i aria-hidden="true">🆘</i>ช่วยเหลือ</a>
</nav>

<div class="tr-big" id="tr-big" role="dialog" aria-label="ข้อความภาษาจีนสำหรับยื่นให้พนักงานดู" hidden>
  <div class="tb-top"><span>请看 · ยื่นให้พนักงานดู</span><button type="button" class="tb-x" id="tb-x" aria-label="ปิด">&times;</button></div>
  <div class="tb-zh" id="tb-zh" lang="zh-CN"></div><div class="tb-py" id="tb-py"></div><div class="tb-th" id="tb-th"></div>
  <div class="tb-acts"><button type="button" class="btn" id="tb-say">🔊 播放 ฟังอีกครั้ง</button><button type="button" class="btn alt" id="tb-reply">🎙️ 请用中文回答 ให้พนักงานตอบ</button></div>
</div>
<div class="pst" id="pst" role="dialog" aria-label="ภาพสรุปแผนเที่ยว" hidden>
  <div class="pst-bar"><b>🖨️ แพลนเที่ยว + ปริ้น</b><button type="button" class="pst-x" id="pst-x" aria-label="ปิด">&times;</button></div>
  <div class="pst-lang" role="radiogroup" aria-label="ภาษาในภาพ"><button type="button" class="on" data-lang="th" role="radio" aria-checked="true">ไทย</button><button type="button" data-lang="zh" role="radio" aria-checked="false">中文 ชื่อจีน</button></div>
  <div class="pst-acts"><button type="button" class="btn" id="pst-save" disabled hidden>💾 บันทึกทั้งหมด</button><button type="button" class="btn ghost" id="pst-pimg" disabled>🖼️ พิมพ์ภาพ A4</button><button type="button" class="btn ghost" id="pst-print">🖨️ พิมพ์เป็นเอกสาร</button></div>
  <p class="pst-tip">🖨️ ตอนพิมพ์ใน Chrome: เปิด <b>"กราฟิกพื้นหลัง"</b> ในหัวข้อ <b>"การตั้งค่าเพิ่มเติม"</b> ไว้ด้วย ไม่งั้นสีพื้นหลังจะหาย</p>
  <p class="pst-st" id="pst-st"></p>
  <div class="pst-grid" id="pst-grid"></div>
  <div class="pv" id="pv" role="dialog" aria-label="ดูภาพขยาย" hidden>
    <div class="pv-bar"><button type="button" id="pv-prev" aria-label="ภาพก่อนหน้า">‹</button><span id="pv-n"></span><button type="button" id="pv-next" aria-label="ภาพถัดไป">›</button><button type="button" class="pv-sh" id="pv-sh" aria-label="แชร์ภาพนี้" hidden>📤</button><button type="button" class="pv-sh" id="pv-dl" aria-label="บันทึกภาพนี้ลงเครื่อง" hidden>💾</button><button type="button" class="pv-x" id="pv-x" aria-label="ปิด">&times;</button></div>
    <div class="pv-sc" id="pv-sc"><img id="pv-img" alt=""></div>
  </div>
</div>
<div class="fly-sheet" id="fly-sheet" role="dialog" aria-label="ติดตามเที่ยวบินบน iPhone" hidden>
  <div class="fs-card">
    <div class="fs-top"><b>📱 ติดตามเที่ยวบินบน iPhone</b><button type="button" class="fs-x" id="fs-x" aria-label="ปิด">&times;</button></div>
    <p class="fs-ok" id="fs-ok"></p>
    <ol>
      <li>กด <b>เปิดแอปโน้ต</b> ด้านล่าง แล้วสร้างโน้ตใหม่</li>
      <li>แตะค้างในโน้ต เลือก <b>วาง (Paste)</b></li>
      <li>เลขเที่ยวบินจะมี<b>เส้นใต้</b> แตะที่เลขนั้น แล้วเลือก <b>แสดงตัวอย่างเที่ยวบิน (Preview Flight)</b></li>
      <li>จะเห็นเวลาออก-ถึง อาคาร ประตูขึ้นเครื่อง จุดรับกระเป๋า และแผนที่เส้นทางบิน แบบเรียลไทม์</li>
    </ol>
    <p class="fs-n">ถ้าไม่มีเส้นใต้ ลองพิมพ์ใหม่เป็น <b class="mono" id="fs-alt"></b> · ใช้ในแอปข้อความ (iMessage) ได้เหมือนกัน · ข้อมูลจะขึ้นก่อนวันบินไม่กี่วัน</p>
    <div class="fs-acts"><a class="btn" id="fs-notes" href="mobilenotes://">📝 เปิดแอปโน้ต</a><button type="button" class="btn ghost" id="fs-copy">📋 คัดลอกอีกครั้ง</button></div>
  </div>
</div>
<div class="lightbox-overlay" id="lightbox-overlay"><span class="lightbox-close" id="lightbox-close" aria-label="ปิด">&times;</span><img id="lightbox-img" src="" alt=""></div>
<div class="qr-modal-overlay" id="qr-modal-overlay"></div>
<div class="qr-modal" id="qr-modal" role="dialog" aria-label="QR Code">
  <button type="button" class="qr-modal-close" id="qr-modal-close" aria-label="ปิด">&times;</button>
  <div class="qr-modal-title">📱 สแกนเปิดแผนทริปนี้</div>
  <div class="qr-modal-sub">ให้เพื่อนร่วมทริปสแกนเพื่อเปิดหน้านี้</div>
  <img class="qr-modal-img" id="qr-modal-img" src="" alt="QR Code">
  <div class="qr-modal-url" id="qr-modal-url"></div>
  <button type="button" class="btn" id="qr-copy-btn">🔗 คัดลอกลิงก์</button>
</div>

<script>
{JS}
</script>
</body>
</html>
'''
open(OUT, "w", encoding="utf-8").write(page)
print("written", len(page))

# ---------- tour.html: animated day-by-day map, data taken from the plan above ----------
# tour: the emoji that pops over the two heads at each stop, and the night effects
EMOJI_KW = [("พลุ", "🎆"), ("Castle", "🏰"), ("Zootopia", "🦊"), ("Adventure", "🧗"), ("Treasure", "🏴‍☠️"), ("拙政园", "🌿"),
            ("ฮั่นฝู", "👘"), ("Shantang", "🛶"), ("บะหมี่", "🍜"), ("Xiao Long", "🥟"), ("Bagel", "🥯"), ("Luneurs", "🍦"), ("Butterful", "🥐"),
            ("MARZO", "🧸"), ("Pane", "👟"), ("Coffee", "☕"), ("Shashlik", "🍢"), ("Sukiyaki", "🍲"), ("Cocina", "🥘"), ("Chef Fei", "🌶️"),
            ("คริสต์มาส", "🎄"), ("Lujiazui", "🌃"), ("Jing'an", "🛕"), ("Xintiandi", "🏮"), ("Dream Center", "🎡"), ("Bund", "📸"), ("Wukang", "📸"),
            ("รถไฟ", "🚄"), ("Maglev", "🚄"), ("Grandma", "🥢"), ("Canton", "🥢"), ("Dongsheng", "🍣"), ("มื้อเย็น", "🍽️")]
EMOJI_KIND = {"food": "🍽️", "shop": "🛍️", "see": "📸", "stay": "🏨", "fly": "✈️", "go": "🚶"}
def stop_emoji(e):
    for k, v in EMOJI_KW:
        if k in e["title"]: return v
    return EMOJI_KIND.get(e["kind"], "✨")
def stop_fx(n, e):
    if "พลุ" in e["title"]: return "fw"
    if (n, e["t"]) in ((2, "19:00"), (7, "17:30"), (7, "20:00")): return "beam"
    return ""

def _tour():
    import json as _j, re as _r
    tpl = open(_osroot.path.join(_ROOT, "src", "tour_template.html"), encoding="utf-8").read()
    def clean(t):
        t = _r.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]", "", t).strip()
        return t if len(t) <= 48 else t[:46].rstrip() + "…"
    def img(e):
        return f"img/hd/{e['hd']}-640.webp" if e.get("hd") else (f"img/{e['img']}.jpg" if e.get("img") else None)
    def cover(n):
        k = DAY_COVER.get(n)
        return f"img/hd/{k}-1280.webp" if k else None
    D = [{"ov": 1, "cover": "img/hd/hero-960.webp"}]
    for d in DAYS:
        n = d["n"]; dd = int(d["iso"].split("-")[2])
        tp = _r.sub(r"^\D*", "", d.get("wx", "")).strip()
        base = {"d": f"วันที่ {n} · {d['dow']} {dd} ธ.ค.", "tp": tp, "h": d["title"], "zh": ZH_DAY.get(n, ""), "cover": cover(n), "iso": d["iso"]}
        evs = d["events"]
        R = day_route(d); pins, idx, suzhou, route, segs = R["pins"], R["idx"], R["suzhou"], R["route"], R["segs"]
        items = [{"t": e["t"], "title": clean(e["title"]), "img": img(e), "pin": idx.get(e["t"]), "hotel": e["kind"] == "stay", "em": stop_emoji(e), "fx": stop_fx(n, e)} for e in evs]
        if not pins or n == len(DAYS):
            D.append(dict(base, asia=1, it=items)); continue
        D.append(dict(base, pins=pins, route=route, it=items, suzhou=suzhou, segs=segs))
    html = (tpl.replace("__TOUR_DATA__", _j.dumps(D, ensure_ascii=False))
               .replace("__HOTEL_LON__", str(HOTEL_LL[1])).replace("__HOTEL_LAT__", str(HOTEL_LL[0]))
               .replace("__TOTAL__", f"{TOTAL:,}").replace("__OSM_TILES__", _j.dumps(ALL_TILES)))
    out = _osroot.path.join(_osroot.path.dirname(OUT), "tour.html")
    open(out, "w", encoding="utf-8").write(html)
    print("written tour.html", len(html))

_tour()


def _present():
    """present.html: a web slideshow with a morphing day wheel (styled after the user's morph deck)."""
    import json as _j, re as _r
    tpl = open(_osroot.path.join(_ROOT, "src", "present_template.html"), encoding="utf-8").read()
    COL = ["#E76F51", "#F4A261", "#E9C46A", "#2A9D8F", "#264653", "#8E5572", "#D1495B", "#3D5A80"]
    SHORT = {1: ["บินไป", "เซี่ยงไฮ้"], 2: ["เที่ยวเบาๆ", "+ The Bund"], 3: ["Shanghai", "Disneyland"], 4: ["Wukang", "+ Jing'an"],
             5: ["West Bund", "+ Xintiandi"], 6: ["ซูโจว", "+ ฮั่นฝู"], 7: ["The Bund", "+ Lujiazui"], 8: ["เดินทาง", "กลับ"]}
    FULL = {"ส.": "เสาร์", "อา.": "อาทิตย์", "จ.": "จันทร์", "อ.": "อังคาร", "พ.": "พุธ", "พฤ.": "พฤหัสบดี", "ศ.": "ศุกร์"}
    def clean(t):
        t = _r.sub(r"[\U0001F300-\U0001FAFF☀-➿️]", "", t).strip()
        return t if len(t) <= 52 else t[:50].rstrip() + "…"
    def img(e):
        return f"img/hd/{e['hd']}-640.webp" if e.get("hd") else (f"img/{e['img']}.jpg" if e.get("img") else None)
    days = []
    for d in DAYS:
        n = d["n"]; dd = int(d["iso"].split("-")[2])
        tp = _r.sub(r"^\D*", "", d.get("wx", "")).strip()
        dow = FULL.get(d["dow"], d["dow"])
        k = DAY_COVER.get(n, "hero")
        days.append({"n": n, "c": COL[(n - 1) % 8], "h": d["title"], "dw": f"{dow} {dd} ธ.ค.", "tp": tp, "iso": d["iso"],
                     "photo": f"img/hd/{k}-640.webp", "short": SHORT.get(n, ["", ""]), "icon": f"img/present/i{n}.png",
                     "rows": [{"t": e["t"], "title": clean(e["title"]), "img": img(e), "stay": e["kind"] == "stay"} for e in d["events"]]})
    cr = []
    try:
        for row in _j.load(open(_osroot.path.join(_osroot.path.dirname(OUT), "img", "hd", "credits.json"), encoding="utf-8")):
            if row[4]:
                cr.append(f"{_r.sub(r'\s*\(วันที่[^)]*\)', '', row[2])} — {row[5]} ({row[4]})")
    except Exception as ex:
        print("credits skipped:", ex)
    html = tpl.replace("__DATA__", _j.dumps({"days": days, "credits": cr, "total": f"{TOTAL:,}"}, ensure_ascii=False))
    out = _osroot.path.join(_osroot.path.dirname(OUT), "present.html")
    open(out, "w", encoding="utf-8").write(html)
    print("written present.html", len(html))

_present()
