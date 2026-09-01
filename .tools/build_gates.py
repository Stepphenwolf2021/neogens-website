#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เปลี่ยนสารบัญเรียงยาวในหน้าแรก เป็นสามประตูตามโครงสามภาคของเว็บ

ของเดิมเป็นบล็อก .hub การ์ด 11 ใบ แบ่งสามกลุ่มที่ไม่ตรงกับโครงเมนู
(the practice · practice areas · working together) คนอ่านจึงเห็นรายการยาว
แต่ไม่เห็นว่าเว็บนี้แบ่งเป็นสามภาคอะไรบ้าง

ของใหม่เป็นสามประตู ตรงกับหัวกลุ่มในเมนูทุกตัวอักษร
  ภาค 1 · แนวคิด            → the-problem
  ภาค 2 · พิพิธภัณฑ์และห้องสมุด → mkm-for-museums-and-libraries
  ภาค 3 · โครงการเพื่อสาธารณะ  → mkm-for-coffee

แต่ละประตูมีหัวข้อที่กดเข้าไปได้ หนึ่งประโยคว่าข้างในคืออะไร และรายการหน้าข้างใน
ที่กดตรงเข้าไปได้ทีละหน้า ไม่ได้ตัดทางลัดของคนที่รู้อยู่แล้วว่าจะไปไหนออก

CSS ใช้ชื่อขึ้นต้น gate- ตรวจแล้วไม่ชนของเดิมทั้งสองไฟล์ ตามบทเรียนข้อ 8
ไฟล์ไทยไม่ถ่างตัวอักษร และ line-height ของย่อหน้าอยู่ที่ 1.8

รันจากรากรีโป:  python3 .tools/build_gates.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── ปิดชั่วคราว 2026-09-01 · หน้าภาค 3 ที่ถูกถอดออกจากหน้าแรก ──
# ลบตัวแปรนี้ทิ้ง แล้วเอาการอ้างถึงมันในด่านตรวจออก เมื่อเปิดภาคกาแฟกลับมา
PAUSED = {"mkm-for-coffee.html", "mkm-for-coffee-why-now.html",
          "mkm-for-coffee-commons.html", "coffee-farmer.html", "coffee-demo.html",
          "th-mkm-for-coffee.html", "th-mkm-for-coffee-why-now.html",
          "th-mkm-for-coffee-commons.html", "th-coffee-farmer.html", "th-coffee-demo.html"}

CSS = """
/* --- สามประตูหน้าแรก --- */
.gates{{padding:clamp(44px,6vw,80px) 0}}
.gates-lead{{font-family:var(--mono);font-size:10px;letter-spacing:{ls};
  text-transform:uppercase;color:var(--mute);margin-bottom:20px}}
.gates-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}
.gate{{border:1px solid var(--line);border-radius:18px;background:var(--surface);
  padding:26px 24px;display:flex;flex-direction:column;
  transition:border-color .2s,transform .2s}}
.gate:hover{{border-color:var(--go-line);transform:translateY(-2px)}}
.gate-k{{font-family:var(--mono);font-size:10px;letter-spacing:{ls};
  text-transform:uppercase;color:var(--go);margin-bottom:12px}}
.gate-t{{font-size:clamp(19px,2.2vw,23px);line-height:1.4;margin:0 0 10px;font-weight:600}}
.gate-t a{{color:var(--fg);text-decoration:none}}
.gate-t a:hover{{color:var(--go)}}
.gate-p{{font-size:15px;line-height:1.8;color:var(--dim);margin:0 0 4px}}
.gate-l{{list-style:none;margin:16px 0 20px;padding:16px 0 0;
  border-top:1px solid var(--line);display:flex;flex-direction:column;gap:7px}}
.gate-l a{{font-size:14.5px;line-height:1.6;color:var(--dim);text-decoration:none}}
.gate-l a:hover{{color:var(--go)}}
.gate-go{{margin-top:auto;font-family:var(--mono);font-size:11px;letter-spacing:{ls};
  text-transform:uppercase}}
.gate-go a{{color:var(--go);text-decoration:none}}
.gates-rest{{margin-top:24px;display:flex;flex-wrap:wrap;gap:10px 22px;font-size:14.5px}}
.gates-rest a{{color:var(--mute);text-decoration:none;line-height:1.8}}
.gates-rest a:hover{{color:var(--go)}}
@media(max-width:980px){{.gates-grid{{grid-template-columns:1fr}}}}
"""

