#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เอาต้นฉบับ exec summary เข้ามาเก็บใน .tools/exec-summary-source/
แล้วแทรกสามย่อหน้าต่อท้ายหัวข้อ 2 ของทั้งสองฉบับ

รันซ้ำได้ ถ้าบล็อกอยู่แล้วจะไม่แทรกซ้ำ
ด่านท้ายไฟล์มีทั้งข้อ *มีครบ* และข้อ *ไม่เหลือ* ตามข้อ 10 ของ LESSONS.md
"""
import sys, pathlib

SRC_DIR = pathlib.Path(__file__).parent / "exec-summary-source"
SRC_DIR.mkdir(exist_ok=True)

# จุดยึด เลือกจากสิ่งที่มีจริงในต้นฉบับ ไม่ใช่คลาสที่นึกออก (ข้อ 9)
ANCHOR_EN = "It is to give the model a substrate that can be checked.\n"
ANCHOR_TH = "สิ่งที่ต้องทำคือหาพื้นที่ยืนที่ตรวจสอบได้ให้มัน\n"

BLOCK_EN = """
### The three routes directors reach for

**The standard.** Adopting C2PA and Content Credentials is worth doing, and an institution that has done it stands on firmer ground than one that has not. But a standard secures a file. What the public questions is a sentence. Ask which piece of evidence supports the third clause of a catalogue description and file-level provenance has nothing to say: the container is signed, the claim inside it is not. Standards were built to survive transmission, not to carry an argument.

**The tool.** Every vendor now offers AI-assisted description, reconciliation or enrichment, and the better ones are genuinely capable. But a tool inherits the quality of the material the institution hands it. Where two accession records disagree, the model cannot know which one your curators treat as authoritative, because nobody has written that down anywhere a machine can read. It does not fail loudly at that point. It answers from whatever it found, in your institution's voice.

**The institution's own hand.** An AI charter, a review step, a rule that no machine-written record is published without a curator's sign-off — this is the strongest of the three, and the only one most institutions can begin this quarter. It is still incomplete, for a reason that has nothing to do with rigour: an institution cannot be its own witness. The people reviewing the output are the people whose earlier records supply its context, and a closed loop can be perfectly disciplined and still confirm its own mistakes. Authenticity has always needed a second pair of hands: VIAF, ORCID, a peer's citation, a source community's own account of itself.

All three are necessary. What none of them supplies is a place to put the answer to *how do we know this?* where a person can read it and a machine can reach it. That is what section 5 proposes to build.
"""

BLOCK_TH = """
### สามทางที่ผู้บริหารมักเลือก

**ทางที่หนึ่ง รับมาตรฐานมาใช้** C2PA และ Content Credentials บอกได้ว่าไฟล์นี้มาจากไหน ผ่านมือใครมาบ้าง องค์กรที่รับมาใช้แล้วยืนอยู่บนที่ที่มั่นคงกว่าองค์กรที่ยังไม่ได้ทำ แต่สิ่งที่มาตรฐานรับรองคือไฟล์ ส่วนสิ่งที่คนตั้งคำถามคือประโยค ลองถามว่าข้อความท่อนที่สามในคำบรรยายชิ้นนี้มาจากหลักฐานชิ้นไหน ที่มาระดับไฟล์ตอบไม่ได้ กล่องมีลายเซ็น ของข้างในไม่มี

**ทางที่สอง ซื้อเครื่องมือ** ผู้ขายทุกรายมีฟังก์ชัน AI ช่วยเขียนคำอธิบาย ช่วยเทียบรายการ ช่วยเติมข้อมูล และของดีก็มีอยู่จริง แต่เครื่องมือทำงานได้ดีเท่าที่ของซึ่งเราส่งให้มันเท่านั้น ทะเบียนสองใบเขียนไม่ตรงกัน เครื่องไม่มีทางรู้ว่าภัณฑารักษ์ของเราถือใบไหนเป็นหลัก เพราะไม่เคยมีใครเขียนเรื่องนี้ลงไปในที่ที่เครื่องอ่านได้ แล้วตอนนั้นมันจะไม่ส่งเสียง มันจะตอบจากของเท่าที่หาเจอ ด้วยน้ำเสียงขององค์กรเรา

