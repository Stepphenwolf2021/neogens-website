# -*- coding: utf-8 -*-
"""
เนื้อหาหน้า "SEO คือการบริหารจัดการความรู้" สองภาษา

ข้อโต้แย้งของหน้านี้ — เนื้อหาคือช่องทางคุยกับคนที่เป็นกลุ่มเป้าหมาย SEO คือช่องทางคุยกับเครื่อง
ผ่านระบบค้นหา ให้เข้าใจว่าเราเป็นใคร ทำเรื่องอะไร เกี่ยวข้องกับสิ่งไหน เพื่อให้ถูกจับคู่กับคนที่ใช่
โดยไม่ต้องซื้อความสนใจแบบไร้ทิศทาง เว็บส่วนใหญ่ออกแบบบทสนทนาชุดแรกไว้ แล้วด้นสดชุดที่สอง
เพราะ SEO ถูกถามหลังจากโครงสร้างถูกตัดสินไปแล้ว จากนั้นจึงเล่าว่าเราออกแบบของเราอย่างไร
มีภาพเปรียบเทียบสองฝั่ง และปิดด้วยผลตรวจจริงจาก Rich Results Test ของ Google

ตัวเลขทุกตัวนับจากไฟล์จริง build_evidence.py นับใหม่ทุกครั้งที่รันและหยุดถ้าไม่ตรง
  43 หน้า 465 ข้อความ   นับจาก @graph ในทุกหน้าที่ไม่ใช่ทางเบี่ยง
  ศัพท์ 4 คำ            DefinedTerm ใน index.html
  ฟอนต์ 28 ไฟล์         assets/fonts/*.woff2
  ทางเบี่ยง 26 หน้า      หน้าที่มี http-equiv="refresh"
  ชนิดที่ประกาศไว้กี่หน้า  Organization 43 · BreadcrumbList 33 · TechArticle 5 · FAQPage 2

ผลตรวจในหน้านี้เป็นผลจริงที่ Noppadol รันเองเมื่อ 21 สิงหาคม 2026 สองหน้า
หน้าแรกได้ Organization และ th-mkm-for-coffee.html ได้ Breadcrumbs ทั้งคู่ไม่มี error ไม่มี warning
ห้ามเพิ่มบรรทัดในตารางนั้นถ้าไม่ได้รันจริง เพราะทั้งหน้าตั้งอยู่บนคำว่าตรวจสอบได้
"""

# ตัวเลขที่หน้านี้อ้าง และต้องตรงกับไฟล์จริงเสมอ build_evidence.py เป็นคนตรวจ
# 2026-09-01 ตัวเลขลดลงเพราะภาค 3 ถูกถอดออกจากเว็บ ดู .tools/pause_coffee.py
FACTS = {"pages": 39, "nodes": 380, "fonts": 28, "stubs": 24, "terms": 4,
         "org": 39, "crumbs": 29, "article": 5, "faq": 0}

# คำที่ใช้สะกดตัวเลขในเนื้อหา ด่านตรวจจะหาคำเหล่านี้ในหน้าที่สร้างเสร็จ
WORDS = {
    "en": {39: "thirty-nine", 380: "three hundred and eighty",
           28: "twenty-eight", 24: "twenty-four", 4: "four"},
    "th": {39: "สามสิบเก้า", 380: "สามร้อยแปดสิบ",
           28: "ยี่สิบแปด", 24: "ยี่สิบสี่", 4: "สี่"},
}
SPELLED = ("pages", "nodes", "fonts", "stubs", "terms")

# ประโยคที่อ้างจำนวนหน้าตามชนิดที่ประกาศไว้ ตรวจด้วยการประกอบประโยคจากค่าที่นับได้จริง
# แล้วหาในหน้าที่สร้างเสร็จ ถ้าเว็บโตขึ้นแล้วตัวเลขไม่ตรง ด่านนี้จะจับได้ทันที
CLAIMS = {
    "en": ["{crumbs} declare their position",
           "{article} are declared as articles",
           # 2026-09-01 หน้าที่มี FAQ อยู่ในภาค 3 ซึ่งถูกถอดออก ข้ออ้างนี้จึงพักไว้
           ],
    "th": ["{crumbs} หน้าประกาศตำแหน่งของตัวเอง",
           "{article} หน้าประกาศตัวเป็นบทความ",
           ],
}

UPDATED_EN = "21 August 2026"
UPDATED_TH = "21 สิงหาคม 2026"
TESTED_EN = "1 September 2026"
TESTED_TH = "1 กันยายน 2026"

# ---------------------------------------------------------------- ภาพเปรียบเทียบ
# โครงเดียวกันสามแถว ฝั่งซ้ายคือเว็บที่ไม่ได้ประกาศโครงสร้าง ฝั่งขวาคือเว็บที่ประกาศ
# ระบบค้นหาเป็นกล่องสีกลางทั้งสองฝั่ง เพราะมันคือตัวเดียวกัน ต่างกันที่สิ่งที่ไปถึงมัน
# ใช้คลาสชุดเดียวกับภาพในหน้า ontology-and-knowledge-graph.html ไม่ได้คิดชุดใหม่

