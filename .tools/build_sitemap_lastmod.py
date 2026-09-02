#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ตั้งค่า <lastmod> ใน sitemap.xml ให้ตรงกับวันที่ไฟล์ถูกแก้จริง · 2026-09-01

**ปัญหาที่แก้** ตรวจเมื่อ 1 กันยายน 2569 พบว่า `sitemap.xml` ประกาศ lastmod
ค้างอยู่ที่ 9 สิงหาคม 23 หน้า ทั้งที่หลายหน้าถูกแก้ไปหลังจากนั้นหลายรอบ

Google อ่าน lastmod เพื่อตัดสินว่าหน้าไหนควรไต่ซ้ำ ค่าที่ค้างจึงเท่ากับ
**เว็บกำลังบอก Google ว่าไม่มีอะไรเปลี่ยนตั้งแต่ 9 สิงหาคม** ซึ่งไม่จริง
กดขอไต่ซ้ำทีละหน้าได้วันละสิบกว่าหน้า แต่ sitemap ที่บอกความจริงครอบคลุมทั้งเว็บ
และเป็นช่องทางที่ Google บอกเองว่าให้ใช้เมื่อมีหน้าจำนวนมาก

**ที่มาของวันที่** ใช้วันแก้ไขไฟล์ในเครื่อง ไม่ใช่วันนี้ทุกหน้า
เพราะการประกาศว่าทุกหน้าเพิ่งแก้วันนี้ทั้งที่ไม่จริง คือการโกหกเครื่องแบบเดียวกัน
แค่คนละทิศ  หน้าไหนไม่ได้แตะ วันที่ก็ต้องไม่ขยับ

**ต้องรันเมื่อไร** หลังแก้เนื้อหาเสร็จ ก่อน publish เสมอ
ควรรันต่อท้าย check.command หรือจำไว้ว่าเป็นขั้นสุดท้ายก่อนกด publish

รันจากรากรีโป:  python3 .tools/build_sitemap_lastmod.py
"""
import io
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SM = ROOT / "sitemap.xml"
BASE = "https://www.neogens.co/"


def run():
    s = SM.read_text(encoding="utf-8")
    orig = s
    locs = re.findall(r"<loc>([^<]*)</loc>", s)
    if not locs:
        sys.exit("✗ sitemap.xml ไม่มี <loc> เลย")

    today = date.today().isoformat()
    changed, missing, future = 0, [], []
    out = s

    for loc in locs:
        if not loc.startswith(BASE):
            missing.append(f"{loc} ไม่ได้อยู่ใต้ {BASE}")
            continue
        name = loc[len(BASE):] or "index.html"
        p = ROOT / name
        if not p.exists():
            missing.append(f"{loc} ชี้ไฟล์ที่ไม่มี")
            continue
        d = datetime.fromtimestamp(p.stat().st_mtime).date().isoformat()
        if d > today:
            future.append(f"{name} วันแก้ไข {d} อยู่ในอนาคต")
            continue

        # แทนที่เฉพาะ <lastmod> ที่อยู่ในบล็อก <url> ของ loc นี้ ไม่ยิงทั้งไฟล์
        i = out.find(f"<loc>{loc}</loc>")
        j = out.find("</url>", i)
        blk = out[i:j]
        new = re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{d}</lastmod>", blk, count=1)
        if "<lastmod>" not in blk:
            missing.append(f"{name} ไม่มี <lastmod> ให้แก้")
            continue
        if new != blk:
            out = out[:i] + new + out[j:]
            changed += 1

    checks = {
        "จำนวน <url> ไม่เปลี่ยน": out.count("<url>") == orig.count("<url>"),
        "จำนวน <loc> ไม่เปลี่ยน": out.count("<loc>") == orig.count("<loc>"),
        "จำนวน <lastmod> ไม่เปลี่ยน": out.count("<lastmod>") == orig.count("<lastmod>"),
        "แท็กเปิดปิดสมดุล": out.count("<url>") == out.count("</url>"),
        "ไม่มีวันที่รูปแบบผิด": not re.search(
            r"<lastmod>(?!\d{4}-\d{2}-\d{2}</lastmod>)", out),
        "ไม่มีวันที่อยู่ในอนาคต": all(
            m <= today for m in re.findall(r"<lastmod>([^<]*)</lastmod>", out)),
    }
    bad = [k for k, ok in checks.items() if not ok] + missing + future
    if bad:
        print("แก้ lastmod · ไม่ผ่าน")
        for b in bad[:10]:
            print("  ✗", b)
        sys.exit(1)

    if out != orig:
        SM.write_text(out, encoding="utf-8")
    counts = {}
    for m in re.findall(r"<lastmod>([^<]*)</lastmod>", out):
        counts[m] = counts.get(m, 0) + 1
    print(f"lastmod · {len(locs)} รายการ · อัปเดต {changed} รายการ")
    for d in sorted(counts):
        print(f"  {d}  {counts[d]} หน้า")
    print(f"✓ ด่านตรวจ {len(checks)} ข้อ ผ่านหมด · วันที่มาจากวันแก้ไขไฟล์จริง ไม่ได้ตั้งเป็นวันนี้ทั้งหมด")


if __name__ == "__main__":
    run()
