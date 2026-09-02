#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""แถบ ก่อนหน้า/ถัดไป ท้ายหน้า · สร้างจากลำดับเมนู แหล่งเดียว · 2026-09-01

**ปัญหาที่แก้** แถบนี้เคยถูกเขียนครั้งเดียวโดย build_sections.py ตอนย้ายโครงเว็บ
แล้วหลังจากนั้นก็ไม่มีใครดูแล พอหน้าถูกเพิ่ม ถูกย้าย และภาค 3 ถูกถอดออก
ลำดับก็เพี้ยนทีละนิดจนตรวจพบเมื่อ 1 กันยายน 2569 ว่าผิด 9 หน้าต่อภาษา

    the-problem                   ปุ่ม ก่อนหน้า ชี้ไปหน้า 02 ซึ่งอยู่ถัดไป
    ontology-and-knowledge-graph  ปุ่ม ก่อนหน้า ข้ามหน้า 03
    ai-sovereignty                ทั้งสองปุ่มเด้งกลับไปภาค 1
    about กับ what-we-wont-do     ปุ่มคู่เดียวกันเป๊ะ สองหน้าอ้างตำแหน่งเดียวกัน
    exec-summary-museums          ไม่มีแถบเลย ทั้งที่หน้าอื่นในภาคเดียวกันมี

**หลักที่ใช้** ลำดับการอ่านมีแหล่งเดียวคือลำดับในเมนู `.tools/shell/nav.*.html`
เหมือนที่ breadcrumb ใช้ป้ายเดียวกับเมนู ถ้าจะเปลี่ยนลำดับ ให้เปลี่ยนที่เมนู
แล้วรันสคริปต์นี้ ห้ามแก้แถบนี้ในไฟล์ HTML ด้วยมือ เพราะจะกลับไปเพี้ยนอีก

**ป้ายที่แสดง** ไม่ได้เขียนใหม่ ใช้ป้ายเดิมที่หน้าอื่นเรียกหน้านั้นอยู่แล้ว
เก็บจากในเว็บตอนรัน ถ้าไม่เคยมีใครเรียก จึงค่อยใช้ป้ายเมนู
สคริปต์นี้แก้ลำดับ ไม่แตะถ้อยคำ

**หน้าไทย** ข้ามรายการที่ไม่ได้ขึ้นต้นด้วย th- เพราะเมนูไทยมีลิงก์บทความยาว
ฉบับอังกฤษอยู่ด้วย ถ้าใส่เข้าลูกโซ่ คนอ่านไทยจะถูกโยนไปหน้าอังกฤษกลางทาง