def _svg(L):
    return f'''<svg class="dsvg" viewBox="0 0 900 400" role="img" aria-label="{L['aria']}">
      <text class="m-am" x="28" y="22">{L['lab_l']}</text>
      <text class="m-go" x="478" y="22">{L['lab_r']}</text>
      <path class="ln-gh" d="M450 34 V386"/>

      <rect class="bx" x="90" y="40" width="270" height="100" rx="12"/>
      <text class="t-s" x="108" y="64">{L['page']}</text>
      <path class="ln-gh" d="M108 84 H346"/>
      <path class="ln-gh" d="M108 100 H326"/>
      <path class="ln-gh" d="M108 116 H346"/>
      <path class="ln-gh" d="M108 132 H286"/>

      <rect class="bx-go" x="540" y="40" width="270" height="100" rx="12"/>
      <text class="t-s" x="558" y="64">{L['page']}</text>
      <path class="ln-gh" d="M558 84 H700"/>
      <path class="ln-gh" d="M558 100 H680"/>
      <path class="ln-gh" d="M558 116 H700"/>
      <path class="ln-gh" d="M558 132 H660"/>
      <text class="m-go" x="752" y="62" text-anchor="middle">JSON-LD</text>
      <path class="ln" d="M752 80 L728 116"/>
      <path class="ln" d="M752 80 L776 116"/>
      <path class="ln" d="M728 116 H776"/>
      <circle class="bx-go" cx="752" cy="80" r="9"/>
      <circle class="bx-go" cx="728" cy="116" r="9"/>
      <circle class="bx-go" cx="776" cy="116" r="9"/>

      <path class="ln" d="M225 140 V184"/>
      <path class="ln" d="M218 174 L225 186 L232 174"/>
      <rect class="bx" x="150" y="148" width="150" height="24" rx="6"/>
      <text class="m" x="225" y="164" text-anchor="middle">{L['chip_l']}</text>

      <path class="ln" d="M675 140 V184"/>
      <path class="ln" d="M668 174 L675 186 L682 174"/>
      <rect class="bx-as" x="600" y="148" width="150" height="24" rx="6"/>
      <text class="m-as" x="675" y="164" text-anchor="middle">schema.org</text>

      <rect class="bx" x="90" y="190" width="270" height="80" rx="12"/>
      <text class="t-b" x="225" y="216" text-anchor="middle">{L['engine']}</text>
      <text class="m" x="225" y="238" text-anchor="middle">{L['eng_l1']}</text>
      <text class="m" x="225" y="254" text-anchor="middle">{L['eng_l2']}</text>

      <rect class="bx" x="540" y="190" width="270" height="80" rx="12"/>
      <text class="t-b" x="675" y="216" text-anchor="middle">{L['engine']}</text>
      <text class="m" x="675" y="238" text-anchor="middle">{L['eng_r1']}</text>
      <text class="m" x="675" y="254" text-anchor="middle">{L['eng_r2']}</text>

      <path class="ln" d="M225 270 V302"/>
      <path class="ln" d="M218 292 L225 304 L232 292"/>
      <path class="ln" d="M675 270 V302"/>
      <path class="ln" d="M668 292 L675 304 L682 292"/>

      <rect class="bx" x="90" y="308" width="270" height="78" rx="12"/>
      <text class="t-b" x="225" y="334" text-anchor="middle">{L['out_l']}</text>
      <text class="m" x="225" y="356" text-anchor="middle">{L['out_l1']}</text>
      <text class="m" x="225" y="372" text-anchor="middle">{L['out_l2']}</text>

      <rect class="bx-go" x="540" y="308" width="270" height="78" rx="12"/>
      <text class="t-b" x="675" y="334" text-anchor="middle">{L['out_r']}</text>
      <text class="m" x="675" y="356" text-anchor="middle">{L['out_r1']}</text>
      <text class="m" x="675" y="372" text-anchor="middle">{L['out_r2']}</text>
    </svg>'''


def figure(lab, svg, cap):
    return (f'<figure class="rv">\n      <div class="dbox">\n'
            f'        <div class="dlab go">{lab}</div>\n        {svg}\n'
            f'      </div>\n      <figcaption>{cap}</figcaption>\n    </figure>')


FIG_EN = figure(
    "THE SAME SEARCH ENGINE, TWO DIFFERENT INPUTS",
    _svg({
        "aria": "A comparison in three rows. On the left, a page containing only lines of "
                "text sends plain text to a search engine, which can only guess what the "
                "organisation is, and the result is being matched by guesswork. On the "
                "right, the same page also carries a small JSON-LD graph, sends it in the "
                "shared schema.org vocabulary to the same search engine, which reads who "
                "the organisation is and what it works on, and the result is being matched "
                "for a reason.",
        "lab_l": "NO STRUCTURE DECLARED", "lab_r": "STRUCTURE DECLARED · ONTOLOGY-BASED",
        "page": "Your page", "chip_l": "PLAIN TEXT ONLY", "engine": "Search engine",
        "eng_l1": "Sees paragraphs. Cannot tell what",
        "eng_l2": "this organisation is or does.",
        "eng_r1": "Reads who you are, what you do,",
        "eng_r2": "what you connect to.",
        "out_l": "Matched by guesswork",
        "out_l1": "Reach has to be bought,",
        "out_l2": "and bought again each time.",
        "out_r": "Matched for a reason",
        "out_r1": "People looking for this find you,",
        "out_r2": "the description keeps working.",
    }),
    "<b>Illustrative.</b> The search engine is the same on both sides. What differs is what "
    "reaches it. Structured data does not make a page better — it makes the page legible as "
    "a thing, rather than only as prose.")

FIG_TH = figure(
    "ระบบค้นหาตัวเดียวกัน ได้รับของคนละอย่าง",
    _svg({
        "aria": "ภาพเปรียบเทียบสามแถว ฝั่งซ้าย หน้าเว็บที่มีแต่บรรทัดข้อความ "
                "ส่งข้อความล้วนไปยังระบบค้นหา ซึ่งได้แต่เดาว่าองค์กรนี้คืออะไร "
                "ผลคือถูกจับคู่แบบเดา ฝั่งขวา หน้าเว็บเดียวกันมีกราฟ JSON-LD ขนาดเล็กติดอยู่ด้วย "
                "ส่งไปด้วยคำศัพท์กลาง schema.org ไปยังระบบค้นหาตัวเดียวกัน "
                "ซึ่งอ่านได้ว่าองค์กรนี้เป็นใครและทำเรื่องอะไร ผลคือถูกจับคู่ด้วยเหตุผล",
        "lab_l": "เว็บที่ไม่ได้ประกาศโครงสร้าง", "lab_r": "เว็บที่ประกาศโครงสร้าง · ONTOLOGY-BASED",
        "page": "หน้าเว็บ", "chip_l": "ข้อความล้วน", "engine": "ระบบค้นหา",
        "eng_l1": "เห็นย่อหน้า แต่ไม่รู้ว่านี่คือ",
        "eng_l2": "องค์กรอะไร ต้องเดาเอาเอง",
        "eng_r1": "อ่านได้ว่าเป็นใคร ทำเรื่องอะไร",
        "eng_r2": "เกี่ยวข้องกับสิ่งไหน",
        "out_l": "ถูกจับคู่แบบเดา",
        "out_l1": "ต้องซื้อการมองเห็นเอา",
        "out_l2": "และจ่ายซ้ำทุกครั้ง",
        "out_r": "ถูกจับคู่ด้วยเหตุผล",
        "out_r1": "คนที่กำลังหาสิ่งนี้ หาเจอเอง",
        "out_r2": "คำอธิบายเดิมใช้ได้ต่อไป",
    }),
    "<b>ภาพประกอบ</b> ระบบค้นหาเป็นตัวเดียวกันทั้งสองฝั่ง ต่างกันที่สิ่งที่ไปถึงมัน "
    "ข้อมูลที่มีโครงสร้างไม่ได้ทำให้หน้าดีขึ้น แต่ทำให้หน้ากลายเป็นสิ่งที่เครื่องอ่านออกว่าเป็นอะไร "
    "ไม่ใช่แค่กองข้อความ")

