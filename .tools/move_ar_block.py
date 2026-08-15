#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ย้ายบล็อกตัวอย่าง AR ดาราศาสตร์ (3 figure ติดกัน) จาก about.html / th-about.html
ไปต่อท้ายย่อหน้า <p class="note rv"> ในบล็อก demo ของ experience.html / th-experience.html

ย้ายอย่างเดียว ห้ามแก้คำ — สคริปต์นี้ตัดข้อความออกมาแล้ววางกลับดิบ ๆ ไม่แตะตัวอักษรใด ๆ
พร้อมคัดลอกกฎ CSS ที่หน้า experience ยังไม่มี (.photo .pcards .pcard .pscreen) ตามมาด้วย

รันจากรากรีโป:  python3 .tools/move_ar_block.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAIRS = [
    ("about.html", "experience.html"),
    ("th-about.html", "th-experience.html"),
]

# กฎ CSS ที่ต้องตามไปด้วย — คัดจาก about.html ช่วง ".photo{" ถึงก่อน ".dbox{"
CSS_START = ".photo{"
CSS_STOP = ".dbox{"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def cut_figures(src: str, name: str):
    """ตัดช่วงตั้งแต่ <figure class="rv"> อันแรก ถึง </figure> อันสุดท้าย"""
    if src.count("<figure") != 3 or src.count("</figure>") != 3:
        sys.exit(f"[abort] {name}: คาดว่ามี figure 3 อัน แต่พบ "
                 f"{src.count('<figure')}/{src.count('</figure>')}")

    m_start = re.search(r'[ \t]*<figure class="rv">', src)
    if not m_start:
        sys.exit(f"[abort] {name}: หา <figure class=\"rv\"> ไม่เจอ")

    idx_end = src.rindex("</figure>") + len("</figure>")

    # กินบรรทัดว่างที่ตามหลังบล็อกไปด้วย เพื่อไม่ให้เหลือช่องว่างซ้อน
    tail = idx_end
    while tail < len(src) and src[tail] in "\r\n":
        tail += 1

    block = src[m_start.start():idx_end]
    remainder = src[:m_start.start()] + src[tail:]
    return block, remainder


def dedent_block(block: str) -> str:
    """คืนบล็อกที่ตัด indent ร่วมออก เพื่อเอาไปจัด indent ใหม่ในไฟล์ปลายทาง"""
    lines = block.split("\n")
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    base = min(indents)
    return "\n".join(l[base:] if l.strip() else "" for l in lines)


def extract_css(src: str) -> str:
    i = src.index("\n" + CSS_START) + 1
    j = src.index("\n" + CSS_STOP) + 1
    return src[i:j]


def insert_after_note(dst: str, block: str, name: str) -> str:
    """แทรกบล็อกหลัง </p> ที่ปิด <p class="note rv">"""
    m = re.search(r'([ \t]*)<p class="note rv">', dst)
    if not m:
        sys.exit(f"[abort] {name}: หา <p class=\"note rv\"> ไม่เจอ")

    indent = m.group(1)
    close = dst.index("</p>", m.end()) + len("</p>")

    body = "\n".join((indent + l) if l.strip() else "" for l in block.split("\n"))
    return dst[:close] + "\n\n" + body + dst[close:]


def insert_css(dst: str, css: str, name: str) -> str:
    if ".pcards{" in dst:
        print(f"    [skip] {name}: มี CSS .pcards อยู่แล้ว")
        return dst
    k = dst.index("\n" + CSS_STOP) + 1
    return dst[:k] + css + dst[k:]


def main():
    css = None
    for src_name, dst_name in PAIRS:
        src_p, dst_p = ROOT / src_name, ROOT / dst_name
        src, dst = read(src_p), read(dst_p)

        block, src_new = cut_figures(src, src_name)
        if css is None:
            css = extract_css(src)

        dst_new = insert_after_note(dst, dedent_block(block), dst_name)
        dst_new = insert_css(dst_new, css, dst_name)

        src_p.write_text(src_new, encoding="utf-8")
        dst_p.write_text(dst_new, encoding="utf-8")
        print(f"  ย้าย {len(block):,} ตัวอักษร  {src_name} -> {dst_name}")

    print("เสร็จ · ตรวจต่อด้วย  python3 .tools/verify_ar_move.py")


if __name__ == "__main__":
    main()
