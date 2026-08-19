#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ซ่อมปุ่มสลับภาษาให้อยู่หน้าเดิม ไม่เด้งกลับหน้าแรก

อาการเดิม ทุกหน้ามีปุ่มสลับภาษาสองชุด ชุดจอกว้างอยู่ใน nav ชุดจอแคบอยู่ใน .nav-mob
ชุดจอแคบของเกือบทุกหน้าชี้ไป index.html / th-index.html ค้างไว้ตั้งแต่ตอนทำแม่แบบ
คนอ่านบนมือถือกดสลับภาษาแล้วจึงหลุดจากเนื้อหาที่กำลังอ่าน กลับไปหน้าแรก

หน้ากลุ่มกาแฟพลาดอีกแบบ ชุดจอแคบชี้ไป coffee.html และ coffee-demo.html
ชี้ผิดตั้งแต่ชุดจอกว้าง คือชี้ไป coffee-farmer.html แทนที่จะเป็นตัวเอง

วิธีแก้ ประกอบปุ่มทั้งสองชุดขึ้นใหม่จากชื่อไฟล์ของหน้านั้นเอง ไม่ก๊อปจากชุดจอกว้าง
เพราะบางหน้าชุดจอกว้างก็ผิดอยู่แล้ว

หน้าที่ยังไม่มีฉบับไทย ใช้ปลายทางที่ใกล้เคียงที่สุดไปก่อน และประกาศไว้ในตาราง FALLBACK

รันจากรากรีโป:  python3 .tools/fix_lang_switch.py
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"404.html"}      # ไม่มีปุ่มสลับภาษา ไม่ต้องแตะ


def is_stub(path):
    """หน้า stub ที่เด้งไปชื่อใหม่ ไม่มีแถบนำทาง จึงไม่มีปุ่มสลับภาษา"""
    s = path.read_text(encoding="utf-8")
    return 'http-equiv="refresh"' in s and 'rel="canonical"' in s

# หน้าที่ยังไม่มีคู่ภาษาไทย ให้ปุ่ม TH พาไปที่ใกล้เคียงที่สุดไปก่อน
FALLBACK = {
    "coffee-demo.html": "th-mkm-for-coffee.html",
    "long-read-museums-and-libraries.html": "th-index.html",
}

BLOCK = re.compile(r'<span class="lang">.*?</span>(?=<button)', re.S)

def targets(name):
    base = name[3:] if name.startswith("th-") else name
    en = base
    th = "th-" + base
    if not (ROOT / th).exists():
        th = FALLBACK.get(base)
        if th is None:
            sys.exit(f"✗ {name} ไม่มีฉบับไทย และไม่ได้ประกาศปลายทางสำรองไว้")
    return en, th

def build(name):
    en, th = targets(name)
    if name.startswith("th-"):
        return (f'<span class="lang"><a class="on" href="{th}">TH</a>'
                f'<span>/</span><a href="{en}">EN</a></span>')
    return (f'<span class="lang"><a class="on" href="{en}">EN</a>'
            f'<span>/</span><a href="{th}">TH</a></span>')

changed, untouched, report = [], [], []
for path in sorted(ROOT.glob("*.html")):
    if path.name in SKIP or is_stub(path):
        continue
    s = before = path.read_text(encoding="utf-8")
    found = BLOCK.findall(s)
    if len(found) != 2:
        sys.exit(f"✗ {path.name} เจอปุ่มสลับภาษา {len(found)} ชุด ควรเจอ 2 ชุด")
    want = build(path.name)
    s = BLOCK.sub(lambda m: want, s)
    if s != before:
        path.write_text(s, encoding="utf-8")
        changed.append(path.name)
        for i, old in enumerate(found):
            if old != want:
                report.append((path.name, "จอกว้าง" if i == 0 else "จอแคบ",
                               " ".join(re.findall(r'href="([^"]+)"', old)),
                               " ".join(re.findall(r'href="([^"]+)"', want))))
    else:
        untouched.append(path.name)

# ---------------------------------------------------------------- ด่านตรวจ
bad = []
for path in sorted(ROOT.glob("*.html")):
    if path.name in SKIP or is_stub(path):
        continue
    s = path.read_text(encoding="utf-8")
    blocks = BLOCK.findall(s)
    en, th = targets(path.name)
    if len(blocks) != 2:
        bad.append(f"{path.name} เหลือปุ่ม {len(blocks)} ชุด")
    if len(set(blocks)) != 1:
        bad.append(f"{path.name} ปุ่มสองชุดยังไม่ตรงกัน")
    for b in blocks:
        hrefs = re.findall(r'href="([^"]+)"', b)
        if set(hrefs) != {en, th}:
            bad.append(f"{path.name} ชี้ไป {hrefs} ควรเป็น {[en, th]}")
        if 'class="on"' not in b:
            bad.append(f"{path.name} ไม่มีปุ่มที่ทำเครื่องหมายภาษาปัจจุบัน")
    for t in (en, th):
        if not (ROOT / t).exists():
            bad.append(f"{path.name} ชี้ไปไฟล์ที่ไม่มีอยู่ {t}")

print(f"แก้ {len(changed)} ไฟล์ · เดิมถูกอยู่แล้ว {len(untouched)} ไฟล์")
for name, which, old, new in report:
    print(f"   {name:34} {which}  {old}  →  {new}")
if bad:
    sys.exit("✗ ด่านตรวจไม่ผ่าน:\n   " + "\n   ".join(bad))
print("✓ ทุกหน้าปุ่มสองชุดตรงกัน และชี้อยู่ที่เนื้อหาเดิมของหน้านั้น")
