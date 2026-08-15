#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
แก้บล็อก story ในหน้า about ให้กลับเป็นคอลัมน์เดียว คุมความกว้างการอ่าน

ที่มา — รอบก่อนหน้าใส่คลาสชื่อ split เข้าไป โดยไม่รู้ว่าไฟล์นี้มี .split อยู่แล้ว
คือ .split{display:grid;grid-template-columns:1fr 54px 1fr} ของบล็อกอื่น
ผลคือ .story.split กลายเป็นกริดสามคอลัมน์ ตัวเนื้อหาไปตกในช่อง 54px
บนเว็บจริงจึงเห็นข้อความเรียงลงมาคำละบรรทัด

สคริปต์นี้
1. ถอด <div class="cols"> และ <div class="col"> ที่ห่อไว้ออก คืนย่อหน้าเดิมทั้งหมด
2. เอาคลาส split ออกจาก .story
3. เปลี่ยน CSS เป็นคอลัมน์เดียว คุมความกว้างบรรทัด และเน้นย่อหน้าแรก

ห้ามแตะตัวอักษรของ Noppadol — ถอดเฉพาะแท็กที่สคริปต์รอบก่อนใส่เข้าไปเอง

รันจากรากรีโป:  python3 .tools/fix_story_layout.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_CSS = [
    ".story.split .col>p:first-child{margin-top:0!important}",
    ".story.split .cols{display:grid;grid-template-columns:1fr 1fr;"
    "gap:clamp(24px,3.4vw,44px);align-items:start}",
    "@media(max-width:900px){.story.split .cols{grid-template-columns:1fr;gap:0}}",
]

# ความกว้างบรรทัดต่างกันสองภาษา ไทยตัวอักษรแคบกว่า จึงตั้ง ch น้อยกว่า
NEW_CSS = {
    "about.html":
        ".story p{max-width:66ch}\n"
        ".story .k+p{font-size:18px;color:var(--fg);line-height:1.55}\n",
    "th-about.html":
        ".story p{max-width:620px}\n"
        ".story .k+p{font-size:18px;color:var(--fg);line-height:1.9}\n",
}


def check_class_free(src: str, cls: str, name: str) -> None:
    """กันความผิดเดิมซ้ำ — คลาสใหม่ต้องไม่มีกฎอยู่ก่อนในไฟล์"""
    if re.search(r"(^|[,\s}])\." + re.escape(cls) + r"[\s,{:.]", src, re.M):
        sys.exit(f"[abort] {name}: มีคลาส .{cls} อยู่แล้วในไฟล์ ห้ามใช้ชื่อซ้ำ")


def unwrap(src: str, name: str) -> str:
    """ถอด <div class="cols"> และ <div class="col"> พร้อม </div> ที่คู่กัน

    wrapper ทั้งสามตัวถูกวางไว้ที่ระดับย่อหน้าพอดี จึงใช้ระดับย่อหน้าเป็นตัวชี้
    ตัวไหนเป็นของ wrapper ตัวไหนเป็นของบล็อก story เดิม
    """
    lines = src.split("\n")
    opens = [i for i, l in enumerate(lines)
             if l.strip() in ('<div class="cols">', '<div class="col">')]
    if not opens:
        print(f"    [skip] {name}: ไม่พบ wrapper")
        return src

    indent = len(lines[opens[0]]) - len(lines[opens[0]].lstrip())
    closes = [i for i, l in enumerate(lines)
              if l.strip() == "</div>"
              and len(l) - len(l.lstrip()) == indent
              and opens[0] < i]
    closes = closes[:len(opens)]

    if len(closes) != len(opens):
        sys.exit(f"[abort] {name}: เปิด {len(opens)} ปิด {len(closes)} ไม่เท่ากัน")

    drop = set(opens) | set(closes)
    out = [l for i, l in enumerate(lines) if i not in drop]
    print(f"    ถอด wrapper {len(opens)} เปิด {len(closes)} ปิด")
    return "\n".join(out)


def main():
    for name in ("about.html", "th-about.html"):
        p = ROOT / name
        s = p.read_text(encoding="utf-8")
        print(f"  {name}")

        s = unwrap(s, name)
        s = s.replace('class="story split rv"', 'class="story rv"')

        for rule in OLD_CSS:
            if rule in s:
                s = s.replace(rule + "\n", "")
        s = s.replace("\n.dlab{", "\n" + NEW_CSS[name] + ".dlab{")

        p.write_text(s, encoding="utf-8")
        print("    ตั้งความกว้างบรรทัดและเน้นย่อหน้าแรกแล้ว")


if __name__ == "__main__":
    main()
