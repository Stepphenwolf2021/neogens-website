#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เขียนบล็อก 01 กับ 02 ของหน้า layer ใหม่ · layer.html + th-layer.html

เปลี่ยนวิธีอธิบายเป็นแบบเดียวกับไดอะแกรมที่ Noppadol ส่งมา
  ontology       = แบบ  มีแต่ประเภทของ ยังไม่มีของจริงสักชิ้น
  knowledge graph = แบบเดิมนั้น ที่มีของจริงกรอกลงไปแล้ว
พร้อมภาพประกอบสองฝั่งวางคั่นระหว่างบล็อก 02 กับ 03

บล็อก 03 mission-driven และ 04 AI-friendly คงเดิมทุกตัวอักษร

ภาพใช้คลาส .dsvg ที่หน้านี้มีอยู่แล้วทั้งหมด ไม่สร้างคลาสใหม่แม้แต่ตัวเดียว
ตามบทเรียนข้อ 8 เรื่องชื่อคลาสชนกัน

รันจากรากรีโป:  python3 .tools/rewrite_layer.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- เนื้อหาใหม่

BLK = {
    "ontology-and-knowledge-graph.html": [
        ("01", "An ontology is the pattern — it holds no actual things",
         ["An ontology is an agreement made in advance: what kinds of things this "
          "organisation keeps, what each kind is called, and how the kinds connect to "
          "one another.",
          "Say the pattern has objects, and it has makers. Every object goes by a name. "
          "Every maker works out of a place. And an object joins a maker through one "
          "phrase — <em>made by</em>. Nothing real has been filed against any of it yet.",
          "Written once. Used across the whole organisation."]),
        ("02", "A knowledge graph is that same pattern with the real holdings filled in",
         ["Put what you actually hold into the pattern and you have a knowledge graph. "
          "One hammered alms bowl, made by the smiths of Ban Bu. The bowl carries its own "
          "name, the smiths carry their own place, and every line drawn in the pattern now "
          "has something real hanging off it.",
          "Here is the difference that earns its keep. In ordinary systems the link between "
          "the bowl and the smiths gets rebuilt from scratch every time somebody asks for "
          "it. In a graph that link is already there — it has a name, it has a direction, "
          "and anything can walk along it."]),
    ],
    "th-ontology-and-knowledge-graph.html": [
        ("01", "ontology คือแบบ ยังไม่มีของจริงสักชิ้นอยู่ในนั้น",
         ["ontology คือการตกลงกันไว้ล่วงหน้าว่า องค์กรนี้เก็บของกี่ประเภท "
          "แต่ละประเภทเรียกว่าอะไร และประเภทไหนเกี่ยวกับประเภทไหน",
          "สมมติว่าในแบบมี วัตถุ กับ ผู้สร้าง วัตถุทุกชิ้นมีชื่อที่คนเรียกกัน "
          "ผู้สร้างทุกคนมีถิ่นที่ทำงาน และวัตถุต่อกับผู้สร้างด้วยคำเดียวคือ “ทำโดย” "
          "ถึงตรงนี้ยังไม่มีของจริงสักชิ้นถูกกรอกลงไป",
          "เขียนครั้งเดียว ใช้ได้ทั้งองค์กร"]),
        ("02", "knowledge graph คือแบบเดิมนั้น ที่ของจริงถูกกรอกลงไปแล้ว",
         ["พอเอาของที่องค์กรถือไว้จริงมาใส่ตามแบบ ก็ได้ knowledge graph "
          "ขันลงหินหนึ่งใบ ทำโดย ช่างบ้านบุ ขันใบนั้นมีชื่อของมันเอง ช่างมีถิ่นของเขาเอง "
          "เส้นทุกเส้นที่ลากไว้ในแบบ ตอนนี้มีของจริงห้อยอยู่",
          "ความต่างที่คุ้มค่าอยู่ตรงนี้ ในระบบทั่วไป ความเกี่ยวข้องระหว่างขันกับช่าง "
          "ต้องประกอบขึ้นใหม่ทุกครั้งที่มีคนถาม แต่ในกราฟ เส้นนั้นถูกเก็บไว้อยู่ก่อนแล้ว "
          "มีชื่อ มีทิศทาง และเดินตามได้"]),
    ],
}

