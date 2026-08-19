#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างหน้าสำหรับคนปลูกกาแฟโดยเฉพาะ · coffee-farmer.html + th-coffee-farmer.html

ที่มา — บทความกาแฟฉบับเต็มอ่าน 13 นาที เขียนไว้ดีสำหรับโรงคั่ว ผู้ส่งออก
นักวิจัย และผู้ให้ทุน แต่คนที่ต้องกดส่งข้อมูลชุดแรกเข้ามาคือเกษตรกร
และเกษตรกรอ่านไม่จบ หน้านี้จึงสั้น ตอบเฉพาะคำถามที่คนปลูกถามจริง
แล้วค่อยส่งต่อไปหน้าเต็มสำหรับคนที่อยากอ่านเบื้องหลัง

ใช้ th-coffee.html กับ coffee.html เป็นแม่แบบ จึงได้ nav ธีม ฟอร์ม และ CSS
ชุดเดียวกันทั้งหมด ไม่มีคลาสใหม่แม้แต่ตัวเดียว ตามบทเรียนข้อ 8

รันจากรากรีโป:  python3 .tools/build_farmer_page.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- ส่วนหัวหน้า

HEAD = {
    "th": dict(
        title="สำหรับคนปลูกกาแฟ — Neo Gens",
        ogtitle="สำหรับคนปลูกกาแฟ",
        desc="ทุกฤดูมีคนขึ้นมาเก็บข้อมูลแปลงคุณ แล้วไม่มีอะไรกลับมาถึงคุณ "
             "หน้านี้อธิบายสั้น ๆ ว่าคุณต้องทำอะไร ได้อะไรกลับ และข้อมูลของคุณอยู่กับใคร",
        kicker="MKM สำหรับกาแฟ · สำหรับคนปลูก",
        h1="ความรู้ที่อยู่ในหัวคุณ หายไปพร้อมกับทุกฤดูที่ผ่านไป",
        stand="ทุกปีมีคนขึ้นมาวัดแปลง ถ่ายรูป จดสายพันธุ์ แล้วก็ไม่มีอะไรกลับมาถึงคุณ "
              "เรากำลังสร้างคลังความรู้กาแฟที่คนปลูกได้ของกลับด้วย และอยากชวนคุณมาเป็นกลุ่มแรก",
        meta="อ่าน 3 นาที",
    ),
    "en": dict(
        title="For coffee farmers — Neo Gens",
        ogtitle="For coffee farmers",
        desc="Every season someone comes to record your plot, and nothing comes back to "
             "you. This page explains in short what you would do, what you get back, and "
             "who holds your data.",
        kicker="MKM for Coffee · for growers",
        h1="What you know about your own plot leaves with every season",
        stand="Every year someone measures the plot, takes the photographs, notes the "
              "varieties — and nothing comes back to you. We are building a coffee "
              "knowledge vault where the grower gets something back, and we are looking "
              "for the first group to build it with.",
        meta="3 min read",
    ),
}

# ---------------------------------------------------------------- เนื้อหา

