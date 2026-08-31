#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้าง exec-summary-museums.html และฉบับไทย จากต้นฉบับใน .tools/exec-summary-source/

หน้านี้อยู่ในภาค 2 พิพิธภัณฑ์และห้องสมุด จึงมี BreadcrumbList ต่างจากหน้า SEO
ใช้ coffee-farmer.html กับ th-coffee-farmer.html เป็นแม่แบบ ตามที่ build_evidence.py
กับ build_privacy.py ทำ จะได้ nav ธีม footer และ CSS ชุดเดียวกับหน้าอื่นในภาษานั้น

**ฟอร์มของแม่แบบถูกถอดออก** เพราะฟอร์มนั้นส่ง topic:'MKM Coffee' ซึ่ง Worker
มี allow-list รับแค่ค่านี้ค่าเดียว ถ้าปล่อยไว้ ผู้อำนวยการพิพิธภัณฑ์ที่กรอกฟอร์ม
จะถูกบันทึกเป็นลูกค้าสายกาแฟ ปิดท้ายด้วยลิงก์ไปหน้า contact.html แทน
JS ที่ผูกกับฟอร์มมี if(form) กันไว้อยู่แล้ว ถอดฟอร์มออกจึงไม่ทำให้ JS พัง

รันซ้ำได้ ผลลัพธ์เท่าเดิม เพราะสร้างจากแม่แบบใหม่ทุกครั้ง ไม่ได้แก้ไฟล์เดิมทับ

รันจากรากรีโป:  python3 .tools/build_exec_summary.py
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".tools" / "exec-summary-source"
BASE = "https://www.neogens.co/"

LANG_BLOCK = re.compile(r'<span class="lang">.*?</span>(?=<button)', re.S)
ALT_BLOCK = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n')
JSONLD_BLOCK = re.compile(r'[ \t]*<script type="application/ld\+json">.*?</script>\n', re.S)
CRUMBS_BLOCK = re.compile(r'[ \t]*<nav class="crumbs".*?</nav>\n', re.S)
JOIN_BLOCK = re.compile(r'<section class="join".*?</section>\n', re.S)

TEMPLATE_MARKS = ("What you know about your own plot", "ความรู้ที่อยู่ในหัวคุณ",
                  "Farm, mill, co-op or roastery", "Send my details",
                  'id="wl"')
# หมายเหตุสองข้อ
# 1 คำว่า MKM Coffee เฉย ๆ ตัดไม่ได้ เพราะเป็นป้ายเมนูของภาค 3 ที่มีอยู่ทุกหน้า
# 2 สตริง topic:'MKM Coffee' ยังอยู่ในบล็อก JS ของแม่แบบ แต่โค้ดก้อนนั้นมี if(form)
#   ครอบไว้ พอถอดฟอร์มออก มันจึงไม่มีวันทำงาน ไม่ตัดทิ้งเพราะการไปตัด JS ด้วย regex
#   คือความผิดข้อ 11 ของ LESSONS.md ซ้ำรอย ด่านข้างล่างจึงตรวจสองอย่างแทน
#   ไม่มี id="wl" ในหน้า และยังมี if(form) กันไว้

LANGS = [
    dict(lang="en", md="neogens-exec-summary-museums-EN.md",
         src="coffee-farmer.html", out="exec-summary-museums.html",
         twin="th-exec-summary-museums.html",
         title="Executive summary — MKM for museums & libraries",
         desc=("Mission-driven ontology and knowledge graphs over the collection you "
               "already have, so that AI works on your institution's confidence and "
               "the public's trust."),
         kicker="executive summary", meta="12 min read",
         cta_k="Start the conversation",
         cta_h="If this is close to what you have been thinking, let's find a time.",
         cta_p=("90 minutes. Bring your curators or librarians, and one question "
                "your institution could not answer."),
         cta_btn="Request a briefing"),
    dict(lang="th", md="neogens-exec-summary-museums-TH.md",
         src="th-coffee-farmer.html", out="th-exec-summary-museums.html",
         twin="exec-summary-museums.html",
         title="บทสรุปสำหรับผู้บริหาร — MKM พิพิธภัณฑ์และห้องสมุด",
         desc=("ออกแบบและสร้าง ontology กับ knowledge graph จากพันธกิจขององค์กร "
               "บนคอลเลกชันที่มีอยู่แล้ว เพื่อให้ AI ทำงานบนความเชื่อมั่นขององค์กร"
               "และความเชื่อถือของสาธารณชน"),
         kicker="บทสรุปสำหรับผู้บริหาร", meta="อ่าน 12 นาที",
         cta_k="เริ่มต้นบทสนทนา",
         cta_h="ถ้าเรื่องนี้ใกล้กับสิ่งที่ท่านคิดอยู่ มานัดเวลากัน",
         cta_p=("90 นาที ชวนภัณฑารักษ์หรือบรรณารักษ์มาด้วย "
                "พร้อมคำถามหนึ่งข้อที่องค์กรของท่านยังตอบไม่ได้"),
         cta_btn="ขอนัดหารือ"),
]


