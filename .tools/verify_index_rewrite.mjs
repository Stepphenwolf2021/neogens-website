import fs from 'fs';
import {JSDOM} from 'jsdom';

// ตรวจว่ารายการสามข้อใหม่บนหน้าแรก "มีผลจริง" ไม่ใช่แค่มีอยู่ในไฟล์ (ข้อ 11 ของ LESSONS.md)
const PAGES=[['index.html','en'],['th-index.html','th']];
let bad=[], ok=0;
const say=(c,m)=>{ if(c) ok++; else bad.push(m); };

for (const [file,lang] of PAGES){
  let html=fs.readFileSync(file,'utf8');
  const link=html.match(/<link rel="stylesheet" href="\/(assets\/site\.[a-z]+\.css)">/);
  if(link) html=html.replace(link[0],'<style>'+fs.readFileSync(link[1],'utf8')+'</style>');
  else say(false, `${file}: ไม่พบลิงก์ไฟล์ CSS ร่วม`);

  const dom=new JSDOM(html,{pretendToBeVisual:true});
  const d=dom.window.document, gcs=el=>dom.window.getComputedStyle(el);

  const ul=d.querySelector('.hero-list');
  say(!!ul, `${file}: ไม่มี .hero-list`);
  if(!ul) continue;

  const lis=[...ul.querySelectorAll('li')];
  say(lis.length===3, `${file}: รายการมี ${lis.length} ข้อ ต้องมี 3`);
  say(lis.every(li=>li.querySelector('b')), `${file}: บางข้อไม่มีหัวข้อตัวหนา`);

  // CSS ติดจริงไหม  ถ้าเป็นค่า default ของเบราว์เซอร์แปลว่าไม่ติด
  const st=gcs(ul);
  say(st.listStyleType==='disc', `${file}: list-style ไม่ติด ได้ ${st.listStyleType}`);
  const lh=parseFloat(st.lineHeight)/parseFloat(st.fontSize)||parseFloat(st.lineHeight);
  const ratio=st.lineHeight.includes('px')? parseFloat(st.lineHeight)/parseFloat(st.fontSize)
                                          : parseFloat(st.lineHeight);
  if(lang==='th') say(ratio>=1.75 && ratio<=1.9, `${file}: line-height ไทย ${ratio} ต้อง 1.75–1.9`);
  else say(ratio>1.3, `${file}: line-height ${ratio}`);
  say(!/^-/.test(st.letterSpacing||''), `${file}: letter-spacing ติดลบ`);

  // ย่อหน้า hero ต้องมีสองก้อน  ประโยคนำ กับ ย่อหน้าหลังรายการ
  const subs=[...d.querySelectorAll('.hero .hero-sub')];
  say(subs.length===2, `${file}: .hero-sub มี ${subs.length} ก้อน ต้องมี 2`);
  say(!!d.querySelector('#ng-sub'), `${file}: หาย id ng-sub`);

  // ลำดับต้องเป็น ประโยคนำ → รายการ → ย่อหน้าปิดท้าย hero
  const kids=[...d.querySelector('.hero .wrap').children].map(e=>e.className||e.tagName);
  const iSub=kids.findIndex(c=>String(c).includes('hero-sub'));
  const iUl=kids.findIndex(c=>String(c).includes('hero-list'));
  say(iSub>=0 && iUl>iSub, `${file}: รายการไม่ได้อยู่หลังประโยคนำ`);

  // ไทย  ไม่มีเว้นวรรคซ้ำ และไม่มีสระวรรณยุกต์ซ้อนเกินสองชั้น
  if(lang==='th'){
    const runs=[...d.querySelectorAll('.hero p, .hero li, .pband .pb-d, .pband .card p')]
      .map(e=>e.textContent);
    say(runs.every(x=>!/  /.test(x)), `${file}: มีเว้นวรรคซ้ำในเนื้อหา`);
    say(runs.every(x=>!/[ัิ-ฺ็-๎]{3,}/.test(x)), `${file}: สระหรือวรรณยุกต์ซ้อนเกินสองชั้น`);
    say(!d.body.textContent.includes('ล็อก'), `${file}: เจอ ล็อก ต้องเป็น ล็อค`);
  }
}
console.log(bad.length? '✗ ไม่ผ่าน\n'+bad.join('\n') : `✓ ผ่านทั้งหมด ${ok} ข้อ`);
process.exit(bad.length?1:0);