# ---------------------------------------------------------------- ตารางผลตรวจ
# สองแถวนี้คือผลจริงที่รันเมื่อ 21 สิงหาคม 2026 ห้ามเติมแถวที่ไม่ได้รันจริง


def report(lab, head, rows, cap):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(
        f'<td class="rr-ok">{c[1:]}</td>' if c.startswith("~") else f"<td>{c}</td>"
        for c in r) + "</tr>" for r in rows)
    return (f'<figure class="rv">\n      <div class="dbox">\n'
            f'        <div class="dlab go">{lab}</div>\n'
            f'        <div class="rr-scroll"><table class="rr">'
            f"<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>\n"
            f'      </div>\n      <figcaption>{cap}</figcaption>\n    </figure>')


RR_EN = report(
    f"GOOGLE RICH RESULTS TEST · {TESTED_EN}",
    ["Address tested", "Item detected", "Result"],
    [["www.neogens.co", "Organization",
      "~Valid · 0 errors · 2 non-critical"]],
    "One page, run on Google's public tool. Valid with no errors. The two non-critical "
    "notes are optional address fields we have chosen not to publish — postalCode and "
    "streetAddress. Anyone can repeat the row in about thirty seconds without asking us "
    "for anything, which is the point of quoting it.")

RR_TH = report(
    f"ผลตรวจจาก GOOGLE RICH RESULTS TEST · {TESTED_TH}",
    ["ที่อยู่ที่ทดสอบ", "สิ่งที่ตรวจพบ", "ผล"],
    [["www.neogens.co", "Organization",
      "~ผ่าน · 0 ข้อผิดพลาด · 2 ข้อสังเกตที่ไม่ร้ายแรง"]],
    "หนึ่งหน้า รันด้วยเครื่องมือสาธารณะของ Google ผ่าน ไม่มีข้อผิดพลาด "
    "ส่วนข้อสังเกตสองข้อคือช่องที่อยู่ซึ่งไม่บังคับ และเราเลือกที่จะไม่เผยแพร่ "
    "คือรหัสไปรษณีย์กับที่อยู่ตามถนน ใครก็ทำซ้ำแถวนี้ได้ในเวลาประมาณสามสิบวินาที "
    "โดยไม่ต้องขออะไรจากเรา ซึ่งเป็นเหตุผลเดียวที่หยิบมาอ้าง")

# ---------------------------------------------------------------- เนื้อหา

# ---------------------------------------------------------------- ภาพเปรียบเทียบ
# เพิ่มเมื่อ 2026-09-01 ตามที่ Noppadol สั่ง  เทียบ SEO แบบเดิม กับ ontology-based SEO
# ไม่มี marker ลูกศรในหน้านี้ จึงใช้เส้นล้วน  เส้นประ = เครื่องเดาเอง  เส้นทึบ = ประกาศไว้
# ใช้คลาสเดิมทั้งหมด .bx .bx-go .bx-as .ln .ln-gh .t-b .t-s .m .m-go ไม่ได้ตั้งชื่อใหม่
_CMP_TEXT = {
    "en": dict(
        lab_l="CONVENTIONAL SEO", lab_r="ONTOLOGY-DRIVEN SEO",
        page="Page", sub_l="words", sub_r="statements",
        chips=("ontology", "museum", "AI"),
        engine="Search", engine_sub="infers",
        aria="Conventional SEO compared with ontology-driven SEO",
        cap_l="Meaning is left for the machine to infer from the words on the page.",
        cap_r="Every thing has an identifier and every relation is written down.",
        figcap="<b>Two ways to be read by a machine.</b> On the left the meaning is guessed "
               "from words. On the right it is declared, and can be checked. Illustrative."),
    "th": dict(
        lab_l="SEO แบบทั่วไป", lab_r="ONTOLOGY-DRIVEN SEO",
        page="หน้าเว็บ", sub_l="มีแต่คำ", sub_r="มีข้อความที่ประกาศไว้",
        chips=("ออนโทโลยี", "พิพิธภัณฑ์", "AI"),
        engine="ระบบค้นหา", engine_sub="เดาเอง",
        aria="เทียบ SEO แบบทั่วไป กับ ontology-driven SEO",
        cap_l="ความหมายและความสัมพันธ์ ปล่อยให้เครื่องเดาเอาเองจากคำบนหน้า",
        cap_r="ทุกสิ่งมีตัวระบุของตัวเอง และทุกความสัมพันธ์ถูกเขียนลงไป",
        figcap="<b>สองวิธีที่เครื่องจะอ่านหน้าเว็บ</b> ด้านซ้าย ความหมายมาจากการเดาจากคำ "
               "ด้านขวา ความหมายถูกประกาศไว้และตรวจสอบได้ เป็นภาพประกอบ"),
}


