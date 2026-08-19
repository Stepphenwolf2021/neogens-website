#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ทำให้แถบเมนูมีต้นฉบับเดียวต่อภาษา   ข้อ 10 จากรายงานตรวจก่อนเปิดตัว

ปัญหาเดิมไม่ใช่แค่ว่าเมนูถูกคัดลอกไว้ 41 ชุด แต่คือ **ไม่มีชุดไหนเป็นต้นฉบับ**
ความผิดสองข้อที่เจอในรอบตรวจนี้เกิดจากการคัดลอกทั้งคู่
  · ปุ่มสลับภาษาฝั่งจอแคบของ 32 หน้าชี้ไปหน้าแรก ค้างมาจากแม่แบบ
  · hreflang ของหน้า about ชี้ไปหน้าอื่นทั้งสองภาษา

ต่อจากนี้แก้เมนูที่ .tools/shell/nav.en.html หรือ nav.th.html แล้วรันสคริปต์นี้
สิ่งที่ต่างกันได้ระหว่างหน้ามีสองอย่างเท่านั้น และสคริปต์ใส่ให้เอง
  1 ปุ่มสลับภาษา ชี้ระหว่างหน้านี้กับคู่ภาษาของมัน
  2 ตัวบ่งชี้หน้าปัจจุบัน class="on" กับ aria-current="page"

ด่านตรวจเทียบไฟล์ทั้งไฟล์นอกเขตเมนู ต้องเหมือนเดิมทุกไบต์ ถ้าไม่เหมือนจะไม่เขียน

รันจากรากรีโป:  python3 .tools/sync_nav.py            (ซิงก์จากต้นฉบับ)
                python3 .tools/sync_nav.py --extract  (ดึงต้นฉบับใหม่จากหน้าตัวอย่าง)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / ".tools" / "shell"
NAV = re.compile(r'<nav id="nav">.*?</nav>', re.S)
SOURCE = {"en": "about.html", "th": "th-about.html"}

# หน้าที่ยังไม่มีคู่ภาษา ให้ปุ่มสลับภาษาไปที่ใกล้เคียงที่สุด ตรงกับ .tools/fix_lang_switch.py
FALLBACK = {"long-read-museums-and-libraries.html": "th-index.html"}


def pages():
    for p in sorted(ROOT.glob("*.html")):
        s = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in s or p.name == "404.html":
            continue
        if NAV.search(s):
            yield p, s


def extract():
    SHELL.mkdir(parents=True, exist_ok=True)
    for lang, src in SOURCE.items():
        s = (ROOT / src).read_text(encoding="utf-8")
        nav = NAV.search(s).group(0)
        nav = re.sub(r'\sclass="on"\saria-current="page"', "", nav)
        nav = re.sub(r'\sclass="on"', "", nav)
        nav = re.sub(r'<span class="lang">.*?</span>(?=<button)', "{LANG}", nav, flags=re.S)
        (SHELL / f"nav.{lang}.html").write_text(nav, encoding="utf-8")
        print(f"  ดึงต้นฉบับ nav.{lang}.html จาก {src} · {len(nav)} ไบต์")


def lang_switch(name):
    th = name.startswith("th-")
    base = name[3:] if th else name
    en_page, th_page = base, "th-" + base
    if not (ROOT / th_page).exists():
        th_page = FALLBACK.get(base)
        if th_page is None:
            sys.exit(f"✗ {name} ไม่มีคู่ภาษา และไม่ได้ประกาศปลายทางสำรอง")
    if th:
        return (f'<span class="lang"><a class="on" aria-current="page" href="{th_page}">TH</a>'
                f'<span>/</span><a href="{en_page}">EN</a></span>')
    return (f'<span class="lang"><a class="on" aria-current="page" href="{en_page}">EN</a>'
            f'<span>/</span><a href="{th_page}">TH</a></span>')


def render(name, lang):
    nav = (SHELL / f"nav.{lang}.html").read_text(encoding="utf-8")
    if nav.count("{LANG}") != 2:
        sys.exit(f"✗ ต้นฉบับ nav.{lang}.html ควรมีจุดวางปุ่มสลับภาษา 2 จุด")
    nav = nav.replace("{LANG}", lang_switch(name))
    # ตัวบ่งชี้หน้าปัจจุบัน ใส่ให้ทุกลิงก์ที่ชี้มาที่หน้านี้
    nav = nav.replace(f'<a href="{name}">', f'<a class="on" aria-current="page" href="{name}">')
    nav = nav.replace(f'<a class="btn" href="{name}">',
                      f'<a class="btn on" aria-current="page" href="{name}">')
    return nav


if "--extract" in sys.argv:
    extract()
    sys.exit(0)

if not (SHELL / "nav.en.html").exists():
    extract()

changed, bad = 0, []
for path, s in pages():
    lang = "th" if path.name.startswith("th-") else "en"
    nav_old = NAV.search(s).group(0)
    nav_new = render(path.name, lang)
    if nav_old == nav_new:
        continue
    out = s.replace(nav_old, nav_new, 1)

    # ด่านตรวจ นอกเขตเมนูต้องไม่ขยับแม้แต่ไบต์เดียว
    if out.replace(nav_new, "", 1) != s.replace(nav_old, "", 1):
        bad.append(f"{path.name} มีอย่างอื่นนอกเมนูเปลี่ยนไปด้วย")
        continue
    path.write_text(out, encoding="utf-8")
    changed += 1

# ด่านรวม
for path, s in pages():
    nav = NAV.search(s).group(0)
    name = path.name
    if f'aria-current="page" href="{name}"' not in nav:
        bad.append(f"{name} ไม่มีตัวบ่งชี้หน้าปัจจุบันในเมนู")
    for h in set(re.findall(r'href="([^"#]+\.html)"', nav)):
        if not (ROOT / h).exists():
            bad.append(f"{name} เมนูชี้ไฟล์ที่ไม่มี {h}")
    if nav.count('<span class="lang">') != 2:
        bad.append(f"{name} ปุ่มสลับภาษาไม่ครบสองชุด")

print(f"ซิงก์เมนู {changed} หน้า จากต้นฉบับสองไฟล์ใน .tools/shell/")
if bad:
    sys.exit("✗ " + "\n   ".join(sorted(set(bad))[:8]))
print("✓ ทุกหน้าใช้เมนูชุดเดียวกัน · ตัวบ่งชี้หน้าปัจจุบันถูก · ไม่มีลิงก์ตายในเมนู")