# ---------------------------------------------------------------- แผงตัวเลข
#
# **ไม่ได้เอาภาพของเจ้าของงานมาแปะ** การ์ดรายงานของ Culture For Causes Network
# กับอินโฟกราฟิกของ AAM เป็นงานออกแบบของเขา การเอาขึ้นเว็บเชิงพาณิชย์ของเราต้องขออนุญาต
# สิ่งที่ทำได้โดยไม่ต้องขอคือ **เอาตัวเลขมาวาดใหม่เอง** ตัวเลขไม่มีลิขสิทธิ์ การนำเสนอมี
# ทุกแผงจึงมีบรรทัดบอกฐาน วันเก็บข้อมูล เจ้าของงาน และลิงก์กลับไปต้นทาง
#
# ถ้าวันไหนได้รับอนุญาตให้ใช้ภาพต้นฉบับ ให้มาแทนที่ตรงนี้ที่เดียว

FIGCSS = {
    "en": """
/* --- แผงตัวเลขจากงานสำรวจ วาดเองจากข้อมูลที่เผยแพร่ ไม่ได้ใช้ภาพของเจ้าของงาน --- */
.esf{{margin:36px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.esf-in{{display:grid}}
.esf-4 .esf-in{{grid-template-columns:repeat(4,1fr)}}
.esf-3 .esf-in{{grid-template-columns:repeat(3,1fr)}}
.esf-c{{padding:20px 18px 20px;border-left:1px solid var(--line)}}
.esf-c:first-child{{border-left:0;padding-left:0}}
.esf-k{{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--mute);line-height:1.9}}
.esf-n{{font-size:40px;line-height:1.15;margin:8px 0 10px;color:var(--fg)}}
.esf-n i{{font-size:19px;font-style:normal;vertical-align:super;color:var(--mute)}}
.esf-t{{font-size:14px;line-height:1.65;color:var(--dim);margin:0}}
.esf-d{{font-family:var(--mono);font-size:10px;line-height:1.9;color:var(--mute);margin:8px 0 0}}
.esf figcaption{{font-family:var(--mono);font-size:11px;line-height:1.9;color:var(--mute);
  padding:12px 0 14px;margin:0}}
.esf figcaption a{{color:var(--mute)}}
.esf figcaption a:hover{{color:var(--go)}}
@media(max-width:760px){{
  .esf-in{{grid-template-columns:repeat(2,1fr)}}
  .esf-c:nth-child(odd){{border-left:0;padding-left:0}}
}}
""",
    "th": """
/* --- แผงตัวเลขจากงานสำรวจ วาดเองจากข้อมูลที่เผยแพร่ ไม่ได้ใช้ภาพของเจ้าของงาน --- */
.esf{{margin:36px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.esf-in{{display:grid}}
.esf-4 .esf-in{{grid-template-columns:repeat(4,1fr)}}
.esf-3 .esf-in{{grid-template-columns:repeat(3,1fr)}}
.esf-c{{padding:20px 18px 20px;border-left:1px solid var(--line)}}
.esf-c:first-child{{border-left:0;padding-left:0}}
.esf-k{{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--mute);line-height:1.9}}
.esf-n{{font-size:40px;line-height:1.2;margin:8px 0 10px;color:var(--fg)}}
.esf-n i{{font-size:19px;font-style:normal;vertical-align:super;color:var(--mute)}}
.esf-t{{font-size:14px;line-height:1.8;color:var(--dim);margin:0}}
.esf-d{{font-size:11px;line-height:1.8;color:var(--mute);margin:8px 0 0}}
.esf figcaption{{font-size:12px;line-height:1.8;color:var(--mute);padding:12px 0 14px;margin:0}}
.esf figcaption a{{color:var(--mute)}}
.esf figcaption a:hover{{color:var(--go)}}
@media(max-width:760px){{
  .esf-in{{grid-template-columns:repeat(2,1fr)}}
  .esf-c:nth-child(odd){{border-left:0;padding-left:0}}
}}
""",
}

