#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ตั้ง regex ตรวจรูปแบบอีเมลของฟอร์มให้เป็นตัวเดียวกันทุกหน้า

แก้เมื่อ 2026-08-23 พร้อมกับการปลดขาตอบกลับใน worker ออกจาก if (notified)

ทำไมต้องรัดขึ้น  เมื่อเมลตอบกลับออกทุกครั้งที่เก็บข้อมูลสำเร็จ ทุกการกดส่งจะยิงเมล
ไปยังที่อยู่ที่คนแปลกหน้าพิมพ์มา ที่อยู่ผิดบ่อย ๆ จะไปลงที่ชื่อเสียงของ send.neogens.co

**ตัวเดียวกันนี้อยู่ใน worker ด้วย** ที่ src/index.js ของรีโป neogens-briefing-worker
ค่าคงที่ชื่อ EMAIL_RE  แก้ฝั่งไหนต้องแก้อีกฝั่งให้ตรงกัน
ถ้าเว็บหลวมกว่า worker ผู้ใช้จะกดส่งได้แล้วโดนตีกลับเป็น 400 ซึ่งบอกสาเหตุไม่ตรง
ถ้าเว็บแน่นกว่า worker ผู้ใช้บางคนจะกรอกไม่ผ่านทั้งที่ระบบหลังบ้านรับได้

รันจากรากรีโป:  python3 .tools/set_email_regex.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = r"/^[^@\s]+@[^@\s]+\.[^@\s]+$/"
NEW = r"/^[^@\s]{1,64}@(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,24}$/i"

# เคสที่ใช้ยืนยันว่า regex ที่เขียนลงไปทำงานตามที่ตั้งใจ ไม่ใช่แค่ว่ามีข้อความอยู่ในไฟล์
MUST_PASS = ["mali@doichang.co", "a.b+tag@sub.example.co.th", "x@xn--12c1bik6bbd.th",
             "A@B.CO", "user_name@my-farm.com"]
MUST_FAIL = ["a@b..com", "a@b.c", "a@-.-", "a@.com", "a@b-.com", "a@-b.com",
             "plain", "a@b", "a b@c.com", "a@b.com."]

changed, bad = 0, []
for p in sorted(ROOT.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or OLD not in s:
        continue
    if s.count(OLD) != 1:
        bad.append(f"{p.name} เจอ regex เดิม {s.count(OLD)} จุด คาด 1")
        continue
    p.write_text(s.replace(OLD, NEW, 1), encoding="utf-8")
    changed += 1

# ── ด่านตรวจ · ทั้งข้อ "มีครบ" และข้อ "ไม่เหลือ" ──────────────────────
n = 0
for p in sorted(ROOT.glob("*.html")):
    s = p.read_text(encoding="utf-8")
    if 'http-equiv="refresh"' in s or "<form id=\"wl\"" not in s:
        continue
    n += 1
    if OLD in s:
        bad.append(f"{p.name} ยังเหลือ regex เดิม")
    if s.count(NEW) != 1:
        bad.append(f"{p.name} regex ใหม่มี {s.count(NEW)} จุด คาด 1")

print(f"แก้ regex {changed} หน้า · หน้าที่มีฟอร์มทั้งหมด {n} หน้า")
if bad:
    for b in bad[:8]:
        print("  ✗", b)
    sys.exit(1)

# พิสูจน์พฤติกรรมจริงด้วย node ไม่ใช่เชื่อว่าข้อความในไฟล์ถูก
import json
import subprocess

probe = (f"const RE={NEW};"
         f"const ok={json.dumps(MUST_PASS)},no={json.dumps(MUST_FAIL)};"
         "let e=[];ok.forEach(v=>{if(!RE.test(v))e.push('ควรผ่านแต่ตก '+v)});"
         "no.forEach(v=>{if(RE.test(v))e.push('ควรตกแต่ผ่าน '+v)});"
         "console.log(JSON.stringify(e));")
try:
    out = subprocess.run(["node", "-e", probe], capture_output=True, text=True, check=True).stdout
    errs = json.loads(out)
except (OSError, subprocess.CalledProcessError) as err:
    sys.exit(f"✗ รัน node ตรวจ regex ไม่ได้ — {err}")
if errs:
    for e in errs:
        print("  ✗", e)
    sys.exit(1)
print(f"✓ regex ตรงกันทุกหน้า · ผ่าน {len(MUST_PASS)} เคสที่ควรผ่าน · ตก {len(MUST_FAIL)} เคสที่ควรตก")
print("  อย่าลืมว่าตัวเดียวกันนี้อยู่ใน worker ที่ EMAIL_RE ของ src/index.js")
