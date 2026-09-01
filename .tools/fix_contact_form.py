#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เปลี่ยนฟอร์มของหน้าที่สร้างจากแม่แบบกาแฟ ให้เป็นฟอร์มขอนัดหารือมาตรฐาน · 2026-09-01

**ปัญหาที่แก้** หน้าที่สร้างจากแม่แบบ coffee-farmer พกฟอร์มของเกษตรกรติดมาทั้งชุด

    ป้ายช่อง org   Farm, mill, co-op or roastery   ฟาร์ม โรงสี สหกรณ์ หรือโรงคั่ว
    ช่อง country    ประเทศ
    ช่อง interest   ข้อมูลที่คุณอยากรู้จาก Coffee Knowledge Vault
    topic          'MKM Coffee'

ผู้อำนวยการพิพิธภัณฑ์ที่กรอกฟอร์มในหน้า SEO จึงถูกถามว่าทำฟาร์มหรือโรงคั่วอะไร
แล้วถูกบันทึกเป็นผู้สนใจสายกาแฟ ทั้งที่ภาค 3 ถูกถอดออกจากเว็บไปแล้วเมื่อ 2026-09-01

**วิธีแก้** ยกทั้ง `<section class="join">` ออก แล้ววาง `<section id="contact" class="cta">`
ของหน้ามาตรฐานภาษาเดียวกันลงไปแทน พร้อมสคริปต์ส่งฟอร์มของหน้านั้น
ฟอร์มมาตรฐาน **ไม่ส่ง topic** ซึ่ง Worker รับได้อยู่แล้ว ยืนยันจากการทดสอบจริงเมื่อ 2026-09-01
จึงไม่ต้องแก้ฝั่ง Worker และไม่ต้อง deploy อะไรเพิ่ม

หน้าที่แตะ  seo-as-knowledge-management · privacy · และคู่ไทยของทั้งสอง

รันซ้ำได้ ถ้าแก้ไปแล้วจะข้ามให้เอง
build_evidence.py กับ build_privacy.py เรียกสคริปต์นี้ต่อท้ายให้เองแล้ว ไม่ต้องจำ

รันจากรากรีโป:  python3 .tools/fix_contact_form.py
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TARGETS = {
    "en": (["seo-as-knowledge-management.html", "privacy.html"], "what-mkm-is.html"),
    "th": (["th-seo-as-knowledge-management.html", "th-privacy.html"], "th-what-mkm-is.html"),
}
# หน้าที่ถอดฟอร์มออกไปแล้ว แต่สคริปต์ส่งฟอร์มของแม่แบบยังค้างอยู่
# ไม่มีฟอร์มให้กด จึงไม่ทำงาน แต่ยังประกาศ topic:'MKM Coffee' ทิ้งไว้ในหน้า
# เป็นคำประกาศที่ไม่ตรงกับสิ่งที่หน้านั้นทำจริง จึงเก็บออก
ORPHAN = ["exec-summary-museums.html", "th-exec-summary-museums.html"]
COFFEE_WORDS = ("Farm, mill, co-op or roastery", "ฟาร์ม โรงสี สหกรณ์ หรือโรงคั่ว",
                "Coffee Knowledge Vault", "learn from the vault", "MKM Coffee",
                'id="country"', 'id="interest"')


def section_span(s, opener):
    """ช่วงของ <section …> ถึง </section> ที่คู่กัน ไล่นับ ไม่ใช้ regex ตามบทเรียนข้อ 11"""
    i = s.find(opener)
    if i < 0:
        return None
    depth, j = 0, i
    while j < len(s):
        if s.startswith("<section", j):
            depth += 1
        elif s.startswith("</section>", j):
            depth -= 1
            if depth == 0:
                return i, j + len("</section>")
        j += 1
    sys.exit(f"✗ หา </section> ปิดของ {opener[:30]} ไม่เจอ")


def form_script(s):
    """สคริปต์ก้อนที่ส่งฟอร์ม หาโดยดูว่ามี NG_ENDPOINT อยู่ข้างใน"""
    for m in re.finditer(r"<script>", s):
        k = s.find("</script>", m.start())
        blk = s[m.start():k + len("</script>")]
        if "NG_ENDPOINT" in blk:
            return m.start(), k + len("</script>"), blk
    return None


