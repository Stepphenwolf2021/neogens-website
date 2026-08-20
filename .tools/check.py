# -*- coding: utf-8 -*-
import io,os,re,glob,sys,json,html as _html,unicodedata
from html.parser import HTMLParser
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
errs=[];warns=[]
def E(f,m): errs.append((f,m))
def W(f,m): warns.append((f,m))

class P(HTMLParser):
    def __init__(s,f): super().__init__(convert_charrefs=True); s.f=f; s._se=False; s.st=[]; s.ids=[]; s.hrefs=[]; s.text=[]; s.vis=[]
    def handle_starttag(s,t,a):
        d=dict(a)
        if 'id' in d: s.ids.append(d['id'])
        if 'href' in d: s.hrefs.append(d['href'])
        for k in ('title','alt','aria-label','content','placeholder'):
            if k in d and d[k]: s.text.append(d[k])
        if t not in VOID and not s._se: s.st.append((t,s.getpos()))
        s._se=False
    def handle_startendtag(s,t,a):
        s._se=True; s.handle_starttag(t,a)
    def handle_endtag(s,t):
        if t in VOID: return
        if not s.st: E(s.f,'stray </%s> at %s'%(t,s.getpos())); return
        if s.st[-1][0]!=t:
            E(s.f,'</%s> closes <%s> opened at line %d'%(t,s.st[-1][0],s.st[-1][1][0])); 
            for i in range(len(s.st)-1,-1,-1):
                if s.st[i][0]==t: del s.st[i:]; return
            return
        s.st.pop()
    def handle_data(s,d): s.text.append(d); s.vis.append(d)

files=sorted(glob.glob('*.html'))
parsed={}
for f in files:
    src=io.open(f,encoding='utf-8').read()
    body=re.sub(r'<script[^>]*>.*?</script>','',src,flags=re.S)
    body=re.sub(r'<style>.*?</style>','',body,flags=re.S)
    p=P(f); p.feed(body); p.close()
    if p.st: E(f,'unclosed: '+', '.join('<%s> line %d'%(t,l[0]) for t,l in p.st[-4:]))
    parsed[f]=(src,p)
    dup=[i for i in set(p.ids) if p.ids.count(i)>1]
    if dup: E(f,'duplicate id: '+', '.join(dup))

# --- link integrity ---
for f,(src,p) in parsed.items():
    for h in set(p.hrefs):
        if h.startswith(('http://','https://','mailto:','tel:','#')): 
            if h.startswith('#') and h[1:] and h[1:] not in p.ids: E(f,'dead in-page anchor %s'%h)
            continue
        tgt=h.split('#')[0].split('?')[0]
        if not tgt: continue
        path=tgt.lstrip('/') or 'index.html'
        if path.endswith('/'): path+='index.html'
        if not os.path.exists(path): E(f,'missing link target: %s'%h)
        frag=h.split('#')[1] if '#' in h else ''
        if frag and os.path.exists(path):
            if ('id="%s"'%frag) not in io.open(path,encoding='utf-8').read(): E(f,'dead fragment %s'%h)

# --- เลขในป้ายหมวดบนหน้า ต้องตรงกับเลขที่เมนูให้ ---
# เว็บนี้เคยมีลำดับเดียวยาว 01-08 ทั้งเว็บ ก่อนแบ่งเป็นสามภาค พอแบ่งแล้วเลขเก่าค้างบางหน้า
# จนมีเลขสองระบบซ้อนกัน เช่นหน้า contact เขียน 08 ทั้งที่เมนูไม่ได้ให้เลขมันเลย
# จัดใหม่เมื่อ 2026-08-20 · ด่านนี้กันไม่ให้เลขค้างแบบนั้นกลับมา
_EYE=re.compile(r'<div class="(?:kicker|eyebrow[^"]*)">(.*?)</div>',re.S)
_NUM=re.compile(r'(?:^|·)\s*(\d{2}[a-z]?)\s*—')
for f in files:
    src,p=parsed[f]
    if 'http-equiv="refresh"' in src or f=='404.html': continue
    # ดูเฉพาะป้ายที่อยู่บนหัวหน้า คือก่อน <h1> · บล็อกท้ายหน้าก็มีป้ายของตัวเอง
    head=src[:src.index('<h1')] if '<h1' in src else src
    m=_EYE.search(head)
    if not m: continue
    eye=_html.unescape(m.group(1))
    hit=_NUM.search(eye)
    if not hit: continue
    dw=re.search(r'<div class="drawer".*?</nav>',src,re.S)
    if not dw: continue
    link=re.search(r'<a[^>]*href="'+re.escape(f)+r'"[^>]*>([^<]*)</a>',dw.group(0))
    if not link:
        E(f,'section label is numbered %s but this page is not in the menu'%hit.group(1))
        continue
    label=_html.unescape(link.group(1))
    if hit.group(1) not in label:
        E(f,'section label says %s but the menu calls this page %r'%(hit.group(1),label))

