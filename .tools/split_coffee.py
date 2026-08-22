#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
แบ่งบทความกาแฟ 4,436 คำ ออกเป็นสามภาค   สั่งเมื่อ 2026-08-22

จุดตัดตามเส้นเหตุผลของบทความ ทำไม · อย่างไร · แล้วไงต่อ

    ภาค 1  s01–s03  mkm-for-coffee.html            URL เดิม ไม่เปลี่ยน
    ภาค 2  s04–s07  mkm-for-coffee-why-now.html
    ภาค 3  s08–s10  mkm-for-coffee-commons.html

**เนื้อหาเป็นคำของ Noppadol ย้ายบล็อกอย่างเดียว ห้ามแก้แม้แต่ตัวเดียว** (LESSONS ข้อ 3)
คำใหม่ที่หน้าใหม่จำเป็นต้องมี — title · ป้ายภาค · ปุ่มก่อนหน้า/ถัดไป — ยกมาจากหัวข้อ h2
ของเขาเองทั้งหมด ไม่ได้แต่งขึ้น ส่วน meta description ตัดที่ขอบวรรคของย่อหน้าแรก
หลักเดียวกับ fix_meta.py คือไม่เขียนใหม่ ตัดคำเดิม

## ต้นฉบับอยู่ที่ไหน

`build_coffee.py` รันไม่ได้แล้ว — ชี้ไปที่ sandbox ที่ตายไปแล้ว และไฟล์บทความต้นทาง
ไม่ได้อยู่ในรีโป สคริปต์นี้จึงเก็บ **ฉบับเต็มก่อนแบ่ง** ไว้ที่ `.tools/coffee-source/`
แล้วสร้างทั้งสามภาคจากที่นั่นทุกครั้ง รันซ้ำได้ ไม่กัดกินตัวเอง
ถ้าจะแก้เนื้อหาบทความ ให้แก้ที่ต้นฉบับในโฟลเดอร์นั้น แล้วรันสคริปต์นี้ใหม่

## สิ่งที่ทุกภาคต้องมี ห้ามตัดทิ้ง

สคริปต์ท้ายหน้าเรียก `getElementById('nav')` กับ `('prog')` โดยไม่เช็ก null
ถ้าหน้าไหนขาดสองตัวนี้ IIFE จะตายทั้งก้อน แล้ว `.rv` ทุกชิ้นค้างที่ `opacity:0`
คือหน้าขาวทั้งหน้าโดยไม่มี error ให้เห็น ด่านตรวจท้ายไฟล์จึงเช็กสองตัวนี้ทุกหน้า

`.artbody > .figplate` เป็น selector ลูกตรง ห้ามใส่ตัวครอบเพิ่มระหว่างสองชั้นนี้
ไม่งั้นรูปกับการ์ดจะหดจากคอลัมน์กว้างมาเป็นคอลัมน์เนื้อความเงียบ ๆ

