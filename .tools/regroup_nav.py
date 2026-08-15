# -*- coding: utf-8 -*-
"""Regroup nav / drawer / footer into the three parts.

Only navigation labels and links change. No prose is touched.
"""
import glob, io, re, os

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'404.html', 'km-for-museums.html'}

EN = dict(
    home='index.html', other='th-index.html', lang='EN', olang='TH',
    cta=('contact.html', 'Request a briefing'),
    top=[('problem.html', 'The idea'),
         ('visit.html', 'MKM for Museums &amp; Libraries'),
         ('coffee.html', 'MKM for Coffee'),
         ('engagement.html', 'Engagement'),
         ('about.html', 'Who we are')],
    all_label='All sections',
    groups=[
        ('Part 1 · The idea', [
            ('problem.html', '01 · The problem'),
            ('what.html', '02 · What it is'),
            ('why.html', '03 · Why it works'),
            ('layer.html', '04 · Ontology &amp; knowledge graph')]),
        ('Part 2 · Museums &amp; libraries', [
            ('advantage.html', 'What you are holding'),
            ('visit.html', '01 · Where things stand'),
            ('experience.html', '02 · Visitors and readers'),
            ('museums.html', '03 · What leadership looks like'),
            ('services.html', 'What we do together'),
            ('engagement.html', 'Engagement'),
            ('sovereignty.html', 'Your data · AI sovereignty'),
            ('proof.html', 'Reference implementation'),
            ('honest.html', "What we won't do"),
            ('km-for-museums-and-libraries.html', 'Long read: MKM for museums &amp; libraries')]),
        ('Part 3 · Public goods', [
            ('coffee.html', 'MKM for Coffee'),
            ('coffee-farmer.html', 'For coffee farmers')]),
        ('&nbsp;', [
            ('about.html', 'Who we are')]),
    ],
    fcols=[
        ('Part 1 · The idea', [('problem.html', 'The problem'), ('what.html', 'What it is'),
                               ('why.html', 'Why it works'), ('layer.html', 'Ontology &amp; knowledge graph')]),
        ('Part 2 · Museums &amp; libraries', [('advantage.html', 'What you are holding'),
                                              ('visit.html', 'Where things stand'),
                                              ('experience.html', 'Visitors and readers'),
                                              ('museums.html', 'What leadership looks like')]),
        ('Part 2 · Working together', [('services.html', 'What we do together'),
                                       ('engagement.html', 'Engagement'),
                                       ('sovereignty.html', 'Your data · AI sovereignty'),
                                       ('proof.html', 'Reference implementation'),
                                       ('honest.html', "What we won't do")]),
        ('Part 3 &amp; company', [('coffee.html', 'MKM for Coffee'),
                                  ('coffee-farmer.html', 'For coffee farmers'),
                                  ('about.html', 'Who we are'),
                                  ('mailto:hello@neogens.co', 'hello@neogens.co'),
                                  ('km-for-museums-and-libraries.html', 'Long read: MKM for museums &amp; libraries'),
                                  ('th-index.html', 'ฉบับภาษาไทย')]),
    ],
)

TH = dict(
    home='th-index.html', other='index.html', lang='TH', olang='EN',
    cta=('th-contact.html', 'ขอนัดหารือ'),
    top=[('th-problem.html', 'แนวคิด'),
         ('th-visit.html', 'MKM สำหรับพิพิธภัณฑ์และห้องสมุด'),
         ('th-coffee.html', 'MKM สำหรับกาแฟ'),
         ('th-engagement.html', 'รูปแบบการทำงาน'),
         ('th-about.html', 'เราคือใคร')],
    all_label='สารบัญทั้งหมด',
    groups=[
        ('ภาค 1 · แนวคิด', [
            ('th-problem.html', '01 · ปัญหา'),
            ('th-what.html', '02 · สิ่งนี้คืออะไร'),
            ('th-why.html', '03 · ทำไมมันถึงได้ผล'),
            ('th-layer.html', '04 · ontology กับ knowledge graph')]),
        ('ภาค 2 · พิพิธภัณฑ์และห้องสมุด', [
            ('th-advantage.html', 'สิ่งที่คุณถืออยู่'),
            ('th-visit.html', '01 · สถานะวันนี้'),
            ('th-experience.html', '02 · ผู้ชมและผู้อ่าน'),
            ('th-museums.html', '03 · ความเป็นผู้นำหน้าตาเป็นอย่างไร'),
            ('th-services.html', 'เราทำอะไรร่วมกัน'),
            ('th-engagement.html', 'รูปแบบการทำงาน'),
            ('th-sovereignty.html', 'ข้อมูลของคุณ · AI Sovereignty'),
            ('th-proof.html', 'งานอ้างอิงที่เราทำเอง'),
            ('th-honest.html', 'สิ่งที่เราไม่ทำ'),
            ('km-for-museums-and-libraries.html', 'บทความยาว: MKM สำหรับพิพิธภัณฑ์และห้องสมุด')]),
        ('ภาค 3 · โครงการเพื่อสาธารณะ', [
            ('th-coffee.html', 'MKM สำหรับกาแฟ'),
            ('th-coffee-farmer.html', 'สำหรับคนปลูกกาแฟ')]),
        ('&nbsp;', [
            ('th-about.html', 'เราคือใคร')]),
    ],
    fcols=[
        ('ภาค 1 · แนวคิด', [('th-problem.html', 'ปัญหา'), ('th-what.html', 'สิ่งนี้คืออะไร'),
                            ('th-why.html', 'ทำไมมันถึงได้ผล'), ('th-layer.html', 'ontology กับ knowledge graph')]),
        ('ภาค 2 · พิพิธภัณฑ์และห้องสมุด', [('th-advantage.html', 'สิ่งที่คุณถืออยู่'),
                                          ('th-visit.html', 'สถานะวันนี้'),
                                          ('th-experience.html', 'ผู้ชมและผู้อ่าน'),
                                          ('th-museums.html', 'ความเป็นผู้นำหน้าตาเป็นอย่างไร')]),
        ('ภาค 2 · การทำงานร่วมกัน', [('th-services.html', 'เราทำอะไรร่วมกัน'),
                                    ('th-engagement.html', 'รูปแบบการทำงาน'),
                                    ('th-sovereignty.html', 'ข้อมูลของคุณ · AI Sovereignty'),
                                    ('th-proof.html', 'งานอ้างอิงที่เราทำเอง'),
                                    ('th-honest.html', 'สิ่งที่เราไม่ทำ')]),
        ('ภาค 3 และบริษัท', [('th-coffee.html', 'MKM สำหรับกาแฟ'),
                            ('th-coffee-farmer.html', 'สำหรับคนปลูกกาแฟ'),
                            ('th-about.html', 'เราคือใคร'),
                            ('mailto:hello@neogens.co', 'hello@neogens.co'),
                            ('km-for-museums-and-libraries.html', 'บทความยาว: MKM สำหรับพิพิธภัณฑ์และห้องสมุด'),
                            ('index.html', 'English edition')]),
    ],
)


