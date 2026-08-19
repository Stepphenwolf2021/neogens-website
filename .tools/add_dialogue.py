#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
แทรกหัวข้อ "อีกฝั่งของแผ่นเดียวกันเห็นอะไร" ลงหน้าเกษตรกร

บทสนทนาระหว่างคนปลูกกับโรงคั่วที่อ่านข้อมูลชุดเดียวกันคนละบรรทัด
สี่ฟิลด์ที่ยกมาคุยกันคือฟิลด์ที่มีอยู่จริงในแผงของ coffee-demo.html
โปรไฟล์รส · คะแนนคัปปิ้งเฉลี่ย · สาวกลับถึงแปลง · เส้นทางที่ยืนยันแล้ว

แทรกเป็นหัวข้อ 03 แล้วเลื่อน 03→04 และ 04→05
ตรวจแล้วว่าไม่มีลิงก์ไหนในเว็บชี้มาที่ #s03 หรือ #s04 การเลื่อนเลขจึงไม่ทำลิงก์พัง

คลาสใหม่ทุกตัวขึ้นต้นด้วย dlg- และมีด่านตรวจว่าไม่ชนของเดิม ตามบทเรียนข้อ 8
ด่านท้ายสคริปต์นับชิ้นส่วนในไฟล์ผลลัพธ์แล้ว exit ถ้าขาด ตามบทเรียนข้อ 9

ไฟล์ไทยไม่ใส่ letter-spacing กับป้าย mono เพราะข้อความในป้ายเป็นภาษาไทย
line-height ของบทพูดอยู่ที่ 1.8 ตามช่วงที่กำหนดไว้ 1.75–1.9

รันจากรากรีโป:  python3 .tools/add_dialogue.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CSS

MARK = "/* --- บทสนทนาคนปลูก / โรงคั่ว --- */"

CSS_TMPL = """
/* --- บทสนทนาคนปลูก / โรงคั่ว --- */
.dlg{{margin:30px 0 34px;display:flex;flex-direction:column;gap:13px}}
.dlg-turn{{max-width:86%;border:1px solid var(--line);border-radius:16px;
  background:var(--surface);padding:17px 20px}}
.dlg-turn.grower{{align-self:flex-start;border-left:2px solid var(--go)}}
.dlg-turn.roaster{{align-self:flex-end;background:var(--surface-2);
  border-right:2px solid var(--ask)}}
.dlg-head{{display:flex;flex-wrap:wrap;align-items:baseline;gap:9px;margin-bottom:8px}}
.dlg-who{{font-family:var(--mono);font-size:11px;letter-spacing:{ls};color:var(--go)}}
.dlg-turn.roaster .dlg-who{{color:var(--ask)}}
.dlg-field{{font-family:var(--mono);font-size:10.5px;letter-spacing:{ls};color:var(--mute);
  border:1px solid var(--line);border-radius:999px;padding:3px 9px}}
.dlg-turn p{{margin:0;font-size:16.5px;line-height:1.8;color:var(--fg)}}
.dlg-foot{{color:var(--dim)}}
@media(max-width:620px){{.dlg-turn{{max-width:100%}}}}
"""

# ---------------------------------------------------------------- เนื้อหา

EN = {
    "ls": ".08em",
    "title": "What the other side is reading",
    "intro": "One record, two people who have never met — a grower in Chiang Rai "
             "and a roaster in northern Europe, both open on the same page of the "
             "vault, each reading a different line in it. Illustrative.",
    "grower": "GROWER · CHIANG RAI",
    "roaster": "ROASTER · NORTHERN EUROPE",
    "turns": [
        ("grower", "FLAVOUR PROFILE",
         "I have said for years that this coffee tastes of longan and tamarind. "
         "Every sheet handed to me offers berry, cocoa, caramel. So berry is what "
         "gets written down, and the words we actually use for our own coffee "
         "never leave the farm."),
        ("roaster", "FLAVOUR PROFILE",
         "Longan is the one thing I cannot buy anywhere else. If the record says "
         "longan and I taste longan, that is a bag I can sell under its own name "
         "instead of burying it in a blend."),
        ("grower", "MEAN CUP SCORE",
         "The harvest goes out and one number comes back, from the person buying "
         "it. In all these years I have never known whether that number was a good "
         "one."),
        ("roaster", "MEAN CUP SCORE",
         "I have had your country's average for years. It arrives in the supplier "
         "reports every season. It has never occurred to this trade that the person "
         "growing the coffee does not have it."),
        ("grower", "TRACEABLE TO PLOT",
         "They ask for papers proving where the trees stand. We know where they "
         "stand. There is simply no way to prove it to someone we will never meet."),
        ("roaster", "TRACEABLE TO PLOT",
         "And without it I cannot bring the coffee into Europe at all. Once the "
         "plot is on record you stop being a risk on my compliance list and become "
         "a supplier I can plan a year around."),
        ("grower", "VERIFIED ROUTES",
         "We sell to the mill and it ends there. After that nobody tells us which "
         "country drinks it."),
        ("roaster", "VERIFIED ROUTES",
         "Ask and I will tell you. Knowing which market pays for what you already "
         "grow is worth more to you than another kilo of yield."),
    ],
    "foot": "Nobody in that exchange added anything new. Every fact in it exists "
            "today — the only difference is that each side can see its own half and "
            "not the other. The vault does not create knowledge. It makes the same "
            "knowledge readable from both ends.",
    "link": '<p class="dlg-foot">All four of those fields are on the '
            '<a href="coffee-demo.html">demo dashboard</a> — click any origin on the '
            'map to see them.</p>',
}

