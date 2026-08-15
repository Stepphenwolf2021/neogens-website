#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
จัดหน้า about ใหม่ · about.html + th-about.html

1. ลบกฎ CSS ที่ตายแล้วหลังย้ายบล็อก AR ออกไป (.photo .pcards .pcard .pscreen .dsplit
   และคลาสลูกทั้งชุดของ .dsvg ที่ไม่มีใครใช้ในหน้านี้อีก)
2. เพิ่มภาพประกอบ SVG ใหม่ คนนั่งคิดกับกราฟความรู้ วาดขึ้นเองทั้งหมด
   ใช้ตัวแปรสีของธีม จึงสลับมืดสว่างได้เอง
3. แตกบล็อก story สองบล็อกเป็นสองคอลัมน์บนจอกว้าง เพื่อลดความสูงของหน้า

ห้ามแตะตัวอักษรของ Noppadol — สคริปต์นี้ห่อ <p> เดิมด้วย <div class="col"> เท่านั้น
ไม่แก้เนื้อในแท็กแม้แต่ตัวเดียว

รันจากรากรีโป:  python3 .tools/relayout_about.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CSS ที่ลบ

DEAD = [
    ".photo{", ".photo img{", ".pcards{",
    "@media(max-width:760px){.pcards{grid-template-columns:1fr}}",
    ".pcard{", ".pcard .who{", ".pcard .got{", ".pcard .got b{", ".pscreen{",
    ".dsplit{", "@media(max-width:820px){.dsplit{grid-template-columns:1fr}}",
    ".dsvg .bx{", ".dsvg .bx-go{", ".dsvg .bx-am{", ".dsvg .bx-as{", ".dsvg .bx-gh{",
    ".dsvg .t{", ".dsvg .t-b{", ".dsvg .t-s{",
    ".dsvg .m{", ".dsvg .m-go{", ".dsvg .m-am{", ".dsvg .m-as{",
    ".dsvg .ln{", ".dsvg .ln-go{", ".dsvg .ln-am{", ".dsvg .ln-gh{",
    ".dsvg .t,.dsvg .t-b{",
]

# ---------------------------------------------------------------- CSS ที่เพิ่ม

CSS_NEW = """.tk-l{stroke:var(--fg);stroke-width:1.8;fill:none;stroke-linejoin:round;stroke-linecap:round}
.tk-f{fill:rgba(var(--w-rgb),.05)}
.tk-e{stroke:var(--go);stroke-width:1.1;fill:none;opacity:.5}
.tk-n{stroke:var(--go);stroke-width:1.5;fill:var(--bg)}
.story.split .col>p:first-child{margin-top:0!important}
.story.split .cols{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,3.4vw,44px);align-items:start}
@media(max-width:900px){.story.split .cols{grid-template-columns:1fr;gap:0}}
"""

# ---------------------------------------------------------------- ภาพประกอบ

EDGES = [
    "M320 96 L540 128", "M324 112 L556 214",
    "M540 128 L620 150", "M556 214 L620 150", "M556 214 L664 268",
    "M620 150 L700 196", "M700 196 L664 268", "M620 150 L752 132",
    "M752 132 L812 204", "M700 196 L812 204", "M664 268 L760 300",
    "M812 204 L760 300", "M664 268 L596 318", "M596 318 L612 406",
    "M760 300 L676 352", "M676 352 L716 420", "M676 352 L612 406",
    "M760 300 L838 300", "M838 300 L804 382", "M804 382 L716 420",
    "M812 204 L868 150", "M752 132 L868 150", "M596 318 L676 352",
]

GRAPH_NODES = [
    (540, 128, 5), (556, 214, 5), (620, 150, 6), (700, 196, 5), (664, 268, 6),
    (752, 132, 5), (812, 204, 6), (760, 300, 5), (676, 352, 6), (596, 318, 5),
    (838, 300, 5), (716, 420, 5), (612, 406, 5), (804, 382, 5), (868, 150, 4),
]

