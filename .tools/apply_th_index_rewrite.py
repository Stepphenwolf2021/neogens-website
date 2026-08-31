#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ปรับหน้าแรกทั้งสองภาษา ตามไฟล์ Neo Gens (1).pdf ที่ Noppadol ส่งมาเมื่อ 2026-08-31

**ข้อความไทยทุกบรรทัดในไฟล์นี้เป็นคำของ Noppadol เอง** ยกมาจาก PDF ตรง ๆ
สิ่งเดียวที่ทำเพิ่มคือต่อคำที่ PDF สกัดออกมาแล้วมีช่องว่างแทรกกลางคำ
และคงตัวสะกด **ล็อค** ไว้ตามเว็บเดิม ตามที่เขาสั่งเมื่อถูกถาม ไม่ใช่ ล็อก อย่างใน PDF
ดูรายการเทียบทั้งหมดที่ .tools/th-index-review.md · กติกาอยู่ในข้อ 3 ของ LESSONS.md

**ฝั่งอังกฤษเขียนสำนวนเอง ไม่ได้แปลตรงตัว** ตามที่เขาสั่ง โครงเรื่องเหมือนกัน
รายการสามข้อเหมือนกัน แต่ประโยคเป็นภาษาอังกฤษที่เขียนขึ้นใหม่

สองย่อหน้าที่ PDF ไม่มี ถูกตัดออกตามที่เขายืนยัน
  1 ซึ่งธรรมชาติของข้อมูลในองค์กรนั้นแตกต่างกัน…   ในการ์ด 04
  2 แต่ความเป็นระเบียบไม่ใช่ปลายทาง…              ย่อหน้าปิด

รันซ้ำได้ ถ้าแก้ไปแล้วจะข้าม

รันจากรากรีโป:  python3 .tools/apply_th_index_rewrite.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CSS ใหม่
# ตั้งชื่อคลาสใหม่แล้ว grep ก่อนว่าไม่ชนของเดิม ตามข้อ 8 ของ LESSONS.md
# ฝั่งไทยไปอยู่ในไฟล์ร่วม ฝั่งอังกฤษฝังในหน้า เพราะ index.html ไม่ได้เอา hero-sub
# จากไฟล์ร่วม แต่ฝังไว้ในตัวเอง ดูหัวข้อ CSS อยู่ที่ไหน ใน HANDOFF
CSS_TH = ("\n.hero-list{margin:20px 0 0;padding-left:1.15em;max-width:54ch;list-style:disc;"
          "font-size:clamp(16.5px,1.9vw,19px);color:var(--dim);line-height:1.85}"
          "\n.hero-list li{margin:0 0 10px}"
          "\n.hero-list li:last-child{margin-bottom:0}"
          "\n.hero-list b{color:var(--fg);font-weight:600}\n")
CSS_EN = ("\n.hero-list{margin:20px 0 0;padding-left:1.15em;max-width:60ch;list-style:disc;"
          "font-size:clamp(17px,1.9vw,20px);color:var(--dim);line-height:1.6}"
          "\n.hero-list li{margin:0 0 10px}"
          "\n.hero-list li:last-child{margin-bottom:0}"
          "\n.hero-list b{color:var(--fg);font-weight:600}\n")

