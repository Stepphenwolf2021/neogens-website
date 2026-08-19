#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ตัดทางเข้าหน้า proof.html และ th-proof.html ออกจากเว็บ โดยไม่ลบตัวไฟล์

ตามที่ตกลงไว้ 2026-08-16 — เอาออกทั้งสองภาษา เก็บไฟล์ไว้ ตัดแค่ทางเข้า
URL เดิมยังเปิดได้ถ้ามีคนจำลิงก์ไว้ แต่ไม่มีทางเดินไปถึงจากในเว็บอีกแล้ว

ทางเข้าที่ตัด ห้าชนิด
  1 ลิงก์ในเมนู drawer          <a href="reference-implementation.html">Reference implementation</a>
  2 ลิงก์ใน footer              ข้อความเดียวกับข้อ 1 จึงตัดพร้อมกัน
  3 การ์ดสารบัญในหน้าแรก        บล็อก <a> ที่มี div.n กับ div.t
  4 ลิงก์ก่อนหน้า/ถัดไปท้ายหน้า  ต่อเชนใหม่ ไม่ใช่ลบทิ้ง ดูหมายเหตุข้างล่าง
  5 ตาราง hash ในหน้าแรก        "proof": "reference-implementation.html"
  6 สอง <url> ใน sitemap.xml

เชนเดิมคือ  engagement → proof → honest  จึงเชื่อม engagement เข้ากับ honest ตรง ๆ
ถ้าลบลิงก์ทิ้งเฉย ๆ คนอ่านจะเดินจาก engagement ไปต่อไม่ได้

**ไม่แตะ proof.html และ th-proof.html เลยแม้แต่ไบต์เดียว** เพราะในสองหน้านั้น
มีปุ่มเดโมที่ใช้ href="reference-implementation.html" onclick="return false" เป็นปุ่มหลอกอยู่สิบกว่าจุด
ถ้ากวาดตามชื่อไฟล์จะพังทั้งหน้า และการเก็บไว้ครบทำให้เอากลับมาง่าย

ย้อนกลับ:  git checkout -- <ไฟล์>   หรือรีเวิร์ต commit นี้ทั้งก้อน

รันจากรากรีโป:  python3 .tools/drop_proof.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = {"reference-implementation.html", "th-reference-implementation.html"}          # ห้ามแตะสองไฟล์นี้

EN = {
    "page": "reference-implementation.html",
    "nav": '<a href="reference-implementation.html">Reference implementation</a>',
    "hash": '"proof": "reference-implementation.html", ',
    "pager": [
        ('<a class="nx" href="reference-implementation.html"><div class="k">Next</div>'
         '<div class="t">Reference implementation</div></a>',
         '<a class="nx" href="what-we-wont-do.html"><div class="k">Next</div>'
         '<div class="t">What we won\'t do</div></a>'),
        ('<a class="pv" href="reference-implementation.html"><div class="k">Previous</div>'
         '<div class="t">Reference implementation</div></a>',
         '<a class="pv" href="engagement.html"><div class="k">Previous</div>'
         '<div class="t">Engagement</div></a>'),
    ],
}

TH = {
    "page": "th-reference-implementation.html",
    "nav": '<a href="th-reference-implementation.html">งานอ้างอิงที่เราทำเอง</a>',
    "hash": '"proof": "th-reference-implementation.html", ',
    "pager": [
        ('<a class="nx" href="th-reference-implementation.html"><div class="k">ถัดไป</div>'
         '<div class="t">งานอ้างอิงที่เราทำเอง</div></a>',
         '<a class="nx" href="th-what-we-wont-do.html"><div class="k">ถัดไป</div>'
         '<div class="t">สิ่งที่เราไม่ทำ</div></a>'),
        ('<a class="pv" href="th-reference-implementation.html"><div class="k">ก่อนหน้า</div>'
         '<div class="t">งานอ้างอิงที่เราทำเอง</div></a>',
         '<a class="pv" href="th-engagement.html"><div class="k">ก่อนหน้า</div>'
         '<div class="t">รูปแบบการทำงาน</div></a>'),
    ],
}

CARD = re.compile(r'\n?<a href="(?:th-)?proof\.html">\s*<div class="n">.*?</a>', re.S)

