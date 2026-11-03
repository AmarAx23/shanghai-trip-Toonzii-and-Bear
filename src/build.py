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

def amap(kw):
    return f"https://uri.amap.com/search?keyword={quote(kw)}&city={quote('上海')}&src=shanghaitrip&callnative=1"

def gmap(q):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(q)

def L(apple_q=None, amap_kw=None, extra=None):
    out = []
    if apple_q: out.append(("🍎 Apple Maps", apple(apple_q)))
    if amap_kw: out.append(("🧭 Amap 高德", amap(amap_kw)))
    if extra: out += extra
    return out

TAXI_HOTEL = ("🚕 การ์ดให้คนขับ", "#taxi")

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
      L("Shanghai Pudong International Airport Terminal 2", "浦东国际机场2号航站楼", [TAXI_HOTEL]), tag="อาคาร 2"),
   ev("23:45", "stay", "เช็คอิน Atour X Hotel",
      'ชั้น 1 และ 6–11 อาคาร Yunhai, 1329 Huaihai Middle Road เขต Xuhui · เดิน ~160 ม. ถึง MRT Changshu Road (สาย 1, 7) · โทร <a href="tel:+8615002128856">+86 150 0212 8856</a>, <a href="tel:+862133561052">+86 21 3356 1052</a>',
      None, L(HOTEL_Q, "淮海中路1329号", [TAXI_HOTEL]), tag="ที่พัก", html_note=True),
  ], note="เครื่องลงค่ำ ถึงที่พักราว 23:45 (เช็คอินได้ตั้งแต่ 14:00 มาดึกได้) พักให้เต็มที่ พรุ่งนี้เริ่มสายได้"),

 dict(n=2, iso="2026-12-06", dow="อา.", date="อาทิตย์ 6 ธ.ค.", title="เที่ยวเบา ๆ + The Bund", icon="🌉", wx="⛅ 5–10°C",
  events=[
   ev("11:00", "go", "ออกจากที่พัก ไป People's Square", "รถไฟฟ้าสาย 1 จาก Changshu Road ไป People's Square ~15 นาที หรือเรียก Didi",
      None, [("🧭 เส้นทางจากที่พัก", apple_dir("People's Square, Shanghai"))]),
   ev("11:30", "food", "Lai Lai Xiao Long Bao (莱莱小笼)", "เสี่ยวหลงเปาไข่ปู Michelin Bib Gourmand · 506 Tianjin Road ใกล้ People's Square · วันอาทิตย์คิวยาว มาก่อนเที่ยงดีกว่า · ถ้าสาขานี้ปิด มีสาขา Jing'an ที่ 1726 Beijing West Road ใกล้ที่พัก (เปิด 8:00–14:00, 15:00–20:00)",
      "lailai", L("Lai Lai Xiao Long Bao, 506 Tianjin Road, Shanghai", "莱莱小笼 天津路"), tag="มื้อกลางวัน"),
   ev("13:30", "see", "People's Square", "เดินเล่นในสวน ถ่ายรูป แล้วเดินต่อไปพิพิธภัณฑ์ซึ่งอยู่ในจัตุรัสเดียวกัน", None, L("People's Square, Shanghai", "人民广场")),
   ev("14:30", "see", "Shanghai Museum (上海博物馆)", "พิพิธภัณฑ์ศิลปะจีนโบราณ ทองสัมฤทธิ์ เซรามิก ภาพวาด · อยู่ในตึก หลบหนาวได้ · เปิด 9:00–17:00 เข้าได้ถึง 16:00 · ไม่ต้องจองล่วงหน้า (ยกเว้นนิทรรศการพิเศษ) · พกพาสปอร์ต · ปิดวันจันทร์ · ดูประมาณ 2 ชม. (เข้าได้ถึง 16:00) แล้วเดินไป Nanjing Road", "peoples-square", L("Shanghai Museum, People's Square, Shanghai", "上海博物馆 人民广场")),
   ev("16:30", "shop", "Nanjing Road Pedestrian Street", "ถนนช้อปปิ้งหลัก ไฟคริสต์มาสตามห้าง · เดินต่อไป The Bund ได้เลย", "nanjing-road", L("Nanjing Road Pedestrian Street, Shanghai", "南京路步行街")),
   ev("17:30", "food", "Rei Flower Coffee Bar (汭REi·FLOWER COFFEE BAR)", "คาเฟ่ริมคลอง Suzhou Creek ย่าน North Bund · พักขาก่อนชม The Bund · ลองลาเต้ดอกหอมหมื่นลี้ (桂花拿铁) ไอศกรีมมะพร้าว · ~¥55/คน · 234 North Suzhou Road (北苏州路234号) ใกล้สถานี Tiantong Road ทางออก 3 · จากปลาย Nanjing Road เดินข้ามสะพาน Waibaidu Bridge ไม่กี่นาที · ยังไม่ได้ยืนยันเวลาปิด เช็กใน Amap/Dianping ก่อน", None, L("Rei Flower Coffee Bar, 234 North Suzhou Road, Shanghai", "汭REi FLOWER COFFEE BAR 北苏州路234号"), tag="คาเฟ่"),
   ev("18:30", "see", "The Bund ชมวิวแม่น้ำหวงผู่", "ตึกฝั่ง Lujiazui เปิดไฟยามค่ำ ธันวาคมมีไฟประดับสวยเป็นพิเศษ · ฟรี · คืนวันอาทิตย์คนแน่น ระวังกระเป๋า", "bund", L("The Bund, Shanghai", "外滩")),
  ], note="ธันวาคมเซี่ยงไฮ้หนาว 4–11°C กลางคืนอาจต่ำกว่านั้น ใส่โค้ท ผ้าพันคอ และถุงมือ"),

 dict(n=3, iso="2026-12-07", dow="จ.", date="จันทร์ 7 ธ.ค.", title="Wukang Road + West Bund + Lujiazui", icon="🌳", wx="☁️ 4–8°C",
  events=[
   ev("11:00", "food", "Grandma's Home (奶奶家) สาขา Wukang Road", "ร้านอาหารเซี่ยงไฮ้ชื่อดัง", "grandmas-home", L("Grandma's Home Wukang Road, Shanghai", "奶奶家 武康路"), tag="มื้อกลางวัน"),
   ev("12:30", "see", "เดินเล่น Wukang Road", "ตึก Wukang Mansion (武康大楼) ตึกยุโรปเก่า ถนนต้นไม้ร่มรื่น คาเฟ่ถ่ายรูปสวย", "wukang-road", L("Wukang Mansion, Shanghai", "武康大楼")),
   ev("14:30", "see", "Gate M West Bund Dream Center (西岸梦中心)", "โรงงานปูนซีเมนต์เก่าริมแม่น้ำหวงผู่ ปรับเป็นย่านคาเฟ่ ร้านอาหาร ร้านค้า ตึกอินดัสเทรียลถ่ายรูปสวย · ทางเดินริมน้ำ 800 ม. · ดูพระอาทิตย์ตกริมน้ำราว 16:50 · 2266 Longteng Avenue · Didi จาก Wukang Road ~15 นาที หรือรถไฟฟ้าสาย 11 สถานี Longyao Road · ฤดูหนาวที่แล้วมีลานสเก็ตน้ำแข็งริมแม่น้ำ (ปีนี้ยังไม่ยืนยัน) · 17:45 เรียก Didi ไป Lujiazui ~25 นาที", None, L("Gate M West Bund Dream Center, 2266 Longteng Avenue, Shanghai", "西岸梦中心")),
   ev("18:30", "food", "Chef Fei (费大厨)", "ร้านพริกผัดหมูชื่อดัง (辣椒炒肉) รสจัดจ้านสไตล์หูหนาน", "chef-fei", L("Chef Fei Lujiazui, Shanghai", "费大厨 陆家嘴"), tag="มื้อเย็น"),
   ev("21:00", "shop", "เดินถนน Huaihai Road แถวที่พัก", "ถนนช้อปปิ้งหน้าที่พัก ไฟประดับสวยตอนค่ำ · ไม่ไปก็ได้ถ้าเหนื่อย", "huaihai-road", L("Huaihai Middle Road, Shanghai", "淮海中路")),
  ], note="Yu Garden ปิดทุกวันจันทร์ เลยย้ายไปพรุ่งนี้ ส่วนที่เที่ยววันนี้เปิดปกติ"),

 dict(n=4, iso="2026-12-08", dow="อ.", date="อังคาร 8 ธ.ค.", title="วัดพระหยก + เมืองเก่า + Yu Garden", icon="🏮", wx="🌥️ 4–9°C",
  events=[
   ev("09:30", "see", "Jade Buddha Temple (玉佛禅寺)", "เปิด 8:00–16:30 · ไปเช้าคนน้อย · ใช้เวลาราว 1 ชม. แล้ว Didi ไป Canton 8 ~25 นาที", None, L("Jade Buddha Temple, Shanghai", "玉佛禅寺")),
   ev("11:15", "food", "Canton 8 (喜粤8号) สาขา Runan Street", "ร้านอาหารกวางตุ้ง", "canton8", L("Canton 8 Runan Street, Shanghai", "喜粤8号"), tag="มื้อกลางวัน"),
   ev("12:45", "see", "Xintiandi (新天地)", "ตรอกอิฐแดงสไตล์ Shikumen ผสมจีน-ยุโรป · คาเฟ่ ร้านบูติก", "xintiandi", L("Xintiandi, Shanghai", "新天地")),
   ev("13:45", "shop", "รองเท้า Pane ที่ TX Huaihai", "แบรนด์รองเท้าผ้าใบเซี่ยงไฮ้ · ชั้น L1 ห้าง TX Huaihai, 523 Huaihai Middle Road (淮海中路523号 TX淮海) · เดินจาก Xintiandi ได้ · เปิด 10:00–22:00 · รุ่นยอดนิยม Aria, Zephyr Training · บางไซซ์หมดบ่อย · ออกจากร้านไม่เกิน 14:45 แล้วนั่ง Didi ไป Yu Garden ~10–15 นาที (ต้องเข้าก่อน 16:00) · ถ้าไซซ์หมด วันที่ 6 ไปอีกสาขา (Yongyuan Road) และวันที่ 7 แวะร้านนี้ซ้ำได้", "pane", L("TX Huaihai, 523 Middle Huaihai Road, Shanghai", "TX淮海 淮海中路523号"), tag="ช้อป"),
   ev("15:00", "see", "Yu Garden (豫园) เข้าชมในสวน", "สวนจีนโบราณกว่า 400 ปี · เปิด 8:45–16:45 ปิดวันจันทร์ ต้องเข้าก่อนบ่าย 4 · ซื้อตั๋วหน้างานหรือในแอป", "yu-garden", L("Yu Garden, Shanghai", "豫园")),
   ev("17:00", "shop", "Yuyuan Bazaar + City God Temple (城隍庙)", "ร้านค้าและแผงขนมรอบสวน เปิดไฟสวยตอนค่ำ · ซื้อของฝาก", None, L("Shanghai City God Temple", "上海城隍庙")),
   ev("18:30", "food", "New Sukiyaki (牛New寿喜烧) ใกล้ Yu Garden", "บุฟเฟต์สุกี้ยากี้ญี่ปุ่นชื่อดัง · เนื้อหลายเกรด ซีฟู้ด น้ำซุปหลายแบบ · เริ่ม ~149 หยวน", "new-sukiyaki", L("New Sukiyaki Yu Garden, Shanghai", "牛New寿喜烧 豫园"), tag="มื้อเย็น"),
  ], note="Yu Garden ปิด 16:45 เลยเรียงให้เข้าชมในสวนตอนบ่าย แล้วค่อยเดินตลาดตอนเปิดไฟ · พรุ่งนี้ออกไป Disney 7:00 กินเสร็จรีบกลับนอน · ถ้าคิวร้าน Pane ยาวข้ามไปก่อน ยังมีวันที่ 6 และ 7"),

 dict(n=5, iso="2026-12-09", dow="พ.", date="พุธ 9 ธ.ค.", title="Shanghai Disneyland", icon="🏰", wx="☀️ 3–9°C", disney=True,
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
  ], note="วันพุธคนน้อยและตั๋วถูกกว่าเสาร์-อาทิตย์ (ประมาณ ¥499–539 ต่อคน) · ต่อแถวกลางแจ้งนาน ใส่เสื้อหนา · ปีนี้ฉลองครบ 10 ปี มีโชว์และขบวนพาเหรดพิเศษ"),

 dict(n=6, iso="2026-12-10", dow="พฤ.", date="พฤหัส 10 ธ.ค.", title="Zhujiajiao + Pane Jing'an", icon="🚤", wx="⛅ 4–10°C",
  events=[
   ev("09:45", "food", "Pushing Coffee คาเฟ่น้องหมา", "สาขาถนน Maoming Road (茂名路) ช่วงตัดกับ Huaihai Middle Road · มีน้องหมาประจำร้านหลายตัว นั่งเก้าอี้หน้าร้านเล่นกับน้องหมาได้ · เช้าวันธรรมดาคนน้อย · ให้น้องหมาเดินมาหาก่อนค่อยลูบ ไม่ใช้แฟลช · Didi จากที่พัก ~5 นาที หรือเดิน ~20 นาที · ยังไม่ได้ยืนยันเวลาเปิด ค้น \"Pushing Coffee 茂名\" ใน Amap ก่อน", "pushing", L("Pushing Coffee Maoming Road, Shanghai", "Pushing Coffee 茂名路"), tag="คาเฟ่"),
   ev("10:45", "go", "ไป Zhujiajiao", "จากคาเฟ่ · Didi ~1 ชม. หรือรถไฟฟ้าสาย 17 ลงสถานี Zhujiajiao", None,
      [("🧭 เส้นทางจากที่พัก", apple_dir("Zhujiajiao Ancient Town, Shanghai")), ("🧭 Amap 高德", amap("朱家角古镇"))]),
   ev("11:45", "see", "เดินเล่นเมืองน้ำ Zhujiajiao (朱家角)", "คลอง สะพานหิน Fangsheng Bridge (放生桥) บ้านเรือนโบราณ · นั่งเรือชมคลอง · วันธรรมดาคนน้อยกว่าเสาร์-อาทิตย์", None, L("Zhujiajiao Ancient Town, Shanghai", "朱家角古镇")),
   ev("13:00", "food", "มื้อกลางวันในเมืองน้ำ", "ร้านริมคลองมีเยอะ ลองบ๊ะจ่าง (粽子) ของขึ้นชื่อ", tag="มื้อกลางวัน"),
   ev("15:30", "go", "กลับเข้าเมือง ไป Jing'an", "เรียก Didi จาก Zhujiajiao ตรงไปถนน Yongyuan Road เขต Jing'an ~1 ชม.", None,
      [("🧭 Amap 高德", amap("PANE 永源路"))]),
   ev("16:45", "shop", "รองเท้า Pane สาขา Yongyuan Road", "แฟลกชิปสโตร์แรกของแบรนด์ ขายดีที่สุด สต๊อกคนละร้านกับ TX Huaihai · ถนน Yongyuan Road (永源路) เขต Jing'an ระหว่าง Nanjing West Road กับ Yuyuan Road · ยังไม่ได้ยืนยันเลขที่อยู่และเวลาเปิด ค้น \"PANE 永源路\" ใน Amap/Dianping ก่อนไป · จากที่พักนั่งรถไฟฟ้าสาย 7 ไป Jing'an Temple 2 สถานี", "pane", L("PANE Yongyuan Road, Jing'an, Shanghai", "PANE 永源路"), tag="ช้อป"),
   ev("18:00", "food", "มื้อเย็นแถว Jing'an / Nanjing West Road", "ย่านห้างและร้านอาหารเยอะ แล้วนั่งรถไฟฟ้าสาย 7 กลับที่พัก 2 สถานี · คืนนี้เก็บกระเป๋าบางส่วนไว้ก่อนได้", tag="มื้อเย็น"),
  ], note="ถ้าวันนี้ฝนตก สลับกับวันพรุ่งนี้ได้"),

 dict(n=7, iso="2026-12-11", dow="ศ.", date="ศุกร์ 11 ธ.ค.", title="The Bund brunch + Tianzifang + Lujiazui", icon="🙏", wx="🌤️ 5–11°C",
  events=[
   ev("10:00", "food", "Cocina 19 ร้านอาหารสเปน ริม The Bund", "มื้อสาย ร้านเปิด 10:00 · 19 Fuzhou Road หัวมุมถนน Zhongshan East 1st Road (The Bund) · ตึกวิลล่าเก่า โต๊ะริมหน้าต่างวิวหอไข่มุก มีระเบียง · เมนูเด่น paella ซีฟู้ด · จองโต๊ะริมหน้าต่างล่วงหน้าได้ · กินแล้ว Didi ไป Manner Coffee North Bund ~5–10 นาที", "cocina19", L("Cocina 19, 19 Fuzhou Road, Shanghai", "Cocina 19西班牙餐厅 外滩"), tag="มื้อสาย"),
   ev("11:30", "food", "Manner Coffee สาขา North Bund ริมแม่น้ำ", "ร้านกระจกใส 3 ด้าน ริมแม่น้ำหวงผู่ หันตรงหอไข่มุก · ท่าเรือสำราญนานาชาติ North Bund (北外滩国客中心码头) ใกล้ Dongdaming Road / Taiping Road เขต Hongkou · ข้ามคลอง Suzhou Creek จาก Cocina 19 ~5–10 นาที · ยังไม่ได้ยืนยันเวลาเปิด · แล้ว Didi ไป Tianzifang ~20 นาที", None, L("Manner Coffee North Bund International Cruise Terminal, Shanghai", "MANNER 北外滩国客中心滨江店"), tag="คาเฟ่"),
   ev("12:30", "shop", "Tianzifang (田子坊) เก็บของฝาก", "ตรอกซอกซอยร้านเล็ก ๆ ของฝาก คาเฟ่ · ใกล้ที่พัก · เดินเล่นถึงราว 15:30", None, L("Tianzifang, Shanghai", "田子坊")),
   ev("16:00", "shop", "แวะ Pane ที่ TX Huaihai (สำรอง)", "เฉพาะถ้าวันที่ 4 และ 6 ยังไม่ได้ไซซ์ที่อยากได้ · ร้านอยู่ทางผ่านจาก Tianzifang ไป Lujiazui (523 Huaihai Middle Road) · ถามพนักงานวันที่ 4 ได้ว่าของจะเข้าวันไหน · ถ้าไม่ต้องแวะ ไป Superbrand ตรงได้เลย", "pane", L("TX Huaihai, 523 Middle Huaihai Road, Shanghai", "TX淮海 淮海中路523号"), tag="ถ้ายังไม่ได้ไซซ์"),
   ev("16:30", "shop", "Superbrand Mall (正大广场)", "ห้างใหญ่ฝั่ง Lujiazui · Didi จาก Tianzifang ~20–25 นาที · ซื้อของฝากรอบสุดท้าย · ตอนค่ำออกมาดูวิว The Bund จากฝั่ง Pudong ได้ · ร้านมื้อเย็นอยู่ย่านเดียวกัน", "superbrand", L("Superbrand Mall, Shanghai", "正大广场")),
   ev("17:30", "see", "เดินถ่ายรูป Lujiazui ตอนเปิดไฟ", "สะพานลอยวงกลม Lujiazui (陆家嘴环形天桥) มุมหอไข่มุก · หน้าห้าง IFC Mall (上海国金中心) · ตึก Jin Mao (金茂大厦) คู่ Shanghai Tower ถ่ายจากถนนด้านล่าง · ทั้งหมดเดินถึงกันจาก Superbrand · พระอาทิตย์ตก ~16:50 ตอนนี้ตึกเปิดไฟแล้ว", None, L("Lujiazui Circular Pedestrian Bridge, Shanghai", "陆家嘴环形天桥"), tag="ถ่ายรูป"),
   ev("18:30", "food", "Long Time Ago Mutton Shashlik (很久以前羊肉串)", "ร้านปิ้งย่างเนื้อแกะชื่อดัง สาขา Guangyin Square (光音广场店) ถนน Yincheng Road ย่าน Lujiazui ใกล้ Superbrand · ย้ายมาจากวัน Disney เพราะโชว์จบดึก · กินเสร็จนั่ง Didi หรือรถไฟฟ้าสาย 2 กลับที่พัก", "long-time-ago", L("Long Time Ago Mutton Shashlik Guangyin Square, Shanghai", "很久以前羊肉串 光音广场"), tag="มื้อเย็น"),
   ev("20:30", "stay", "เก็บกระเป๋า", "ชั่งกระเป๋า โหลดไม่เกิน 20 กก. ถือขึ้นไม่เกิน 10 กก."),
  ], note="พรุ่งนี้ต้องเช็คเอาท์ก่อน 12:00 และออกไปสนามบินประมาณ 13:00"),

 dict(n=8, iso="2026-12-12", dow="ส.", date="เสาร์ 12 ธ.ค.", title="เดินทางกลับ", icon="✈️", wx="🌤️ 5–11°C",
  events=[
   ev("10:00", "stay", "เช็คเอาท์ Atour X Hotel", "ต้องเช็คเอาท์ก่อน 12:00 · ฝากกระเป๋าที่ล็อบบี้ได้ถ้าจะออกไปเดินเล่นก่อน"),
   ev("11:00", "food", "มื้อสายแถว Huaihai Road", "กินใกล้ที่พัก ไม่ควรไปไกล"),
   ev("13:00", "fly", "ไปสนามบินผู่ตง อาคาร 2", "Didi หรือแท็กซี่ ~1 ชม. · ถึงก่อนบิน 2–3 ชม.", None,
      [("🧭 เส้นทางจากที่พัก", apple_dir("Shanghai Pudong International Airport Terminal 2", "d")), ("🧭 Amap 高德", amap("浦东国际机场2号航站楼")), ("🚕 การ์ดให้คนขับ", "#taxi-pvg")]),
   ev("17:00", "fly", "บิน PVG → BKK · 9C7289", "บินประมาณ 4 ชม. 45 น. ถึงสุวรรณภูมิ 20:45 (เวลาไทย)"),
  ], note="ขากลับมีของฝาก ชั่งกระเป๋าก่อนออกจากที่พัก"),
]

