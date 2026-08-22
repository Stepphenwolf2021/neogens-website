#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างหน้า seo-as-knowledge-management.html และฉบับไทย

หน้านี้เป็นข้อโต้แย้งต่อสาธารณะว่า SEO คือการบริหารจัดการความรู้รูปแบบหนึ่ง
สำนักที่ปรึกษาด้านการจัดการความรู้จึงต้องทำของตัวเองให้ถูก และเปิดให้ตรวจได้
เนื้อหาอยู่ใน .tools/copy_evidence.py ตัวเลขทุกตัวนับจากไฟล์จริง ดูหัวไฟล์นั้นว่านับจากไหน

ใช้ coffee-farmer.html กับ th-coffee-farmer.html เป็นแม่แบบ เหมือนที่ build_privacy.py ทำ
จะได้ nav ธีม footer ฟอร์ม และ CSS ชุดเดียวกับหน้าอื่นในภาษานั้น

หน้านี้ไม่อยู่ในโครงสามภาค เหมือน about.html และ privacy.html จึงไม่มี BreadcrumbList
รันซ้ำได้ ผลลัพธ์เท่าเดิม เพราะสร้างจากแม่แบบใหม่ทุกครั้ง ไม่ได้แก้ไฟล์เดิมทับ

รันจากรากรีโป:  python3 .tools/build_evidence.py
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copy_evidence import CLAIMS, CSS, FACTS, LANGS, SPELLED, WORDS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.neogens.co/"

LANG_BLOCK = re.compile(r'<span class="lang">.*?</span>(?=<button)', re.S)
ALT_BLOCK = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n')
JSONLD_BLOCK = re.compile(
    r'[ \t]*<script type="application/ld\+json">.*?</script>\n', re.S)
CRUMBS_BLOCK = re.compile(r'[ \t]*<nav class="crumbs".*?</nav>\n', re.S)
TEMPLATE_MARKS = ("What you know about your own plot", "ความรู้ที่อยู่ในหัวคุณ",
                  "Questions worth asking first", "คำถามที่ควรถามก่อนตัดสินใจ")


def article(C):
    out = ["<article>", '  <div class="wrap">']
    for kind, val in C["body"]:
        if kind == "raw":                      # ภาพและตารางผลตรวจ ส่งเป็น HTML ตรง ๆ
            out.append("    " + val)
        elif kind == "ul":
            out.append("    <ul>" + "".join(f"<li>{x}</li>" for x in val) + "</ul>")
        else:
            out.append(f"    <{kind}>{val}</{kind}>")
    out += ["  </div>", "</article>"]
    return "\n".join(out)


