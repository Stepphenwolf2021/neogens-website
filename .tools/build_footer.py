#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ทำให้ footer มีต้นฉบับเดียวต่อภาษา แล้วจัดเป็นห้าคอลัมน์ให้ตรงกับแถบเมนูบน

สั่งโดย Noppadol เมื่อ 2026-08-23  "MKM for Coffee น่าจะอยู่แยกกับ Company"

เดิม footer มีสี่คอลัมน์ คอลัมน์สุดท้ายชื่อ Part 3 & company เอาภาคกาแฟไปปนกับบริษัท
และไม่มีต้นฉบับ ต้องไล่แก้ทีละหน้า 47 ครั้ง ซึ่งเป็นโรคเดียวกับที่ sync_nav.py แก้ให้แถบเมนูไปแล้ว

ต่อจากนี้แก้ footer ที่ .tools/shell/footer.en.html หรือ footer.th.html แล้วรันสคริปต์นี้

สิ่งที่ตรวจแล้วก่อนตัดสินใจ  บล็อก .f-cols ของทุกหน้าในภาษาเดียวกันเหมือนกันทุกไบต์
ลิงก์สลับภาษาใน footer ชี้ไป index ของอีกภาษาเสมอ ไม่ได้ชี้ตามหน้า จึงไม่ต้องแทนค่าต่อหน้า

รันจากรากรีโป:  python3 .tools/build_footer.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / ".tools" / "shell"

