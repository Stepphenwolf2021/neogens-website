#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เปลี่ยนชื่อไฟล์หน้าเว็บให้ตรงกับเนื้อหา · ตกลงกันไว้ 2026-08-19

ของเดิมหลายชื่อมาจากคำที่อยู่ในหน้าอื่น ไม่ได้มาจากเนื้อหาของหน้านั้นเอง
ที่สับสนที่สุดคือ visit.html เป็นหน้าเปิดภาคพิพิธภัณฑ์ ส่วน museums.html
เป็นหน้าเรื่องความเป็นผู้นำ คนเดาสลับกันตลอด

ทำสี่อย่าง
  1 git mv ทั้งคู่ไทย-อังกฤษ ประวัติไฟล์ไม่ขาด
  2 ไล่แก้ลิงก์ในไฟล์ html ทุกไฟล์ · sitemap.xml · สคริปต์ใน .tools
  3 วางไฟล์ stub ไว้ที่ชื่อเดิมทุกชื่อ เด้งไปชื่อใหม่พร้อม canonical และ noindex
    ตามแบบเดียวกับ km-for-museums.html ที่มีอยู่ก่อนแล้ว
  4 ด่านตรวจท้ายสคริปต์ ถ้าเหลือลิงก์ชื่อเก่าหรือมีลิงก์ตายจะ exit

URL เดิมที่เคยแชร์ออกไปและที่ Google เก็บไว้ยังใช้ได้ต่อ เพราะ stub รับไว้
GitHub Pages ทำ redirect ฝั่งเซิร์ฟเวอร์ไม่ได้ จึงต้องเป็น stub เท่านั้น

รันจากรากรีโป:  python3 .tools/rename_pages.py
"""
import re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ชื่อฐาน เดิม → ใหม่ (ฉบับไทยเติม th- ให้อัตโนมัติถ้าไฟล์มีอยู่)
RENAMES = {
    "mkm-for-museums-and-libraries.html":                        "mkm-for-museums-and-libraries.html",
    "mkm-for-coffee.html":                       "mkm-for-coffee.html",
    "leadership.html":                      "leadership.html",
    "visitors-and-readers.html":                   "visitors-and-readers.html",
    "ontology-and-knowledge-graph.html":                        "ontology-and-knowledge-graph.html",
    "what-you-are-holding.html":                    "what-you-are-holding.html",
    "what-we-wont-do.html":                       "what-we-wont-do.html",
    "ai-sovereignty.html":                  "ai-sovereignty.html",
    "what-mkm-is.html":                         "what-mkm-is.html",
    "why-it-works.html":                          "why-it-works.html",
    "the-problem.html":                      "the-problem.html",
    "reference-implementation.html":                        "reference-implementation.html",
    "long-read-museums-and-libraries.html": "long-read-museums-and-libraries.html",
}

# ข้อความบน stub ต่อชื่อใหม่ · อังกฤษกับไทยคนละสำนวน
LABEL = {
    "mkm-for-museums-and-libraries.html": ("MKM for Museums &amp; Libraries", "MKM สำหรับพิพิธภัณฑ์และห้องสมุด"),
    "mkm-for-coffee.html":                ("MKM for Coffee", "MKM สำหรับกาแฟ"),
    "leadership.html":                    ("What leadership looks like", "ความเป็นผู้นำหน้าตาเป็นอย่างไร"),
    "visitors-and-readers.html":          ("Visitors and readers", "ผู้ชมและผู้อ่าน"),
    "ontology-and-knowledge-graph.html":  ("Ontology &amp; knowledge graph", "ontology และ knowledge graph"),
    "what-you-are-holding.html":          ("What you are holding", "สิ่งที่คุณถืออยู่ในมือ"),
    "what-we-wont-do.html":               ("What we won't do", "สิ่งที่เราไม่ทำ"),
    "ai-sovereignty.html":                ("Your data · AI sovereignty", "ข้อมูลของคุณ · AI Sovereignty"),
    "what-mkm-is.html":                   ("What it is", "MKM คืออะไร"),
    "why-it-works.html":                  ("Why it works", "ทำไมมันได้ผล"),
    "the-problem.html":                   ("The problem", "ปัญหา"),
    "reference-implementation.html":      ("Reference implementation", "งานอ้างอิงที่เราทำเอง"),
    "long-read-museums-and-libraries.html": ("MKM for museums &amp; libraries — long read", "บทความยาว MKM สำหรับพิพิธภัณฑ์และห้องสมุด"),
}

STUB = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{moved} — Neo Gens</title>
<link rel="canonical" href="https://www.neogens.co/{new}">
<meta http-equiv="refresh" content="0; url=/{new}">
<meta name="robots" content="noindex, follow">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>
html{{background:#08090A;color:#A2A8AF;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
body{{display:flex;min-height:100vh;align-items:center;justify-content:center;margin:0;padding:24px;text-align:center;line-height:1.75}}
a{{color:#B8F04A}}
</style>
<script>location.replace('/{new}'+location.hash);</script>
</head>
<body>
<p>{sentence} <a href="/{new}">{label}</a>.</p>
</body>
</html>
"""