BUDGET = [("ตั๋วเครื่องบิน Spring Airlines ไป-กลับ", 13330, "✈️"), ("ที่พัก 7 คืน Atour X Hotel", 6565, "🏨"), ("ค่าอาหาร", 5000, "🍜"),
          ("ตั๋ว Disney + คูปอง 30 หยวน", 2208, "🏰"), ("ค่าเดินทางในเมือง", 1000, "🚇"), ("ค่าเดินทางไป-กลับสนามบิน", 800, "🚕"),
          ("e-SIM", 632, "📱"), ("ประกันการเดินทาง", 325, "🛡️")]
TOTAL = sum(b[1] for b in BUDGET)
assert TOTAL == 29860

PACK = [("sim", "📱", "ซิมต่างประเทศ / eSIM จีน"), ("pay", "💳", "Alipay / WeChat Pay ผูกบัตร"), ("passport", "🛂", "Passport + สำเนา"),
        ("powerbank", "🔋", "Power Bank ≤100Wh"), ("meds", "💊", "ยาแก้แพ้ / แก้ปวด"), ("plug", "🔌", "หัวแปลงปลั๊กไฟ (Type A/I)"),
        ("coat", "🧣", "เสื้อกันหนาว + ผ้าพันคอ + ถุงมือ"), ("booking", "📄", "ปริ้น Booking ทั้งหมด"), ("vpn", "🌐", "VPN (Google/LINE ใช้ไม่ได้)"),
        ("shoes", "👟", "รองเท้าเดินสบาย (เดินเยอะ)"), ("cash", "💴", "เงินสดหยวนสำรอง"), ("lipbalm", "💧", "ลิปมัน/โลชั่นกันผิวแห้ง"),
        ("motionsick", "🤢", "ยาแก้เมารถ/เมาเครื่องบิน"), ("luggage", "⚖️", "ชั่งกระเป๋า: โหลด ≤20 กก. / ถือขึ้น ≤10 กก."), ("umbrella", "☂️", "ร่มพับ/เสื้อกันลม"),
        ("maps", "🗺️", "โหลด Amap หรือใช้ Apple Maps (Google Maps ใช้ในจีนไม่ได้)")]