# --- JSON-LD ต้องตรงกับหน้าปัจจุบัน ไม่ใช่แค่เป็น JSON ที่อ่านได้ ---
# ด่านชุดแรกตรวจแค่ว่าแยกวิเคราะห์ผ่านและ @id ที่อ้างมีตัวจริง ซึ่งยังปล่อยให้กราฟ
# พูดถึงหน้าที่เปลี่ยนไปแล้วได้ ชุดนี้จึงเทียบกับสิ่งที่อยู่ในหน้าจริงทีละอย่าง
# ข้อความที่คนเห็นต้องตัด script style svg ออกก่อน ไม่งั้นด่าน FAQ จะไปเจอคำถาม
# ใน JSON-LD ของตัวเองแล้วผ่านทุกครั้งโดยไม่ได้ตรวจอะไรเลย
BASE='https://www.neogens.co/'

def _visible(src):
    t=re.sub(r'<(script|style|svg)\b.*?</\1>','',src,flags=re.S)
    return ' '.join(re.sub(r'<[^>]+>',' ',t).split())

for f in files:
    src,p=parsed[f]
    if 'http-equiv="refresh"' in src or f=='404.html': continue
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',src,re.S)
    if not m: continue                      # ด่านก่อนหน้าฟ้องเรื่องไม่มี JSON-LD ไปแล้ว
    try: graph=json.loads(m.group(1)).get('@graph') or []
    except Exception: continue
    me=BASE if f=='index.html' else BASE+f
    page=next((n for n in graph if n.get('@id')==me), None)
    if not page:
        E(f,'JSON-LD has no node describing this page'); continue

    t=re.search(r'<title>(.*?)</title>',src,re.S)
    if t:
        want=_html.unescape(t.group(1)).replace(' — Neo Gens','').strip()
        if (page.get('name') or '').strip()!=want:
            E(f,'JSON-LD name is stale: %r but the title says %r'
              %((page.get('name') or '')[:40],want[:40]))

    d=re.search(r'<meta name="description" content="([^"]*)"',src)
    if d and page.get('description'):
        if _html.unescape(d.group(1)).strip()!=page['description'].strip():
            E(f,'JSON-LD description no longer matches the meta description')

    want_lang='th' if f.startswith('th-') else 'en'
    if page.get('inLanguage')!=want_lang:
        E(f,'JSON-LD inLanguage is %r, should be %r'%(page.get('inLanguage'),want_lang))

    for k in ('translationOfWork','workTranslation'):
        v=(page.get(k) or {}).get('@id')
        if v:
            tgt=v.replace(BASE,'') or 'index.html'
            twin=f[3:] if f.startswith('th-') else 'th-'+f
            if not os.path.exists(tgt):
                E(f,'JSON-LD %s points at a file that does not exist: %s'%(k,tgt))
            elif tgt!=twin:
                E(f,'JSON-LD %s points at %s but the language twin is %s'%(k,tgt,twin))

    bid=(page.get('breadcrumb') or {}).get('@id')
    if bid:
        bc=next((n for n in graph if n.get('@id')==bid), None)
        if not bc:
            E(f,'JSON-LD breadcrumb id is declared but the list is missing')
        else:
            items=bc.get('itemListElement') or []
            if [i.get('position') for i in items]!=list(range(1,len(items)+1)):
                E(f,'JSON-LD breadcrumb positions are not 1..n')
            for i in items:
                tgt=(i.get('item') or '').replace(BASE,'') or 'index.html'
                if not os.path.exists(tgt):
                    E(f,'JSON-LD breadcrumb points at a file that does not exist: %s'%tgt)
            if items and (items[-1].get('item') or '')!=me and len(items)>2:
                E(f,'JSON-LD breadcrumb does not end at this page')
            # เส้นทางที่ประกาศกับเครื่อง ต้องมีเส้นทางที่คนเห็นคู่กันเสมอ
            # เพิ่มเมื่อ 2026-08-20 หลังพบว่ามี BreadcrumbList 33 หน้าแต่ไม่มีแถบให้คนเห็นสักหน้า
            vnav=re.search(r'<nav class="crumbs".*?</nav>',src,re.S)
            if not vnav:
                E(f,'has BreadcrumbList but no breadcrumb a reader can see')
            else:
                shown=[_html.unescape(x).strip() for x in
                       re.findall(r'<li[^>]*>(?:<a[^>]*>)?([^<]*)',vnav.group(0))]
                want=[i.get('name') for i in items]
                if shown!=want:
                    E(f,'visible breadcrumb %s does not match the JSON-LD %s'%(shown,want))
                if vnav.group(0).count('aria-current="page"')!=1:
                    E(f,'visible breadcrumb does not mark exactly one current step')
            # ภาคที่ breadcrumb บอก ต้องตรงกับกลุ่มที่เมนูจัดหน้านี้ไว้
            # เพิ่มเมื่อ 2026-08-20 หลังพบว่าหน้า what-you-are-holding ถูกเมนูจัดไว้ภาค 2
            # แต่ breadcrumb บอกว่าภาค 1 อยู่หลายวันโดยไม่มีใครเห็น เพราะยังไม่ได้แสดงบนหน้า
            dw=re.search(r'<div class="drawer".*?</nav>',src,re.S)
            if dw and len(items)>2:
                groups=re.findall(r'<div class="h">([^<]*)</div>|<a[^>]*href="([^"]+)"',dw.group(0))
                head=None; where={}
                for g,h in groups:
                    if g: head=g.strip()
                    elif h: where.setdefault(h,head)
                opener=(items[1].get('item') or '').replace(BASE,'') or 'index.html'
                mine=f if f!='index.html' else ''
                if where.get(mine) and where.get(opener) and where[mine]!=where[opener]:
                    E(f,'menu files this page under %r but the breadcrumb says %r'
                      %(where[mine],where[opener]))

    faq=next((n for n in graph if n.get('@type')=='FAQPage'), None)
    if faq:
        vis=_visible(src)
        for q in faq.get('mainEntity') or []:
            if (q.get('name') or '')[:30] not in vis:
                E(f,'JSON-LD declares a FAQ question that is not on the page: %s'
                  %(q.get('name') or '')[:40])

