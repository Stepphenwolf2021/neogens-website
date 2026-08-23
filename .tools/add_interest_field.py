#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เพิ่มช่อง "ข้อมูลที่คุณอยากรู้" ลงฟอร์มหน้าภาค MKM for Coffee และเอาแถบ GET IN TOUCH ออก

สั่งโดย Noppadol เมื่อ 2026-08-23  ให้หน้าในภาคกาแฟเหลือทางติดต่อทางเดียวคือฟอร์ม

แตะเฉพาะสิบหน้าในภาคกาแฟ  privacy กับ seo-as-knowledge-management ใช้ฟอร์มหน้าตาเดียวกัน
เพราะสร้างจากแม่แบบเดียวกัน แต่ไม่ได้อยู่ในภาคนี้ จึงไม่แตะ

ข้อความไทยเป็นคำของ Noppadol เอง วางลงไปตรง ๆ ห้ามเกลา  ดูข้อ 3 ของ LESSONS.md
ตัด <section class="cta"> ด้วยการไล่นับแท็ก ไม่ใช่ regex non-greedy  ดูข้อ 11

รันจากรากรีโป:  python3 .tools/add_interest_field.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = ["mkm-for-coffee.html", "mkm-for-coffee-why-now.html", "mkm-for-coffee-commons.html",
         "coffee-farmer.html", "coffee-demo.html"]
PAGES += ["th-" + p for p in PAGES]

LABEL = {"en": "What you would like to learn from the vault",
         "th": "ข้อมูลที่คุณอยากรู้จาก Coffee Knowledge Vault"}

HONEYPOT = '<input type="text" name="website" id="website"'

# ── CSS ของกล่องหลายบรรทัด ───────────────────────────────────────────────
# ยึดค่าจาก form input ที่มีอยู่แล้วทุกตัว ต่างแค่มุมโค้งกับความสูง เพราะเป็นกล่องไม่ใช่แคปซูล
# line-height 1.75 ตามกฎภาษาไทยใน CLAUDE.md  และไม่มี letter-spacing ติดลบ
CSS = """
/* >>> ช่องข้อมูลที่อยากรู้ · add_interest_field.py >>> */
form textarea{width:100%;background:var(--surface);border:1px solid var(--line-2);
  border-radius:18px;outline:none;color:var(--fg);font-family:var(--sans);font-size:15px;
  line-height:1.75;padding:13px 20px;min-height:98px;resize:vertical;
  display:block;transition:border-color .22s}
form textarea::placeholder{color:var(--mute)}
form textarea:focus{border-color:rgba(var(--go-rgb),.5)}
/* <<< ช่องข้อมูลที่อยากรู้ <<< */
"""


def field(lang):
    return ('<div class="frow"><div class="ffield">'
            f'<label class="flab" for="interest">{LABEL[lang]}</label>'
            '<textarea id="interest" rows="3" maxlength="600"></textarea>'
            '</div></div>\n        ')


def drop_cta(s, name):
    """ตัด <section class="cta"> ทั้งก้อนด้วยการไล่นับแท็ก section"""
    i = s.find('<section class="cta">')
    if i < 0:
        return s, False
    depth, j = 0, i
    while j < len(s):
        if s.startswith("<section", j):
            depth += 1
        elif s.startswith("</section>", j):
            depth -= 1
            if depth == 0:
                j += len("</section>")
                break
        j += 1
    else:
        sys.exit(f"✗ {name} หา </section> ปิดของแถบ GET IN TOUCH ไม่เจอ")
    end = j
    while end < len(s) and s[end] in " \n\t":      # เก็บช่องว่างท้ายไปด้วย ไม่ให้เหลือบรรทัดเปล่า
        end += 1
    return s[:i] + s[end:], True


