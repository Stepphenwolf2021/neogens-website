#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างหน้านโยบายความเป็นส่วนตัว privacy.html และ th-privacy.html

ทุกบรรทัดในหน้านี้มาจากการอ่านโค้ดจริง ไม่ได้คัดลอกแบบสำเร็จรูปมาใส่
  ฟอร์มเก็บอะไร            อ่านจาก <input> ในหน้าเว็บ
  เก็บไว้ที่ไหน นานแค่ไหน   อ่านจาก src/index.js ของ Worker · KV · RETENTION_SECONDS
  ปลายทางภายนอก           ไล่โดเมนทั้งหมดที่หน้าเว็บเรียกออกไป
  คุกกี้                    ค้น document.cookie ทั้งเว็บแล้วไม่มีสักที่

ถ้าเปลี่ยนพฤติกรรมของ Worker หรือใส่ของภายนอกกลับเข้ามา ต้องกลับมาแก้หน้านี้ด้วย
ไม่งั้นนโยบายจะกลายเป็นคำกล่าวอ้างที่ไม่ตรงกับระบบ

ใช้ coffee-farmer.html กับ th-coffee-farmer.html เป็นแม่แบบ เพื่อให้ได้ nav ธีม
footer และ CSS ชุดเดียวกับหน้าอื่นในภาษานั้น

รันจากรากรีโป:  python3 .tools/build_privacy.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPDATED = "19 สิงหาคม 2026"
UPDATED_EN = "19 August 2026"

EN = {
    "src": "coffee-farmer.html", "out": "privacy.html", "twin": "th-privacy.html",
    "lang": "en",
    "title": "Privacy — Neo Gens",
    "desc": "What this site collects, where it goes, how long it is kept, and how to have "
            "it removed. No cookies, no analytics, no third-party scripts.",
    "kicker": "Privacy",
    "h1": "What this site collects, and what it does not",
    "stand": "Short, because there is not much to say. This site sets no cookies, runs no "
             "analytics, and loads no third-party scripts. The only personal data it "
             "handles is what you type into the briefing form yourself.",
    "meta": f"updated {UPDATED_EN}",
    "body": [
        ("h2", "What we collect"),
        ("p", "Only what you enter in the form: your name, your email address, your "
              "organisation, and your country. On the coffee pages, the form also records "
              "which topic you wrote in about. Nothing else is collected from you, and "
              "there is no form anywhere on this site that asks for more."),
        ("p", "Alongside your entry we store the page you sent it from, the language you "
              "were reading in, the browser you used, and the country code our network "
              "provider derives from the connection. We do not store your IP address."),
        ("h2", "What we do with it"),
        ("p", "We reply to you. That is the whole purpose. Your details are not used for "
              "anything else, are never sold, and are never passed to an advertiser or a "
              "data broker."),
        ("h2", "Where it goes"),
        ("p", "The form sends your entry to our own endpoint running on Cloudflare "
              "Workers, where it is stored, and an email notification is delivered through "
              "Resend. The site itself is hosted on GitHub Pages. Typefaces are served by "
              "Google Fonts, which means Google receives your IP address when a page "
              "loads — we are moving those files onto our own domain to end that."),
        ("h2", "How long we keep it"),
        ("p", "Twenty-four months, after which the record is deleted automatically. The "
              "counter that stops the form being submitted repeatedly from one network "
              "holds an IP address for at most two hours and then expires on its own — it "
              "is never attached to your entry."),
        ("h2", "What this site does not do"),
        ("ul", ["It sets no cookies at all.",
                "It runs no analytics and no tracking of any kind.",
                "It loads no third-party JavaScript.",
                "It does not build a profile of you, and cannot follow you to other sites.",
                "Your dark or light theme choice is kept in your own browser and is never "
                "sent anywhere."]),
        ("h2", "Your rights"),
        ("p", "Under Thailand's Personal Data Protection Act you may ask to see what we "
              "hold about you, to correct it, to have it deleted, or to withdraw consent. "
              "Write to us and we will act on it. There is no form to fill in and no "
              "process to go through — an email is enough."),
        ("h2", "Getting in touch"),
        ("p", "Write to <a href=\"mailto:hello@neogens.co\">hello@neogens.co</a>. We are "
              "Neo Gens Co., Ltd., in Bangkok, Thailand."),
        ("h2", "Changes"),
        ("p", f"This page was last updated on {UPDATED_EN}. If what we collect changes, "
              "this page changes with it on the same day — a privacy policy that describes "
              "a system that no longer exists is worse than none."),
    ],
    "join_k": "Your data",
    "join_h": "Want to see what we hold, or have it deleted?",
    "join_p": "Write to hello@neogens.co and we will act on it. Or use the form below.",
}