# ---------------------------------------------------------------- ภาษาไทย
TH = [
    # 1 พาดหัว
    ('<h1 class="motto" id="ng-h1">ยิ่ง AI ตอบได้ทุกเรื่อง <em>ความรู้ในองค์กรคุณยิ่งมีค่า</em></h1>',
     '<h1 class="motto" id="ng-h1">ยิ่ง AI ฉลาดขึ้น <em>ความรู้เฉพาะในองค์กรยิ่งมีคุณค่า</em></h1>'),

    # 2 + 3 ประโยคนำ รายการสามข้อ และย่อหน้าขุมทรัพย์
    ('<p class="hero-sub" id="ng-sub">เมื่อความรู้สาธารณะกลายเป็นของที่ทุกคนเข้าถึงได้เท่ากัน '
     'สิ่งที่ยังสร้างความต่างคือความรู้ที่มีอยู่เฉพาะในองค์กรของคุณ<br>'
     'เอกสารงานวิจัยที่ใช้งบลงทุนไปมากมาย ข้อมูลการตลาด บันทึกการสัมภาษณ์ลูกค้า '
     'ขั้นตอนการผลิตที่สร้างความได้เปรียบด้านต้นทุน และความรู้ที่อยู่ในพนักงานที่สั่งสมมานานหลายสิบปี '
     'เป็นความรู้ที่ถูกล็อคอยู่ในองค์กร ไม่มี AI สาธารณะไหนเข้าถึงได้</p>',

     '<p class="hero-sub" id="ng-sub">เมื่อความรู้สาธารณะกลายเป็นสิ่งที่ทุกคนเข้าถึงได้เท่ากัน '
     'สินทรัพย์เดียวที่จะสร้างความได้เปรียบแข่งขันอย่างแท้จริง คือความรู้เฉพาะที่มีอยู่แค่ในองค์กรคุณ</p>\n'
     '    <ul class="hero-list">\n'
     '      <li><b>Research &amp; Insights</b> งานวิจัยและข้อมูลการตลาดเชิงลึก '
     'ที่แลกมาด้วยงบลงทุนมากมายทุกปี</li>\n'
     '      <li><b>Operational Know-How</b> ขั้นตอนการผลิตและเทคนิคการบริหารต้นทุน '
     'ที่เป็นความลับทางธุรกิจ</li>\n'
     '      <li><b>Human Experience</b> ประสบการณ์และทักษะของพนักงาน '
     'ที่สั่งสมมานานหลายสิบปี</li>\n'
     '    </ul>\n'
     '    <p class="hero-sub">ขุมทรัพย์ความรู้เหล่านี้ถูกล็อคอยู่ภายในองค์กร '
     'ซึ่งไม่มี AI สาธารณะใดสามารถเข้าถึงได้ — และหลายครั้งแม้กระทั่งระบบ IT '
     'ที่คุณลงทุนไปมากมาย ก็ยังไม่สามารถปลดล็อคนำข้อมูลออกมาใช้ประโยชน์ได้อย่างเต็มศักยภาพ</p>'),

    # 4 ย่อหน้าความเสี่ยง
    ('<b>AI ที่ตอบคำถามแทนคุณ ตอบผิดครั้งเดียว ความเชื่อมั่นที่คนมีต่อองค์กรก็สั่นคลอน '
     'แต่ถ้าไม่ใช้เลย คำถามที่ตามมาคือ องค์กรที่คนคาดหวังสูงเรื่องการบริหารจัดการความรู้ '
     'ทำไมยังไม่ขยับ</b>',
     '<b>AI ที่ตอบผิดเพียงครั้งเดียว ความเชื่อมั่นที่คนมีต่อองค์กรก็สั่นคลอน แต่ถ้าไม่ใช้เลย '
     'คำถามที่ตามมาคือ เราจะสามารถแข่งขันในธุรกิจไปได้อีกนานแค่ไหน</b>'),

    # 5 หัวข้อภาพใหญ่
    ('<div class="pb-d">ทุกองค์กรกำลังจะเอา AI มาใช้ คำถามที่สำคัญกว่าว่าจะใช้ตัวไหน '
     'คือ AI ตัวนั้นกำลังเดินอยู่บนอะไร</div>',
     '<div class="pb-d">ถ้าเปรียบความรู้ขององค์กรถูกเก็บอยู่ในกล่อง ทุกองค์กรมีกล่องความรู้มากมาย '
     'คำถามที่สำคัญสำหรับองค์กรที่จะเริ่มนำ AI มาใช้คือ AI สามารถอ่านข้อมูลในกล่องทุกกล่องได้มั้ย '
     'และจะตรวจสอบได้อย่างไรว่า คำตอบของ AI มาจากกล่องความรู้กล่องไหนบ้าง '
     'และคำตอบนั้นถูกต้องหรือไม่ ?</div>'),

    # 6 ป้ายในภาพ และคำบรรยายใต้ภาพ
    ('<div class="dlab go">ทุกกล่องเต็ม แต่ไม่มีอะไรวิ่งระหว่างกล่อง</div>',
     '<div class="dlab go">ทุกกล่องเต็มไปด้วยความรู้ แต่ไม่มีอะไรเชื่อมโยงความรู้ระหว่างกล่อง</div>'),
    ('<figcaption><b>ภาพประกอบ</b> ความรู้อยู่ครบในกล่อง และไม่มีกล่องไหนถูกออกแบบมาให้ต่อกัน '
     'ทุกอย่างที่องค์กรต้องใช้ตอบคำถามอยู่ในห้องนี้แล้ว แต่ไม่มีเส้นทางไหนเดินผ่านมันได้</figcaption>',
     '<figcaption><b>ภาพประกอบ</b> ความรู้อยู่ครบในกล่อง แต่ไม่มีกล่องไหนถูกออกแบบมาให้เชื่อมต่อกัน '
     'ทุกอย่างที่องค์กรต้องใช้ตอบคำถามอยู่ในกล่องทั้งหมด '
     'ขาดแต่วิธีการเชื่อมโยงความรู้ระหว่างกล่องให้ AI เดินตาม</figcaption>'),

    # 7 การ์ด 02 เติมท้าย
    ('ยิ่งมีข้อมูลให้ AI ดูมากแค่ไหน ความแม่นยำในการเดาคำก็มากขึ้นตามไปด้วย</p>',
     'ยิ่งมีข้อมูลให้ AI ดูมากแค่ไหน ความแม่นยำในการเดาคำก็มากขึ้นตามไปด้วย '
     'ซึ่งอาจใช้งานได้ดีในงานทั่วๆ ไป แต่มีความเสี่ยงสูงเกินไป '
     'สำหรับการใช้ในงานที่มีความสำคัญทางธุรกิจ</p>'),

    # 8 การ์ด 03 ตัด แต่ก็ ออก
    ('<p>แต่ก็มีบางครั้งที่เราพบว่า AI สาธารณะอาจมีอาการมั่วข้อมูลขึ้นมาเองได้',
     '<p>บางครั้งที่เราพบว่า AI สาธารณะอาจมีอาการมั่วข้อมูลขึ้นมาเองได้'),

    # 9 การ์ด 04 หัวข้อและเนื้อ · ตัดย่อหน้าแรกเดิมทิ้งตามที่ยืนยัน
    ('<h3>โครงเส้นทางความรู้ที่ตรงกัน</h3>',
     '<h3>โครงเส้นทางความรู้ที่เป็นมิตรกับ AI</h3>'),
    ('<p>ซึ่งธรรมชาติของข้อมูลในองค์กรนั้นแตกต่างกัน แม้จะมีข้อมูลมาก '
     'แต่ก็ไม่มากขนาดข้อมูลสาธารณะที่มีในโลกอินเตอร์เน็ต<br><br>ดังนั้นการเพิ่มเติม',
     '<p>การออกแบบและสร้างโครงสร้างข้อมูลที่เป็นมิตรกับ AI เพื่อให้ AI '
     'ใช้เป็นแกนในการเดินทางค้นหาข้อมูลขององค์กรที่อยู่ในกล่องต่างๆ และทำให้ AI '
     'เดินตามความสัมพันธ์ (relationship) ระหว่างความรู้ต่างๆ ที่แตกต่างกันตามภารกิจ (Mission) '
     'ขององค์กร<br><br>ดังนั้นการเพิ่มเติม'),
    ('ว่ามาจากกล่องความรู้กล่องใดบ้างขององค์กร จึงเป็นสิ่งสำคัญ</p>',
     'ว่ามาจากกล่องความรู้กล่องใดบ้างขององค์กร จึงเป็นการกลัดกระดุมเม็ดแรกที่สำคัญ</p>'),

    # 10 ย่อหน้า Neo Gens
    ('Neo Gens ทำงานอยู่ตรงเส้นทางระหว่างกล่องนี้ ด้วย mission-driven ontology และ '
     'knowledge graph โครงสร้างที่เก็บทั้งสิ่งที่องค์กรรู้ และรู้มาได้อย่างไร',
     'Neo Gens ทำงานอยู่บนเส้นทางการเชื่อมต่อความรู้ระหว่างกล่องนี้ ด้วย mission-driven ontology '
     'และ knowledge graph เพื่อออกแบบและสร้างโครงสร้างความรู้ขององค์กรในรูปแบบที่มนุษย์และ AI '
     'เข้าใจตรงกัน'),

    # 11 ตัดย่อหน้าปิดเดิม แล้วเปลี่ยนสามบรรทัดปิด
    ('    <div class="pb-d" style="margin-top:20px">แต่ความเป็นระเบียบไม่ใช่ปลายทาง '
     'คลังที่จัดไว้สวยงามแต่ไม่มีใครหยิบไปใช้ ก็ยังเป็นต้นทุน ไม่ใช่สินทรัพย์ '
     'งานของเราคือเปลี่ยนความรู้ที่องค์กรมีอยู่ ให้กลายเป็นสินทรัพย์ที่เอาไปสร้างมูลค่าต่อได้จริง '
     'ตอบคำถามที่เมื่อก่อนตอบไม่ได้ เปิดบริการที่เมื่อก่อนไม่มีคนพอจะทำ ลดงานที่ต้องทำซ้ำใหม่ทุกรอบ '
     'และทำให้คนรุ่นถัดไปเริ่มงานจากจุดที่คนรุ่นก่อนวางไว้ ไม่ใช่เริ่มนับหนึ่ง</div>\n', ''),
    ('<div class="pb-d" style="margin-top:30px;color:var(--fg)">ความรู้ที่ไม่มีใครใช้ '
     'ไม่ใช่สินทรัพย์</div>',
     '<div class="pb-d" style="margin-top:30px;color:var(--fg)">ความรู้ที่ไม่มีใครใช้ได้ '
     'ไม่ใช่สินทรัพย์ (Assets) แต่เป็นภาระ (Liabilities)</div>'),
    ('<div class="pb-t" style="margin-top:10px;margin-bottom:10px">เปลี่ยนความรู้ให้เป็นสินทรัพย์'
     'ที่สร้างมูลค่า</div>',
     '<div class="pb-t" style="margin-top:10px;margin-bottom:10px">เราช่วยเปลี่ยนความรู้'
     'ให้เป็นสินทรัพย์ที่สร้างคุณค่าให้กับองค์กร</div>'),
]