MW_URL = "https://museumweek2h1r4.substack.com/p/museumweek-2026-the-story-of-a-week"
AAM_URL = ("https://www.aam-us.org/2026/03/30/"
           "ai-in-museums-and-community-trust-a-2025-annual-survey-of-museum-goers-data-story/")

FIGURES = {
    "survey": {
        "en": dict(
            label="Museums & AI Survey · 180 institutions · 35 countries",
            cols=[("AI adoption", "52", "of institutions report having adopted AI tools",
                   "Don't know · 11%"),
                  ("Written policy", "9", "have a formal AI charter or written policy",
                   "Don't know · 11%"),
                  ("Trained staff", "26", "have received any formal AI training", ""),
                  ("Perception", "46", "frame AI as an opportunity; 43% remain uncertain", "")],
            cap=("Fieldwork 17 September – 14 November 2025 · n=180 per measure · "
                 "MuseumWeek and Culture For Causes Network · "
                 f'figures redrawn by Neo Gens from the published report card, <a href="{MW_URL}">source</a>'),
        ),
        "th": dict(
            label="Museums & AI Survey · 180 หน่วยงาน · 35 ประเทศ",
            cols=[("รับ AI มาใช้แล้ว", "52", "ของหน่วยงานตอบว่ารับเครื่องมือ AI เข้ามาใช้แล้ว",
                   "ตอบว่าไม่รู้ · 11%"),
                  ("มีนโยบายเป็นลายลักษณ์อักษร", "9",
                   "มีธรรมนูญหรือนโยบายเรื่อง AI ที่เขียนไว้", "ตอบว่าไม่รู้ · 11%"),
                  ("เคยผ่านการอบรม", "26", "ของผู้ตอบเคยผ่านการอบรมเรื่อง AI มาบ้าง", ""),
                  ("มุมมอง", "46", "มองว่า AI เป็นโอกาส อีก 43% ยังไม่มีจุดยืน", "")],
            cap=("เก็บข้อมูล 17 กันยายน ถึง 14 พฤศจิกายน 2025 · ฐาน 180 ต่อทุกตัวเลข · "
                 "MuseumWeek กับ Culture For Causes Network · "
                 f'Neo Gens วาดแผงนี้ขึ้นใหม่จากการ์ดรายงานที่เผยแพร่ <a href="{MW_URL}">ดูต้นทาง</a>'),
        ),
    },
    "public": {
        "en": dict(
            label="What the public expects · 2,000+ US adults",
            cols=[("Exhibitions", "70", "want no AI at all in developing exhibitions", ""),
                  ("Everything", "43", "expect human beings to write every piece of content", ""),
                  ("Disclosure", "45", "want to be told every time AI is used", "")],
            cap=("Surveyed January 2026 · demographically representative sample of more than "
                 "2,000 US adults · American Alliance of Museums and Wilkening Consulting · "
                 f'figures redrawn by Neo Gens, <a href="{AAM_URL}">source</a>'),
        ),
        "th": dict(
            label="สิ่งที่ผู้เข้าชมคาดหวัง · ผู้ใหญ่ในสหรัฐกว่า 2,000 คน",
            cols=[("นิทรรศการ", "70", "ไม่อยากให้ใช้ AI ในการพัฒนานิทรรศการเลย", ""),
                  ("ทุกชิ้นงาน", "43", "อยากให้คนเป็นผู้เขียนเนื้อหาทุกชิ้นของพิพิธภัณฑ์", ""),
                  ("การเปิดเผย", "45", "อยากรู้ทุกครั้งที่มีการใช้ AI", "")],
            cap=("สำรวจเมื่อมกราคม 2026 · กลุ่มตัวอย่างที่คุมสัดส่วนตามโครงสร้างประชากร "
                 "ผู้ใหญ่ในสหรัฐกว่า 2,000 คน · American Alliance of Museums กับ Wilkening Consulting · "
                 f'Neo Gens วาดแผงนี้ขึ้นใหม่ <a href="{AAM_URL}">ดูต้นทาง</a>'),
        ),
    },
}