# --- title กับ description ต้องไม่ยาวจนถูกตัดในผลค้นหา ---
# ย่อเมื่อ 2026-08-19 · เดิม title เกิน 60 อยู่ 25 หน้า ยาวสุด 113
import html as _html
for f in files:
    src,p=parsed[f]
    if 'http-equiv="refresh"' in src or f=='404.html': continue
    m=re.search(r'<title>(.*?)</title>',src,re.S)
    if m and len(_html.unescape(m.group(1)))>60:
        E(f,'title is %d characters, over the 60 that fit a search result'
          %len(_html.unescape(m.group(1))))
    d=re.search(r'<meta name="description" content="([^"]*)"',src)
    if d and len(_html.unescape(d.group(1)))>160:
        E(f,'description is %d characters, over 160'%len(_html.unescape(d.group(1))))
    od=re.search(r'<meta property="og:description" content="([^"]*)"',src)
    if d and od and d.group(1)!=od.group(1):
        E(f,'og:description does not match the meta description')

# --- ลำดับหัวข้อห้ามข้ามระดับ ---
# แก้เมื่อ 2026-08-19 · เดิมข้าม 33 จาก 39 หน้า เช่น h1 → h5
# โปรแกรมอ่านหน้าจอใช้ลำดับหัวข้อเป็นสารบัญของหน้า ข้ามระดับแล้วสารบัญจะมีรู
for f in files:
    src,p=parsed[f]
    if 'http-equiv="refresh"' in src: continue
    body=re.sub(r'<(script|style|svg)\b.*?</\1>','',src,flags=re.S)
    prev=0
    for m in re.finditer(r'<h([1-6])\b',body):
        lvl=int(m.group(1))
        if prev and lvl>prev+1:
            E(f,'heading level jumps h%d to h%d'%(prev,lvl)); break
        prev=lvl