def fix(path, donor_path):
    s = io.open(path, encoding="utf-8").read()
    orig = s
    if '<section class="join"' not in s:
        return "ข้ามแล้ว ไม่มีฟอร์มกาแฟ", 0

    d = io.open(donor_path, encoding="utf-8").read()
    ds = section_span(d, '<section id="contact" class="cta">')
    if not ds:
        sys.exit(f"✗ {donor_path.name} ไม่มี section ติดต่อมาตรฐานให้ยกมา")
    donor_section = d[ds[0]:ds[1]]
    dj = form_script(d)
    if not dj:
        sys.exit(f"✗ {donor_path.name} ไม่มีสคริปต์ส่งฟอร์ม")
    donor_script = dj[2]

    # 1 · แทนที่ section ฟอร์มกาแฟ ด้วย section ติดต่อมาตรฐาน
    a, b = section_span(s, '<section class="join" id="join">')
    s = s[:a] + donor_section + s[b:]

    # 2 · แถบ GET IN TOUCH เก่าที่ยังค้างอยู่เฉพาะหน้ากลุ่มนี้ ซ้ำกับ section ที่เพิ่งวาง
    sp = section_span(s, '<section class="cta">')
    if sp:
        s = s[:sp[0]] + s[sp[1]:]

    # 3 · สคริปต์ส่งฟอร์ม ใช้ของหน้ามาตรฐาน ซึ่งไม่ส่ง topic และไม่มี country/interest
    sj = form_script(s)
    if sj:
        s = s[:sj[0]] + donor_script + s[sj[1]:]

    checks = {
        "ไม่เหลือฟอร์มกาแฟ": '<section class="join"' not in s,
        "ไม่เหลือคำของสายกาแฟ": not any(w in s for w in COFFEE_WORDS),
        "มี section ติดต่อมาตรฐาน": '<section id="contact" class="cta">' in s,
        "มีฟอร์มเดียว": s.count('<form id="wl"') == 1,
        "มีสคริปต์ส่งฟอร์มก้อนเดียว": s.count("NG_ENDPOINT") >= 1
                                       and len(re.findall(r"NG_ENDPOINT\s*=", s)) == 1,
        "แท็ก section สมดุล": s.count("<section") == s.count("</section>"),
        "แท็ก div สมดุล": s.count("<div") == s.count("</div>"),
        "โครงหน้ายังครบ": all(x in s for x in ["</footer>", "<h1", "id=\"main\""]),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {path.name} ไม่ผ่าน: " + " · ".join(bad))
    io.open(path, "w", encoding="utf-8").write(s)
    return "แก้แล้ว", len(s) - len(orig)


def drop_orphan_script(path):
    s = io.open(path, encoding="utf-8").read()
    if '<form id="wl"' in s or "NG_ENDPOINT" not in s:
        return "ข้ามแล้ว ไม่มีสคริปต์กำพร้า", 0
    orig = s
    sj = form_script(s)
    s = s[:sj[0]] + s[sj[1]:]
    checks = {"ไม่เหลือสคริปต์ฟอร์ม": "NG_ENDPOINT" not in s,
              "ไม่เหลือ topic กาแฟ": "MKM Coffee" not in s,
              "ไม่มีฟอร์มอยู่แล้ว": '<form id="wl"' not in s,
              "โครงหน้ายังครบ": all(x in s for x in ["</footer>", "<h1"])}
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {path.name} ไม่ผ่าน: " + " · ".join(bad))
    io.open(path, "w", encoding="utf-8").write(s)
    return "ถอดสคริปต์กำพร้าออก", len(s) - len(orig)


def run():
    n = 0
    for f in ORPHAN:
        p = ROOT / f
        if not p.exists():
            continue
        msg, delta = drop_orphan_script(p)
        print(f"  {f:38} {msg}" + (f" · {delta:+d} ตัวอักษร" if delta else ""))
        n += 1 if delta else 0
    for lang, (files, donor) in TARGETS.items():
        dp = ROOT / donor
        for f in files:
            p = ROOT / f
            if not p.exists():
                continue
            msg, delta = fix(p, dp)
            print(f"  {f:38} {msg}" + (f" · {delta:+d} ตัวอักษร" if delta else ""))
            n += 1 if msg == "แก้แล้ว" else 0
    print(f"✓ ฟอร์มขอนัดหารือมาตรฐาน · แก้ {n} หน้า · ไม่ต้องแตะฝั่ง Worker")


if __name__ == "__main__":
    run()
