# -*- coding: utf-8 -*-
"""Generate the Coffee Belt map as an original inline SVG.

Coastlines come from the GSHHS low-resolution dataset shipped with basemap-data
(public domain). Nothing is traced from any third-party image.
Output: two SVG fragments (EN + TH) written next to the build script.
"""
import io, os, struct
from shapely.geometry import Polygon

D = '/sessions/practical-pensive-rubin/.local/lib/python3.10/site-packages/mpl_toolkits/basemap_data'
DAT = os.path.join(D, 'gshhs_l.dat')
META = os.path.join(D, 'gshhsmeta_l.dat')

MIN_AREA = 900.0          # km² — drops specks, keeps Sri Lanka / Jamaica / Bali
SIMPLIFY = 0.34           # degrees
LON0, LON1 = -180.0, 180.0
LAT_TOP, LAT_BOT = 84.0, -58.0        # crop Antarctica and the high Arctic

# canvas
W, H = 1140.0, 622.0
MX, MY = 40.0, 104.0                  # map origin
MW = W - 2 * MX
MH = MW * (LAT_TOP - LAT_BOT) / (LON1 - LON0)

TROPIC = 23.4366


def x_of(lon):
    return MX + (lon - LON0) / (LON1 - LON0) * MW


def y_of(lat):
    return MY + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MH


def load_polygons():
    raw = io.open(DAT, 'rb').read()
    polys = []
    for line in io.open(META, encoding='latin-1'):
        f = line.split()
        if len(f) < 7:
            continue
        level = int(f[0])
        area = float(f[1])
        npts = int(f[2])
        south = float(f[3])
        north = float(f[4])
        off = int(f[5])
        nbytes = int(f[6])
        if level != 1 or area < MIN_AREA:
            continue
        if south > LAT_TOP or north < LAT_BOT:
            continue
        vals = struct.unpack('<%df' % (npts * 2), raw[off:off + nbytes])
        pts = list(zip(vals[0::2], vals[1::2]))
        if len(pts) < 4:
            continue
        try:
            p = Polygon(pts)
            if not p.is_valid:
                p = p.buffer(0)
            p = p.simplify(SIMPLIFY, preserve_topology=True)
        except Exception:
            continue
        if p.is_empty:
            continue
        for g in (p.geoms if p.geom_type == 'MultiPolygon' else [p]):
            if g.area <= 0:
                continue
            polys.append(list(g.exterior.coords))
    return polys


def path_d(rings):
    out = []
    for ring in rings:
        seg = []
        for lon, lat in ring:
            lat = max(LAT_BOT - 2, min(LAT_TOP + 2, lat))
            seg.append('%.1f %.1f' % (x_of(lon), y_of(lat)))
        out.append('M' + 'L'.join(seg) + 'Z')
    return ''.join(out)


TXT = {
    'en': dict(
        title='The Coffee Belt',
        sub='Coffee grows in one band of the world — between the Tropic of Cancer and the Tropic of Capricorn.',
        cancer='TROPIC OF CANCER · 23.5°N',
        equator='EQUATOR · 0°',
        capricorn='TROPIC OF CAPRICORN · 23.5°S',
        legend='Latitudes where coffee is grown',
        cap='The Coffee Belt — the latitudes every origin in this article sits inside.',
        serif="'Charter','Iowan Old Style',Georgia,serif",
        sans="'Helvetica Neue',Arial,sans-serif",
    ),
    'th': dict(
        title='แถบกาแฟของโลก',
        sub='กาแฟปลูกได้ในแถบเดียวของโลก คือระหว่างเส้นทรอปิกออฟแคนเซอร์กับทรอปิกออฟแคปริคอร์น',
        cancer='TROPIC OF CANCER · 23.5°N',
        equator='EQUATOR · เส้นศูนย์สูตร',
        capricorn='TROPIC OF CAPRICORN · 23.5°S',
        legend='ละติจูดที่ปลูกกาแฟได้',
        cap='แถบกาแฟของโลก — ละติจูดที่แหล่งปลูกทุกแห่งในบทความนี้อยู่ข้างใน',
        serif="'IBM Plex Sans Thai',Georgia,serif",
        sans="'IBM Plex Sans Thai','Helvetica Neue',Arial,sans-serif",
    ),
}

