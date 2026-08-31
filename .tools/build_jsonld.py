#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ฝังกราฟความรู้ของเว็บลงในทุกหน้าเป็น JSON-LD   ข้อ 07–08 จากรายงานตรวจก่อนเปิดตัว

ก่อนหน้านี้เว็บทั้งเว็บไม่มี structured data สักบรรทัด ซึ่งเป็นช่องโหว่สองชั้น
ชั้นแรกคือเทคนิค ผลค้นหาไม่มี rich result และ AI ที่มาอ่านต้องเดาเอาเองว่าใครทำอะไร
ชั้นที่สองหนักกว่า สำนักที่ปรึกษาด้านการจัดการความรู้ ที่เว็บตัวเองไม่มีความรู้ที่เครื่องอ่านได้

วิธีที่คนทั่วไปทำคือแปะ Organization ไว้หน้าแรกแล้วจบ ที่นี่ทำอีกแบบ
ประกาศเป็นกราฟเดียวที่ให้ @id กับทุกสิ่งที่เว็บพูดถึง แล้วให้ทุกหน้าอ้างกลับมาที่ id เดิม
  · DefinedTerm ผูกกับหน้าที่นิยามคำนั้นไว้จริง
  · Service สองสายงาน ชี้กลับมาที่ผู้ให้บริการรายเดียวกัน
  · ทุกหน้าประกาศว่าตัวเองพูดถึง entity ตัวไหน ด้วย about
  · คู่ไทย-อังกฤษผูกกันที่ระดับ entity ด้วย translationOfWork ไม่ใช่แค่ hreflang
  · BreadcrumbList ตรงกับโครงสามภาคที่ใช้อยู่จริง
  · FAQPage ในหน้าเกษตรกร ดึงคำถามคำตอบจากเนื้อหาที่มีอยู่แล้ว ไม่ได้เขียนใหม่

ชื่อกับคำอธิบายของแต่ละหน้าดึงจาก <title> และ meta description ของหน้านั้นเอง
จึงไม่มีข้อความใหม่โผล่ขึ้นมาจากสคริปต์นี้ และไม่มีวันขัดกับสิ่งที่หน้าเขียนไว้

รันจากรากรีโป:  python3 .tools/build_jsonld.py
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.neogens.co/"


def U(name):
    return BASE if name == "index.html" else BASE + name


# ---------------------------------------------------------------- โครงสามภาค

PART = {
    "the-problem.html": 1, "what-mkm-is.html": 1, "why-it-works.html": 1,
    "ontology-and-knowledge-graph.html": 1,
    # "สิ่งที่คุณถืออยู่" อยู่ภาค 2 ตามเมนูและป้ายบนหน้าตัวเอง ไม่ใช่ภาค 1
    # เดิมผมจัดไว้ภาค 1 ซึ่งขัดกับที่เหลือ และเพิ่งเห็นตอนเอา breadcrumb ขึ้นหน้า
    "what-you-are-holding.html": 2,
    "mkm-for-museums-and-libraries.html": 2, "visitors-and-readers.html": 2,
    "leadership.html": 2, "services.html": 2, "engagement.html": 2,
    "ai-sovereignty.html": 2, "what-we-wont-do.html": 2,
    "long-read-museums-and-libraries.html": 2, "reference-implementation.html": 2,
    # บทสรุปสำหรับผู้บริหาร เข้ามาเมื่อ 08-31 ดู .tools/build_exec_summary.py
    "exec-summary-museums.html": 2,
    "mkm-for-coffee.html": 3, "coffee-farmer.html": 3, "coffee-demo.html": 3,
    # บทความกาแฟถูกแบ่งเป็นสามภาคเมื่อ 08-22 ดู .tools/split_coffee.py
    "mkm-for-coffee-why-now.html": 3, "mkm-for-coffee-commons.html": 3,
}
PART_NAME = {
    1: ("The idea", "แนวคิด", "the-problem.html"),
    2: ("MKM for Museums & Libraries", "MKM สำหรับพิพิธภัณฑ์และห้องสมุด",
        # หน้าแรกของภาค 2 คือ exec summary ตั้งแต่ 08-31 ไม่ใช่ 01 · สถานะวันนี้
        "exec-summary-museums.html"),
    3: ("MKM for Coffee", "MKM สำหรับกาแฟ", "mkm-for-coffee.html"),
}

