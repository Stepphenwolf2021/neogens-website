#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ปิดภาค 3 · MKM for Coffee ชั่วคราว · 2026-09-01

สั่งโดย Noppadol  "ถอดเมนู MKM for Coffee และ content ทั้งหมดข้างในออกไปก่อน
แต่ยังเก็บทุกอย่างไว้ เพื่อใส่กลับมาใหม่ในอนาคต"

สิ่งที่สคริปต์นี้ทำ
  1  ย้ายไฟล์หน้ากาแฟ 12 ไฟล์ออกจากรากเว็บ ไปไว้ .tools/coffee-archive/
     โฟลเดอร์นั้นไม่ถูกเสิร์ฟ เพราะ GitHub Pages ตัดโฟลเดอร์ที่ขึ้นต้นด้วยจุดทิ้ง
  2  วางหน้าแจ้ง "ปิดชั่วคราว" ไว้ที่ URL เดิมทั้ง 12 ตัว ลิงก์เก่าที่คนแปะไว้จึงไม่ตาย
     ตามกติกาข้อ 9 ของโปรเจกต์ · ทุกหน้าเป็น noindex เสิร์ชเอนจินจะถอดออกเอง
  3  ถอดกลุ่มกาแฟออกจากต้นฉบับเมนูทั้งสองภาษา เก็บชิ้นที่ถอดไว้ในคลัง
  4  ถอด 11 รายการของกาแฟออกจาก sitemap.xml เก็บ XML ที่ถอดไว้ในคลัง
  5  แก้ลิงก์กาแฟใน 404.html

