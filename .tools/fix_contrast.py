#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ยกระดับ contrast ของสี --mute ให้ผ่านเกณฑ์ WCAG AA · ข้อ 03 จากรายงานตรวจก่อนเปิดตัว

--mute ใช้กับป้าย mono ขนาด 10–11px ทั่วเว็บ — ป้ายหมวด หัวตาราง ป้ายในแดชบอร์ด
ขนาดนั้นนับเป็นข้อความปกติตามเกณฑ์ ต้องได้ 4.5:1 แต่ของเดิมได้

    ธีมมืด  บนพื้นหน้า   4.27:1     บนพื้นการ์ด  3.96:1
    ธีมสว่าง บนพื้นหน้า   3.81:1

ค่าใหม่เลือกโดยขยับจากค่าเดิมทีละขั้นจนผ่านเกณฑ์บนพื้นที่เข้มที่สุดที่มันไปวางอยู่
จึงเป็นการขยับน้อยที่สุดที่ยังผ่าน และยังคงลำดับความเข้ม fg → dim → mute ไว้เหมือนเดิม

รันจากรากรีโป:  python3 .tools/fix_contrast.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# เดิม → ใหม่ · พื้นที่ต้องผ่านเกณฑ์
FIX = {
    "--mute:#6E757D": ("--mute:#7C838B", ["#08090A", "#111417", "#171B1F"]),   # ธีมมืด
    "--mute:#79818A": ("--mute:#6D757E", ["#FCFBF8"]),                          # ธีมสว่าง
}


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def ratio(a, b):
    l1, l2 = sorted([lum(a), lum(b)], reverse=True)
    return (l1 + .05) / (l2 + .05)


# พิสูจน์ก่อนแตะไฟล์ว่าค่าใหม่ผ่านเกณฑ์จริง ไม่ใช่เชื่อว่าผ่าน
for old, (new, grounds) in FIX.items():
    col = new.split(":")[1]
    for g in grounds:
        r = ratio(col, g)
        if r < 4.5:
            sys.exit(f"✗ {col} บนพื้น {g} ได้ {r:.2f}:1 ยังไม่ถึง 4.5 ยังไม่ได้แตะไฟล์")
    print(f"  {old.split(':')[1]} → {col}  " +
          "  ".join(f"บน {g} {ratio(col, g):.2f}:1" for g in grounds))

changed = 0
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    for old, (new, _) in FIX.items():
        s = s.replace(old, new)
    if s != before:
        path.write_text(s, encoding="utf-8")
        changed += 1

left = []
for path in ROOT.glob("*.html"):
    s = path.read_text(encoding="utf-8")
    for old in FIX:
        if old in s:
            left.append(f"{path.name} {old}")

print(f"\nแก้ {changed} ไฟล์")
if left:
    sys.exit("✗ ยังเหลือค่าเดิม: " + ", ".join(left[:6]))
print("✓ ไม่เหลือค่าเดิมในไฟล์ไหน")
