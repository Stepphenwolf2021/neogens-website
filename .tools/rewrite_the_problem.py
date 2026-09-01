# -*- coding: utf-8 -*-
"""เขียนเนื้อหาหน้า 01 · ปัญหา ใหม่ ทั้งสองภาษา · 2026-09-01

ฉบับไทยเป็นคำของ Noppadol ทุกตัวอักษร ยกมาตรงตามที่เขาส่งมา ห้ามเกลา
ฉบับอังกฤษเขียนสำนวนเอง เดินตามสาระเดียวกัน ไม่ได้แปลตรงตัว

รันซ้ำได้ ถ้ารันแล้วข้อความเก่าไม่อยู่ในไฟล์ สคริปต์จะหยุดพร้อมบอกว่าจุดไหนไม่เจอ
ห้ามใช้ build_sections.py กับหน้านี้ ตัวนั้นรันไม่ได้แล้ว พาธในไฟล์ชี้ไป sandbox ที่ไม่มีอยู่
"""
import io, os, re, sys

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── ฉบับไทย · คำของ Noppadol ยกมาตรง ๆ ────────────────────────────
TH = [
 # (ข้อความเดิมในไฟล์, ข้อความใหม่)
 ('ทุกองค์กรกำลังเอา AI มาใช้ และเกือบทุกแห่งเอามันไปวางทับกองเอกสารของตัวเองตรง ๆ',
  'ทุกองค์กรกำลังเอา AI มาใช้ และเกือบทุกแห่งเอามันไปวางทับบนกองเอกสารของตัวเองตรง ๆ'),
 ('ใช้ได้ดี จนถึงวินาทีที่คำตอบนั้นสำคัญจริง<',
  'ใช้ได้ดี จนถึงวินาทีที่คำตอบนั้นสำคัญจริง ๆ ต่อธุรกิจคุณ<'),
 ('ไม่มีใครออกแบบให้ความรู้แต่ละชิ้นเชื่อมกันตั้งแต่ต้น ยิ่งนานวันกล่องยิ่งมากขึ้น '
  'รูปแบบยิ่งหลากหลาย จนไม่มีสมองใครไล่ความสัมพันธ์ทั้งหมดไหว',
  'ไม่มีใครออกแบบให้ความรู้แต่ละชิ้นเชื่อมกันตั้งแต่ต้น ยิ่งนานวันกล่องเก็บความรู้ยิ่งมากขึ้น '
  'รูปแบบยิ่งหลากหลาย จนไม่มีสมองมนุษย์คนไหนไล่หาความสัมพันธ์ทั้งหมดได้'),
 ('LLM ทำงานบนสถิติว่าคำถัดไปน่าจะเป็นคำอะไร มันตอบถูกเพราะเคยผ่านตาการเรียงแบบนี้'
  'มาแล้วนับล้านครั้ง ไม่ใช่เพราะรู้จักองค์กรของคุณ',
  'LLM ทำงานบนสถิติว่าคำถัดไปน่าจะเป็นคำอะไร มันตอบถูกเพราะเคยผ่านตาการเรียงตัวอักษรแบบนี้'
  'มาแล้วนับล้านครั้ง ไม่ใช่เพราะมันเข้าใจว่าคุณต้องการอะไร'),
 ('คำตอบที่สาวกลับไม่ได้ ออกไปในนามคุณ',
  'คำตอบที่สืบย้อนกลับไปไม่ได้ ถูกประกาศออกไปในนามคุณ'),
 ('ทุกคำตอบที่ AI ให้แทนองค์กร คือคำแถลงขององค์กร ตอบผิดครั้งเดียว '
  'ความเชื่อมั่นที่สะสมมานานก็สั่นคลอน',
  'ทุกคำตอบที่ AI ให้ตอบในที่สาธารณะ คือคำแถลงขององค์กร ตอบผิดเพียงครั้งเดียว '
  'ความเชื่อมั่นที่สะสมมานานก็สั่นคลอน'),
 ('เราเชื่อว่าความสำเร็จขององค์กร วัดกันที่ความสามารถในการบริหารสินทรัพย์ที่ชื่อว่าข้อมูลและความรู้ '
  'ให้สร้างคุณค่าได้จริง ทั้งกับองค์กรเอง ลูกค้า คู่ค้า สังคม ประเทศ และโลก',
  'เราเชื่อว่าความสำเร็จขององค์กร ขึ้นกับความสามารถในการบริหารสินทรัพย์ข้อมูลและความรู้ '
  'ให้สร้างคุณค่าได้จริง ทั้งกับองค์กรเอง ลูกค้า คู่ค้า สังคม ประเทศ และโลก'),
 ('สิ่งที่ขาดจึงไม่ใช่ AI ที่เก่งขึ้น แต่คือชั้นที่บอกว่าองค์กรนี้รู้อะไร รู้มาได้อย่างไร '
  'และให้ความสำคัญกับอะไร',
  'สิ่งที่ขาดหายไปจึงไม่ใช่ AI ที่เก่งขึ้น แต่คือชั้นความรู้ที่อยู่ระหว่าง AI กับความรู้ขององค์กร'
  ' เพื่อสื่อสารกับ AI ว่าองค์กรนี้รู้อะไร รู้มาได้อย่างไร และให้ความสำคัญกับอะไร'),
 # meta · og · ให้ตามคำใหม่ของเขา
 ('ทุกองค์กรกำลังเอา AI ไปวางทับกองเอกสารของตัวเองตรง ๆ ใช้ได้ดี จนถึงวินาทีที่คำตอบนั้นสำคัญจริง',
  'ทุกองค์กรกำลังเอา AI ไปวางทับบนกองเอกสารของตัวเองตรง ๆ ใช้ได้ดี จนถึงวินาทีที่คำตอบนั้นสำคัญจริง ๆ ต่อธุรกิจคุณ'),
]

