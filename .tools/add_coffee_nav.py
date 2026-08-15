# -*- coding: utf-8 -*-
"""Add the MKM for Coffee entry to nav / drawer / footer on every page.

Region-scoped so the within-practice-area pager on visit.html is left alone.
No prose is rewritten; only navigation labels and links change.
"""
import glob, io, re, sys

SKIP = {'coffee.html', 'th-coffee.html', '404.html', 'km-for-museums.html'}

EN = dict(
    visit_re=r'<a[^>]*href="visit\.html"[^>]*>MKM for Museums &amp; Libraries</a>',
    museums_re=r'<a[^>]*href="museums\.html"[^>]*>03 · What leadership looks like</a>',
    coffee='<a href="coffee.html">MKM for Coffee</a>',
    old_h='<div class="h">First practice area</div>',
    new_h='<div class="h">Practice areas</div>',
    hub_card='<a href="coffee.html"><div class="n">MKM for Coffee</div>'
             '<div class="t">The industry is drowning in data and starving for knowledge</div></a>',
)
TH = dict(
    visit_re=r'<a[^>]*href="th-visit\.html"[^>]*>MKM สำหรับพิพิธภัณฑ์และห้องสมุด</a>',
    museums_re=r'<a[^>]*href="th-museums\.html"[^>]*>03 · ความเป็นผู้นำหน้าตาเป็นอย่างไร</a>',
    coffee='<a href="th-coffee.html">MKM สำหรับกาแฟ</a>',
    old_h='<div class="h">โดเมนแรก</div>',
    new_h='<div class="h">โดเมนที่ทำ</div>',
    hub_card='<a href="th-coffee.html"><div class="n">MKM สำหรับกาแฟ</div>'
             '<div class="t">แปลงเดียว ถูกสำรวจสามรอบ แล้วไม่มีใครได้ความรู้เพิ่ม</div></a>',
)


def region(s, start_marker, end_marker, frm=0):
    a = s.find(start_marker, frm)
    if a < 0:
        return None
    b = s.find(end_marker, a)
    if b < 0:
        return None
    return a, b + len(end_marker)


def sub_once(text, pattern, repl_fn, where, log):
    m = re.search(pattern, text)
    if not m:
        log.append('   ! no match in %s' % where)
        return text, False
    return text[:m.end()] + repl_fn() + text[m.end():], True


def process(f):
    s = io.open(f, encoding='utf-8').read()
    orig = s
    C = TH if f.startswith('th-') else EN
    log = []

    # ---- 1. top nav links ------------------------------------------------
    r = region(s, '<div class="nav-links">', '</div>')
    if r:
        a, b = r
        seg = s[a:b]
        if 'coffee.html' not in seg:
            seg2, ok = sub_once(seg, C['visit_re'], lambda: C['coffee'], 'nav-links', log)
            if ok:
                log.append('   nav-links +coffee')
            s = s[:a] + seg2 + s[b:]

    # ---- 2. drawer -------------------------------------------------------
    r = region(s, '<div class="drawer" id="drawer">', '</nav>')
    if r:
        a, b = r
        seg = s[a:b]
        if C['old_h'] in seg:
            seg = seg.replace(C['old_h'], C['new_h'])
            log.append('   drawer heading renamed')
        if 'coffee.html' not in seg:
            seg, ok = sub_once(seg, C['museums_re'], lambda: C['coffee'], 'drawer', log)
            if ok:
                log.append('   drawer +coffee')
        s = s[:a] + seg + s[b:]

    # ---- 3. footer -------------------------------------------------------
    r = region(s, '<footer>', '</footer>')
    if r:
        a, b = r
        seg = s[a:b]
        if C['old_h'] in seg:
            seg = seg.replace(C['old_h'], C['new_h'])
            log.append('   footer heading renamed')
        if 'coffee.html' not in seg and re.search(C['museums_re'], seg):
            seg, ok = sub_once(seg, C['museums_re'], lambda: C['coffee'], 'footer', log)
            if ok:
                log.append('   footer +coffee')
        s = s[:a] + seg + s[b:]

    # ---- 4. homepage hub card -------------------------------------------
    hub_start = '<div class="hg">' + C['old_h']
    if hub_start in s:
        a = s.find(hub_start)
        b = s.find('</div></div>', a)
        seg = s[a:b]
        seg = seg.replace(C['old_h'], C['new_h'])
        if 'coffee.html' not in seg:
            seg = seg + C['hub_card']
            log.append('   hub card +coffee')
        s = s[:a] + seg + s[b:]

    # ---- 5. nav breakpoint: 5 links no longer fit at 960px ---------------
    for old, new in [('@media(min-width:961px){.drawer{display:none!important}}',
                      '@media(min-width:1121px){.drawer{display:none!important}}'),
                     ('@media(max-width:960px){\n  .nav-links{display:none!important}',
                      '@media(max-width:1120px){\n  .nav-links{display:none!important}'),
                     ('@media(max-width:960px){.nav-links a:not(.btn){display:none}}',
                      '@media(max-width:1120px){.nav-links a:not(.btn){display:none}}')]:
        if old in s:
            s = s.replace(old, new)
            log.append('   breakpoint 960->1120')

    # ---- 6. tighten nav so five labels fit -------------------------------
    s2 = re.sub(r'\.nav-links\{display:flex;gap:22px', '.nav-links{display:flex;gap:19px', s)
    if s2 != s:
        log.append('   nav gap 22->19')
        s = s2
    s2 = re.sub(r'(\.nav-links a\{font-size:)14px', r'\g<1>13.5px', s)
    if s2 != s:
        log.append('   nav font 14->13.5')
        s = s2

    if s != orig:
        io.open(f, 'w', encoding='utf-8').write(s)
    return log


changed = 0
for f in sorted(glob.glob('*.html')):
    if f in SKIP:
        print('%-38s skipped' % f)
        continue
    log = process(f)
    if log:
        changed += 1
    print('%-38s %s' % (f, ' ·'.join(x.strip() for x in log) if log else 'no change'))
print('\nfiles changed:', changed)