def _cmp_fig(lang):
    t = _CMP_TEXT[lang]
    c1, c2, c3 = t["chips"]
    nodes = ("Organization", "Service", "DefinedTerm")
    edges = ("publisher", "provider", "about")
    chips = "".join(
        f'<rect class="bx" x="196" y="{y}" width="118" height="38" rx="9"/>'
        f'<text class="t-s" x="255" y="{y+24}" text-anchor="middle">{c}</text>'
        for y, c in zip((62, 122, 182), (c1, c2, c3)))
    dashes = "".join(
        f'<path class="ln-gh" d="M314 {y+19} L352 145"/>' for y in (62, 122, 182))
    rnodes = "".join(
        f'<rect class="bx" x="672" y="{y}" width="132" height="42" rx="9"/>'
        f'<text class="t-s" x="738" y="{y+26}" text-anchor="middle">{n}</text>'
        f'<path class="ln" d="M628 {y+21} L672 {y+21}"/>'
        f'<text class="m-go" x="650" y="{y+15}" text-anchor="middle">{e}</text>'
        for y, n, e in zip((60, 122, 184), nodes, edges))
    return f'''<figure class="rv">
      <div class="dbox">
        <div class="dlab go">{t["lab_l"]} · {t["lab_r"]}</div>
        <svg class="dsvg" viewBox="0 0 900 300" role="img"
             aria-label="{t['aria']}">
          <text class="m" x="16" y="22">{t["lab_l"]}</text>
          <rect class="bx" x="16" y="60" width="140" height="164" rx="12"/>
          <text class="t-b" x="86" y="134" text-anchor="middle">{t["page"]}</text>
          <text class="t-s" x="86" y="156" text-anchor="middle">{t["sub_l"]}</text>
          {chips}
          {dashes}
          <rect class="bx-as" x="352" y="112" width="96" height="66" rx="12"/>
          <text class="t-b" x="400" y="142" text-anchor="middle">{t["engine"]}</text>
          <text class="t-s" x="400" y="162" text-anchor="middle">{t["engine_sub"]}</text>
          <text class="t-s" x="16" y="262">{t["cap_l"]}</text>

          <path class="ln-gh" d="M474 16 L474 284"/>

          <text class="m-go" x="490" y="22">{t["lab_r"]}</text>
          <rect class="bx-go" x="490" y="60" width="138" height="164" rx="12"/>
          <text class="t-b" x="559" y="134" text-anchor="middle">{t["page"]}</text>
          <text class="t-s" x="559" y="156" text-anchor="middle">{t["sub_r"]}</text>
          {rnodes}
          <text class="t-s" x="490" y="262">{t["cap_r"]}</text>
        </svg>
      </div>
      <figcaption>{t["figcap"]}</figcaption>
    </figure>'''


EN = {
    "src": "coffee-farmer.html",
    "out": "seo-as-knowledge-management.html",
    "twin": "th-seo-as-knowledge-management.html",
    "lang": "en",
    "title": "SEO as knowledge management — Neo Gens",
    "desc": "Content speaks to people. SEO speaks to software. How we designed ours as "
            "ontology-driven SEO from day one, and what the test reports.",
    "kicker": "Evidence",
    "toc_label": "Contents",
    "toc_head": "In this piece",
    "h1": "Content speaks to people.<br>SEO speaks to software.<br>All of it is Modern Knowledge Management.",
    "stand": "Most websites are designed for the first conversation and improvised for the "
             "second. This is how we designed ours as ontology-driven SEO from day one.",
    "meta": f"updated {UPDATED_EN}",
    "body": [
        ("h2", "Most sites are written for one reader and read by two"),
        ("p", "Almost every website is commissioned the same way. Someone settles the "
              "structure, someone writes the copy, someone designs the pages. Then, near the "
              "end, somebody asks about SEO. A few titles are rewritten, a plugin is "
              "installed, a list of keywords is handed over, and the site goes live."),
        ("p", "By then the structure has already been decided, and the structure was the part "
              "that mattered. What launches is a site that reads well and cannot be read: "
              "nothing in it states what the organisation is, which field it works in, how "
              "its pages relate to one another, or which of its words are being used in a "
              "specific sense. A person infers all of that in seconds. A machine cannot infer "
              "it at all."),
        ("p", "The cause is order, not effort. The question arrived after the decisions it "
              "should have shaped."),

        ("h2", "Content speaks to people. SEO speaks to computers."),
        ("p", "We think of a website as two conversations sharing one file. The content is "
              "the conversation with the people we want to reach — the argument, the tone, "
              "the examples, the things worth disagreeing with. SEO is the conversation with "
              "the computers standing between us and those people: who we are, what we work "
              "on, what we are connected to."),
        ("p", "What you prepare for that second conversation is read by a crawler — Google's "
              "and everyone else's — which records it in an index, and that index is how "
              "people looking for what you hold arrive at you. The crawler makes one pass. "
              "If it comes away without an answer it does not return to check. That single "
              "pass is the chance to say what you hold, how it connects, and how far it can "
              "be trusted."),
        ("p", "Doing it properly is what lets the right people find you for a reason. An "
              "organisation that has described itself accurately to a machine gets matched to "
              "the people looking for exactly that. The alternative is buying attention "
              "without direction — paying to appear in front of people who do not want you, "
              "again and again, for as long as the budget lasts. That cost repeats every "
              "time. An accurate description of what you are does not."),

        ("h2", "How we designed ours: ontology-driven SEO"),
        ("p", "Most SEO work starts from keywords: guess the phrases people type, then bend "
              "the pages toward them. It treats a search engine as a lock to be picked."),
        ("p", "We started at the other end, by describing what actually exists — the things, "
              "and the relations between them. That is an ontology, and it is the same kind of "
              "material we build with clients. The difference is only that here the vocabulary "
              "was set by search engines rather than by a web team or a curatorial one. That "
              "vocabulary is schema.org: a shared dictionary of types and relations that the "
              "major search engines agreed on, so that a statement written once is understood "
              "the same way by all of them. Follow the structure schema.org already gives you "
              "and every search engine can find you, without buying expensive keywords."),
        ("raw", _cmp_fig("en")),
        ("p", "In practice: the organisation has one identifier, declared once and referenced "
              "from every page. Each of the four terms this site uses in a specific sense has "
              "its own identifier and points at the page that defines it. The practice area we "
              "run is declared as a service pointing back to the same provider, and every "
              "page states which of those things it is about."),
        ("p", "The Thai and English versions of a page declare each other as one work "
              "written in two languages, not two pages that happen to resemble each other. "
              "Across the site that comes to three hundred and eighty declarations in "
              "thirty-nine pages."),
        ("p", "Around that: an address for every page that says what the page is, twenty-four "
              "redirects so that every link ever shared still arrives, and twenty-eight "
              "typeface files and every stylesheet served from this domain, so that reading a "
              "page contacts nobody but us."),
        ("raw", FIG_EN),
        ("p", "The reason to prefer this to keyword work is that it does not expire. Ranking "
              "formulas change every year, and tactics built for one are worth nothing under "
              "the next. A true description of what an organisation is does not go out of "
              "date when the formula changes — and it is the same form that AI assistants "
              "read, which is where a growing share of people now put their questions."),

        ("h2", "Whether a machine can actually read it, you can check yourself"),
        ("p", "None of the above is worth anything as a claim. Google publishes a free tool, "
              "the Rich Results Test, which takes any address, fetches the page the way its "
              "crawler would, and reports back exactly which structured items it found and "
              "whether each one is valid. It is the closest thing there is to an outside "
              "reading of what a site says about itself."),
        ("raw", RR_EN),
        ("p", "Across the whole site, thirty-nine pages declare the organisation, 29 declare "
              "their position in the navigation and 5 are declared as articles. "
              "Those numbers are counted from the files at build time, "
              "not typed in by hand — if a page loses its graph, the build stops."),

        ("h2", "What passing buys, and what failing costs"),
        ("p", "Passing is not a ranking boost, and anyone who tells you otherwise is selling "
              "something. What it buys is narrower: the search engine stops inferring and "
              "starts quoting. Your organisation becomes one identified thing rather than a "
              "name that happens to appear in some text; your pages can be shown with their "
              "path, their author, their questions and answers; and the same declarations are "
              "what an AI assistant reads when someone asks it a question in your field."),
        ("p", "Failing is worse than it looks, because of how quietly it happens. An item with "
              "an error is not shown with a red mark — it is dropped. The page still looks "
              "perfect to a person, still loads, still reads well, and simply is not "
              "considered for anything it declared. Nobody writes to tell you. A warning is "
              "the softer version: the item is kept but loses the features it did not qualify "
              "for."),
        ("p", "The deeper cost is trust that spreads. A declaration a machine cannot confirm "
              "does not only lose its own page. When two pages name each other as "
              "translations and only one of them agrees, a search engine stops trusting that "
              "kind of statement across the whole domain. One unverifiable claim quietly "
              "discounts the true ones next to it — which is the same reason a catalogue with "
              "unreliable records is worth less than its accurate half."),
        ("p", "So we treat the test as a condition of publishing rather than a badge to "
              "collect. Every page on this site is built by a script that refuses to write "
              "the file if the structure it declares does not match what the page actually "
              "shows a reader."),

        ("h2", "What the site actually got out of it"),
        ("p", "What changed is not rank. It is what a machine knows about us without having "
              "to guess. Every page can say what it is about, where it sits in the site, and "
              "what it relates to. Search results show the page's path instead of a long "
              "address, and an AI assistant reading the page gets the same declarations a "
              "person sees, rather than prose it has to interpret."),
        ("p", "The longer-lived advantage is that none of it expires. Keyword tactics have to "
              "be rebuilt every time the ranking formula moves. A truthful description of what "
              "an organisation is stays true, and we have never paid for a single keyword."),
        ("p", "For a knowledge management practice there is a further point: this site is a "
              "checkable example of the thing we sell. We are not saying structure matters "
              "and then leaving our own structure to chance."),
        ("p", "If you want to know where your own organisation stands, you can check it "
              "yourself. Google's Rich Results Test lives at "
              "search.google.com/test/rich-results — no account, nothing to install. Paste "
              "your home page address and run it. It takes about thirty seconds."),
        ("p", "The line worth reading is not pass or fail. It is the line that says what was "
              "detected. If nothing was detected, your site has not said anything to a machine "
              "at all, however well people read it. That gap is what this whole piece is "
              "about."),
    ],
    "join_k": "The same method",
    "join_h": "Curious what this looks like applied to a collection rather than a website?",
    "join_p": "Leave your details and we will show you the working, not the summary.",
}