# --- สีข้อความรองต้องผ่านเกณฑ์ contrast ---
# --mute ใช้กับป้ายขนาด 10–11px ซึ่งนับเป็นข้อความปกติ ต้องได้ 4.5:1
# ยกระดับเมื่อ 2026-08-19 ด่านนี้กันไม่ให้ใครขยับกลับไปค่าที่อ่านไม่ออก
def _lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def _ratio(a,b):
    l1,l2=sorted([_lum(a),_lum(b)],reverse=True); return (l1+.05)/(l2+.05)
for f in files:
    src,p=parsed[f]
    if 'http-equiv="refresh"' in src: continue
    for block,bgvar in (('root','--bg'),):
        pass
    for m in re.finditer(r'(:root|html\[data-theme="light"\])\{([^}]*)',src):
        body=m.group(2)
        mute=re.search(r'--mute:\s*(#[0-9A-Fa-f]{6})',body)
        bg=re.search(r'--bg:\s*(#[0-9A-Fa-f]{6})',body)
        surf=re.search(r'--surface:\s*(#[0-9A-Fa-f]{6})',body)
        if not (mute and bg): continue
        for name,ground in (('page',bg.group(1)),('card',surf.group(1) if surf else None)):
            if not ground: continue
            r=_ratio(mute.group(1),ground)
            if r < 4.5:
                E(f,'--mute %s on %s %s is %.2f:1, below the 4.5 minimum'
                  %(mute.group(1),name,ground,r))

# --- ห้ามมีสคริปต์หรือทรัพยากรจากภายนอกที่เก็บข้อมูลผู้อ่าน ---
# ถอด Google Analytics ออกเมื่อ 2026-08-19 ด่านนี้กันไม่ให้ใครเผลอใส่กลับมา
# เว็บที่ขายเรื่องอธิปไตยเหนือข้อมูล ต้องไม่ส่ง IP ผู้อ่านออกไปก่อนเขาได้อ่านอะไร
# ครอบทั้ง script และ link เพราะฟอนต์จากภายนอกก็ส่ง IP ผู้อ่านออกไปเหมือนกัน
THIRD_PARTY=re.compile(r'<(?:script|link|iframe|img)[^>]*\s(?:src|href)="(?:https?:)?//([^"/]+)')
OURS={'www.neogens.co','neogens.co','neogens-briefing.neogens.workers.dev'}
for f in files:
    src,p=parsed[f]
    for m in THIRD_PARTY.finditer(src):
        host=m.group(1)
        if host not in OURS:
            E(f,'third-party resource: %s'%host)
    if 'googletagmanager' in src or 'gtag(' in src:
        E(f,'analytics tag is back')
# หน้าในโฟลเดอร์ย่อยก็เปิดจากเว็บได้ ต้องตรวจด้วย แม้จะไม่อยู่ในรายการหน้าหลัก
import glob as _glob
for _p in _glob.glob('*/*.html'):
    if _p.startswith('.tools'): continue
    _s=io.open(_p,encoding='utf-8').read()
    for m in THIRD_PARTY.finditer(_s):
        if m.group(1) not in OURS:
            E(_p,'third-party resource: %s'%m.group(1))
    if 'googletagmanager' in _s or 'gtag(' in _s:
        E(_p,'analytics tag is back')