def figure(key, lang):
    F = FIGURES[key][lang]
    cols = "".join(
        f'<div class="esf-c"><div class="esf-k">{inline(k)}</div>'
        f'<div class="esf-n">{n}<i>%</i></div>'
        f'<p class="esf-t">{inline(t)}</p>'
        + (f'<p class="esf-d">{inline(d)}</p>' if d else "")
        + "</div>"
        for k, n, t, d in F["cols"])
    return (f'<figure class="esf esf-{len(F["cols"])}" role="group" '
            f'aria-label="{inline(F["label"])}">'
            f'<div class="esf-in">{cols}</div>'
            f'<figcaption>{F["cap"]}</figcaption></figure>')


# ---------------------------------------------------------------- markdown

def inline(t):
    """escape ก่อน แล้วค่อยแปลง **หนา** กับ *เอียง* ลำดับนี้ห้ามสลับ"""
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", t)
    return t


def parse(md):
    """คืน (front, blocks) — front คือส่วนหัวก่อน --- เส้นแรก"""
    lines = md.rstrip().split("\n")
    cut = lines.index("---")
    front, body = lines[:cut], lines[cut + 1:]

    h1 = front[0].lstrip("# ").strip()
    stand = next(l for l in front[1:] if l.startswith("**")).strip("* ")
    tag = [l.strip() for l in front if l.strip()][2:]

    blocks, buf, mode = [], [], None

    def flush():
        nonlocal buf, mode
        if buf:
            blocks.append((mode, buf))
        buf, mode = [], None

    for raw in body:
        l = raw.rstrip()
        if not l.strip() or l.strip() == "---":
            flush()
            continue
        if l.startswith("### "):
            flush()
            blocks.append(("h3", [l[4:].strip()]))
        elif l.startswith("## "):
            flush()
            blocks.append(("h2", [l[3:].strip()]))
        elif l.startswith("- "):
            if mode != "ul":
                flush()
                mode = "ul"
            buf.append(l[2:].strip())
        elif re.match(r"^\d+\. ", l):
            if mode != "ol":
                flush()
                mode = "ol"
            buf.append(re.sub(r"^\d+\. ", "", l).strip())
        else:
            if mode != "p":
                flush()
                mode = "p"
            buf.append(l.strip())
    flush()
    return dict(h1=h1, stand=stand, tag=tag), blocks


def render(blocks, lang):
    out, n, first = [], 0, True
    for kind, val in blocks:
        if kind == "p" and len(val) == 1 and re.fullmatch(r"\[\[FIGURE:(\w+)\]\]", val[0]):
            out.append(figure(re.fullmatch(r"\[\[FIGURE:(\w+)\]\]", val[0]).group(1), lang))
            continue
        if kind == "h2":
            m = re.match(r"^(\d+)\.\s+(.*)$", val[0])
            if m:
                n = int(m.group(1))
                out.append(f'<h2 id="s{n:02d}"><span class="sn">{n:02d}</span>'
                           f"{inline(m.group(2))}</h2>")
            else:
                out.append(f"<h2>{inline(val[0])}</h2>")
        elif kind == "h3":
            out.append(f"<h3>{inline(val[0])}</h3>")
        elif kind in ("ul", "ol"):
            items = "".join(f"<li>{inline(x)}</li>" for x in val)
            out.append(f"<{kind}>{items}</{kind}>")
        else:
            cls = ' class="first"' if first else ""
            out.append(f"<p{cls}>{inline(' '.join(val))}</p>")
            first = False
    return "\n".join(out)


# ---------------------------------------------------------------- build

