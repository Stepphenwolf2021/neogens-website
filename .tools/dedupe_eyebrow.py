#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ตัดส่วนที่ป้ายหมวดพูดซ้ำกับเส้นทาง breadcrumb   สั่งเมื่อ 2026-08-20

พอเอา breadcrumb ขึ้นมาแสดงบนหน้า ป้ายหมวดที่อยู่ใต้มันก็กลายเป็นการพูดซ้ำ
ตัวอย่างที่ชัดที่สุดคือหน้า สิ่งที่คุณถืออยู่ สองบรรทัดติดกันพูดเหมือนกันทุกคำ

    Neo Gens › MKM สำหรับพิพิธภัณฑ์และห้องสมุด › สิ่งที่คุณถืออยู่
    MKM สำหรับพิพิธภัณฑ์และห้องสมุด · 01b — สิ่งที่คุณถืออยู่

กฎที่ใช้
  1 ถ้าท้ายป้ายพูดคำเดียวกับขั้นสุดท้ายของเส้นทาง  ตัดทั้งบรรทัด เพราะไม่ได้บอกอะไรใหม่
  2 ถ้าซ้ำแค่ชื่อภาค                              ตัดชื่อภาคออก เหลือเลขกับคำบรรยาย
  3 ถ้าไม่ซ้ำ                                     ไม่แตะ

รันจากรากรีโป:  python3 .tools/dedupe_eyebrow.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EYE = re.compile(r'[ \t]*<div class="(?:kicker|eyebrow[^"]*)">(.*?)</div>\n?', re.S)
CRUMBS = re.compile(r'<nav class="crumbs".*?</nav>', re.S)


def norm(x):
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", x)).split())


dropped, trimmed, left = [], [], []
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s:
        continue
    nav = CRUMBS.search(s)
    head = s[:s.index('<h1')] if '<h1' in s else s
    eye = EYE.search(head)
    if not (nav and eye):
        continue

    crumbs = [norm(x) for x in re.findall(r"<li[^>]*>(?:<a[^>]*>)?([^<]*)", nav.group(0))]
    e = norm(eye.group(1))
    m = re.match(r"^(.*?)\s*·\s*(?:(\d{2}[a-z]?)\s*—\s*)?(.*)$", e)
    sec, num, tail = (m.group(1), m.group(2), m.group(3)) if m else (None, None, e)

    if tail and crumbs and tail == crumbs[-1]:
        s = s[:eye.start()] + s[eye.end():]          # กฎ 1 · ตัดทั้งบรรทัด
        dropped.append(path.name)
    elif sec and len(crumbs) > 1 and sec == crumbs[1]:
        rest = (f"{num} — {tail}" if num else tail)   # กฎ 2 · เหลือเฉพาะส่วนที่เพิ่มข้อมูล
        s = s[:eye.start()] + re.sub(r">(.*?)</div>", ">" + rest + "</div>",
                                     eye.group(0), count=1, flags=re.S) + s[eye.end():]
        trimmed.append(path.name)
    else:
        left.append(path.name)

    if s != before:
        path.write_text(s, encoding="utf-8")

# ---------------------------------------------------------------- ด่านตรวจ
bad = []
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s:
        continue
    nav = CRUMBS.search(s)
    head = s[:s.index('<h1')] if '<h1' in s else s
    eye = EYE.search(head)
    if not nav:
        continue
    crumbs = [norm(x) for x in re.findall(r"<li[^>]*>(?:<a[^>]*>)?([^<]*)", nav.group(0))]
    if eye:
        e = norm(eye.group(1))
        if len(crumbs) > 1 and crumbs[1] and crumbs[1] in e:
            bad.append(f"{path.name} ป้ายยังมีชื่อภาคซ้ำกับเส้นทาง")
        if crumbs and crumbs[-1] and e == crumbs[-1]:
            bad.append(f"{path.name} ป้ายยังพูดคำเดียวกับขั้นสุดท้าย")
    if s.index('class="crumbs"') > s.index("<h1"):
        bad.append(f"{path.name} เส้นทางหลุดไปอยู่หลังพาดหัว")

print(f"  ตัดทั้งบรรทัด {len(dropped)} หน้า · ตัดชื่อภาคออก {len(trimmed)} หน้า · ไม่แตะ {len(left)} หน้า")
if dropped:
    print("   ตัดทั้งบรรทัด:", ", ".join(dropped))
if bad:
    sys.exit("✗ " + "\n   ".join(sorted(set(bad))[:8]))
print("✓ ไม่เหลือป้ายที่พูดซ้ำกับเส้นทางแล้ว")