# ---------------------------------------------------------------- ภาษาอังกฤษ
# เขียนสำนวนเอง ไม่ได้แปล โครงและลำดับเดียวกับฝั่งไทย
EN = [
    ('<h1 class="motto" id="ng-h1">The better AI gets, <em>the more your own knowledge '
     'is worth</em>.</h1>',
     '<h1 class="motto" id="ng-h1">The smarter AI gets, <em>the more your own knowledge '
     'is worth</em>.</h1>'),

    ('<p class="hero-sub" id="ng-sub">When public knowledge becomes equally available to '
     'everyone, what still makes a difference is the knowledge held only inside your '
     'organisation.<br>Research documents that cost a great deal to produce, market data, '
     'records of customer interviews, the production steps behind your cost advantage, and '
     'the knowledge carried by staff who have accumulated it over decades. All of it is '
     'locked inside the organisation. No public AI can reach it.</p>',

     '<p class="hero-sub" id="ng-sub">Once public knowledge is equally available to everyone, '
     'the only asset that still buys you an advantage is the knowledge held nowhere but '
     'inside your own organisation.</p>\n'
     '    <ul class="hero-list">\n'
     '      <li><b>Research &amp; insights</b> the studies and market intelligence you pay '
     'for again every year</li>\n'
     '      <li><b>Operational know-how</b> the production steps and cost decisions you '
     'would never publish</li>\n'
     '      <li><b>Human experience</b> the judgement your people have built up over decades '
     'on the job</li>\n'
     '    </ul>\n'
     '    <p class="hero-sub">All of it is locked inside the organisation, where no public AI '
     'can reach it — and often the IT systems you have already paid for cannot get it out '
     'and put it to work either.</p>'),

    ('<b>Let an AI answer in your name and one wrong answer shakes public trust in the '
     'organisation. Field none at all, and the question becomes why the organisation everyone '
     'expects to lead on knowledge has not moved.</b>',
     '<b>One wrong answer in your name is enough to shake the trust people place in the '
     'organisation. Field no AI at all, and the question becomes how long you can stay in the '
     'race.</b>'),

    ('<div class="pb-d">Every organisation is about to put AI to work. The question that '
     'decides the outcome is not which model you choose. It is what that model is standing '
     'on.</div>',
     '<div class="pb-d">Picture everything your organisation knows as kept in boxes, and every '
     'organisation has a great many of them. The question worth asking before you put AI to '
     'work is this: can it read every box, and can you check which box each answer came out '
     'of, and whether that answer is right?</div>'),

    ('<div class="dlab go">EVERY BOX FULL · NOTHING RUNNING BETWEEN THEM</div>',
     '<div class="dlab go">EVERY BOX FULL OF KNOWLEDGE · NOTHING CONNECTING THEM</div>'),

    ('<b>Illustrative.</b> The knowledge is all there, in boxes, and none of it was designed '
     'to connect. Everything the organisation needs to answer well is in the room, and no '
     'route runs through it.',
     '<b>Illustrative.</b> The knowledge is all there, in the boxes, and no box was designed '
     'to connect to the next. Everything the organisation needs in order to answer well is '
     'already in those boxes. What is missing is a route between them for an AI to follow.'),

    ('The more data the AI has seen, the more accurate its guess at the next word becomes.',
     'The more data the AI has seen, the more accurate its guess at the next word becomes. '
     'That serves well enough for everyday work, and carries far too much risk for work the '
     'business depends on.'),

    ('<h3>One shared path through the knowledge</h3>',
     '<h3>A knowledge path an AI can follow</h3>'),

    ('Knowledge inside an organisation behaves differently. There may be a great deal of it, '
     'but never on the scale of the public data on the internet.<br><br>So it matters to add',
     'The work is to design a structure over your data that an AI can travel: a spine it '
     'follows from box to box, along the relationships between one piece of knowledge and the '
     'next, as your mission defines them.<br><br>So it matters to add'),

    ('and which of the organisation’s boxes it came out of.</p>',
     'and which of the organisation’s boxes it came out of. That is the first button done up '
     'straight, and everything after it depends on getting it right.</p>'),

    ('Neo Gens works on what runs between those boxes, with a mission-driven ontology and '
     'knowledge graph: a structure that holds both what your organisation knows and how it '
     'came to know it.',
     'Neo Gens works on the route between those boxes, with a mission-driven ontology and '
     'knowledge graph: we design and build your organisation’s knowledge structure in a form '
     'that people and AI read the same way.'),
]