EN = {
    "file": "index.html",
    "ls": ".14em",
    "lead": "Two ways in — start wherever you already are",
    "gates": [
        ("Part 1 · The idea", "The idea", "the-problem.html",
         "AI answers everything and knows nothing about your organisation. What a "
         "knowledge layer is, where it sits, and why it changes the answer.",
         [("the-problem.html", "01 · The problem"),
          ("what-mkm-is.html", "02 · What is MKM ?"),
          ("why-it-works.html", "03 · Why it works"),
          ("ontology-and-knowledge-graph.html", "04 · Ontology &amp; knowledge graph")],
         "Start with the problem"),
        ("Part 2 · Museums &amp; libraries", "MKM for Museums &amp; Libraries",
         "exec-summary-museums.html",
         "The institutions with the best knowledge in the room are losing the room. "
         "What that costs, and how we work with your specialists rather than instead "
         "of them.",
         [("exec-summary-museums.html", "Executive summary"),
          ("mkm-for-museums-and-libraries.html", "01 · Where things stand"),
          ("what-you-are-holding.html", "01b · What you are holding"),
          ("visitors-and-readers.html", "02 · The new experience"),
          ("leadership.html", "03 · What leadership looks like"),
          ("services.html", "What we do together"),
          ("engagement.html", "Engagement"),
          ("ai-sovereignty.html", "Your data · AI sovereignty")],
         "See the practice"),
        # ── ปิดชั่วคราว 2026-09-01 · ถอดประตูที่สาม MKM for Coffee ออก ──
        # เอากลับ: ปลด comment สองบล็อกนี้ · เปลี่ยน lead กลับเป็น Three ways in
        # และ .gates-grid กลับเป็น repeat(3,1fr) · ดู .tools/pause_coffee.py
        # ("Part 3 · Public goods", "MKM for Coffee", "mkm-for-coffee.html",
        #  "An industry drowning in data and starving for knowledge. A vault no single "
        #  "party owns, that everyone along the chain can use — open for comment now.",
        #  [("mkm-for-coffee.html", "The full argument"),
        #   ("coffee-farmer.html", "For coffee farmers"),
        #   ("coffee-demo.html", "Demo: the vault in use")],
        #  "Read the project"),
    ],
    "rest": [("what-we-wont-do.html", "What we won't do"),
             ("long-read-museums-and-libraries.html", "Long read: MKM for museums &amp; libraries"),
             ("about.html", "Who we are"),
             ("contact.html", "Request a briefing")],
}

TH = {
    "file": "th-index.html",
    "ls": "0",
    "lead": "ทางเข้าสองทาง เริ่มจากตรงที่คุณอยู่ตอนนี้",
    "gates": [
        ("ภาค 1 · แนวคิด", "แนวคิด", "th-the-problem.html",
         "AI ตอบได้ทุกเรื่อง แต่ไม่รู้อะไรเลยเกี่ยวกับองค์กรของคุณ ชั้นความรู้คืออะไร "
         "วางอยู่ตรงไหน และทำไมมันถึงเปลี่ยนคำตอบ",
         [("th-the-problem.html", "01 · ปัญหา"),
          ("th-what-mkm-is.html", "02 · MKM คืออะไร"),
          ("th-why-it-works.html", "03 · ทำไมมันถึงได้ผล"),
          ("th-ontology-and-knowledge-graph.html", "04 · ontology กับ knowledge graph")],
         "เริ่มที่ปัญหา"),
        ("ภาค 2 · พิพิธภัณฑ์และห้องสมุด", "MKM สำหรับพิพิธภัณฑ์และห้องสมุด",
         "th-exec-summary-museums.html",
         "สถาบันที่มีความรู้ดีที่สุดในห้องกำลังเสียห้องนั้นไป เรื่องนี้มีต้นทุนเท่าไร "
         "และเราทำงานร่วมกับผู้เชี่ยวชาญของคุณอย่างไร ไม่ใช่ทำแทนพวกเขา",
         [("th-exec-summary-museums.html", "บทสรุปสำหรับผู้บริหาร"),
          ("th-mkm-for-museums-and-libraries.html", "01 · สถานะวันนี้"),
          ("th-what-you-are-holding.html", "01b · สิ่งที่คุณถืออยู่"),
          ("th-visitors-and-readers.html", "02 · ประสบการณ์ใหม่ของการเรียนรู้"),
          ("th-leadership.html", "03 · ความเป็นผู้นำหน้าตาเป็นอย่างไร"),
          ("th-services.html", "เราทำอะไรร่วมกัน"),
          ("th-engagement.html", "รูปแบบการทำงาน"),
          ("th-ai-sovereignty.html", "ข้อมูลของคุณ · AI Sovereignty")],
         "ดูงานฝั่งปฏิบัติ"),
        # ── ปิดชั่วคราว 2026-09-01 · ถอดประตูที่สาม MKM สำหรับกาแฟ ออก ──
        # ("ภาค 3 · โครงการเพื่อสาธารณะ", "MKM สำหรับกาแฟ", "th-mkm-for-coffee.html",
        #  "อุตสาหกรรมที่จมอยู่ในข้อมูล แต่ขาดความรู้ คลังที่ไม่มีใครเป็นเจ้าของแต่ผู้เดียว "
        #  "และทุกคนตลอดห่วงโซ่ใช้ได้ ตอนนี้เปิดรับความคิดเห็นอยู่",
        #  [("th-mkm-for-coffee.html", "อ่านโครงการเต็ม"),
        #   ("th-coffee-farmer.html", "สำหรับคนปลูกกาแฟ"),
        #   ("th-coffee-demo.html", "เดโมแดชบอร์ด")],
        #  "อ่านโครงการ"),
    ],
    "rest": [("th-what-we-wont-do.html", "สิ่งที่เราไม่ทำ"),
             ("long-read-museums-and-libraries.html", "บทความยาว: MKM สำหรับพิพิธภัณฑ์และห้องสมุด (อังกฤษ)"),
             ("th-about.html", "เราคือใคร"),
             ("th-contact.html", "ขอนัดหารือ")],
}