SOS = [("110", "👮", "ตำรวจ", "มีสายด่วนรองรับภาษาอังกฤษ", "110"), ("120", "🚑", "รถพยาบาล", "เหตุฉุกเฉินทางการแพทย์", "120"),
       ("119", "🚒", "ดับเพลิง", "ไฟไหม้ / เหตุฉุกเฉินอื่น ๆ", "119"),
       ("+862164390630", "🌐", "สายด่วนช่วยเหลือชาวต่างชาติ", "ศูนย์บริการข้อมูลเซี่ยงไฮ้", "+86 21 6439 0630"),
       ("+862152609899", "🇹🇭", "สถานกงสุลใหญ่ไทย ณ เซี่ยงไฮ้", "ต่อ 888 · 18 ถ.หว่านซาน เขต Changning", "+86 21 5260 9899"),
       ("+862122163999", "🏥", "รพ. United Family (Changning)", "ห้องฉุกเฉิน 24 ชม. หมอพูดอังกฤษ · 699 Pingtang Rd · Didi ~20–30 นาที", "+86 21 2216 3999"),
       ("+862162483986", "🏥", "รพ. Huashan 华山医院", "ใกล้ที่พักที่สุด ~1.5 กม. · 12 Middle Wulumuqi Rd · แผนกต่างชาติพูดอังกฤษ จ.–ศ. 8:00–17:00", "+86 21 6248 3986")]