# ── ห้าคอลัมน์ เรียงตามกลุ่มบนแถบเมนู ────────────────────────────────
# ชื่อกลุ่มยกมาจากเมนูสไลด์ใน .tools/shell/nav.*.html ไม่ได้ตั้งใหม่
# คอลัมน์ 3 เป็นส่วนที่ล้นจากกลุ่ม 2 ซึ่ง footer แยกไว้อยู่แล้วตั้งแต่เดิม
COLS = {
    "en": [
        ("Part 1 · The idea", None, [
            ("the-problem.html", "The problem"),
            ("what-mkm-is.html", "What is MKM ?"),
            ("why-it-works.html", "Why it works"),
            ("ontology-and-knowledge-graph.html", "Ontology &amp; knowledge graph")]),
        ("Part 2 · Museums &amp; libraries", None, [
            ("exec-summary-museums.html", "Executive summary"),
            ("mkm-for-museums-and-libraries.html", "Where things stand"),
            ("what-you-are-holding.html", "What you are holding"),
            ("visitors-and-readers.html", "The new experience"),
            ("leadership.html", "What leadership looks like"),
            ("long-read-museums-and-libraries.html", "Long read: MKM for museums &amp; libraries")]),
        ("Working together", None, [
            ("services.html", "What we do together"),
            ("engagement.html", "Engagement"),
            ("ai-sovereignty.html", "Your data · AI sovereignty"),
            ("what-we-wont-do.html", "What we won't do")]),
        # ── ปิดชั่วคราว 2026-09-01 · ถอดภาค 3 MKM for Coffee ออกจากเว็บ ──
        # เอากลับ: ปลด comment สี่บล็อกนี้ทั้งไฟล์ แล้วเปลี่ยน repeat(4 กลับเป็น repeat(5
        # และคืนไฟล์หน้ากาแฟจาก .tools/coffee-archive/ ดู .tools/pause_coffee.py
        # ("Part 3 · Public goods", None, [
        #     ("mkm-for-coffee.html", "MKM for Coffee"),
        #     ("mkm-for-coffee-why-now.html", "Why this is possible now"),
        #     ("mkm-for-coffee-commons.html", "How a commons stays a commons"),
        #     ("coffee-farmer.html", "For coffee farmers"),
        #     ("coffee-demo.html", "Demo dashboard")]),
        # เดิมหัวคอลัมน์นี้คือ "Part 2 · Working together" ทำให้มีคอลัมน์ชื่อ Part 2
        # สองอันติดกัน อ่านแล้วเหมือนไล่เลขใหม่หลังถอดภาค 3 แล้วทำค้างไว้ · 2026-09-01
        ("Company", "Neo Gens Co., Ltd.", [
            ("about.html", "Who we are"),
            ("seo-as-knowledge-management.html", "How we built this site"),
            ("mailto:hello@neogens.co", "hello@neogens.co"),
            # ลิงก์ที่คนเห็น คู่กับ sameAs ใน JSON-LD ที่เครื่องอ่าน · 2026-09-01
            ("https://www.linkedin.com/company/neogens/", "LinkedIn"),
            ("th-index.html", "ฉบับภาษาไทย")]),
    ],
    "th": [
        ("ภาค 1 · แนวคิด", None, [
            ("th-the-problem.html", "ปัญหา"),
            ("th-what-mkm-is.html", "MKM คืออะไร"),
            ("th-why-it-works.html", "ทำไมมันถึงได้ผล"),
            ("th-ontology-and-knowledge-graph.html", "ontology กับ knowledge graph")]),
        ("ภาค 2 · พิพิธภัณฑ์และห้องสมุด", None, [
            ("th-exec-summary-museums.html", "บทสรุปสำหรับผู้บริหาร"),
            ("th-mkm-for-museums-and-libraries.html", "สถานะวันนี้"),
            ("th-what-you-are-holding.html", "สิ่งที่คุณถืออยู่"),
            ("th-visitors-and-readers.html", "ประสบการณ์ใหม่ของการเรียนรู้"),
            ("th-leadership.html", "ความเป็นผู้นำหน้าตาเป็นอย่างไร"),
            ("long-read-museums-and-libraries.html",
             "บทความยาว: MKM สำหรับพิพิธภัณฑ์และห้องสมุด (อังกฤษ)")]),
        ("การทำงานร่วมกัน", None, [
            ("th-services.html", "เราทำอะไรร่วมกัน"),
            ("th-engagement.html", "รูปแบบการทำงาน"),
            ("th-ai-sovereignty.html", "ข้อมูลของคุณ · AI Sovereignty"),
            ("th-what-we-wont-do.html", "สิ่งที่เราไม่ทำ")]),
        # ── ปิดชั่วคราว 2026-09-01 · ถอดภาค 3 MKM สำหรับกาแฟ ออกจากเว็บ ──
        # ("ภาค 3 · โครงการเพื่อสาธารณะ", None, [
        #     ("th-mkm-for-coffee.html", "MKM สำหรับกาแฟ"),
        #     ("th-mkm-for-coffee-why-now.html", "ทำไมเพิ่งทำได้ตอนนี้"),
        #     ("th-mkm-for-coffee-commons.html", "จะทำอย่างไรให้สมบัติร่วมยังเป็นของร่วม"),
        #     ("th-coffee-farmer.html", "สำหรับคนปลูกกาแฟ"),
        #     ("th-coffee-demo.html", "เดโมแดชบอร์ด")]),
        ("บริษัท", "Neo Gens Co., Ltd.", [
            ("th-about.html", "เราคือใคร"),
            ("th-seo-as-knowledge-management.html", "เว็บนี้สร้างมาอย่างไร"),
            ("mailto:hello@neogens.co", "hello@neogens.co"),
            ("https://www.linkedin.com/company/neogens/", "LinkedIn"),
            ("index.html", "English edition")]),
    ],
}

