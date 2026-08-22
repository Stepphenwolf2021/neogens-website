#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
เมนูย่อยแบบ dropdown บนแถบเมนูบน สำหรับจอกว้างกว่า 1300px   สั่งเมื่อ 2026-08-22

ปัญหาที่แก้ — โครงเว็บสามภาคมีอยู่ในเมนูสไลด์เท่านั้น แต่ปุ่มที่เปิดเมนูนั้น
โผล่เฉพาะจอแคบกว่า 1300px (ดู @media ใน CSS) จอกว้างกว่านั้นเห็นแค่ห้าลิงก์บนแถบบน
คนใช้เดสก์ท็อปจึงมองไม่เห็นว่าเว็บนี้มีอะไรอยู่ข้างในบ้าง ต้องเดาจากหน้าที่เปิดอยู่

**เมนูย่อยไม่ได้เขียนขึ้นใหม่ แต่อ่านจากเมนูสไลด์ในไฟล์เดียวกัน**
สองที่จึงตรงกันโดยโครงสร้าง ไม่ใช่โดยความตั้งใจของคนแก้ หลักเดียวกับ add_breadcrumbs.py
ที่ดึงเส้นทางจาก JSON-LD ของหน้านั้นเอง

กฎจับคู่ — รายการบนแถบบนได้เมนูย่อย ก็ต่อเมื่อมีกลุ่มในเมนูสไลด์ที่ **ลิงก์แรกของกลุ่ม**
ชี้ไปหน้าเดียวกัน ด้วยกฎนี้ Engagement จึงไม่ได้เมนูย่อย ทั้งที่ชื่อมันอยู่ในกลุ่มภาค 2
เพราะมันไม่ใช่หัวของกลุ่มไหน ไม่ต้องมีรายชื่อฮาร์ดโค้ดต่อภาษา

เปิดด้วยการชี้ค้าง และด้วย :focus-within เมื่อแท็บเข้าไป จึงไม่ต้องใช้ JS
มีสคริปต์บรรทัดเดียวในเปลือกเมนูไว้รับปุ่ม Escape อย่างเดียว
ตัวหัวข้อยังเป็นลิงก์ไปหน้าตัวเองได้เหมือนเดิม ไม่ได้กลายเป็นปุ่มเปล่า

ต่ำกว่า 1300px ไม่ต้องกันอะไรเพิ่ม เพราะ .nav-links{display:none!important} อยู่แล้ว

รันจากรากรีโป:  python3 .tools/add_nav_dropdown.py
สคริปต์เรียก sync_nav.py ต่อให้เอง ไม่ต้องจำว่าต้องรันอะไรตาม
"""
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / ".tools" / "shell"

MARK_A = "/* >>> เมนูย่อยบนแถบเมนูบน · add_nav_dropdown.py >>> */"
MARK_B = "/* <<< เมนูย่อยบนแถบเมนูบน <<< */"

ESC = ('<script>document.addEventListener("keydown",function(e){'
       'if(e.key==="Escape"&&document.activeElement&&document.activeElement.closest'
       '&&document.activeElement.closest(".hs"))document.activeElement.blur()});</script>')


def css(lang):
    """ไทยต้องการ line-height สูงกว่า และห้าม letter-spacing ติดลบ"""
    lh = "1.85" if lang == "th" else "1.6"
    fs = "13px" if lang == "th" else "13.5px"
    return f"""{MARK_A}
.nav-links .hs{{position:relative;display:inline-flex;align-items:center}}
.nav-links .hs>a{{display:inline-flex;align-items:center;gap:6px}}
.nav-links .hs>a::after{{content:"";width:5px;height:5px;border-right:1.4px solid currentColor;
  border-bottom:1.4px solid currentColor;transform:translateY(-2px) rotate(45deg);
  opacity:.5;transition:opacity .2s,transform .2s}}
.nav-links .hs:hover>a::after,.nav-links .hs:focus-within>a::after{{opacity:1;transform:translateY(1px) rotate(225deg)}}
.nav-links .sub{{position:absolute;top:100%;left:-16px;min-width:262px;max-width:340px;
  margin-top:14px;padding:9px 0;background:var(--surface);border:1px solid var(--line);
  border-radius:14px;box-shadow:0 16px 44px var(--shadow);display:flex;flex-direction:column;
  opacity:0;visibility:hidden;transform:translateY(-6px);
  transition:opacity .18s,transform .18s,visibility .18s;z-index:120}}
.nav-links .sub::before{{content:"";position:absolute;top:-16px;left:0;right:0;height:16px}}
.nav-links .hs:hover>.sub,.nav-links .hs:focus-within>.sub{{opacity:1;visibility:visible;transform:translateY(0)}}
.nav-links .sub a{{display:block;padding:7px 18px;font-size:{fs};line-height:{lh};
  color:var(--dim);white-space:normal;text-decoration:none;transition:color .18s,background .18s}}