# ── ฉบับอังกฤษ · เขียนสำนวนเอง ให้สาระตรงกับฉบับไทย ────────────────
EN = [
 ('That works, right up to the moment the answer matters.<',
  'That works, right up to the moment the answer really matters to your business.<'),
 ('None of this knowledge was designed to connect in the first place. Each year adds more boxes '
  'and more formats, until no human mind can hold the relationships between them.',
  'None of this knowledge was designed to connect in the first place. Each year adds more boxes '
  'of knowledge and more formats, until no human mind can trace all the relationships between them.'),
 ('A better guess is not understanding',
  'A better guess does not mean it understands you'),
 ('It answers correctly because it has met that sequence a million times before, not because it '
  'knows anything about your organisation.',
  'It answers correctly because it has met that sequence of characters a million times before, '
  'not because it understands what you need.'),
 ('An answer nobody can trace still goes out in your name',
  'An answer nobody can trace back is published in your name'),
 ('Every answer an AI gives on your behalf is a statement by the organisation. One wrong answer '
  'shakes trust that took decades to build.',
  'Every answer an AI gives in public is a statement by the organisation. One wrong answer shakes '
  'trust that took decades to build.'),
 ('how well it manages the asset called knowledge, so that it creates real value',
  'how well it manages the assets called data and knowledge, so that they create real value'),
 ('It is the layer that records what this organisation knows, how it came to know it, and what it '
  'exists to do.',
  'It is the knowledge layer that sits between the AI and what the organisation knows, and tells '
  'the AI what this organisation knows, how it came to know it, and what it holds important.'),
 ('Almost every organisation points AI straight at its own pile of documents. That works, right up '
  'to the moment the answer matters.',
  'Almost every organisation points AI straight at its own pile of documents. That works, right up '
  'to the moment the answer really matters to your business.'),
]


def apply(fname, pairs):
    p = os.path.join(W, fname)
    s = io.open(p, encoding='utf-8').read()
    orig = s
    missing, hits = [], 0
    for old, new in pairs:
        n = s.count(old)
        if n == 0:
            if new in s:                      # รันซ้ำ ของใหม่อยู่แล้ว
                hits += 1
                continue
            missing.append(old[:60])
            continue
        s = s.replace(old, new)
        hits += n
    if missing:
        sys.exit('%s · หาข้อความเดิมไม่เจอ %d จุด\n  %s' % (fname, len(missing), '\n  '.join(missing)))

    checks = {
        'ข้อความใหม่เข้าครบ': all(new in s for _, new in pairs),
        'ข้อความเก่าไม่เหลือ': not any(old in s for old, new in pairs if old != new and old not in new),
        'แท็กสมดุล': s.count('<div') == s.count('</div>')
                     and len(re.findall(r'<p\b', s)) == s.count('</p>'),
        'ปีกกาใน style สมดุล': s[:s.index('</head>')].count('{') == s[:s.index('</head>')].count('}'),
        'โครงหน้ายังครบ': all(x in s for x in ['<h1', 'class="blk', 'class="creed', 'class="closer', '</footer>']),
        'ไฟล์ไม่หด': len(s) >= len(orig) - 200,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        sys.exit('%s · ไม่ผ่าน: %s' % (fname, ', '.join(bad)))
    io.open(p, 'w', encoding='utf-8').write(s)
    return hits, len(s) - len(orig)


for f, pairs in [('th-the-problem.html', TH), ('the-problem.html', EN)]:
    hits, delta = apply(f, pairs)
    print('  เขียนใหม่ %-22s · แทนที่ %2d จุด · %+d ตัวอักษร' % (f, hits, delta))
print('✓ สองภาษาเดินตามสาระเดียวกัน · ฉบับไทยเป็นคำของ Noppadol ไม่ได้เกลา')
