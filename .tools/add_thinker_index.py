#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เพิ่มภาพประกอบในหน้าแรก · index.html + th-index.html

ร่างเดียวกับหน้า about แต่เปลี่ยนสิ่งที่อยู่รอบตัว จากกราฟความรู้ที่เชื่อมถึงกัน
เป็นกล่องข้อมูลกระจัดกระจาย สี่เหลี่ยม สามเหลี่ยม วงกลม ไม่มีเส้นเชื่อมสักเส้น
ตรงกับประโยคที่อยู่บนหน้าอยู่แล้ว — ทุกกล่องเต็ม แต่ไม่มีอะไรวิ่งระหว่างกล่อง

วางไว้ใต้ย่อหน้านำของ section pband ก่อนการ์ดสี่ใบ

รันจากรากรีโป:  python3 .tools/add_thinker_index.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CSS ที่ต้องมี

CSS_NEW = (".tk-l{stroke:var(--fg);stroke-width:1.8;fill:none;"
           "stroke-linejoin:round;stroke-linecap:round}\n"
           ".tk-f{fill:rgba(var(--w-rgb),.05)}\n")

# ---------------------------------------------------------------- ร่างคนนั่งคิด
# ชุดเดียวกับหน้า about — (d, มีพื้นจาง, opacity เส้น)

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

# ---------------------------------------------------------------- กล่องข้อมูล
# ไม่มีเส้นเชื่อมระหว่างกันแม้แต่เส้นเดียว นั่นคือประเด็นทั้งหมดของภาพ
# ตำแหน่งสร้างจากสุ่มที่ตรึง seed ไว้ จึงได้ผลเดิมทุกครั้งที่รันซ้ำ
# และไม่มีชิ้นไหนตกในกรอบที่ร่างคนนั่งอยู่

FIGURE_BOX = (322, 74, 694, 528)   # เขตห้ามวาง — ซ้าย บน ขวา ล่าง
CANVAS = (900, 620)
N_SHAPES = 125


def make_shapes():
    import random
    rnd = random.Random(7)
    W, H = CANVAS
    fx0, fy0, fx1, fy1 = FIGURE_BOX
    out, placed = [], []

    def clashes(x0, y0, x1, y1):
        if x1 > fx0 and x0 < fx1 and y1 > fy0 and y0 < fy1:
            return True
        for a0, b0, a1, b1 in placed:
            if x1 > a0 - 6 and x0 < a1 + 6 and y1 > b0 - 6 and y0 < b1 + 6:
                return True
        return False

    kinds = ["r"] * 5 + ["c"] * 3 + ["t"] * 2
    guard = 0
    while len(out) < N_SHAPES and guard < 40000:
        guard += 1
        kind = rnd.choice(kinds)
        cls = "bx" if rnd.random() < .55 else "bx-gh"
        if kind == "r":
            w = rnd.randint(26, 74)
            h = rnd.randint(16, 40)
            x = rnd.randint(6, W - w - 6)
            y = rnd.randint(6, H - h - 6)
            box = (x, y, x + w, y + h)
            shape = ("r", (x, y, w, h), cls)
        elif kind == "c":
            r = rnd.randint(7, 18)
            x = rnd.randint(6 + r, W - r - 6)
            y = rnd.randint(6 + r, H - r - 6)
            box = (x - r, y - r, x + r, y + r)
            shape = ("c", (x, y, r), cls)
        else:
            r = rnd.randint(9, 22)
            x = rnd.randint(6 + r, W - r - 6)
            y = rnd.randint(6 + r, H - r - 6)
            box = (x - r, y - r, x + r, y + r)
            shape = ("t", (x, y, r), cls)
        if clashes(*box):
            continue
        placed.append(box)
        out.append(shape)
    return out


SHAPES = make_shapes()

