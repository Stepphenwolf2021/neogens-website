#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
แยกข้อความกรณีโดนจำกัดอัตรา (HTTP 429) ออกจากกรณีส่งไม่สำเร็จจริง ในฟอร์มทุกหน้า

อาการเดิม มีแค่หน้ากลุ่มกาแฟหกหน้าที่แยกสองกรณีนี้ หน้าที่เหลือถ้าโดน 429
จะขึ้นว่า "ส่งไม่สำเร็จ และไม่มีการบันทึกใด ๆ" ซึ่งบอกสาเหตุผิด
คนกรอกจะคิดว่าฟอร์มพัง ทั้งที่ระบบแค่กันการส่งซ้ำถี่เกินไป

ข้อความที่ใช้ยกมาจากหน้ากาแฟทั้งสองภาษา ไม่ได้เขียนใหม่ เพื่อให้ทั้งเว็บพูดเหมือนกัน

รันจากรากรีโป:  python3 .tools/add_rate_limit_msg.py
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RATE_EN = ("Too many submissions from your network in the last hour, so this one was "
           "not recorded. Try again later, or write directly to "
           "<b>hello@neogens.co</b>.")
RATE_TH = ("ชั่วโมงนี้มีการส่งจากเครือข่ายเดียวกับคุณมากเกินกำหนด รายการนี้จึงยังไม่ถูกบันทึก "
           "ลองใหม่ภายหลัง หรือเขียนตรงมาที่ <b>hello@neogens.co</b> ได้เลย")

BRANCH = ("if(res.status===429){var e=new Error('rate_limited');e.rate=true;throw e;}\n"
          "      throw new Error('http_'+res.status);")
CATCH = re.compile(r"\}\)\.catch\(function\(\)\{\n(\s*)if\(errEl\)\{errEl\.innerHTML=('.*?');",
                   re.S)

done, already, skipped = [], [], []
for path in sorted(ROOT.glob("*.html")):
    s = before = path.read_text(encoding="utf-8")
    if "NG_ENDPOINT" not in s or "errEl" not in s:
        skipped.append(path.name); continue
    if "res.status===429" in s:
        already.append(path.name); continue

    if s.count("throw new Error('http_'+res.status);") != 1:
        sys.exit(f"✗ {path.name} เจอจุดโยน error {s.count(chr(39))} รูปแบบไม่ตรงที่คาด")
    s = s.replace("throw new Error('http_'+res.status);", BRANCH, 1)

    rate = RATE_TH if path.name.startswith("th-") else RATE_EN
    m = CATCH.search(s)
    if not m:
        sys.exit(f"✗ {path.name} หา catch ของฟอร์มไม่เจอ")
    generic = m.group(2)
    s = (s[:m.start()] + "}).catch(function(e){\n" + m.group(1) +
         "if(errEl){errEl.innerHTML=(e&&e.rate)?" + repr(rate).replace('"', "&quot;") +
         ":" + generic + ";" + s[m.end():])

    # ---- ด่านตรวจต่อไฟล์ ----
    checks = {
        "มีสาขา 429": s.count("res.status===429") == 1,
        "catch รับพารามิเตอร์": s.count("}).catch(function(e){") == 1,
        "แยกสองข้อความ": s.count("(e&&e.rate)?") == 1,
        "ข้อความเดิมยังอยู่": generic.strip("'") in s,
        "ไม่มี catch แบบเก่าเหลือ": "}).catch(function(){" not in s,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"✗ {path.name} ด่านตรวจไม่ผ่าน: " + " · ".join(bad))
    path.write_text(s, encoding="utf-8")
    done.append(path.name)

print(f"แก้ {len(done)} หน้า · แยกไว้อยู่แล้ว {len(already)} หน้า · ไม่มีฟอร์ม {len(skipped)} หน้า")