def section(C):
    cards = []
    for kick, title, href, promise, inside, cta in C["gates"]:
        items = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in inside)
        cards.append(
            f'<div class="gate"><div class="gate-k">{kick}</div>'
            f'<h3 class="gate-t"><a href="{href}">{title}</a></h3>'
            f'<p class="gate-p">{promise}</p>'
            f'<ul class="gate-l">{items}</ul>'
            f'<div class="gate-go"><a href="{href}">{cta} →</a></div></div>')
    rest = "".join(f'<a href="{h}">{t}</a>' for h, t in C["rest"])
    return ('<section class="gates"><div class="wrap">'
            f'<div class="gates-lead">{C["lead"]}</div>'
            '<div class="gates-grid">' + "".join(cards) + "</div>"
            f'<div class="gates-rest">{rest}</div>'
            "</div></section>")


for C in (EN, TH):
    path = ROOT / C["file"]
    s = before = path.read_text(encoding="utf-8")

    # รันซ้ำได้ · ถอดของที่สคริปต์นี้เคยวางไว้ออกก่อน แล้วค่อยประกอบใหม่จากต้นฉบับ
    s = re.sub(r'<section class="gates">.*?</section>', '<section class="hub"></section>',
               s, count=1, flags=re.S)
    s = re.sub(r'\n/\* --- สามประตูหน้าแรก --- \*/.*?(?=</style>)', '', s, count=1, flags=re.S)

    m = re.search(r'<section class="hub">.*?</section>', s, re.S)
    if not m:
        sys.exit(f"✗ {C['file']} หาบล็อกสารบัญเดิมไม่เจอ")
    old_links = set(re.findall(r'href="([^"]+)"', m.group(0)))
    s = s[:m.start()] + section(C) + s[m.end():]

    if s.count("</style>") != 1:
        sys.exit(f"✗ {C['file']} มี </style> ไม่ใช่จุดเดียว")
    s = s.replace("</style>", CSS.format(ls=C["ls"]) + "</style>", 1)

    # ---- ด่านตรวจ ----
    new_links = set(re.findall(r'href="([^"]+)"', section(C)))
    checks = {
        # ปิดชั่วคราว 2026-09-01 · ภาค 3 ถูกถอดออก ประตูจึงเหลือสอง
        # เอากลับเป็น 3 ทั้งสามข้อ เมื่อเปิดภาคกาแฟกลับมา
        "สองประตู": s.count('<div class="gate">') == 2,
        "หัวข้อประตูกดได้": s.count('class="gate-t"') == 2,
        "ปุ่มเข้าครบ": s.count('class="gate-go"') == 2,
        "รายการข้างในครบ": s.count("<li><a href=") == sum(len(g[4]) for g in C["gates"]),
        "แถวลิงก์รอง": s.count('class="gates-rest"') == 1,
        "CSS เข้าไฟล์": ".gate{" in s and s.index(".gate{") < s.index("</style>"),
        "CSS ชุดเดียว": s.count("/* --- สามประตูหน้าแรก --- */") == 1,
        "ไม่เหลือบล็อกเดิม": '<section class="hub">' not in s,
        "ไทยไม่ถ่างตัวอักษร": ("letter-spacing:0;" in CSS.format(ls=C["ls"])
                               if C["ls"] == "0" else True),
        # ปิดชั่วคราว 2026-09-01 · ลิงก์ภาคกาแฟตั้งใจให้หายไป จึงยกเว้นให้ชุดนี้ชุดเดียว
        # เอากลับ: ลบ - PAUSED ออกจากบรรทัดล่าง เมื่อเปิดภาคกาแฟกลับมา
        "ไม่มีลิงก์ไหนหายไปจากหน้าแรก": not (old_links - new_links - PAUSED - set(
            re.findall(r'href="([^"]+)"', s))),
        "ไม่เหลือลิงก์กาแฟในหน้าแรก": not (PAUSED & set(
            re.findall(r'href="([^"]+)"', s))),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {C['file']} ด่านตรวจไม่ผ่าน: " + " · ".join(bad))

    path.write_text(s, encoding="utf-8")
    dropped = sorted(old_links - new_links)
    print(f"✓ {C['file']}  {len(before)//1024} KB → {len(s)//1024} KB · "
          f"การ์ด 11 ใบ → สามประตู + ลิงก์รอง {len(C['rest'])} เส้น")
    if dropped:
        print("   หน้าที่ไม่อยู่ในสามประตูแล้ว แต่ยังไปถึงได้จากเมนูและ footer:",
              ", ".join(dropped))
