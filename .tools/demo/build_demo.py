#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างหน้าเดโม · coffee-demo.html และ th-coffee-demo.html

แดชบอร์ดสาธิตว่า Coffee Knowledge Vault จะหน้าตาเป็นอย่างไรเมื่อมีผู้ร่วมสร้าง
คลัง 5,000 รายทั่วโลก แผนที่โลกกับกราฟความรู้ซ้อนกัน คลิกดูรายละเอียดได้
ทุกตัวเลขเป็นข้อมูลจำลอง และหน้าบอกเรื่องนี้ไว้ตั้งแต่บรรทัดแรก

ทำสองภาษาจากโครงเดียวกัน ข้อความทั้งหมดอยู่ใน copy_demo.py
ฉบับอังกฤษใช้ coffee-farmer.html เป็นแม่แบบ ฉบับไทยใช้ th-coffee-farmer.html
จึงได้ nav ธีม ฟอร์ม และ CSS ชุดเดียวกับหน้าอื่นในภาษานั้น

ป้ายในแผงที่ขึ้นตอนคลิกจุดอยู่ฝั่ง JS ตัวสร้างจึงฝัง window.__VAULT_LABELS__
ให้ dashboard.js อ่าน ถ้าไม่มีพจนานุกรม ทุกป้ายตกกลับเป็นอังกฤษ

คลาสใหม่ทั้งหมดขึ้นต้นด้วย dm- และมีด่านตรวจว่าไม่ชนของเดิม ตามบทเรียนข้อ 8
ด่านท้ายสคริปต์นับชิ้นส่วนในไฟล์ผลลัพธ์แล้ว exit ถ้าขาด ตามบทเรียนข้อ 9

รันจากรากรีโป:  python3 .tools/demo/build_demo.py
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from copy_demo import LANGS, TH_CSS          # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

DATA = json.loads((HERE / "participants.json").read_text(encoding="utf-8"))
LAND = (HERE / "land_path.txt").read_text(encoding="utf-8").strip()
CSS = (HERE / "dashboard.css").read_text(encoding="utf-8")
JS = (HERE / "dashboard.js").read_text(encoding="utf-8")

K, TY, RAD = 152.7887, 165.33, 3.141592653589793 / 180


def py(lat):
    return TY - K * lat * RAD


# ---------------------------------------------------------------- ตัวเลขในการ์ด

def by_process():
    """คะแนนคัปปิ้งเฉลี่ยรายวิธีแปรรูป ถ่วงน้ำหนักด้วยจำนวนเกษตรกร"""
    acc = {}
    for p in DATA["places"]:
        if p["role"] != "origin" or not p["proc"] or p["proc"] == "mixed":
            continue
        a = acc.setdefault(p["proc"], [0, 0])
        a[0] += p["score"] * p["c"]["farmers"]
        a[1] += p["c"]["farmers"]
    out = [(k, v[0] / v[1], v[1]) for k, v in acc.items() if v[1]]
    return sorted(out, key=lambda r: -r[1])


def bars(items, unit=""):
    top = max(v for _, v, *_ in items)
    out = []
    for row in items:
        name, val = row[0], row[1]
        w = round(val / top * 100)
        shown = f"{val:.1f}" if isinstance(val, float) else str(val)
        out.append(f'<div class="dm-bar"><span class="n">{name}</span>'
                   f'<span class="t"><i style="width:{w}%"></i></span>'
                   f'<span class="v">{shown}{unit}</span></div>')
    return "".join(out)


# ---------------------------------------------------------------- ตัวหน้า

def head_block(C):
    t = DATA["totals"]
    vals = ["5,000", f"{t['farmers']:,}", f"{t['roasters']:,}",
            f"{t['coops'] + t['mills']}", f"{t['exporters']}", f"{t['cafes']}",
            f"{t['researchers']}", f"{t['certifiers']}"]
    roles = [None, "farmers", "roasters", "coops", "exporters", "cafes",
             "researchers", "certifiers"]
    cells = []
    for v, l, p, role in zip(vals, C["stats"], C["stats_sub"], roles):
        attr = f' data-role="{role}" tabindex="0"' if role else ""
        cells.append(f'<div class="dm-stat"{attr}><div class="v">{v}</div>'
                     f'<div class="l">{l}</div><div class="p">{p}</div></div>')
    return '<div class="dm-stats">' + "".join(cells) + "</div>"


