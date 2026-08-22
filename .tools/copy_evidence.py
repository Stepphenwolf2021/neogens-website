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
FACTS = {"pages": 43, "nodes": 465, "fonts": 28, "stubs": 26, "terms": 4,
         "org": 43, "crumbs": 33, "article": 5, "faq": 2}

# คำที่ใช้สะกดตัวเลขในเนื้อหา ด่านตรวจจะหาคำเหล่านี้ในหน้าที่สร้างเสร็จ
WORDS = {
    "en": {43: "forty-three", 465: "four hundred and sixty-five",
           28: "twenty-eight", 26: "twenty-six", 4: "four"},
    "th": {43: "สี่สิบสาม", 465: "สี่ร้อยหกสิบห้า",
           28: "ยี่สิบแปด", 26: "ยี่สิบหก", 4: "สี่"},
}
SPELLED = ("pages", "nodes", "fonts", "stubs", "terms")

# ประโยคที่อ้างจำนวนหน้าตามชนิดที่ประกาศไว้ ตรวจด้วยการประกอบประโยคจากค่าที่นับได้จริง
# แล้วหาในหน้าที่สร้างเสร็จ ถ้าเว็บโตขึ้นแล้วตัวเลขไม่ตรง ด่านนี้จะจับได้ทันที
CLAIMS = {
    "en": ["{crumbs} declare their position",
           "{article} are declared as articles",
           "{faq} carry questions and answers"],
    "th": ["{crumbs} หน้าประกาศตำแหน่งของตัวเอง",
           "{article} หน้าประกาศตัวเป็นบทความ",
           "{faq} หน้ามีคำถามคำตอบ"],
}

UPDATED_EN = "21 August 2026"
UPDATED_TH = "21 สิงหาคม 2026"
TESTED_EN = "21 August 2026"
TESTED_TH = "21 สิงหาคม 2026"

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
    "<b>ภาพประกอบ.</b> ระบบค้นหาเป็นตัวเดียวกันทั้งสองฝั่ง ต่างกันที่สิ่งที่ไปถึงมัน "
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
    [["www.neogens.co", "Organization", "~Valid · 0 errors · 0 warnings"],
     ["www.neogens.co/th-mkm-for-coffee.html", "Breadcrumbs",
      "~Valid · 0 errors · 0 warnings"]],
    "Two pages, run on Google's public tool. Anyone can repeat either row in about thirty "
    "seconds without asking us for anything — which is the point of quoting it.")

RR_TH = report(
    f"ผลตรวจจาก GOOGLE RICH RESULTS TEST · {TESTED_TH}",
    ["ที่อยู่ที่ทดสอบ", "สิ่งที่ตรวจพบ", "ผล"],
    [["www.neogens.co", "Organization", "~ผ่าน · 0 ข้อผิดพลาด · 0 คำเตือน"],
     ["www.neogens.co/th-mkm-for-coffee.html", "Breadcrumbs",
      "~ผ่าน · 0 ข้อผิดพลาด · 0 คำเตือน"]],
    "สองหน้า รันด้วยเครื่องมือสาธารณะของ Google ใครก็ทำซ้ำทีละแถวได้ในเวลาประมาณสามสิบวินาที "
    "โดยไม่ต้องขออะไรจากเรา ซึ่งเป็นเหตุผลเดียวที่หยิบมาอ้าง")

# ---------------------------------------------------------------- เนื้อหา