BODY = {
    "th": """
<h2 id="s01"><span class="sn">01</span>คุณต้องทำอะไรบ้าง</h2>
<p class="first">สั้นที่สุดคือ เล่าสิ่งที่ทำอยู่แล้วในแต่ละวัน ด้วยเครื่องมือที่มีอยู่แล้วในมือ ไม่มีแอปใหม่ให้โหลด ไม่มีฟอร์มสี่สิบช่อง</p>
<div class="pcards three rv">
  <div class="pc"><h4>ส่งด้วยของที่ถนัด</h4><p>ถ่ายรูปลานตากตอนบ่าย อัดเสียงเล่าว่าวันนี้หมักกี่ชั่วโมง ถ่ายคลิปสั้นตอนกลับกอง หรือพิมพ์ประโยคเดียวก็ได้ ส่งผ่านแอปแชตที่คุณใช้อยู่ทุกวัน</p></div>
  <div class="pc"><h4>ระบบเป็นฝ่ายจัดให้</h4><p>สิ่งที่คุณส่งมาถูกแปลงเป็นข้อมูลที่ใช้ต่อได้ ถ้าระบบไม่แน่ใจ มันถามกลับสั้น ๆ ทีละคำถาม ไม่เดาเงียบ ๆ และเก็บคำพูดจริงของคุณไว้ก่อนเสมอ</p></div>
  <div class="pc"><h4>ไม่มีตารางบังคับ</h4><p>ส่งเมื่อมีอะไรจะเล่า ฤดูไหนยุ่งก็เว้นไว้ได้ ที่จุดรวบรวมของสหกรณ์ เครื่องวัดส่งค่าเข้ามาเองอยู่แล้ว โดยคุณไม่ต้องทำอะไรเพิ่ม</p></div>
</div>
<p class="beat">คนปลูกกาแฟไม่ควรต้องกลายเป็นคนกรอกข้อมูล เพื่อให้ความรู้ของตัวเองอยู่ในระบบ</p>

<h2 id="s02"><span class="sn">02</span>แล้วคุณได้อะไรกลับ</h2>
<h3>เทียบกับแปลงที่คล้ายกับของคุณ</h3>
<p>แปลงที่ความสูงใกล้กัน ดินคล้ายกัน สายพันธุ์เดียวกัน เขาหมักกี่ชั่วโมง ตากกี่วัน แล้วคะแนนออกมาเท่าไร วันนี้ต้องรู้จักกันเป็นการส่วนตัวถึงจะถามได้ ต่อไปเปิดดูได้ นี่คือสิ่งที่เกษตรกรรายย่อยหาไม่ได้เลยในวันนี้</p>
<h3>ประวัติของแปลงคุณ ที่มีหลักฐานรองรับ</h3>
<p>สิ่งที่คุณทำในแต่ละฤดูถูกบันทึกไว้พร้อมที่มา เวลาคุยราคากับผู้ซื้อ คุณมีของให้ดู ไม่ใช่มีแต่คำพูด และคุณภาพที่ดีขึ้นข้ามฤดูก็แสดงให้เห็นได้</p>
<h3>คนปลายทางตามกลับมาถึงคุณได้</h3>
<p>ถ้าคุณอนุญาต คนที่ซื้อกาแฟถุงนั้นตามกลับมาถึงแปลงและถึงชื่อคุณได้จริง ไม่ใช่แค่ชื่อจังหวัดบนถุง</p>
<p>และยิ่งมีคนเข้ามาร่วมมากขึ้น ของที่คุณมีก็ยิ่งมีค่ามากขึ้น เพราะการเทียบทุกครั้งจะแม่นขึ้นตามจำนวนแปลงในคลัง</p>

<h2 id="s03"><span class="sn">03</span>คำถามที่ควรถามก่อนตัดสินใจ</h2>
<h3>ต้องจ่ายเท่าไร</h3>
<p>เกษตรกรไม่มีค่าใช้จ่าย รายได้ของโครงการมาจากฝ่ายอื่นในสายโซ่ที่เอาความรู้ชุดนี้ไปใช้ทำงาน ไม่ได้มาจากคนปลูก</p>
<h3>ข้อมูลแปลงผมเป็นของใคร</h3>
<p>เป็นของคุณ คุณเลือกได้ว่าจะให้ใครเห็น ให้สิทธิ์ผู้ซื้อที่คุณเลือกเองได้ และถอนคืนจากคนที่คุณไม่เลือกได้ ไม่มีใครเปิดข้อมูลของคุณให้คนอื่นโดยที่คุณไม่ได้อนุญาต</p>
<h3>ปีที่กาแฟไม่ดี จะอยู่ในนั้นด้วยไหม</h3>
<p>สิ่งที่คุณส่งเข้ามา คุณเป็นคนกำหนดว่าใครเห็นได้ กติกาข้อนี้เขียนไว้ตั้งแต่ต้น ไม่ใช่มาเพิ่มทีหลัง</p>
<h3>ไม่ถนัดพิมพ์ ทำได้ไหม</h3>
<p>ได้ ถ่ายรูปหรืออัดเสียงด้วยภาษาที่คุณพูดทุกวัน รวมทั้งภาษาถิ่น ระบบเป็นฝ่ายแปลง ไม่ใช่คุณ</p>
<h3>ทิ้งอีเมลไว้แล้วเจออะไรต่อ</h3>
<p>เราติดต่อกลับ แล้วชวนคุณเข้าร่วมทดลองระบบเป็นกลุ่มแรก ๆ ระหว่างนั้นเราอยากฟังด้วยว่าเราเข้าใจอะไรผิดเกี่ยวกับวิธีที่กาแฟทำงานจริงในพื้นที่ของคุณ</p>

<h2 id="s04"><span class="sn">04</span>ทำไมต้องเป็นของสาธารณะ</h2>
<p>คลังนี้เป็น public goods หรือของสาธารณะ แบบเดียวกับถนนหรือระบบชลประทาน คือสิ่งที่ทุกคนใช้ได้และไม่มีใครเป็นเจ้าของคนเดียว</p>
<p>โครงสร้างของคลังเผยแพร่ทั้งหมด ใครจะเอาไปทำระบบของตัวเองหรือเถียงกับมันก็ได้ ข้อมูลของคุณยังเป็นของคุณ พกไปได้ ถอนได้ และทุกข้อเท็จจริงในคลังพกที่มาติดตัวเสมอ ว่าใครเป็นคนบอก และมีหลักฐานอะไรหนุนอยู่</p>
<p>Neo Gens ลงทุนและดูแลงานนี้ แต่ไม่ได้เป็นเจ้าของความรู้ที่อยู่ในนั้น เพราะคลังที่บริษัทเดียวเป็นเจ้าของ ก็เป็นแค่ฐานข้อมูลที่การตลาดดีขึ้น และไม่ควรมีใครเอาข้อมูลของตัวเองไปไว้</p>
<p class="colophon">อยากอ่านเบื้องหลังทั้งหมด ว่าทำไมวงการกาแฟต้องมีคลังความรู้ร่วม และแต่ละฝ่ายในสายโซ่ได้อะไรกลับไป — <a href="th-mkm-for-coffee.html">อ่านฉบับเต็ม</a></p>
""",
    "en": """
<h2 id="s01"><span class="sn">01</span>What you would actually do</h2>
<p class="first">The short version: tell us what you already do, using what is already in your hand. No new app to install, no form with forty fields.</p>
<div class="pcards three rv">
  <div class="pc"><h4>Send it however suits you</h4><p>Photograph the drying beds in the afternoon. Record a voice note saying how long the ferment ran. Take a short clip while turning the pile. Or type one sentence. It goes through the messaging app you already use every day.</p></div>
  <div class="pc"><h4>The system does the filing</h4><p>What you send gets turned into something the vault can use. When it isn't sure, it asks one short question back rather than guessing quietly — and your own words are always kept first.</p></div>
  <div class="pc"><h4>No schedule to keep</h4><p>Send something when there is something to say. Skip the weeks when the harvest is on. At the cooperative's collection point the meters already report their own readings, with nothing extra asked of you.</p></div>
</div>
<p class="beat">Nobody should have to become a data-entry clerk to get their own knowledge on the record.</p>

<h2 id="s02"><span class="sn">02</span>What you get back</h2>
<h3>A comparison with plots like yours</h3>
<p>Plots at a similar altitude, on similar soil, growing the same variety: how long they fermented, how long they dried, and what the cup scored. Today you have to know someone personally to ask. This is the one thing smallholders cannot get anywhere at present.</p>
<h3>A record of your plot, with the evidence attached</h3>
<p>What you did each season is written down with its source. When you talk price with a buyer, you have something to show rather than only something to say — and improvement across seasons becomes something you can demonstrate.</p>
<h3>The person at the other end can trace it back to you</h3>
<p>With your permission, whoever buys that bag can follow it back to the plot and to your name, instead of stopping at a province printed on the label.</p>
<p>And the more growers take part, the more your own contribution is worth, because every comparison gets sharper as the number of plots in the vault grows.</p>

<h2 id="s03"><span class="sn">03</span>Questions worth asking first</h2>
<h3>What does it cost</h3>
<p>Nothing for the farmer. The project earns from others along the chain who put this knowledge to work — not from the people growing the coffee.</p>
<h3>Who owns my plot data</h3>
<p>You do. You choose who sees it, you grant access to the buyers you choose, and you withdraw it from the ones you don't. Nobody opens your data to anyone else without your say-so.</p>
<h3>What about a bad year</h3>
<p>Whatever you send, you decide who can see it. That rule was written at the start, not added later.</p>
<h3>I'm not comfortable typing</h3>
<p>Then don't. Photograph it, or speak it in the language you use every day, dialect included. The translating is the system's job, not yours.</p>
<h3>What happens after I leave my email</h3>
<p>We get in touch, and invite you into the first group testing the system. While we're at it we want to hear what we have got wrong about how coffee actually works where you are.</p>

<h2 id="s04"><span class="sn">04</span>Why it has to be public</h2>
<p>This vault is a public good — like a road or an irrigation system. Everyone can use it and no single party owns it.</p>
<p>The structure is published in full: anyone can build their own system on it or argue with it. Your data stays yours, portable and withdrawable. And every fact in the vault carries its own provenance — who said it, and what evidence stands behind it.</p>
<p>Neo Gens funds and stewards the work but does not own the knowledge inside it. A vault owned by one company is just a database with better marketing, and nobody should put their own data into one.</p>
<p class="colophon">If you want the full reasoning — why the coffee sector needs a shared knowledge vault, and what each party along the chain gets back — <a href="mkm-for-coffee.html">read the long version</a>.</p>
""",
}