def map_block(C):
    y_top, y_bot, y_eq = py(23.5), py(-23.5), py(0)
    leg = "".join(
        f'<span><i style="background:var(--{c})"></i>{t}</span>' if c else f"<span>{t}</span>"
        for c, t in zip(["go", "ask", None], C["legend"]))
    return f'''<div class="dm-mapbox">
      <svg id="dm-map" class="dm-map" viewBox="0 0 960 293" role="img"
           aria-label="{C['map_alt']}">
        <rect class="dm-belt" x="0" y="{y_top:.1f}" width="960" height="{y_bot - y_top:.1f}"/>
        <path class="dm-land" d="{LAND}"/>
        <path class="dm-grid" d="M0 {y_top:.1f}H960M0 {y_eq:.1f}H960M0 {y_bot:.1f}H960"/>
        <text class="dm-glab" x="6" y="{y_top - 4:.1f}">TROPIC OF CANCER</text>
        <text class="dm-glab" x="6" y="{y_eq - 4:.1f}">EQUATOR</text>
        <text class="dm-glab" x="6" y="{y_bot - 4:.1f}">TROPIC OF CAPRICORN</text>
      </svg>
      <div class="dm-legend">{leg}</div>
    </div>'''


def tools_block(C):
    keys = ["trade", "quality", "match", "people"]
    btns = "".join(
        f'<button class="dm-tool{" on" if k == "trade" else ""}" data-layer="{k}">{lab}</button>'
        for k, lab in zip(keys, C["tools"]))
    return ('<div class="dm-tools">' + btns +
            f'<label class="dm-slide">{C["slider"]} '
            '<input id="dm-score" type="range" min="0" max="87" step="0.5" value="0" '
            f'aria-label="{C["slider_alt"]}">'
            f'<span id="dm-score-v">{C["slider_any"]}</span></label></div>')


def cards_block(C):
    lab = (C["labels"] or {}).get("proc", {})
    proc = [(lab.get(n, n.replace("-", " ")), s) for n, s, _ in by_process()][:5]
    body = [bars(proc), bars(C["searches"]), bars(C["hops_row"], "%")]
    out = ['<div class="dm-cards">']
    for (k, h, p), chart in zip(C["cards"], body):
        out.append(f'<div class="dm-card"><div class="k">{k}</div><h4>{h}</h4>'
                   f'<p>{p}</p>{chart}</div>')
    return "".join(out) + "</div>"


def table_block(C):
    rows = []
    for lot, origin, proc, score, notes, hops, match, kind in C["lots"]:
        rows.append(
            f"<tr><td class='mono'>{lot}</td><td><b>{origin}</b></td>"
            f"<td>{proc}</td><td><b>{score}</b></td><td>{notes}</td>"
            f"<td class='mono'>{hops} {C['hops']}</td>"
            f"<td><span class='dm-chip{' am' if kind == 'am' else ''}'>{match}</span></td></tr>")
    head = "".join(f"<th>{h}</th>" for h in C["thead"])
    return f'''<div class="dm-tablewrap">
      <table class="dm-table">
        <thead><tr>{head}</tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>
    <p class="dm-cap">{C["caption"]}</p>'''


def body(C):
    return "\n".join([
        '<article>',
        '  <div class="wrap">',
        f'    <div class="dm-warn"><b>{C["warn_b"]}</b><p>{C["warn_p"]}</p></div>',
        "    " + head_block(C),
        '    <div class="dm-wrap">',
        "      " + map_block(C),
        '      <div class="dm-panel" id="dm-panel" aria-live="polite"></div>',
        "    </div>",
        "    " + tools_block(C),
        "    " + cards_block(C),
        "    " + table_block(C),
        "  </div>",
        "</article>",
    ])


LANG_BLOCK = re.compile(r'<span class="lang">.*?</span>(?=<button)', re.S)