.nav-links .sub a:hover,.nav-links .sub a:focus-visible{{color:var(--fg);background:var(--wash)}}
.nav-links .sub a.on{{color:var(--go)}}
@media(prefers-reduced-motion:reduce){{
  .nav-links .sub,.nav-links .hs>a::after{{transition:none}}
}}
{MARK_B}"""


def groups(drawer):
    """แตกเมนูสไลด์เป็นกลุ่ม คืน [(หน้าแรกของกลุ่ม, [(href, ป้าย), …]), …]"""
    out = []
    for chunk in drawer.split('<div class="h">')[1:]:
        body = chunk.split("</div>", 1)[1]
        links = [(h, t) for h, t in re.findall(r'<a href="([^"]+)">(.*?)</a>', body)]
        if links:
            out.append((links[0][0], links))
    return out


def build(lang):
    path = SHELL / f"nav.{lang}.html"
    nav = path.read_text(encoding="utf-8")

    # รันซ้ำได้ ถอดของเดิมออกก่อนเสมอ
    nav = re.sub(r'<span class="hs">(<a [^>]*>.*?</a>)<span class="sub">.*?</span></span>',
                 r"\1", nav, flags=re.S)
    # ถอดสคริปต์เดิมพร้อมช่องว่างที่พามาด้วย ไม่งั้นบรรทัดว่างจะงอกทุกรอบที่รัน
    nav = re.sub(r"\s*" + re.escape(ESC) + r"\s*(?=</nav>)", "", nav)

    m = re.search(r'<div class="drawer".*?</div></div>', nav, re.S)
    if not m:
        sys.exit(f"✗ nav.{lang}.html ไม่มีเมนูสไลด์ให้อ่าน")
    by_head = dict(groups(m.group(0)))

    links_blk = re.search(r'<div class="nav-links">(.*?)</div>', nav, re.S)
    if not links_blk:
        sys.exit(f"✗ nav.{lang}.html ไม่มีแถบเมนูบน")
    blk = links_blk.group(1)

    made = []
    for href, label in re.findall(r'<a href="([^"]+)">(.*?)</a>', blk):
        kids = by_head.get(href)
        if not kids:
            continue
        items = "".join(f'<a href="{h}">{t}</a>' for h, t in kids)
        old = f'<a href="{href}">{label}</a>'
        new = f'<span class="hs">{old}<span class="sub">{items}</span></span>'
        blk = blk.replace(old, new, 1)
        made.append((label, len(kids)))

    nav = nav.replace(links_blk.group(1), blk, 1)
    nav = re.sub(r"\s*</nav>\s*$", "\n" + ESC + "\n</nav>", nav)
    path.write_text(nav, encoding="utf-8")
    return made


def strip(s):
    """ถอดบล็อกเดิมพร้อมบรรทัดว่างที่ติดมา ไม่งั้นไฟล์จะยาวขึ้นทุกรอบที่รัน"""
    return re.sub(r"\n*" + re.escape(MARK_A) + ".*?" + re.escape(MARK_B) + r"\n*",
                  "\n", s, flags=re.S)


def restyle(lang):
    path = ROOT / "assets" / f"site.{lang}.css"
    s = strip(path.read_text(encoding="utf-8")).rstrip()
    path.write_text(s + "\n\n" + css(lang) + "\n", encoding="utf-8")


def restyle_inline(path, lang):
    """หน้าที่ไม่ได้ลิงก์ไฟล์ CSS ร่วม ต้องได้กฎชุดนี้ในบล็อก <style> ของตัวเอง

    มี 11 หน้าที่เก็บ CSS ไว้ในตัวเองทั้งหมด เพราะ split_css.mjs ถอดออกได้เฉพาะกฎที่
    ซ้ำกันตั้งแต่ 80% ของหน้าในภาษานั้น หน้าที่หน้าตาต่างจากพวกจึงไม่เข้าเกณฑ์
    ถ้าไม่ใส่ให้ เมนูย่อยบนหน้าเหล่านี้จะไม่มีกฎอะไรเลย แล้วกางค้างอยู่บนแถบเมนู
    """
    s = path.read_text(encoding="utf-8")
    out = strip(s)
    # ต้องเป็น </style> ตัวท้ายที่ยังอยู่ใน <head> เท่านั้น
    # บทความยาวมี <style> อีกก้อนซ้อนอยู่ใน <svg><defs> ซึ่งเป็นคนละ namespace
    # ถ้าใช้ตัวท้ายสุดของไฟล์ กฎจะไปตกในนั้นแล้วไม่มีผลกับหน้า — เจอจริงตอนวัดด้วย jsdom
    head = out.index("</head>")
    i = out.rindex("</style>", 0, head)
    out = out[:i].rstrip("\n") + "\n" + css(lang) + "\n" + out[i:]
    if out != s:
        path.write_text(out, encoding="utf-8")
        return True
    return False


LINKED = re.compile(r'href="/assets/site\.(?:en|th)\.css"')

made = {}
for lang in ("en", "th"):
    made[lang] = build(lang)
    restyle(lang)

inlined = []
for p in sorted(ROOT.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or '<nav id="nav">' not in s or "</style>" not in s:
        continue
    if LINKED.search(s):
        continue
    if restyle_inline(p, "th" if p.name.startswith("th-") else "en"):
        inlined.append(p.name)

r = subprocess.run([sys.executable, str(ROOT / ".tools" / "sync_nav.py")],
                   capture_output=True, text=True, cwd=ROOT)
print(r.stdout.strip() or r.stderr.strip())
if r.returncode:
    sys.exit("✗ sync_nav.py ไม่ผ่าน หยุดก่อนตรวจต่อ")

# ---- ด่านตรวจ ทั้งข้อ "มีครบ" และข้อ "ไม่เหลือ" (LESSONS ข้อ 10) ----
checks, pages = {}, []
for p in sorted(ROOT.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or p.name == "404.html" or '<nav id="nav">' not in s:
        continue
    pages.append((p, s))

for p, s in pages:
    lang = "th" if p.name.startswith("th-") else "en"
    nav = re.search(r'<nav id="nav">.*?</nav>', s, re.S).group(0)
    top = re.search(r'<div class="nav-links">(.*?)</div>\s*<div class="nav-mob">', nav, re.S)
    drawer = re.search(r'<div class="drawer".*?</div></div>', nav, re.S).group(0)
    n = p.name

    checks[f"{n} · มีเมนูย่อย {len(made[lang])} ชุด"] = nav.count('<span class="sub">') == len(made[lang])
    checks[f"{n} · เมนูย่อยอยู่ในแถบบน ไม่ใช่ในเมนูสไลด์"] = (
        bool(top) and top.group(1).count('<span class="sub">') == len(made[lang])
        and '<span class="sub">' not in drawer)
    checks[f"{n} · หัวข้อยังเป็นลิงก์"] = nav.count('<span class="hs"><a ') == len(made[lang])
    checks[f"{n} · มีตัวรับปุ่ม Escape 1 ชุด"] = nav.count('e.key==="Escape"') == 1
    # หน้าที่ไม่ได้ลิงก์ CSS ร่วม ต้องมีกฎอยู่ในตัวเอง ไม่งั้นเมนูย่อยจะกางค้าง
    head = s[:s.index("</head>")]
    inhead = "".join(re.findall(r"<style[^>]*>(.*?)</style>", head, re.S))
    inline = "".join(re.findall(r"<style[^>]*>(.*?)</style>", s, re.S))
    checks[f"{n} · กฎเมนูย่อยไปถึงหน้านี้"] = bool(LINKED.search(s)) or MARK_A in inhead
    checks[f"{n} · กฎเมนูย่อยไม่ซ้อนกัน"] = inline.count(MARK_A) <= 1

    # ทุกลิงก์ในเมนูย่อย ต้องมีอยู่ในเมนูสไลด์ด้วย ป้ายตรงกันทุกตัวอักษร
    for sub in re.findall(r'<span class="sub">(.*?)</span>', nav, re.S):
        for h, t in re.findall(r'<a (?:class="on" aria-current="page" )?href="([^"]+)">(.*?)</a>', sub):
            ok = f'href="{h}">{t}</a>' in drawer or f'aria-current="page" href="{h}">{t}</a>' in drawer
            checks[f"{n} · {html.unescape(t)[:34]} ตรงกับเมนูสไลด์"] = ok
            checks[f"{n} · {html.unescape(t)[:34]} ไฟล์มีจริง"] = (ROOT / h).exists()

for lang in ("en", "th"):
    c = (ROOT / "assets" / f"site.{lang}.css").read_text(encoding="utf-8")
    checks[f"site.{lang}.css · มีกฎเมนูย่อย 1 ชุด"] = c.count(MARK_A) == 1 and c.count(MARK_B) == 1
    checks[f"site.{lang}.css · ไม่มี letter-spacing ติดลบในกฎไทย"] = not (
        lang == "th" and re.search(r"letter-spacing:-", c[c.index(MARK_A):]))

bad = [k for k, ok in checks.items() if not ok]
if bad:
    sys.exit("✗ ด่านตรวจไม่ผ่าน:\n  " + "\n  ".join(bad[:12]))

for lang in ("en", "th"):
    print(f"  {lang}: " + " · ".join(f"{html.unescape(l)} ({n})" for l, n in made[lang]))
print(f"  กฎ CSS · ไฟล์ร่วมสองไฟล์ + ฝังในหน้าที่ไม่ได้ลิงก์อีก {len(inlined)} หน้า")
print(f"ด่านตรวจผ่าน {len(checks)} ข้อ บน {len(pages)} หน้า")
