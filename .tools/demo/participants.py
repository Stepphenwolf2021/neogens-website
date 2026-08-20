#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ชุดข้อมูลจำลองของเดโม Coffee Knowledge Vault · ผู้ร่วมสร้างคลัง 5,000 ราย

ทุกตัวเลขในไฟล์นี้แต่งขึ้นเพื่อการสาธิตเท่านั้น ไม่ใช่ข้อมูลจริง
สัดส่วนที่ตกลงกันไว้
  เกษตรกร            4,000   80%
  โรงคั่ว               500   10%
  อีกหกกลุ่มรวม          500   10%
      สหกรณ์และกลุ่มเกษตรกร     150
      โรงแปรรูปและโรงล้าง        120
      ผู้ส่งออกและผู้นำเข้า         90
      ร้านกาแฟ                  70
      นักวิจัยและสถาบัน           40
      ผู้ตรวจรับรอง               30

สร้างเป็น JSON ให้หน้าเดโมฝังไว้ในไฟล์เดียว ไม่ต้องเรียก network ตอนเปิดหน้า
"""

import json
from pathlib import Path

# (ชื่อ, lon, lat, บทบาท, เกษตรกร, โรงคั่ว, สหกรณ์, โรงแปรรูป, ผู้ส่งออก, ร้านกาแฟ, วิจัย, ตรวจรับรอง,
#  คะแนนคัปปิ้งเฉลี่ย, ช่วงความสูง, โปรไฟล์รสเด่น, วิธีแปรรูปที่ใช้มากที่สุด)
ROWS = [
    # ---------------- แหล่งปลูก ----------------
    ("Brazil",            -45.9, -21.5, "origin", 620,  35, 22, 18, 12, 6, 4, 2, 83.1, "800–1,200 m",  "nut · cocoa · caramel",     "natural"),
    ("Vietnam",           108.0,  12.7, "origin", 540,   8, 14, 12,  8, 3, 2, 1, 81.4, "600–1,500 m",  "dark cocoa · spice",        "washed"),
    ("Colombia",          -75.5,   4.6, "origin", 470,  22, 20, 14,  9, 5, 3, 2, 85.2, "1,400–2,000 m","citrus · red fruit",        "washed"),
    ("Indonesia",          99.5,   2.6, "origin", 330,  12, 11,  9,  6, 3, 2, 1, 84.0, "1,100–1,600 m","herbal · earthy · cedar",   "wet-hulled"),
    ("Ethiopia",           38.7,   7.7, "origin", 420,   9, 18, 11,  7, 3, 3, 1, 90.4, "1,700–2,200 m","jasmine · bergamot · peach","natural"),
    ("Honduras",          -87.2,  14.6, "origin", 210,   5,  9,  7,  4, 2, 1, 1, 84.3, "1,200–1,700 m","brown sugar · stone fruit", "washed"),
    ("India",              75.8,  12.9, "origin", 190,   7,  7,  6,  4, 3, 2, 1, 82.6, "900–1,500 m",  "pepper · malt",             "monsooned"),
    ("Uganda",             32.6,   0.9, "origin", 175,   3,  8,  5,  3, 1, 1, 1, 83.2, "1,300–1,900 m","dried fruit · cocoa",       "natural"),
    ("Mexico",            -96.9,  16.9, "origin", 150,   8,  7,  5,  3, 3, 1, 1, 83.8, "1,000–1,600 m","almond · cane sugar",       "washed"),
    ("Guatemala",         -90.8,  14.9, "origin", 145,   6,  8,  6,  4, 2, 2, 1, 85.0, "1,300–1,900 m","apple · chocolate",         "washed"),
    ("Peru",              -75.4,  -6.5, "origin", 140,   4,  9,  6,  3, 1, 1, 1, 84.1, "1,200–1,800 m","toffee · orange",           "washed"),
    ("Nicaragua",         -86.0,  13.1, "origin",  95,   3,  5,  4,  2, 1, 1, 1, 84.4, "1,100–1,600 m","honey · citrus",            "honey"),
    ("Costa Rica",        -84.0,   9.8, "origin",  85,   6,  5,  5,  3, 2, 2, 1, 85.5, "1,200–1,800 m","tangerine · panela",        "honey"),
    ("Kenya",              37.2,  -0.5, "origin", 120,   4,  7,  5,  3, 1, 2, 1, 86.1, "1,500–2,100 m","blackcurrant · tomato",     "washed"),
    ("Tanzania",           35.0,  -6.5, "origin",  90,   2,  5,  4,  2, 1, 1, 1, 84.0, "1,300–1,900 m","plum · black tea",          "washed"),
    ("Rwanda",             29.9,  -2.0, "origin",  80,   3,  6,  4,  2, 1, 1, 1, 85.3, "1,500–2,000 m","red apple · floral",        "washed"),
    ("Burundi",            29.9,  -3.4, "origin",  55,   1,  4,  3,  2, 1, 1, 0, 84.8, "1,400–1,900 m","grapefruit · honey",        "washed"),
    ("El Salvador",       -89.2,  13.9, "origin",  70,   3,  4,  3,  2, 1, 1, 1, 84.6, "1,200–1,700 m","caramel · cherry",          "honey"),
    ("Papua New Guinea",  145.0,  -6.5, "origin",  60,   1,  4,  3,  2, 1, 1, 0, 83.5, "1,300–1,800 m","tropical fruit · cocoa",    "washed"),
    ("Thailand",           99.3,  19.6, "origin", 165,  14,  9,  6,  3, 6, 4, 1, 84.9, "1,100–1,500 m","longan · tamarind · lychee","honey"),
    ("Laos",              106.0,  15.1, "origin",  45,   1,  3,  2,  1, 1, 1, 0, 83.0, "1,000–1,400 m","cocoa · dried longan",      "natural"),
    ("Yemen",              44.2,  15.0, "origin",  35,   1,  2,  2,  1, 0, 1, 0, 90.1, "1,500–2,200 m","dried fig · incense",       "natural"),
    ("Panama",            -82.4,   8.8, "origin",  30,   3,  2,  2,  1, 1, 1, 1, 91.8, "1,400–1,900 m","jasmine · bergamot",        "washed"),
    ("Ecuador",           -79.0,  -1.5, "origin",  40,   2,  3,  2,  1, 1, 1, 0, 84.7, "1,200–1,900 m","cane sugar · pear",         "washed"),
    ("DR Congo",           28.9,  -2.5, "origin",  50,   1,  3,  2,  1, 0, 1, 0, 83.9, "1,400–1,900 m","dark cherry · cocoa",       "washed"),
    ("Rest of origins",   -60.0,  -8.0, "origin",  90,   2,  6,  4,  2, 1, 1, 1, 83.6, "900–1,800 m",  "mixed",                     "mixed"),

    # ---------------- ตลาดปลายทาง ----------------
    ("United States",     -96.0,  39.0, "market",   0, 112,  0,  0,  8, 12, 3, 2, 0.0, "",             "",                          ""),
    ("Japan",             139.7,  35.7, "market",   0,  58,  0,  0,  4,  8, 2, 1, 0.0, "",             "",                          ""),
    ("Germany",            10.4,  51.2, "market",   0,  46,  0,  0,  4,  5, 2, 1, 0.0, "",             "",                          ""),
    ("Italy",              12.5,  42.5, "market",   0,  28,  0,  0,  2,  3, 1, 0, 0.0, "",             "",                          ""),
    ("United Kingdom",     -1.5,  52.5, "market",   0,  32,  0,  0,  3,  4, 2, 1, 0.0, "",             "",                          ""),
    ("South Korea",       127.0,  37.5, "market",   0,  30,  0,  0,  2,  5, 1, 0, 0.0, "",             "",                          ""),
    ("Australia",         149.0, -33.0, "market",   0,  26,  0,  0,  2,  4, 1, 0, 0.0, "",             "",                          ""),
    ("Canada",            -79.0,  44.0, "market",   0,  22,  0,  0,  2,  3, 1, 0, 0.0, "",             "",                          ""),
    ("Nordics",            15.0,  60.0, "market",   0,  20,  0,  0,  2,  3, 1, 1, 0.0, "",             "",                          ""),
    ("France",              2.3,  48.9, "market",   0,  18,  0,  0,  2,  3, 1, 0, 0.0, "",             "",                          ""),
    ("Netherlands",         5.0,  52.2, "market",   0,  14,  0,  0,  3,  2, 1, 1, 0.0, "",             "",                          ""),
    ("China",             116.4,  39.9, "market",   0,  24,  0,  0,  2,  4, 1, 0, 0.0, "",             "",                          ""),
    ("Taiwan",            121.0,  25.0, "market",   0,  16,  0,  0,  1,  3, 1, 0, 0.0, "",             "",                          ""),
    ("Bangkok",           100.5,  13.7, "market",   0,  18,  0,  0,  1,  4, 1, 0, 0.0, "",             "",                          ""),
    ("UAE",                55.3,  25.2, "market",   0,  10,  0,  0,  1,  2, 1, 0, 0.0, "",             "",                          ""),
    ("Spain",              -3.7,  40.4, "market",   0,   9,  0,  0,  1,  2, 0, 0, 0.0, "",             "",                          ""),
    ("Switzerland",         8.2,  46.8, "market",   0,   7,  0,  0,  1,  1, 1, 1, 0.0, "",             "",                          ""),
]

KEYS = ["farmers", "roasters", "coops", "mills", "exporters", "cafes",
        "researchers", "certifiers"]

TARGET = {"farmers": 4000, "roasters": 500, "coops": 150, "mills": 120,
          "exporters": 90, "cafes": 70, "researchers": 40, "certifiers": 30}


def build():
    places = []
    for r in ROWS:
        name, lon, lat, role = r[0], r[1], r[2], r[3]
        counts = dict(zip(KEYS, r[4:12]))
        places.append(dict(n=name, lon=lon, lat=lat, role=role,
                           c=counts, score=r[12], alt=r[13],
                           notes=r[14], proc=r[15]))
    return places


def rescale(places):
    """ปรับให้ยอดรวมของแต่ละบทบาทตรงตามสัดส่วนที่ตกลงกันไว้เป๊ะ"""
    for key, target in TARGET.items():
        cur = sum(p["c"][key] for p in places)
        if cur == 0:
            continue
        for p in places:
            p["c"][key] = round(p["c"][key] * target / cur)
        # ปัดเศษแล้วอาจขาดหรือเกิน เกลี่ยส่วนต่างไปที่รายใหญ่สุด
        diff = target - sum(p["c"][key] for p in places)
        while diff != 0:
            p = max(places, key=lambda q: q["c"][key])
            p["c"][key] += 1 if diff > 0 else -1
            diff += -1 if diff > 0 else 1
    return places


def main():
    places = rescale(build())
    totals = {k: sum(p["c"][k] for p in places) for k in KEYS}
    grand = sum(totals.values())
    out = dict(places=places, totals=totals, grand=grand)

    p = Path(__file__).parent / "participants.json"
    p.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")),
                 encoding="utf-8")

    print(f"  แหล่งข้อมูล {len(places)} จุด · รวม {grand} ราย")
    for k in KEYS:
        print(f"    {k:12} {totals[k]:>5}  ({totals[k]*100/grand:.0f}%)")
    print(f"  ขนาดไฟล์ {len(p.read_text(encoding='utf-8'))//1024} KB")


if __name__ == "__main__":
    main()