# หน้าไหนพูดถึง entity ตัวไหน
ABOUT = {
    "ontology-and-knowledge-graph.html": ["#term-ontology", "#term-kg"],
    "what-mkm-is.html": ["#term-mkm"], "why-it-works.html": ["#term-kg"],
    "the-problem.html": ["#term-mkm"], "what-you-are-holding.html": ["#term-mkm"],
    "ai-sovereignty.html": ["#term-sovereignty"],
    "mkm-for-museums-and-libraries.html": ["#service-museums"],
    "visitors-and-readers.html": ["#service-museums"],
    "leadership.html": ["#service-museums"], "services.html": ["#service-museums"],
    "engagement.html": ["#service-museums"], "what-we-wont-do.html": ["#service-museums"],
    "reference-implementation.html": ["#service-museums"],
    "long-read-museums-and-libraries.html": ["#service-museums", "#term-mkm"],
    "exec-summary-museums.html": ["#service-museums", "#term-mkm", "#term-ontology"],
    "mkm-for-coffee.html": ["#service-coffee"], "coffee-farmer.html": ["#service-coffee"],
    "coffee-demo.html": ["#service-coffee"],
    "mkm-for-coffee-why-now.html": ["#service-coffee"],
    "mkm-for-coffee-commons.html": ["#service-coffee"],
    # หน้านี้พูดถึงการทำ ontology ของเว็บตัวเอง จึงประกาศว่าพูดถึงศัพท์สองคำนั้นจริง
    "seo-as-knowledge-management.html": ["#term-ontology", "#term-mkm"],
}
ARTICLES = {"long-read-museums-and-libraries.html", "mkm-for-coffee.html",
            "th-mkm-for-coffee.html", "seo-as-knowledge-management.html",
            "th-seo-as-knowledge-management.html",
            "mkm-for-coffee-why-now.html", "th-mkm-for-coffee-why-now.html",
            "mkm-for-coffee-commons.html", "th-mkm-for-coffee-commons.html",
            "exec-summary-museums.html", "th-exec-summary-museums.html"}

TERMS = [
    ("#term-mkm", "Modern Knowledge Management", "การบริหารจัดการความรู้สมัยใหม่",
     "what-mkm-is.html"),
    ("#term-ontology", "Ontology", "ontology", "ontology-and-knowledge-graph.html"),
    ("#term-kg", "Knowledge graph", "knowledge graph", "ontology-and-knowledge-graph.html"),
    ("#term-sovereignty", "AI sovereignty", "AI sovereignty", "ai-sovereignty.html"),
]


def menu_label(name):
    """ป้ายที่เมนูใช้เรียกหน้านี้ ตัดเลขลำดับข้างหน้าออก
    ใช้กับขั้นสุดท้ายของ breadcrumb เพราะ breadcrumb คือการนำทาง ควรใช้คำเดียวกับเมนู
    ไม่ใช่ <title> ซึ่งเขียนเพื่อผลค้นหาและมักยาวกว่า"""
    lang = "th" if name.startswith("th-") else "en"
    nav = (ROOT / ".tools" / "shell" / f"nav.{lang}.html").read_text(encoding="utf-8")
    dw = re.search(r'<div class="drawer".*?</nav>', nav, re.S)
    if not dw:
        return None
    m = re.search(r'<a[^>]*href="' + re.escape(name) + r'"[^>]*>([^<]*)</a>', dw.group(0))
    if not m:
        return None
    return re.sub(r"^\s*\d{2}[a-z]?\s*·\s*", "", html.unescape(m.group(1))).strip()


