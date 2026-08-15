#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างหน้าเดโม · coffee-demo.html

แดชบอร์ดสาธิตว่า Coffee Knowledge Vault จะหน้าตาเป็นอย่างไรเมื่อมีผู้ร่วมสร้าง
คลัง 5,000 รายทั่วโลก แผนที่โลกกับกราฟความรู้ซ้อนกัน คลิกดูรายละเอียดได้
ทุกตัวเลขเป็นข้อมูลจำลอง และหน้าบอกเรื่องนี้ไว้ตั้งแต่บรรทัดแรก

ใช้ coffee-farmer.html เป็นแม่แบบ จึงได้ nav ธีม ฟอร์ม และ CSS ชุดเดียวกัน
คลาสใหม่ทั้งหมดขึ้นต้นด้วย dm- และมีด่านตรวจว่าไม่ชนของเดิม ตามบทเรียนข้อ 8

รันจากรากรีโป:  python3 .tools/demo/build_demo.py
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SRC = ROOT / "coffee-farmer.html"
OUT = ROOT / "coffee-demo.html"

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


SEARCHES = [
    ("floral · tea-like", 214),
    ("low acidity", 187),
    ("honey process", 156),
    ("single plot", 143),
    ("shade grown", 98),
]

LOTS = [
    ("LOT-2026-0412", "Chiang Rai, Thailand", "honey", "86.5",
     "longan · tamarind", "5", "Osaka · 2 roasters", "go"),
    ("LOT-2026-0388", "Huila, Colombia", "washed", "85.9",
     "citrus · red fruit", "6", "Berlin · 4 roasters", "go"),
    ("LOT-2026-0361", "Yirgacheffe, Ethiopia", "natural", "87.2",
     "jasmine · peach", "4", "Seoul · 3 roasters", "go"),
    ("LOT-2026-0344", "Nyeri, Kenya", "washed", "86.8",
     "blackcurrant · tomato", "5", "Melbourne · 2 roasters", "go"),
    ("LOT-2026-0329", "Cerrado, Brazil", "natural", "83.4",
     "nut · cocoa", "3", "moisture reading pending", "am"),
    ("LOT-2026-0317", "Aceh, Indonesia", "wet-hulled", "84.1",
     "cedar · herbal", "4", "Taipei · 1 roaster", "go"),
]


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

def head_block():
    t = DATA["totals"]
    stat = [
        ("5,000", "Contributors", "43 origins and markets", None),
        (f"{t['farmers']:,}", "Farmers", "80% of the vault", "farmers"),
        (f"{t['roasters']:,}", "Roasters", "10%", "roasters"),
        (f"{t['coops'] + t['mills']}", "Co-ops &amp; mills", "the collection layer", "coops"),
        (f"{t['exporters']}", "Exporters &amp; importers", "compliance and shipping", "exporters"),
        (f"{t['cafes']}", "Cafés", "the last mile", "cafes"),
        (f"{t['researchers']}", "Researchers", "agronomy and sensory", "researchers"),
        (f"{t['certifiers']}", "Certifiers", "independent verification", "certifiers"),
    ]
    cells = []
    for v, l, p, role in stat:
        attr = f' data-role="{role}" tabindex="0"' if role else ""
        cells.append(f'<div class="dm-stat"{attr}><div class="v">{v}</div>'
                     f'<div class="l">{l}</div><div class="p">{p}</div></div>')
    return '<div class="dm-stats">' + "".join(cells) + "</div>"


def map_block():
    y_top, y_bot, y_eq = py(23.5), py(-23.5), py(0)
    return f'''<div class="dm-mapbox">
      <svg id="dm-map" class="dm-map" viewBox="0 0 960 293" role="img"
           aria-label="World map with the coffee belt shaded, showing 43 points where contributors have registered, and curved lines linking each origin to the markets that buy from it">
        <rect class="dm-belt" x="0" y="{y_top:.1f}" width="960" height="{y_bot - y_top:.1f}"/>
        <path class="dm-land" d="{LAND}"/>
        <path class="dm-grid" d="M0 {y_top:.1f}H960M0 {y_eq:.1f}H960M0 {y_bot:.1f}H960"/>
        <text class="dm-glab" x="6" y="{y_top - 4:.1f}">TROPIC OF CANCER</text>
        <text class="dm-glab" x="6" y="{y_eq - 4:.1f}">EQUATOR</text>
        <text class="dm-glab" x="6" y="{y_bot - 4:.1f}">TROPIC OF CAPRICORN</text>
      </svg>
      <div class="dm-legend">
        <span><i style="background:var(--go)"></i>origin · farms, co-ops, mills</span>
        <span><i style="background:var(--ask)"></i>market · roasters, cafés, importers</span>
        <span>line = a trade route already carrying verified lots</span>
      </div>
    </div>'''


