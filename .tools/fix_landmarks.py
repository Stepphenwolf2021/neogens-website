#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เพิ่ม landmark · ลิงก์ข้ามไปเนื้อหา · aria-current · focus-visible   ข้อ 12 จากรายงานตรวจ

ของเดิม
  ไม่มี <main> สักหน้า      คนใช้โปรแกรมอ่านหน้าจอต้องฟังเมนูซ้ำทุกหน้าก่อนถึงเนื้อหา
  ไม่มีลิงก์ข้ามไปเนื้อหา    คนใช้คีย์บอร์ดต้อง tab ผ่านเมนูทั้งชุดทุกครั้ง
  ไม่มี aria-current        หน้าปัจจุบันในเมนูบอกด้วยสีอย่างเดียว ซึ่งโปรแกรมอ่านหน้าจอไม่เห็น
  ไม่มี :focus-visible      มีแค่ :focus ที่เปลี่ยนสีขอบ บนพื้นเข้มแทบมองไม่เห็น

ลิงก์ข้ามใช้ background:var(--fg) กับ color:var(--bg) ไม่ใช่สีเน้น
เพราะสีเน้นเปลี่ยนค่าระหว่างธีม (มืด #B8F04A · สว่าง #4C7A0B) ตัวอักษรบนพื้นนั้นจะต้องสลับตาม
คู่ fg/bg สลับให้เองอยู่แล้วและได้ contrast สูงสุดทั้งสองธีม

aria-current ใส่เฉพาะลิงก์ที่ชี้มาที่หน้าตัวเองจริง และไม่ใส่ให้ปุ่มหลอกที่มี onclick
เพราะในหน้า reference-implementation มีแท็บสาธิตที่ใช้ href ชี้ตัวเองเป็นปุ่มหลอกอยู่หลายตัว

รันจากรากรีโป:  python3 .tools/fix_landmarks.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS = """
/* --- ลิงก์ข้ามไปเนื้อหา กับกรอบโฟกัสที่มองเห็นได้ --- */
.skip{position:absolute;left:-9999px;top:0;z-index:120}
.skip:focus{left:10px;top:10px;background:var(--fg);color:var(--bg);
  padding:11px 18px;border-radius:10px;text-decoration:none;font-size:14.5px;
  line-height:1.75;box-shadow:0 8px 30px var(--shadow,rgba(0,0,0,.4))}
:focus-visible{outline:2px solid var(--go);outline-offset:3px;border-radius:3px}
"""

LABEL = {"en": "Skip to content", "th": "ข้ามไปยังเนื้อหา"}


def close_of(s, start):
    """หา </nav> ที่ปิด <nav id="nav"> โดยนับความลึก กัน nav ซ้อนใน nav"""
    depth, i = 0, start
    for m in re.finditer(r'<nav\b|</nav>', s[start:]):
        depth += 1 if m.group(0) == "<nav" else -1
        if depth == 0:
            return start + m.end()
    sys.exit("หา </nav> ที่ปิดแถบเมนูไม่เจอ")


done = []
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue
    if "<main" in s:
        continue

    lang = "th" if path.name.startswith("th-") else "en"

    # 1 · ครอบเนื้อหาด้วย <main>
    nav = s.index('<nav id="nav">')
    start = close_of(s, nav)
    end = s.rindex("<footer")
    s = s[:start] + '\n<main id="main">' + s[start:end] + "</main>\n" + s[end:]

    # 2 · ลิงก์ข้ามไปเนื้อหา เป็น element แรกใน body
    body = re.search(r"<body[^>]*>", s)
    s = (s[:body.end()] + f'\n<a class="skip" href="#main">{LABEL[lang]}</a>'
         + s[body.end():])

    # 3 · aria-current ตรงที่ใส่ class="on" อยู่แล้ว และชี้มาที่หน้านี้จริง
    me = re.escape(path.name)
    s, n_cur = re.subn(r'<a class="on" href="' + me + r'">',
                       f'<a class="on" aria-current="page" href="{path.name}">', s)

    # 4 · CSS
    s = s.replace("</style>", CSS + "</style>", 1)

    checks = {
        "มี main เดียว": s.count("<main id=\"main\">") == 1 and s.count("</main>") == 1,
        "main อยู่หลังเมนู": s.index("<main") > s.index('<nav id="nav">'),
        "main จบก่อน footer": s.index("</main>") < s.rindex("<footer"),
        "ลิงก์ข้ามอยู่ต้น body": s.index('class="skip"') < s.index('<nav id="nav">'),
        "aria-current อย่างน้อยหนึ่งจุด": n_cur >= 1,
        "ไม่ใส่ aria-current ให้ปุ่มหลอก": 'aria-current="page" href="' + path.name + '" onclick' not in s,
        "CSS เข้าไฟล์": ".skip{" in s and s.index(".skip{") < s.index("</style>"),
        "แท็กสมดุล": s.count("<main") == s.count("</main>"),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {path.name}: " + " · ".join(bad))
    path.write_text(s, encoding="utf-8")
    done.append((path.name, n_cur))

print(f"แก้ {len(done)} หน้า · aria-current รวม {sum(n for _, n in done)} จุด")
print("✓ ทุกหน้ามี main · ลิงก์ข้ามไปเนื้อหา · กรอบโฟกัสที่มองเห็นได้")
