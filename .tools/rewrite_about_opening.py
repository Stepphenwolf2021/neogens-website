#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เปลี่ยนหัวหน้า about ทั้งสองภาษา · 2026-09-01

สั่งโดย Noppadol  ถอดภาพ ดาราศาสตร์ กับ ห้องประวัติศาสตร์พื้นถิ่น ออก
แล้วแทนด้วยข้อความที่เป็นกลาง ไม่ผูกกับพิพิธภัณฑ์ สิ่งที่หน้านี้ต้องสื่อคือ
Neo Gens เป็นทีมที่ทำงานกับการใช้ AI · ontology · knowledge graph
บริหารจัดการความรู้ขององค์กร เพื่อให้องค์กรเดินไปถึงกลยุทธ์และพันธกิจที่ตั้งไว้

ย่อหน้าที่สาม การจะลากเส้นแบบนี้… ขึ้นต้นด้วยคำว่า เส้น อยู่แล้ว
ข้อความใหม่จึงต้องวางคำว่า เส้น ไว้ให้ ไม่งั้นย่อหน้าถัดไปจะอ้างถึงสิ่งที่ไม่มี

ฉบับไทยเขียนขึ้นใหม่จากความคิด ไม่ได้แปลจากอังกฤษ ตามสกิล neogens-thai-voice
รันซ้ำได้  รันจากรากรีโป:  python3 .tools/rewrite_about_opening.py
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EN_OLD_H1 = ("What finally makes astronomy land with a visitor may not be in the astronomy "
             "gallery. It may be two rooms away, in local history.")
EN_NEW_H1 = ("The knowledge an organisation needs in order to deliver its mission is rarely "
             "in one place.")
EN_OLD_LEDE = """      And usually nobody in the organisation can see that line. The two rooms sit in different departments,
      use different vocabularies, and nothing anywhere records that they are related at all."""
EN_NEW_LEDE = """      It sits in different departments, built at different times, each with its own vocabulary,
      and nothing anywhere records that the pieces are related. The line between them is real.
      Usually nobody in the organisation can see it, and the work the strategy depends on quietly
      does not happen."""
EN_OLD_TITLE = "What makes astronomy land may be two rooms away — Neo Gens"
EN_NEW_TITLE = "Who we are — Neo Gens"
EN_NEW_DESC = ("The knowledge an organisation needs to deliver its mission is rarely in one place. "
               "We use AI, ontology and knowledge graphs to draw the lines between them.")

TH_OLD_H1 = ("สิ่งที่จะทำให้คนเข้าใจดาราศาสตร์ อาจไม่ได้อยู่ในห้องดาราศาสตร์ "
             "แต่อยู่ในห้องประวัติศาสตร์พื้นถิ่นที่อยู่ถัดไปสองห้อง")
TH_NEW_H1 = "ความรู้ที่ทำให้พันธกิจขององค์กรเดินได้จริง มักไม่ได้อยู่รวมกันที่เดียว"
TH_OLD_LEDE = """      และมักไม่มีใครในองค์กรมองเห็นเส้นนั้น เพราะสองห้องอยู่คนละฝ่าย ใช้คำศัพท์คนละชุด
      และไม่เคยมีใครเขียนไว้ว่ามันเกี่ยวกันตรงไหน"""
TH_NEW_LEDE = """      มันกระจายอยู่คนละฝ่าย สร้างขึ้นคนละเวลา ใช้คำศัพท์คนละชุด
      และไม่เคยมีใครเขียนไว้ว่าชิ้นไหนเกี่ยวกับชิ้นไหน เส้นที่เชื่อมกันมีอยู่จริง
      แต่มักไม่มีใครในองค์กรมองเห็น งานที่กลยุทธ์ต้องพึ่งจึงเงียบหายไปเฉย ๆ"""