# ---------------------------------------------------------------- ภาพประกอบ

TXT = {
    "ontology-and-knowledge-graph.html": dict(
        lab="THE PATTERN, AND THE SAME PATTERN FILLED IN",
        left="THE PATTERN", right="WHAT YOU ACTUALLY HOLD",
        n1="Object", n2="Maker", n3="The alms bowl", n4="The Ban Bu smiths",
        edge="made by",
        a1="goes by", a2="works from", v1="a name", v2="a place",
        v3="“Hammered alms bowl”", v4="Ban Bu, Bangkok",
        aria=("Two diagrams side by side. On the left a pattern: a circle marked Object "
              "linked to a circle marked Maker through the phrase made by, each with an "
              "empty value box below it. On the right the same shape with real holdings "
              "filled in: the alms bowl, the Ban Bu smiths, and their actual values"),
        cap=("<b>Illustrative.</b> Same shape on both sides. The left one is agreed on "
             "before anything is filed; the right one is what the organisation actually "
             "holds, sitting in it."),
    ),
    "th-ontology-and-knowledge-graph.html": dict(
        lab="แบบ กับ แบบเดียวกันที่กรอกของจริงลงไปแล้ว",
        left="แบบ", right="ของจริงที่องค์กรถือไว้",
        n1="วัตถุ", n2="ผู้สร้าง", n3="ขันลงหิน", n4="ช่างบ้านบุ",
        edge="ทำโดย",
        a1="มีชื่อว่า", a2="ทำงานอยู่ที่", v1="ชื่อเรียก", v2="ถิ่นที่ทำงาน",
        v3="“ขันลงหินสลักลาย”", v4="บ้านบุ กรุงเทพฯ",
        aria=("ไดอะแกรมสองฝั่งวางเทียบกัน ฝั่งซ้ายคือแบบ วงกลมคำว่าวัตถุต่อกับวงกลมคำว่าผู้สร้าง "
              "ด้วยคำว่าทำโดย ใต้แต่ละวงมีกล่องค่าที่ยังว่าง ฝั่งขวาเป็นรูปเดียวกัน "
              "แต่กรอกของจริงลงไปแล้ว คือขันลงหิน ช่างบ้านบุ และค่าจริงของทั้งคู่"),
        cap=("<b>ภาพประกอบ</b> สองฝั่งเป็นรูปเดียวกัน ฝั่งซ้ายตกลงกันไว้ก่อนจะมีของสักชิ้น "
             "ฝั่งขวาคือของที่องค์กรถือไว้จริง เข้าไปนั่งอยู่ในนั้น"),
    ),
}


def build_svg(k):
    t = TXT[k]
    n = ["<svg class=\"dsvg\" viewBox=\"0 0 900 342\" role=\"img\" "
         f"aria-label=\"{t['aria']}\">"]

    def block(x, lab, lab_cls, node_cls, val_cls, top, bot, at1, at2, val1, val2):
        c1, c2 = x + 104, x + 296
        o = [f'  <text class="{lab_cls}" x="{x + 8}" y="24">{lab}</text>']
        for cx, label in ((c1, top), (c2, bot)):
            o.append(f'  <circle class="{node_cls}" cx="{cx}" cy="120" r="56"/>')
            o.append(f'  <text class="t-b" x="{cx}" y="125" text-anchor="middle">{label}</text>')
        # เส้นความสัมพันธ์ พร้อมป้ายคร่อมเส้น
        o.append(f'  <path class="ln" d="M{c2 - 56} 120 H{c1 + 64}"/>')
        o.append(f'  <path class="ln" d="M{c1 + 78} 111 L{c1 + 62} 120 L{c1 + 78} 129"/>')
        mid = (c1 + c2) // 2
        o.append(f'  <rect class="bx" x="{mid - 38}" y="108" width="76" height="24" rx="6"/>')
        o.append(f'  <text class="m" x="{mid}" y="123" text-anchor="middle">{t["edge"]}</text>')
        # คุณสมบัติใต้แต่ละวง
        for cx, at, val in ((c1, at1, val1), (c2, at2, val2)):
            o.append(f'  <path class="ln-gh" d="M{cx} 176 V210"/>')
            o.append(f'  <text class="m" x="{cx}" y="228" text-anchor="middle">{at}</text>')
            o.append(f'  <path class="ln-gh" d="M{cx} 236 V266"/>')
            o.append(f'  <path class="ln-gh" d="M{cx - 7} 257 L{cx} 269 L{cx + 7} 257"/>')
            o.append(f'  <rect class="{val_cls}" x="{cx - 86}" y="272" width="172" height="38" rx="8"/>')
            o.append(f'  <text class="t-s" x="{cx}" y="296" text-anchor="middle">{val}</text>')
        return o

    n += block(20, t["left"], "m-as", "bx-as", "bx-as",
               t["n1"], t["n2"], t["a1"], t["a2"], t["v1"], t["v2"])
    n.append('  <path class="ln-gh" d="M450 34 V320"/>')
    n += block(470, t["right"], "m-go", "bx-go", "bx-go",
               t["n3"], t["n4"], t["a1"], t["a2"], t["v3"], t["v4"])
    n.append("</svg>")
    return "\n        ".join(n)