ส่วนที่ไม่ได้อยู่ในสคริปต์นี้ อยู่ในตัวเครื่องมือเอง ทำเป็น comment ไว้ทั้งหมด
  .tools/build_footer.py   คอลัมน์ ภาค 3 · และ repeat(5 → repeat(4
  .tools/build_gates.py    ประตูที่สาม · lead สามทาง → สองทาง · repeat(3 → repeat(2
  .tools/build_jsonld.py   PART_NAME[3] และ Service #service-coffee

เอากลับ:  python3 .tools/pause_coffee.py resume
          แล้วปลด comment ในสามไฟล์ข้างบน
          แล้วรัน sync_nav → build_jsonld → add_breadcrumbs → build_footer → build_gates

รันจากรากรีโป:  python3 .tools/pause_coffee.py [pause|resume]
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARC = ROOT / ".tools" / "coffee-archive"

PAGES = [
    ("mkm-for-coffee.html", "th-mkm-for-coffee.html"),
    ("mkm-for-coffee-why-now.html", "th-mkm-for-coffee-why-now.html"),
    ("mkm-for-coffee-commons.html", "th-mkm-for-coffee-commons.html"),
    ("coffee-farmer.html", "th-coffee-farmer.html"),
    ("coffee-demo.html", "th-coffee-demo.html"),
    ("coffee.html", "th-coffee.html"),          # ทางเบี่ยงเก่า
]
ALL = [f for pair in PAGES for f in pair]

# ── หน้าแจ้งปิดชั่วคราว ────────────────────────────────────────────
# สไตล์เดียวกับทางเบี่ยงที่โปรเจกต์ใช้อยู่แล้ว ไม่มีเมนู ไม่มี footer
# มี http-equiv refresh ไม่ได้ เพราะหน้านี้ต้องให้คนอ่าน ไม่ใช่เด้งต่อ
# จึงใส่ data-standalone ไว้ให้เครื่องมืออื่นข้าม และ noindex ให้บอตถอดออก
NOTICE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, follow">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>
html{{background:#08090A;color:#A2A8AF;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
body{{display:flex;min-height:100vh;align-items:center;justify-content:center;
  margin:0;padding:28px;text-align:center;line-height:{lh}}}
.box{{max-width:44ch}}
h1{{color:#ECEFF3;font-size:21px;line-height:{lhh};margin:0 0 14px;font-weight:600}}
p{{margin:0 0 18px;font-size:15.5px}}
a{{color:#B8F04A}}
</style>
</head>
<body data-standalone="notice">
<div class="box">
<h1>{h1}</h1>
<p>{body}</p>
<p><a href="/{home}">{cta}</a></p>
</div>
</body>
</html>
"""

EN_TEXT = dict(
    lang="en", lh="1.75", lhh="1.4", home="index.html",
    title="Temporarily closed — Neo Gens",
    desc="MKM for Coffee is closed while we rework it. It will return.",
    h1="This section is closed for now",
    body="MKM for Coffee is off the site while we rework it. Nothing has been lost, "
         "and it will come back. If you were reading it and want the material, write to "
         "<a href=\"mailto:hello@neogens.co\">hello@neogens.co</a>.",
    cta="Back to Neo Gens")
TH_TEXT = dict(
    lang="th", lh="1.85", lhh="1.55", home="th-index.html",
    title="ปิดชั่วคราว — Neo Gens",
    desc="MKM สำหรับกาแฟ ปิดชั่วคราวระหว่างปรับปรุง แล้วจะกลับมา",
    h1="ส่วนนี้ปิดไว้ชั่วคราว",
    body="MKM สำหรับกาแฟ ถูกถอดออกจากเว็บระหว่างปรับปรุง เนื้อหาทั้งหมดยังอยู่ครบ "
         "และจะกลับมา ถ้าคุณกำลังอ่านอยู่แล้วอยากได้เนื้อหา เขียนมาที่ "
         "<a href=\"mailto:hello@neogens.co\">hello@neogens.co</a>",
    cta="กลับหน้าแรก Neo Gens")


def notice(th):
    return NOTICE.format(**(TH_TEXT if th else EN_TEXT))


# ── เมนู · ถอดกลุ่มกาแฟออกจากต้นฉบับทั้งสองภาษา ────────────────────
def nav_cut(s):
    """คืน (ข้อความที่เหลือ, ชิ้นที่ถอดออก)  ไล่นับ span ไม่ใช้ regex ตามข้อ 11"""
    cuts = []
    # 1 · กลุ่มบนแถบเมนูบน  <span class="hs"><a href="mkm-for-coffee.html">…</span></span>
    i = s.find('<span class="hs"><a href="mkm-for-coffee.html">')
    if i < 0:
        i = s.find('<span class="hs"><a href="th-mkm-for-coffee.html">')
    if i >= 0:
        depth, j = 0, i
        while j < len(s):
            if s.startswith("<span", j):
                depth += 1
            elif s.startswith("</span>", j):
                depth -= 1
                if depth == 0:
                    j += len("</span>")
                    break
            j += 1
        cuts.append(s[i:j])
        s = s[:i] + s[j:]
    # 2 · หัวข้อภาค 3 ในเมนูสไลด์ ถึงหัวข้อถัดไป
    for head in ('<div class="h">Part 3 · Public goods</div>',
                 '<div class="h">ภาค 3 · โครงการเพื่อสาธารณะ</div>'):
        a = s.find(head)
        if a < 0:
            continue
        b = s.find('<div class="h">', a + len(head))
        if b < 0:
            sys.exit("✗ หาหัวข้อถัดไปในเมนูสไลด์ไม่เจอ")
        cuts.append(s[a:b])
        s = s[:a] + s[b:]
    return s, cuts


def do_pause():
    ARC.mkdir(parents=True, exist_ok=True)
    # คัดลอกเข้าคลังก่อน แล้วเขียนทับด้วยหน้าแจ้งในขั้นถัดไป
    # ไม่ได้ลบไฟล์ เพราะกล่องที่รันสคริปต์ลบไฟล์บนเครื่องจริงไม่ได้
    # ผลลัพธ์เท่ากัน คือ URL เดิมไม่มีเนื้อหาเดิมอยู่แล้ว
    moved = []
    for f in ALL:
        src, dst = ROOT / f, ARC / f
        if src.exists() and not dst.exists():
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            moved.append(f)
    print("  เก็บต้นฉบับเข้าคลัง %d ไฟล์" % len(moved))

    for en, th in PAGES:
        (ROOT / en).write_text(notice(False), encoding="utf-8")
        (ROOT / th).write_text(notice(True), encoding="utf-8")
    print("  วางหน้าแจ้งปิดชั่วคราว %d ไฟล์" % (len(PAGES) * 2))

    for nav in ("nav.en.html", "nav.th.html"):
        p = ROOT / ".tools" / "shell" / nav
        s = p.read_text(encoding="utf-8")
        if "coffee" not in s:
            print("  %s ถอดไปแล้ว ข้าม" % nav)
            continue
        s2, cuts = nav_cut(s)
        if "coffee" in s2:
            sys.exit("✗ %s ยังเหลือลิงก์กาแฟหลังถอด" % nav)
        (ARC / (nav + ".cut")).write_text("\n\n".join(cuts), encoding="utf-8")
        p.write_text(s2, encoding="utf-8")
        print("  ถอดกลุ่มกาแฟออกจาก %s · เก็บชิ้นที่ถอดไว้ %d ชิ้น" % (nav, len(cuts)))

    # sitemap
    p = ROOT / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    blocks = re.findall(r"  <url>\n(?:.*?\n)*?  </url>\n", s)
    gone = [b for b in blocks if "coffee" in b]
    for b in gone:
        s = s.replace(b, "")
    if gone:
        (ARC / "sitemap-coffee.xml").write_text("".join(gone), encoding="utf-8")
        p.write_text(s, encoding="utf-8")
    print("  ถอด sitemap %d รายการ · เหลือ %d" % (len(gone), s.count("<loc>")))

    # 404
    p = ROOT / "404.html"
    s = p.read_text(encoding="utf-8")
    if "mkm-for-coffee.html" in s:
        s = re.sub(r'<a href="/mkm-for-coffee\.html">[^<]*</a>',
                   '<a href="/exec-summary-museums.html">Executive summary</a>', s)
        p.write_text(s, encoding="utf-8")
        print("  แก้ลิงก์กาแฟใน 404.html")


def do_resume():
    if not ARC.exists():
        sys.exit("✗ ไม่มีคลัง .tools/coffee-archive/")
    back = []
    for f in ALL:
        src = ARC / f
        if src.exists():
            (ROOT / f).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            back.append(f)
    print("  คืนไฟล์จากคลัง %d ไฟล์" % len(back))
    for nav in ("nav.en.html", "nav.th.html"):
        c = ARC / (nav + ".cut")
        if c.exists():
            print("  ชิ้นเมนูของ %s อยู่ที่ %s เอากลับเข้าที่เดิมด้วยมือ" % (nav, c))
    print("  รายการ sitemap ที่ถอดไว้อยู่ที่ %s" % (ARC / "sitemap-coffee.xml"))
    print("  อย่าลืมปลด comment ใน build_footer.py · build_gates.py · build_jsonld.py")


mode = sys.argv[1] if len(sys.argv) > 1 else "pause"
if mode == "pause":
    print("ปิดภาค 3 · MKM for Coffee")
    do_pause()
elif mode == "resume":
    print("เปิดภาค 3 กลับ")
    do_resume()
else:
    sys.exit("ใช้: python3 .tools/pause_coffee.py [pause|resume]")

# ── ด่านตรวจ · มีทั้งข้อ มีครบ และข้อ ไม่เหลือ ────────────────────
if mode == "pause":
    checks = {
        "ไฟล์ต้นฉบับอยู่ในคลังครบ": all((ARC / f).exists() for f in ALL),
        "หน้าแจ้งอยู่ที่ URL เดิมครบ": all((ROOT / f).exists() for f in ALL),
        "หน้าแจ้งเป็น noindex": all("noindex" in (ROOT / f).read_text(encoding="utf-8")
                                    for f in ALL),
        "เมนูไม่เหลือลิงก์กาแฟ": all("coffee" not in (ROOT / ".tools" / "shell" / n)
                                     .read_text(encoding="utf-8")
                                     for n in ("nav.en.html", "nav.th.html")),
        "sitemap ไม่เหลือกาแฟ": "coffee" not in (ROOT / "sitemap.xml")
                                 .read_text(encoding="utf-8"),
        "404 ไม่เหลือลิงก์กาแฟ": "coffee" not in (ROOT / "404.html")
                                  .read_text(encoding="utf-8"),
        "เนื้อหาเดิมยังอ่านได้": (ARC / "mkm-for-coffee.html")
                                  .stat().st_size > 50000,
    }
    bad = [k for k, ok in checks.items() if not ok]
    print("ด่านตรวจ %d ข้อ · ไม่ผ่าน %d" % (len(checks), len(bad)))
    for b in bad:
        print("  ✗", b)
    if bad:
        sys.exit(1)
    print("✓ ภาค 3 ถอดออกจากเว็บแล้ว เนื้อหาอยู่ครบใน .tools/coffee-archive/")
    print("  ต่อด้วย  sync_nav → build_jsonld → add_breadcrumbs → build_footer → build_gates")
