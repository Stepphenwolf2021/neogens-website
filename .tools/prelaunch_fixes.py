#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ชุดแก้ก่อน launch · จากการตรวจรอบสุดท้าย 1 กันยายน 2569

ทุกข้อในไฟล์นี้มาจากการตรวจที่พิสูจน์ด้วยการวัดหน้าจริงหรืออ่านไฟล์จริง
ไม่ใช่ข้อสงสัย รันซ้ำได้ ถ้าแก้ไปแล้วจะข้ามให้เอง

รันจากรากรีโป:  python3 .tools/prelaunch_fixes.py
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
log, bad = [], []


def rd(f):
    return (ROOT / f).read_text(encoding="utf-8")


def wr(f, s):
    (ROOT / f).write_text(s, encoding="utf-8")


def sub(f, old, new, must=1, delete=False):
    """แทนที่ข้อความตรงตัว พร้อมพิสูจน์ว่าเกิดขึ้นจริงตามจำนวนที่คาด

    delete=True  คือการลบทิ้ง new เป็นสตริงว่าง จึงใช้ new เป็นหลักฐานว่าแก้แล้วไม่ได้
    กรณีนี้ถือว่าหาไม่เจอ แปลว่าเคยลบไปแล้ว และปล่อยให้ด่าน ไม่เหลือ ข้างล่างเป็นตัวยืนยันแทน
    """
    s = rd(f)
    n = s.count(old)
    if n == 0 and delete:
        log.append(f"  {f:42} ข้ามแล้ว")
        return
    if n == 0:
        # ระวัง  new ที่เป็นสตริงว่างจะอยู่ใน s เสมอ ถ้าเช็กด้วย `new in s` เฉย ๆ
        # สคริปต์จะรายงานว่าข้ามแล้วทั้งที่ยังไม่ได้แก้ · เจอบั๊กนี้ตอนรันจริง 2026-09-01
        if new and new in s:
            log.append(f"  {f:42} ข้ามแล้ว")
            return
        bad.append(f"{f} หาข้อความที่จะแก้ไม่เจอ: {old[:60]}")
        return
    if must and n != must:
        bad.append(f"{f} เจอ {n} ที่ แต่คาด {must}: {old[:50]}")
        return
    wr(f, s.replace(old, new))
    log.append(f"  {f:42} แก้ {n} จุด")


# ── 1 · หน้าแรกเลื่อนออกด้านข้างบนมือถือ ──────────────────────────────
# วัดที่ 375px  เนื้อหากว้าง 412px  เกินขอบ 37px  ทั้งสองภาษา
# ต้นเหตุ .hero เป็น position:static  .hero-bg ที่เป็น absolute จึงอ้างอิง body
# แล้วหลุดจาก overflow:hidden ที่ .hero ตั้งไว้แล้ว  เติม relative บรรทัดเดียวจบ
# ทดสอบด้วยการฉีดกฎเข้าหน้าจริงก่อน  scrollWidth กลับมาเท่าความกว้างจอพอดี
def fix_hero():
    n = 0
    for p in sorted(list(ROOT.glob("*.html")) + list((ROOT / "assets").glob("*.css"))):
        s = p.read_text(encoding="utf-8")
        if ".hero{" not in s or ".hero{position:relative" in s:
            continue
        out = s.replace(".hero{", ".hero{position:relative;")
        if out.count(".hero{position:relative;") != s.count(".hero{"):
            bad.append(f"{p.name} แทนที่ .hero{{ ไม่ครบ")
            continue
        p.write_text(out, encoding="utf-8")
        n += 1
    log.append(f"  .hero{{position:relative}}                     {n} ไฟล์")


# ── 2 · หน้าอ้างอิงชี้ไปเนื้อหาที่ถูกตัดออกจาก about.html เมื่อ 2026-09-01 ──
# Noppadol เลือก: ตัดประโยคที่อ้างออก เก็บหน้าไว้
EN_REF = ('The institutional half of this record — TCDC, Ubonratchathani, TK Park, '
          'the ThaiHealth Learning Center — is on the '
          '<a href="about.html" style="color:var(--go)">who is behind this</a> page. '
          'What follows is the technical half.')