BODY_NODES = [
    (316, 100, 4.5), (324, 196, 4), (238, 348, 4.5), (288, 162, 4),
    (206, 378, 4), (448, 340, 4), (378, 186, 4), (322, 436, 4),
]

# ร่าง — (d, มีพื้นจาง, opacity เส้น)
BODY = [
    ("M170 520 L500 506 L594 534 L594 580 L170 592 Z", False, ".4"),
    ("M170 520 L594 534", False, ".4"),
    ("M356 336 L474 328 L502 374 L498 476 L452 502 L372 502 Z", False, ".28"),
    ("M282 62 L326 78 L336 116 L316 146 L286 148 L268 116 L268 82 Z", True, None),
    ("M286 148 L316 146 L300 158 Z", True, None),
    ("M318 146 L378 186 L424 262 L448 340 L360 348 L326 258 L308 190 Z", True, None),
    ("M326 258 L360 348", False, None),
    ("M324 196 L286 288 L238 348 L214 336 L268 262 L300 188 Z", True, None),
    ("M214 336 L238 348 L300 214 L288 162 L266 168 L262 226 Z", True, None),
    ("M266 168 L288 162 L302 152 L296 138 L272 142 Z", True, None),
    ("M378 186 L410 272 L378 340 L352 330 L386 268 L356 196 Z", True, None),
    ("M360 348 L250 350 L206 378 L226 412 L340 398 L406 360 Z", True, None),
    ("M226 412 L206 378 L222 486 L266 492 Z", True, None),
    ("M222 486 L266 492 L294 512 L210 516 Z", False, None),
    ("M406 360 L340 398 L322 436 L376 442 L444 392 Z", True, None),
    ("M322 436 L376 442 L384 498 L336 496 Z", True, None),
    ("M336 496 L384 498 L414 518 L326 520 Z", False, None),
]

ARIA = {
    "en": ("An abstract line drawing of a seated figure, elbow on knee and hand at the "
           "chin, with a knowledge graph of linked nodes opening out from the head"),
    "th": ("ภาพลายเส้นแบบนามธรรม คนนั่งคิด ศอกวางบนเข่า มือแตะคาง "
           "มีกราฟความรู้เป็นโหนดและเส้นเชื่อมแผ่ออกจากศีรษะ"),
}

LAB = {
    "en": "THE PERSON DRAWS THE LINE · THE GRAPH KEEPS IT",
    "th": "คนลากเส้น เครื่องเก็บเส้น",
}

CAP = {
    "en": ("<b>Illustrative.</b> An ontology and a knowledge graph will hold every line "
           "you give them. Neither can tell you which line means something. Every line in "
           "this picture starts with the person on the left."),
    "th": ("<b>ภาพประกอบ</b> ออนโทโลยีและกราฟความรู้เก็บเส้นเชื่อมได้ทุกเส้นที่เราป้อนให้ "
           "แต่ไม่มีเครื่องมือตัวไหนบอกได้ว่าเส้นไหนมีความหมาย "
           "ทุกเส้นในภาพนี้เริ่มจากคนที่นั่งอยู่ทางซ้าย"),
}


def figure(lang: str) -> str:
    p = []
    p.append('    <figure class="rv">')
    p.append('      <div class="dbox">')
    p.append(f'        <div class="dlab go">{LAB[lang]}</div>')
    p.append(f'        <svg class="dsvg" viewBox="0 0 900 620" role="img" '
             f'aria-label="{ARIA[lang]}">')

    p.append('          <g class="tk-e">')
    for d in EDGES:
        p.append(f'            <path d="{d}"/>')
    p.append('          </g>')

    p.append('          <g class="tk-n">')
    for x, y, r in GRAPH_NODES:
        p.append(f'            <circle cx="{x}" cy="{y}" r="{r}"/>')
    p.append('          </g>')

    p.append('          <g class="tk-l">')
    for d, filled, op in BODY:
        cls = ' class="tk-f"' if filled else ''
        o = f' opacity="{op}"' if op else ''
        p.append(f'            <path d="{d}"{cls}{o}/>')
    p.append('          </g>')

    p.append('          <g class="tk-n">')
    for x, y, r in BODY_NODES:
        p.append(f'            <circle cx="{x}" cy="{y}" r="{r}"/>')
    p.append('          </g>')

    p.append('        </svg>')
    p.append('      </div>')
    p.append(f'      <figcaption>{CAP[lang]}</figcaption>')
    p.append('    </figure>')
    return "\n".join(p)