tally = {"nav": 0, "card": 0, "pager": 0, "hash": 0}
touched = []

for path in sorted(ROOT.glob("*.html")):
    if path.name in KEEP:
        continue
    s = before = path.read_text(encoding="utf-8")

    for d in (EN, TH):
        # การ์ดสารบัญต้องตัดก่อน เพราะขึ้นต้นด้วย <a href> เหมือนกัน
        s, n = CARD.subn("", s)
        tally["card"] += n
        for old, new in d["pager"]:
            if old in s:
                s = s.replace(old, new)
                tally["pager"] += 1
        n = s.count("\n" + d["nav"])
        s = s.replace("\n" + d["nav"], "")
        tally["nav"] += n
        n = s.count(d["nav"])
        s = s.replace(d["nav"], "")
        tally["nav"] += n
        if d["hash"] in s:
            s = s.replace(d["hash"], "")
            tally["hash"] += 1

    if s != before:
        path.write_text(s, encoding="utf-8")
        touched.append(path.name)

# ---------------------------------------------------------------- sitemap

sm_path = ROOT / "sitemap.xml"
sm = sm_before = sm_path.read_text(encoding="utf-8")
sm, dropped = re.subn(
    r'  <url>\s*<loc>https://www\.neogens\.co/(?:th-)?proof\.html</loc>.*?</url>\n',
    "", sm, flags=re.S)
sm_path.write_text(sm, encoding="utf-8")

# ---------------------------------------------------------------- ด่านตรวจ

left = {}
for path in sorted(ROOT.glob("*.html")):
    if path.name in KEEP:
        continue
    n = path.read_text(encoding="utf-8").count("reference-implementation.html")
    if n:
        left[path.name] = n

eng = (ROOT / "engagement.html").read_text(encoding="utf-8")
hon = (ROOT / "what-we-wont-do.html").read_text(encoding="utf-8")
abt = (ROOT / "about.html").read_text(encoding="utf-8")
t_eng = (ROOT / "th-engagement.html").read_text(encoding="utf-8")
t_hon = (ROOT / "th-what-we-wont-do.html").read_text(encoding="utf-8")
t_abt = (ROOT / "th-about.html").read_text(encoding="utf-8")

checks = {
    "ไม่เหลือลิงก์ไปหน้า proof เลย": not left,
    "sitemap ตัดออกสองบล็อก": dropped == 2,
    "sitemap ไม่เหลือคำว่า proof": "reference-implementation.html" not in sm,
    "sitemap เหลือ 36 url": sm.count("<url>") == 36,
    "การ์ดสารบัญถูกตัดสองใบ": tally["card"] == 2,
    "ตาราง hash ถูกตัดสองที่": tally["hash"] == 2,
    "ต่อเชนใหม่ครบหกจุด": tally["pager"] == 6,
    "engagement ต่อไป honest": 'class="nx" href="what-we-wont-do.html"' in eng,
    "honest ย้อนกลับไป engagement": 'class="pv" href="engagement.html"' in hon,
    "about ย้อนกลับไป engagement": 'class="pv" href="engagement.html"' in abt,
    "th-engagement ต่อไป th-honest": 'class="nx" href="th-what-we-wont-do.html"' in t_eng,
    "th-honest ย้อนกลับไป th-engagement": 'class="pv" href="th-engagement.html"' in t_hon,
    "th-about ย้อนกลับไป th-engagement": 'class="pv" href="th-engagement.html"' in t_abt,
    "ไม่มีลิงก์ว่างค้าง": all('href=""' not in p.read_text(encoding="utf-8")
                              for p in ROOT.glob("*.html")),
}

bad = [k for k, ok in checks.items() if not ok]
print(f"แก้ไป {len(touched)} ไฟล์ · ลิงก์เมนูกับ footer {tally['nav']} จุด · "
      f"การ์ด {tally['card']} ใบ · เชน {tally['pager']} จุด · "
      f"hash {tally['hash']} ที่ · sitemap {dropped} บล็อก")
if left:
    print("ยังเหลือ:", left)
if bad:
    sys.exit("✗ ด่านตรวจไม่ผ่าน: " + " · ".join(bad))
print("✓ ผ่านด่านตรวจครบทุกข้อ · proof.html กับ th-proof.html ไม่ถูกแตะ")
