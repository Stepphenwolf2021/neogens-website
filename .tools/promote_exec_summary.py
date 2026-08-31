#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ทำให้ exec summary เป็นหน้าแรกของภาค 2 จริง ตามที่ Noppadol สั่งเมื่อ 2026-08-31

ไม่ใช่แค่สลับลำดับในเมนู หัวกลุ่มบนแถบเมนู ประตูที่สองในหน้าแรก คอลัมน์ footer
และปลายทางของ breadcrumb ทุกหน้าในภาค 2 ชี้มาที่หน้านี้ทั้งหมด

ป้ายในเมนูคือ Executive summary ไม่มีเลขนำ ตามที่เขาเลือก
เลข 01 02 03 ของหน้าเดิมจึงคงไว้เท่าเดิม ไม่ได้ไล่เลื่อน

แก้ที่ต้นฉบับ ไม่ได้แก้ HTML ทีละไฟล์
  .tools/shell/nav.en.html · nav.th.html   ต้นฉบับเมนู
  .tools/build_footer.py                    ต้นฉบับ footer อยู่ในตัวแปร COLS ดูข้อ 15 ของ LESSONS
  .tools/build_gates.py                     สามประตูหน้าแรก
  .tools/build_jsonld.py                    PART_NAME กำหนดปลายทางของ breadcrumb ภาค 2

รันซ้ำได้ ถ้าย้ายไปแล้วจะข้าม

รันจากรากรีโป:  python3 .tools/promote_exec_summary.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EN_ITEM = '<a href="exec-summary-museums.html">Executive summary</a>'
TH_ITEM = '<a href="th-exec-summary-museums.html">บทสรุปสำหรับผู้บริหาร</a>'
EN_FIRST = '<a href="mkm-for-museums-and-libraries.html">01 · Where things stand</a>'
TH_FIRST = '<a href="th-mkm-for-museums-and-libraries.html">01 · สถานะวันนี้</a>'

JOBS = [
    # ---- เมนู ย้ายรายการขึ้นหัวกลุ่ม ทั้งแถบบนและ drawer ----
    (".tools/shell/nav.en.html", [
        (EN_ITEM, "", 2),                       # ถอดออกจากที่เดิม สองที่
        (EN_FIRST, EN_ITEM + EN_FIRST, 2),      # ใส่กลับไว้หน้าสุด สองที่
        # หัวกลุ่มบนแถบเมนู ชี้มาที่หน้าใหม่
        ('<span class="hs"><a href="mkm-for-museums-and-libraries.html">'
         'MKM for Museums &amp; Libraries</a>',
         '<span class="hs"><a href="exec-summary-museums.html">'
         'MKM for Museums &amp; Libraries</a>', 1),
    ]),
    (".tools/shell/nav.th.html", [
        (TH_ITEM, "", 2),
        (TH_FIRST, TH_ITEM + TH_FIRST, 2),
        ('<span class="hs"><a href="th-mkm-for-museums-and-libraries.html">'
         'MKM สำหรับพิพิธภัณฑ์และห้องสมุด</a>',
         '<span class="hs"><a href="th-exec-summary-museums.html">'
         'MKM สำหรับพิพิธภัณฑ์และห้องสมุด</a>', 1),
    ]),

    # ---- footer ต้นฉบับอยู่ใน COLS ของสคริปต์ ไม่ใช่ในไฟล์ shell ----
    (".tools/build_footer.py", [
        ('            ("exec-summary-museums.html", "Executive summary"),\n', "", 1),
        ('            ("mkm-for-museums-and-libraries.html", "Where things stand"),',
         '            ("exec-summary-museums.html", "Executive summary"),\n'
         '            ("mkm-for-museums-and-libraries.html", "Where things stand"),', 1),
        ('            ("th-exec-summary-museums.html", "บทสรุปสำหรับผู้บริหาร"),\n', "", 1),
        ('            ("th-mkm-for-museums-and-libraries.html", "สถานะวันนี้"),',
         '            ("th-exec-summary-museums.html", "บทสรุปสำหรับผู้บริหาร"),\n'
         '            ("th-mkm-for-museums-and-libraries.html", "สถานะวันนี้"),', 1),
    ]),

    # ---- สามประตูหน้าแรก ทั้งปลายทางของการ์ดและรายการในการ์ด ----
    (".tools/build_gates.py", [
        ('("Part 2 · Museums &amp; libraries", "MKM for Museums &amp; Libraries",\n'
         '         "mkm-for-museums-and-libraries.html",',
         '("Part 2 · Museums &amp; libraries", "MKM for Museums &amp; Libraries",\n'
         '         "exec-summary-museums.html",', 1),
        ('         [("mkm-for-museums-and-libraries.html", "01 · Where things stand"),',
         '         [("exec-summary-museums.html", "Executive summary"),\n'
         '          ("mkm-for-museums-and-libraries.html", "01 · Where things stand"),', 1),
        ('         "th-mkm-for-museums-and-libraries.html",',
         '         "th-exec-summary-museums.html",', 1),
        ('         [("th-mkm-for-museums-and-libraries.html", "01 · สถานะวันนี้"),',
         '         [("th-exec-summary-museums.html", "บทสรุปสำหรับผู้บริหาร"),\n'
         '          ("th-mkm-for-museums-and-libraries.html", "01 · สถานะวันนี้"),', 1),
    ]),

    # ---- ปลายทางของ breadcrumb ภาค 2 ----
    (".tools/build_jsonld.py", [
        ('    2: ("MKM for Museums & Libraries", "MKM สำหรับพิพิธภัณฑ์และห้องสมุด",\n'
         '        "mkm-for-museums-and-libraries.html"),',
         '    2: ("MKM for Museums & Libraries", "MKM สำหรับพิพิธภัณฑ์และห้องสมุด",\n'
         '        # หน้าแรกของภาค 2 คือ exec summary ตั้งแต่ 08-31 ไม่ใช่ 01 · สถานะวันนี้\n'
         '        "exec-summary-museums.html"),', 1),
    ]),
]