def panel_block():
    return '<div class="dm-panel" id="dm-panel" aria-live="polite"></div>'


def tools_block():
    tools = [("trade", "Trade routes"), ("quality", "High-scoring origins"),
             ("match", "Buyer matches"), ("people", "Contributors only")]
    btns = "".join(
        f'<button class="dm-tool{" on" if k == "trade" else ""}" data-layer="{k}">{lab}</button>'
        for k, lab in tools)
    return ('<div class="dm-tools">' + btns +
            '<label class="dm-slide">cup score '
            '<input id="dm-score" type="range" min="0" max="87" step="0.5" value="0" '
            'aria-label="Filter origins by mean cup score">'
            '<span id="dm-score-v">any</span></label></div>')


def cards_block():
    proc = [(n.replace("-", " "), s) for n, s, _ in by_process()][:5]
    return f'''<div class="dm-cards">
      <div class="dm-card">
        <div class="k">Quality</div>
        <h4>What method gets the score, at your altitude</h4>
        <p>Mean cup score by processing method across every lot in the vault. A farmer
        filters this to plots within 150 m of their own elevation before deciding what to
        try next season.</p>
        {bars(proc)}
      </div>
      <div class="dm-card">
        <div class="k">Market</div>
        <h4>What buyers are searching for</h4>
        <p>Roasters query the vault by profile rather than by broker relationship. These
        are the searches that returned too few lots this month — each one is a market
        opening visible from the growing side.</p>
        {bars(SEARCHES)}
      </div>
      <div class="dm-card">
        <div class="k">Traceability</div>
        <h4>How far back a bag can be walked</h4>
        <p>Every hop carries a date, a quantity and a source. Where a machine reading
        backs the claim, the lot is marked verified rather than stated.</p>
        {bars([("plot", 81), ("mill", 93), ("exporter", 97), ("roaster", 99)], "%")}
      </div>
    </div>'''


def table_block():
    rows = []
    for lot, origin, proc, score, notes, hops, match, kind in LOTS:
        rows.append(
            f"<tr><td class='mono'>{lot}</td><td><b>{origin}</b></td>"
            f"<td>{proc}</td><td><b>{score}</b></td><td>{notes}</td>"
            f"<td class='mono'>{hops} hops</td>"
            f"<td><span class='dm-chip{' am' if kind == 'am' else ''}'>{match}</span></td></tr>")
    return f'''<div class="dm-tablewrap">
      <table class="dm-table">
        <thead><tr><th>Lot</th><th>Origin</th><th>Process</th><th>Score</th>
        <th>Flavour</th><th>Traceable</th><th>Buyer match</th></tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>
    <p class="dm-cap">Every figure on this page is simulated. The point is the shape of
    the answer, not the numbers: one structure, contributed to by everyone along the
    chain, that a farmer can query for what to do next season and a roaster can query
    for what to buy — and both get an answer that carries its own evidence.</p>'''


def body():
    return ("\n".join([
        '<article>',
        '  <div class="wrap">',
        '    <div class="dm-warn"><b>Simulated</b><p>Nothing on this page is real data. '
        'It is a working sketch of what the Coffee Knowledge Vault looks like once '
        '5,000 people along the chain have contributed to it. No one has contributed '
        'yet — that is the phase we are in.</p></div>',
        "    " + head_block(),
        '    <div class="dm-wrap">',
        "      " + map_block(),
        "      " + panel_block(),
        "    </div>",
        "    " + tools_block(),
        "    " + cards_block(),
        "    " + table_block(),
        "  </div>",
        "</article>",
    ]))