EN_DROP = [
    ('    <div class="pb-d" style="margin-top:20px">Order is not the destination. A well-kept '
     'archive nobody draws on is still a cost, not an asset. Our work is to turn what your '
     'organisation already knows into an asset it can put to work — answering the enquiries '
     'that used to go unanswered, opening services you never had the people to run, cutting '
     'the work that gets redone every time, and letting the next generation start where the '
     'last one finished.</div>\n', ''),
    ('<div class="pb-d" style="margin-top:30px;color:var(--fg)">Knowledge nobody uses is not '
     'an asset.</div>',
     '<div class="pb-d" style="margin-top:30px;color:var(--fg)">Knowledge nobody can use is '
     'not an asset. It is a liability.</div>'),
    # บรรทัดสุดท้ายฝั่งอังกฤษไม่แตะ  Turn knowledge into value-creating assets เป็นวลีประจำ
    # ของบริษัท อยู่ใน footer ทุกหน้าอยู่แล้ว ฝั่งไทยใช้วลีนี้เป็นบรรทัดที่สาม ฝั่งอังกฤษใช้เป็นบรรทัดที่สอง
    # จบเท่ากันโดยไม่ต้องพูดซ้ำสองรอบในภาษาเดียวกัน
]


def patch(path, jobs, label):
    p = ROOT / path
    s = before = p.read_text(encoding="utf-8")
    done = skipped = 0
    problems = []
    for old, new in jobs:
        if new and new in s:
            skipped += 1
            continue
        if not new and old not in s:
            skipped += 1
            continue
        n = s.count(old)
        if n != 1:
            problems.append(f"{path}: จุดยึดเจอ {n} ครั้ง · {old[:70]}")
            continue
        s = s.replace(old, new, 1)
        done += 1
    if problems:
        return problems
    if s != before:
        p.write_text(s, encoding="utf-8")
    print(f"  {label} · แก้ {done} จุด · ข้าม {skipped} จุด")
    return []