# ── CSS · ต่อท้ายสุดของ <style> จึงชนะกฎเดิมด้วยลำดับ ไม่ต้องไปแก้กฎเก่า ──
# ลำดับใน media query สำคัญ ตัวกว้างน้อยกว่าต้องอยู่ทีหลัง ไม่งั้นจอแคบจะได้กฎของจอกว้าง
#
# เว็บนี้มี CSS สองรุ่นอยู่พร้อมกัน ตรวจแล้วเมื่อ 08-23
#   หน้าที่ลิงก์ assets/site.*.css   กฎ .f-cols อยู่ในไฟล์ภายนอก และ site.th.css ยัง .f-in{display:block}
#   หน้าที่ฝัง CSS ทั้งก้อน (กาแฟ · privacy · seo)  กฎอยู่ใน <style> ของหน้าเอง เป็นรุ่นเก่ากว่า
# กฎข้างล่างจึงเขียนให้พอเพียงในตัว มี display:grid ด้วย จะได้ไม่ต้องพึ่งว่ารุ่นไหนให้อะไรมา
# และวางท้ายสุดของ <style> ซึ่งอยู่หลัง <link> จึงชนะทั้งสองรุ่นด้วยลำดับ
# minmax(0,1fr) กันคอลัมน์ดันกันบวมเวลาป้ายยาว ซึ่งเป็นสำนวนที่ CSS รุ่นใหม่ของเว็บนี้ใช้อยู่แล้ว
CSS = """
/* >>> footer ห้าคอลัมน์ · build_footer.py >>> */
.f-cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:26px 18px}
@media(max-width:1000px){.f-cols{grid-template-columns:repeat(3,minmax(0,1fr));gap:26px 22px}}
@media(max-width:900px){.f-cols{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.f-cols{grid-template-columns:minmax(0,1fr)}}
/* <<< footer ห้าคอลัมน์ <<< */
"""
OPEN, CLOSE = "/* >>> footer ห้าคอลัมน์", "/* <<< footer ห้าคอลัมน์ · build_footer.py <<< */"


def strip_old_css(s):
    """ถอดบล็อกที่สคริปต์นี้เคยใส่ไว้ออกก่อน จะได้แก้ CSS แล้วรันซ้ำได้จริง"""
    i = s.find(OPEN)
    if i < 0:
        return s
    j = s.find("<<< footer ห้าคอลัมน์ <<< */", i)
    if j < 0:
        sys.exit("✗ บล็อก CSS ของ build_footer.py ปิดไม่ครบ")
    j += len("<<< footer ห้าคอลัมน์ <<< */")
    return s[:i].rstrip("\n") + "\n" + s[j:].lstrip("\n")


def render(lang):
    out = ['<div class="f-cols">']
    for head, para, links in COLS[lang]:
        out.append(f'<div class="f-col"><div class="h">{head}</div>')
        if para:
            out.append(f"<p>{para}</p>")
        for href, label in links:
            out.append(f'<a href="{href}">{label}</a>')
        out.append("</div>")
    out.append("</div>")
    return "".join(out)


def fcols_span(s, name):
    """หาช่วงของ <div class="f-cols"> ด้วยการไล่นับ div  ห้ามใช้ regex  ดูข้อ 11"""
    i = s.find('<div class="f-cols">')
    if i < 0:
        return None
    depth, j = 0, i
    while j < len(s):
        if s.startswith("<div", j):
            depth += 1
        elif s.startswith("</div>", j):
            depth -= 1
            if depth == 0:
                return i, j + len("</div>")
        j += 1
    sys.exit(f"✗ {name} หา </div> ปิดของ .f-cols ไม่เจอ")


def pages():
    for p in sorted(ROOT.glob("*.html")):
        s = p.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in s or p.name == "404.html":
            continue
        if '<div class="f-cols">' in s:
            yield p, s


if "--extract" in sys.argv:                      # เก็บของเดิมไว้เทียบ เผื่ออยากย้อน
    SHELL.mkdir(parents=True, exist_ok=True)
    for lang, src in (("en", "about.html"), ("th", "th-about.html")):
        s = (ROOT / src).read_text(encoding="utf-8")
        a, b = fcols_span(s, src)
        (SHELL / f"footer.{lang}.html").write_text(s[a:b], encoding="utf-8")
        print(f"  ดึงต้นฉบับ footer.{lang}.html จาก {src} · {b - a} ไบต์")
    sys.exit(0)

for lang in ("en", "th"):
    SHELL.mkdir(parents=True, exist_ok=True)
    (SHELL / f"footer.{lang}.html").write_text(render(lang), encoding="utf-8")