BEAN = ('<g transform="translate(%(bx).1f %(by).1f)">'
        '<ellipse rx="9" ry="6.4" fill="#8a5238"/>'
        '<path d="M-7.4 -2.6 C-2.6 1.9 2.6 -1.9 7.4 2.6" fill="none" '
        'stroke="#faf9f7" stroke-width="1.5" stroke-linecap="round"/></g>')


def build(lang, rings):
    t = TXT[lang]
    land = path_d(rings)
    yC, yE, yP = y_of(TROPIC), y_of(0.0), y_of(-TROPIC)
    s = []
    a = s.append
    a('<svg preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" '
      'viewBox="0 0 %g %g" width="100%%" role="img" aria-label="%s">' % (W, H, t['title']))
    a('<defs>')
    a('<clipPath id="beltclip-%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>'
      % (lang, MX, yC, MW, yP - yC))
    a('<path id="land-%s" d="%s"/>' % (lang, land))
    a('</defs>')
    a('<rect width="%g" height="%g" fill="#faf9f7"/>' % (W, H))
    # titles
    a('<text x="%.0f" y="46" font-family=%s font-size="21" font-weight="700" fill="#1c1a17">%s</text>'
      % (MX, '"%s"' % t['serif'], t['title']))
    a('<text x="%.0f" y="76" font-family=%s font-size="15" fill="#8a7f70">%s</text>'
      % (MX, '"%s"' % t['serif'], t['sub']))
    # ocean panel
    a('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="#f2f0ea"/>'
      % (MX, MY, MW, MH))
    # belt band behind the land
    a('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#faf2dd"/>'
      % (MX, yC, MW, yP - yC))
    # land outside the belt
    a('<use href="#land-%s" fill="#dcd6c8"/>' % lang)
    # land inside the belt
    a('<use href="#land-%s" fill="#8a5238" clip-path="url(#beltclip-%s)"/>' % (lang, lang))
    # latitude lines
    a('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1c1a17" stroke-width="1.2"/>'
      % (MX, yC, MX + MW, yC))
    a('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#1c1a17" stroke-width="1.2"/>'
      % (MX, yP, MX + MW, yP))
    a('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8a7f70" stroke-width="1" '
      'stroke-dasharray="5 5"/>' % (MX, yE, MX + MW, yE))
    # line labels
    lab = ('<text x="%.1f" y="%.1f" text-anchor="end" font-family="%s" font-size="10.5" '
           'letter-spacing="0.1em" fill="%s">%s</text>')
    a(lab % (MX + MW - 8, yC - 7, t['sans'], '#1c1a17', t['cancer']))
    a(lab % (MX + MW - 8, yE - 7, t['sans'], '#8a7f70', t['equator']))
    a(lab % (MX + MW - 8, yP + 16, t['sans'], '#1c1a17', t['capricorn']))
    # frame
    a('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="10" fill="none" '
      'stroke="#c4bcae" stroke-width="1"/>' % (MX, MY, MW, MH))
    # legend
    ly = MY + MH + 36
    a(BEAN % dict(bx=MX + 9, by=ly - 4))
    a('<rect x="%.1f" y="%.1f" width="26" height="11" rx="2.5" fill="#8a5238"/>'
      % (MX + 26, ly - 9.5))
    a('<text x="%.1f" y="%.1f" font-family="%s" font-size="12.5" fill="#5f584e">%s</text>'
      % (MX + 60, ly, t['sans'], t['legend']))
    a('</svg>')
    return ''.join(s), t['cap']


rings = load_polygons()
print('land rings:', len(rings), '· points:', sum(len(r) for r in rings))
out = {}
for lang in ('en', 'th'):
    svg, cap = build(lang, rings)
    out[lang] = (svg, cap)
    print(lang, 'svg bytes:', len(svg))

io.open('/sessions/practical-pensive-rubin/mnt/outputs/coffee_belt_en.svg', 'w',
        encoding='utf-8').write(out['en'][0])
io.open('/sessions/practical-pensive-rubin/mnt/outputs/coffee_belt_th.svg', 'w',
        encoding='utf-8').write(out['th'][0])

with io.open('/sessions/practical-pensive-rubin/mnt/outputs/coffee_belt_frag.py', 'w',
             encoding='utf-8') as fh:
    fh.write('# -*- coding: utf-8 -*-\n# generated by make_coffee_belt.py — do not hand-edit\n')
    fh.write('HERO = {\n')
    for lang in ('en', 'th'):
        svg, cap = out[lang]
        fh.write('  %r: (%r, %r),\n' % (lang, svg, cap))
    fh.write('}\n')
print('wrote fragments')