# ---------------------------------------------------------------- สร้างแผนที่เต็ม

pairs = {}
for old, new in RENAMES.items():
    if not (ROOT / old).exists():
        sys.exit(f"✗ ไม่มีไฟล์ {old}")
    pairs[old] = new
    if (ROOT / ("th-" + old)).exists():
        pairs["th-" + old] = "th-" + new

for new in pairs.values():
    if (ROOT / new).exists():
        sys.exit(f"✗ {new} มีอยู่แล้ว ยังไม่ได้แตะอะไร")

# ---------------------------------------------------------------- 1 · git mv

for old, new in pairs.items():
    r = subprocess.run(["git", "--no-optional-locks", "mv", old, new],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"✗ git mv {old} ล้มเหลว: {r.stderr.strip()}")
print(f"1 · เปลี่ยนชื่อ {len(pairs)} ไฟล์ด้วย git mv")

# ---------------------------------------------------------------- 2 · แก้ลิงก์

edited = 0
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    for old, new in pairs.items():
        s = s.replace(f'"{old}"', f'"{new}"')          # href / ตาราง hash
        s = s.replace(f'/{old}"', f'/{new}"')           # ลิงก์แบบมี /
        s = s.replace(f'.co/{old}', f'.co/{new}')       # url เต็มใน meta
    if s != before:
        path.write_text(s, encoding="utf-8"); edited += 1

sm = ROOT / "sitemap.xml"
s = sm.read_text(encoding="utf-8")
for old, new in pairs.items():
    s = s.replace(f'.co/{old}', f'.co/{new}')
sm.write_text(s, encoding="utf-8")

tools = 0
for path in sorted((ROOT / ".tools").rglob("*.py")):
    s = before = path.read_text(encoding="utf-8")
    for old, new in pairs.items():
        s = s.replace(f'"{old}"', f'"{new}"').replace(f"'{old}'", f"'{new}'")
    if s != before:
        path.write_text(s, encoding="utf-8"); tools += 1
print(f"2 · แก้ลิงก์ใน {edited} ไฟล์ html · sitemap.xml · สคริปต์ {tools} ตัว")

# ---------------------------------------------------------------- 3 · stub

for old, new in pairs.items():
    th = old.startswith("th-")
    label = LABEL[new[3:] if th else new][1 if th else 0]
    (ROOT / old).write_text(STUB.format(
        lang="th" if th else "en", new=new, label=label,
        moved="ย้ายแล้ว" if th else "Moved",
        sentence="หน้านี้ย้ายไปอยู่ที่" if th else "This page now lives at",
    ), encoding="utf-8")
print(f"3 · วาง stub ไว้ที่ชื่อเดิม {len(pairs)} ไฟล์")

# ---------------------------------------------------------------- 4 · ด่านตรวจ

bad, stubs = [], set(pairs)
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if path.name in stubs:
        want = pairs[path.name]
        if s.count(want) != 4:
            bad.append(f"{path.name} stub ชี้ปลายทางไม่ครบสี่ที่")
        continue
    for old in pairs:
        if re.search(r'href="/?' + re.escape(old) + r'"', s):
            bad.append(f"{path.name} ยังลิงก์ไปชื่อเก่า {old}")
    for h in set(re.findall(r'href="(?!https?:|mailto:|#)/?([^"#?]+\.html)', s)):
        if not (ROOT / h).exists():
            bad.append(f"{path.name} ลิงก์ตาย {h}")

s = sm.read_text(encoding="utf-8")
for old in pairs:
    if f".co/{old}" in s:
        bad.append(f"sitemap ยังมีชื่อเก่า {old}")
for loc in re.findall(r'<loc>https://www\.neogens\.co/([^<]+)</loc>', s):
    if not (ROOT / loc).exists():
        bad.append(f"sitemap ชี้ไฟล์ที่ไม่มี {loc}")

print(f"4 · ตรวจแล้ว {len(list(ROOT.glob('*.html')))} ไฟล์")
if bad:
    sys.exit("✗ ด่านตรวจไม่ผ่าน:\n   " + "\n   ".join(sorted(set(bad))[:25]))
print("✓ ไม่มีลิงก์ชื่อเก่าค้าง · ไม่มีลิงก์ตาย · sitemap ตรงกับไฟล์จริง")