def build(C):
    src, out = ROOT / C["src"], ROOT / C["out"]
    s = src.read_text(encoding="utf-8")

    # ---- หัวเรื่องและ meta ----
    s = re.sub(r"<title>.*?</title>", f"<title>{C['title']}</title>", s, count=1, flags=re.S)
    for tag in ('<meta name="description" content="',
                '<meta property="og:description" content="'):
        cur = re.search(re.escape(tag) + r'([^"]*)"', s).group(1)
        s = s.replace(tag + cur, tag + C["desc"], 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*"',
               r"\1" + C["title"] + '"', s, count=1)
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
    s = s[:m.start()] + (
        f'<div class="kicker">{C["kicker"]}</div>\n'
        f'      <h1>{C["h1"]}</h1>\n'
        f'      <p class="stand">{C["stand"]}</p>\n'
        f'      <div class="meta"><span>Neo Gens</span><span>{C["meta"]}</span></div>\n'
        f'    </div>\n  </div>\n</header>') + s[m.end():]

    # ---- เนื้อหา ----
    i, j = s.index("<article>"), s.index("</article>") + len("</article>")
    s = s[:i] + article(C) + s[j:]

    # ---- ของที่ติดมากับแม่แบบและไม่ใช่ของหน้านี้ ----
    # JSON-LD กับแถบเส้นทางของ coffee-farmer พูดถึงหน้านั้น ไม่ใช่หน้านี้
    # ทิ้งไว้จะกลายเป็นหน้าที่ประกาศตัวเองผิด ซึ่งเป็นความผิดที่หน้านี้เขียนถึงพอดี
    # JSON-LD ที่ถูกต้อง build_jsonld.py จะใส่กลับให้ตอนท้ายสคริปต์นี้
    # หน้านี้ไม่อยู่ในโครงสามภาค จึงไม่มีแถบเส้นทาง เหมือน about.html และ privacy.html
    s = JSONLD_BLOCK.sub("", s)
    s = CRUMBS_BLOCK.sub("", s)

    # ---- CSS ของภาพและตารางผลตรวจ แม่แบบไม่มีคลาสพวกนี้ ต้องเติมเอง ----
    if "</style>" not in s:
        sys.exit(f"[abort] {C['out']} ไม่มีบล็อก style ให้เติม CSS")
    s = s.replace("</style>", CSS[C["lang"]] + "</style>", 1)

    # ---- กล่องชวนคุยท้ายหน้า ----
    s = re.sub(r'(<div class="k rv">)[^<]*(</div>)',
               lambda x: x.group(1) + C["join_k"] + x.group(2), s, count=1)
    s = re.sub(r'(<section class="join".*?<h2 class="rv">)[^<]*(</h2>)',
               lambda x: x.group(1) + C["join_h"] + x.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<p class="lead rv">)[^<]*(</p>)',
               lambda x: x.group(1) + C["join_p"] + x.group(2), s, count=1)

    # ---- ด่านตรวจ เขียนไฟล์ต่อเมื่อผ่านครบ ----
    n_h2 = sum(1 for k, _ in C["body"] if k == "h2")
    n_p = sum(1 for k, _ in C["body"] if k == "p")
    n_li = sum(len(v) for k, v in C["body"] if k == "ul")
    checks = {
        "หัวข้อครบตามที่เขียนไว้": s.count("<h2>") == n_h2,
        "ย่อหน้าครบตามที่เขียนไว้": s.count("<p>") >= n_p,
        "รายการครบตามที่เขียนไว้": s.count("<li>") >= n_li,
        "พาดหัวถูกภาษา": f"<h1>{C['h1']}</h1>" in s,
        "มี h1 เดียว": s.count("<h1>") == 1,
        "title ไม่เกิน 60": len(C["title"]) <= 60,
        "description ไม่เกิน 160": len(C["desc"]) <= 160,
        "og:description ตรงกับ description": s.count(C["desc"]) >= 2,
        "canonical ชี้หน้านี้": f'rel="canonical" href="{BASE}{C["out"]}"' in s,
        "hreflang ชี้คู่ถูก": (f'hreflang="en" href="{BASE}{en_page}"' in s and
                              f'hreflang="th" href="{BASE}{th_page}"' in s and
                              f'hreflang="x-default" href="{BASE}{en_page}"' in s),
        "ปุ่มสลับภาษาสองชุด": n_lang == 2,
        "ไม่เหลือเนื้อหาแม่แบบ": not any(t in s for t in TEMPLATE_MARKS),
        "คำบรรยายภาพมีกฎของตัวเอง": "\nfigcaption{" in s,
        "CSS ของภาพเข้าไฟล์แล้ว": ".dsvg{" in s and s.index(".dsvg{") < s.index("</style>"),
        "CSS ของตารางเข้าไฟล์แล้ว": ".rr{" in s and s.index(".rr{") < s.index("</style>"),
        "ทุกคลาสในภาพมีกฎรองรับ": all(
            (c + "{") in s for c in re.findall(r'class="(m-am|m-go|m-as|m|t-b|t-s|bx-go|bx-as|bx|ln-gh|ln)"', s)
            for c in ["." + c]),
        "ภาพมีคำบรรยายให้โปรแกรมอ่านหน้าจอ": s.count('role="img"') == 1 and 'aria-label="' in s,
        "ตารางกว้างเกินแล้วเลื่อนได้": s.count('class="rr-scroll"') == 1,
        "ไม่เหลือ JSON-LD ของแม่แบบ": "application/ld+json" not in s,
        "ไม่เหลือแถบเส้นทางของแม่แบบ": 'class="crumbs"' not in s,
        "ไม่มีของภายนอก": not re.search(r'(src|href)="https?://(?!www\.neogens\.co)', s),
        "ลิงก์ในหน้าไปไฟล์ที่มีจริง": all(
            (ROOT / h).exists()
            for h in re.findall(r'href="([a-z0-9][a-z0-9.-]*\.html)"', s)
            if h not in (C["twin"], C["out"])),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"[abort] {C['out']}: " + " · ".join(bad))

    out.write_text(s, encoding="utf-8")
    print(f"  สร้าง {out.name} · {len(s.encode()) // 1024} KB · ตรวจผ่าน {len(checks)} ข้อ")


for C in LANGS:
    build(C)

# ---- คู่ภาษาต้องยืนยันกลับหากัน อ่านจากไฟล์ที่เขียนเสร็จแล้วทั้งคู่ ----
for C in LANGS:
    a = (ROOT / C["out"]).read_text(encoding="utf-8")
    b = (ROOT / C["twin"]).read_text(encoding="utf-8")
    ca = re.search(r'rel="canonical" href="([^"]+)"', a).group(1)
    if f'href="{ca}"' not in b:
        sys.exit(f"✗ {C['twin']} ไม่ได้ชี้กลับมาที่ {ca}")
print("✓ สองหน้าประกาศฉบับแปลของกันและกันตรงกัน")