def build(C):
    md = (SRC / C["md"]).read_text(encoding="utf-8")
    front, blocks = parse(md)
    body = render(blocks, C["lang"])
    n_fig = body.count('<figure class="esf')

    s = (ROOT / C["src"]).read_text(encoding="utf-8")

    # ---- หัวเรื่องและ meta ----
    s = re.sub(r"<title>.*?</title>", f"<title>{html.escape(C['title'])}</title>",
               s, count=1, flags=re.S)
    for tag in ('<meta name="description" content="',
                '<meta property="og:description" content="'):
        cur = re.search(re.escape(tag) + r'([^"]*)"', s).group(1)
        s = s.replace(tag + cur, tag + html.escape(C["desc"]), 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*"',
               lambda m: m.group(1) + html.escape(C["title"]) + '"', s, count=1)
    for old in ("coffee-farmer.html", "th-coffee-farmer.html"):
        s = s.replace(f"{BASE}{old}", f"{BASE}{C['out']}")

    # ---- คู่ภาษา ----
    en_page = C["out"] if C["lang"] == "en" else C["twin"]
    th_page = C["out"] if C["lang"] == "th" else C["twin"]
    alts = "".join(f'<link rel="alternate" hreflang="{k}" href="{BASE}{v}">\n'
                   for k, v in (("en", en_page), ("th", th_page), ("x-default", en_page)))
    s, n_alt = ALT_BLOCK.subn("", s)
    if n_alt != 3:
        sys.exit(f"[abort] แม่แบบมี hreflang {n_alt} ตัว คาดว่า 3")
    s = s.replace('<link rel="canonical"', alts + '<link rel="canonical"', 1)

    lang_html = (f'<span class="lang"><a class="on" href="{th_page}">TH</a>'
                 f'<span>/</span><a href="{en_page}">EN</a></span>') if C["lang"] == "th" else (
                f'<span class="lang"><a class="on" href="{en_page}">EN</a>'
                f'<span>/</span><a href="{th_page}">TH</a></span>')
    s, n_lang = LANG_BLOCK.subn(lambda m: lang_html, s)

    # ---- หัวหน้า ----
    m = re.search(r'<div class="kicker">.*?</div>\s*</div>\s*</header>', s, re.S)
    if not m:
        sys.exit(f"[abort] {C['src']} ไม่มีหัวหน้าแบบ kicker ที่คาดไว้")
    meta_bits = "".join(f"<span>{inline(x)}</span>" for x in ["Neo Gens", C["meta"]])
    s = s[:m.start()] + (
        f'<div class="kicker">{C["kicker"]}</div>\n'
        f'      <h1>{inline(front["h1"])}</h1>\n'
        f'      <p class="stand">{inline(front["stand"])}</p>\n'
        f'      <div class="meta">{meta_bits}</div>\n'
        f'    </div>\n  </div>\n</header>') + s[m.end():]

    # ---- เนื้อหา ----
    i, j = s.index("<article>"), s.index("</article>") + len("</article>")
    s = s[:i] + ('<article>\n  <div class="wrap">\n    <div class="artbody">\n'
                 + body + "\n    </div>\n  </div>\n</article>") + s[j:]

    # ---- CSS ของแผงตัวเลข แม่แบบไม่มีคลาสพวกนี้ ต้องเติมเอง ----
    # แทรกที่ </style> ตัวท้ายที่ยังอยู่ใน <head> ไม่ใช่ตัวท้ายของไฟล์ ดู HANDOFF ข้อ 3
    head_end = s.index("</head>")
    last_style = s.rindex("</style>", 0, head_end)
    s = s[:last_style] + FIGCSS[C["lang"]].replace("{{", "{").replace("}}", "}") + s[last_style:]

    # ---- ของที่ติดมากับแม่แบบและไม่ใช่ของหน้านี้ (ข้อ 10 ของ LESSONS.md) ----
    s = JSONLD_BLOCK.sub("", s)
    s = CRUMBS_BLOCK.sub("", s)

    # ---- ฟอร์มกาแฟออก กล่องชวนคุยเข้า ----
    cta = (f'<section class="join" id="join">\n'
           f'  <div class="join-bg"></div>\n'
           f'  <div class="wrap">\n    <div class="inner">\n'
           f'      <div class="k rv">{inline(C["cta_k"])}</div>\n'
           f'      <h2 class="rv">{inline(C["cta_h"])}</h2>\n'
           f'      <p class="lead rv">{inline(C["cta_p"])}</p>\n'
           f'      <p class="rv"><a class="btn" href="contact.html">'
           f'{inline(C["cta_btn"])}</a></p>\n'
           f'      <p class="form-note rv">hello@neogens.co</p>\n'
           f'    </div>\n  </div>\n</section>\n')
    s, n_join = JOIN_BLOCK.subn(lambda m: cta, s)
    if n_join != 1:
        sys.exit(f"[abort] {C['out']} ตัดกล่องฟอร์มได้ {n_join} ก้อน คาดว่า 1")

    # ---- ด่านตรวจ เขียนไฟล์ต่อเมื่อผ่านครบ ----
    n_h2 = sum(1 for k, _ in blocks if k == "h2")
    n_h3 = sum(1 for k, _ in blocks if k == "h3")
    # ตัวยึดรูปนับเป็นบล็อก p ในต้นฉบับ แต่ไม่ได้ออกมาเป็น <p> จึงต้องหักออก
    n_p = sum(1 for k, v in blocks if k == "p"
              and not re.fullmatch(r"\[\[FIGURE:\w+\]\]", v[0]))
    body_wo_fig = re.sub(r'<figure class="esf.*?</figure>', "", body, flags=re.S)
    n_li = sum(len(v) for k, v in blocks if k in ("ul", "ol"))
    checks = {
        # --- มีครบ ---
        "หัวข้อ h2 ครบตามต้นฉบับ": s.count("<h2") == n_h2 + 1,     # +1 คือกล่องชวนคุย
        "หัวข้อ h3 ครบตามต้นฉบับ": s.count("<h3>") == n_h3,
        "ย่อหน้าครบตามต้นฉบับ": body_wo_fig.count("<p") == n_p,
        "รายการครบตามต้นฉบับ": body_wo_fig.count("<li>") == n_li,
        "พาดหัวมาจากต้นฉบับ": f'<h1>{inline(front["h1"])}</h1>' in s,
        "มี h1 เดียว": s.count("<h1>") == 1,
        "title ไม่เกิน 60": len(C["title"]) <= 60,
        "description ไม่เกิน 160": len(C["desc"]) <= 160,
        "og:description ตรงกับ description": s.count(html.escape(C["desc"])) >= 2,
        "canonical ชี้หน้านี้": f'rel="canonical" href="{BASE}{C["out"]}"' in s,
        "hreflang ชี้คู่ถูก": (f'hreflang="en" href="{BASE}{en_page}"' in s and
                              f'hreflang="th" href="{BASE}{th_page}"' in s and
                              f'hreflang="x-default" href="{BASE}{en_page}"' in s),
        "ปุ่มสลับภาษาสองชุด": n_lang == 2,
        "หลักการห้าข้อครบ": all(c in s for c in "①②③④⑤"),
        # สองบล็อกนี้ถูกตัดออกเมื่อ 08-31 รอบดึก ตามที่ Noppadol ยืนยัน ห้ามเติมกลับโดยไม่ถาม
        # ดูหัวข้อ exec summary ใน HANDOFF
        "ไม่เหลือบล็อกสามทางที่ผู้บริหารมักเลือก":
            "The three routes directors reach for" not in s
            and "สามทางที่ผู้บริหารมักเลือก" not in s,
        "ไม่เหลือย่อหน้าข้อสังเกตเรื่องตัวเลข":
            "One caution about that survey" not in s
            and "ขอตั้งข้อสังเกตเรื่องตัวเลขชุดนี้" not in s,
        "แผงตัวเลขครบสองแผง": n_fig == 2,
        "ทุกแผงมีบรรทัดบอกที่มา": s.count("<figcaption>") == 2,
        "แผงตัวเลขมีคำบรรยายให้โปรแกรมอ่านหน้าจอ": s.count('role="group"') == 2,
        "CSS ของแผงเข้าไฟล์แล้ว": ".esf{" in s and s.index(".esf{") < s.index("</head>"),
        "ไม่เหลือตัวยึดรูปที่ยังไม่แปลง": "[[FIGURE:" not in s,
        "ปุ่มปิดท้ายชี้หน้าติดต่อ": 'class="btn" href="contact.html"' in s,
        # --- ไม่เหลือ ---
        "ไม่เหลือเนื้อหาแม่แบบ (" + " · ".join(
            t for t in TEMPLATE_MARKS if t in s) + ")": not any(t in s for t in TEMPLATE_MARKS),
        "ไม่เหลือฟอร์มของแม่แบบ": "<form" not in s and "<textarea" not in s,
        "โค้ดส่งฟอร์มกลายเป็นโค้ดตาย": "if(form)" in s and 'id="wl"' not in s,
        "ไม่เหลือ JSON-LD ของแม่แบบ": "application/ld+json" not in s,
        "ไม่เหลือแถบเส้นทางของแม่แบบ": 'class="crumbs"' not in s,
        "ไม่เหลือ markdown ที่ยังไม่แปลง": not re.search(r"(?m)^#{1,3} |\*\*", body),
        # ลิงก์ออกนอกเว็บได้เฉพาะบรรทัดอ้างอิงใต้แผงตัวเลข และต้องเป็นสองที่มาที่ประกาศไว้
        # เท่านั้น ไม่มีการโหลดของจากภายนอกเลย src ยังห้ามเด็ดขาดเหมือนเดิม
        "ไม่โหลดของจากภายนอก": not re.search(r'src="https?://(?!www\.neogens\.co)', s),
        "ลิงก์ออกนอกเว็บมีแต่ที่มาของตัวเลข": sorted(
            set(re.findall(r'href="(https?://(?!www\.neogens\.co)[^"]+)"', s))
        ) == sorted({AAM_URL, MW_URL}),
        "ลิงก์ที่มาอยู่ในบรรทัดอ้างอิงใต้แผง": all(
            s.count(f'<a href="{u}">') == s.count(u) for u in (AAM_URL, MW_URL)),
        "ปีกกาใน style สมดุล": s.count("{", 0, s.rindex("</style>")) >= 0,
        "ลิงก์ในหน้าไปไฟล์ที่มีจริง": all(
            (ROOT / h).exists()
            for h in re.findall(r'href="([a-z0-9][a-z0-9.-]*\.html)"', s)
            if h not in (C["twin"], C["out"])),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"[abort] {C['out']}: " + " · ".join(bad))

    (ROOT / C["out"]).write_text(s, encoding="utf-8")
    print(f"  สร้าง {C['out']} · {len(s.encode()) // 1024} KB · "
          f"h2 {n_h2} · h3 {n_h3} · ย่อหน้า {n_p} · รายการ {n_li} · ตรวจผ่าน {len(checks)} ข้อ")