รันจากรากรีโป:  python3 .tools/split_coffee.py
"""
import html
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".tools" / "coffee-source"
PN_DONOR = "mkm-for-museums-and-libraries.html"      # หน้าที่มีกฎ CSS ของปุ่มก่อนหน้า/ถัดไป

MARK_A = "/* >>> ปุ่มก่อนหน้า/ถัดไป · split_coffee.py >>> */"
MARK_B = "/* <<< ปุ่มก่อนหน้า/ถัดไป <<< */"

# ภาค → (ชื่อไฟล์ฐาน, หัวข้อที่อยู่ในภาคนี้)
PARTS = [
    ("mkm-for-coffee.html", ["s01", "s02", "s03"]),
    ("mkm-for-coffee-why-now.html", ["s04", "s05", "s06", "s07"]),
    ("mkm-for-coffee-commons.html", ["s08", "s09", "s10"]),
]
WORDS = {
    "en": {"part": "Part {} of 3", "prev": "Previous", "next": "Next"},
    "th": {"part": "ภาค {} จาก 3", "prev": "ก่อนหน้า", "next": "ถัดไป"},
}


def name(base, lang):
    return base if lang == "en" else "th-" + base


def keep_name(lang):
    """ต้นฉบับลงท้าย .html.src ไม่ใช่ .html โดยตั้งใจ

    `.tools/` ทั้งโฟลเดอร์ถูกเสิร์ฟออกเว็บ ถ้าเก็บเป็น .html จะกลายเป็นบทความฉบับเต็ม
    อีกชุดที่คนและบอตเปิดได้ แล้วไปแย่งอันดับกับสามภาคที่ตั้งใจให้เป็นของจริง
    นามสกุลนี้ทำให้เซิร์ฟเวอร์ไม่เสิร์ฟเป็นหน้าเว็บ
    """
    return name("mkm-for-coffee.html", lang) + ".src"


def snapshot():
    """เก็บฉบับเต็มไว้ครั้งแรกที่รัน แล้วใช้เป็นต้นฉบับตลอดไป"""
    SRC.mkdir(parents=True, exist_ok=True)
    for lang in ("en", "th"):
        n = name("mkm-for-coffee.html", lang)
        keep = SRC / keep_name(lang)
        if keep.exists():
            continue
        live = ROOT / n
        s = live.read_text(encoding="utf-8")
        found = re.findall(r'<h2 class="rv" id="s(\d\d)"', s)
        if found != [f"{i:02d}" for i in range(1, 11)]:
            sys.exit(f"✗ {n} ไม่ใช่ฉบับเต็ม เจอหัวข้อ {found} — ไม่เก็บเป็นต้นฉบับ")
        shutil.copy2(live, keep)
        print(f"  เก็บต้นฉบับ {keep.relative_to(ROOT)}")


def rules_of(css):
    """ตัด CSS เป็นกฎทีละก้อนโดยนับวงเล็บปีกกา ไม่ใช่ด้วย regex

    regex ตัดกฎธรรมดาได้ แต่ตัด @media ไม่ได้ เพราะมันซ้อนอีกชั้น
    รอบแรกผมใช้ regex แล้วได้ @media ที่ขาดปีกกาปิด ไปกลืนกฎทุกข้อที่ตามหลัง
    เข้าไปอยู่ในเงื่อนไข max-width:640px — เมนูย่อยบนจอกว้างเลยกางค้าง ดู LESSONS ข้อ 11
    """
    out, buf, depth = [], "", 0
    for ch in css:
        buf += ch
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(buf.strip())
                buf = ""
    return [r for r in out if r]


def pn_css():
    """ยกกฎ CSS ของปุ่มก่อนหน้า/ถัดไปมาจากหน้าที่ใช้อยู่จริง ไม่เขียนใหม่ให้ต่างกัน"""
    s = (ROOT / PN_DONOR).read_text(encoding="utf-8")
    st = "".join(re.findall(r"<style[^>]*>(.*?)</style>", s, re.S))
    rules = [r for r in rules_of(st) if re.search(r"(^|[\s,{])\.pn[\s.:,{a-z-]", r)]
    if not rules:
        sys.exit(f"✗ หากฎ .pn ใน {PN_DONOR} ไม่เจอ")
    block = MARK_A + "\n" + "\n".join(rules) + "\n" + MARK_B
    if block.count("{") != block.count("}"):
        sys.exit(f"✗ กฎ .pn ที่ยกมาปีกกาไม่สมดุล เปิด {block.count('{')} ปิด {block.count('}')}")
    return block


def cut(s):
    """แยกไฟล์ออกเป็นชิ้นที่ประกอบกลับได้ คืน (หัว, แผนที่, สารบัญ, {sid: html}, ท้าย)"""
    # หัวต้องจบก่อน <article> เพราะสคริปต์ประกอบ <article> ขึ้นใหม่เอง
    # ถ้าตัดหัวเลยเข้าไปถึง .artbody จะได้ <article> ซ้อนกันสองชั้น แล้วแผนที่ตกไปอยู่ข้างใน
    a = s.index("<article>")
    i = s.index('<div class="artbody">', a) + len('<div class="artbody">')
    j = s.index("</article>")
    # ก่อน </article> มี </div> สองตัว ตัวท้ายปิด .wrap ตัวรองปิด .artbody
    # ต้องหยุดที่ตัวรอง ถ้าเอาตัวท้าย </div> ของ .artbody จะติดมากับหัวข้อสุดท้าย
    # แล้วเฉพาะภาคที่มีหัวข้อนั้นจะมีแท็กปิดเกินหนึ่งตัว — check.py จับได้ ผมไม่ทันเห็นเอง
    end = s.rindex("</div>", i, s.rindex("</div>", i, j))
    head, body, tail = s[:a], s[i:end], s[j:]

    m = re.search(r'\s*<nav class="toc rv".*?</nav>', body, re.S)
    if not m:
        sys.exit("✗ หาสารบัญไม่เจอ")
    toc, body = m.group(0), body.replace(m.group(0), "", 1)

    pieces = re.split(r'(?=<h2 class="rv" id="s\d\d")', body)
    if pieces[0].strip():
        sys.exit("✗ มีอะไรค้างอยู่ก่อนหัวข้อแรกที่ไม่ใช่สารบัญ")
    secs = {}
    for p in pieces[1:]:
        secs[re.match(r'<h2 class="rv" id="(s\d\d)"', p).group(1)] = p

    m = re.search(r'\s*<div class="wrap">\s*<figure class="figplate hero-map rv".*?</figure>\s*</div>',
                  head, re.S)
    if not m:
        sys.exit("✗ หาแผนที่ Coffee Belt ไม่เจอ")
    return head.replace(m.group(0), "", 1), m.group(0), toc, secs, tail


def build_toc(toc, sids, lang):
    """สารบัญยังแสดงครบสิบหัวข้อทุกภาค หัวข้อที่อยู่คนละภาคชี้ข้ามหน้าไป

    ตัวไล่ตำแหน่งในสคริปต์ท้ายหน้าอ่าน href.slice(1) เป็นคีย์ ลิงก์ข้ามหน้าจึงได้คีย์ที่
    ไม่ตรงกับ id ไหนเลย แล้วเงียบไป ไม่ error — เป็นพฤติกรรมที่ต้องการพอดี
    """
    where = {sid: name(base, lang) for base, ss in PARTS for sid in ss}
    me = {s: True for s in sids}

    def fix(m):
        sid = m.group(1)
        href = f"#{sid}" if sid in me else f"{where[sid]}#{sid}"
        return f'<a href="{href}"'
    return re.sub(r'<a href="#(s\d\d)"', fix, toc)


def head_text(sec):
    """ข้อความในหัวข้อ h2 ตัดเลขลำดับออก ใช้เป็นชื่อภาค"""
    m = re.match(r'<h2 class="rv" id="s\d\d"><span class="sn">\d\d</span>(.*?)</h2>', sec, re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()


def first_para(sec, limit=155):
    """ย่อหน้าแรกของหัวข้อ ตัดที่ขอบวรรค ไม่เขียนใหม่ หลักเดียวกับ fix_meta.py"""
    m = re.search(r"<p[^>]*>(.*?)</p>", sec, re.S)
    t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    if len(t) <= limit:
        return t
    return t[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—·")


def pn(idx, lang, titles):
    w = WORDS[lang]
    out = []
    if idx > 0:
        b = name(PARTS[idx - 1][0], lang)
        out.append(f'<a class="pv" href="{b}"><div class="k">{w["prev"]}</div>'
                   f'<div class="t">{html.escape(titles[idx - 1])}</div></a>')
    if idx < len(PARTS) - 1:
        b = name(PARTS[idx + 1][0], lang)
        out.append(f'<a class="nx" href="{b}"><div class="k">{w["next"]}</div>'
                   f'<div class="t">{html.escape(titles[idx + 1])}</div></a>')
    return '<div class="pn"><div class="pn-in">' + "".join(out) + "</div></div>\n"


def swap_meta(s, base, lang, title, desc):
    n = name(base, lang)
    en, th = name(PARTS[0][0], "en"), name(PARTS[0][0], "th")
    en, th = base, "th-" + base
    url = "https://www.neogens.co/"
    s = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} — Neo Gens</title>", s, 1, re.S)
    for k in ('name="description"', 'property="og:description"'):
        s = re.sub(r'<meta ' + k + r' content="[^"]*"',
                   f'<meta {k} content="{html.escape(desc)}"', s, 1)
    s = re.sub(r'<meta property="og:title" content="[^"]*"',
               f'<meta property="og:title" content="{html.escape(title)}"', s, 1)
    s = re.sub(r'<meta property="og:url" content="[^"]*"',
               f'<meta property="og:url" content="{url}{n}"', s, 1)
    s = re.sub(r'<link rel="canonical" href="[^"]*"',
               f'<link rel="canonical" href="{url}{n}"', s, 1)
    s = re.sub(r'(<link rel="alternate" hreflang="en" href=")[^"]*"', r"\g<1>" + url + en + '"', s, 1)
    s = re.sub(r'(<link rel="alternate" hreflang="th" href=")[^"]*"', r"\g<1>" + url + th + '"', s, 1)
    s = re.sub(r'(<link rel="alternate" hreflang="x-default" href=")[^"]*"',
               r"\g<1>" + url + en + '"', s, 1)
    return s


snapshot()
CSS = pn_css()
made = []

for lang in ("en", "th"):
    src = (SRC / keep_name(lang)).read_text(encoding="utf-8")
    head, hero, toc, secs, tail = cut(src)
    titles = [head_text(secs[ss[0]]) for _, ss in PARTS]

    for idx, (base, sids) in enumerate(PARTS):
        s = head
        if idx == 0:
            s += hero                                    # แผนที่อยู่ภาคเดียว
        s += '<article>\n<div class="wrap">\n<div class="artbody">\n'
        s += build_toc(toc, sids, lang).lstrip() + "\n"
        s += "".join(secs[k] for k in sids)
        s += "</div>\n</div>\n" + tail

        # ป้ายภาค ต่อท้ายป้ายเดิม ไม่ทับของเดิม
        s = re.sub(r'(<div class="kicker"[^>]*>)([^<]*)(</div>)',
                   lambda m: m.group(1) + m.group(2).strip() + " · "
                   + WORDS[lang]["part"].format(idx + 1) + m.group(3), s, 1)

        s = s.replace("</main>", pn(idx, lang, titles) + "</main>", 1)

        # กฎ CSS ของปุ่ม หน้ากลุ่มนี้ไม่ได้ลิงก์ไฟล์ CSS ร่วม ต้องฝังเอง
        s = re.sub(r"\n*" + re.escape(MARK_A) + ".*?" + re.escape(MARK_B) + r"\n*", "\n", s, flags=re.S)
        k = s.rindex("</style>", 0, s.index("</head>"))
        s = s[:k].rstrip("\n") + "\n" + CSS + "\n" + s[k:]

        title = titles[idx] if idx else head_text("<h2 class=\"rv\" id=\"s00\">"
                                                  "<span class=\"sn\">00</span>"
                                                  + re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1)
                                                  + "</h2>")
        desc = first_para(secs[sids[0]]) if idx else re.search(
            r'<meta name="description" content="([^"]*)"',
            (SRC / keep_name(lang)).read_text(encoding="utf-8")).group(1)
        s = swap_meta(s, base, lang, title, html.unescape(desc))

        (ROOT / name(base, lang)).write_text(s, encoding="utf-8")
        made.append((name(base, lang), len(sids), title))

# ---------------- ด่านตรวจ ทั้งข้อ "มีครบ" และข้อ "ไม่เหลือ" (LESSONS ข้อ 10) ----------------
checks = {}
for lang in ("en", "th"):
    full = (SRC / keep_name(lang)).read_text(encoding="utf-8")
    _, _, _, secs, _ = cut(full)
    seen = ""
    for base, sids in PARTS:
        n = name(base, lang)
        s = (ROOT / n).read_text(encoding="utf-8")
        art = s[s.index('<div class="artbody">'):s.index("</article>")]
        got = re.findall(r'<h2 class="rv" id="(s\d\d)"', art)

        checks[f"{n} · มีหัวข้อครบตามที่ตัด"] = got == sids
        checks[f"{n} · ไม่เหลือหัวข้อของภาคอื่น"] = not (set(got) - set(sids))
        checks[f"{n} · สารบัญยังครบสิบรายการ"] = s.count('<li><a href=') >= 10
        checks[f"{n} · มี nav id=nav"] = '<nav id="nav">' in s
        checks[f"{n} · มี prog"] = 'id="prog"' in s
        checks[f"{n} · มี article ครอบ (ตัวไล่ตำแหน่งใช้)"] = "<article>" in s
        checks[f"{n} · มีฟอร์มครบทุกช่องที่สคริปต์อ้าง"] = all(
            f'id="{x}"' in s for x in ("wl", "email", "ok", "err", "website"))
        checks[f"{n} · ป้ายภาคขึ้นครั้งเดียว"] = s.count(
            WORDS[lang]["part"].format(PARTS.index((base, sids)) + 1)) == 1
        checks[f"{n} · กฎปุ่มก่อนหน้า/ถัดไปมีชุดเดียว"] = s.count(MARK_A) == 1
        # ปีกกาในบล็อก <style> ต้องสมดุล กฎที่ปิดไม่ครบจะกลืนทุกกฎที่ตามหลังเงียบ ๆ
        for st in re.findall(r"<style[^>]*>(.*?)</style>", s, re.S):
            checks[f"{n} · ปีกกาในบล็อก style สมดุล"] = st.count("{") == st.count("}")
        checks[f"{n} · ไม่มีตัวครอบแทรกใต้ .artbody"] = "<section" not in art
        checks[f"{n} · มี article ชั้นเดียว"] = s.count("<article>") == 1 == s.count("</article>")
        checks[f"{n} · มี .artbody ชั้นเดียว"] = s.count('<div class="artbody">') == 1
        # นับ div ในเขต <article> ต้องสมดุล ไม่งั้นแท็กปิดจะไปปิด <article> แทน
        blk = s[s.index("<article>"):s.index("</article>")]
        checks[f"{n} · div ในเขตบทความสมดุล"] = (
            len(re.findall(r"<div\b", blk)) == len(re.findall(r"</div>", blk)))
        # เช็กที่ตัว <figure> ไม่ใช่คำว่า hero-map เฉย ๆ เพราะกฎ CSS ชื่อเดียวกันอยู่ทุกหน้า
        checks[f"{n} · แผนที่อยู่ภาคแรกเท่านั้น"] = (
            ('class="figplate hero-map rv"' in s) == (base == PARTS[0][0]))
        checks[f"{n} · canonical ชี้ตัวเอง"] = f'rel="canonical" href="https://www.neogens.co/{n}"' in s

        for sid in sids:                       # เนื้อหาต้องเท่าเดิมทุกตัวอักษร
            checks[f"{n} · {sid} เนื้อหาตรงต้นฉบับ"] = secs[sid] in s
            seen += secs[sid]

    checks[f"{lang} · รวมสามภาคแล้วได้เนื้อหาเท่าฉบับเต็ม"] = seen == "".join(
        secs[f"s{i:02d}"] for i in range(1, 11))

bad = [k for k, ok in checks.items() if not ok]
if bad:
    sys.exit("✗ ด่านตรวจไม่ผ่าน:\n  " + "\n  ".join(bad[:12]))

for n, k, t in made:
    print(f"  {n:<34} {k} หัวข้อ · {t[:46]}")
print(f"ด่านตรวจผ่าน {len(checks)} ข้อ")
print("ยังไม่จบ — ต้องเพิ่มสองหน้าใหม่เข้าเมนู แล้วรัน sync_nav · add_nav_dropdown ·"
      " build_jsonld · add_breadcrumbs และเติม sitemap")
