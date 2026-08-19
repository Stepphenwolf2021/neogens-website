# -*- coding: utf-8 -*-
"""Stage 1 of the three-part restructure.

Creates, by cloning why.html / th-why.html as a shell so the chrome, CSS,
nav, footer and theme stay byte-identical to the rest of the site:

  ภาค 1  problem.html    rewritten — generic, short
  ภาค 1  layer.html      new — what ontology / knowledge graph actually are
  ภาค 2  advantage.html  new — the old museum-specific problem page, moved verbatim
  ภาค 2  sovereignty.html new — AI Sovereignty

Existing prose written by Noppadol is moved, never reworded.
"""
import io, os, re

W = '/sessions/practical-pensive-rubin/mnt/neogens-website'

EXTRA_CSS = """
/* section pages (added) */
.blks{display:grid;gap:12px;margin-top:clamp(30px,4vw,46px)}
.blk{border:1px solid var(--line);border-radius:16px;background:var(--surface);padding:clamp(22px,3vw,30px)}
.blk .n{font-family:var(--mono);font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:var(--go);margin-bottom:12px}
.blk h3{font-size:clamp(17px,2.1vw,21px);line-height:1.35;margin-bottom:10px;color:var(--fg)}
.blk p{font-size:15.5px;color:var(--dim);margin:0}
.blk p+p{margin-top:12px}
.blks.three{grid-template-columns:repeat(3,1fr)}
@media(max-width:900px){.blks.three{grid-template-columns:1fr}}
.creed{margin-top:clamp(34px,4.5vw,52px);border-left:2px solid var(--go);padding:6px 0 6px clamp(20px,3vw,30px)}
.creed p{font-family:var(--serif);font-size:clamp(20px,2.6vw,28px);line-height:1.35;color:var(--fg);margin:0}
.closer{margin-top:clamp(28px,3.5vw,40px);font-size:16.5px;color:var(--dim);max-width:64ch}
"""

TH_CSS = EXTRA_CSS.replace('line-height:1.35', 'line-height:1.75')


def block(n, h, ps):
    return ('<div class="blk rv"><div class="n">%s</div><h3>%s</h3>%s</div>'
            % (n, h, ''.join('<p>%s</p>' % p for p in ps)))


PAGES = {}