HEAD = dict(
    title="What 5,000 contributors would look like — Neo Gens",
    ogtitle="What 5,000 contributors would look like",
    desc="A simulated dashboard of the Coffee Knowledge Vault: 5,000 contributors "
         "along the coffee chain, a knowledge graph laid over the world map, and what "
         "a farmer or a roaster would actually ask it.",
    kicker="MKM for Coffee · demo",
    h1="What the vault looks like with 5,000 people in it",
    stand="A simulated view of the Coffee Knowledge Vault — every origin, every market, "
          "and the routes already carrying verified lots between them. Click any point.",
    meta="interactive demo",
)


def main():
    if not SRC.exists():
        sys.exit(f"[abort] ไม่พบแม่แบบ {SRC.name}")
    s = SRC.read_text(encoding="utf-8")

    # กันชื่อคลาสชนของเดิม ตามบทเรียนข้อ 8
    for cls in sorted(set(re.findall(r"\.(dm-[a-z-]+)", CSS))):
        if re.search(r"(^|[\s,}])\." + re.escape(cls) + r"[\s,{:.]", s, re.M):
            sys.exit(f"[abort] คลาส .{cls} มีอยู่แล้วในแม่แบบ")

    s = re.sub(r"<title>.*?</title>", f"<title>{HEAD['title']}</title>", s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*"', r"\1" + HEAD["desc"] + '"', s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*"', r"\1" + HEAD["ogtitle"] + '"', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*"', r"\1" + HEAD["desc"] + '"', s, count=1)
    s = s.replace("https://www.neogens.co/coffee-farmer.html",
                  "https://www.neogens.co/coffee-demo.html")
    s = s.replace("https://www.neogens.co/th-coffee-farmer.html",
                  "https://www.neogens.co/coffee-demo.html")


    # ประกาศให้ check.py รู้ว่าหน้านี้เป็นข้อมูลจำลองโดยเจตนา
    s = s.replace('<meta name="robots"',
                  '<meta name="ng-data" content="simulated">\n<meta name="robots"', 1)

    # hero
    m = re.search(r'<div class="kicker">.*?</div>\s*</div>\s*</header>', s, re.S)
    s = s[:m.start()] + (
        f'<div class="kicker">{HEAD["kicker"]}</div>\n'
        f'      <h1>{HEAD["h1"]}</h1>\n'
        f'      <p class="stand">{HEAD["stand"]}</p>\n'
        f'      <div class="meta"><span>Neo Gens</span><span>{HEAD["meta"]}</span>'
        f'<span><a href="coffee.html">The full argument</a></span></div>\n'
        f'    </div>\n  </div>\n</header>') + s[m.end():]

    # CSS
    s = s.replace("\n.dlab{", "\n" + CSS + ".dlab{")

    # เนื้อหา
    i, j = s.index("<article>"), s.index("</article>") + len("</article>")
    s = s[:i] + body() + s[j:]

    # บล็อกชวนเข้าร่วม
    s = re.sub(r'(<div class="k rv">)[^<]*(</div>)',
               r"\1Build the real one\2", s, count=1)
    s = re.sub(r'(<section class="join".*?<h2 class="rv">)[^<]*(</h2>)',
               r"\1This is a sketch. The real one needs contributors.\2",
               s, count=1, flags=re.S)
    s = re.sub(r'(<p class="lead rv">)[^<]*(</p>)',
               r"\1Leave your details if you want to put the first real data into it.\2",
               s, count=1)

    # ข้อมูลกับสคริปต์ ฝังไว้ในไฟล์ ไม่เรียก network ตอนเปิดหน้า
    payload = ('<script>window.__VAULT_DEMO__=' +
               json.dumps(DATA, ensure_ascii=False, separators=(",", ":")) +
               ";</script>\n<script>\n" + JS + "</script>\n")
    s = s.replace("</body>", payload + "</body>")

    OUT.write_text(s, encoding="utf-8")
    print(f"  สร้าง {OUT.name} · {len(s.encode()) // 1024} KB · "
          f"{DATA['grand']:,} ราย · {len(DATA['places'])} จุดบนแผนที่")


if __name__ == "__main__":
    main()