def meta_of(path):
    s = path.read_text(encoding="utf-8")
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    return (html.unescape(t.group(1)).replace(" — Neo Gens", "").strip() if t else "",
            html.unescape(d.group(1)).strip() if d else "")


def faq_nodes(path, page_id):
    """ดึงคำถามคำตอบที่มีอยู่แล้วในหน้า ไม่เขียนใหม่"""
    s = path.read_text(encoding="utf-8")
    anchor = "Questions worth asking first" if not path.name.startswith("th-") \
        else "คำถามที่ควรถามก่อนตัดสินใจ"
    if anchor not in s:
        return None
    i = s.index(anchor)
    j = s.index("<h2", i)
    pairs = re.findall(r"<h\d[^>]*>(.*?)</h\d>\s*<p>(.*?)</p>", s[i:j], re.S)
    strip = lambda x: html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
    if len(pairs) < 3:
        return None
    return {
        "@type": "FAQPage", "@id": page_id + "#faq", "isPartOf": {"@id": page_id},
        "mainEntity": [{"@type": "Question", "name": strip(q),
                        "acceptedAnswer": {"@type": "Answer", "text": strip(a)}}
                       for q, a in pairs],
    }


# ---------------------------------------------------------------- กราฟส่วนกลาง

def shared_graph(lang):
    th = lang == "th"
    org = {
        "@type": "Organization", "@id": BASE + "#org", "name": "Neo Gens",
        "legalName": "Neo Gens Co., Ltd.", "url": BASE,
        "email": "hello@neogens.co",
        "address": {"@type": "PostalAddress", "addressLocality": "Bangkok",
                    "addressCountry": "TH"},
        "knowsAbout": [{"@id": BASE + t[0]} for t in TERMS],
    }
    site = {
        "@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Neo Gens",
        "publisher": {"@id": BASE + "#org"}, "inLanguage": ["en", "th"],
    }
    glossary = {
        "@type": "DefinedTermSet", "@id": BASE + "#glossary",
        "name": "Modern Knowledge Management" if not th
        else "การบริหารจัดการความรู้สมัยใหม่",
        "url": U("ontology-and-knowledge-graph.html" if not th
                 else "th-ontology-and-knowledge-graph.html"),
    }
    terms = [{"@type": "DefinedTerm", "@id": BASE + tid,
              "name": en if not th else t_th,
              "inDefinedTermSet": {"@id": BASE + "#glossary"},
              "url": U(("th-" if th else "") + page)}
             for tid, en, t_th, page in TERMS]
    services = [
        {"@type": "Service", "@id": BASE + "#service-museums",
         "name": "MKM for Museums & Libraries" if not th
         else "MKM สำหรับพิพิธภัณฑ์และห้องสมุด",
         "provider": {"@id": BASE + "#org"},
         "url": U(("th-" if th else "") + "mkm-for-museums-and-libraries.html"),
         "about": [{"@id": BASE + "#term-mkm"}]},
        {"@type": "Service", "@id": BASE + "#service-coffee",
         "name": "MKM for Coffee" if not th else "MKM สำหรับกาแฟ",
         "provider": {"@id": BASE + "#org"},
         "url": U(("th-" if th else "") + "mkm-for-coffee.html"),
         "about": [{"@id": BASE + "#term-mkm"}]},
    ]
    return [org, site, glossary] + terms + services