TH = {
    "src": "th-coffee-farmer.html", "out": "th-privacy.html", "twin": "privacy.html",
    "lang": "th",
    "title": "ความเป็นส่วนตัว — Neo Gens",
    "desc": "เว็บนี้เก็บอะไร ข้อมูลไปอยู่ที่ไหน เก็บไว้นานแค่ไหน และขอให้ลบได้อย่างไร "
            "ไม่มีคุกกี้ ไม่มีการวัดผลการเข้าชม ไม่มีสคริปต์จากภายนอก",
    "kicker": "ความเป็นส่วนตัว",
    "h1": "เว็บนี้เก็บอะไร และไม่เก็บอะไร",
    "stand": "หน้านี้สั้น เพราะไม่มีอะไรให้พูดมาก เว็บนี้ไม่ตั้งคุกกี้ ไม่มีการวัดผลการเข้าชม "
             "และไม่โหลดสคริปต์จากภายนอกเลยสักตัว ข้อมูลส่วนบุคคลอย่างเดียวที่ระบบนี้ถือไว้ "
             "คือสิ่งที่คุณพิมพ์ลงในฟอร์มด้วยตัวเอง",
    "meta": f"ปรับปรุง {UPDATED}",
    "body": [
        ("h2", "เก็บอะไรบ้าง"),
        ("p", "เฉพาะสิ่งที่คุณกรอกในฟอร์ม — ชื่อ อีเมล องค์กร และประเทศ ในหน้ากลุ่มกาแฟ "
              "ฟอร์มจะบันทึกด้วยว่าคุณติดต่อมาเรื่องอะไร นอกจากนี้ไม่มีอะไรถูกเก็บจากคุณอีก "
              "และไม่มีฟอร์มไหนในเว็บนี้ที่ถามมากกว่านั้น"),
        ("p", "พร้อมกับสิ่งที่คุณกรอก ระบบเก็บว่าคุณส่งมาจากหน้าไหน อ่านอยู่ในภาษาใด "
              "ใช้เบราว์เซอร์อะไร และรหัสประเทศที่ผู้ให้บริการเครือข่ายของเราอ่านได้จากการเชื่อมต่อ "
              "เราไม่เก็บหมายเลข IP ของคุณ"),
        ("h2", "เอาไปทำอะไร"),
        ("p", "ตอบกลับคุณ เท่านั้น ข้อมูลของคุณไม่ถูกใช้ทำอย่างอื่น ไม่ถูกขาย "
              "และไม่ถูกส่งต่อให้ผู้ลงโฆษณาหรือคนกลางซื้อขายข้อมูลไม่ว่ากรณีใด"),
        ("h2", "ข้อมูลไปอยู่ที่ไหน"),
        ("p", "ฟอร์มส่งสิ่งที่คุณกรอกไปยังปลายทางของเราเองที่ทำงานอยู่บน Cloudflare Workers "
              "และเก็บไว้ที่นั่น แล้วส่งอีเมลแจ้งเตือนผ่าน Resend ตัวเว็บโฮสต์อยู่บน GitHub Pages "
              "ส่วนฟอนต์ตอนนี้เรียกจาก Google Fonts ซึ่งแปลว่า Google ได้รับหมายเลข IP ของคุณ "
              "ตอนหน้าเว็บโหลด — เรากำลังย้ายไฟล์ฟอนต์มาไว้บนโดเมนของเราเองเพื่อยุติเรื่องนี้"),
        ("h2", "เก็บไว้นานแค่ไหน"),
        ("p", "ยี่สิบสี่เดือน แล้วเรคอร์ดจะถูกลบเองโดยอัตโนมัติ ส่วนตัวนับที่กันไม่ให้ส่งฟอร์มซ้ำ "
              "ถี่เกินไปจากเครือข่ายเดียวกัน จะถือหมายเลข IP ไว้ไม่เกินสองชั่วโมงแล้วหมดอายุไปเอง "
              "และไม่เคยถูกผูกเข้ากับสิ่งที่คุณกรอกไว้"),
        ("h2", "สิ่งที่เว็บนี้ไม่ทำ"),
        ("ul", ["ไม่ตั้งคุกกี้เลยแม้แต่ตัวเดียว",
                "ไม่มีการวัดผลการเข้าชม และไม่มีการติดตามใด ๆ ทั้งสิ้น",
                "ไม่โหลด JavaScript จากภายนอก",
                "ไม่สร้างโปรไฟล์ของคุณ และตามคุณไปเว็บอื่นไม่ได้",
                "การเลือกธีมมืดหรือสว่างเก็บไว้ในเบราว์เซอร์ของคุณเอง ไม่ถูกส่งไปที่ไหน"]),
        ("h2", "สิทธิของคุณ"),
        ("p", "ตามพระราชบัญญัติคุ้มครองข้อมูลส่วนบุคคล คุณขอดูข้อมูลที่เราถือไว้ได้ "
              "ขอแก้ไข ขอให้ลบ หรือถอนความยินยอมได้ เขียนมาบอกแล้วเราจัดการให้ "
              "ไม่มีแบบฟอร์มให้กรอกและไม่มีขั้นตอนให้เดิน อีเมลฉบับเดียวพอ"),
        ("h2", "ติดต่อเรา"),
        ("p", "เขียนมาที่ <a href=\"mailto:hello@neogens.co\">hello@neogens.co</a> "
              "เราคือบริษัท นีโอ เจนส์ จำกัด อยู่ที่กรุงเทพมหานคร"),
        ("h2", "การเปลี่ยนแปลง"),
        ("p", f"หน้านี้ปรับปรุงล่าสุดเมื่อ {UPDATED} ถ้าสิ่งที่เก็บเปลี่ยนไป "
              "หน้านี้จะเปลี่ยนตามในวันเดียวกัน — นโยบายที่บรรยายระบบซึ่งไม่มีอยู่แล้ว "
              "แย่กว่าการไม่มีนโยบายเลย"),
    ],
    "join_k": "ข้อมูลของคุณ",
    "join_h": "อยากดูว่าเราถืออะไรไว้ หรืออยากให้ลบ",
    "join_p": "เขียนมาที่ hello@neogens.co แล้วเราจัดการให้ หรือใช้ฟอร์มด้านล่างก็ได้",
}