# ── ภาค 1 · 01 ปัญหา (ฉบับทั่วไป) ────────────────────────────────
PAGES['problem'] = dict(
    th=dict(
        title='AI ตอบได้ทุกเรื่อง แต่ไม่รู้ว่าองค์กรคุณต้องการอะไร',
        desc='ทุกองค์กรกำลังเอา AI ไปวางทับกองเอกสารของตัวเองตรง ๆ ใช้ได้ดี จนถึงวินาทีที่คำตอบนั้นสำคัญจริง',
        eyebrow='ภาค 1 · แนวคิด — 01 ปัญหา',
        h1='AI ตอบได้ทุกเรื่อง แต่ไม่รู้ว่าองค์กรคุณต้องการอะไร',
        lede=['ทุกองค์กรกำลังเอา AI มาใช้ และเกือบทุกแห่งเอามันไปวางทับกองเอกสารของตัวเองตรง ๆ '
              'โมเดลอ่านสิ่งที่ได้รับ แล้วผลิตคำตอบที่ฟังดูสมเหตุสมผลที่สุดออกมา',
              'ใช้ได้ดี จนถึงวินาทีที่คำตอบนั้นสำคัญจริง'],
        blocks=[('01', 'ความรู้อยู่ครบทุกกล่อง แต่ไม่มีเส้นทางระหว่างกล่อง',
                 ['ไม่มีใครออกแบบให้ความรู้แต่ละชิ้นเชื่อมกันตั้งแต่ต้น ยิ่งนานวันกล่องยิ่งมากขึ้น '
                  'รูปแบบยิ่งหลากหลาย จนไม่มีสมองใครไล่ความสัมพันธ์ทั้งหมดไหว']),
                ('02', 'AI เดาแม่นขึ้น ไม่ได้แปลว่ามันเข้าใจคุณ',
                 ['LLM ทำงานบนสถิติว่าคำถัดไปน่าจะเป็นคำอะไร มันตอบถูกเพราะเคยผ่านตาการเรียงแบบนี้'
                  'มาแล้วนับล้านครั้ง ไม่ใช่เพราะรู้จักองค์กรของคุณ']),
                ('03', 'คำตอบที่สาวกลับไม่ได้ ออกไปในนามคุณ',
                 ['ทุกคำตอบที่ AI ให้แทนองค์กร คือคำแถลงขององค์กร ตอบผิดครั้งเดียว '
                  'ความเชื่อมั่นที่สะสมมานานก็สั่นคลอน'])],
        creed='เราเชื่อว่าความสำเร็จขององค์กร วัดกันที่ความสามารถในการบริหารสินทรัพย์ที่ชื่อว่าข้อมูลและความรู้ '
              'ให้สร้างคุณค่าได้จริง ทั้งกับองค์กรเอง ลูกค้า คู่ค้า สังคม ประเทศ และโลก',
        closer='สิ่งที่ขาดจึงไม่ใช่ AI ที่เก่งขึ้น แต่คือชั้นที่บอกว่าองค์กรนี้รู้อะไร รู้มาได้อย่างไร และให้ความสำคัญกับอะไร',
        prev=('th-index.html', 'สารบัญทั้งหมด'), next=('th-what-mkm-is.html', 'สิ่งนี้คืออะไร'),
    ),
    en=dict(
        title='AI answers everything, and knows nothing about what your organisation is for',
        desc='Almost every organisation points AI straight at its own pile of documents. That works, right up to the moment the answer matters.',
        eyebrow='Part 1 · The idea — 01 The problem',
        h1='AI answers everything, and knows nothing about what your organisation is for',
        lede=['Every organisation is putting AI to work, and almost all of them point it straight at '
              'their own pile of documents. The model reads what it is given and produces the answer '
              'that sounds most plausible.',
              'That works, right up to the moment the answer matters.'],
        blocks=[('01', 'Every box is full. Nothing runs between them.',
                 ['None of this knowledge was designed to connect in the first place. Each year adds '
                  'more boxes and more formats, until no human mind can hold the relationships '
                  'between them.']),
                ('02', 'A better guess is not understanding',
                 ['An LLM works on the statistics of which word most likely comes next. It answers '
                  'correctly because it has met that sequence a million times before, not because it '
                  'knows anything about your organisation.']),
                ('03', 'An answer nobody can trace still goes out in your name',
                 ['Every answer an AI gives on your behalf is a statement by the organisation. One '
                  'wrong answer shakes trust that took decades to build.'])],
        creed='We believe an organisation succeeds or fails on one thing: how well it manages the asset '
              'called knowledge, so that it creates real value — for the organisation, its customers, '
              'its partners, its society, its country and the world.',
        closer='What is missing is not a cleverer AI. It is the layer that records what this organisation '
               'knows, how it came to know it, and what it exists to do.',
        prev=('index.html', 'All sections'), next=('what-mkm-is.html', 'What it is'),
    ),
)