changed, fail = [], []
for name in PAGES:
    p = ROOT / name
    if not p.exists():
        fail.append(f"{name} ไม่มีไฟล์นี้")
        continue
    lang = "th" if name.startswith("th-") else "en"
    s = before = p.read_text(encoding="utf-8")

    # 1 · ช่องใหม่ วางก่อน honeypot จึงอยู่ท้ายสุดของช่องที่คนเห็น
    if 'id="interest"' not in s:
        if s.count(HONEYPOT) != 1:
            fail.append(f"{name} หา honeypot ไม่เจอหรือเจอเกินหนึ่งจุด")
            continue
        s = s.replace(HONEYPOT, field(lang) + HONEYPOT, 1)

    # 2 · CSS  ยึดกับ </style> ซึ่งมีจริงแน่นอน ไม่ใช่คลาสที่บังเอิญนึกออก  ข้อ 9
    if "form textarea{" not in s:
        if s.count("</style>") != 1:
            fail.append(f"{name} มี </style> ไม่ใช่หนึ่งก้อน")
            continue
        s = s.replace("</style>", CSS + "</style>", 1)

    # 3 · ส่งค่าไปกับ payload  ไม่งั้น worker ไม่มีทางเห็น
    anchor = "originCountry:(document.getElementById('country')||{}).value||'',"
    if "interest:(document.getElementById" not in s:
        if s.count(anchor) != 1:
            fail.append(f"{name} หาจุดต่อ payload ไม่เจอ")
            continue
        s = s.replace(anchor, anchor + "\ninterest:(document.getElementById('interest')||{}).value||'',", 1)

    # 4 · เอาแถบ GET IN TOUCH ออก
    s, _ = drop_cta(s, name)

    if s != before:
        p.write_text(s, encoding="utf-8")
        changed.append(name)

# ── ด่านตรวจ · มีทั้งข้อ "มีครบ" และข้อ "ไม่เหลือ"  ข้อ 10 ───────────────
checks = {}
for name in PAGES:
    s = (ROOT / name).read_text(encoding="utf-8")
    lang = "th" if name.startswith("th-") else "en"
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", s, re.S))
    checks[f"{name} · มีช่อง interest หนึ่งช่อง"] = s.count('id="interest"') == 1
    checks[f"{name} · ป้ายช่องเป็นภาษาถูก"] = LABEL[lang] in s
    checks[f"{name} · ช่องอยู่ในฟอร์ม"] = '<textarea id="interest"' in re.search(r"<form\b.*?</form>", s, re.S).group(0)
    checks[f"{name} · payload ส่ง interest"] = "interest:(document.getElementById('interest')" in s
    checks[f"{name} · มีกฎ CSS ของ textarea"] = "form textarea{" in css
    checks[f"{name} · ไม่เหลือแถบ GET IN TOUCH"] = '<section class="cta">' not in s
    checks[f"{name} · ไม่เหลือปุ่ม Request a briefing ในเนื้อหน้า"] = \
        s.count('class="btn" href="contact.html"') <= 2      # เหลือได้เฉพาะในเมนูบนกับเมนูสไลด์
    checks[f"{name} · ปีกกา CSS สมดุล"] = css.count("{") == css.count("}")
    checks[f"{name} · แท็ก section สมดุล"] = s.count("<section") == s.count("</section>")
    checks[f"{name} · แท็ก div สมดุล"] = s.count("<div") == s.count("</div>")

# หน้าที่ห้ามโดนหางเลข
for name in ["privacy.html", "seo-as-knowledge-management.html", "index.html", "contact.html"]:
    s = (ROOT / name).read_text(encoding="utf-8")
    checks[f"{name} · ไม่โดนแตะ (ยังไม่มี interest)"] = 'id="interest"' not in s

bad = [k for k, ok in checks.items() if not ok]
print(f"แก้ {len(changed)} หน้า · ด่านตรวจ {len(checks)} ข้อ · ไม่ผ่าน {len(bad)}")
for b in bad[:12]:
    print("  ✗", b)
for f in fail:
    print("  !!", f)
if bad or fail:
    sys.exit(1)
print("✓ ผ่านทั้งหมด")