TH_NEW_DESC = ("ความรู้ที่ทำให้พันธกิจขององค์กรเดินได้จริง มักไม่ได้อยู่รวมกันที่เดียว "
               "เราใช้ AI ontology และ knowledge graph ลากเส้นระหว่างชิ้นส่วนเหล่านั้น")

JOBS = [
    # ลำดับสำคัญ · ข้อความใน meta เป็นประโยคเดียวกับ h1 ทุกตัวอักษร
    # ถ้าแทน h1 ก่อน ตัวใน meta จะถูกแทนไปด้วย แล้วคู่ของ meta จะหาไม่เจอ
    ("about.html", [
        (f"<title>{EN_OLD_TITLE}</title>", f"<title>{EN_NEW_TITLE}</title>"),
        (f'<meta property="og:title" content="{EN_OLD_TITLE}">',
         f'<meta property="og:title" content="{EN_NEW_TITLE}">'),
        (f'<meta name="description" content="{EN_OLD_H1}">',
         f'<meta name="description" content="{EN_NEW_DESC}">'),
        (f'<meta property="og:description" content="{EN_OLD_H1}">',
         f'<meta property="og:description" content="{EN_NEW_DESC}">'),
        (EN_OLD_LEDE, EN_NEW_LEDE),
        (EN_OLD_H1, EN_NEW_H1),
    ]),
    ("th-about.html", [
        (f'<meta name="description" content="{TH_OLD_H1}">',
         f'<meta name="description" content="{TH_NEW_DESC}">'),
        (f'<meta property="og:description" content="{TH_OLD_H1}">',
         f'<meta property="og:description" content="{TH_NEW_DESC}">'),
        (TH_OLD_LEDE, TH_NEW_LEDE),
        (TH_OLD_H1, TH_NEW_H1),
    ]),
]

BANNED = ["astronomy", "ดาราศาสตร์", "two rooms", "สองห้อง", "local history",
          "ประวัติศาสตร์พื้นถิ่น", "gallery"]

for fname, pairs in JOBS:
    p = ROOT / fname
    s = io.open(p, encoding="utf-8").read()
    orig = s
    hits = 0
    for old, new in pairs:
        n = s.count(old)
        if n == 0:
            if new in s:            # รันซ้ำ
                hits += 1
                continue
            sys.exit(f"✗ {fname} หาข้อความเดิมไม่เจอ: {old[:60]}")
        s = s.replace(old, new)
        hits += n

    body = s[s.index("<main"):s.index("</main>")]
    checks = {
        "ข้อความใหม่เข้าครบ": all(new in s for _, new in pairs),
        "ไม่เหลือภาพเดิมในเนื้อหา": not any(b in body for b in BANNED),
        "ย่อหน้าถัดไปยังมีคำว่า เส้น ให้อ้างถึง":
            ("The line between them" in body and "Drawing that line" in body)
            if fname == "about.html"
            else ("เส้นที่เชื่อมกันมีอยู่จริง" in body and "การจะลากเส้นแบบนี้" in body),
        "แท็กสมดุล": s.count("<div") == s.count("</div>")
                     and len(re.findall(r"<p\b", s)) == s.count("</p>"),
        "h1 มีตัวเดียว": s.count("<h1") == 1,
        "โครงหน้ายังครบ": all(x in s for x in ["<h1", 'class="lede', "</footer>",
                                               "Neo Gens"]),
        "ไม่หดผิดปกติ": abs(len(s) - len(orig)) < 1200,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {fname} ไม่ผ่าน: " + " · ".join(bad))
    io.open(p, "w", encoding="utf-8").write(s)
    print(f"  เขียนใหม่ {fname:16} · แทนที่ {hits} จุด · {len(s)-len(orig):+d} ตัวอักษร")

print("✓ หัวหน้า about เป็นกลาง ไม่ผูกกับพิพิธภัณฑ์แล้ว ทั้งสองภาษา")
print("  ต่อด้วย  python3 .tools/build_jsonld.py   เพื่อให้ JSON-LD ตามชื่อและคำอธิบายใหม่")
