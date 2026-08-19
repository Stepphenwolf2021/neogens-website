#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ใส่ป้ายชื่อช่องจริงให้ฟอร์ม และบอกให้ชัดเมื่ออีเมลผิดรูป   ข้อ 13 จากรายงานตรวจ

ของเดิมใช้ placeholder กับ aria-label แทนป้ายชื่อช่อง
  aria-label ช่วยโปรแกรมอ่านหน้าจอได้จริง แต่ไม่ช่วยคนที่พิมพ์ไปครึ่งทางแล้วลืมว่าช่องนี้คืออะไร
  เพราะ placeholder หายไปทันทีที่เริ่มพิมพ์

และของเดิม ถ้ากรอกอีเมลผิดรูป สคริปต์แค่ย้ายเคอร์เซอร์กลับไปที่ช่องเงียบ ๆ ไม่บอกอะไรเลย
คนกรอกจะเห็นแค่ปุ่มที่กดแล้วไม่เกิดอะไรขึ้น

ข้อความบนป้ายยกมาจาก aria-label เดิมของแต่ละช่อง ไม่ได้เขียนใหม่
จึงไม่มีคำใหม่โผล่บนเว็บจากสคริปต์นี้ และสองภาษายังตรงกันเหมือนเดิม

รันจากรากรีโป:  python3 .tools/fix_form_labels.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS = """
/* --- ป้ายชื่อช่องในฟอร์ม --- */
.ffield{{flex:1;min-width:0;display:flex;flex-direction:column;gap:6px}}
.ffield input{{width:100%}}
.flab{{font-family:var(--mono);font-size:10.5px;letter-spacing:{ls};text-transform:uppercase;
  color:var(--mute);padding-left:17px;line-height:1.8}}
"""

MSG = {"en": "That email address does not look right — check it and try again.",
       "th": "รูปแบบอีเมลยังไม่ถูก ลองตรวจอีกครั้ง"}

INPUT = re.compile(
    r'<input type="(text|email)" id="(\w+)"[^>]*?placeholder="([^"]*)"[^>]*?'
    r'aria-label="([^"]*)"([^>]*)>')

done = []
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or "NG_ENDPOINT" not in s:
        continue
    if 'class="flab"' in s:
        continue
    lang = "th" if path.name.startswith("th-") else "en"

    # 1 · ป้ายชื่อช่อง ใช้ข้อความเดิมจาก aria-label ตัด placeholder กับ aria-label ที่ซ้ำซ้อนออก
    def wrap(m):
        typ, fid, ph, label, rest = m.groups()
        rest = rest.rstrip()
        return (f'<div class="ffield"><label class="flab" for="{fid}">{label}</label>'
                f'<input type="{typ}" id="{fid}"{rest}></div>')

    s, n_lab = INPUT.subn(wrap, s)

    # 2 · ประกาศให้โปรแกรมอ่านหน้าจอรู้ตัวเมื่อผลลัพธ์เปลี่ยน
    s = s.replace('<div class="ok" id="ok">', '<div class="ok" id="ok" role="status">', 1)
    s = s.replace('<div class="err" id="err">', '<div class="err" id="err" role="alert">', 1)

    # 3 · อีเมลผิดรูป ต้องบอก ไม่ใช่ย้ายเคอร์เซอร์เงียบ ๆ
    old_js = "{emailEl.focus();return;}"
    new_js = ("{emailEl.setAttribute('aria-invalid','true');"
              "if(errEl){errEl.innerHTML=" + repr(MSG[lang]).replace("'", '"') + ";"
              "errEl.style.display='block';}emailEl.focus();return;}")
    if s.count(old_js) != 1:
        sys.exit(f"✗ {path.name} เจอจุดตรวจอีเมล {s.count(old_js)} จุด คาดว่า 1")
    s = s.replace(old_js, new_js, 1)
    s = s.replace("if(errEl) errEl.style.display='none';",
                  "if(errEl) errEl.style.display='none';\n    emailEl.removeAttribute('aria-invalid');", 1)

    s = s.replace("</style>", CSS.format(ls=".08em" if lang == "en" else "0") + "</style>", 1)

    checks = {
        "ป้ายครบทุกช่องที่มองเห็น": n_lab >= 3 and s.count('class="flab"') == n_lab,
        "ไม่เหลือ placeholder ในช่องที่มีป้ายแล้ว": s.count('placeholder="') == 0,
        "ไม่เหลือ aria-label ซ้ำซ้อนในฟอร์ม": '<input type="email"' in s and 'aria-label="' not in re.search(r'<form id="wl".*?</form>', s, re.S).group(0),
        "for ตรงกับ id ทุกคู่": all(f'id="{fid}"' in s for fid in re.findall(r'<label class="flab" for="(\w+)">', s)),
        "กับดักบอทยังอยู่และยังซ่อน": 'id="website"' in s and 'left:-9999px' in s,
        "แจ้งเตือนอีเมลผิดรูป": "aria-invalid" in s and MSG[lang] in s,
        "err ประกาศตัวเป็น alert": 'id="err" role="alert"' in s,
        "CSS เข้าไฟล์": ".flab{" in s and s.index(".flab{") < s.index("</style>"),
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {path.name}: " + " · ".join(bad))
    path.write_text(s, encoding="utf-8")
    done.append((path.name, n_lab))

print(f"แก้ {len(done)} หน้า · ป้ายชื่อช่องรวม {sum(n for _, n in done)} ป้าย")
print("✓ ทุกช่องมีป้ายที่มองเห็น · อีเมลผิดรูปมีข้อความบอก · err ประกาศตัวเป็น alert")
