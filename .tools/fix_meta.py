#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ย่อ <title> และ meta description ให้ไม่ถูกตัดในหน้าผลค้นหา   ข้อ 04 จากรายงานตรวจ

ของเดิมเอาประโยคพาดหัวของหน้ามาเป็น title ทั้งประโยค ยาวสุด 113 ตัวอักษร
Google ตัดที่ราว 60 คำที่อยู่หลังจุดตัดจึงไม่มีใครเห็น

title เขียนใหม่ทีละหน้า ใช้คำจากป้ายในเมนูที่มีอยู่แล้วทั้งสองภาษา
ไม่ตัดพาดหัวกลางประโยค เพราะลองแล้วความหมายเพี้ยน เช่น
"AI answers everything" ที่หายท่อน "and knows nothing" ไป กลายเป็นคนละเรื่อง

description ไม่เขียนใหม่ ตัดที่ท้ายประโยคเต็มให้อยู่ใน 155 ตัวอักษร
ภาษาไทยไม่มีเครื่องหมายจบประโยค จึงตัดที่ขอบวรรคแทน คำทุกคำยังเป็นคำเดิม

รันจากรากรีโป:  python3 .tools/fix_meta.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUF = " — Neo Gens"
T_MAX, D_MAX = 60, 155

TITLES = {
    "ai-sovereignty.html": "Your data · AI sovereignty",
    "contact.html": "Request a briefing",
    "engagement.html": "Engagement · how we work together",
    "leadership.html": "What leadership looks like",
    "long-read-museums-and-libraries.html": "Long read · MKM for museums & libraries",
    "mkm-for-museums-and-libraries.html": "MKM for Museums & Libraries",
    "ontology-and-knowledge-graph.html": "Ontology & knowledge graph",
    "reference-implementation.html": "Reference implementation",
    "services.html": "What we do together",
    "the-problem.html": "The problem · Modern Knowledge Management",
    "visitors-and-readers.html": "The new experience · modern knowledge management",
    "what-mkm-is.html": "What Modern Knowledge Management is",
    "what-you-are-holding.html": "What you are holding",
    "why-it-works.html": "Why it works · Modern Knowledge Management",
    "th-ai-sovereignty.html": "ข้อมูลของคุณ · AI Sovereignty",
    "th-contact.html": "ขอนัดหารือ",
    "th-engagement.html": "รูปแบบการทำงาน",
    "th-leadership.html": "ความเป็นผู้นำหน้าตาเป็นอย่างไร",
    "th-mkm-for-museums-and-libraries.html": "MKM สำหรับพิพิธภัณฑ์และห้องสมุด",
    "th-ontology-and-knowledge-graph.html": "ontology กับ knowledge graph",
    "th-reference-implementation.html": "งานอ้างอิงที่เราทำเอง",
    "th-services.html": "เราทำอะไรร่วมกัน",
    "th-the-problem.html": "ปัญหา · Modern Knowledge Management",
    "th-visitors-and-readers.html": "ประสบการณ์ใหม่ของการเรียนรู้ · MKM",
    "th-what-mkm-is.html": "Modern Knowledge Management คืออะไร",
    "th-what-you-are-holding.html": "สิ่งที่คุณถืออยู่",
    "th-why-it-works.html": "ทำไมมันถึงได้ผล · MKM",
}


def trim_desc(d):
    d = html.unescape(d).strip()
    if len(d) <= D_MAX:
        return None
    parts = re.split(r"(?<=[.!?])\s+", d)
    out = ""
    for p in parts:
        if len(out) + len(p) + 1 > D_MAX:
            break
        out = (out + " " + p).strip()
    if len(out) < 60:                      # ไทยไม่มีจุดจบประโยค ใช้ขอบวรรคแทน
        out = ""
        for w in d.split(" "):
            if len(out) + len(w) + 1 > D_MAX:
                break
            out = (out + " " + w).strip()
    return out or None


bad, t_fixed, d_fixed = [], 0, 0
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue

    if path.name in TITLES:
        new = TITLES[path.name] + SUF
        if len(new) > T_MAX:
            sys.exit(f"✗ title ของ {path.name} ยาว {len(new)} เกิน {T_MAX}")
        s = re.sub(r"<title>.*?</title>", f"<title>{new}</title>", s, count=1, flags=re.S)
        s = re.sub(r'(<meta property="og:title" content=")[^"]*"',
                   lambda m: m.group(1) + TITLES[path.name] + '"', s, count=1)
        t_fixed += 1

    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    if m:
        nd = trim_desc(m.group(1))
        if nd:
            esc = nd.replace('"', "&quot;")
            s = s.replace(f'content="{m.group(1)}"', f'content="{esc}"')
            # og:description ต้องตามกันเสมอ เป็นจุดที่ข้อความเก่าค้างบ่อย
            s = re.sub(r'(<meta property="og:description" content=")[^"]*"',
                       lambda x: x.group(1) + esc + '"', s, count=1)
            d_fixed += 1

    if s != before:
        path.write_text(s, encoding="utf-8")

for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue
    t = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1))
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    od = re.search(r'<meta property="og:description" content="([^"]*)"', s)
    if len(t) > T_MAX:
        bad.append(f"{path.name} title ยาว {len(t)}")
    if d and len(html.unescape(d.group(1))) > 160:
        bad.append(f"{path.name} description ยาว {len(d.group(1))}")
    if d and od and d.group(1) != od.group(1):
        bad.append(f"{path.name} og:description ไม่ตรงกับ description")

print(f"เขียน title ใหม่ {t_fixed} หน้า · ย่อ description {d_fixed} หน้า")
if bad:
    sys.exit("✗ " + "\n   ".join(bad[:10]))
print("✓ ทุกหน้า title ไม่เกิน 60 · description ไม่เกิน 160 · og:description ตรงกับ description")
