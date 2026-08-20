#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เพิ่มแถบ breadcrumb ที่คนมองเห็นได้ ให้ตรงกับ BreadcrumbList ใน JSON-LD

ก่อนหน้านี้เว็บมี BreadcrumbList อยู่ 33 หน้า แต่ไม่มีหน้าไหนแสดงเส้นทางนั้นให้คนเห็นเลย
คือมีร่องรอยที่บอกเครื่อง แต่ไม่มีร่องรอยที่บอกคน คนที่เปิดหน้ากลางเว็บมาจากผลค้นหา
จึงต้องเดาเองว่าตัวเองอยู่ตรงไหนของเว็บ

ข้อความและลิงก์ **ดึงจาก JSON-LD ของหน้านั้นเอง** ไม่ได้เขียนใหม่
สองอย่างจึงตรงกันโดยโครงสร้าง ไม่ใช่โดยความตั้งใจของคนแก้

แทรกไว้ก่อนบรรทัดป้ายหมวดที่ต้น hero ซึ่งเป็นจุดยึดที่มีทั้งสองโครงหน้าที่เว็บนี้ใช้
  แบบ kicker   7 หน้า
  แบบ eyebrow  26 หน้า

ขั้นสุดท้ายของเส้นทางคือหน้าปัจจุบัน จึงไม่ทำเป็นลิงก์ และใส่ aria-current="page"
ตัวคั่น › วางด้วย CSS ::before โปรแกรมอ่านหน้าจอจึงไม่อ่านมันออกมาเป็นข้อความ

รันจากรากรีโป:  python3 .tools/add_breadcrumbs.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.neogens.co/"

CSS = """
/* --- เส้นทางที่คนมองเห็น ตรงกับ BreadcrumbList ใน JSON-LD --- */
.crumbs{{margin-bottom:14px}}
.crumbs ol{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;
  font-family:var(--mono);font-size:11px;letter-spacing:{ls};line-height:1.9;color:var(--mute)}}
.crumbs li+li::before{{content:"\\203a";margin:0 7px;opacity:.65}}
.crumbs a{{color:var(--mute);text-decoration:none;transition:color .2s}}
.crumbs a:hover{{color:var(--go)}}
.crumbs [aria-current]{{color:var(--dim)}}
"""

ANCHOR = re.compile(r'<div class="(?:kicker|eyebrow[^"]*)">')
BLOCK = re.compile(r'[ \t]*<nav class="crumbs".*?</nav>\n', re.S)

done, skipped = [], []
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if "BreadcrumbList" not in s:
        skipped.append(path.name)
        continue

    graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',
                                 s, re.S).group(1))["@graph"]
    bc = next(n for n in graph if n.get("@type") == "BreadcrumbList")
    items = sorted(bc["itemListElement"], key=lambda x: x["position"])
    me = BASE if path.name == "index.html" else BASE + path.name

    lis = []
    for it in items:
        name = html.escape(it["name"])
        url = it.get("item") or ""
        if url == me:                       # ขั้นสุดท้ายคือหน้านี้ ไม่ทำเป็นลิงก์
            lis.append(f'<li aria-current="page">{name}</li>')
        else:
            lis.append(f'<li><a href="{url.replace(BASE, "") or "index.html"}">{name}</a></li>')
    nav = ('<nav class="crumbs" aria-label="Breadcrumb"><ol>'
           + "".join(lis) + "</ol></nav>\n")

    s = BLOCK.sub("", s)                    # รันซ้ำได้ ไม่ซ้อนทับ
    # ปกติแทรกก่อนป้ายบนหัวหน้า · หน้าที่ตัดป้ายทิ้งไปแล้วให้ยึดกับ <h1> แทน
    m = ANCHOR.search(s, s.index("<main"))
    if not m or m.start() > s.index("<h1"):
        m = re.compile(r"<h1").search(s, s.index("<main"))
    if not m:
        sys.exit(f"✗ {path.name} หาจุดยึดไม่เจอ")
    s = s[:m.start()] + nav + s[m.start():]

    if ".crumbs ol{" not in s:
        lang = "th" if path.name.startswith("th-") else "en"
        s = s.replace("</style>", CSS.format(ls="0" if lang == "th" else ".08em") + "</style>", 1)

    # ---- ด่านตรวจ เทียบกับกราฟทีละขั้น ----
    vis = re.search(r'<nav class="crumbs".*?</nav>', s, re.S).group(0)
    names = [html.unescape(x) for x in re.findall(r'<li[^>]*>(?:<a[^>]*>)?([^<]*)', vis)]
    checks = {
        "จำนวนขั้นตรงกับกราฟ": len(names) == len(items),
        "ข้อความตรงกันทุกขั้น": names == [i["name"] for i in items],
        "ขั้นสุดท้ายไม่ใช่ลิงก์": vis.count('aria-current="page"') == 1
                                  and vis.rindex("<li") > (vis.rindex("</a>") if "</a>" in vis else -1),
        "ลิงก์ทุกเส้นมีไฟล์จริง": all((ROOT / h).exists()
                                      for h in re.findall(r'<a href="([^"]+)"', vis)),
        "แถบเดียวต่อหน้า": s.count('<nav class="crumbs"') == 1,
        "อยู่ก่อนพาดหัว": s.index('class="crumbs"') < s.index("<h1"),
        "อยู่ใน main": s.index("<main") < s.index('class="crumbs"'),
        "CSS เข้าไฟล์": ".crumbs ol{" in s and s.index(".crumbs ol{") < s.index("</style>"),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {path.name}: " + " · ".join(bad))
    path.write_text(s, encoding="utf-8")
    done.append(path.name)

print(f"เพิ่มแถบเส้นทาง {len(done)} หน้า · ไม่มี BreadcrumbList จึงข้าม {len(skipped)} หน้า")
print("✓ ข้อความและลิงก์ทุกขั้นตรงกับ JSON-LD ของหน้านั้นเอง")