# ── 3 · คำอธิบายหน้าที่ถูกตัดกลางประโยค ────────────────────────────────
# เนื้อความในหน้าสมบูรณ์อยู่แล้ว ตัวที่ขาดคือ meta ที่ถูกตัดตามจำนวนตัวอักษร
# แก้ให้จบประโยค โดยใช้คำต่อจากเนื้อความในหน้านั้นเอง ไม่ได้แต่งคำใหม่
DESCS = {
    "mkm-for-museums-and-libraries.html": (
        "Four educated adults spend an afternoon in a well-funded new gallery, read "
        "every panel, try every interactive — and leave with nothing they can repeat to a",
        "Four educated adults spend an afternoon in a well-funded new gallery, try "
        "every interactive — and leave with nothing they can repeat to a child in the car."),
    "what-you-are-holding.html": (
        "Museums, libraries and archives built this discipline. Cataloguing, authority "
        "control, provenance, the practice of separating an attribution from a",
        "Museums, libraries and archives built this discipline. Cataloguing, authority "
        "control, provenance, the practice of separating an attribution from a certainty."),
    "visitors-and-readers.html": (
        "Once concepts, objects, people and evidence are modelled as a graph, a route "
        "through the collection becomes a question rather than a construction project —",
        "Once concepts, objects, people and evidence are modelled as a graph, a route "
        "through the collection becomes a question rather than a construction project."),
}


