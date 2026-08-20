import { JSDOM } from 'jsdom'; import fs from 'fs'; import path from 'path';
const ROOT='/Users/noppadolweerakitti/projects/neogens-website/';

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

// กลุ่มตามภาษา เพราะ font stack ต่างกันโดยตั้งใจ
const groups={en:pages.filter(f=>!f.startsWith('th-')), th:pages.filter(f=>f.startsWith('th-'))};
const shared={};
for(const [k,g] of Object.entries(groups)){
  const c=new Map();
  for(const f of g) for(const r of new Set(rulesOf.get(f))) c.set(r,(c.get(r)||0)+1);
  const need=Math.ceil(g.length*0.8);
  shared[k]=new Set([...c.entries()].filter(([,n])=>n>=need).map(([r])=>r));
}
// ลำดับอ้างอิง เอาจากหน้าที่มีกฎร่วมมากที่สุดในกลุ่ม
const order={};
for(const [k,g] of Object.entries(groups)){
  let best=g[0],n=-1;
  for(const f of g){const m=rulesOf.get(f).filter(r=>shared[k].has(r)).length; if(m>n){n=m;best=f;}}
  const seen=new Set(), arr=[];
  for(const r of rulesOf.get(best)) if(shared[k].has(r)&&!seen.has(r)){arr.push(r);seen.add(r);}
  for(const r of shared[k]) if(!seen.has(r)){arr.push(r);seen.add(r);}
  order[k]=arr;
  console.log(`${k}: ${g.length} หน้า · กฎร่วม ${arr.length} · ${Math.round(arr.join('').length/1024)} KB`);
}

const PROPS=['display','position','fontSize','fontWeight','lineHeight','fontFamily','color',
 'backgroundColor','marginTop','marginBottom','marginLeft','marginRight','paddingTop','paddingBottom',
 'paddingLeft','paddingRight','borderRadius','maxWidth','flexDirection','gridTemplateColumns',
 'textTransform','letterSpacing','alignSelf','opacity','textAlign','borderTopWidth','borderLeftWidth'];
function snap(src){
  const {window}=new JSDOM(src,{pretendToBeVisual:true});
  const d=window.document;
  const out=[...d.querySelectorAll('body *')].map(e=>{
    const cs=window.getComputedStyle(e); return PROPS.map(p=>cs[p]).join('|');});
  window.close(); return out;
}

// ขั้นที่ 1 · จัดกฎร่วมมาไว้ต้นบล็อกตามลำดับอ้างอิง แล้วพิสูจน์ว่าหน้าตาไม่เปลี่ยน
let ok=0, skip=[];
for(const f of pages){
  const k=f.startsWith('th-')?'th':'en';
  const src=fs.readFileSync(ROOT+f,'utf8');
  const before=snap(src);
  const mine=rulesOf.get(f), mineSet=new Set(mine);
  const head=order[k].filter(r=>mineSet.has(r));
  const tail=mine.filter(r=>!shared[k].has(r));
  let first=true;
  const out=src.replace(/<style>([\s\S]*?)<\/style>/g,()=> {
    const body=first ? head.concat(tail).join('\n') : '';
    first=false;
    return '<style>\n'+body+'\n</style>';
  });
  const after=snap(out);
  const bad=before.length!==after.length ? 'จำนวน element ต่าง'
    : (()=>{const i=before.findIndex((v,x)=>v!==after[x]); return i<0?null:`element ที่ ${i}`;})();
  if(bad){ skip.push([f,bad]); continue; }
  fs.writeFileSync(ROOT+f,out); ok++;
}
console.log(`\nขั้นที่ 1 จัดลำดับใหม่ · สำเร็จ ${ok} หน้า · ข้าม ${skip.length}`);
skip.slice(0,8).forEach(([f,r])=>console.log('  ',f,r));