TH = {
    "src": "th-coffee-farmer.html",
    "out": "th-seo-as-knowledge-management.html",
    "twin": "seo-as-knowledge-management.html",
    "lang": "th",
    "title": "SEO คือการบริหารจัดการความรู้ — Neo Gens",
    "desc": "เนื้อหาใช้สื่อสารกับคน SEO ใช้สื่อสารกับซอฟต์แวร์ "
            "เราออกแบบเว็บของเราให้เป็น ontology-driven SEO ตั้งแต่วันแรก และผลตรวจบอกอะไร",
    "kicker": "หลักฐาน",
    "toc_label": "สารบัญ",
    "toc_head": "ในบทความนี้",
    "h1": "เนื้อหาใช้สื่อสารกับคน<br>SEO ใช้สื่อสารกับซอฟต์แวร์<br>งานทั้งหมดคือการบริหารจัดการความรู้สมัยใหม่",
    "stand": "เว็บส่วนใหญ่ออกแบบมาเพื่อบทสนทนาชุดแรก แล้วค่อยมาด้นสดเอากับบทสนทนาชุดที่สอง "
             "หน้านี้คือวิธีที่เราออกแบบเว็บของเราให้เป็น ontology-driven SEO ตั้งแต่วันแรก",
    "meta": f"ปรับปรุง {UPDATED_TH}",
    "body": [
        ("h2", "เว็บส่วนใหญ่เขียนไว้ให้ผู้อ่านแบบเดียว"),
        ("p", "เว็บเกือบทุกเว็บเกิดขึ้นแบบเดียวกัน มีคนตัดสินใจโครงสร้าง มีคนเขียนเนื้อหา "
              "มีคนออกแบบหน้า แล้วตอนใกล้เสร็จจึงมีคนถามขึ้นมาว่า แล้ว SEO ล่ะ "
              "จากนั้นชื่อหน้าถูกเขียนใหม่ไม่กี่หน้า ติดปลั๊กอินสักตัว "
              "ส่งรายการคำค้นมาให้ชุดหนึ่ง แล้วเว็บก็ขึ้นสู่สายตาสาธารณชน"),
        ("p", "ถึงตอนนั้นโครงสร้างถูกตัดสินไปเรียบร้อยแล้ว และโครงสร้างคือส่วนที่สำคัญที่สุด "
              "สิ่งที่ได้จึงเป็นเว็บที่คนอ่านได้ แต่ระบบค้นหาอ่านไม่เข้าใจ "
              "ไม่มีอะไรในโครงสร้างนั้นบอกว่าองค์กรนี้คืออะไร ทำงานอยู่ในสาขาไหน "
              "หน้าแต่ละหน้าเกี่ยวข้องกันอย่างไร หรือคำไหนในเว็บที่ใช้ในความหมายเฉพาะ "
              "คนอ่านอนุมานทั้งหมดนี้ได้ในไม่กี่วินาที เครื่องอนุมานไม่ได้เลยสักอย่าง"),
        ("p", "สาเหตุอยู่ที่ลำดับการทำงาน ไม่ได้อยู่ที่ความตั้งใจ "
              "คำถามเรื่อง SEO มาถึงหลังจากการตัดสินใจที่มันควรมีส่วนกำหนดผ่านไปหมดแล้ว"),

        ("h2", "เนื้อหาคุยกับคน ข้อมูล SEO คุยกับคอมพิวเตอร์"),
        ("p", "เรามองว่าเว็บหนึ่งเว็บมีบทสนทนาสองชุดอยู่ในนั้น "
              "เนื้อหาที่แสดงบนหน้าเว็บคือบทสนทนากับคนที่เราอยากสื่อสารด้วย "
              "ส่วนข้อมูล SEO คือบทสนทนากับระบบค้นหาที่ยืนอยู่ตรงกลางระหว่างเรากับคนเหล่านั้น "
              "เป็นการประกาศว่าเราเป็นใคร ทำงานเรื่องอะไร และเกี่ยวข้องกับสิ่งไหนบ้าง"),
        ("p", "ข้อมูล SEO ที่เราเตรียมไว้ มีไว้ให้บอตของระบบค้นหาอย่าง Google "
              "เข้ามาอ่านแล้วบันทึกลงระบบของเขา เว็บของเราจึงถูกค้นเจอ "
              "ตอนที่มีคนกำลังต้องการสิ่งที่เรามี บอตเข้ามาอ่านรอบเดียว "
              "ถ้าอ่านแล้วไม่ได้คำตอบ มันไม่ย้อนกลับมาตรวจซ้ำให้ "
              "โอกาสรอบเดียวนั้นคือโอกาสที่จะบอกว่าคุณถืออะไรอยู่ อะไรเชื่อมกับอะไร "
              "และเชื่อถือได้แค่ไหน"),
        ("p", "ทำให้ถูกแล้วคนที่ใช่จะหาเราเจอด้วยเหตุผลที่สมเหตุสมผล "
              "องค์กรที่อธิบายตัวเองกับเครื่องไว้ตรงกับความจริง "
              "จะถูกจับคู่กับคนที่กำลังมองหาสิ่งนั้นพอดี "
              "ทางเลือกอีกทางคือซื้อความสนใจแบบไร้ทิศทาง "
              "จ่ายเงินไปโผล่ต่อหน้าคนที่ไม่ได้ต้องการเรา ซ้ำแล้วซ้ำเล่า "
              "นานเท่าที่งบยังมีอยู่ ค่าใช้จ่ายแบบนั้นเกิดซ้ำทุกครั้ง "
              "คำอธิบายที่ตรงกับความจริงว่าเราเป็นอะไร ไม่ต้องจ่ายซ้ำ"),

        ("h2", "SEO ของเราออกแบบอย่างไร — ontology-driven SEO"),
        ("p", "งาน SEO ส่วนใหญ่เริ่มจากคำค้น เดาว่าคนพิมพ์อะไร "
              "แล้วดัดหน้าเว็บเข้าหาคำเหล่านั้น "
              "วิธีนี้มองระบบค้นหาเป็นกุญแจที่ต้องหาทางสะเดาะ"),
        ("p", "เราเริ่มจากอีกด้าน คือเขียนให้ชัดว่าองค์กรนี้มีอะไรอยู่บ้าง "
              "และแต่ละอย่างเกี่ยวกันอย่างไร นั่นคือ ontology "
              "และเป็นข้อมูลชนิดเดียวกับที่เราสร้างร่วมกับลูกค้า "
              "ต่างกันตรงที่คำศัพท์ชุดนี้ระบบค้นหาเป็นคนกำหนด "
              "ไม่ใช่ทีมพัฒนาเว็บ หรือภัณฑารักษ์ "
              "คำศัพท์ชุดนั้นชื่อ schema.org "
              "เป็นพจนานุกรมกลางของชนิดและความสัมพันธ์ที่ระบบค้นหารายใหญ่ตกลงกันไว้ "
              "เขียนครั้งเดียว ทุกรายอ่านเข้าใจตรงกัน "
              "ดังนั้น ถ้าเราทำตามโครงสร้างที่มีอยู่ใน schema.org "
              "ระบบค้นหาทุกตัวก็จะหาเราเจอ โดยไม่ต้องเสียเงินซื้อ keyword ราคาแพง"),
        ("raw", _cmp_fig("th")),
        ("p", "ในทางปฏิบัติ องค์กรมีตัวระบุตัวเดียว ประกาศครั้งเดียวแล้วให้ทุกหน้าอ้างถึง "
              "ศัพท์สี่คำที่เว็บนี้ใช้ในความหมายเฉพาะ แต่ละคำมีตัวระบุของตัวเอง "
              "และชี้ไปยังหน้าที่นิยามมันไว้จริง "
              # 2026-09-01 ภาค 3 ถูกถอดออก เหลือสายงานเดียว ประโยคเดิมเขียนว่าสองสาย จึงไม่จริงแล้ว
              "สายงานที่เปิดอยู่ประกาศตัวเป็นบริการ ที่ชี้กลับมาที่ผู้ให้บริการรายเดียวกัน "
              "และทุกหน้าบอกว่าตัวเองพูดถึงสิ่งไหนในนั้น"),
        ("p", "หน้าเดียวกันฉบับไทยกับฉบับอังกฤษ ประกาศว่าเป็นงานชิ้นเดียวที่เขียนไว้สองภาษา "
              "ไม่ใช่คนละหน้าที่บังเอิญเนื้อหาคล้ายกัน "
              "นับรวมทั้งเว็บแล้วเป็นคำประกาศสามร้อยแปดสิบชิ้น ในสามสิบเก้าหน้า"),
        ("p", "รอบ ๆ นั้นคือที่อยู่ของทุกหน้าที่บอกได้เองว่าหน้านั้นเป็นเรื่องอะไร "
              "ทางเบี่ยงยี่สิบสี่เส้นที่ทำให้ลิงก์เก่าทุกเส้นยังไปถึงปลายทาง "
              "ไฟล์ฟอนต์ยี่สิบแปดไฟล์และสไตล์ทั้งหมดเสิร์ฟจากโดเมนนี้ "
              "เปิดหน้าเว็บนี้แล้วไม่ได้ติดต่อใครนอกจากเรา"),
        ("raw", FIG_TH),
        ("p", "ที่เลือกวิธีนี้แทนการไล่ตามคำค้น เพราะมันไม่หมดอายุ "
              "สูตรจัดอันดับเปลี่ยนทุกปี เทคนิคที่สร้างมาเพื่อสูตรหนึ่งใช้กับสูตรถัดไปไม่ได้ "
              "แต่คำอธิบายที่ตรงกับความจริงว่าองค์กรนี้เป็นอะไร ไม่ล้าสมัยตามสูตร "
              "และเป็นรูปแบบเดียวกับที่ผู้ช่วย AI อ่าน "
              "ซึ่งเป็นที่ที่คนเอาคำถามไปถามมากขึ้นทุกปี"),

        ("h2", "เครื่องอ่านได้จริงหรือเปล่า ตรวจเองได้"),
        ("p", "ทุกอย่างข้างบนไม่มีน้ำหนักเลยถ้าเป็นแค่คำกล่าวอ้าง "
              "Google เปิดเครื่องมือฟรีตัวหนึ่งชื่อ Rich Results Test "
              "ใส่ที่อยู่หน้าไหนก็ได้ มันจะดึงหน้านั้นมาแบบเดียวกับที่บอตของมันทำ "
              "แล้วรายงานกลับมาว่าเจอข้อมูลที่มีโครงสร้างอะไรบ้าง และแต่ละชิ้นใช้ได้หรือไม่ "
              "นี่คือสิ่งที่ใกล้เคียงที่สุดกับการให้คนนอกอ่านว่าเว็บหนึ่งพูดถึงตัวเองว่าอย่างไร"),
        ("raw", RR_TH),
        ("p", "ทั้งเว็บ สามสิบเก้าหน้าประกาศตัวองค์กร "
              "29 หน้าประกาศตำแหน่งของตัวเองในเส้นทางนำทาง และ 5 หน้าประกาศตัวเป็นบทความ "
              "ตัวเลขเหล่านี้นับจากไฟล์ตอนสร้างหน้า ไม่ได้พิมพ์มือ "
              "ถ้าหน้าไหนกราฟหาย กระบวนการสร้างจะหยุดทันที"),

        ("h2", "ผ่านแล้วได้อะไร ไม่ผ่านแล้วเสียอะไร"),
        ("p", "ผ่านการตรวจไม่ได้แปลว่าอันดับดีขึ้น ใครบอกว่าใช่คือกำลังขายของ "
              "สิ่งที่ได้แคบกว่านั้นมาก คือระบบค้นหาเลิกเดา "
              "แล้วหันมาอ้างสิ่งที่เราเขียนไว้แทน "
              "องค์กรกลายเป็นสิ่งที่ระบุตัวได้ ไม่ใช่ชื่อที่บังเอิญโผล่อยู่ในข้อความ "
              "หน้าเว็บถูกแสดงพร้อมเส้นทาง ผู้เขียน หรือคำถามคำตอบได้ "
              "และคำประกาศชุดเดียวกันนี้คือสิ่งที่ผู้ช่วย AI อ่าน "
              "เวลามีคนถามคำถามในสาขาที่เราทำงานอยู่"),
        ("p", "การไม่ผ่านหนักกว่าที่เห็น เพราะมันเงียบ "
              "ข้อมูลที่มีข้อผิดพลาดไม่ได้ขึ้นเครื่องหมายสีแดงให้ใครเห็น มันถูกทิ้งไปเฉย ๆ "
              "หน้ายังดูสมบูรณ์สำหรับคน ยังโหลดขึ้น ยังอ่านรื่น "
              "เพียงแต่ไม่ถูกนับในเรื่องที่มันประกาศไว้เลย และไม่มีใครเขียนมาบอก "
              "ส่วนคำเตือนคือฉบับเบากว่า ข้อมูลยังอยู่ "
              "แต่เสียคุณสมบัติที่มันไม่ผ่านเกณฑ์ไป"),
        ("p", "ราคาที่แพงกว่านั้นคือความไว้ใจที่ลามข้ามหน้า "
              "คำประกาศที่เครื่องยืนยันไม่ได้ ไม่ได้เสียแค่หน้าตัวเอง "
              "สองหน้าอ้างว่าเป็นฉบับแปลของกันและกัน แต่มีหน้าเดียวที่ยืนยันกลับ "
              "ระบบค้นหาก็เลิกเชื่อคำประกาศชนิดนั้นทั้งโดเมน "
              "คำอ้างที่ตรวจไม่ได้หนึ่งข้อ ดึงน้ำหนักของข้อที่จริงข้าง ๆ ลงไปด้วย "
              "เหมือนทะเบียนที่มีระเบียนเชื่อถือไม่ได้ปนอยู่ "
              "ทั้งเล่มมีค่าน้อยกว่าครึ่งที่ถูกต้องของมันเอง"),
        ("p", "เราจึงถือว่าการตรวจนี้เป็นเงื่อนไขของการปล่อยหน้า ไม่ใช่เหรียญเอาไว้สะสม "
              "ทุกหน้าบนเว็บนี้สร้างด้วยสคริปต์ที่จะไม่ยอมเขียนไฟล์ "
              "ถ้าโครงสร้างที่มันประกาศ ไม่ตรงกับสิ่งที่ผู้อ่านเห็นจริงบนหน้า"),

        ("h2", "แล้วเว็บนี้ได้อะไรขึ้นมาจริง ๆ"),
        ("p", "สิ่งที่เปลี่ยนไปไม่ใช่อันดับ แต่คือสิ่งที่เครื่องรู้เกี่ยวกับเราโดยไม่ต้องเดา "
              "ทุกหน้าบอกได้เองว่าตัวเองเป็นเรื่องอะไร อยู่ตรงไหนของเว็บ และเกี่ยวกับสิ่งไหน "
              "ผลค้นหาจึงแสดงเส้นทางของหน้าแทนที่อยู่ยาว ๆ "
              "และผู้ช่วย AI ที่เข้ามาอ่าน ได้คำประกาศชุดเดียวกับที่คนเห็น "
              "ไม่ใช่ข้อความที่มันต้องตีความเอาเอง"),
        ("p", "ข้อได้เปรียบที่ยาวกว่านั้นคือมันไม่หมดอายุ "
              "เทคนิคไล่ตามคำค้นต้องรื้อใหม่ทุกครั้งที่สูตรจัดอันดับเปลี่ยน "
              "ส่วนคำอธิบายว่าองค์กรนี้เป็นอะไร ยังจริงอยู่เท่าเดิม "
              "และเราไม่เคยจ่ายเงินซื้อคำค้นสักคำเดียว"),
        ("p", "ที่สำคัญกว่านั้นสำหรับสำนักที่ปรึกษาด้านการบริหารจัดการความรู้ "
              "คือเว็บนี้เป็นตัวอย่างที่ตรวจได้ของสิ่งที่เราขาย "
              "เราไม่ได้บอกว่าโครงสร้างสำคัญ แล้วปล่อยเว็บของตัวเองไว้เฉย ๆ"),
        ("p", "ถ้าอยากรู้ว่าเว็บขององค์กรคุณอยู่ตรงไหน ลองเอาไปตรวจดูเองได้ "
              "เครื่องมือชื่อ Rich Results Test ของ Google "
              "อยู่ที่ search.google.com/test/rich-results "
              "ไม่ต้องสมัคร ไม่ต้องติดตั้งอะไร "
              "วางที่อยู่หน้าแรกขององค์กรลงไปแล้วกดทดสอบ ใช้เวลาประมาณสามสิบวินาที"),
        ("p", "สิ่งที่ควรดูไม่ใช่คำว่าผ่านหรือไม่ผ่าน แต่คือบรรทัดที่บอกว่ามันตรวจพบอะไร "
              "ถ้าไม่พบอะไรเลย แปลว่าเว็บขององค์กรคุณยังไม่ได้พูดอะไรกับเครื่องสักคำ "
              "ทั้งที่คนอ่านเข้าใจมันได้ดี นั่นคือระยะห่างที่หน้านี้ทั้งหน้าพูดถึง"),
    ],
    "join_k": "วิธีเดียวกัน",
    "join_h": "อยากเห็นวิธีนี้ตอนใช้กับคอลเลกชัน ไม่ใช่กับเว็บไซต์",
    "join_p": "ทิ้งรายละเอียดไว้ แล้วเราจะพาดูร่องรอยการทำงาน ไม่ใช่บทสรุป",
}