changed, bad = 0, []
for p, s in pages():
    lang = "th" if p.name.startswith("th-") else "en"
    new = (SHELL / f"footer.{lang}.html").read_text(encoding="utf-8")

    # ใส่ CSS ก่อน แล้วค่อยหาช่วง footer ใหม่
    # เพราะ <style> อยู่ก่อน footer ในไฟล์ ถ้าใส่ทีหลังตำแหน่งที่จำไว้จะเลื่อนทั้งหมด
    out = strip_old_css(s)
    if out.count("</style>") != 1:
        bad.append(f"{p.name} มี </style> ไม่ใช่หนึ่งก้อน")
        continue
    out = out.replace("</style>", CSS + "</style>", 1)

    a, b = fcols_span(out, p.name)
    head, tail = out[:a], out[b:]
    out = head + new + tail

    # ด่านตรวจ นอกเขต footer ต้องไม่ขยับ เทียบกับตัวที่ใส่ CSS แล้วเท่านั้น
    if not out.startswith(head) or not out.endswith(tail):
        bad.append(f"{p.name} มีอย่างอื่นนอก footer เปลี่ยนไปด้วย")
        continue
    if out != s:
        p.write_text(out, encoding="utf-8")
        changed += 1

# ── ด่านรวม · มีทั้งข้อ "มีครบ" และข้อ "ไม่เหลือ"  ข้อ 10 ────────────────
checks, n = {}, 0
for p, s in pages():
    lang = "th" if p.name.startswith("th-") else "en"
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", s, re.S))
    a, b = fcols_span(s, p.name)
    foot = s[a:b]
    n += 1
    parts = foot.split('<div class="f-col">')
    checks[f"{p.name} · footer สี่คอลัมน์"] = len(parts) == 5
    checks[f"{p.name} · ไม่เหลือลิงก์กาแฟใน footer"] = "coffee" not in foot
    checks[f"{p.name} · long-read อยู่คอลัมน์พิพิธภัณฑ์"] = \
        len(parts) == 5 and "long-read-museums-and-libraries.html" in parts[2]
    checks[f"{p.name} · ไม่เหลือหัวคอลัมน์เก่า"] = \
        "Part 3 &amp; company" not in foot and "ภาค 3 และบริษัท" not in foot
    checks[f"{p.name} · กฎ CSS สี่คอลัมน์ติด"] = "repeat(4,minmax(0,1fr))" in css
    checks[f"{p.name} · กฎนี้มีอยู่ชุดเดียว ไม่ซ้อนกัน"] = css.count(OPEN) == 1
    checks[f"{p.name} · กฎเพียงพอในตัว มี display:grid"] = \
        "repeat(4,minmax(0,1fr))" in css and "display:grid;grid-template-columns:repeat(4" in css
    checks[f"{p.name} · ปีกกา CSS สมดุล"] = css.count("{") == css.count("}")
    checks[f"{p.name} · แท็ก div สมดุล"] = s.count("<div") == s.count("</div>")
    for href, _ in sum([c[2] for c in COLS[lang]], []):
        # ลิงก์ออกนอกเว็บ ตรวจด้วยการหาไฟล์ไม่ได้ จึงข้าม
        # ลิงก์พวกนี้ต้องเป็น URL ที่เปิดดูได้จริงและเราคุมปลายทางได้ เช่นเพจ LinkedIn ของเรา
        if href.startswith(("mailto:", "https://", "http://")):
            continue
        if not (ROOT / href).exists():
            bad.append(f"{p.name} footer ชี้ไฟล์ที่ไม่มี {href}")

fails = [k for k, ok in checks.items() if not ok]
print(f"เขียน footer ใหม่ {changed} หน้า จาก {n} หน้า · ด่านตรวจ {len(checks)} ข้อ · ไม่ผ่าน {len(fails)}")
for f in fails[:10]:
    print("  ✗", f)
for b_ in sorted(set(bad))[:8]:
    print("  !!", b_)
if fails or bad:
    sys.exit(1)
print("✓ ทุกหน้าใช้ footer ชุดเดียวกัน · สี่คอลัมน์ตรงกับเมนูบน · ไม่มีลิงก์ตาย")