def add_css(path, css, anchor_last_style_in_head=True):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    if ".hero-list{" in s:
        print(f"  CSS มีอยู่แล้วใน {path}")
        return []
    if path.endswith(".css"):
        s = s.rstrip() + "\n" + css
    else:
        head_end = s.index("</head>")
        i = s.rindex("</style>", 0, head_end)
        s = s[:i] + css + s[i:]
    p.write_text(s, encoding="utf-8")
    print(f"  เติม CSS ลง {path}")
    return []


problems = []
print("ภาษาไทย")
problems += patch("th-index.html", TH, "th-index.html")
problems += add_css("assets/site.th.css", CSS_TH)
print("ภาษาอังกฤษ")
problems += patch("index.html", EN + EN_DROP, "index.html")
problems += add_css("index.html", CSS_EN)

if problems:
    sys.exit("ไม่ผ่าน\n" + "\n".join(problems))

# ---------------------------------------------------------------- ด่านตรวจ
# ทุกชุดมีทั้งข้อ *มีครบ* และข้อ *ไม่เหลือ* ตามข้อ 10 ของ LESSONS.md
th = (ROOT / "th-index.html").read_text(encoding="utf-8")
en = (ROOT / "index.html").read_text(encoding="utf-8")
css_th = (ROOT / "assets" / "site.th.css").read_text(encoding="utf-8")