# ── ภาค 1 · 04 ontology กับ knowledge graph ──────────────────────
PAGES['layer'] = dict(
    th=dict(
        title='ontology กับ knowledge graph คืออะไร พูดด้วยภาษาคน',
        desc='สองคำนี้อยู่แทบทุกหน้าของเว็บนี้ หน้านี้อธิบายมันครั้งเดียวให้จบ ด้วยตัวอย่างจากงานจริง',
        eyebrow='ภาค 1 · แนวคิด — 04 ศัพท์สองคำ',
        h1='ontology กับ knowledge graph คืออะไร พูดด้วยภาษาคน',
        lede=['สองคำนี้อยู่แทบทุกหน้าของเว็บนี้ หน้านี้อธิบายมันครั้งเดียวให้จบ '
              'ไม่มีศัพท์เทคนิคเพิ่มอีกแม้แต่คำเดียว'],
        blocks=[('01', 'ontology คือการตกลงกันว่าเราเรียกอะไรว่าอะไร และอะไรเกี่ยวกับอะไร',
                 ['ภัณฑารักษ์เรียกของชิ้นหนึ่งว่าวัตถุ นักอนุรักษ์เรียกชิ้นงาน หอจดหมายเหตุเรียกรายการ '
                  'ontology คือเอกสารที่ระบุว่าสามคำนี้หมายถึงสิ่งเดียวกัน สิ่งนั้นมีผู้สร้าง มีแหล่งที่พบ '
                  'มีเจ้าของก่อนหน้า และแต่ละเส้นความสัมพันธ์แปลว่าอะไร',
                  'เขียนครั้งเดียว ใช้ได้ทั้งองค์กร']),
                ('02', 'knowledge graph คือของจริงที่สร้างขึ้นตาม ontology นั้น',
                 ['ontology คือแบบแปลน knowledge graph คือตัวอาคาร',
                  'ในกราฟ ความสัมพันธ์ระหว่างสองสิ่งไม่ใช่สิ่งที่ต้องประกอบขึ้นใหม่ทุกครั้งที่ค้น '
                  'มันถูกเก็บไว้แล้ว มีชื่อ มีทิศทาง และเดินตามได้']),
                ('03', 'mission-driven — ธุรกิจเดียวกันไม่จำเป็นต้องมี ontology เหมือนกัน',
                 ['พิพิธภัณฑ์สองแห่งเก็บของประเภทเดียวกันได้ แต่ถ้าแห่งหนึ่งมีภารกิจด้านการศึกษา '
                  'อีกแห่งมีภารกิจด้านการวิจัย เส้นที่ต้องลากก็ไม่เหมือนกัน',
                  'ontology สำเร็จรูปจึงตอบไม่ได้ทั้งสองแห่ง เราออกแบบจากภารกิจขององค์กร '
                  'ไม่ใช่จากแม่แบบของอุตสาหกรรม']),
                ('04', 'AI-Friendly — ทำให้ AI รู้ว่าองค์กรคุณต้องการอะไร',
                 ['AI ทั่วไปเดาจากรูปประโยค ส่วน AI ที่ทำงานบน knowledge graph '
                  'เดินตามเส้นที่องค์กรลากไว้เอง',
                  'คำตอบจึงสาวกลับไปหาหลักฐานได้ ถามซ้ำแล้วได้คำตอบเดิม '
                  'และไม่พูดเกินสิ่งที่องค์กรยืนยัน'])],
        creed='ontology ที่ตรงกับภารกิจ คือสิ่งที่ทำให้ AI ทำงานให้องค์กรได้ ไม่ใช่ทำงานแทนองค์กร',
        closer='ส่วนที่ยากของงานนี้จึงไม่ใช่เทคโนโลยี แต่คือการทำให้แต่ละแผนกตกลงกันว่าอะไรคืออะไร '
               'ซึ่งเป็นงานที่มีแต่คนขององค์กรเท่านั้นที่ทำได้',
        prev=('th-why-it-works.html', 'ทำไมมันถึงได้ผล'), next=('th-mkm-for-museums-and-libraries.html', 'MKM สำหรับพิพิธภัณฑ์และห้องสมุด'),
    ),
    en=dict(
        title='What an ontology and a knowledge graph actually are',
        desc='Two words appear on nearly every page of this site. This page explains them once, in plain language, with examples from real work.',
        eyebrow='Part 1 · The idea — 04 Two words',
        h1='What an ontology and a knowledge graph actually are',
        lede=['Two words appear on nearly every page of this site. This page explains them once, '
              'in plain language, and adds no further jargon.'],
        blocks=[('01', 'An ontology is an agreement about what you call things, and what relates to what',
                 ['A curator calls it an object. A conservator calls it a piece. The archive calls it '
                  'an item. The ontology is the document that says all three mean the same thing — '
                  'that this thing has a maker, a findspot, a previous owner, and what each of those '
                  'relationships means.',
                  'Written once. Used across the whole organisation.']),
                ('02', 'A knowledge graph is the real thing built to that ontology',
                 ['The ontology is the drawing. The graph is the building.',
                  'In a graph the connection between two things is not something you reconstruct in '
                  'every query. It is stored, it has a name and a direction, and it can be walked.']),
                ('03', 'Mission-driven — two organisations in the same field should not share one ontology',
                 ['Two museums can hold the same kinds of objects. But if one exists to teach and the '
                  'other exists to research, the lines worth drawing are different.',
                  'An off-the-shelf ontology therefore serves neither. We design from the '
                  "organisation's mission, not from an industry template."]),
                ('04', 'AI-friendly — it tells the AI what your organisation is for',
                 ['A general AI guesses from the shape of sentences. An AI working on your knowledge '
                  'graph follows the lines your own people drew.',
                  'So answers trace back to evidence, the same question returns the same answer, and '
                  'nothing is claimed beyond what the organisation stands behind.'])],
        creed='An ontology that matches the mission is what lets AI work for the organisation, rather '
              'than in place of it.',
        closer='Which makes the hard part of this work not technical. It is getting departments to agree '
               'on what things are — and only your own people can do that.',
        prev=('why-it-works.html', 'Why it works'), next=('mkm-for-museums-and-libraries.html', 'MKM for Museums & Libraries'),
    ),
)

