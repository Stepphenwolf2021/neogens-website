#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เติมลิงก์หน้า SEO ลงใน footer ทุกหน้า   สั่งเมื่อ 2026-08-22

ตอนสร้างหน้านี้ ลิงก์ถูกใส่ไว้ในเมนูสไลด์อย่างเดียว แต่ปุ่มขีดสามขีดที่เปิดเมนูนั้น
โผล่เฉพาะจอแคบกว่า 1300px (ดู @media ใน CSS) จอกว้างกว่านั้นจึงเข้าหน้านี้ไม่ได้เลย
ไม่มีทั้งในแถบเมนูบน ในสามประตูหน้าแรก และใน footer

ตรวจแล้วหน้านี้เป็นหน้าเดียวในเว็บที่อยู่ใน drawer อย่างเดียว หน้าอื่นมีทางเข้าจาก
สามประตูหรือ footer เสมอ จึงเป็นของหลุด ไม่ใช่การออกแบบ

วางไว้ในคอลัมน์สุดท้ายของ footer ต่อจาก "เราคือใคร" ให้ตรงลำดับกับในเมนูสไลด์
ป้ายใช้คำเดียวกับในเมนู ไม่ได้ตั้งใหม่ สองที่จึงเรียกหน้าเดียวกันด้วยชื่อเดียวกัน

รันซ้ำได้ ลบของเดิมใน footer ก่อนแล้วค่อยใส่ใหม่
รันจากรากรีโป:  python3 .tools/add_evidence_footer.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ภาษา → (ลิงก์ที่ใช้ยึด, หน้าเป้าหมาย, ป้าย)  ป้ายยกมาจาก .tools/shell/nav.*.html
LANG = {
    "en": ('<a href="about.html">Who we are</a>',
           "seo-as-knowledge-management.html", "How we built this site"),
    "th": ('<a href="th-about.html">เราคือใคร</a>',
           "th-seo-as-knowledge-management.html", "เว็บนี้สร้างมาอย่างไร"),
}

# บทความยาวใช้ footer แบบแถบเดียวห้าลิงก์ ไม่มีคอลัมน์ ภาค 3 และบริษัท
# จึงไม่มีจุดยึด และไม่แตะ คนอ่านหน้านั้นกลับหน้าแรกแล้วเจอลิงก์ใน footer ปกติ
# ถ้าจะเติมด้วย ต้องตัดสินใจเรื่องหน้าตาแถบนั้นก่อน ไม่ใช่แทรกเงียบ ๆ
EXCEPT = {"long-read-museums-and-libraries.html"}

done, skipped, missing = [], [], []

for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")

    if "<footer" not in s or path.name in EXCEPT:   # ทางเบี่ยง · บทความยาว
        skipped.append(path.name)
        continue

    lang = "th" if path.name.startswith("th-") else "en"
    anchor, target, label = LANG[lang]
    link = f'<a href="{target}">{label}</a>'

    i = s.rfind("<footer")
    head, foot = s[:i], s[i:]

    foot = foot.replace(link, "")               # รันซ้ำได้ ไม่ซ้อนทับ

    if anchor not in foot:
        missing.append(path.name)
        continue

    foot = foot.replace(anchor, anchor + link, 1)
    s = head + foot

    if s != before:
        path.write_text(s, encoding="utf-8")
        done.append(path.name)

if missing:
    sys.exit("✗ หาจุดยึดใน footer ไม่เจอ: " + " · ".join(missing))

# ---- ด่านตรวจ ทั้งข้อ "มีครบ" และข้อ "ไม่เหลือ" (LESSONS ข้อ 10) ----
pages = [p for p in sorted(ROOT.glob("*.html"))
         if "<footer" in p.read_text(encoding="utf-8") and p.name not in EXCEPT]
checks = {}
for p in pages:
    s = p.read_text(encoding="utf-8")
    lang = "th" if p.name.startswith("th-") else "en"
    _, target, label = LANG[lang]
    i = s.rfind("<footer")
    foot, body = s[i:], s[:i]
    other = LANG["en" if lang == "th" else "th"][1]

    checks[f"{p.name} · footer มีลิงก์ 1 ชุด"] = foot.count(f'href="{target}"') == 1
    checks[f"{p.name} · footer ไม่หลุดไปอีกภาษา"] = f'href="{other}"' not in foot
    checks[f"{p.name} · footer ใช้ป้ายเดียวกับเมนู"] = foot.count(f">{label}</a>") == 1
    # นับจากป้าย ไม่ใช่จาก href เพราะบนหน้าตัวเอง href เดียวกันโผล่ในปุ่มสลับภาษาด้วย
    # และต้องนับในเมนูสไลด์เท่านั้น ตั้งแต่ add_nav_dropdown.py ป้ายเดียวกันโผล่บนแถบบนด้วย
    m = re.search(r'<div class="drawer".*?</div></div>', body, re.S)
    drawer = m.group(0) if m else ""
    checks[f"{p.name} · ยังมีในเมนูสไลด์เหมือนเดิม"] = drawer.count(f">{label}</a>") == 1

bad = [k for k, ok in checks.items() if not ok]
if bad:
    sys.exit("✗ ด่านตรวจไม่ผ่าน:\n  " + "\n  ".join(bad))

print(f"เติมลิงก์ใน footer แล้ว {len(done)} หน้า · ข้ามทางเบี่ยง {len(skipped)} ไฟล์")
print(f"ด่านตรวจผ่าน {len(checks)} ข้อ")