checks = {
    # มีครบ — ไทย
    "ไทย พาดหัวใหม่": "ยิ่ง AI ฉลาดขึ้น" in th,
    "ไทย ประโยคนำใหม่": "สินทรัพย์เดียวที่จะสร้างความได้เปรียบแข่งขันอย่างแท้จริง" in th,
    "ไทย รายการสามข้อครบ": th.count('<li><b>') == 3 and '<ul class="hero-list">' in th,
    "ไทย ย่อหน้าขุมทรัพย์": "ขุมทรัพย์ความรู้เหล่านี้ถูกล็อคอยู่ภายในองค์กร" in th,
    "ไทย ย่อหน้าความเสี่ยงใหม่": "เราจะสามารถแข่งขันในธุรกิจไปได้อีกนานแค่ไหน" in th,
    "ไทย ชุดคำถามภาพใหญ่": "และคำตอบนั้นถูกต้องหรือไม่ ?" in th,
    "ไทย ป้ายในภาพใหม่": "ทุกกล่องเต็มไปด้วยความรู้" in th,
    "ไทย การ์ด 02 เติมท้ายแล้ว": "มีความเสี่ยงสูงเกินไป" in th,
    "ไทย การ์ด 04 หัวข้อใหม่": "โครงเส้นทางความรู้ที่เป็นมิตรกับ AI" in th,
    "ไทย กลัดกระดุมเม็ดแรก": "จึงเป็นการกลัดกระดุมเม็ดแรกที่สำคัญ" in th,
    "ไทย บรรทัดปิดใหม่": "แต่เป็นภาระ (Liabilities)" in th,
    # ไม่เหลือ — ไทย
    "ไทย ไม่เหลือพาดหัวเก่า": "ยิ่ง AI ตอบได้ทุกเรื่อง" not in th,
    "ไทย ไม่เหลือย่อหน้า 04 เดิม": "ไม่มากขนาดข้อมูลสาธารณะที่มีในโลกอินเตอร์เน็ต" not in th,
    "ไทย ไม่เหลือย่อหน้าปิดเดิม": "แต่ความเป็นระเบียบไม่ใช่ปลายทาง" not in th,
    "ไทย ไม่เหลือ แต่ก็ หน้าการ์ด 03": "แต่ก็มีบางครั้งที่เราพบว่า" not in th,
    "ไทย คงตัวสะกด ล็อค ไม่ใช่ ล็อก": "ล็อก" not in th and th.count("ล็อค") >= 2,
    # มีครบ — อังกฤษ
    "อังกฤษ พาดหัวใหม่": "The smarter AI gets" in en,
    "อังกฤษ รายการสามข้อครบ": en.count("<li><b>") == 3 and '<ul class="hero-list">' in en,
    "อังกฤษ ย่อหน้า locked": "no public AI can reach it" in en,
    "อังกฤษ ชุดคำถามภาพใหญ่": "can it read every box" in en,
    "อังกฤษ การ์ด 04 หัวข้อใหม่": "A knowledge path an AI can follow" in en,
    "อังกฤษ first button": "first button done up straight" in en,
    "อังกฤษ บรรทัดปิดใหม่": "It is a liability." in en,
    # ไม่เหลือ — อังกฤษ
    "อังกฤษ ไม่เหลือพาดหัวเก่า": "The better AI gets" not in en,
    "อังกฤษ ไม่เหลือย่อหน้าปิดเดิม": "Order is not the destination" not in en,
    "อังกฤษ ไม่เหลือหัวข้อ 04 เดิม": "One shared path through the knowledge" not in en,
    # CSS
    "CSS ไทยอยู่ในไฟล์ร่วม": ".hero-list{" in css_th,
    "CSS อังกฤษฝังในหน้า": ".hero-list{" in en and en.index(".hero-list{") < en.index("</head>"),
    "CSS ไทยไม่มี letter-spacing ติดลบ": not re.search(
        r"\.hero-list[^}]*letter-spacing:\s*-", css_th),
    "CSS ไทย line-height อยู่ในช่วง": "line-height:1.85" in css_th,
}
bad = [k for k, ok in checks.items() if not ok]
if bad:
    sys.exit("[abort] " + " · ".join(bad))
print(f"✓ ตรวจผ่าน {len(checks)} ข้อ")
