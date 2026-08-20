# -*- coding: utf-8 -*-
"""
ข้อความทั้งหมดของหน้าเดโม สองภาษา แยกออกมาจากตัวสร้าง

ตัวสร้าง build_demo.py อ่านไฟล์นี้แล้วประกอบหน้า coffee-demo.html กับ
th-coffee-demo.html จากแม่แบบคนละไฟล์ แต่ใช้โครงเดียวกันทุกบรรทัด

ป้ายในแผงที่ขึ้นตอนคลิกจุดบนแผนที่อยู่ใน LABELS เพราะมันอยู่ในฝั่ง JS
dashboard.js จะอ่านจาก window.__VAULT_LABELS__ ถ้าไม่มีจะตกกลับเป็นอังกฤษ

ชื่อเส้นสมมติบนแผนที่ (TROPIC OF CANCER ฯลฯ) คงเป็นอังกฤษทั้งสองฉบับ
เพราะตัวอักษรบนแผนที่เล็ก 7px ภาษาไทยที่ขนาดนั้นอ่านไม่ออก
"""

# ---------------------------------------------------------------- ตัวหน้า

EN = {
    "src": "coffee-farmer.html",
    "out": "coffee-demo.html",
    "twin": "th-coffee-demo.html",
    "lang": "en",
    "title": "What 5,000 contributors would look like — Neo Gens",
    "ogtitle": "What 5,000 contributors would look like",
    "desc": "A simulated dashboard of the Coffee Knowledge Vault: 5,000 contributors "
            "along the coffee chain, and what a farmer or a roaster would actually ask it.",
    "kicker": "MKM for Coffee · demo",
    "h1": "What the vault looks like with 5,000 people in it",
    "stand": "A simulated view of the Coffee Knowledge Vault — every origin, every market, "
             "and the routes already carrying verified lots between them. Click any point.",
    "meta": "interactive demo",
    "fullargument": "The full argument",
    "warn_b": "Simulated",
    "warn_p": "Nothing on this page is real data. It is a working sketch of what the "
              "Coffee Knowledge Vault looks like once 5,000 people along the chain have "
              "contributed to it. No one has contributed yet — that is the phase we are in.",
    "stats": ["Contributors", "Farmers", "Roasters", "Co-ops &amp; mills",
              "Exporters &amp; importers", "Cafés", "Researchers", "Certifiers"],
    "stats_sub": ["43 origins and markets", "80% of the vault", "10%",
                  "the collection layer", "compliance and shipping", "the last mile",
                  "agronomy and sensory", "independent verification"],
    "legend": ["origin · farms, co-ops, mills", "market · roasters, cafés, importers",
               "line = a trade route already carrying verified lots"],
    "map_alt": "World map with the coffee belt shaded, showing 43 points where "
               "contributors have registered, and curved lines linking each origin to "
               "the markets that buy from it",
    "tools": ["Trade routes", "High-scoring origins", "Buyer matches", "Contributors only"],
    "slider": "cup score",
    "slider_any": "any",
    "match_hint": "Select a point on the map first",
    "slider_alt": "Filter origins by mean cup score",
    "cards": [
        ("Quality", "What method gets the score, at your altitude",
         "Mean cup score by processing method across every lot in the vault. A farmer "
         "filters this to plots within 150 m of their own elevation before deciding what "
         "to try next season."),
        ("Market", "What buyers are searching for",
         "Roasters query the vault by profile rather than by broker relationship. These "
         "are the searches that returned too few lots this month — each one is a market "
         "opening visible from the growing side."),
        ("Traceability", "How far back a bag can be walked",
         "Every hop carries a date, a quantity and a source. Where a machine reading "
         "backs the claim, the lot is marked verified rather than stated."),
    ],
    "searches": [("floral · tea-like", 214), ("low acidity", 187), ("honey process", 156),
                 ("single plot", 143), ("shade grown", 98)],
    "hops_row": [("plot", 81), ("mill", 93), ("exporter", 97), ("roaster", 99)],
    "thead": ["Lot", "Origin", "Process", "Score", "Flavour", "Traceable", "Buyer match"],
    "hops": "hops",
    "caption": "Every figure on this page is simulated. The point is the shape of the "
               "answer, not the numbers: one structure, contributed to by everyone along "
               "the chain, that a farmer can query for what to do next season and a "
               "roaster can query for what to buy — and both get an answer that carries "
               "its own evidence.",
    "join_k": "Build the real one",
    "join_h": "This is a sketch. The real one needs contributors.",
    "join_p": "Leave your details if you want to put the first real data into it.",
    "lots": [
        ("LOT-2026-0412", "Chiang Rai, Thailand", "honey", "86.5", "longan · tamarind",
         "5", "Osaka · 2 roasters", "go"),
        ("LOT-2026-0388", "Huila, Colombia", "washed", "85.9", "citrus · red fruit",
         "6", "Berlin · 4 roasters", "go"),
        ("LOT-2026-0361", "Yirgacheffe, Ethiopia", "natural", "87.2", "jasmine · peach",
         "4", "Seoul · 3 roasters", "go"),
        ("LOT-2026-0344", "Nyeri, Kenya", "washed", "86.8", "blackcurrant · tomato",
         "5", "Melbourne · 2 roasters", "go"),
        ("LOT-2026-0329", "Cerrado, Brazil", "natural", "83.4", "nut · cocoa",
         "3", "moisture reading pending", "am"),
        ("LOT-2026-0317", "Aceh, Indonesia", "wet-hulled", "84.1", "cedar · herbal",
         "4", "Taipei · 1 roaster", "go"),
    ],
    "labels": None,          # อังกฤษใช้ค่าที่ฝังอยู่ใน dashboard.js อยู่แล้ว
}