รันจากรากรีโป:  python3 .tools/build_chain.py
"""
import html
import io
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHELL = ROOT / ".tools" / "shell"

# หน้าเปิดกับหน้าปิดของลูกโซ่ ไม่นับเป็นสมาชิก แต่เป็นปลายทางของหัวและท้าย
ENDS = {"en": ("index.html", "contact.html"),
        "th": ("th-index.html", "th-contact.html")}


def nav_order(lang):
    """ลำดับและป้ายจากลิ้นชักเมนู · แหล่งความจริงเดียวของลำดับการอ่าน"""
    nav = (SHELL / f"nav.{lang}.html").read_text(encoding="utf-8")
    dw = re.search(r'<div class="drawer".*?</nav>', nav, re.S)
    if not dw:
        sys.exit(f"✗ nav.{lang}.html ไม่มีลิ้นชักเมนู")
    out = []
    for href, lab in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>([^<]*)</a>', dw.group(0)):
        if href.endswith(".html") and href not in [h for h, _ in out]:
            out.append((href, html.unescape(lab).strip()))
    return out


def harvest_labels():
    """ป้ายที่เว็บเรียกแต่ละหน้าอยู่แล้ว เก็บจากแถบเดิมทุกหน้า เอาตัวที่ใช้บ่อยสุด"""
    c = {}
    for p in sorted(ROOT.glob("*.html")):
        s = p.read_text(encoding="utf-8")
        for href, lab in re.findall(
                r'<a class="(?:pv|nx)" href="([^"]+)">'
                r'<div class="k">[^<]*</div><div class="t">([^<]*)</div></a>', s):
            c.setdefault(href, Counter())[lab] += 1
    return {h: k.most_common(1)[0][0] for h, k in c.items()}


def span(s):
    """ช่วงของ <div class="pn"> ถึง </div> ที่คู่กัน ไล่นับ ไม่ใช้ regex ตามบทเรียนข้อ 11"""
    i = s.find('<div class="pn">')
    if i < 0:
        return None
    depth, j = 0, i
    while j < len(s):
        if s.startswith("<div", j):
            depth += 1
        elif s.startswith("</div>", j):
            depth -= 1
            if depth == 0:
                return i, j + len("</div>")
        j += 1
    sys.exit("✗ หา </div> ปิดของแถบ pn ไม่เจอ")


def block(thai, pv, nx):
    return ('<div class="pn"><div class="pn-in">'
            '<a class="pv" href="%s"><div class="k">%s</div><div class="t">%s</div></a>'
            '<a class="nx" href="%s"><div class="k">%s</div><div class="t">%s</div></a>'
            '</div></div>' % (pv[0], "ก่อนหน้า" if thai else "Previous", pv[1],
                              nx[0], "ถัดไป" if thai else "Next", nx[1]))


def run():
    labels = harvest_labels()
    total, written, chains = 0, 0, {}

    for lang in ("en", "th"):
        head, tail = ENDS[lang]
        order = [(h, l) for h, l in nav_order(lang) if h not in (head, tail)]
        if lang == "th":
            order = [(h, l) for h, l in order if h.startswith("th-")]
        chains[lang] = [h for h, _ in order]

        def label(href, fallback):
            return html.escape(labels.get(href, fallback), quote=False)

        # ป้ายของหัวและท้ายลูกโซ่ ไม่มีในเมนูแบบเดียวกัน จึงกำหนดตรงนี้
        head_lab = "สารบัญทั้งหมด" if lang == "th" else "All sections"
        tail_lab = labels.get(tail, "ขอนัดหารือ" if lang == "th" else "Request a briefing")

        for i, (href, navlab) in enumerate(order):
            p = ROOT / href
            if not p.exists():
                sys.exit(f"✗ เมนูชี้ไฟล์ที่ไม่มี {href}")
            s = p.read_text(encoding="utf-8")
            total += 1
            pv = (head, head_lab) if i == 0 else \
                 (order[i - 1][0], label(order[i - 1][0], order[i - 1][1]))
            nx = (tail, tail_lab) if i == len(order) - 1 else \
                 (order[i + 1][0], label(order[i + 1][0], order[i + 1][1]))
            new = block(lang == "th", pv, nx)

            sp = span(s)
            if sp:
                out = s[:sp[0]] + new + s[sp[1]:]
            else:
                k = s.find("</main>")
                if k < 0:
                    sys.exit(f"✗ {href} ไม่มี </main> ให้วางแถบ")
                out = s[:k] + new + "\n" + s[k:]

            checks = {
                "มีแถบเดียว": out.count('<div class="pn">') == 1,
                "ไม่ชี้ตัวเอง": f'href="{href}"' not in new,
                "ปุ่มครบสองปุ่ม": new.count('class="pv"') == 1 and new.count('class="nx"') == 1,
                "แท็ก div สมดุล": out.count("<div") == out.count("</div>"),
                "แถบอยู่ใน main": out.find('<div class="pn">') < out.find("</main>"),
                "โครงหน้ายังครบ": all(x in out for x in ["</footer>", "<h1", 'id="main"']),
            }
            bad = [k2 for k2, ok in checks.items() if not ok]
            if bad:
                sys.exit(f"✗ {href} ไม่ผ่าน: " + " · ".join(bad))
            if out != s:
                p.write_text(out, encoding="utf-8")
                written += 1

    # ── ด่านตรวจรวม ทั้งแบบ มีครบ และ ไม่เหลือ ──
    bad = []
    for lang in ("en", "th"):
        head, tail = ENDS[lang]
        ch = chains[lang]
        for i, href in enumerate(ch):
            s = (ROOT / href).read_text(encoding="utf-8")
            hs = dict(re.findall(r'class="(pv|nx)" href="([^"]+)"', s))
            want_p = head if i == 0 else ch[i - 1]
            want_n = tail if i == len(ch) - 1 else ch[i + 1]
            if hs.get("pv") != want_p:
                bad.append(f"{href} ก่อนหน้า={hs.get('pv')} ควรเป็น {want_p}")
            if hs.get("nx") != want_n:
                bad.append(f"{href} ถัดไป={hs.get('nx')} ควรเป็น {want_n}")
            for h in hs.values():
                if not (ROOT / h).exists():
                    bad.append(f"{href} ชี้ไฟล์ที่ไม่มี {h}")
        if len(set(ch)) != len(ch):
            bad.append(f"ลูกโซ่ {lang} มีหน้าซ้ำ")

    print(f"ลูกโซ่การอ่าน · อังกฤษ {len(chains['en'])} หน้า · ไทย {len(chains['th'])} หน้า "
          f"· เขียนใหม่ {written} จาก {total}")
    for b in bad[:10]:
        print("  ✗", b)
    if bad:
        sys.exit(1)
    print("✓ ทุกหน้าเดินหน้าถอยหลังได้ตรงลำดับเมนู · ไม่มีหน้าไหนข้ามหรือชี้ตัวเอง")


if __name__ == "__main__":
    run()