for C in LANGS:
    build(C)

# เมนูที่ติดมากับแม่แบบยังชี้ว่าหน้านี้คือ coffee-farmer ต้องซิงก์ใหม่ก่อน
# แล้วค่อยฝัง JSON-LD เพราะกราฟดึงป้ายเมนูไปใช้ แล้วปิดท้ายด้วยแถบเส้นทาง
# ซึ่งดึงจาก JSON-LD ของหน้านั้นเอง ลำดับนี้ห้ามสลับ ดู HANDOFF หัวข้อ ลำดับที่ห้ามสลับ
for tool in ("sync_nav.py", "build_jsonld.py", "add_breadcrumbs.py"):
    subprocess.run([sys.executable, str(Path(__file__).with_name(tool))],
                   check=True, cwd=ROOT)

# ---- หน้านี้ต้องไม่ประกาศว่าตัวเองเป็นหน้าอื่น (ข้อ 10 และ 12) ----
for C in LANGS:
    t = (ROOT / C["out"]).read_text(encoding="utf-8")
    ac = re.findall(r'<a[^>]*aria-current="page"[^>]*>', t)
    for a in ac:
        href = re.search(r'href="([^"]+)"', a).group(1)
        if href != C["out"]:
            sys.exit(f"✗ {C['out']} เมนูชี้ว่าหน้าปัจจุบันคือ {href}")
    if len(ac) != 1:
        sys.exit(f"✗ {C['out']} มี aria-current ในลิงก์ {len(ac)} อัน ต้องมีอันเดียว")
    if 'class="crumbs"' not in t:
        sys.exit(f"✗ {C['out']} ไม่มีแถบเส้นทาง ทั้งที่อยู่ในภาค 2")

# ---- คู่ภาษาต้องยืนยันกลับหากัน ----
for C in LANGS:
    a = (ROOT / C["out"]).read_text(encoding="utf-8")
    b = (ROOT / C["twin"]).read_text(encoding="utf-8")
    ca = re.search(r'rel="canonical" href="([^"]+)"', a).group(1)
    if f'href="{ca}"' not in b:
        sys.exit(f"✗ {C['twin']} ไม่ได้ชี้กลับมาที่ {ca}")
print("✓ สองหน้าประกาศฉบับแปลของกันและกันตรงกัน")