# ---------------------------------------------------------------- CSS ของภาพและตาราง
# คลาสภาพยกมาจากหน้า ontology-and-knowledge-graph.html เพื่อให้ภาพในเว็บนี้หน้าตาชุดเดียวกัน
# ฉบับไทยเปลี่ยนฟอนต์ในภาพเป็น IBM Plex Sans Thai และดันขนาดตัวอักษรเล็กขึ้นเล็กน้อย
# ห้ามใช้ letter-spacing ติดลบกับกฎที่มีข้อความไทย

_CSS_COMMON = """
/* --- ภาพเปรียบเทียบและตารางผลตรวจ --- */
/* แม่แบบ coffee-farmer มีแค่ .figplate figcaption ไม่มีกฎ figure/figcaption เปล่า ๆ
   ภาพในหน้านี้ไม่ได้อยู่ใน .figplate คำบรรยายจึงต้องมีกฎของตัวเอง ไม่งั้นตกไปใช้ขนาดตัวเนื้อ */
figure{margin:clamp(34px,4.5vw,56px) 0 0}
figure svg{max-width:100%;height:auto}
figcaption b{color:var(--dim);font-weight:600}
.dbox{border:1px solid var(--line);border-radius:16px;background:var(--surface);
  padding:clamp(16px,2.6vw,26px)}
.dlab{font-family:var(--mono);font-size:10.5px;text-transform:uppercase;margin-bottom:14px}
.dlab.go{color:var(--go)}
.dsvg{width:100%;height:auto;display:block}
.bx{fill:var(--surface-2);stroke:var(--line-2);stroke-width:1}
.bx-go{fill:var(--go-soft);stroke:var(--go);stroke-width:1.3}
.bx-as{fill:rgba(var(--ask-rgb),.07);stroke:rgba(var(--ask-rgb),.5);stroke-width:1.2}
.ln{stroke:var(--line-2);stroke-width:1;fill:none}
.ln-gh{stroke:var(--line);stroke-width:1;fill:none;stroke-dasharray:4 4}
.rr-scroll{overflow-x:auto}
.rr{width:100%;border-collapse:collapse;font-family:var(--mono);font-size:11.5px}
.rr th{text-align:left;font-weight:400;color:var(--mute);font-size:10px;
  text-transform:uppercase;padding:0 16px 10px 0;border-bottom:1px solid var(--line);
  white-space:nowrap}
.rr td{padding:12px 16px 12px 0;border-bottom:1px solid var(--line);color:var(--dim);
  vertical-align:top}
.rr tbody tr:last-child td{border-bottom:0}
.rr td.rr-ok{color:var(--go);white-space:nowrap}
"""

