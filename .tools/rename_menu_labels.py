#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เปลี่ยนป้ายในเมนูสามอัน ตามที่ Noppadol สั่งเมื่อ 2026-08-20

  All sections          → Home
  What it is            → What is MKM ?
  Visitors and readers  → The new experience

ป้ายพวกนี้ไม่ได้อยู่แค่ใน drawer แต่โผล่ในสี่ที่ที่ล้วนเป็นการนำทาง
  เมนู drawer · แถบ footer · ประตูหน้าแรก · ป้ายในลิงก์ก่อนหน้า/ถัดไป
ถ้าแก้ที่เดียวจะเหลือชื่อเก่าค้างอีกสามที่

คำอังกฤษเป็นคำที่ Noppadol เขียนมาเอง วางลงตรง ๆ ทุกตัวอักษร รวมเว้นวรรคหน้าเครื่องหมายคำถาม
คำไทยเป็นคำที่ Claude เสนอ ให้เปลี่ยนได้ถ้าไม่ตรงใจ

**ไม่แตะ <title> และ breadcrumb ของหน้า** เพราะคำสั่งบอกว่าในเมนู
ทั้งสองจุดนั้นยังใช้ชื่อเดิม ดูหมายเหตุท้ายผลรัน

รันจากรากรีโป:  python3 .tools/rename_menu_labels.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIRS = [
    # (เก่า, ใหม่) · เทียบทั้งก้อนข้อความใน >…< จึงไม่ไปโดนคำเดียวกันในเนื้อหา
    ("All sections", "Home"),
    ("02 · What it is", "02 · What is MKM ?"),
    ("What it is", "What is MKM ?"),
    ("02 · Visitors and readers", "02 · The new experience"),
    ("Visitors and readers", "The new experience"),
    ("สารบัญทั้งหมด", "หน้าแรก"),
    ("02 · สิ่งนี้คืออะไร", "02 · MKM คืออะไร"),
    ("สิ่งนี้คืออะไร", "MKM คืออะไร"),
    ("02 · ผู้ชมและผู้อ่าน", "02 · ประสบการณ์แบบใหม่"),
    ("ผู้ชมและผู้อ่าน", "ประสบการณ์แบบใหม่"),
]

# แก้เฉพาะข้อความที่เป็นป้ายนำทาง ไม่แตะเนื้อหาในหน้า
TARGETS = [
    re.compile(r'(<a[^>]*>)([^<]+)(</a>)'),          # ลิงก์ในเมนู footer ประตู
    re.compile(r'(<div class="t">)([^<]+)(</div>)'),  # ป้ายในลิงก์ก่อนหน้า/ถัดไป
]


def swap(text):
    for old, new in PAIRS:
        if text.strip() == old:
            return new
    return None


def apply(s):
    n = 0
    for pat in TARGETS:
        def sub(m):
            nonlocal n
            new = swap(m.group(2))
            if new is None:
                return m.group(0)
            n += 1
            return m.group(1) + new + m.group(3)
        s = pat.sub(sub, s)
    return s, n


total = 0
for p in [ROOT / ".tools" / "shell" / "nav.en.html",
          ROOT / ".tools" / "shell" / "nav.th.html"]:
    s, n = apply(p.read_text(encoding="utf-8"))
    p.write_text(s, encoding="utf-8")
    total += n
    print(f"  {p.name} {n} จุด")

pages = 0
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s:
        continue
    s, n = apply(s)
    if s != before:
        path.write_text(s, encoding="utf-8")
        pages += 1
        total += n
print(f"  หน้าเว็บ {pages} ไฟล์ · รวมทั้งหมด {total} จุด")

# ตัวสร้างประตูหน้าแรก ต้องแก้ที่ต้นทางด้วย ไม่งั้น build รอบหน้าจะย้อนกลับ
g = ROOT / ".tools" / "build_gates.py"
s = g.read_text(encoding="utf-8")
for old, new in PAIRS:
    s = s.replace(f'"{old}")', f'"{new}")')
g.write_text(s, encoding="utf-8")

# ---------------------------------------------------------------- ด่านตรวจ
bad = []
OLD = ["All sections", "What it is", "Visitors and readers",
       "สารบัญทั้งหมด", "สิ่งนี้คืออะไร", "ผู้ชมและผู้อ่าน"]
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s:
        continue
    for pat in TARGETS:
        for m in pat.finditer(s):
            if m.group(2).strip() in OLD:
                bad.append(f"{path.name} ยังมีป้ายเก่า {m.group(2).strip()!r}")
if bad:
    sys.exit("✗ " + "\n   ".join(sorted(set(bad))[:8]))
print("✓ ไม่เหลือป้ายเก่าในเมนู footer ประตู หรือเชนหน้า")
