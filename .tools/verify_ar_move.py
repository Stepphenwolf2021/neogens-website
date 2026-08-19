#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ตรวจการย้ายบล็อก AR ระดับ "ข้อความที่มองเห็น"

ใช้คู่กับ move_ar_block.py
  python3 .tools/verify_ar_move.py --snap /tmp/ar_before.json   # ก่อนย้าย
  python3 .tools/move_ar_block.py
  python3 .tools/verify_ar_move.py --check /tmp/ar_before.json  # หลังย้าย

พิสูจน์สองข้อ
  1. ข้อความที่มองเห็นของทั้งสี่ไฟล์รวมกัน ก่อนกับหลัง เหมือนกันทุกตัวอักษร (ไม่มีคำหาย ไม่มีคำเพิ่ม)
  2. ทุกชิ้นที่หายไปจาก about ไปโผล่ที่ experience ครบ
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["about.html", "th-about.html", "visitors-and-readers.html", "th-visitors-and-readers.html"]


def visible(html: str):
    """คืนลิสต์ข้อความที่ผู้ใช้มองเห็น + ข้อความใน attribute ที่คนอ่านได้"""
    s = re.sub(r"<script\b.*?</script>", " ", html, flags=re.S | re.I)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.S | re.I)

    attrs = re.findall(
        r'(?:alt|aria-label|title|placeholder)="([^"]*)"', s, flags=re.I)

    s = re.sub(r"<[^>]+>", "\n", s)
    words = [w for w in (t.strip() for t in s.split("\n")) if w]
    words += [a.strip() for a in attrs if a.strip()]
    return words


def snapshot():
    return {f: visible((ROOT / f).read_text(encoding="utf-8")) for f in FILES}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snap")
    ap.add_argument("--check")
    a = ap.parse_args()

    if a.snap:
        Path(a.snap).write_text(json.dumps(snapshot(), ensure_ascii=False),
                                encoding="utf-8")
        print(f"เก็บ snapshot แล้ว -> {a.snap}")
        return

    if not a.check:
        ap.error("ต้องระบุ --snap หรือ --check")

    before = json.loads(Path(a.check).read_text(encoding="utf-8"))
    after = snapshot()
    ok = True

    tot_b = Counter(x for f in FILES for x in before[f])
    tot_a = Counter(x for f in FILES for x in after[f])

    lost = tot_b - tot_a
    gained = tot_a - tot_b

    print(f"ข้อความที่มองเห็นรวมสี่ไฟล์  ก่อน {sum(tot_b.values())} ชิ้น  "
          f"หลัง {sum(tot_a.values())} ชิ้น")

    if lost:
        ok = False
        print("\n[ผิด] ข้อความที่หายไปจากเว็บ")
        for t, n in lost.items():
            print(f"  -{n}  {t[:110]}")
    if gained:
        ok = False
        print("\n[ผิด] ข้อความที่โผล่ขึ้นมาใหม่")
        for t, n in gained.items():
            print(f"  +{n}  {t[:110]}")
    if not lost and not gained:
        print("  ผ่าน · ไม่มีคำหาย ไม่มีคำเพิ่ม ไม่มีคำเปลี่ยน")

    print()
    for src, dst in [("about.html", "visitors-and-readers.html"),
                     ("th-about.html", "th-visitors-and-readers.html")]:
        moved_out = Counter(before[src]) - Counter(after[src])
        moved_in = Counter(after[dst]) - Counter(before[dst])
        n = sum(moved_out.values())
        if moved_out == moved_in:
            print(f"  ผ่าน · {src} -> {dst} · ย้าย {n} ชิ้น ตรงกันทุกชิ้น")
        else:
            ok = False
            print(f"  [ผิด] {src} -> {dst} ไม่ตรงกัน")
            for t, c in (moved_out - moved_in).items():
                print(f"    ออกจาก {src} แต่ไม่ถึง {dst}: {t[:100]}")
            for t, c in (moved_in - moved_out).items():
                print(f"    โผล่ที่ {dst} แต่ไม่ได้มาจาก {src}: {t[:100]}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
