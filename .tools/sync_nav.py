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
        if ('http-equiv="refresh"' in s or 'data-standalone="notice"' in s
                or p.name == "404.html"):
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
        return (f'<span class="lang"><a class="on" href="{th_page}">TH</a>'
                f'<span>/</span><a href="{en_page}">EN</a></span>')
    return (f'<span class="lang"><a class="on" href="{en_page}">EN</a>'
            f'<span>/</span><a href="{th_page}">TH</a></span>')


def hs_spans(nav):
    """คืนช่วง (start, end) ของทุก <span class="hs"> โดยไล่นับ span ซ้อนชั้น

    ห้ามใช้ regex ตัดตรงนี้ ด้วยเหตุผลเดียวกับข้อ 11 ของ LESSONS.md
    เมนูย่อยอยู่ใน <span class="sub"> ที่ซ้อนอยู่ข้างใน regex non-greedy จะปิดเร็วไปหนึ่งชั้น
    """
    out = []
    for m in re.finditer(r'<span class="hs">', nav):
        depth, i = 0, m.start()
        while i < len(nav):
            if nav.startswith("<span", i):
                depth += 1
            elif nav.startswith("</span>", i):
                depth -= 1
                if depth == 0:
                    out.append((m.start(), i + len("</span>")))
                    break
            i += 1
        else:
            sys.exit("✗ <span class=\"hs\"> ปิดไม่ครบในต้นฉบับเมนู")
    return out


def mark_group_head(nav, name):
    """หัวกลุ่มบนแถบเมนูติดสีเข้มทุกหน้าในภาคนั้น ไม่ใช่เฉพาะหน้าแรกของกลุ่ม

    ใช้ class="on" ตัวเดิม จึงไม่ต้องเพิ่มกฎ CSS ใหม่ และไม่ต้องตั้งชื่อคลาสใหม่ให้ชนของเดิม
    ไม่ใส่ aria-current ให้หัวกลุ่ม เพราะหัวกลุ่มไม่ใช่หน้าที่เปิดอยู่ เป็นแค่ตัวบอกว่าอยู่ภาคไหน
    """
    for start, end in reversed(hs_spans(nav)):
        block = nav[start:end]
        sub = block[block.index('<span class="sub">'):] if '<span class="sub">' in block else ""
        if f'href="{name}"' not in sub:
            continue
        head = re.search(r"<a\b[^>]*>", block)
        if head is None or 'class="on"' in head.group(0):
            continue
        new_head = head.group(0).replace("<a ", '<a class="on" ', 1)
        nav = nav[:start] + block[:head.start()] + new_head + block[head.end():] + nav[end:]
    return nav


def render(name, lang):
    nav = (SHELL / f"nav.{lang}.html").read_text(encoding="utf-8")
    if nav.count("{LANG}") != 2:
        sys.exit(f"✗ ต้นฉบับ nav.{lang}.html ควรมีจุดวางปุ่มสลับภาษา 2 จุด")
    nav = nav.replace("{LANG}", lang_switch(name))
    # ตัวบ่งชี้สายตา ใส่ให้ทุกลิงก์ที่ชี้มาที่หน้านี้
    nav = nav.replace(f'<a href="{name}">', f'<a class="on" href="{name}">')
    nav = nav.replace(f'<a class="btn" href="{name}">', f'<a class="btn on" href="{name}">')
    nav = mark_group_head(nav, name)
    # aria-current="page" มีได้อันเดียวต่อหน้า ใส่ให้ลิงก์ตัวเองตัวแรกในเมนู
    first = re.search(rf'<a class="(?:btn )?on" href="{re.escape(name)}">', nav)
    if first:
        tag = first.group(0).replace(' href=', ' aria-current="page" href=', 1)
        nav = nav[:first.start()] + tag + nav[first.end():]
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
    # ตัวบ่งชี้สถานะต้องตรวจสามข้อ ไม่ใช่ข้อเดียว  ดูข้อ 12 ของ LESSONS.md
    if f'aria-current="page" href="{name}"' not in nav:
        bad.append(f"{name} ไม่มีตัวบ่งชี้หน้าปัจจุบันในเมนู")
    n_ac = nav.count('aria-current="page"')
    if n_ac != 1:
        bad.append(f"{name} มีตัวบ่งชี้หน้าปัจจุบัน {n_ac} อันในเมนู ต้องมีอันเดียว")
    # หน้าที่อยู่ในกลุ่มเดียวกัน หัวกลุ่มต้องติดเท่ากันทุกหน้า ไม่ใช่เฉพาะหน้าแรกของกลุ่ม
    for start, end in hs_spans(nav):
        block = nav[start:end]
        sub = block[block.index('<span class="sub">'):] if '<span class="sub">' in block else ""
        head = re.search(r"<a\b[^>]*>", block)
        if head is None:
            continue
        in_group = f'href="{name}"' in sub
        marked = 'class="on"' in head.group(0)
        if in_group != marked:
            label = re.sub(r"<[^>]+>", "", block[head.end():block.find("</a>", head.end())])[:24]
            bad.append(f"{name} หัวกลุ่ม «{label}» อยู่ในกลุ่ม={in_group} แต่ติดสี={marked}")
    for h in set(re.findall(r'href="([^"#]+\.html)"', nav)):
        if not (ROOT / h).exists():
            bad.append(f"{name} เมนูชี้ไฟล์ที่ไม่มี {h}")
    if nav.count('<span class="lang">') != 2:
        bad.append(f"{name} ปุ่มสลับภาษาไม่ครบสองชุด")

print(f"ซิงก์เมนู {changed} หน้า จากต้นฉบับสองไฟล์ใน .tools/shell/")
if bad:
    sys.exit("✗ " + "\n   ".join(sorted(set(bad))[:8]))
print("✓ ทุกหน้าใช้เมนูชุดเดียวกัน · ตัวบ่งชี้หน้าปัจจุบันถูก · ไม่มีลิงก์ตายในเมนู")
