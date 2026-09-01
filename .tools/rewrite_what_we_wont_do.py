#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เขียนเนื้อหาหน้า สิ่งที่เราไม่ทำ ใหม่ ทั้งสองภาษา · 2026-09-01

ฉบับไทยเป็นคำของ Noppadol ยกมาตรงทุกตัวอักษร ห้ามเกลา
สิ่งเดียวที่ตัดคือช่องว่างท้ายบรรทัด ซึ่งมองไม่เห็นบนหน้าเว็บ
ฉบับอังกฤษเขียนสำนวนเอง เดินตามสาระเดียวกัน ไม่ได้แปลตรงตัว

โครงหน้าเดิมรับได้พอดี  eyebrow · h1 · lede · กล่อง .gap ห้ากล่อง
แต่ละกล่องมี .k เป็นป้าย แล้วหัวข้อ แล้วย่อหน้าเดียว

รันซ้ำได้  รันจากรากรีโป:  python3 .tools/rewrite_what_we_wont_do.py
"""
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TH = [
    # eyebrow · h1 · lede
    ('<div class="eyebrow rv">จุดที่เราพูดตรง ๆ กับคุณ</div>',
     '<div class="eyebrow rv">เพื่อความเข้าใจที่ตรงกัน</div>'),
    ('<h1>สิ่งนี้ไม่ใช่อะไร และมันขออะไรจากทีมของคุณ</h1>',
     '<h1>นี่คืองานที่ต้องร่วมมือกันอย่างจริงจัง</h1>'),
    ('<p class="lede">เรายอมเสียงานดีกว่าปล่อยให้คุณมารู้เรื่องนี้เอาตอนเดือนที่สี่</p>',
     '<p class="lede">ความสำเร็จของโครงการคือการที่ทีมสามารถขยายโครงการไปต่อได้ด้วยตัวเอง</p>'),
    # กล่อง 1
    ('<p>ไม่ใช่ค่าจ้างเรา แต่คือตารางเวลาของเขา ต้องมีผู้เชี่ยวชาญอาวุโสอยู่ในเวิร์กช็อป'
     'อย่างสม่ำเสมอ ถ้าจัดเวลานั้นไม่ได้ งานจะไม่แข็งแรงพอ และเราขอบอกกันตรงนี้ '
     'ดีกว่าไปรู้กันทีหลัง</p>',
     '<p>ไม่ใช่ค่าจ้างเรา แต่คือตารางเวลาของทีมงาน และต้องมีผู้เชี่ยวชาญอาวุโสอยู่ใน'
     'เวิร์กช็อปอย่างสม่ำเสมอ ถ้าจัดเวลานั้นไม่ได้ งานจะไม่แข็งแรงพอ</p>'),
    # กล่อง 2
    ('<div class="k">ไม่แทนที่งานวิชาการ</div>',
     '<div class="k">AI ไม่ได้ทำงานแทนที่งานวิชาการ</div>'),
    ('<h3 class="hkeep-2">มีเพียงผู้เชี่ยวชาญของคุณที่เลื่อนข้ออ้างขึ้นเป็นข้อเท็จจริงได้</h3>',
     '<h3 class="hkeep-2">มีเพียงผู้เชี่ยวชาญของคุณที่ตัดสินใจว่าอะไรคือข้อเท็จจริงได้ '
     'ไม่ใช่ AI</h3>'),
    # กล่อง 3
    ('<div class="k">ไม่ใช่ทางลัด</div>',
     '<div class="k">ไม่มีทางลัดที่ไม่มีความเสี่ยง</div>'),
    ('<p>ส่วนที่ยากคือการทำให้แต่ละแผนกตกลงกันเรื่องศัพท์ ที่ต่างฝ่ายต่างถือไว้เงียบๆ '
     'มาหลายสิบปี ไม่มีสินค้าไหนข้ามขั้นตอนนี้ได้</p>',
     '<p>ส่วนที่ยากคือการทำให้เกิดฉันทามติในเรื่องคำเรียกชื่อ คำศัพท์ต่าง ๆ '
     'ที่ต่างฝ่ายถือไว้เงียบ ๆ มาหลายสิบปี ไม่มีทางลัด เป็นโอกาสดีที่จะได้นำมาพูดกัน</p>'),
    # กล่อง 4
    ('<h4>เราไม่รับงานนี้ในรูปโครงการดิจิไทซ์ที่จ้างออกไปข้างนอก</h4>',
     '<h4>เราไม่รับงานนี้ในรูปโครงการดิจิไทซ์ที่จ้างออกไปทำข้างนอก</h4>'),
    ('และของแบบนั้นก็มักถูกทิ้งภายในปีเดียวอยู่ดี',
     'และงานแบบนั้นก็มักถูกทิ้งภายในปีเดียวอยู่ดี'),
    # กล่อง 5
    ('<div class="k">แคบโดยตั้งใจ</div>',
     '<div class="k">โครงการขนาดเล็กโดยตั้งใจ</div>'),
    # meta
    ('<title>สิ่งนี้ไม่ใช่อะไร และมันขออะไรจากทีมของคุณ — Neo Gens</title>',
     '<title>นี่คืองานที่ต้องร่วมมือกันอย่างจริงจัง — Neo Gens</title>'),
    ('<meta property="og:title" content="สิ่งนี้ไม่ใช่อะไร และมันขออะไรจากทีมของคุณ — Neo Gens">',
     '<meta property="og:title" content="นี่คืองานที่ต้องร่วมมือกันอย่างจริงจัง — Neo Gens">'),
    ('<meta name="description" content="เรายอมเสียงานดีกว่าปล่อยให้คุณมารู้เรื่องนี้เอาตอนเดือนที่สี่">',
     '<meta name="description" content="ความสำเร็จของโครงการคือการที่ทีมสามารถขยาย'
     'โครงการไปต่อได้ด้วยตัวเอง เวลาของผู้เชี่ยวชาญคุณคือต้นทุนจริงของงานนี้">'),
    ('<meta property="og:description" content="เรายอมเสียงานดีกว่าปล่อยให้คุณมารู้เรื่องนี้เอาตอนเดือนที่สี่">',
     '<meta property="og:description" content="ความสำเร็จของโครงการคือการที่ทีมสามารถขยาย'
     'โครงการไปต่อได้ด้วยตัวเอง เวลาของผู้เชี่ยวชาญคุณคือต้นทุนจริงของงานนี้">'),
]

EN = [
    ("<div class=\"eyebrow rv\">Where we're honest with you</div>",
     '<div class="eyebrow rv">So we start from the same page</div>'),
    ('<h1>What this is not, and what it asks of your team.</h1>',
     '<h1>This is work we do together, in earnest.</h1>'),
    ("<p class=\"lede\">We'd rather lose the engagement than have you discover this in month four.</p>",
     '<p class="lede">The engagement has succeeded when your own team can carry it '
     'further without us.</p>'),
    ('<p>Not our fees — their calendars. Expect senior curators, librarians and archivists '
     "in working sessions on a regular rhythm. If that time can't be committed, the work "
     'will not hold.</p>',
     "<p>Not our fees — your team's calendars. Expect senior specialists in working "
     "sessions on a regular rhythm. If that time can't be committed, the work will not "
     'hold.</p>'),
    ('<div class="k">Does not replace scholarship</div>',
     '<div class="k">AI does not replace scholarship</div>'),
    ('<h3 class="hkeep-2">Only your own specialists promote a claim to an established fact</h3>',
     '<h3 class="hkeep-2">Only your own specialists decide what counts as fact — not an AI</h3>'),
    ('<div class="k">Not a quick fix</div>',
     '<div class="k">No shortcut without risk</div>'),
    ('<p>The hard part is getting departments to agree on terminology they have each held '
     'privately for decades. No product shortcuts that.</p>',
     '<p>The hard part is reaching agreement on the names and terms each department has '
     'held quietly for decades. There is no shortcut, and it is a good chance to finally '
     'talk about it.</p>'),
    ("<h4>We won't run this as an outsourced digitisation project</h4>",
     "<h4>We won't take this on as an outsourced digitisation project</h4>"),
    ('and that deliverable tends to be abandoned within a year anyway.',
     'and work like that tends to be abandoned within a year anyway.'),
    ('<div class="k">Deliberately narrow</div>',
     '<div class="k">Small by design</div>'),
    ('<title>What this is not, and what it asks of your team. — Neo Gens</title>',
     '<title>This is work we do together, in earnest. — Neo Gens</title>'),
    ('<meta property="og:title" content="What this is not, and what it asks of your team. — Neo Gens">',
     '<meta property="og:title" content="This is work we do together, in earnest. — Neo Gens">'),
    ('<meta name="description" content="We&#x27;d rather lose the engagement than have you discover this in month four.">',
     '<meta name="description" content="The engagement has succeeded when your own team '
     'can carry it further without us. Your specialists’ time is the real cost.">'),
    ('<meta property="og:description" content="We&#x27;d rather lose the engagement than have you discover this in month four.">',
     '<meta property="og:description" content="The engagement has succeeded when your own team '
     'can carry it further without us. Your specialists’ time is the real cost.">'),
]

GONE_TH = ["เรายอมเสียงาน", "เดือนที่สี่", "ไม่มีสินค้าไหนข้ามขั้นตอนนี้ได้",
           "แคบโดยตั้งใจ", "สิ่งนี้ไม่ใช่อะไร"]
GONE_EN = ["month four", "No product shortcuts that", "Deliberately narrow",
           "What this is not"]

for fname, pairs, gone in [("th-what-we-wont-do.html", TH, GONE_TH),
                           ("what-we-wont-do.html", EN, GONE_EN)]:
    p = ROOT / fname
    s = io.open(p, encoding="utf-8").read()
    orig = s
    hits = 0
    for old, new in pairs:
        n = s.count(old)
        if n == 0:
            if new in s:                 # รันซ้ำ
                hits += 1
                continue
            sys.exit(f"✗ {fname} หาข้อความเดิมไม่เจอ: {old[:70]}")
        s = s.replace(old, new)
        hits += n

    # JSON-LD ถูกสร้างใหม่ด้วย build_jsonld.py ทีหลัง ข้อความเก่าในนั้นจึงไม่นับ
    # ป้าย .k มีในแถบก่อนหน้า-ถัดไปด้วย จึงต้องนับเฉพาะในเขต .gaps
    body = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', "", s)
    gaps = s[s.index('<div class="gaps">'):s.index("</section>")]
    checks = {
        "ข้อความใหม่เข้าครบ": all(new in s for _, new in pairs),
        "ข้อความเก่าไม่เหลือนอก JSON-LD": not any(g in body for g in gone),
        "กล่องยังครบห้ากล่อง": s.count('<div class="gap rv">') == 5,
        "ป้ายกล่องครบห้าอัน": gaps.count('<div class="k">') == 5,
        "h1 มีตัวเดียว": s.count("<h1") == 1,
        "แท็กสมดุล": s.count("<div") == s.count("</div>")
                     and len(re.findall(r"<p\b", s)) == s.count("</p>"),
        "ไม่มีเว้นวรรคซ้อนในเนื้อหา":
            "  " not in re.sub(r"\s*\n\s*", "\n",
                               s[s.index('<div class="gaps">'):s.index("</section>")]),
        "meta description ไม่เกิน 160": all(
            len(m) <= 160 for m in re.findall(
                r'<meta name="description" content="([^"]*)"', s)),
        "โครงหน้ายังครบ": all(x in s for x in ["</footer>", 'id="contact"', "<h1"]),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {fname} ไม่ผ่าน: " + " · ".join(bad))
    io.open(p, "w", encoding="utf-8").write(s)
    print(f"  เขียนใหม่ {fname:24} · แทนที่ {hits:2d} จุด · {len(s)-len(orig):+d} ตัวอักษร")

print("✓ สองภาษาเดินตามสาระเดียวกัน · ฉบับไทยเป็นคำของ Noppadol ไม่ได้เกลา")
print("  ต่อด้วย  python3 .tools/build_jsonld.py")