PHRASES = [("多少钱？", "duō shǎo qián", "เท่าไหร่ครับ/คะ"), ("不要辣", "bú yào là", "ไม่เอาเผ็ด"), ("少辣", "shǎo là", "เผ็ดน้อย"),
           ("洗手间在哪里？", "xǐ shǒu jiān zài nǎ lǐ", "ห้องน้ำอยู่ไหน"), ("可以用支付宝吗？", "kě yǐ yòng zhī fù bǎo ma", "จ่าย Alipay ได้ไหม"),
           ("这个", "zhè ge", "อันนี้ (ชี้ที่เมนู)"), ("买单", "mǎi dān", "เช็กบิล"), ("谢谢", "xiè xie", "ขอบคุณ")]

TIPS = [("🛂", "วีซ่า", "พาสปอร์ตไทยเข้าจีนแบบ Free Visa อยู่ได้สูงสุด 30 วัน (ไม่เกิน 90 วันใน 180 วัน) · ตั้งแต่ 1 มี.ค. 2026 ไทย-จีนยกเว้นวีซ่าให้กันแบบสองทาง มีผลถึง 31 ธ.ค. 2026 ครอบคลุมทริปนี้"),
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
 (1, "22:05"): (PVG_LL, "สนามบินผู่ตง T2"),
 (2, "11:30"): ((31.2381, 121.4726), "Lai Lai"), (2, "13:30"): ((31.2339, 121.4710), "People's Square"), (2, "14:30"): ((31.2283, 121.4703), "Shanghai Museum"),
 (2, "16:30"): ((31.2375, 121.4790), "Nanjing Road"), (2, "17:30"): ((31.2445, 121.4880), "Rei Flower"), (2, "18:30"): ((31.2400, 121.4905), "The Bund"),
 (3, "11:00"): ((31.2068, 121.4352), "Grandma's Home"), (3, "12:30"): ((31.2063, 121.4337), "Wukang Mansion"),
 (3, "14:30"): ((31.1700, 121.4632), "Gate M West Bund"), (3, "18:30"): ((31.2372, 121.5000), "Chef Fei"),
 (3, "21:00"): ((31.2163, 121.4585), "Huaihai Road"),
 (4, "09:30"): ((31.2437, 121.4398), "วัดพระหยก"), (4, "11:15"): ((31.2046, 121.4793), "Canton 8"), (4, "12:45"): ((31.2219, 121.4704), "Xintiandi"),
 (4, "13:45"): ((31.2208, 121.4710), "Pane TX Huaihai"), (4, "15:00"): ((31.2289, 121.4880), "Yu Garden"), (4, "17:00"): ((31.2280, 121.4880), "City God Temple"),
 (4, "18:30"): ((31.2272, 121.4900), "New Sukiyaki"),
 (5, "08:30"): ((31.1440, 121.6570), "Disneyland"),
 (6, "09:45"): ((31.2185, 121.4590), "Pushing Coffee"), (6, "11:45"): ((31.1136, 121.0515), "Zhujiajiao"), (6, "16:45"): ((31.2262, 121.4475), "Pane (โดยประมาณ)"), (6, "18:00"): ((31.2268, 121.4530), "มื้อเย็น Jing'an"),
 (7, "10:00"): ((31.2385, 121.4887), "Cocina 19"), 
 (7, "11:30"): ((31.2480, 121.4985), "Manner North Bund"), (7, "12:30"): ((31.2103, 121.4641), "Tianzifang"), (7, "16:30"): ((31.2387, 121.4947), "Superbrand Mall"), (7, "17:30"): ((31.2397, 121.5000), "สะพานลอยวงกลม"), (7, "18:30"): ((31.2370, 121.5010), "Long Time Ago"),
 (8, "13:00"): (PVG_LL, "สนามบินผู่ตง T2"),
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
    pts = [dict(hotel, label="ที่พัก 亚朵X酒店")] + [dict(s, label=f'{k+1} {s["zh"] or s["name"]}') for k, s in enumerate(stops)]
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
    legend = "".join(f'<button type="button" class="mleg" data-go="{s["id"]}"><b>{k+1}</b>{E(s["name"])}</button>' for k, s in enumerate(stops))
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
HD_BY_SLOT = {(2, "13:30"): "peoplespark", (2, "17:30"): "waibaidu", (3, "14:30"): "westbund", (5, "10:00"): "zootopia", (1, "16:45"): "spring", (8, "17:00"): "spring", (6, "13:00"): "zongzi", (6, "18:00"): "jingan", (7, "11:30"): "northbund", (7, "17:30"): "ljznight", (8, "11:00"): "huaihai", (8, "13:00"): "pvg", (4, "17:00"): "citygod", (6, "11:45"): "zhujiajiao", (4, "09:30"): "jade", (7, "12:30"): "tianzifang"}
for _d in DAYS:
    for _e in _d["events"]:
        _e["hd"] = HD_BY_SLOT.get((_d["n"], _e["t"])) or HD_BY_OLD.get(_e["img"] or "")
def commons_page(name):
    return "https://commons.wikimedia.org/wiki/File:" + quote(name.replace(" ", "_"))
def credit_html(key):
    r = _CRED[key]
    return (f'<small class="credit">ภาพ: {E(r[5])} · <a href="{E(commons_page(r[3]))}" target="_blank" rel="noopener">{E(r[4])}</a></small>')


# Chinese names for the summary pictures (ไทย / 中文 switch)
ZH_DAY = {1: "出发去上海", 2: "人民广场 + 外滩", 3: "武康路 + 西岸 + 陆家嘴", 4: "玉佛寺 + 老城厢 + 豫园", 5: "上海迪士尼乐园", 6: "朱家角古镇 + 静安 PANE", 7: "Cocina 19 + 田子坊 + 陆家嘴", 8: "回国"}
ZH_EV = {
 (1, "13:45"): "曼谷素万那普机场 值机", (1, "16:45"): "航班 9C7284 曼谷 → 上海浦东", (1, "22:05"): "抵达浦东国际机场 2号航站楼", (1, "23:45"): "入住 亚朵X酒店 淮海中路",
 (2, "11:00"): "从酒店出发 去人民广场", (2, "11:30"): "莱莱小笼（天津路）", (2, "13:30"): "人民广场", (2, "14:30"): "上海博物馆（人民广场）", (2, "16:30"): "南京路步行街", (2, "17:30"): "汭REi·FLOWER COFFEE BAR（北苏州路234号）", (2, "18:30"): "外滩 · 黄浦江夜景",
 (3, "11:00"): "奶奶家（武康路店）", (3, "12:30"): "武康路 · 武康大楼", (3, "14:30"): "西岸梦中心 Gate M（徐汇滨江）", (3, "18:30"): "费大厨辣椒炒肉（陆家嘴）", (3, "21:00"): "淮海中路 散步",
 (4, "09:30"): "玉佛禅寺", (4, "11:15"): "喜粤8号（汝南街店）", (4, "12:45"): "新天地", (4, "13:45"): "PANE 球鞋（TX淮海 淮海中路523号）", (4, "15:00"): "豫园", (4, "17:00"): "豫园商城 · 上海城隍庙", (4, "18:30"): "牛New寿喜烧（豫园）",
 (5, "07:00"): "从酒店出发 去上海迪士尼", (5, "08:30"): "奇幻童话城堡", (5, "10:00"): "疯狂动物城 + 明日世界", (5, "13:00"): "探险岛", (5, "15:00"): "宝藏湾",
 (5, "18:00"): "园内晚餐", (5, "21:15"): "点亮奇梦 + 烟花表演", (5, "22:00"): "回酒店",
 (6, "09:45"): "Pushing Coffee 狗狗咖啡（茂名路）", (6, "10:45"): "出发去朱家角", (6, "11:45"): "朱家角古镇 · 放生桥", (6, "13:00"): "古镇午餐 · 粽子", (6, "15:30"): "回市区 去静安", (6, "16:45"): "PANE 球鞋（永源路店）", (6, "18:00"): "静安 南京西路 晚餐",
 (7, "10:00"): "Cocina 19 西班牙餐厅（外滩 福州路19号）", (7, "11:30"): "MANNER 咖啡（北外滩国客中心滨江店）", (7, "12:30"): "田子坊 买伴手礼", (7, "16:00"): "PANE（TX淮海）备选", (7, "16:30"): "正大广场（陆家嘴）", (7, "17:30"): "陆家嘴环形天桥 · 国金中心 · 金茂大厦 拍照", (7, "18:30"): "很久以前羊肉串（光音广场店）", (7, "20:30"): "整理行李",
 (8, "10:00"): "亚朵X酒店 退房", (8, "11:00"): "淮海路 早午餐", (8, "13:00"): "去浦东国际机场 2号航站楼", (8, "17:00"): "航班 9C7289 上海浦东 → 曼谷",
}
for _d in DAYS:
    _d["zh"] = ZH_DAY.get(_d["n"], "")
    for _e in _d["events"]:
        _e["zh"] = ZH_EV.get((_d["n"], _e["t"]), "")

def event_html(e):
    tag = f' <span class="tag">{E(e["tag"])}</span>' if e["tag"] else ""
    note = e["note"] if e["html_note"] else E(e["note"])
    if e.get("hd"):
        k = e["hd"]
        img = (f'<figure class="ph"><img class="thumb" src="img/hd/{k}-640.webp" srcset="img/hd/{k}-640.webp 640w, img/hd/{k}-1280.webp 1280w" '
               f'sizes="(max-width: 640px) calc(100vw - 110px), 520px" alt="{E(e["title"])}" loading="lazy" decoding="async">{credit_html(k)}</figure>')
    else:
        img = (f'<figure class="ph"><img class="thumb" src="img/{e["img"]}.jpg" alt="{E(e["title"])}" loading="lazy" decoding="async"></figure>' if e["img"] else "")
    eid = f' id="{e["eid"]}"' if e.get("eid") else ""
    return (f'<li class="ev"{eid} data-t="{e["data_t"]}" data-kind="{e["kind"]}" data-zh="{E(e.get("zh", ""))}" style="--dot:{KIND_DOT[e["kind"]]}">'
            f'<time>{E(e["t"])}</time><span class="dot" aria-hidden="true"></span>'
            f'<div class="evb">{img}<h3>{E(e["title"])}{tag}</h3>'
            + (f'<p>{note}</p>' if note else "") + links_html(e["links"]) + '</div></li>')

DAY_COVER = {1: "spring", 2: "bund", 3: "wukang", 4: "yu", 5: "castle", 6: "zhujiajiao", 7: "ljznight", 8: "pvg"}
def day_html(d):
    disney = ' <span class="tag gold">DISNEY DAY</span>' if d.get("disney") else ""
    mp = day_geo(d)
    evs = "".join(event_html(e) for e in d["events"])
    return f'''
    <section class="day" id="day-{d["n"]}" data-day="{d["n"]}" data-date="{d["iso"]}" data-zh="{E(d.get("zh", ""))}" data-cover="img/hd/{DAY_COVER.get(d["n"], "hero")}-640.webp" aria-label="วันที่ {d["n"]}">
      <div class="dayhead">
        <div class="num">{d["n"]}</div>
        <div class="dh-txt"><h3>{E(d["title"])}{disney}</h3><p>{E(d["date"])} · <span class="wxb" data-date="{d["iso"]}">{E(d["wx"])}</span></p></div>
        <div class="dicon" aria-hidden="true">{d["icon"]}</div>
      </div>
      {mp}
      <ol class="tl">{evs}</ol>
      <div class="note"><span aria-hidden="true">⭐</span><span>{E(d["note"])}</span></div>
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
pack_rows = "".join(f'<li class="packing-item" id="pack-{k}"><label><input type="checkbox" data-key="{k}"><span class="pack-box">{CHECK_SVG}</span><span class="packing-txt">{ic} {E(t)}</span></label></li>' for k, ic, t in PACK)

sos_rows = "".join(f'<a class="sos" href="tel:{tel}"><span class="si" aria-hidden="true">{ic}</span><span><b>{E(n)}</b><small>{E(sub)}</small><em>{E(num)}</em></span></a>' for tel, ic, n, sub, num in SOS)

phr_rows = "".join(f'<button type="button" class="phr" data-say="{E(zh)}"><span><span class="zh">{E(zh)}</span><span class="th">{E(th)} · {E(py)}</span></span><span class="spk" aria-hidden="true">🔊</span></button>' for zh, py, th in PHRASES)

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
    for i, e in enumerate(d["events"]):
        tag = f' <span class="p-tag">{E(e["tag"])}</span>' if e["tag"] else ""
        note = _short(e["note"])
        src = _ev_src(e)
        pic = f'<img class="p-pic" data-psrc="{src}" alt="">' if src else f'<span class="p-pic p-emo">{KIND_EMO.get(e["kind"], "📍")}</span>'
        zh = e.get("zh", "")
        rows.append(f'<div class="p-ev {"alt" if i % 2 else ""}"><span class="p-time">{E(e["t"])}</span>{pic}<div class="p-body"><b>{E(e["title"])}</b>{tag}'
                    + (f'<div class="p-n">{E(note)}</div>' if note else "") + (f'<div class="p-zh" lang="zh-CN">{E(zh)}</div>' if zh else "") + '</div></div>')
    disney = " · DISNEY DAY" if d.get("disney") else ""
    return (f'<section class="p-day"><h3><span class="p-num">{d["n"]}</span><span class="p-dt"><small>{E(d["date"])} 2026{disney} · {E(d["wx"])}</small>{E(d["title"])}</span><span class="p-dzh" lang="zh-CN">{E(d.get("zh", ""))}</span></h3>'
            f'<div class="p-evs">{"".join(rows)}</div>'
            + (f'<p class="p-tip">⭐ {E(_plain(d["note"]))}</p>' if d.get("note") else "") + '</section>')
_pr_over = "".join(f'<tr><td class="p-t">{d["n"]}</td><td>{E(d["date"])}</td><td><b>{E(d["title"])}</b></td><td class="p-zh" lang="zh-CN">{E(d.get("zh", ""))}</td></tr>' for d in DAYS)
_pr_budget = "".join(f'<tr><td>{E(l)}</td><td class="p-r">{a:,} ฿</td></tr>' for l, a, i in BUDGET)
_pr_sos = "".join(f'<tr><td><b>{E(n)}</b><div class="p-n">{E(sub)}</div></td><td class="p-r p-mono">{E(num)}</td></tr>' for tel, ic, n, sub, num in SOS)
_pr_phr = "".join(f'<tr><td class="p-zh" lang="zh-CN">{E(zh)}</td><td class="p-n">{E(py)}</td><td>{E(th)}</td></tr>' for zh, py, th in PHRASES)
_pr_pack = "".join(f'<li>☐ {E(t)}</li>' for k, ic, t in PACK)
PRINTDOC = f"""
<div id="printdoc" aria-hidden="true">
  <header class="p-head"><img class="p-hero" data-psrc="img/hd/hero-960.webp" alt=""><div class="p-hin"><small>SHANGHAI · DECEMBER 2026 · Toonzii &amp; Bear</small><h1>แผนเที่ยวเซี่ยงไฮ้ 8 วัน 7 คืน</h1><p>เสาร์ 5 – เสาร์ 12 ธันวาคม 2026 · พิมพ์จากเว็บ อัปเดต {BUILD_TH}</p></div></header>
  <div class="p-grid">
    <div class="p-box"><h4>✈️ เที่ยวบิน Spring Airlines</h4><table class="p-tbl"><tbody>
      <tr><td><b>ขาไป</b> ส. 5 ธ.ค.</td><td class="p-mono">9C7284</td><td>BKK 16:45 → PVG 22:05</td></tr>
      <tr><td><b>ขากลับ</b> ส. 12 ธ.ค.</td><td class="p-mono">9C7289</td><td>PVG 17:00 → BKK 20:45</td></tr></tbody></table>
      <div class="p-n">กระเป๋า: ถือขึ้น 1 ชิ้น ≤10 กก. (55×40×20 ซม.) · โหลด 20 กก. · ไม่มีอาหารฟรี</div></div>
    <div class="p-box"><h4>🏨 ที่พัก 7 คืน</h4><b>Atour X Hotel · Huaihai Middle Road</b><div lang="zh-CN" class="p-zh">亚朵X酒店 · 上海市徐汇区淮海中路1329号</div>
      <div class="p-n">ใกล้ MRT Changshu Road (สาย 1, 7) · โทร +86 150 0212 8856, +86 21 3356 1052 · เช็คอิน 14:00 เช็คเอาท์ 12:00</div></div>
  </div>
  <h2>ภาพรวม 8 วัน</h2>
  <table class="p-tbl p-over"><tbody>{_pr_over}</tbody></table>
  <h2>แผนรายวัน</h2>
  {"".join(_pr_day(d) for d in DAYS)}
  <section class="p-help">
    <h2>ยื่นให้คนขับ · 请带我去</h2>
    <div class="p-grid">
      <div class="p-taxi"><small>ไปที่พัก</small><div lang="zh-CN">上海市徐汇区<br>淮海中路1329号<br>亚朵X酒店</div></div>
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
    <div class="chips"><span class="chip">🏨 Atour X Huaihai Rd</span><span class="chip">💰 {TOTAL:,} ฿/คน</span><span class="chip">🚇 Metro + Didi</span></div>
    <div class="hero-actions">
      <button type="button" class="hbtn" id="share-btn"><span aria-hidden="true">🔗</span>แชร์</button>
      <button type="button" class="hbtn" id="qr-btn"><span aria-hidden="true">📱</span>QR</button>
      <button type="button" class="hbtn" id="print-btn"><span aria-hidden="true">🖼️</span>ภาพสรุป</button>
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
        <div class="route"><div class="ap"><b>PVG</b><span>ผู่ตง อาคาร 2</span></div><div class="mid fly" data-dep="2026-12-12T17:00:00+08:00" data-arr="2026-12-12T20:45:00+07:00"><svg aria-hidden="true"><path/></svg><span class="plane" aria-hidden="true">✈️</span><span class="dur">4 ชม. 45 น.</span></div><div class="ap r"><b>BKK</b><span>สุวรรณภูมิ</span></div></div>
        <div class="times"><span>17:00</span><span>20:45</span></div>
        <div class="links"><a href="https://www.flightradar24.com/data/flights/9c7289" target="_blank" rel="noopener">🛬 FR24</a><a href="https://www.flightaware.com/live/flight/CQH7289" target="_blank" rel="noopener">🛬 FlightAware</a><button type="button" class="fly-ip" data-fly="9C7289">📱 iPhone</button></div>
      </div>
      <div class="stub"><small>FLIGHT</small><b>9C7289</b><span class="flip-hint">แตะพลิก ↻</span></div>
      </div>
      <div class="pass-back" aria-hidden="true"><div class="pbk"><span class="tag gold">9C7289 · ข้อมูลเพิ่มเติม</span><ul><li><b>🧳 กระเป๋า (ต่อคน)</b>ถือขึ้นเครื่อง 1 ชิ้น ≤ 10 กก. · 55×40×20 ซม.</li><li><b>🧳 โหลด</b>รวม 20 กก. · แต่ละชิ้นไม่เกิน 100×60×40 ซม.</li><li><b>⏰ ออกจากที่พัก</b>ประมาณ 13:00 ให้ถึงก่อนบิน 2–3 ชม.</li><li><b>🍱 บนเครื่อง</b>ไม่มีอาหารฟรี · ชั่งกระเป๋าถือเข้ม</li></ul><small>แตะเพื่อพลิกกลับ ↻</small></div></div>
    </div></div>
    <details class="card more">
      <summary>กระเป๋า เวลาออกจากที่พัก และวิธีเช็กไฟลท์</summary>
      <ul class="facts">
        <li><b>🧳 กระเป๋า (ต่อคน ทั้งไปและกลับ)</b>ถือขึ้นเครื่อง 1 ชิ้น ไม่เกิน 10 กก. ขนาดไม่เกิน 55×40×20 ซม. · โหลดรวม 20 กก. ขนาดแต่ละชิ้นไม่เกิน 100×60×40 ซม. · Spring Airlines ชั่งกระเป๋าถือค่อนข้างเข้ม และไม่มีอาหารฟรีบนเครื่อง</li>
        <li><b>⏰ ขากลับ</b>ออกจากที่พักไปสนามบินประมาณ 13:00 (นั่งรถ ~1 ชม.) ให้ถึงก่อนบิน 2–3 ชม.</li>
        <li><b>📱 เช็กไฟลท์บน iPhone</b>เปิดแอป Notes หรือ iMessage พิมพ์ <b class="mono">Fly 9C7284</b> หรือ <b class="mono">Fly 9C7289</b> แล้วกดค้างที่รหัสที่มีเส้นใต้ เลือก Preview Flight</li>
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
    <div class="sec-h"><h2 id="pk-h">🎒 สิ่งที่ต้องเตรียม</h2><span class="sec-note" id="pack-count">0/{len(PACK)}</span></div>
    <div class="card">
      <div class="pack-bar"><i id="pack-bar-fill"></i></div>
      <ul class="pack">{pack_rows}</ul>
    </div>
    <div class="card offmap" id="offmap" data-tiles="{E(json.dumps(ALL_TILES))}">
      <div class="om-h"><span class="om-i" aria-hidden="true">🗺️</span><div><b>แผนที่ออฟไลน์</b><span id="om-status">เก็บแผนที่ของทั้ง 8 วันไว้ในเครื่อง เปิดได้แม้ไม่มีเน็ตหรือไม่ได้เปิด VPN</span></div></div>
      <div class="om-bar" aria-hidden="true"><i id="om-fill"></i></div>
      <button type="button" class="btn" id="om-btn">💾 เก็บแผนที่ไว้ใช้ออฟไลน์</button>
      <small class="om-note">ทำตอนอยู่ไทยและต่อ Wi-Fi · ใช้เน็ตประมาณ 3 MB · แผนที่ © OpenStreetMap contributors</small>
    </div>
  </section>

  <section class="sec" id="sos" aria-labelledby="sos-h">
    <div class="sec-h"><h2 id="sos-h">🆘 ช่วยเหลือในจีน</h2></div>
    <div class="taxi" id="taxi">
      <div class="tx-en">请带我去 · ยื่นให้คนขับดู</div>
      <div class="tx-zh">上海市徐汇区<br>淮海中路1329号<br><span>亚朵X酒店</span></div>
      <div class="tx-en">Atour X Hotel · 1329 Huaihai Middle Road · เทียบกับที่อยู่ภาษาจีนในใบจองอีกครั้ง</div>
      <button type="button" class="btn" data-say="请带我去上海市徐汇区淮海中路1329号，亚朵X酒店">🔊 ให้เว็บพูดภาษาจีน</button>
    </div>
    <div class="taxi alt" id="taxi-pvg">
      <div class="tx-en">请带我去 · ขากลับไปสนามบิน</div>
      <div class="tx-zh">浦东国际机场<br>2号航站楼</div>
      <div class="tx-en">Pudong Airport Terminal 2 · เที่ยวบิน 9C7289 ออก 17:00</div>
      <button type="button" class="btn" data-say="请带我去浦东国际机场2号航站楼">🔊 ให้เว็บพูดภาษาจีน</button>
    </div>
    <h3 class="sub-h" id="tr-h">🗣️ ล่ามแปล ไทย ⇄ จีน <small>กดไมค์แล้วพูด</small></h3>
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
    <h3 class="sub-h">ประโยคที่ใช้บ่อย <small>กดเพื่อฟังเสียง</small></h3>
    <div class="phrases">{phr_rows}</div>
    <h3 class="sub-h">เบอร์ฉุกเฉิน <small>แตะเพื่อโทร</small></h3>
    <div class="sos-grid">{sos_rows}</div>
    <p class="hint">แนะนำแคปหน้านี้เก็บไว้ เผื่อไม่มีเน็ต</p>
    <h3 class="sub-h">เคล็ดลับเที่ยวเซี่ยงไฮ้ 2026</h3>
    <div class="tips">{tips_rows}</div>
  </section>

  <footer class="foot">🎄 Merry Christmas & Happy Shanghai Trip 🦌
    <small class="ver">อัปเดตล่าสุด {BUILD_TH}</small>
    <small>ภาพสถานที่จาก Wikimedia Commons ตามสัญญาอนุญาต Creative Commons · ภาพหัวเว็บ: {E(_CRED["hero"][5])} · <a href="{E(commons_page(_CRED["hero"][3]))}" target="_blank" rel="noopener">{E(_CRED["hero"][4])}</a> · แผนที่ © OpenStreetMap contributors</small></footer>
</main>
{PRINTDOC}
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
  <div class="pst-bar"><b>🖼️ ภาพสรุปทริป</b><button type="button" class="pst-x" id="pst-x" aria-label="ปิด">&times;</button></div>
  <div class="pst-lang" role="radiogroup" aria-label="ภาษาในภาพ"><button type="button" class="on" data-lang="th" role="radio" aria-checked="true">ไทย</button><button type="button" data-lang="zh" role="radio" aria-checked="false">中文 ชื่อจีน</button></div>
  <div class="pst-acts"><button type="button" class="btn" id="pst-save" disabled hidden>📥 บันทึกทั้งหมด</button><button type="button" class="btn ghost" id="pst-print">🖨️ พิมพ์เป็นเอกสาร</button></div>
  <p class="pst-st" id="pst-st"></p>
  <div class="pst-grid" id="pst-grid"></div>
  <div class="pv" id="pv" role="dialog" aria-label="ดูภาพขยาย" hidden>
    <div class="pv-bar"><button type="button" id="pv-prev" aria-label="ภาพก่อนหน้า">‹</button><span id="pv-n"></span><button type="button" id="pv-next" aria-label="ภาพถัดไป">›</button><button type="button" class="pv-sh" id="pv-sh" aria-label="แชร์ภาพนี้" hidden>📤</button><button type="button" class="pv-x" id="pv-x" aria-label="ปิด">&times;</button></div>
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
