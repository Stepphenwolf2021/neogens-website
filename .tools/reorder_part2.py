#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ย้าย "สิ่งที่คุณถืออยู่" ไปอยู่หลังหน้า 01 ของภาค 2   ตกลงกันไว้ 2026-08-20

ปัญหาเดิม เว็บพูดเรื่องหน้านี้ไม่ตรงกันห้าที่
  เมนู · ประตูหน้าแรก · ป้ายบนหน้า  บอกว่าอยู่ภาค 2 และอยู่เหนือ 01
  เชนก่อนหน้า/ถัดไป · breadcrumb   บอกว่าอยู่ภาค 1
ความขัดกันสองอันหลังเป็นของที่ผมใส่ผิดตอนสร้าง JSON-LD แล้วมันเพิ่งโผล่ให้เห็น
ตอนเอา breadcrumb ขึ้นมาแสดงบนหน้า ก่อนหน้านั้นมันซ่อนอยู่ในไฟล์

ลำดับใหม่ของภาค 2 คือ  01 สถานะวันนี้ → สิ่งที่คุณถืออยู่ → 02 → 03 → ที่เหลือ
สคริปต์นี้แก้เมนูในต้นฉบับ กับแถบ footer ในทุกหน้า
ส่วนประตูหน้าแรก เชนหน้า และ JSON-LD แก้ที่ตัวสร้างของมันเอง แล้วรันใหม่

รันจากรากรีโป:  python3 .tools/reorder_part2.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIRS = {
    "en": ("what-you-are-holding.html", "mkm-for-museums-and-libraries.html"),
    "th": ("th-what-you-are-holding.html", "th-mkm-for-museums-and-libraries.html"),
}


def move_after(block, mover, anchor):
    """ดึงลิงก์ mover ออกมาแล้ววางต่อท้ายลิงก์ anchor · คืน None ถ้าเรียงถูกอยู่แล้ว"""
    m = re.search(r'<a[^>]*href="' + re.escape(mover) + r'"[^>]*>.*?</a>', block, re.S)
    a = re.search(r'<a[^>]*href="' + re.escape(anchor) + r'"[^>]*>.*?</a>', block, re.S)
    if not (m and a):
        return None
    if m.start() > a.start():
        return None                      # อยู่หลัง anchor แล้ว ไม่ต้องทำอะไร
    tag = m.group(0)
    out = block[:m.start()] + block[m.end():]
    a = re.search(r'<a[^>]*href="' + re.escape(anchor) + r'"[^>]*>.*?</a>', out, re.S)
    return out[:a.end()] + tag + out[a.end():]


# ---------------------------------------------------------------- 1 · ต้นฉบับเมนู
for lang, (mover, anchor) in PAIRS.items():
    p = ROOT / ".tools" / "shell" / f"nav.{lang}.html"
    s = p.read_text(encoding="utf-8")
    # ต้องทำเฉพาะในเขต drawer เพราะแถบบนมีลิงก์ชื่อเดียวกันอยู่ก่อนหน้า
    dw = re.search(r'<div class="drawer".*?</nav>', s, re.S)
    if not dw:
        sys.exit(f"✗ nav.{lang}.html หาเขต drawer ไม่เจอ")
    moved_block = move_after(dw.group(0), mover, anchor)
    out = None if moved_block is None else s[:dw.start()] + moved_block + s[dw.end():]
    if out is None:
        print(f"  nav.{lang}.html เรียงถูกอยู่แล้ว")
        continue
    order = re.findall(r'href="([^"]+)"',
                       re.search(r'<div class="drawer".*?</nav>', out, re.S).group(0))
    if order.index(anchor) + 1 != order.index(mover):
        sys.exit(f"✗ nav.{lang}.html ย้ายแล้วลำดับยังไม่ติดกัน")
    p.write_text(out, encoding="utf-8")
    print(f"  nav.{lang}.html ย้ายแล้ว")

# ---------------------------------------------------------------- 2 · แถบ footer ทุกหน้า
FCOL = re.compile(r'<div class="f-col">.*?(?=<div class="f-col">|</div></div>)', re.S)
moved = 0
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or "f-cols" not in s:
        continue
    lang = "th" if path.name.startswith("th-") else "en"
    mover, anchor = PAIRS[lang]

    def fix(m):
        out = move_after(m.group(0), mover, anchor)
        return out if out else m.group(0)

    s = FCOL.sub(fix, s)
    if s != before:
        path.write_text(s, encoding="utf-8")
        moved += 1
print(f"  แถบ footer ย้ายแล้ว {moved} หน้า")

# ---------------------------------------------------------------- ด่านตรวจ
bad = []
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue
    lang = "th" if path.name.startswith("th-") else "en"
    mover, anchor = PAIRS[lang]
    for label, block in (("เมนู", re.search(r'<div class="drawer".*?</nav>', s, re.S)),
                         ("footer", re.search(r'<div class="f-cols">.*?</footer>', s, re.S))):
        if not block:
            continue
        order = re.findall(r'href="([^"]+)"', block.group(0))
        if mover in order and anchor in order:
            if order.index(mover) < order.index(anchor):
                bad.append(f"{path.name} {label} ยังเรียง {mover} ก่อน {anchor}")
if bad:
    sys.exit("✗ " + "\n   ".join(bad[:6]))
print("✓ ทั้งเมนูและ footer เรียง 01 ก่อน สิ่งที่คุณถืออยู่ ทุกหน้า")
