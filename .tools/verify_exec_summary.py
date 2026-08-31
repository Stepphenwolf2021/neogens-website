#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เทียบข้อความที่มองเห็นในหน้า exec summary กับต้นฉบับ .md ตัวต่อตัว

เนื้อหาสองฉบับนี้เป็นงานเขียนที่ตัดสินใจไว้แล้ว หน้าเว็บมีหน้าที่แสดงมันให้ครบ
ไม่ใช่เกลาใหม่ ด่านนี้จึงเทียบทุกตัวอักษร ไม่ใช่เทียบจำนวนย่อหน้า

ตัดช่องว่างทิ้งทั้งสองฝั่งก่อนเทียบ เพราะ HTML แทรกช่องว่างตรงขอบแท็ก <strong>
กับ <em> ซึ่งไม่ใช่ความต่างของเนื้อหา ส่วนเลขลำดับหัวข้อ 01–07 เป็นของที่หน้าเว็บ
ใส่เอง ไม่ได้อยู่ในต้นฉบับ จึงถอดออกก่อนเทียบเช่นกัน

รันจากรากรีโป:  python3 .tools/verify_exec_summary.py
"""
import difflib
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".tools" / "exec-summary-source"
PAIRS = [("exec-summary-museums.html", "neogens-exec-summary-museums-EN.md"),
         ("th-exec-summary-museums.html", "neogens-exec-summary-museums-TH.md")]
# คำที่ต้องมี เป็นหมุดว่าเนื้อหาหลักไม่หายไประหว่างแปลง
# บล็อกสามทางที่ผู้บริหารมักเลือก ถูกตัดออกเมื่อ 08-31 รอบดึก VIAF จึงเหลือที่เดียว
# เทียบกับข้อความที่ตัดช่องว่างทิ้งแล้ว หมุดจึงต้องไม่มีช่องว่างด้วย
PROBES = ["VIAF", "ORCID", "C2PA", "CIDOCCRM"]

bad = []
for page, md in PAIRS:
    s = (ROOT / page).read_text(encoding="utf-8")
    body = s[s.index('<div class="artbody">'):s.index("</article>")]
    body = re.sub(r'<span class="sn">\d+</span>', "", body)
    # แผงตัวเลขเป็นของที่หน้าเว็บวาดเอง ไม่ได้อยู่ในต้นฉบับ ถอดออกก่อนเทียบ
    n_fig = len(re.findall(r'<figure class="esf', body))
    body = re.sub(r'<figure class="esf.*?</figure>', "", body, flags=re.S)
    got = re.sub(r"\s+", "", html.unescape(re.sub(r"<[^>]+>", " ", body)))

    if n_fig != 2:
        bad.append(page)
        print(f"✗ {page} มีแผงตัวเลข {n_fig} แผง ต้องมี 2")
        continue

    lines = (SRC / md).read_text(encoding="utf-8").rstrip().split("\n")
    b = "\n".join(lines[lines.index("---") + 1:])
    b = re.sub(r"(?m)^---$", "", b)
    b = re.sub(r"(?m)^#{2,3}\s*", "", b)
    b = re.sub(r"(?m)^-\s+", "", b)
    b = re.sub(r"(?m)^\d+\.\s+", "", b)
    b = re.sub(r"\[\[FIGURE:\w+\]\]", "", b)      # ตัวยึดรูป ไม่ใช่ข้อความที่คนอ่าน
    want = re.sub(r"\s+", "", b.replace("**", "").replace("*", ""))

    if got != want:
        bad.append(page)
        print(f"✗ {page} ต้นฉบับ {len(want)} ในหน้า {len(got)}")
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, want, got).get_opcodes():
            if op != "equal":
                print(f"   {op} {want[i1:i2]!r} → {got[j1:j2]!r}")
        continue

    missing = [p for p in PROBES if p not in got]
    if missing:
        bad.append(page)
        print(f"✗ {page} ขาดคำที่ต้องมี: {' · '.join(missing)}")
        continue
    print(f"✓ {page} · {len(got)} ตัวอักษร ตรงกับต้นฉบับตัวต่อตัว")

sys.exit(1 if bad else 0)