def run():
    fix_hero()

    for f, one in (("reference-implementation.html", EN_REF),):
        s = rd(f)
        if one in s:
            wr(f, s.replace(one, "What follows is the technical half."))
            log.append(f"  {f:42} ตัดประโยคที่อ้าง about ออก")
        elif "TCDC" in s and "about.html" in s:
            bad.append(f"{f} ยังอ้าง TCDC คู่กับ about.html แต่รูปประโยคไม่ตรงที่คาด")
        else:
            log.append(f"  {f:42} ข้ามแล้ว")

    th = "th-reference-implementation.html"
    s = rd(th)
    m = re.search(r'[^<>]*TCDC[^<>]*<a href="th-about\.html"[^>]*>[^<]*</a>[^<>]*', s)
    if m:
        wr(th, s.replace(m.group(0), ""))
        log.append(f"  {th:42} ตัดประโยคที่อ้าง th-about ออก")
    elif "TCDC" in s:
        bad.append(f"{th} ยังมี TCDC อยู่ แต่รูปประโยคไม่ตรงที่คาด")
    else:
        log.append(f"  {th:42} ข้ามแล้ว")

    for f, (old, new) in DESCS.items():
        if len(new) > 160:
            bad.append(f"{f} คำอธิบายใหม่ยาว {len(new)} เกิน 160")
            continue
        s = rd(f)
        # ต้องเช็ก new ก่อนเสมอ  เพราะ old เป็นคำนำหน้าของ new ในสองในสามหน้า
        # ถ้าเช็ก old ก่อน การรันซ้ำจะไปแทนที่ซ้อนในข้อความที่แก้แล้ว
        # เกิดขึ้นจริงตอนรันรอบสอง ได้ "…from a certainty. certainty." · 2026-09-01
        if new in s:
            log.append(f"  {f:42} ข้ามแล้ว")
            continue
        n = s.count(old)
        if n < 2:
            bad.append(f"{f} คาดว่าเจอทั้ง description และ og:description แต่เจอ {n}")
            continue
        wr(f, s.replace(old, new))
        log.append(f"  {f:42} คำอธิบาย {len(old)}→{len(new)} ตัวอักษร · {n} จุด")

    # ── 4 · ประโยคที่อ้างถึงเนื้อหาที่ไม่มีในหน้า เศษจากตารางที่ถูกถอดออก ──
    # ประโยคอยู่กลางย่อหน้า ไม่ได้เป็น <p> ของตัวเอง จึงตัดเฉพาะประโยค
    sub("engagement.html",
        " Durations are the typical shape and are scoped per institution.", "", delete=True)
    sub("th-engagement.html",
        "\n        ส่วนระยะเวลาที่ระบุเป็นรูปแบบทั่วไป กำหนดขอบเขตกันเป็นรายองค์กร", "", delete=True)

    # ── 5 · ประโยคที่อ่านไม่รู้เรื่องในบทความยาว · เติมคำเดียว ไม่เปลี่ยนความหมาย ──
    sub("long-read-museums-and-libraries.html",
        "can be recorded reasoning, not merely recommending.",
        "can be recorded while reasoning, not merely recommending.")

    # ── 6 · เลข 11% ถูกใช้กับสองเรื่อง · Noppadol เลือกถอดออกจากการ์ดนโยบาย ──
    sub("exec-summary-museums.html",
        '<p class="esf-t">have a formal AI charter or written policy</p>'
        '<p class="esf-d">Don\'t know · 11%</p>',
        '<p class="esf-t">have a formal AI charter or written policy</p>')
    sub("th-exec-summary-museums.html",
        '<p class="esf-t">มีธรรมนูญหรือนโยบายเรื่อง AI ที่เขียนไว้</p>'
        '<p class="esf-d">ตอบว่าไม่รู้ · 11%</p>',
        '<p class="esf-t">มีธรรมนูญหรือนโยบายเรื่อง AI ที่เขียนไว้</p>')

    # ── ตัวอักษรใต้การ์ด 11px เล็กเกินไปสำหรับไทยที่มีสระสองชั้น · เฉพาะหน้าไทย ──
    sub("th-exec-summary-museums.html",
        ".esf-d{font-size:11px;line-height:1.8;", ".esf-d{font-size:12.5px;line-height:1.85;")

    # ── 7 · การสะกดที่ Noppadol ตัดสินเอง เมื่อ 2026-09-01 ────────────────
    sub("th-index.html", "Halluciations", "Hallucinations", must=0)
    sub("th-index.html", "อินเทอร์เน็ต", "อินเตอร์เน็ต", must=0)
    sub("th-exec-summary-museums.html", "อัพเดท", "อัปเดต", must=0)

    n = 0
    for p in sorted(ROOT.glob("th-*.html")):
        s = p.read_text(encoding="utf-8")
        if "สร้างมูลค่า" in s:
            p.write_text(s.replace("สร้างมูลค่า", "สร้างคุณค่า"), encoding="utf-8")
            n += 1
    log.append(f"  สร้างมูลค่า → สร้างคุณค่า                       {n} หน้า")

    # ── 8 · นามบัตรที่มีเบอร์มือถือส่วนตัว ถูกเสิร์ฟอยู่จริง ────────────────
    gi = ROOT / ".gitignore"
    g = gi.read_text(encoding="utf-8")
    if "card/" not in g:
        gi.write_text(g.rstrip("\n") + "\n\n"
                      "# นามบัตร · มีเบอร์มือถือส่วนตัวและไฟล์ต้นฉบับ .ai\n"
                      "# รีโปนี้คือเว็บที่เสิร์ฟจริง ทุกอย่างที่ commit ถูกเปิดดูได้จากภายนอก\n"
                      "card/\n", encoding="utf-8")
        log.append("  .gitignore                                 เพิ่ม card/")
    else:
        log.append("  .gitignore                                 ข้ามแล้ว")

    # ── ด่านตรวจ แบบ ไม่เหลือ ──────────────────────────────────────────
    checks = {
        "ไม่เหลือ TCDC ที่ชี้ไป about": all(
            not ("TCDC" in rd(f) and re.search(r'TCDC[^<>]*<a href="(th-)?about', rd(f)))
            for f in ("reference-implementation.html", "th-reference-implementation.html")),
        "ไม่เหลือ Halluciations": "Halluciations" not in rd("th-index.html"),
        "ไม่เหลือ อินเทอร์เน็ต": "อินเทอร์เน็ต" not in rd("th-index.html"),
        "ไม่เหลือ อัพเดท": "อัพเดท" not in rd("th-exec-summary-museums.html"),
        "ไม่เหลือ สร้างมูลค่า": not any("สร้างมูลค่า" in p.read_text(encoding="utf-8")
                                        for p in ROOT.glob("th-*.html")),
        "ไม่เหลือ Durations": "Durations are the typical" not in rd("engagement.html"),
        "ไม่เหลือระยะเวลาที่ไม่มีในหน้า": "ระยะเวลาที่ระบุ" not in rd("th-engagement.html"),
        # ต้องนับด้วย <p\b  ไม่ใช่ "<p" เฉย ๆ เพราะ <path ใน SVG จะถูกนับด้วย
        # หน้านี้มี <path 11 อัน ด่านจึงฟ้องผิดในการรันรอบแรก · บทเรียนข้อ 11
        "ย่อหน้าที่ตัดยังปิดแท็กครบ": all(
            len(re.findall(r"<p\b", rd(f))) == rd(f).count("</p>")
            for f in ("engagement.html", "th-engagement.html")),
        "ไม่เหลือประโยคพัง": "recorded reasoning," not in rd("long-read-museums-and-libraries.html"),
        "11% เหลือที่เดียวในการ์ด อังกฤษ": rd("exec-summary-museums.html").count(
            '<p class="esf-d">Don\'t know · 11%</p>') == 1,
        "11% เหลือที่เดียวในการ์ด ไทย": rd("th-exec-summary-museums.html").count(
            '<p class="esf-d">ตอบว่าไม่รู้ · 11%</p>') == 1,
        "card/ ถูก ignore": "card/" in (ROOT / ".gitignore").read_text(encoding="utf-8"),
    }
    for f in DESCS:
        d = re.search(r'name="description" content="([^"]*)"', rd(f)).group(1)
        checks[f"{f} คำอธิบายจบประโยค"] = d.endswith(".") and len(d) <= 160

    print("แก้ก่อน launch · 1 กันยายน 2569")
    for line in log:
        print(line)
    fails = [k for k, ok in checks.items() if not ok]
    for b in bad[:10]:
        print("  ✗", b)
    for f in fails:
        print("  ✗ ด่านไม่ผ่าน:", f)
    if bad or fails:
        sys.exit(1)
    print(f"✓ ด่านตรวจ {len(checks)} ข้อ ผ่านหมด")


if __name__ == "__main__":
    run()