# ---- ตัวเลขในหน้าต้องตรงกับไฟล์จริง ไม่ใช่กับสิ่งที่จำได้ ----
# หน้านี้ทั้งหน้าตั้งอยู่บนคำว่าตรวจสอบได้ ตัวเลขที่ค้างจึงไม่ใช่เรื่องเล็ก
# นับใหม่ทุกครั้งที่รัน แล้วเทียบกับ FACTS ถ้าไม่ตรงให้หยุด อย่าเขียนไฟล์

def live_facts():
    import json
    pages = nodes = 0
    for f in sorted(ROOT.glob("*.html")):
        t = f.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in t:
            continue
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
        if m:
            pages += 1
            nodes += len(json.loads(m.group(1))["@graph"])
    idx = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',
                               (ROOT / "index.html").read_text(encoding="utf-8"),
                               re.S).group(1))["@graph"]
    return {
        "pages": pages,
        "nodes": nodes,
        "fonts": len(list((ROOT / "assets" / "fonts").glob("*.woff2"))),
        "stubs": sum('http-equiv="refresh"' in f.read_text(encoding="utf-8")
                     for f in ROOT.glob("*.html")),
        "terms": sum(n.get("@type") == "DefinedTerm" for n in idx),
        **_type_pages(),
    }


def _type_pages():
    """นับว่าแต่ละชนิดถูกประกาศอยู่กี่หน้า ตัวเลขนี้ไปโผล่ในเนื้อหาหน้าโดยตรง"""
    import json
    want = {"org": "Organization", "crumbs": "BreadcrumbList",
            "article": "TechArticle", "faq": "FAQPage"}
    got = {k: 0 for k in want}
    for f in sorted(ROOT.glob("*.html")):
        t = f.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in t:
            continue
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
        if not m:
            continue
        seen = set()
        for n in json.loads(m.group(1))["@graph"]:
            ty = n.get("@type")
            seen.update(ty if isinstance(ty, list) else [ty])
        for k, v in want.items():
            got[k] += v in seen
    return got


# เมนูที่ติดมากับแม่แบบยังชี้ว่าหน้านี้คือ coffee-farmer อยู่ ต้องซิงก์ใหม่ก่อน
# แล้วค่อยฝัง JSON-LD เพราะกราฟดึงป้ายเมนูไปใช้
for tool in ("sync_nav.py", "build_jsonld.py"):
    subprocess.run([sys.executable, str(Path(__file__).with_name(tool))],
                   check=True, cwd=ROOT)

# ---- หน้านี้ต้องไม่ประกาศว่าตัวเองเป็นหน้าอื่น ----
for C in LANGS:
    t = (ROOT / C["out"]).read_text(encoding="utf-8")
    for m in re.finditer(r'<a[^>]*aria-current="page"[^>]*href="([^"]+)"', t):
        if m.group(1) != C["out"]:
            sys.exit(f"✗ {C['out']} เมนูชี้ว่าหน้าปัจจุบันคือ {m.group(1)}")
    for m in re.finditer(r'<a[^>]*href="([^"]+)"[^>]*aria-current="page"', t):
        if m.group(1) != C["out"]:
            sys.exit(f"✗ {C['out']} เมนูชี้ว่าหน้าปัจจุบันคือ {m.group(1)}")

live = live_facts()
off = {k: (v, live[k]) for k, v in FACTS.items() if live[k] != v}
if off:
    sys.exit("✗ ตัวเลขในหน้าไม่ตรงกับไฟล์จริง แก้ FACTS และคำในเนื้อหาก่อน · "
             + " · ".join(f"{k} เขียนไว้ {a} ของจริง {b}" for k, (a, b) in off.items()))

for C in LANGS:
    t = (ROOT / C["out"]).read_text(encoding="utf-8")
    # ตัวเลขบางตัวขึ้นต้นประโยค จึงเทียบแบบไม่สนตัวพิมพ์ใหญ่เล็ก
    low = t.lower()
    missing = [f"{k}={FACTS[k]}" for k in SPELLED
               if WORDS[C["lang"]][FACTS[k]].lower() not in low]
    # ประโยคที่อ้างจำนวนหน้าตามชนิด ประกอบขึ้นจากค่าที่นับได้จริงแล้วต้องเจอในหน้า
    missing += [c.format(**live) for c in CLAIMS[C["lang"]]
                if c.format(**live) not in t]
    if missing:
        sys.exit(f"✗ {C['out']} ตัวเลขในเนื้อหาไม่ตรง: " + " · ".join(missing))
print("✓ ตัวเลขที่หน้านี้อ้าง ตรงกับที่นับได้จากไฟล์จริงทั้ง "
      + " ".join(f"{k}={v}" for k, v in FACTS.items()))