def page_graph(path):
    name = path.name
    th = name.startswith("th-")
    base_name = name[3:] if th else name
    twin = ("th-" + base_name) if not th else base_name
    pid = U(name)
    title, desc = meta_of(path)

    page = {
        "@type": "WebPage", "@id": pid, "url": pid, "name": title,
        "isPartOf": {"@id": BASE + "#website"},
        "inLanguage": "th" if th else "en",
        "publisher": {"@id": BASE + "#org"},
    }
    if desc:
        page["description"] = desc
    ab = ABOUT.get(base_name)
    if ab:
        page["about"] = [{"@id": BASE + a} for a in ab]
    if (ROOT / twin).exists():
        page["translationOfWork" if th else "workTranslation"] = {"@id": U(twin)}

    nodes = [page]

    part = PART.get(base_name)
    if part:
        pn_en, pn_th, opener = PART_NAME[part]
        crumbs = [(("Neo Gens"), U("th-index.html" if th else "index.html")),
                  ((pn_th if th else pn_en), U(("th-" if th else "") + opener))]
        if base_name != opener:
            crumbs.append((menu_label(name) or title, pid))
        page["breadcrumb"] = {"@id": pid + "#crumbs"}
        nodes.append({
            "@type": "BreadcrumbList", "@id": pid + "#crumbs",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                for i, (n, u) in enumerate(crumbs)],
        })

    if base_name in ARTICLES or name in ARTICLES:
        page["@type"] = ["WebPage", "TechArticle"]
        page["headline"] = title
        page["author"] = {"@id": BASE + "#org"}

    faq = faq_nodes(path, pid)
    if faq:
        nodes.append(faq)
        page["mainEntity"] = {"@id": pid + "#faq"}

    return nodes


# ---------------------------------------------------------------- ลงมือ

BLOCK = re.compile(
    r'[ \t]*<script type="application/ld\+json">.*?</script>\n', re.S)

written, stats = 0, {"faq": 0, "crumbs": 0, "article": 0}
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue
    lang = "th" if path.name.startswith("th-") else "en"
    graph = shared_graph(lang) + page_graph(path)
    blob = json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)
    tag = '<script type="application/ld+json">\n' + blob + "\n</script>\n"

    s = BLOCK.sub("", s)
    if "</head>" not in s:
        sys.exit(f"✗ {path.name} ไม่มี </head>")
    s = s.replace("</head>", tag + "</head>", 1)
    path.write_text(s, encoding="utf-8")
    written += 1
    stats["faq"] += sum(1 for n in graph if n.get("@type") == "FAQPage")
    stats["crumbs"] += sum(1 for n in graph if n.get("@type") == "BreadcrumbList")
    stats["article"] += sum(1 for n in graph
                            if isinstance(n.get("@type"), list) and "TechArticle" in n["@type"])

# ---------------------------------------------------------------- ด่านตรวจ

bad = []
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue
    m = BLOCK.search(s)
    if not m:
        bad.append(f"{path.name} ไม่มี JSON-LD")
        continue
    raw = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1)
    try:
        data = json.loads(raw)
    except Exception as e:
        bad.append(f"{path.name} JSON พัง: {e}")
        continue
    graph = data["@graph"]
    ids = {n["@id"] for n in graph if "@id" in n}
    # ทุก @id ที่ถูกอ้าง ต้องมีตัวจริงอยู่ในกราฟเดียวกัน
    refs = set(re.findall(r'"@id":\s*"([^"]+)"', raw))
    dangling = {r for r in refs if r not in ids and r.startswith(BASE + "#")}
    if dangling:
        bad.append(f"{path.name} อ้าง id ที่ไม่มีในกราฟ: {sorted(dangling)[:2]}")
    # ทุก url ต้องมีไฟล์จริง
    for u in set(re.findall(r'"url":\s*"' + re.escape(BASE) + r'([^"]*)"', raw)):
        if u and not (ROOT / u).exists():
            bad.append(f"{path.name} url ชี้ไฟล์ที่ไม่มี {u}")
    page = next((n for n in graph if n.get("@id") == U(path.name)), None)
    if not page:
        bad.append(f"{path.name} ไม่มี node ของหน้าตัวเอง")
    elif not page.get("name"):
        bad.append(f"{path.name} node ของหน้าไม่มีชื่อ")

print(f"ฝัง JSON-LD {written} หน้า · breadcrumb {stats['crumbs']} · "
      f"FAQ {stats['faq']} · บทความ {stats['article']}")
if bad:
    sys.exit("✗ " + "\n   ".join(bad[:10]))
print("✓ JSON ทุกหน้าอ่านได้ · ทุก @id ที่อ้างมีตัวจริงในกราฟ · ทุก url มีไฟล์จริง")