def a(href, label, cur):
    on = ' class="on"' if href == cur else ''
    return '<a%s href="%s">%s</a>' % (on, href, label)


def build_navlinks(C, cur, tgl):
    links = ''.join(a(h, l, cur) for h, l in C['top'])
    lang = ('<span class="lang"><a class="on" href="%s">%s</a><span>/</span><a href="%s">%s</a></span>'
            % (cur, C['lang'], other_of(cur), C['olang']))
    return links + lang + tgl + '<a class="btn" href="%s">%s</a>' % C['cta']


def other_of(cur):
    """The same page in the other language — falls back to that language's
    home page for shared pages such as the English-only long read."""
    alt = cur[3:] if cur.startswith('th-') else 'th-' + cur
    if os.path.exists(os.path.join(W, alt)):
        return alt
    return 'th-index.html' if not cur.startswith('th-') else 'index.html' 


def build_drawer(C, cur):
    out = ['<a href="%s">%s</a>' % (C['home'], C['all_label'])]
    for h, items in C['groups']:
        out.append('<div class="h">%s</div>' % h)
        out += [a(hr, lb, cur) for hr, lb in items]
    out.append('<a class="btn" href="%s">%s</a>' % C['cta'])
    return '<div class="drawer" id="drawer"><div class="dw">%s</div></div>' % ''.join(out)


def build_fcols(C):
    cols = []
    for h, items in C['fcols']:
        inner = '<div class="h">%s</div>' % h
        if 'company' in h.lower() or 'บริษัท' in h:
            inner += '<p>Neo Gens Co., Ltd.</p>'
        inner += ''.join('<a href="%s">%s</a>' % (hr, lb) for hr, lb in items)
        cols.append('<div class="f-col">%s</div>' % inner)
    return '<div class="f-cols">%s</div>' % ''.join(cols)


def region(s, start, end):
    i = s.find(start)
    if i < 0:
        return None
    j = s.find(end, i)
    return (i, j + len(end)) if j >= 0 else None


n = 0
for f in sorted(glob.glob(os.path.join(W, '*.html'))):
    name = os.path.basename(f)
    if name in SKIP:
        continue
    s = io.open(f, encoding='utf-8').read()
    orig = s
    C = TH if name.startswith('th-') else EN
    cur = name

    # top nav links — keep the existing theme-toggle markup exactly as it is
    r = region(s, '<div class="nav-links">', '</div>')
    if r:
        seg = s[r[0]:r[1]]
        m = re.search(r'<button class="tgl".*?</button>', seg, re.S)
        if m:
            s = s[:r[0]] + '<div class="nav-links">' + build_navlinks(C, cur, m.group(0)) + '</div>' + s[r[1]:]

    # drawer
    r = region(s, '<div class="drawer" id="drawer">', '</nav>')
    if r:
        s = s[:r[0]] + build_drawer(C, cur) + '\n</nav>' + s[r[1]:]

    # footer columns
    r = region(s, '<div class="f-cols">', '</div></div>')
    if r:
        j = s.find('</div>', s.find('<div class="f-cols">'))
        # find the true end of f-cols by counting
        start = s.find('<div class="f-cols">')
        depth, k = 0, start
        while k < len(s):
            if s.startswith('<div', k):
                depth += 1
            elif s.startswith('</div>', k):
                depth -= 1
                if depth == 0:
                    k += 6
                    break
            k += 1
        s = s[:start] + build_fcols(C) + s[k:]

    if s != orig:
        io.open(f, 'w', encoding='utf-8').write(s)
        n += 1
        print('  regrouped %s' % name)
print('\nfiles changed:', n)