TH = {
    "ls": "0",
    "title": "อีกฝั่งของแผ่นเดียวกันเห็นอะไร",
    "intro": "ข้อมูลชุดเดียว คนสองคนที่ไม่เคยเจอหน้ากัน — คนปลูกอยู่บนดอยในเชียงราย "
             "โรงคั่วอยู่ยุโรปเหนือ ทั้งคู่เปิดหน้าเดียวกันในคลัง แล้วอ่านได้คนละบรรทัด "
             "ตัวอย่างเพื่อให้เห็นภาพ",
    "grower": "คนปลูก · เชียงราย",
    "roaster": "โรงคั่ว · ยุโรปเหนือ",
    "turns": [
        ("grower", "โปรไฟล์รส",
         "บอกมาตลอดว่ากาแฟที่นี่มีกลิ่นลำไยกับมะขาม แต่ใบที่เขายื่นมาให้กรอกมีแต่ "
         "เบอร์รี่ โกโก้ คาราเมล ก็ต้องกรอกตามนั้น คำที่ใช้เรียกกาแฟของตัวเองจริง ๆ "
         "เลยไม่เคยออกไปพ้นสวน"),
        ("roaster", "โปรไฟล์รส",
         "ลำไยคือสิ่งที่หาซื้อจากที่อื่นไม่ได้ ถ้าในบันทึกเขียนว่าลำไย แล้วชิมแล้วเจอจริง "
         "นั่นคือถุงที่ขายได้ในชื่อของมันเอง ไม่ใช่เมล็ดที่เอาไปผสมอยู่ในเบลนด์"),
        ("grower", "คะแนนคัปปิ้งเฉลี่ย",
         "ส่งผลผลิตไปแล้วได้ยินตัวเลขกลับมาตัวเดียว จากปากคนที่รับซื้อ "
         "ตลอดมาไม่เคยรู้ว่าตัวเลขนั้นถือว่าดีหรือไม่ดี"),
        ("roaster", "คะแนนคัปปิ้งเฉลี่ย",
         "ค่าเฉลี่ยของประเทศคุณ ฝั่งนี้รู้มาหลายปีแล้ว มันอยู่ในรายงานที่ซัพพลายเออร์ส่งให้ทุกฤดู "
         "ไม่มีใครในวงการเคยคิดว่าคนปลูกไม่มีตัวเลขนี้อยู่ในมือ"),
        ("grower", "สาวกลับถึงแปลง",
         "เขาขอเอกสารยืนยันว่าต้นกาแฟอยู่ตรงไหน เรารู้อยู่แล้วว่ามันอยู่ตรงไหน "
         "แต่ไม่มีทางพิสูจน์ให้คนที่ไม่มีวันได้เจอหน้ากันดู"),
        ("roaster", "สาวกลับถึงแปลง",
         "และถ้าไม่มีอันนี้ นำกาแฟเข้ายุโรปไม่ได้เลย พอแปลงของคุณอยู่ในระบบ "
         "คุณจะเลิกเป็นความเสี่ยงในรายการตรวจ แล้วกลายเป็นคนที่วางแผนสั่งของล่วงหน้าทั้งปีได้"),
        ("grower", "เส้นทางที่ยืนยันแล้ว",
         "ขายให้โรงสี จบตรงนั้น หลังจากนั้นไม่มีใครบอกว่ากาแฟที่ปลูกไปอยู่ประเทศไหน"),
        ("roaster", "เส้นทางที่ยืนยันแล้ว",
         "ถามมาก็ตอบได้ การรู้ว่าตลาดไหนจ่ายให้กับสิ่งที่คุณปลูกอยู่แล้ว "
         "มีค่ากับคุณมากกว่าผลผลิตที่เพิ่มขึ้นอีกกิโลหนึ่ง"),
    ],
    "foot": "ไม่มีใครในบทสนทนานี้เพิ่มข้อมูลใหม่เข้าไปสักชิ้น ทุกอย่างที่พูดกันมีอยู่แล้ววันนี้ "
            "ต่างแค่ว่าแต่ละฝ่ายเห็นได้เฉพาะครึ่งของตัวเอง คลังความรู้ไม่ได้สร้างความรู้ใหม่ "
            "มันแค่ทำให้ความรู้ชุดเดิมอ่านได้จากทั้งสองปลาย",
    "link": '<p class="dlg-foot">ทั้งสี่ฟิลด์ที่ยกมาคุยกันอยู่บน'
            '<a href="coffee-demo.html">หน้าเดโม</a> คลิกจุดต้นทางบนแผนที่แล้วเห็นได้เลย '
            'หน้านั้นยังมีเฉพาะภาษาอังกฤษ</p>',
}