JOIN = {
    "th": dict(k="ร่วมทดลองเป็นกลุ่มแรก",
               h2="ตอนนี้เรากำลังหาคนปลูกกลุ่มแรก",
               lead="ทิ้งชื่อกับอีเมลไว้ แล้วเราจะติดต่อกลับ ไม่มีค่าใช้จ่าย และไม่มีข้อผูกมัด"),
    "en": dict(k="Join the first group",
               h2="We are looking for the first growers",
               lead="Leave your name and email and we will get in touch. "
                    "No cost, and nothing to commit to."),
}


def build(lang):
    src_name = "th-mkm-for-coffee.html" if lang == "th" else "mkm-for-coffee.html"
    out_name = "th-coffee-farmer.html" if lang == "th" else "coffee-farmer.html"
    other = "coffee-farmer.html" if lang == "th" else "th-coffee-farmer.html"
    s = (ROOT / src_name).read_text(encoding="utf-8")
    h = HEAD[lang]

    # --- ส่วนหัวเอกสาร ---
    s = re.sub(r"<title>.*?</title>", f"<title>{h['title']}</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*"', r"\1" + h["desc"] + '"', s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*"', r"\1" + h["ogtitle"] + '"', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*"', r"\1" + h["desc"] + '"', s, count=1)
    s = s.replace(f"https://www.neogens.co/{src_name}", f"https://www.neogens.co/{out_name}")
    other_src = "mkm-for-coffee.html" if lang == "th" else "th-mkm-for-coffee.html"
    s = s.replace(f"https://www.neogens.co/{other_src}", f"https://www.neogens.co/{other}")

    # --- hero ---
    hero_old = re.search(r'<div class="kicker">.*?</div>\s*</div>\s*</header>', s, re.S)
    if not hero_old:
        sys.exit(f"[abort] {src_name}: หา hero ไม่เจอ")
    hero_new = (f'<div class="kicker">{h["kicker"]}</div>\n'
                f'      <h1>{h["h1"]}</h1>\n'
                f'      <p class="stand">{h["stand"]}</p>\n'
                f'      <div class="meta"><span>Neo Gens</span><span>{h["meta"]}</span></div>\n'
                f'    </div>\n  </div>\n</header>')
    s = s[:hero_old.start()] + hero_new + s[hero_old.end():]

    # --- ตัดแผนที่ coffee belt ออก หน้านี้ไม่ต้องการ ---
    m = re.search(r'<div class="wrap">\s*<figure class="figplate hero-map rv">.*?</figure>\s*</div>',
                  s, re.S)
    if m:
        s = s[:m.start()] + s[m.end():]

    # --- เนื้อหา ---
    i, j = s.index("<article>"), s.index("</article>") + len("</article>")
    s = (s[:i]
         + '<article>\n  <div class="wrap">\n    <div class="artbody">'
         + BODY[lang]
         + "    </div>\n  </div>\n</article>"
         + s[j:])

    # --- บล็อกชวนเข้าร่วม ---
    jn = JOIN[lang]
    s = re.sub(r'(<div class="k rv">)[^<]*(</div>)', r"\1" + jn["k"] + r"\2", s, count=1)
    s = re.sub(r'(<section class="join".*?<h2 class="rv">)[^<]*(</h2>)',
               r"\1" + jn["h2"] + r"\2", s, count=1, flags=re.S)
    s = re.sub(r'(<p class="lead rv">)[^<]*(</p>)', r"\1" + jn["lead"] + r"\2", s, count=1)

    (ROOT / out_name).write_text(s, encoding="utf-8")
    kb = len(s.encode()) // 1024
    print(f"  สร้าง {out_name} · {kb} KB")


def main():
    for lang in ("th", "en"):
        build(lang)
    print("เสร็จ · ต่อเมนูและ sitemap ด้วย regroup_nav.py")


if __name__ == "__main__":
    main()