problems, moved = [], 0
for path, jobs in JOBS:
    p = ROOT / path
    s = before = p.read_text(encoding="utf-8")
    for old, new, want in jobs:
        if new and new in s:
            continue
        if not new and s.count(old) == 0:
            continue
        n = s.count(old)
        if n != want:
            problems.append(f"{path}: จุดยึดเจอ {n} ครั้ง ต้องเจอ {want} · {old[:60]}")
            continue
        s = s.replace(old, new)
        moved += 1
    if s != before:
        p.write_text(s, encoding="utf-8")
        print(f"  แก้ {path}")

if problems:
    sys.exit("ไม่ผ่าน\n" + "\n".join(problems))

# ---- สร้างใหม่ตามลำดับที่ห้ามสลับ ----
for tool in ("build_exec_summary.py", "build_gates.py", "build_footer.py"):
    subprocess.run([sys.executable, str(Path(__file__).with_name(tool))],
                   check=True, cwd=ROOT)

# ---- ด่านตรวจ มีครบ และ ไม่เหลือ ----
nav_en = (ROOT / ".tools/shell/nav.en.html").read_text(encoding="utf-8")
nav_th = (ROOT / ".tools/shell/nav.th.html").read_text(encoding="utf-8")
idx = (ROOT / "index.html").read_text(encoding="utf-8")
tidx = (ROOT / "th-index.html").read_text(encoding="utf-8")
ex = (ROOT / "exec-summary-museums.html").read_text(encoding="utf-8")
lead = (ROOT / "leadership.html").read_text(encoding="utf-8")

checks = {
    # มีครบ
    "EN หัวกลุ่มชี้หน้าใหม่": '<span class="hs"><a href="exec-summary-museums.html">' in nav_en,
    "TH หัวกลุ่มชี้หน้าใหม่": '<span class="hs"><a href="th-exec-summary-museums.html">' in nav_th,
    "EN อยู่หน้าสุดของกลุ่ม สองที่": nav_en.count(EN_ITEM + EN_FIRST) == 2,
    "TH อยู่หน้าสุดของกลุ่ม สองที่": nav_th.count(TH_ITEM + TH_FIRST) == 2,
    "EN ประตูที่สองชี้หน้าใหม่": 'href="exec-summary-museums.html"' in idx,
    "TH ประตูที่สองชี้หน้าใหม่": 'href="th-exec-summary-museums.html"' in tidx,
    "EN footer มีรายการนี้": 'href="exec-summary-museums.html"' in idx[idx.index("<footer"):],
    "หน้าอื่นในภาค 2 breadcrumb ชี้มาที่นี่":
        'href="exec-summary-museums.html">MKM for Museums' in lead
        or '"item": "https://www.neogens.co/exec-summary-museums.html"' in lead,
    "หน้านี้ breadcrumb เหลือสองขั้น": lead.count('class="crumbs"') == 1,
    # ไม่เหลือ
    "EN ไม่เหลือรายการซ้ำ": nav_en.count(EN_ITEM) == 2,
    "TH ไม่เหลือรายการซ้ำ": nav_th.count(TH_ITEM) == 2,
    "EN หัวกลุ่มไม่ชี้หน้าเดิมแล้ว":
        '<span class="hs"><a href="mkm-for-museums-and-libraries.html">' not in nav_en,
    "TH หัวกลุ่มไม่ชี้หน้าเดิมแล้ว":
        '<span class="hs"><a href="th-mkm-for-museums-and-libraries.html">' not in nav_th,
    "ป้ายเมนูไม่มีเลขนำ": "01 · Executive summary" not in nav_en,
}
bad = [k for k, ok in checks.items() if not ok]
if bad:
    sys.exit("[abort] " + " · ".join(bad))
print(f"✓ ย้ายแล้ว {moved} จุด · ตรวจผ่าน {len(checks)} ข้อ")