TXT = {
    "index.html": dict(
        lab="EVERY BOX FULL · NOTHING RUNNING BETWEEN THEM",
        aria=("An abstract line drawing of a seated figure, elbow on knee and hand at "
              "the chin, surrounded by scattered squares, triangles and circles — "
              "boxes of information with no lines running between any of them"),
        cap=("<b>Illustrative.</b> The knowledge is all there, in boxes, and none of it "
             "was designed to connect. Everything the organisation needs to answer well "
             "is in the room, and no route runs through it."),
    ),
    "th-index.html": dict(
        lab="ทุกกล่องเต็ม แต่ไม่มีอะไรวิ่งระหว่างกล่อง",
        aria=("ภาพลายเส้นแบบนามธรรม คนนั่งคิด ศอกวางบนเข่า มือแตะคาง "
              "รายล้อมด้วยสี่เหลี่ยม สามเหลี่ยม และวงกลมกระจัดกระจาย "
              "คือกล่องข้อมูลที่ไม่มีเส้นเชื่อมถึงกันสักเส้น"),
        cap=("<b>ภาพประกอบ</b> ความรู้อยู่ครบในกล่อง และไม่มีกล่องไหนถูกออกแบบมาให้ต่อกัน "
             "ทุกอย่างที่องค์กรต้องใช้ตอบคำถามอยู่ในห้องนี้แล้ว แต่ไม่มีเส้นทางไหนเดินผ่านมันได้"),
    ),
}


def shapes_svg():
    out = []
    for kind, p, cls in SHAPES:
        if kind == "r":
            x, y, w, h = p
            out.append(f'    <rect class="{cls}" x="{x}" y="{y}" '
                       f'width="{w}" height="{h}" rx="6"/>')
        elif kind == "c":
            cx, cy, r = p
            out.append(f'    <circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}"/>')
        else:
            cx, cy, r = p
            out.append(f'    <path class="{cls}" d="M{cx} {cy - r} '
                       f'L{cx + r} {cy + r} L{cx - r} {cy + r} Z"/>')
    return out


def build_svg(k):
    t = TXT[k]
    n = ['<svg class="dsvg" viewBox="0 0 900 620" role="img" '
         f'aria-label="{t["aria"]}">']
    n += shapes_svg()
    # ร่างคน ย่อและเลื่อนมาไว้กลางภาพ ให้กล่องล้อมรอบได้ทุกด้าน
    n.append('    <g class="tk-l" transform="translate(210,44) scale(0.78)">')
    for d, filled, op in BODY:
        cls = ' class="tk-f"' if filled else ''
        o = f' opacity="{op}"' if op else ''
        n.append(f'      <path d="{d}"{cls}{o}/>')
    n.append("    </g>")
    n.append("  </svg>")
    return "\n    ".join(n)


def figure(k):
    t = TXT[k]
    return ('  <figure class="rv">\n'
            '    <div class="dbox">\n'
            f'      <div class="dlab go">{t["lab"]}</div>\n'
            f'    {build_svg(k)}\n'
            "    </div>\n"
            f'    <figcaption>{t["cap"]}</figcaption>\n'
            "  </figure>")


def check_classes(src, svg, name):
    """ทุกคลาสในภาพต้องมีกฎอยู่จริงในไฟล์นั้น ตามบทเรียนข้อ 8"""
    used = set(re.findall(r'class="([a-z0-9\- ]+)"', svg)) - {"dsvg"}
    missing = []
    for c in sorted(used):
        if c.startswith("tk-"):
            if f".{c}{{" not in src:
                missing.append(c)
        elif not re.search(r"\.dsvg \." + re.escape(c) + r"\{", src):
            missing.append(c)
    if missing:
        sys.exit(f"[abort] {name}: ไม่มีกฎของคลาส {missing}")


def main():
    for k in ("index.html", "th-index.html"):
        p = ROOT / k
        s = p.read_text(encoding="utf-8")
        print(f"  {k}")

        if "<figure" in s:
            print("    [ข้าม] หน้านี้มีภาพอยู่แล้ว")
            continue

        # กันชื่อคลาสชนของเดิม
        for cls in ("tk-l", "tk-f"):
            if re.search(r"(^|[\s,}])\." + cls + r"[\s,{:.]", s, re.M):
                sys.exit(f"[abort] {k}: มีคลาส .{cls} อยู่แล้ว")
        s = s.replace("\n.dlab{", "\n" + CSS_NEW + ".dlab{")

        svg = build_svg(k)
        check_classes(s, svg, k)

        # แทรกใต้ย่อหน้านำของ section pband ก่อนการ์ดสี่ใบ
        m = re.search(r'[ \t]*<div class="cards2">', s)
        if not m:
            sys.exit(f"[abort] {k}: หา .cards2 ไม่เจอ")
        s = s[:m.start()] + figure(k) + "\n" + s[m.start():]

        p.write_text(s, encoding="utf-8")
        print("    เพิ่มภาพแล้ว · วางก่อนการ์ดสี่ใบใน section pband")


if __name__ == "__main__":
    main()
