#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ย้ายฟอนต์จาก Google Fonts มาไว้บนโดเมนตัวเอง   ข้อ 05 จากรายงานตรวจก่อนเปิดตัว

เหตุผลสามข้อ
  1 ความเป็นส่วนตัว ทุกหน้าเรียก fonts.googleapis.com แปลว่า Google ได้รับ IP ของผู้อ่าน
    ตั้งแต่ก่อนเขาได้อ่านย่อหน้าแรก บนเว็บที่มีหน้าชื่อ ข้อมูลของคุณ · AI Sovereignty
  2 ความเร็ว ตัดการเชื่อมต่อไปโดเมนอื่นสองแห่ง และตัด CSS ที่ขวางการเรนเดอร์หนึ่งชั้น
  3 ความแน่นอน ฟอนต์อยู่ในรีโป จะไม่หายไปเพราะบริการภายนอกเปลี่ยนเงื่อนไข

เก็บเฉพาะชุดอักขระที่เว็บนี้ใช้จริง คือ latin · latin-ext · thai
ตัด cyrillic greek vietnamese ออก เพราะไม่มีข้อความภาษาเหล่านั้นในเว็บ

ทั้งสี่ตระกูลอยู่ใต้ SIL Open Font License 1.1 ซึ่งอนุญาตให้โฮสต์เองได้
บันทึกที่มาไว้ใน assets/fonts/LICENSES.txt

รันจากรากรีโป:  python3 .tools/selfhost_fonts.py
"""
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "fonts"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")
KEEP = {"latin", "latin-ext", "thai"}

FAMILIES = ("family=IBM+Plex+Sans+Thai:wght@400;500;600;700"
            "&family=Inter:wght@400;500;600;700"
            "&family=Instrument+Serif:ital@0;1"
            "&family=JetBrains+Mono:wght@400;500")


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read() if binary else r.read().decode("utf-8")


print("1/4  ดึงรายการ @font-face จาก Google")
css = get(f"https://fonts.googleapis.com/css2?{FAMILIES}&display=swap")

blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", css)
if not blocks:
    sys.exit("✗ ดึง CSS ไม่ได้หรือรูปแบบเปลี่ยนไป ยังไม่ได้แตะอะไร")
kept = [(sub, b) for sub, b in blocks if sub in KEEP]
print(f"     ทั้งหมด {len(blocks)} face · เก็บไว้ {len(kept)} face "
      f"({', '.join(sorted(KEEP))})")

print("2/4  ดาวน์โหลดไฟล์ woff2")
OUT.mkdir(parents=True, exist_ok=True)
out_css, total = [], 0
for sub, block in kept:
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    wght = re.search(r"font-weight:\s*(\d+)", block).group(1)
    style = re.search(r"font-style:\s*(\w+)", block).group(1)
    url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
    name = f"{fam.replace(' ', '')}-{wght}{'i' if style == 'italic' else ''}-{sub}.woff2"
    data = get(url, binary=True)
    (OUT / name).write_bytes(data)
    total += len(data)
    out_css.append(block.replace(url, f"/assets/fonts/{name}"))
print(f"     {len(kept)} ไฟล์ · รวม {total // 1024} KB")

(OUT / "fonts.css").write_text(
    "/* ฟอนต์ของ neogens.co · โฮสต์เอง ไม่เรียกโดเมนภายนอก\n"
    "   สร้างด้วย .tools/selfhost_fonts.py · เก็บเฉพาะชุดอักขระ latin, latin-ext, thai\n"
    "   ทั้งสี่ตระกูลอยู่ใต้ SIL Open Font License 1.1 ดู LICENSES.txt */\n\n"
    + "\n\n".join(out_css) + "\n", encoding="utf-8")

(OUT / "LICENSES.txt").write_text(
    "Fonts served from this directory\n"
    "================================\n\n"
    "Inter                — SIL Open Font License 1.1 — https://github.com/rsms/inter\n"
    "Instrument Serif     — SIL Open Font License 1.1 — https://github.com/Instrument/instrument-serif\n"
    "JetBrains Mono       — SIL Open Font License 1.1 — https://github.com/JetBrains/JetBrainsMono\n"
    "IBM Plex Sans Thai   — SIL Open Font License 1.1 — https://github.com/IBM/plex\n\n"
    "Downloaded from Google Fonts and re-hosted on neogens.co so that no reader's\n"
    "IP address is sent to a third party in order to render this site.\n",
    encoding="utf-8")

print("3/4  เปลี่ยนหน้าเว็บให้เรียกจากโดเมนตัวเอง")
LINKS = re.compile(
    r'[ \t]*<link rel="preconnect" href="https://fonts\.googleapis\.com">\n'
    r'[ \t]*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
    r'[ \t]*<link href="https://fonts\.googleapis\.com/css2[^"]*" rel="stylesheet">\n')
NEW = '<link rel="stylesheet" href="/assets/fonts/fonts.css">\n'

changed = 0
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    s, n = LINKS.subn(NEW, s)
    if n:
        path.write_text(s, encoding="utf-8")
        changed += 1
print(f"     {changed} หน้า")

print("4/4  ตรวจ")
left = [p.name for p in ROOT.glob("*.html")
        if "fonts.googleapis.com" in p.read_text(encoding="utf-8")
        or "fonts.gstatic.com" in p.read_text(encoding="utf-8")]
fonts_css = (OUT / "fonts.css").read_text(encoding="utf-8")
missing = [m for m in re.findall(r"url\(/assets/fonts/([^)]+)\)", fonts_css)
           if not (OUT / m).exists()]
fams = set(re.findall(r"font-family:\s*'([^']+)'", fonts_css))

checks = {
    "ไม่มีหน้าไหนเรียก Google Fonts แล้ว": not left,
    "ทุก url ในไฟล์ CSS มีไฟล์จริง": not missing,
    "ครบสี่ตระกูล": len(fams) == 4,
    "มีชุดอักขระไทย": any("thai" in n for n in re.findall(r"url\(/assets/fonts/([^)]+)\)", fonts_css)),
    "มีตัวเอียงของ Instrument Serif": "font-style: italic" in fonts_css,
    # หน้า stub ที่เด้งไปชื่อใหม่ไม่ได้โหลดฟอนต์ เพราะแสดงข้อความบรรทัดเดียว
    "ทุกหน้าจริงชี้ไฟล์ CSS ของเราเอง": all(
        "/assets/fonts/fonts.css" in p.read_text(encoding="utf-8")
        for p in ROOT.glob("*.html")
        if 'http-equiv="refresh"' not in p.read_text(encoding="utf-8")),
}
bad = [k for k, ok in checks.items() if not ok]
if bad:
    sys.exit("✗ " + " · ".join(bad) + (f" · ยังเหลือ: {left[:5]}" if left else ""))
print("     ✓ " + " · ".join(f"{k}" for k in checks))
print(f"\nเสร็จ · {len(kept)} ไฟล์ · {total // 1024} KB · {', '.join(sorted(fams))}")
