#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ถอด Google Analytics ออกจากทุกหน้า

ตกลงกันไว้ 2026-08-19 หลังตรวจก่อนเปิดตัว เหตุผลสามข้อ
  1 PDPA กำหนดให้แจ้งวัตถุประสงค์ก่อนเก็บข้อมูลส่วนบุคคล ตอนนี้ยิงตั้งแต่วินาทีแรก
  2 กลุ่มเป้าหมายมีสถาบันในยุโรปและโรงคั่วกลุ่มนอร์ดิก ซึ่งอยู่ใต้ GDPR
  3 เว็บที่ขายเรื่องอธิปไตยเหนือข้อมูล ไม่ควรส่ง IP ผู้อ่านไป Google
    ตั้งแต่ก่อนเขาได้อ่านย่อหน้าแรก

ถ้าต้องการตัวเลขผู้เข้าชม ให้ใช้ Cloudflare Web Analytics ซึ่งไม่ใช้คุกกี้
และไม่เก็บข้อมูลระบุตัวตน จึงไม่ต้องมีแบนเนอร์ขอความยินยอม

รันจากรากรีโป:  python3 .tools/remove_analytics.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# บล็อกทั้งก้อน ตั้งแต่คอมเมนต์ถึงปิด script ตัวที่สอง
BLOCK = re.compile(
    r'[ \t]*<!-- Google tag \(gtag\.js\) -->\n'
    r'[ \t]*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=[^"]*"></script>\n'
    r'[ \t]*<script>\n(?:.*?\n)*?[ \t]*</script>\n')

done, left = [], []
# กวาดโฟลเดอร์ย่อยด้วย · หน้าใน archive/ ยังเปิดจากเว็บได้แม้จะ noindex
# คนที่เปิด URL เก่าตรง ๆ จึงยังถูกส่ง IP ไป Google อยู่ ถ้าไม่ถอดออก
for path in sorted(ROOT.rglob("*.html")):
    if ".tools" in path.parts:
        continue
    s = before = path.read_text(encoding="utf-8")
    if "googletagmanager" not in s:
        continue
    s, n = BLOCK.subn("", s)
    if n != 1:
        sys.exit(f"✗ {path.relative_to(ROOT)} เจอบล็อก analytics {n} ก้อน รูปแบบไม่ตรงที่คาด ยังไม่ได้แก้อะไร")
    # ด่านต่อไฟล์ ต้องไม่เหลือร่องรอย และต้องไม่กินโค้ดอื่นไปด้วย
    checks = {
        "ไม่เหลือ gtag": "gtag" not in s and "googletagmanager" not in s and "dataLayer" not in s,
        "สคริปต์อื่นยังอยู่ครบ": s.count("<script") == before.count("<script") - 2,
        "ไม่ได้ลบสคริปต์ตั้งธีมไปด้วย": ("ng-theme" in s) == ("ng-theme" in before),
        "ตัดออกไม่เกินขนาดบล็อก": 0 < len(before) - len(s) < 400,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {path.relative_to(ROOT)} ด่านตรวจไม่ผ่าน: " + " · ".join(bad))
    path.write_text(s, encoding="utf-8")
    done.append(str(path.relative_to(ROOT)))

for path in ROOT.rglob("*.html"):
    if ".tools" in path.parts: continue
    if "googletagmanager" in path.read_text(encoding="utf-8"):
        left.append(path.name)

print(f"ถอด GA ออกจาก {len(done)} หน้า")
if left:
    sys.exit("✗ ยังเหลือใน: " + ", ".join(left))
print("✓ ไม่เหลือ Google Analytics ในไฟล์ไหนเลย")