# ── ภาค 2 · AI Sovereignty ───────────────────────────────────────
PAGES['sovereignty'] = dict(
    th=dict(
        title='เราสร้างคุณค่าบนข้อมูลของคุณ โดยข้อมูลไม่ออกจากองค์กร',
        desc='คำถามแรกของฝ่ายกฎหมายและฝ่ายระบบคือข้อมูลจะไปอยู่ที่ไหน คำตอบของเราสั้น คืออยู่ที่เดิม',
        eyebrow='ภาค 2 · โซลูชัน — ข้อมูลของคุณ',
        h1='เราสร้างคุณค่าบนข้อมูลของคุณ โดยข้อมูลไม่ออกจากองค์กร',
        lede=['คำถามแรกที่ฝ่ายกฎหมายและฝ่ายระบบถามเสมอ คือข้อมูลจะไปอยู่ที่ไหน',
              'คำตอบของเราสั้น คืออยู่ที่เดิม'],
        blocks=[('01', 'ชั้นความรู้อยู่ในบ้านของคุณ',
                 ['สร้างบนโครงสร้างพื้นฐานขององค์กร หรือใน tenancy ที่องค์กรถือเอง '
                  'ไม่ใช่บนระบบกลางที่เราถือไว้แล้วให้คุณเช่าใช้']),
                ('02', 'ไม่มีข้อมูลขององค์กรไปเป็นข้อมูลฝึกของ AI สาธารณะ',
                 ['ความรู้ขององค์กรถูกใช้เพื่อตอบคำถามขององค์กร ไม่ถูกส่งออกไปฝึกโมเดลของใคร '
                  'ทั้งของเราและของผู้ให้บริการรายอื่น']),
                ('03', 'เจ้าของคือองค์กร และนำออกได้เสมอ',
                 ['ทั้ง ontology schema และกราฟเป็นของคุณ ย้ายระบบได้ ย้ายผู้ให้บริการได้ '
                  'โดยไม่สูญเสียสิ่งที่สะสมไว้'])],
        creed='หลักนี้เรียกกันว่า AI Sovereignty และสำหรับองค์กรที่ถือความรู้ของสังคมไว้ '
              'มันไม่ใช่ฟีเจอร์ แต่เป็นเงื่อนไข',
        closer='เรื่องรายละเอียดตามกฎหมายคุ้มครองข้อมูลส่วนบุคคล ขึ้นกับลักษณะข้อมูลของแต่ละองค์กร '
               'เป็นเรื่องที่คุยกันในวงแรกได้เลย',
        prev=('th-what-we-wont-do.html', 'สิ่งที่เราไม่ทำ'), next=('th-reference-implementation.html', 'งานอ้างอิงที่เราทำเอง'),
    ),
    en=dict(
        title='We build value on your data, and your data stays with you',
        desc='The first question legal and IT ask is where the data goes. Our answer is short: it stays where it is.',
        eyebrow='Part 2 · The practice — Your data',
        h1='We build value on your data, and your data stays with you',
        lede=['The first question your legal and IT teams ask is where the data goes.',
              'Our answer is short. It stays where it is.'],
        blocks=[('01', 'The knowledge layer lives in your house',
                 ['Built on your own infrastructure, or in a tenancy your organisation holds — not on '
                  'a central system we own and rent back to you.']),
                ('02', 'Nothing of yours becomes training data for a public AI',
                 ["Your organisation's knowledge is used to answer your organisation's questions. It "
                  "is not sent out to train anyone's model — ours or a vendor's."]),
                ('03', 'You own it, and you can always take it out',
                 ['The ontology, the schema and the graph are yours. Change systems, change suppliers, '
                  'and lose none of what you have accumulated.'])],
        creed='This principle is called AI sovereignty. For an organisation that holds knowledge on '
              'behalf of the public, it is not a feature. It is a condition.',
        closer='How this maps onto your specific data-protection obligations depends on what you hold. '
               'That is a good subject for the first conversation.',
        prev=('what-we-wont-do.html', "What we won't do"), next=('reference-implementation.html', 'Reference implementation'),
    ),
)


def content_html(d, thai):
    blks = ''.join(block(n, h, ps) for n, h, ps in d['blocks'])
    cls = 'three' if len(d['blocks']) == 3 else ''
    ledes = ''.join(
        '<p class="lede"%s>%s</p>' % (' style="margin-top:16px;color:var(--fg)"' if i else '', t)
        for i, t in enumerate(d['lede']))
    return '''<section id="sec">
  <div class="wrap">
    <div class="eyebrow rv">%s</div>
    <div class="grid-2">
      <div class="rv"><h1>%s</h1></div>
      <div class="rv">%s</div>
    </div>
    <div class="blks %s">%s</div>
    <div class="creed rv"><p>%s</p></div>
    <p class="closer rv">%s</p>
  </div>
</section>
''' % (d['eyebrow'], d['h1'], ledes, cls, blks, d['creed'], d['closer'])