def section(d):
    """ประกอบ HTML ของหัวข้อทั้งก้อน"""
    turns = []
    for who, field, said in d["turns"]:
        turns.append(
            f'<div class="dlg-turn {who}">'
            f'<div class="dlg-head"><span class="dlg-who">{d[who]}</span>'
            f'<span class="dlg-field">{field}</span></div>'
            f'<p>{said}</p></div>'
        )
    return (
        f'<h2 id="s03"><span class="sn">03</span>{d["title"]}</h2>\n'
        f'<p>{d["intro"]}</p>\n'
        f'<div class="dlg">\n' + "\n".join(turns) + "\n</div>\n"
        f'<p>{d["foot"]}</p>\n'
        f'{d["link"]}\n\n'
    )


# ---------------------------------------------------------------- ลงมือ

def build(path, d):
    s = original = path.read_text(encoding="utf-8")

    if "dlg-turn" in s:
        sys.exit(f"✗ {path.name} มีบทสนทนาอยู่แล้ว ยังไม่ได้แตะไฟล์")
    for cls in ("dlg", "dlg-turn", "dlg-who", "dlg-field", "dlg-head", "dlg-foot"):
        if re.search(r"\." + cls + r"[{,\s]", s):
            sys.exit(f"✗ {path.name} มีคลาส .{cls} อยู่ก่อนแล้ว ต้องเปลี่ยนชื่อก่อน")

    # เลื่อนเลขหัวข้อ ทำ 04 ก่อน 03 กันเลขทับกัน
    s = s.replace('<h2 id="s04"><span class="sn">04</span>',
                  '<h2 id="s05"><span class="sn">05</span>', 1)
    s = s.replace('<h2 id="s03"><span class="sn">03</span>',
                  '<h2 id="s04"><span class="sn">04</span>', 1)

    # แทรกหัวข้อใหม่ก่อนหัวข้อที่เพิ่งกลายเป็น 04
    anchor = '<h2 id="s04">'
    if anchor not in s:
        sys.exit(f"✗ {path.name} หาจุดแทรกไม่เจอ")
    s = s.replace(anchor, section(d) + anchor, 1)

    # แทรก CSS ก่อนปิดบล็อก style
    css = CSS_TMPL.format(ls=d["ls"])
    if "</style>" not in s:
        sys.exit(f"✗ {path.name} ไม่มี </style>")
    s = s.replace("</style>", css + "</style>", 1)

    # ---- ด่านตรวจ นับของจริงในผลลัพธ์ ไม่เชื่อว่า replace สำเร็จ ----
    checks = {
        "ไฟล์เปลี่ยนจริง": s != original,
        "บทพูดครบ 8 ช่วง": s.count('class="dlg-turn ') == 8,
        "ฝั่งคนปลูก 4 ช่วง": s.count('class="dlg-turn grower"') == 4,
        "ฝั่งโรงคั่ว 4 ช่วง": s.count('class="dlg-turn roaster"') == 4,
        "ป้ายฟิลด์ครบ 8 ป้าย": s.count('class="dlg-field"') == 8,
        "กล่องหุ้มบทสนทนา 1 อัน": s.count('<div class="dlg">') == 1,
        "หัวข้อครบ 5 ระดับ": [re.search(f'id="s0{n}"', s) is not None
                              for n in range(1, 6)] == [True] * 5,
        "ไม่เหลือเลขซ้ำ": all(s.count(f'<span class="sn">0{n}</span>') == 1
                              for n in range(1, 6)),
        "CSS อยู่ในบล็อก style": ".dlg-turn{" in s and s.index(".dlg-turn{") < s.index("</style>"),
        "CSS ชุดเดียว ไม่ซ้ำ": s.count(MARK) == 1,
        # .dlg-who{ นับได้สองครั้งเพราะมีกฎซ้อนของฝั่งโรงคั่วด้วย จึงเช็กแค่ว่ามีจริง
        "กฎย่อยครบทุกตัว": all(r in s for r in
                              (".dlg{", ".dlg-turn.grower{", ".dlg-turn.roaster{",
                               ".dlg-who{", ".dlg-field{", ".dlg-turn p{",
                               ".dlg-head{", ".dlg-foot{")),
        "ลิงก์ไปหน้าเดโม": s.count('href="coffee-demo.html"') >= 1,
        "ไม่มี letter-spacing ติดลบในกฎใหม่": "letter-spacing:-" not in css,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit("✗ " + path.name + " ด่านตรวจไม่ผ่าน: " + " · ".join(bad))

    path.write_text(s, encoding="utf-8")
    print(f"✓ {path.name}  {len(original) // 1024} KB → {len(s) // 1024} KB  "
          f"· บทพูด 8 ช่วง · หัวข้อ 5 ระดับ")


for name, data in (("coffee-farmer.html", EN), ("th-coffee-farmer.html", TH)):
    build(ROOT / name, data)

print("เสร็จแล้ว ทั้งสองไฟล์ผ่านด่านตรวจครบทุกข้อ")