**ทางที่สาม จัดการเองภายใน** ตั้งนโยบายเรื่อง AI เพิ่มขั้นตอนตรวจ วางกฎว่าระเบียนที่เครื่องเขียนต้องมีภัณฑารักษ์เซ็นกำกับก่อนออกไป ทางนี้แข็งแรงที่สุดในสามทาง และเป็นทางเดียวที่เริ่มได้ในไตรมาสนี้ แต่ก็ยังไม่พอ ด้วยเหตุผลที่ไม่เกี่ยวกับความเข้มงวดเลย องค์กรเป็นพยานให้ตัวเองไม่ได้ คนที่ตรวจงาน คือคนที่ระเบียนเก่าของเขาเองเป็นฐานให้งานชิ้นนั้น วงจรที่ปิดอยู่ในตัวเอง มีวินัยแค่ไหนก็ยังยืนยันความผิดของตัวเองได้อยู่ดี ความแท้ต้องการมือที่สองเสมอมา ไม่ว่าจะเป็น VIAF, ORCID, การอ้างอิงของเพื่อนร่วมวงการ หรือคำบอกเล่าของชุมชนเจ้าของเรื่องเอง

สามทางนี้ต้องทำทั้งสามทาง สิ่งที่ยังขาดเหมือนกันหมดคือที่วางคำตอบของคำถามว่า *เรารู้เรื่องนี้ได้อย่างไร* ในที่ที่คนเปิดอ่านได้ และเครื่องเดินไปถึงได้ นั่นคือสิ่งที่ข้อ 5 เสนอให้สร้าง
"""

JOBS = [
    ("neogens-exec-summary-museums-EN.md", ANCHOR_EN, BLOCK_EN),
    ("neogens-exec-summary-museums-TH.md", ANCHOR_TH, BLOCK_TH),
]


def run(uploads: pathlib.Path):
    problems = []
    for name, anchor, block in JOBS:
        out = SRC_DIR / name
        raw = (out if out.exists() else uploads / name).read_text(encoding="utf-8")

        marker = block.strip().splitlines()[0]
        if marker in raw:
            s = raw                      # แทรกไปแล้ว ไม่แทรกซ้ำ
        else:
            if raw.count(anchor) != 1:
                problems.append(f"{name}: จุดยึดเจอ {raw.count(anchor)} ครั้ง ต้องเจอ 1")
                continue
            s = raw.replace(anchor, anchor + block, 1)

        out.write_text(s, encoding="utf-8")

        # ด่านตรวจ — มีครบ
        checks = {
            "แทรกบล็อกแล้ว": marker in s,
            "มีสามย่อหน้าครบ": s.count("**", s.index(marker)) >= 6,
            "บล็อกอยู่ก่อนหัวข้อ 3": s.index(marker) < s.index("\n## 3."),
            "บล็อกอยู่หลังหัวข้อ 2": s.index("\n## 2.") < s.index(marker),
            "แทรกครั้งเดียว": s.count(marker) == 1,
        }
        # ด่านตรวจ — ไม่เหลือ
        checks["ไม่มีเว้นวรรคซ้ำในบล็อก"] = "  " not in block
        if name.endswith("TH.md"):
            checks["ไม่มี ครับ ในเนื้อความ"] = "ครับ" not in block
            checks["ไม่ใช้คำว่า สถาบัน แทน organisation"] = "สถาบัน" not in block
            checks["ขีดยาวไม่เกินหนึ่งครั้งต่อย่อหน้า"] = all(
                p.count("—") <= 1 for p in block.split("\n\n"))
        bad = [k for k, ok in checks.items() if not ok]
        if bad:
            problems.append(f"{name}: {' · '.join(bad)}")
        else:
            print(f"ผ่าน {name} · {len(s)} ตัวอักษร")

    if problems:
        sys.exit("ไม่ผ่าน\n" + "\n".join(problems))
    print("ผ่านทั้งหมด")


if __name__ == "__main__":
    run(pathlib.Path(sys.argv[1]))