def build(C):
    src = ROOT / C["src"]
    out = ROOT / C["out"]
    if not src.exists():
        sys.exit(f"[abort] ไม่พบแม่แบบ {src.name}")
    s = src.read_text(encoding="utf-8")

    # กันชื่อคลาสชนของเดิม ตามบทเรียนข้อ 8
    for cls in sorted(set(re.findall(r"\.(dm-[a-z-]+)", CSS))):
        if re.search(r"(^|[\s,}])\." + re.escape(cls) + r"[\s,{:.]", s, re.M):
            sys.exit(f"[abort] คลาส .{cls} มีอยู่แล้วในแม่แบบ {src.name}")

    s = re.sub(r"<title>.*?</title>", f"<title>{C['title']}</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*"', r"\1" + C["desc"] + '"', s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*"', r"\1" + C["ogtitle"] + '"', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*"', r"\1" + C["desc"] + '"', s, count=1)
    # canonical กับ og:url ชี้มาที่หน้านี้
    s = s.replace('rel="canonical" href="https://www.neogens.co/' + C["src"] + '"',
                  'rel="canonical" href="https://www.neogens.co/' + C["out"] + '"')
    s = s.replace('property="og:url" content="https://www.neogens.co/' + C["src"] + '"',
                  'property="og:url" content="https://www.neogens.co/' + C["out"] + '"')
    # hreflang ต้องชี้ระหว่างเดโมสองฉบับ ไม่ใช่หน้าเกษตรกรที่เป็นแม่แบบ
    # ถ้าลืมข้อนี้ ทั้งสองฉบับจะประกาศตัวเองเป็นฉบับแปลของตัวเอง
    en_page = C["out"] if C["lang"] == "en" else C["twin"]
    th_page = C["out"] if C["lang"] == "th" else C["twin"]
    alts = ('<link rel="alternate" hreflang="en" href="https://www.neogens.co/%s">\n'
            '<link rel="alternate" hreflang="th" href="https://www.neogens.co/%s">\n'
            '<link rel="alternate" hreflang="x-default" href="https://www.neogens.co/%s">\n'
            % (en_page, th_page, en_page))
    s, n_alt = re.subn(r'[ \t]*<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n',
                       "", s)
    if n_alt != 3:
        sys.exit(f"[abort] แม่แบบมีแท็ก hreflang {n_alt} ตัว คาดว่าต้องมี 3")
    s = s.replace('<link rel="canonical"', alts + '<link rel="canonical"', 1)
    for old in ("coffee-farmer.html", "th-coffee-farmer.html"):
        s = s.replace(f"https://www.neogens.co/{old}", f"https://www.neogens.co/{C['out']}")

    # ปุ่มสลับภาษา ต้องชี้ระหว่างเดโมสองฉบับ ไม่ใช่หน้าเกษตรกรที่เป็นแม่แบบ
    th_out = C["out"] if C["lang"] == "th" else C["twin"]
    en_out = C["out"] if C["lang"] == "en" else C["twin"]
    lang_html = (f'<span class="lang"><a class="on" href="{th_out}">TH</a>'
                 f'<span>/</span><a href="{en_out}">EN</a></span>') if C["lang"] == "th" else (
                f'<span class="lang"><a class="on" href="{en_out}">EN</a>'
                f'<span>/</span><a href="{th_out}">TH</a></span>')
    s, n_lang = LANG_BLOCK.subn(lambda m: lang_html, s)

    # ประกาศให้ check.py รู้ว่าหน้านี้เป็นข้อมูลจำลองโดยเจตนา
    s = s.replace('<meta name="robots"',
                  '<meta name="ng-data" content="simulated">\n<meta name="robots"', 1)

    # hero
    m = re.search(r'<div class="kicker">.*?</div>\s*</div>\s*</header>', s, re.S)
    s = s[:m.start()] + (
        f'<div class="kicker">{C["kicker"]}</div>\n'
        f'      <h1>{C["h1"]}</h1>\n'
        f'      <p class="stand">{C["stand"]}</p>\n'
        f'      <div class="meta"><span>Neo Gens</span><span>{C["meta"]}</span>'
        f'<span><a href="{"th-" if C["lang"] == "th" else ""}mkm-for-coffee.html">'
        f'{C["fullargument"]}</a></span></div>\n'
        f'    </div>\n  </div>\n</header>') + s[m.end():]

    # CSS — แทรกก่อนปิดบล็อก style ของแม่แบบ
    if s.count("</style>") != 1:
        sys.exit(f"[abort] แม่แบบมี </style> {s.count('</style>')} จุด คาดว่าต้องมีจุดเดียว")
    css = CSS
    if C["lang"] == "th":
        # 1.1 ตัดหางวรรณยุกต์ไทย ต้องแก้ที่ค่าต้นทาง ไม่ใช่ทับด้วยกฎท้ายไฟล์
        css = css.replace("line-height:1.1}", "line-height:1.35}") + TH_CSS
    css = "\n/* ===== demo dashboard ===== */\n" + css
    s = s.replace("</style>", css + "</style>", 1)

    # เนื้อหา
    i, j = s.index("<article>"), s.index("</article>") + len("</article>")
    s = s[:i] + body(C) + s[j:]

    # บล็อกชวนเข้าร่วม
    s = re.sub(r'(<div class="k rv">)[^<]*(</div>)', lambda m: m.group(1) + C["join_k"] + m.group(2), s, count=1)
    s = re.sub(r'(<section class="join".*?<h2 class="rv">)[^<]*(</h2>)',
               lambda m: m.group(1) + C["join_h"] + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r'(<p class="lead rv">)[^<]*(</p>)', lambda m: m.group(1) + C["join_p"] + m.group(2), s, count=1)

    # ข้อมูลกับสคริปต์ ฝังไว้ในไฟล์ ไม่เรียก network ตอนเปิดหน้า
    payload = "<script>window.__VAULT_DEMO__=" + json.dumps(DATA, ensure_ascii=False, separators=(",", ":")) + ";"
    if C["labels"]:
        payload += "window.__VAULT_LABELS__=" + json.dumps(C["labels"], ensure_ascii=False, separators=(",", ":")) + ";"
    payload += "</script>\n<script>\n" + JS + "</script>\n"
    s = s.replace("</body>", payload + "</body>")

    # ---- ด่านสุดท้าย ทุกชิ้นต้องอยู่ในไฟล์จริง ----
    checks = {
        "กฎ CSS ของแดชบอร์ด": s.count(".dm-stat{") == 1 and s.count(".dm-panel{") == 1,
        "CSS อยู่ในบล็อก style": s.index(".dm-stat{") < s.index("</style>"),
        "ข้อมูลจำลอง": "__VAULT_DEMO__" in s,
        "สคริปต์แดชบอร์ด": "dm-node" in s and "function setLayer" in s,
        "แผนที่": 'id="dm-map"' in s and len(LAND) > 10000,
        "แผงรายละเอียด": 'id="dm-panel"' in s,
        "ป้ายบอกว่าเป็นข้อมูลจำลอง": 'name="ng-data"' in s and C["warn_b"] in s,
        "ปุ่มสลับภาษาสองชุด": n_lang == 2 and s.count(lang_html) == 2,
        "ปุ่มสลับภาษาชี้เดโมอีกฉบับ": f'href="{C["twin"]}"' in lang_html,
        "hreflang ชี้เดโมสองฉบับ": (
            f'hreflang="en" href="https://www.neogens.co/{en_page}"' in s and
            f'hreflang="th" href="https://www.neogens.co/{th_page}"' in s),
        "canonical ชี้หน้านี้": f'rel="canonical" href="https://www.neogens.co/{C["out"]}"' in s,
        "การ์ดสามใบ": s.count('<div class="dm-card">') == 3,
        "ตัวเลขสรุปแปดช่อง": s.count('<div class="dm-stat"') == 8,
        "แถวตารางหกแถว": s.count("<tr>") == 7,
        "หัวข้อหลักเป็นภาษาที่ถูก": C["h1"] in s,
    }
    if C["labels"]:
        checks["พจนานุกรมป้ายไทย"] = "__VAULT_LABELS__" in s and C["labels"]["origin"] in s
        checks["ไทยไม่ถ่างตัวอักษร"] = "letter-spacing:0}" in s
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit(f"[abort] {C['out']} ชิ้นส่วนที่ไม่เข้าไฟล์: " + ", ".join(bad))

    out.write_text(s, encoding="utf-8")
    print(f"  สร้าง {out.name} · {len(s.encode()) // 1024} KB · ตรวจชิ้นส่วนครบ {len(checks)} ข้อ")


def main():
    for C in LANGS:
        build(C)
    print(f"  {DATA['grand']:,} ราย · {len(DATA['places'])} จุดบนแผนที่")


if __name__ == "__main__":
    main()