# ---------------------------------------------------------------- ตัวช่วย

def drop_css(src: str, name: str) -> str:
    out, removed = [], 0
    for line in src.split("\n"):
        s = line.strip()
        if any(s.startswith(d) for d in DEAD):
            removed += 1
            continue
        out.append(line)
    print(f"    ลบกฎ CSS {removed} บรรทัด")
    return "\n".join(out)


def add_css(src: str) -> str:
    anchor = "\n.dlab{"
    k = src.index(anchor) + 1
    return src[:k] + CSS_NEW + src[k:]


def add_figure(src: str, lang: str) -> str:
    """แทรกภาพก่อนบล็อก story แรก"""
    m = re.search(r'[ \t]*<div class="story rv"', src)
    if not m:
        sys.exit("[abort] หา .story rv ไม่เจอ")
    return src[:m.start()] + figure(lang) + "\n\n" + src[m.start():]


def split_stories(src: str) -> str:
    """ห่อ <p> ในบล็อก story ด้วยสองคอลัมน์ ไม่แตะข้อความข้างใน"""
    lines = src.split("\n")
    starts = [i for i, l in enumerate(lines) if 'class="story rv"' in l]
    if not starts:
        sys.exit("[abort] หา story ไม่เจอ")

    for start in reversed(starts):
        # หาปลายบล็อก
        depth, end = 0, None
        for i in range(start, len(lines)):
            depth += lines[i].count("<div") - lines[i].count("</div>")
            if depth == 0 and i > start:
                end = i
                break
        if end is None:
            sys.exit("[abort] หาปลาย story ไม่เจอ")

        p_open = [i for i in range(start, end) if lines[i].strip().startswith("<p")]
        p_close = [i for i in range(start, end) if lines[i].strip() == "</p>"]
        # เกณฑ์เดียวกันทั้งสองภาษา แตกเฉพาะบล็อกที่ยาวจริง ตั้งแต่ห้าย่อหน้าขึ้นไป
        # บล็อกที่สองของหน้าอังกฤษมีสองย่อหน้า จึงไม่แตก และภาษาไทยก็ต้องไม่แตกตาม
        if len(p_open) < 5 or len(p_open) != len(p_close):
            print(f"    [skip] story ที่บรรทัด {start+1}: มี {len(p_open)} ย่อหน้า")
            continue

        half = (len(p_open) + 1) // 2
        ind = " " * (len(lines[start]) - len(lines[start].lstrip()))
        body = ind + "  "

        first, mid_close, mid_open, last = (
            p_open[0], p_close[half - 1], p_open[half], p_close[-1])

        lines[last] = lines[last] + "\n" + body + "</div>"
        lines[mid_open] = body + '<div class="col">\n' + lines[mid_open]
        lines[mid_close] = lines[mid_close] + "\n" + body + "</div>"
        lines[first] = (body + '<div class="cols">\n'
                        + body + '<div class="col">\n' + lines[first])
        lines[end] = body + "</div>\n" + lines[end]
        lines[start] = lines[start].replace('class="story rv"',
                                            'class="story split rv"')
        print(f"    แตกสองคอลัมน์ · story ที่บรรทัด {start+1} · "
              f"{len(p_open)} ย่อหน้า แบ่ง {half}+{len(p_open)-half}")

    return "\n".join(lines)


def main():
    for name, lang in [("about.html", "en"), ("th-about.html", "th")]:
        p = ROOT / name
        s = p.read_text(encoding="utf-8")
        print(f"  {name}")
        s = drop_css(s, name)
        s = add_css(s)
        s = add_figure(s, lang)
        s = split_stories(s)
        p.write_text(s, encoding="utf-8")
    print("เสร็จ")


if __name__ == "__main__":
    main()