# --- hreflang ต้องชี้คู่ภาษาที่ถูกหน้า ---
# ความผิดที่เคยเกิดจริง หน้าที่สร้างจากแม่แบบลืมแก้แท็ก แล้วประกาศฉบับแปลเป็นหน้าอื่น
# search engine เจอการประกาศที่ไม่ยืนยันกลับ จะเลิกเชื่อ hreflang ทั้งโดเมน ไม่ใช่แค่หน้านั้น
# ตรวจ "ชี้ถูกหน้าไหม" ไม่ใช่แค่ "มีแท็กครบไหม" เพราะรอบแรกเขียนแบบหลังแล้วจับความผิดไม่ได้
BASE='https://www.neogens.co/'
def _page(v): return v or 'index.html'
for f in files:
    src,p=parsed[f]
    if 'http-equiv="refresh"' in src or f=='404.html': continue
    alts=dict(re.findall(r'hreflang="([^"]+)" href="'+re.escape(BASE)+r'([^"]*)"',src))
    if not alts:
        E(f,'no hreflang tags'); continue
    en_self = f[3:] if f.startswith('th-') else f
    th_self = f if f.startswith('th-') else 'th-'+f
    want={}
    if os.path.exists(en_self): want['en']=en_self
    if os.path.exists(th_self): want['th']=th_self
    want['x-default']=want.get('en') or want.get('th')
    want={k:('' if v=='index.html' else v) for k,v in want.items()}
    for k,v in want.items():
        if k not in alts:
            E(f,'hreflang %s is missing (should be %s)'%(k,_page(v)))
        elif alts[k]!=v:
            E(f,'hreflang %s points at %s but should point at %s'%(k,_page(alts[k]),_page(v)))
    for k in alts:
        if k not in want: E(f,'hreflang %s declares a version that does not exist'%k)
    me='' if f=='index.html' else f
    if me not in alts.values(): E(f,'hreflang never points back at this page')

# --- required shell on every real page ---
# หน้า stub ที่เด้งไปชื่อใหม่ ไม่ใช่หน้าเว็บเต็ม ไม่ต้องมี nav ธีม หรือ footer
def is_stub(f):
    src=parsed[f][0]
    return 'http-equiv="refresh"' in src and 'rel="canonical"' in src
STUBS=[f for f in files if is_stub(f)]
REAL=[f for f in files if f not in STUBS]
for f in REAL:
    src,p=parsed[f]
    for need,msg in [('<title>','title'),('data-theme','theme boot'),('class="tgl"','theme toggle')]:
        if need not in src: E(f,'missing %s'%msg)
    if f!='404.html':
        for need,msg in [('id="drawer"','mobile drawer'),('id="burger"','burger button'),
                         ('rel="canonical"','canonical'),('<footer>','footer'),('name="viewport"','viewport')]:
            if need not in src: E(f,'missing %s'%msg)

# --- canonical uniqueness ---
seen={}
for f in REAL:
    m=re.search(r'<link rel="canonical" href="([^"]+)"',parsed[f][0])
    if m:
        if m.group(1) in seen: E(f,'canonical duplicated with %s: %s'%(seen[m.group(1)],m.group(1)))
        seen[m.group(1)]=f

# --- Thai diacritic sanity ---
AV=set('\u0e31\u0e34\u0e35\u0e36\u0e37\u0e47')      # above vowels + maitaikhu
TONE=set('\u0e48\u0e49\u0e4a\u0e4b')              # tone marks
SIGN=set('\u0e4c\u0e4d\u0e4e')                # thanthakhat, nikhahit, yamakkan
BELOW=set('\u0e38\u0e39\u0e3a')               # below vowels + phinthu
MARKS=AV|TONE|SIGN|BELOW
def cls(ch):
    return 'AV' if ch in AV else 'TONE' if ch in TONE else 'SIGN' if ch in SIGN else 'BELOW' if ch in BELOW else None
# legal stacking order on one consonant: [BELOW] [AV] [TONE] [SIGN]
RANK={'BELOW':0,'AV':1,'TONE':2,'SIGN':3}
for f in files:
    if not f.startswith('th-'): continue
    src,p=parsed[f]
    t=' '.join(p.text)
    run=[]
    for i,ch in enumerate(t):
        c=cls(ch)
        if c:
            if not run and not ('\u0e01'<=t[i-1]<='\u0e2e' if i else False):
                W(f,'mark on non-consonant: …%s…'%t[max(0,i-8):i+6])
            if run:
                pc=run[-1]
                if RANK[c]<=RANK[pc[0]]:
                    E(f,'illegal Thai mark order (%s after %s): …%s…'%(c,pc[0],t[max(0,i-9):i+5]))
            run.append((c,ch))
        else:
            run=[]