CSS = {
    "en": _CSS_COMMON + """
figcaption{font-family:var(--mono);font-size:11.5px;line-height:1.65;color:var(--mute);
  margin-top:14px;max-width:66ch}
.dlab{letter-spacing:.13em}
.t-b{font-family:'Inter',sans-serif;font-size:14px;fill:var(--fg);font-weight:600}
.t-s{font-family:'Inter',sans-serif;font-size:11.5px;fill:var(--dim)}
.m{font-family:'JetBrains Mono',monospace;font-size:8.5px;fill:var(--mute);letter-spacing:.1em}
.m-go{font-family:'JetBrains Mono',monospace;font-size:8.5px;fill:var(--go);letter-spacing:.1em}
.m-as{font-family:'JetBrains Mono',monospace;font-size:8.5px;fill:var(--ask);letter-spacing:.1em}
.m-am{font-family:'JetBrains Mono',monospace;font-size:8.5px;fill:var(--guess);letter-spacing:.1em}
.rr th{letter-spacing:.1em}
""",
    "th": _CSS_COMMON + """
figcaption{font-family:var(--mono);font-size:13px;line-height:1.9;color:var(--mute);
  margin-top:14px;max-width:62ch}
.dlab{letter-spacing:.06em}
.t-b{font-family:'IBM Plex Sans Thai',sans-serif;font-size:14px;fill:var(--fg);font-weight:600}
.t-s{font-family:'IBM Plex Sans Thai',sans-serif;font-size:11.5px;fill:var(--dim)}
.m{font-family:'IBM Plex Sans Thai',sans-serif;font-size:10px;fill:var(--mute);letter-spacing:0}
.m-go{font-family:'IBM Plex Sans Thai',sans-serif;font-size:10px;fill:var(--go);letter-spacing:0}
.m-as{font-family:'IBM Plex Sans Thai',sans-serif;font-size:10px;fill:var(--ask);letter-spacing:0}
.m-am{font-family:'IBM Plex Sans Thai',sans-serif;font-size:10px;fill:var(--guess);letter-spacing:0}
.rr{font-size:12px;line-height:1.8}
.rr th{letter-spacing:0}
""",
}

LANGS = (EN, TH)