EN = {
    "src": "coffee-farmer.html",
    "out": "seo-as-knowledge-management.html",
    "twin": "th-seo-as-knowledge-management.html",
    "lang": "en",
    "title": "SEO as knowledge management — Neo Gens",
    "desc": "Content speaks to the people you want to reach. SEO speaks to the machines in "
            "between. How we designed ours as an ontology, and what the test reports.",
    "kicker": "Evidence",
    "h1": "Content speaks to people. SEO speaks to machines. Both are knowledge work.",
    "stand": "Most websites are designed for the first conversation and improvised for the "
             "second. This is how we designed ours as an ontology, and what happens when a "
             "machine is asked to read it back.",
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
        ("p", "Take the marketing vocabulary out of the second one and what is left is a "
              "cataloguing problem. Something arrives that cannot ask a question, cannot read "
              "tone, and will not come back to check. It has one pass to work out what you "
              "hold, how it connects, and whether to trust it. That is the same problem a "
              "catalogue record solves for a reader who will never meet the curator. Same "
              "discipline, different reader."),
        ("p", "Doing it properly is what lets the right people find you for a reason. An "
              "organisation that has described itself accurately to a machine gets matched to "
              "the people looking for exactly that. The alternative is buying attention "
              "without direction — paying to appear in front of people who do not want you, "
              "again and again, for as long as the budget lasts. That cost repeats every "
              "time. An accurate description of what you are does not."),

        ("h2", "How we designed ours: ontology-based SEO"),
        ("p", "Most SEO work starts from keywords: guess the phrases people type, then bend "
              "the pages toward them. It treats a search engine as a lock to be picked."),
        ("p", "We started at the other end, by describing what actually exists — the things, "
              "and the relations between them. That is an ontology, and it is the same object "
              "we build with clients. The difference is only that here the vocabulary was set "
              "by search engines rather than by a curatorial team. That vocabulary is "
              "schema.org: a shared dictionary of types and relations that the major search "
              "engines agreed on, so that a statement written once is understood the same way "
              "by all of them."),
        ("p", "In practice: the organisation has one identifier, declared once and referenced "
              "from every page. Each of the four terms this site uses in a specific sense has "
              "its own identifier and points at the page that defines it. Both practice areas "
              "are declared as services pointing back to the same provider. Every page states "
              "which of those things it is about. The Thai and English versions of a page are "
              "bound together as one work in two languages, not two pages that happen to "
              "resemble each other. Four hundred and sixty-five statements across forty-three "
              "pages."),
        ("p", "Around that: an address for every page that says what the page is, twenty-six "
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
        ("p", "Across the whole site, forty-three pages declare the organisation, 33 declare "
              "their position in the navigation, 5 are declared as articles and 2 carry "
              "questions and answers. Those numbers are counted from the files at build time, "
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
    "desc": "เนื้อหาคือสิ่งที่ใช้คุยกับคนที่เราอยากไปให้ถึง SEO คือสิ่งที่ใช้คุยกับเครื่องที่ยืนอยู่ตรงกลาง "
            "เราออกแบบของเราให้เป็น ontology อย่างไร และผลตรวจบอกอะไร",
    "kicker": "หลักฐาน",
    "h1": "เนื้อหาคุยกับคน SEO คุยกับเครื่อง ทั้งสองอย่างคืองานความรู้",
    "stand": "เว็บส่วนใหญ่ออกแบบมาเพื่อบทสนทนาชุดแรก แล้วด้นสดเอากับบทสนทนาชุดที่สอง "
             "หน้านี้คือวิธีที่เราออกแบบของเราให้เป็น ontology "
             "และสิ่งที่เกิดขึ้นเมื่อให้เครื่องลองอ่านกลับมาให้ฟัง",
    "meta": f"ปรับปรุง {UPDATED_TH}",
    "body": [
        ("h2", "เว็บส่วนใหญ่เขียนไว้ให้ผู้อ่านแบบเดียว แต่มีผู้อ่านสองแบบ"),
        ("p", "เว็บเกือบทุกเว็บเกิดขึ้นแบบเดียวกัน มีคนตัดสินใจโครงสร้าง มีคนเขียนเนื้อหา "
              "มีคนออกแบบหน้า แล้วตอนใกล้เสร็จจึงมีคนถามขึ้นมาว่า แล้ว SEO ล่ะ "
              "จากนั้นชื่อหน้าถูกเขียนใหม่ไม่กี่หน้า ติดปลั๊กอินสักตัว "
              "ส่งรายการคำค้นมาให้ชุดหนึ่ง แล้วเว็บก็ขึ้น"),
        ("p", "ถึงตอนนั้นโครงสร้างถูกตัดสินไปเรียบร้อยแล้ว และโครงสร้างคือส่วนที่สำคัญที่สุด "
              "สิ่งที่ได้คือเว็บที่คนอ่านรื่น แต่เครื่องอ่านไม่ออก "
              "ไม่มีอะไรในนั้นบอกว่าองค์กรนี้คืออะไร ทำงานอยู่ในสาขาไหน "
              "หน้าแต่ละหน้าเกี่ยวข้องกันอย่างไร หรือคำไหนในเว็บที่ใช้ในความหมายเฉพาะ "
              "คนอ่านอนุมานทั้งหมดนี้ได้ในไม่กี่วินาที เครื่องอนุมานไม่ได้เลยสักอย่าง"),
        ("p", "สาเหตุอยู่ที่ลำดับ ไม่ได้อยู่ที่ความตั้งใจ "
              "คำถามเรื่อง SEO มาถึงหลังจากการตัดสินใจที่มันควรมีส่วนกำหนดผ่านไปหมดแล้ว"),

        ("h2", "เนื้อหาคุยกับคน SEO คุยกับคอมพิวเตอร์"),
        ("p", "เรามองว่าเว็บหนึ่งเว็บมีบทสนทนาสองชุดอยู่ในไฟล์เดียวกัน "
              "เนื้อหาคือบทสนทนากับคนที่เราอยากไปให้ถึง — ข้อโต้แย้ง น้ำเสียง ตัวอย่าง "
              "และสิ่งที่ควรค่าแก่การเห็นต่าง ส่วน SEO คือบทสนทนากับคอมพิวเตอร์ "
              "ที่ยืนอยู่ระหว่างเรากับคนเหล่านั้น ว่าเราเป็นใคร ทำงานเรื่องอะไร "
              "และเกี่ยวข้องกับสิ่งไหน"),
        ("p", "ถอดคำศัพท์การตลาดออกจากบทสนทนาชุดหลัง สิ่งที่เหลือคือปัญหาการทำทะเบียน "
              "มีสิ่งหนึ่งเดินเข้ามา มันถามคำถามไม่ได้ อ่านน้ำเสียงไม่ออก "
              "และจะไม่ย้อนกลับมาตรวจซ้ำ มันมีโอกาสรอบเดียวที่จะเข้าใจว่าคุณถืออะไรอยู่ "
              "อะไรเชื่อมกับอะไร และควรเชื่อแค่ไหน "
              "นั่นคือปัญหาเดียวกับที่ระเบียนทะเบียนแก้ให้ผู้อ่านที่ไม่มีวันได้เจอภัณฑารักษ์ "
              "วิชาเดียวกัน ผู้อ่านคนละแบบ"),
        ("p", "การทำให้ถูกคือสิ่งที่ทำให้คนที่ใช่หาเราเจอด้วยเหตุผลที่สมเหตุสมผล "
              "องค์กรที่อธิบายตัวเองกับเครื่องไว้ตรงกับความจริง "
              "จะถูกจับคู่กับคนที่กำลังมองหาสิ่งนั้นพอดี "
              "ทางเลือกอีกทางคือซื้อความสนใจแบบไร้ทิศทาง "
              "จ่ายเงินเพื่อไปโผล่ต่อหน้าคนที่ไม่ได้ต้องการเรา ซ้ำแล้วซ้ำเล่า "
              "นานเท่าที่งบยังมีอยู่ ค่าใช้จ่ายแบบนั้นเกิดซ้ำทุกครั้ง "
              "คำอธิบายที่ตรงกับความจริงว่าเราเป็นอะไร ไม่ต้องจ่ายซ้ำ"),

        ("h2", "SEO ของเราออกแบบอย่างไร — ontology-based SEO"),
        ("p", "งาน SEO ส่วนใหญ่เริ่มจากคำค้น เดาว่าคนพิมพ์อะไร แล้วดัดหน้าเว็บเข้าหาคำเหล่านั้น "
              "วิธีนี้ปฏิบัติกับระบบค้นหาเหมือนกุญแจที่ต้องหาทางสะเดาะ"),
        ("p", "เราเริ่มจากอีกด้าน คืออธิบายสิ่งที่มีอยู่จริง ว่ามีอะไรบ้าง "
              "และแต่ละอย่างสัมพันธ์กันอย่างไร นั่นคือ ontology "
              "และเป็นวัตถุชนิดเดียวกับที่เราสร้างร่วมกับลูกค้า "
              "ต่างกันเพียงว่าที่นี่ระบบค้นหาเป็นผู้กำหนดคำศัพท์ ไม่ใช่ทีมภัณฑารักษ์ "
              "คำศัพท์ชุดนั้นคือ schema.org "
              "พจนานุกรมกลางของชนิดและความสัมพันธ์ที่ระบบค้นหารายใหญ่ตกลงร่วมกันไว้ "
              "เขียนครั้งเดียวแล้วทุกรายเข้าใจตรงกัน"),
        ("p", "ในทางปฏิบัติ องค์กรมีตัวระบุตัวเดียว ประกาศครั้งเดียวแล้วอ้างถึงจากทุกหน้า "
              "ศัพท์สี่คำที่เว็บนี้ใช้ในความหมายเฉพาะ แต่ละคำมีตัวระบุของตัวเอง "
              "และชี้ไปยังหน้าที่นิยามมันไว้จริง "
              "สองสายงานประกาศเป็นบริการที่ชี้กลับมาที่ผู้ให้บริการรายเดียวกัน "
              "ทุกหน้าบอกว่าตัวเองพูดถึงสิ่งไหนในนั้น "
              "ฉบับไทยกับอังกฤษของหน้าเดียวกันผูกกันในฐานะงานชิ้นเดียวสองภาษา "
              "ไม่ใช่สองหน้าที่บังเอิญคล้ายกัน รวมสี่ร้อยหกสิบห้าข้อความ ในสี่สิบสามหน้า"),
        ("p", "รอบ ๆ นั้นคือที่อยู่ของทุกหน้าที่บอกได้เองว่าหน้านั้นเป็นเรื่องอะไร "
              "ทางเบี่ยงยี่สิบหกเส้นที่ทำให้ลิงก์ทุกเส้นที่เคยส่งออกไปยังไปถึงปลายทาง "
              "ไฟล์ฟอนต์ยี่สิบแปดไฟล์และสไตล์ทั้งหมดที่เสิร์ฟจากโดเมนนี้ "
              "การเปิดหน้าเว็บจึงไม่ได้ติดต่อใครนอกจากเรา"),
        ("raw", FIG_TH),
        ("p", "เหตุผลที่เลือกวิธีนี้แทนการไล่คำค้น คือมันไม่หมดอายุ สูตรจัดอันดับเปลี่ยนทุกปี "
              "และเทคนิคที่สร้างมาเพื่อสูตรหนึ่งก็ใช้ไม่ได้กับสูตรถัดไป "
              "แต่คำอธิบายที่ตรงกับความจริงว่าองค์กรนี้เป็นอะไร ไม่ล้าสมัยเมื่อสูตรเปลี่ยน "
              "และมันคือรูปแบบเดียวกับที่ผู้ช่วย AI อ่าน "
              "ซึ่งเป็นที่ที่คนจำนวนมากขึ้นเรื่อย ๆ เอาคำถามไปถาม"),

        ("h2", "เครื่องอ่านได้จริงหรือเปล่า ตรวจเองได้"),
        ("p", "ทุกอย่างข้างบนไม่มีค่าอะไรเลยถ้าเป็นแค่คำกล่าวอ้าง "
              "Google เปิดเครื่องมือฟรีตัวหนึ่งชื่อ Rich Results Test "
              "รับที่อยู่หน้าไหนก็ได้ ดึงหน้านั้นมาแบบเดียวกับที่ตัวเก็บข้อมูลของมันทำ "
              "แล้วรายงานกลับมาว่าเจอรายการที่มีโครงสร้างอะไรบ้าง และแต่ละรายการใช้ได้หรือไม่ "
              "นี่คือสิ่งที่ใกล้เคียงที่สุดกับการให้คนนอกอ่านว่าเว็บหนึ่งพูดถึงตัวเองว่าอย่างไร"),
        ("raw", RR_TH),
        ("p", "ทั้งเว็บ สี่สิบสามหน้าประกาศตัวองค์กร 33 หน้าประกาศตำแหน่งของตัวเองในเส้นทางนำทาง "
              "5 หน้าประกาศตัวเป็นบทความ และ 2 หน้ามีคำถามคำตอบ "
              "ตัวเลขเหล่านี้นับจากไฟล์ตอนสร้างหน้า ไม่ได้พิมพ์มือ "
              "ถ้าหน้าไหนกราฟหาย กระบวนการสร้างจะหยุดทันที"),

        ("h2", "ผ่านแล้วได้อะไร ไม่ผ่านแล้วเสียอะไร"),
        ("p", "การผ่านไม่ใช่การเพิ่มอันดับ ใครบอกว่าใช่คือกำลังขายของ "
              "สิ่งที่ได้แคบกว่านั้น คือระบบค้นหาเลิกอนุมานแล้วเปลี่ยนมาอ้างสิ่งที่เราเขียนไว้ "
              "องค์กรกลายเป็นสิ่งหนึ่งที่ถูกระบุตัวได้ ไม่ใช่ชื่อที่บังเอิญโผล่อยู่ในข้อความ "
              "หน้าเว็บถูกแสดงพร้อมเส้นทางของมัน ผู้เขียน หรือคำถามคำตอบได้ "
              "และคำประกาศชุดเดียวกันนี้คือสิ่งที่ผู้ช่วย AI อ่าน "
              "เวลามีคนถามคำถามในสาขาที่เราทำงานอยู่"),
        ("p", "ส่วนการไม่ผ่านนั้นหนักกว่าที่เห็น เพราะมันเกิดขึ้นอย่างเงียบมาก "
              "รายการที่มีข้อผิดพลาดไม่ได้ถูกแสดงพร้อมเครื่องหมายสีแดง แต่ถูกทิ้ง "
              "หน้ายังดูสมบูรณ์สำหรับคน ยังโหลดขึ้น ยังอ่านรื่น "
              "เพียงแต่ไม่ถูกพิจารณาในเรื่องที่มันประกาศไว้เลย และไม่มีใครเขียนมาบอก "
              "ส่วนคำเตือนคือฉบับเบากว่า รายการยังอยู่ แต่เสียคุณสมบัติที่มันไม่ผ่านเกณฑ์ไป"),
        ("p", "ราคาที่แพงกว่านั้นคือความไว้ใจที่ลามข้ามหน้า "
              "คำประกาศที่เครื่องยืนยันไม่ได้ ไม่ได้เสียแค่หน้าตัวเอง "
              "เมื่อสองหน้าอ้างว่าเป็นฉบับแปลของกันและกัน แต่มีหน้าเดียวที่ยืนยันกลับ "
              "ระบบค้นหาจะเลิกเชื่อคำประกาศชนิดนั้นของทั้งโดเมน "
              "คำอ้างที่ตรวจไม่ได้หนึ่งข้อ ลดน้ำหนักของข้ออื่นที่จริงซึ่งอยู่ข้าง ๆ ไปด้วย "
              "ด้วยเหตุผลเดียวกับที่ทะเบียนซึ่งมีระเบียนเชื่อถือไม่ได้ปนอยู่ "
              "มีค่าน้อยกว่าครึ่งที่ถูกต้องของมันเอง"),
        ("p", "เราจึงถือว่าการตรวจนี้เป็นเงื่อนไขของการปล่อยหน้า ไม่ใช่เหรียญที่เอาไว้สะสม "
              "ทุกหน้าบนเว็บนี้สร้างด้วยสคริปต์ที่จะไม่ยอมเขียนไฟล์ "
              "ถ้าโครงสร้างที่มันประกาศไม่ตรงกับสิ่งที่หน้านั้นแสดงให้ผู้อ่านเห็นจริง"),
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