# --- Thai typography traps ---
for f in files:
    if not f.startswith('th-'): continue
    src=parsed[f][0]
    css=''.join(re.findall(r'<style>(.*?)</style>',src,re.S))
    for rule in re.findall(r'([^{}]+)\{([^{}]*letter-spacing\s*:\s*-[^;}]*)',css):
        sel=rule[0].strip().splitlines()[-1]
        if 'mono' not in rule[1] and not re.search(r'\.(k|m|en|eyebrow|kicker|lbl|pb-k|brand|bt|f-brand|glyph|lang|tgl)\b',sel):
            W(f,'negative letter-spacing on Thai-bearing rule: %s'%sel[:70])
    for lh in re.findall(r'line-height\s*:\s*(0?\.\d+|1\.[01]\d*)\b',css):
        W(f,'line-height %s may clip Thai tone marks'%lh)

# --- unverifiable statistics (house rule §8) ---
# หน้าเดโมที่ประกาศตัวเองด้วย <meta name="ng-data" content="simulated"> ถูกข้ามการตรวจนี้
# เพราะตัวเลขทั้งหน้าเป็นของสมมติโดยเจตนา และหน้าบอกผู้อ่านไว้แล้ว
# ข้อยกเว้นนี้ไม่เงียบ — ท้ายรายงานจะบอกว่าข้ามไฟล์ไหนไปบ้าง
NUMPAT=re.compile(r'(?<![\w-])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?\s?%|\d+x\b)')
ALLOW=re.compile(r'(90[- ]minute|© 20\d\d|20\d\d|G-TPB|1962|1998|2014|2011|01|02|03|04|05|\d+ min read)')
SIMULATED=re.compile(r'<meta\s+name="ng-data"\s+content="simulated"')
skipped_num=[]
for f in files:
    src,p=parsed[f]
    if SIMULATED.search(src):
        vis=' '.join(p.vis).lower()
        # ฉบับไทยบอกผู้อ่านด้วยคำว่า ข้อมูลจำลอง ไม่ใช่คำอังกฤษ
        if 'simulated' not in vis and 'จำลอง' not in vis:
            E(f,'declared ng-data=simulated but the page never says so to the reader')
        skipped_num.append(f); continue
    t=' '.join(x.strip() for x in p.text if x.strip())
    for m in NUMPAT.finditer(t):
        seg=t[max(0,m.start()-45):m.end()+35]
        if ALLOW.search(m.group(0)): continue
        W(f,'possible unverifiable figure: …%s…'%seg)

# --- EN/TH parity ---
IDS=['problem','what','why','visit','experience','museums','services','engagement','proof','honest','contact']
for i in IDS:
    a,b='%s.html'%i,'th-%s.html'%i
    if a not in parsed or b not in parsed: E(a,'missing pair'); continue
    for tag in ['h2','h3','figure','blockquote','section']:
        ca=len(re.findall(r'<%s\b'%tag,parsed[a][0])); cb=len(re.findall(r'<%s\b'%tag,parsed[b][0]))
        if ca!=cb: E('EN↔TH','%s: <%s> EN %d / TH %d'%(i,tag,ca,cb))

print('files checked:',len(files))
print()
if errs:
    print('✗ must fix (%d)'%len(errs))
    for f,m in errs: print('   %-34s %s'%(f,m))
else: print('✓ no blocking errors')
print()
if warns:
    print('⚠ review (%d)'%len(warns))
    seenw=set()
    for f,m in warns:
        k=(f,m[:60])
        if k in seenw: continue
        seenw.add(k); print('   %-34s %s'%(f,m[:150]))
if skipped_num:
    print('figure check skipped on %d page(s) declaring simulated data: %s'
          %(len(skipped_num),', '.join(skipped_num)))
    print()
print('Not checked by this script: whether the page looks right, and whether EN and TH still say the same thing.')
sys.exit(1 if errs else 0)
