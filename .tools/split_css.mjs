import { JSDOM } from 'jsdom'; import fs from 'fs'; import path from 'path';
const ROOT='/Users/noppadolweerakitti/projects/neogens-website/';
const ASSETS=path.join(ROOT,'assets');

function splitRules(css){
  const out=[]; let i=0,d=0,st=0;
  while(i<css.length){const c=css[i];
    if(c==='{')d++; else if(c==='}'){d--; if(d===0){out.push(css.slice(st,i+1).trim()); st=i+1;}}
    i++;}
  const t=css.slice(st).trim(); if(t)out.push(t);
  return out.filter(Boolean);
}
const pages=fs.readdirSync(ROOT).filter(f=>f.endsWith('.html')).filter(f=>{
  const s=fs.readFileSync(ROOT+f,'utf8');
  return !s.includes('http-equiv="refresh"') && s.includes('<style>');});
const rulesOf=new Map();
for(const f of pages) rulesOf.set(f,
  [...fs.readFileSync(ROOT+f,'utf8').matchAll(/<style>([\s\S]*?)<\/style>/g)].flatMap(m=>splitRules(m[1])));

const groups={en:pages.filter(f=>!f.startsWith('th-')), th:pages.filter(f=>f.startsWith('th-'))};
const shared={};
for(const [k,g] of Object.entries(groups)){
  const c=new Map();
  for(const f of g) for(const r of new Set(rulesOf.get(f))) c.set(r,(c.get(r)||0)+1);
  shared[k]=new Set([...c.entries()].filter(([,n])=>n>=Math.ceil(g.length*0.8)).map(([r])=>r));
}
// หน้าที่กฎร่วมเรียงติดกันอยู่ต้นบล็อกแล้ว และมีครบทุกกฎในชุด จึงถอดออกไฟล์ได้อย่างปลอดภัย
const canon={};
for(const k of ['en','th']){
  let best=null, n=-1;
  for(const f of groups[k]){
    const rs=rulesOf.get(f); let i=0; while(i<rs.length && shared[k].has(rs[i])) i++;
    const contiguous = rs.slice(i).every(r=>!shared[k].has(r));
    if(contiguous && i>n){ n=i; best=rs.slice(0,i); }
  }
  canon[k]=best||[];
  console.log(`${k}: ชุดกฎร่วมที่จะแยกออกไฟล์ ${canon[k].length} กฎ · ${Math.round(canon[k].join('').length/1024)} KB`);
}
fs.mkdirSync(ASSETS,{recursive:true});
const files={};
for(const k of ['en','th']){
  const head=`/* สไตล์เปลือกของหน้า ฉบับภาษา${k==='th'?'ไทย':'อังกฤษ'}\n`
    +`   แยกออกมาด้วย .tools/split_css.mjs · แก้ที่นี่ที่เดียวแล้วมีผลทุกหน้าที่ลิงก์ไฟล์นี้\n`
    +`   กฎเฉพาะหน้ายังอยู่ในหน้านั้นเหมือนเดิม และอยู่หลังไฟล์นี้เสมอ จึงยังชนะเหมือนเดิม */\n`;
  files[k]=head+canon[k].join('\n')+'\n';
  fs.writeFileSync(path.join(ASSETS,`site.${k}.css`), files[k]);
}

const PROPS=['display','position','fontSize','fontWeight','lineHeight','fontFamily','color',
 'backgroundColor','marginTop','marginBottom','marginLeft','marginRight','paddingTop','paddingBottom',
 'paddingLeft','paddingRight','borderRadius','maxWidth','flexDirection','gridTemplateColumns',
 'textTransform','letterSpacing','alignSelf','opacity','textAlign','borderTopWidth','borderLeftWidth'];
function snap(src,k){
  let s=src;
  // jsdom ไม่โหลด <link> เอง ต้องฉีด CSS ร่วมเข้าไปตรงตำแหน่งลิงก์เพื่อจำลองลำดับจริง
  s=s.replace(`<link rel="stylesheet" href="/assets/site.${k}.css">`, `<style>${files[k]}</style>`);
  const {window}=new JSDOM(s,{pretendToBeVisual:true});
  const d=window.document;
  const out=[...d.querySelectorAll('body *')].map(e=>{
    const cs=window.getComputedStyle(e); return PROPS.map(p=>cs[p]).join('|');});
  window.close(); return out;
}

let ok=0, saved=0, skip=[];
for(const f of pages){
  const k=f.startsWith('th-')?'th':'en';
  if(!canon[k].length) continue;
  const src=fs.readFileSync(ROOT+f,'utf8');
  const rs=rulesOf.get(f);
  // ต้องขึ้นต้นด้วยชุดกฎร่วมทั้งชุดพอดี ไม่งั้นการลิงก์ไฟล์จะเพิ่มกฎที่หน้านั้นไม่เคยมี
  const startsWithCanon = canon[k].every((r,i)=>rs[i]===r);
  if(!startsWithCanon){ skip.push([f,'กฎร่วมไม่ได้ขึ้นต้นครบชุด']); continue; }
  const rest=rs.slice(canon[k].length);
  let first=true;
  let out=src.replace(/<style>([\s\S]*?)<\/style>/g,()=>{
    const body=first?rest.join('\n'):''; first=false;
    return '<style>\n'+body+'\n</style>';
  });
  out=out.replace('<style>',`<link rel="stylesheet" href="/assets/site.${k}.css">\n<style>`);
  const before=snap(src,k), after=snap(out,k);
  const bad=before.length!==after.length ? 'จำนวน element ต่าง'
    : (()=>{const i=before.findIndex((v,x)=>v!==after[x]); return i<0?null:`element ที่ ${i}`;})();
  if(bad){ skip.push([f,bad]); continue; }
  saved+=src.length-out.length;
  fs.writeFileSync(ROOT+f,out); ok++;
}
console.log(`\nขั้นที่ 2 แยกออกไฟล์ · สำเร็จ ${ok} หน้า · ข้าม ${skip.length} · ลดขนาดรวม ${Math.round(saved/1024)} KB`);
skip.slice(0,10).forEach(([f,r])=>console.log('  ',f,r));