TH = {
    "src": "th-coffee-farmer.html",
    "out": "th-coffee-demo.html",
    "twin": "coffee-demo.html",
    "lang": "th",
    "title": "ถ้ามีคนร่วมสร้างคลังห้าพันราย หน้าตาจะเป็นแบบนี้ — Neo Gens",
    "ogtitle": "ถ้ามีคนร่วมสร้างคลังห้าพันราย หน้าตาจะเป็นแบบนี้",
    "desc": "แดชบอร์ดจำลองของคลังความรู้กาแฟ ผู้ร่วมบันทึกข้อมูลห้าพันรายตลอดห่วงโซ่ "
            "กราฟความรู้วางซ้อนบนแผนที่โลก และคำถามที่เกษตรกรกับโรงคั่วจะถามมันจริง ๆ",
    "kicker": "MKM สำหรับกาแฟ · เดโม",
    "h1": "จำลองคลังความรู้กาแฟ เมื่อมีผู้บันทึกและร่วมสร้างคลังความรู้กาแฟห้าพันคน",
    "stand": "ภาพจำลองของคลังความรู้กาแฟ ทุกแหล่งกาแฟ ทุกตลาด และเส้นทางที่มีล็อตผ่านการยืนยัน "
             "วิ่งอยู่ระหว่างกันแล้ว คลิกที่จุดไหนก็ได้",
    "meta": "เดโมกดเล่นได้",
    "fullargument": "อ่านโครงการเต็ม",
    "warn_b": "ข้อมูลจำลอง",
    "warn_p": "ไม่มีอะไรในหน้านี้เป็นข้อมูลจริง นี่คือภาพร่างที่ใช้งานได้จริงว่าคลังความรู้กาแฟ "
              "จะหน้าตาเป็นอย่างไรเมื่อคนตลอดห่วงโซ่ห้าพันรายลงข้อมูลเข้าไปแล้ว "
              "ตอนนี้ยังไม่มีใครลงสักราย นั่นคือช่วงที่เราอยู่",
    "stats": ["ผู้ร่วมบันทึกข้อมูล", "เกษตรกร", "โรงคั่ว", "สหกรณ์และโรงสี",
              "ผู้ส่งออกและผู้นำเข้า", "ร้านกาแฟ", "นักวิจัย", "ผู้ตรวจรับรอง"],
    "stats_sub": ["43 แหล่งกาแฟและตลาด", "80% ของทั้งคลัง", "10%",
                  "ชั้นที่รวบรวมผลผลิต", "งานเอกสารและการขนส่ง", "ปลายทางสุดท้าย",
                  "เกษตรศาสตร์และการชิม", "ตรวจสอบโดยคนนอก"],
    "legend": ["แหล่งกาแฟ · แปลง สหกรณ์ โรงสี", "ตลาด · โรงคั่ว ร้านกาแฟ ผู้นำเข้า",
               "เส้น = เส้นทางการค้าที่มีล็อตผ่านการยืนยันวิ่งอยู่แล้ว"],
    "map_alt": "แผนที่โลกที่แรเงาแถบปลูกกาแฟ แสดง 43 จุดที่มีผู้ร่วมบันทึกข้อมูลลงทะเบียนไว้ "
               "และเส้นโค้งที่เชื่อมแต่ละแหล่งกาแฟเข้ากับตลาดที่รับซื้อ",
    "tools": ["เส้นทางการค้าทั้งหมด", "เฉพาะแหล่งกาแฟคะแนนสูง",
              "เฉพาะที่โรงคั่ว/ผู้ซื้อที่ตรงโปรไฟล์", "เฉพาะผู้ร่วมบันทึกข้อมูล"],
    "slider": "คะแนนคัปปิ้ง",
    "slider_any": "ทั้งหมด",
    "match_hint": "เลือกจุดบนแผนที่ก่อน",
    "slider_alt": "กรองแหล่งกาแฟด้วยคะแนนคัปปิ้งเฉลี่ย",
    "cards": [
        ("คุณภาพ", "วิธีแปรรูปไหนได้คะแนน ที่ความสูงระดับคุณ",
         "คะแนนคัปปิ้งเฉลี่ยแยกตามวิธีแปรรูป จากทุกล็อตในคลัง เกษตรกรกรองให้เหลือเฉพาะแปลง "
         "ที่ความสูงห่างจากของตัวเองไม่เกิน 150 เมตร ก่อนตัดสินใจว่าฤดูหน้าจะลองอะไร"),
        ("ตลาด", "ผู้ซื้อกำลังค้นหาอะไรอยู่",
         "โรงคั่วค้นในคลังด้วยโปรไฟล์รส ไม่ใช่ด้วยความสัมพันธ์กับนายหน้า รายการนี้คือคำค้น "
         "ที่เดือนนี้หาล็อตมาตอบได้น้อยเกินไป แต่ละบรรทัดคือช่องว่างในตลาดที่ฝั่งคนปลูกมองเห็น"),
        ("การสาวกลับ", "ถุงหนึ่งเดินย้อนกลับไปได้ไกลแค่ไหน",
         "ทุกช่วงของการส่งต่อมีวันที่ ปริมาณ และแหล่งที่มากำกับ ช่วงไหนที่มีค่าจากเครื่องมือ "
         "รองรับ ล็อตนั้นจะถูกทำเครื่องหมายว่ายืนยันแล้ว ไม่ใช่แค่กล่าวอ้าง"),
    ],
    "searches": [("ดอกไม้ · คล้ายชา", 214), ("เปรี้ยวน้อย", 187), ("แปรรูปแบบฮันนี่", 156),
                 ("แปลงเดียว", 143), ("ปลูกใต้ร่มเงา", 98)],
    "hops_row": [("แปลง", 81), ("โรงสี", 93), ("ผู้ส่งออก", 97), ("โรงคั่ว", 99)],
    "thead": ["ล็อต", "แหล่งกาแฟ", "วิธีแปรรูป", "คะแนน", "รสชาติ", "สาวกลับได้", "ผู้ซื้อที่ตรงกัน"],
    "hops": "ช่วง",
    "caption": "ทุกตัวเลขบนหน้านี้เป็นข้อมูลจำลอง สิ่งที่อยากให้เห็นคือรูปร่างของคำตอบ "
               "ไม่ใช่ตัวเลข — โครงสร้างเดียวที่ทุกคนตลอดห่วงโซ่ช่วยกันลงข้อมูล "
               "เกษตรกรถามมันได้ว่าฤดูหน้าควรทำอะไร โรงคั่วถามมันได้ว่าควรซื้ออะไร "
               "และทั้งคู่ได้คำตอบที่มีหลักฐานติดมาด้วย",
    "join_k": "ช่วยกันสร้างของจริง",
    "join_h": "นี่เป็นแค่ภาพร่าง ของจริงต้องมีคนช่วยกันลงข้อมูล",
    "join_p": "ทิ้งรายละเอียดไว้ ถ้าอยากเป็นคนแรกที่ลงข้อมูลจริงเข้าไปในคลังนี้",
    "lots": [
        ("LOT-2026-0412", "เชียงราย ไทย", "ฮันนี่", "86.5", "ลำไย · มะขาม",
         "5", "โอซากา · 2 โรงคั่ว", "go"),
        ("LOT-2026-0388", "อุยลา โคลอมเบีย", "ล้าง", "85.9", "ส้ม · ผลไม้แดง",
         "6", "เบอร์ลิน · 4 โรงคั่ว", "go"),
        ("LOT-2026-0361", "เยอร์กาเชฟฟี เอธิโอเปีย", "ตากแห้ง", "87.2", "มะลิ · พีช",
         "4", "โซล · 3 โรงคั่ว", "go"),
        ("LOT-2026-0344", "ไนเยรี เคนยา", "ล้าง", "86.8", "แบล็กเคอร์แรนต์ · มะเขือเทศ",
         "5", "เมลเบิร์น · 2 โรงคั่ว", "go"),
        ("LOT-2026-0329", "เซอร์ราโด บราซิล", "ตากแห้ง", "83.4", "ถั่ว · โกโก้",
         "3", "รอค่าความชื้น", "am"),
        ("LOT-2026-0317", "อาเจะห์ อินโดนีเซีย", "สีเปียก", "84.1", "ไม้ซีดาร์ · สมุนไพร",
         "4", "ไทเป · 1 โรงคั่ว", "go"),
    ],
    # ป้ายฝั่ง JS ที่ขึ้นตอนคลิกจุดบนแผนที่
    "labels": {
        "participants": "ราย",
        "anyScore": "ทั้งหมด",
        "today": "คลังในวันนี้",
        "contributors5k": "ผู้ร่วมบันทึกข้อมูล 5,000 ราย",
        "originsMarkets": "43 แหล่งกาแฟและตลาด · ข้อมูลจำลอง",
        "farmers": "เกษตรกร",
        "roasters": "โรงคั่ว",
        "coops": "สหกรณ์",
        "mills": "โรงสีและสถานีล้าง",
        "exporters": "ผู้ส่งออกและผู้นำเข้า",
        "cafes": "ร้านกาแฟ",
        "researchers": "นักวิจัย",
        "certifiers": "ผู้ตรวจรับรอง",
        "hint": "คลิกจุดไหนบนแผนที่ก็ได้ เพื่อดูว่าแหล่งกาแฟนั้นลงอะไรไว้ในคลังบ้าง "
                "และโปรไฟล์ของมันตรงกับโรงคั่วรายไหน",
        "origin": "แหล่งกาแฟ",
        "market": "ตลาด",
        "marketSub": "โรงคั่ว ร้านกาแฟ และผู้นำเข้า",
        "contributors": "ผู้ร่วมบันทึกข้อมูล",
        "coopsMills": "สหกรณ์ / โรงสี",
        "lots": "ล็อตที่มีบันทึก",
        "score": "คะแนนคัปปิ้งเฉลี่ย",
        "traceable": "สาวกลับถึงแปลง",
        "flavour": "โปรไฟล์รส",
        "importers": "ผู้นำเข้า",
        "sourced": "แหล่งกาแฟที่รับซื้อ",
        "cupping": "ผลคัปปิ้งที่แบ่งปันไว้",
        "routes": "ซื้อจากแหล่งกาแฟนี้วันนี้ แปลว่าได้อ่านเส้นทางที่ยืนยันแล้ว {n} เส้น เข้าสู่{list}{more}",
        "more": " และอีก {n} แห่ง",
        "matchBtn": "ดูโรงคั่วที่รับซื้อโปรไฟล์นี้",
        "backBtn": "กลับไปภาพรวม",
        "marketNote": "ผลคัปปิ้งทุกครั้งที่เพิ่มเข้ามาตรงนี้ "
                      "ทำให้เกณฑ์เทียบที่เกษตรกรอีกฟากของแผนที่มองเห็นคมขึ้น",
        "proc": {
            "honey": "ฮันนี่", "washed": "ล้าง", "natural": "ตากแห้ง",
            "wet-hulled": "สีเปียก", "monsooned": "ผึ่งลมมรสุม", "mixed": "ผสม",
        },
        "place": {
            "Brazil": "บราซิล", "Vietnam": "เวียดนาม", "Colombia": "โคลอมเบีย",
            "Indonesia": "อินโดนีเซีย", "Ethiopia": "เอธิโอเปีย", "Honduras": "ฮอนดูรัส",
            "India": "อินเดีย", "Uganda": "ยูกันดา", "Mexico": "เม็กซิโก",
            "Guatemala": "กัวเตมาลา", "Peru": "เปรู", "Nicaragua": "นิการากัว",
            "Costa Rica": "คอสตาริกา", "Kenya": "เคนยา", "Tanzania": "แทนซาเนีย",
            "Rwanda": "รวันดา", "Burundi": "บุรุนดี", "El Salvador": "เอลซัลวาดอร์",
            "Papua New Guinea": "ปาปัวนิวกินี", "Thailand": "ไทย", "Laos": "ลาว",
            "Yemen": "เยเมน", "Panama": "ปานามา", "Ecuador": "เอกวาดอร์",
            "DR Congo": "คองโก", "Rest of origins": "แหล่งกาแฟอื่น ๆ",
            "United States": "สหรัฐอเมริกา", "Japan": "ญี่ปุ่น", "Germany": "เยอรมนี",
            "Italy": "อิตาลี", "United Kingdom": "สหราชอาณาจักร", "South Korea": "เกาหลีใต้",
            "Australia": "ออสเตรเลีย", "Canada": "แคนาดา", "Nordics": "กลุ่มนอร์ดิก",
            "France": "ฝรั่งเศส", "Netherlands": "เนเธอร์แลนด์", "China": "จีน",
            "Taiwan": "ไต้หวัน", "Bangkok": "กรุงเทพ", "UAE": "สหรัฐอาหรับเอมิเรตส์",
            "Spain": "สเปน", "Switzerland": "สวิตเซอร์แลนด์",
        },
    },
}

# ไทยไม่ถ่างตัวอักษร กฎเดิมตั้ง letter-spacing ไว้สำหรับ mono อังกฤษ
TH_CSS = """
/* --- ฉบับไทย ยกเลิกการถ่างตัวอักษรในกฎที่ตอนนี้ใส่ข้อความไทย --- */
.dm-warn b,.dm-stat .l,.dm-legend,.dm-tool,.dm-panel .k,.dm-row .a,
.dm-act,.dm-card .k,.dm-bar .n,.dm-table th,.dm-chip{letter-spacing:0}
.dm-bar .n{width:88px}
"""

LANGS = [EN, TH]