LANG_BLOCK = re.compile(r'<span class="lang">.*?</span>(?=<button)', re.S)
ALT_BLOCK = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n')
BASE = "https://www.neogens.co/"


def article(C):
    out = ['<article>', '  <div class="wrap">']
    for kind, val in C["body"]:
        if kind == "ul":
            out.append("    <ul>" + "".join(f"<li>{x}</li>" for x in val) + "</ul>")
        else:
            out.append(f"    <{kind}>{val}</{kind}>")
    out += ["  </div>", "</article>"]
    return "\n".join(out)


def build(C):
    src, out = ROOT / C["src"], ROOT / C["out"]
    s = src.read_text(encoding="utf-8")

    s = re.sub(r"<title>.*?</title>", f"<title>{C['title']}</title>", s, count=1, flags=re.S)
    for tag in ('<meta name="description" content="', '<meta property="og:description" content="'):
        s = s.replace(tag + re.search(re.escape(tag) + r'([^"]*)"', s).group(1), tag + C["desc"], 1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*"', r"\1" + C["title"] + '"', s, count=1)
    for old in ("coffee-farmer.html", "th-coffee-farmer.html"):
        s = s.replace(f"{BASE}{old}", f"{BASE}{C['out']}")

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

    m = re.search(r'<div class="kicker">.*?</div>\s*</div>\s*</header>', s, re.S)
    s = s[:m.start()] + (
        f'<div class="kicker">{C["kicker"]}</div>\n'
        f'      <h1>{C["h1"]}</h1>\n'
        f'      <p class="stand">{C["stand"]}</p>\n'
        f'      <div class="meta"><span>Neo Gens</span><span>{C["meta"]}</span></div>\n'
        f'    </div>\n  </div>\n</header>') + s[m.end():]

    i, j = s.index("<article>"), s.index("</article>") + len("</article>")
    s = s[:i] + article(C) + s[j:]

    s = re.sub(r'(<div class="k rv">)[^<]*(</div>)', lambda x: x.group(1) + C["join_k"] + x.group(2), s, count=1)
    s = re.sub(r'(<section class="join".*?<h2 class="rv">)[^<]*(</h2>)',
               lambda x: x.group(1) + C["join_h"] + x.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<p class="lead rv">)[^<]*(</p>)', lambda x: x.group(1) + C["join_p"] + x.group(2), s, count=1)

    # ---- ด่านตรวจ ----
    checks = {
        "หัวข้อครบตามที่เขียนไว้": s.count("<h2>") == sum(1 for k, _ in C["body"] if k == "h2"),
        "ย่อหน้าครบตามที่เขียนไว้": s.count("<p>") >= sum(1 for k, _ in C["body"] if k == "p"),
        "หัวข้อหลักถูกภาษา": f"<h1>{C['h1']}</h1>" in s,
        "รายการสิ่งที่ไม่ทำ 5 ข้อ": s.count("<li>") >= 5,
        "canonical ชี้หน้านี้": f'rel="canonical" href="{BASE}{C["out"]}"' in s,
        "hreflang ชี้คู่ถูก": (f'hreflang="en" href="{BASE}{en_page}"' in s and
                              f'hreflang="th" href="{BASE}{th_page}"' in s),
        "ปุ่มสลับภาษาสองชุด": n_lang == 2,
        "ไม่เหลือเนื้อหาแม่แบบ": "ความรู้ที่อยู่ในหัวคุณ" not in s and "What you know about your own plot" not in s,
        "ไม่มีสคริปต์ภายนอก": "googletagmanager" not in s,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"[abort] {C['out']}: " + ", ".join(bad))

    out.write_text(s, encoding="utf-8")
    print(f"  สร้าง {out.name} · {len(s.encode()) // 1024} KB · ตรวจครบ {len(checks)} ข้อ")


for C in (EN, TH):
    build(C)

# ---------------------------------------------------------------- ลิงก์ใน footer

# แถบท้าย footer มีสองแบบในเว็บนี้ บางหน้าเป็น class="f-bot" เฉย ๆ
# บางหน้าเป็น class="wrap f-bot" และมีกล่อง span.f-links รวมลิงก์ไว้ข้างใน
FBOT = re.compile(r'<div class="[^"]*\bf-bot\b[^"]*">(.*?)</div>', re.S)
FLINKS = re.compile(r'(<span class="f-links">)(.*?)(</span>)', re.S)

added, already, skipped = 0, 0, []
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue
    th = path.name.startswith("th-")
    target = ("th-" if th else "") + "privacy.html"
    link = f'<a href="{target}">{"ความเป็นส่วนตัว" if th else "Privacy"}</a>'

    m = FBOT.search(s)
    if not m:
        skipped.append(path.name)
        continue
    if link in m.group(1):
        already += 1
        continue

    inner = m.group(1)
    fl = FLINKS.search(inner)
    if fl:
        new_inner = inner[:fl.end(2)] + link + inner[fl.end(2):]
    else:
        new_inner = inner + link
    s = s[:m.start(1)] + new_inner + s[m.end(1):]
    path.write_text(s, encoding="utf-8")
    added += 1

# ---- ด่านตรวจ ทุกหน้าจริงต้องมีลิงก์ และต้องชี้ฉบับภาษาเดียวกับหน้า ----
bad = []
for path in sorted(ROOT.glob("*.html")):
    s = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or path.name == "404.html":
        continue
    want = ("th-" if path.name.startswith("th-") else "") + "privacy.html"
    if f'href="{want}"' not in s:
        bad.append(f"{path.name} ไม่มีลิงก์ไป {want}")

print(f"เพิ่มลิงก์ในแถบท้าย footer {added} หน้า · มีอยู่แล้ว {already} หน้า")
if skipped:
    print("  ไม่มีแถบท้าย footer:", ", ".join(skipped))
if bad:
    sys.exit("✗ " + " · ".join(bad[:8]))
print("✓ ทุกหน้ามีลิงก์นโยบายความเป็นส่วนตัว และชี้ฉบับภาษาเดียวกับหน้า")