def make(shell_file, out_file, d, thai, base_en, base_th):
    s = io.open(os.path.join(W, shell_file), encoding='utf-8').read()
    canon = 'https://www.neogens.co/' + out_file
    s = re.sub(r'<title>.*?</title>', '<title>%s — Neo Gens</title>' % d['title'], s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content=".*?">',
               '<meta name="description" content="%s">' % d['desc'], s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content=".*?">',
               '<meta property="og:title" content="%s">' % d['title'], s, count=1, flags=re.S)
    s = re.sub(r'<meta property="og:description" content=".*?">',
               '<meta property="og:description" content="%s">' % d['desc'], s, count=1, flags=re.S)
    s = re.sub(r'<link rel="canonical" href=".*?">',
               '<link rel="canonical" href="%s">' % canon, s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="en" href=".*?">',
               '<link rel="alternate" hreflang="en" href="https://www.neogens.co/%s">' % base_en, s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="th" href=".*?">',
               '<link rel="alternate" hreflang="th" href="https://www.neogens.co/%s">' % base_th, s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="x-default" href=".*?">',
               '<link rel="alternate" hreflang="x-default" href="https://www.neogens.co/%s">' % base_en, s, count=1)
    s = re.sub(r'<meta property="og:url" content=".*?">',
               '<meta property="og:url" content="%s">' % canon, s, count=1)
    s = s.replace('</style>', (TH_CSS if thai else EXTRA_CSS) + '</style>', 1)

    a = s.index('<section id="why">')
    b = s.index('<div class="pn">')
    keep_cta = s[s.index('<section id="contact"'):b]
    s = s[:a] + content_html(d, thai) + keep_cta + s[b:]

    pv, nx = d['prev'], d['next']
    s = re.sub(r'<div class="pn"><div class="pn-in">.*?</div></div></div>',
               '<div class="pn"><div class="pn-in">'
               '<a class="pv" href="%s"><div class="k">%s</div><div class="t">%s</div></a>'
               '<a class="nx" href="%s"><div class="k">%s</div><div class="t">%s</div></a>'
               '</div></div>' % (pv[0], 'ก่อนหน้า' if thai else 'Previous', pv[1],
                                 nx[0], 'ถัดไป' if thai else 'Next', nx[1]),
               s, count=1, flags=re.S)
    io.open(os.path.join(W, out_file), 'w', encoding='utf-8').write(s)
    return out_file, len(s)


# ── 1. move the old museum-specific problem page to advantage.html ──
for src, dst in [('the-problem.html', 'what-you-are-holding.html'), ('th-the-problem.html', 'th-what-you-are-holding.html')]:
    s = io.open(os.path.join(W, src), encoding='utf-8').read()
    thai = dst.startswith('th-')
    canon = 'https://www.neogens.co/' + dst
    s = s.replace('https://www.neogens.co/' + src, canon)
    s = re.sub(r'<link rel="canonical" href=".*?">', '<link rel="canonical" href="%s">' % canon, s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="en" href=".*?">',
               '<link rel="alternate" hreflang="en" href="https://www.neogens.co/advantage.html">', s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="th" href=".*?">',
               '<link rel="alternate" hreflang="th" href="https://www.neogens.co/th-advantage.html">', s, count=1)
    s = re.sub(r'<link rel="alternate" hreflang="x-default" href=".*?">',
               '<link rel="alternate" hreflang="x-default" href="https://www.neogens.co/advantage.html">', s, count=1)
    # renumber the section label only — the prose is untouched
    s = s.replace('01 — ปัญหา', 'ภาค 2 · โซลูชัน — สิ่งที่คุณถืออยู่')
    s = s.replace('01 — The problem', 'Part 2 · The practice — What you are holding')
    io.open(os.path.join(W, dst), 'w', encoding='utf-8').write(s)
    print('moved  %-22s -> %-22s %d bytes' % (src, dst, len(s)))

# ── 2. build the new / rewritten pages ─────────────────────────────
for key, spec in PAGES.items():
    en = key + '.html'
    th = 'th-' + key + '.html'
    print('wrote  %-22s %d bytes' % make('why-it-works.html', en, spec['en'], False, en, th))
    print('wrote  %-22s %d bytes' % make('th-why-it-works.html', th, spec['th'], True, en, th))
