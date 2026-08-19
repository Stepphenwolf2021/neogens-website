#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ซ่อมแท็ก hreflang ที่ชี้ไปหน้าอื่น

พบตอนตรวจก่อนเปิดตัว 2026-08-19 สามหน้าประกาศฉบับแปลของตัวเองผิด
  about.html · th-about.html      ชี้ไป what-we-wont-do ซึ่งคนละเรื่องกันทั้งหน้า
                                  ติดมาตั้งแต่สร้างหน้าจากแม่แบบเดิมแล้วไม่ได้แก้ตาม
  long-read-museums-and-libraries ประกาศว่ามีฉบับไทย ทั้งที่ไม่มี และ en ชี้ไปหน้าแรก

การประกาศฉบับแปลที่ไม่ยืนยันกลับ ทำให้ search engine เลิกเชื่อ hreflang ทั้งโดเมน
ไม่ใช่แค่หน้าที่ผิด จึงต้องแก้ก่อนปล่อยให้เข้ามาเก็บข้อมูล

หน้าที่ไม่มีคู่ภาษา ประกาศแค่ภาษาตัวเองกับ x-default ที่ชี้มาที่ตัวเอง

รันจากรากรีโป:  python3 .tools/fix_hreflang.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.neogens.co/"
SKIP = {"404.html"}

BLOCK = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n')


def twin(name):
    """คู่ภาษาของหน้านี้ ถ้ามีอยู่จริง"""
    other = name[3:] if name.startswith("th-") else "th-" + name
    return other if (ROOT / other).exists() else None


def tags(name):
    en = name[3:] if name.startswith("th-") else name
    th = twin(name) if not name.startswith("th-") else name
    if name.startswith("th-") and not (ROOT / en).exists():
        en = None
    out = []
    if en:
        out.append(("en", en))
    if th:
        out.append(("th", th))
    out.append(("x-default", en or name))
    # หน้าแรกใช้รากโดเมน ไม่ใช่ index.html ตามที่ canonical ตั้งไว้อยู่แล้ว
    return [(k, "" if v == "index.html" else v) for k, v in out]


changed, report = [], []
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if path.name in SKIP or 'http-equiv="refresh"' in s:
        continue
    found = BLOCK.findall(s)
    if not found:
        sys.exit(f"✗ {path.name} ไม่มีแท็ก hreflang เลย")

    want = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{v}">\n'
                   for k, v in tags(path.name))
    first = s.index(found[0])
    s = BLOCK.sub("", s)
    s = s[:first] + want + s[first:]

    if s != before:
        old = [re.search(r'hreflang="([^"]*)" href="[^"]*/([^"/]*)"', b).groups() for b in found]
        path.write_text(s, encoding="utf-8")
        changed.append(path.name)
        report.append((path.name,
                       " ".join(f"{k}→{v or '/'}" for k, v in old),
                       " ".join(f"{k}→{v or '/'}" for k, v in tags(path.name))))

# ---------------------------------------------------------------- ด่านตรวจ
bad = []
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if path.name in SKIP or 'http-equiv="refresh"' in s:
        continue
    alts = dict(re.findall(r'hreflang="([^"]+)" href="' + re.escape(BASE) + r'([^"]*)"', s))
    self_name = "" if path.name == "index.html" else path.name
    if self_name not in alts.values():
        bad.append(f"{path.name} hreflang ไม่ยืนยันกลับมาที่ตัวเอง")
    if "x-default" not in alts:
        bad.append(f"{path.name} ขาด x-default")
    for k, v in alts.items():
        target = v or "index.html"
        if not (ROOT / target).exists():
            bad.append(f"{path.name} hreflang {k} ชี้ไฟล์ที่ไม่มี {target}")
    t = twin(path.name)
    if t and "th" not in alts:
        bad.append(f"{path.name} มีฉบับไทยอยู่ แต่ไม่ได้ประกาศ")
    if not t and path.name.startswith("th-") is False and "th" in alts:
        bad.append(f"{path.name} ประกาศฉบับไทย ทั้งที่ไม่มีไฟล์")

for name, old, new in report:
    print(f"  {name}\n      เดิม {old}\n      ใหม่ {new}")
print(f"\nแก้ {len(changed)} ไฟล์")
if bad:
    sys.exit("✗ ด่านตรวจไม่ผ่าน:\n   " + "\n   ".join(bad))
print("✓ ทุกหน้า hreflang ยืนยันกลับมาที่ตัวเอง · มี x-default · ปลายทางมีจริง")