def check_classes(src: str, svg: str, name: str) -> None:
    """ทุกคลาสที่ภาพเรียกใช้ ต้องมีกฎ .dsvg .<cls> อยู่จริงในไฟล์นั้น

    ไฟล์ไทยกับไฟล์อังกฤษมีชุดคลาสไม่เท่ากัน เคยพลาดมาแล้วเพราะ .bx-gh
    มีเฉพาะฝั่งอังกฤษ พอเรียกใช้ในไฟล์ไทย rect เลยกลายเป็นสี่เหลี่ยมดำทึบ
    """
    used = set(re.findall(r'class="([a-z0-9\- ]+)"', svg)) - {"dsvg"}
    missing = [c for c in sorted(used)
               if not re.search(r"\.dsvg \." + re.escape(c) + r"\{", src)]
    if missing:
        sys.exit(f"[abort] {name}: ไฟล์นี้ไม่มีกฎของคลาส {missing}")


def figure(k):
    t = TXT[k]
    return ("    <figure class=\"rv\">\n"
            "      <div class=\"dbox\">\n"
            f"        <div class=\"dlab go\">{t['lab']}</div>\n"
            f"        {build_svg(k)}\n"
            "      </div>\n"
            f"      <figcaption>{t['cap']}</figcaption>\n"
            "    </figure>")


# ---------------------------------------------------------------- ประกอบหน้า

def blk_html(n, h3, ps):
    body = "".join(f"<p>{p}</p>" for p in ps)
    return f'<div class="blk rv"><div class="n">{n}</div><h3>{h3}</h3>{body}</div>'


def main():
    for k in ("ontology-and-knowledge-graph.html", "th-ontology-and-knowledge-graph.html"):
        p = ROOT / k
        s = p.read_text(encoding="utf-8")
        print(f"  {k}")

        check_classes(s, build_svg(k), k)

        m = re.search(r'([ \t]*)<div class="blks ?">(.*?)</div>\n', s, re.S)
        if not m:
            sys.exit(f"[abort] {k}: หา .blks ไม่เจอ")

        inner = m.group(2)
        parts = re.findall(r'<div class="blk rv">.*?</div></div>', inner)
        if len(parts) != 4:
            # แยกด้วยตัวเลขกำกับแทน เมื่อ regex ด้านบนจับไม่ครบ
            parts = [x for x in re.split(r'(?=<div class="blk rv">)', inner) if x.strip()]
        if len(parts) != 4:
            sys.exit(f"[abort] {k}: คาดว่ามี 4 บล็อก แต่พบ {len(parts)}")

        keep34 = "".join(parts[2:])
        new12 = "".join(blk_html(n, h, ps) for n, h, ps in BLK[k])
        ind = m.group(1)

        block = (f'{ind}<div class="blks ">{new12}</div>\n'
                 f'{figure(k)}\n'
                 f'{ind}<div class="blks ">{keep34}</div>\n')

        s = s[:m.start()] + block + s[m.end():]
        p.write_text(s, encoding="utf-8")
        print("    เขียนบล็อก 01–02 ใหม่ · แทรกภาพ · บล็อก 03–04 คงเดิม")


if __name__ == "__main__":
    main()
