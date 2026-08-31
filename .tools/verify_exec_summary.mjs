import fs from 'fs';
import {JSDOM} from 'jsdom';

const PAGES=[['exec-summary-museums.html','en'],['th-exec-summary-museums.html','th']];
let bad=[], ok=0;
const say=(c,m)=>{ if(c) ok++; else bad.push(m); };

for (const [file,lang] of PAGES){
  let html=fs.readFileSync(file,'utf8');
  // หน้านี้สร้างจากแม่แบบที่ฝัง CSS ทั้งก้อน แต่เผื่อไว้ ถ้ามี link ไฟล์ร่วมให้แทรกเอง
  const link=html.match(/<link rel="stylesheet" href="(assets\/site\.[a-z]+\.css)">/);
  if(link) html=html.replace(link[0],'<style>'+fs.readFileSync(link[1],'utf8')+'</style>');

  const dom=new JSDOM(html,{pretendToBeVisual:true});
  const d=dom.window.document, gcs=el=>dom.window.getComputedStyle(el);

  const body=d.querySelector('article .artbody');
  say(!!body, `${file}: ไม่มี .artbody`);
  if(!body) continue;

  // CSS ติดจริงไหม ไม่ใช่ค่า default ของเบราว์เซอร์
  const h2=body.querySelector('h2'), p=body.querySelector('p'), li=body.querySelector('li');
  say(gcs(h2).display==='block' && gcs(h2).fontSize!=='', `${file}: h2 ไม่ได้รับกฎ`);
  const rawLh=gcs(p).lineHeight, fs_=parseFloat(gcs(p).fontSize);
  const lh=rawLh.includes('px')? parseFloat(rawLh)/fs_ : parseFloat(rawLh);
  if(lang==='th') say(lh>=1.75 && lh<=1.9, `${file}: line-height ไทย ${lh.toFixed(2)} ต้องอยู่ 1.75–1.9`);
  else say(lh>1.3, `${file}: line-height ${lh}`);
  say(gcs(li).display==='list-item'||gcs(li).display==='block', `${file}: li ไม่ได้รับกฎ`);

  // ไม่มี letter-spacing ติดลบในกฎที่แตะข้อความไทย
  if(lang==='th'){
    const css=[...d.querySelectorAll('style')].map(s=>s.textContent).join('\n');
    const neg=[...css.matchAll(/([^{}]+)\{([^}]*letter-spacing:\s*-[^;}]+)[^}]*\}/g)]
      .map(m=>m[1].trim())
      .filter(sel=>/artbody|\bp\b|body|\.stand|h1|h2|h3|li/.test(sel));
    say(neg.length===0, `${file}: letter-spacing ติดลบใน ${neg.join(' / ')}`);
  }

  // แผงตัวเลข  ต้องมีสองแผง มีบรรทัดที่มา และ CSS ต้องติดจริง
  const figs=[...body.querySelectorAll('figure.esf')];
  say(figs.length===2, `${file}: แผงตัวเลข ${figs.length} แผง ต้องมี 2`);
  figs.forEach((f,i)=>{
    const cap=f.querySelector('figcaption');
    say(!!cap && cap.querySelector('a[href^="https://"]'),
        `${file}: แผงที่ ${i+1} ไม่มีลิงก์กลับไปต้นทาง`);
    const grid=f.querySelector('.esf-in');
    say(gcs(grid).display==='grid', `${file}: แผงที่ ${i+1} ไม่ได้เป็น grid CSS ไม่ติด`);
    const cells=f.querySelectorAll('.esf-c').length;
    say(f.classList.contains('esf-'+cells),
        `${file}: แผงที่ ${i+1} มี ${cells} ช่อง แต่คลาสไม่ตรง`);
    const t=f.querySelector('.esf-t');
    const r=gcs(t).lineHeight, fz=parseFloat(gcs(t).fontSize);
    const ratio=r.includes('px')? parseFloat(r)/fz : parseFloat(r);
    if(lang==='th') say(ratio>=1.75 && ratio<=1.9,
        `${file}: แผงที่ ${i+1} line-height ไทย ${ratio}`);
  });

  // ตัวบ่งชี้หน้าปัจจุบัน  มี · ชี้ถูก · ไม่เกินหนึ่ง (ข้อ 12)
  const ac=[...d.querySelectorAll('a[aria-current="page"]')];
  say(ac.length===1, `${file}: aria-current ในลิงก์ ${ac.length} อัน`);
  say(ac.length===1 && ac[0].getAttribute('href')===file, `${file}: aria-current ชี้ผิดหน้า`);

  // แถบเส้นทาง และไม่มีฟอร์มหลงเหลือ
  say(!!d.querySelector('nav.crumbs'), `${file}: ไม่มีแถบเส้นทาง`);
  say(d.querySelectorAll('form').length===0, `${file}: ยังมีฟอร์ม`);
  say(!!d.querySelector('section.join a.btn[href="contact.html"]'), `${file}: ไม่มีปุ่มไปหน้าติดต่อ`);

  // เมนูมีลิงก์เข้าหน้านี้บนจอกว้าง  กฎ 9b  แถบเมนูบนหรือ footer
  const inNav=!!d.querySelector(`.nav-links a[href="${file}"]`);
  const inFoot=!!d.querySelector(`footer a[href="${file}"]`);
  say(inNav||inFoot, `${file}: ไม่มีทางเข้าบนจอกว้าง`);

  // สระวรรณยุกต์ไทย  ไม่มีสระซ้ำซ้อนหรือวรรณยุกต์ลอย
  if(lang==='th'){
    const t=body.textContent;
    say(!/[ัิ-ฺ็-๎]{3,}/.test(t), `${file}: เจอสระหรือวรรณยุกต์ซ้อนเกินสองชั้น`);
    say(!/^[ัิ-ฺ็-๎]/.test(t.trim()), `${file}: ข้อความขึ้นต้นด้วยสระลอย`);
    // เทียบเฉพาะข้อความในย่อหน้า ไม่ใช่ช่องว่างจัดรูปแบบระหว่างแท็ก
    const runs=[...body.querySelectorAll('p,li,h2,h3')].map(e=>e.textContent);
    say(runs.every(x=>!/  /.test(x)), `${file}: มีเว้นวรรคซ้ำในเนื้อหา`);
  }
}
console.log(bad.length? '✗ ไม่ผ่าน\n'+bad.join('\n') : `✓ ผ่านทั้งหมด ${ok} ข้อ`);
process.exit(bad.length?1:0);
