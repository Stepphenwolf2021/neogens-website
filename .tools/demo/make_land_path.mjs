import { readFileSync, writeFileSync } from 'fs';
import * as topojson from 'topojson-client';
import { geoEquirectangular, geoPath } from 'd3-geo';
const world = JSON.parse(readFileSync('node_modules/world-atlas/land-110m.json'));
const land = topojson.feature(world, world.objects.land);

const W = 960;
const k = W / (2 * Math.PI);            // scale ให้ลองจิจูดเต็มพอดีความกว้าง
const latTop = 62, latBot = -48;
const y = lat => k * Math.log(1);       // equirectangular ใช้เชิงเส้น
const ty = k * (latTop * Math.PI / 180);
const H = Math.round(k * ((latTop - latBot) * Math.PI / 180));

const proj = geoEquirectangular().scale(k).translate([W / 2, ty])
  .clipExtent([[0, 0], [W, H]]);
let d = geoPath(proj)(land);
d = d.replace(/-?\d+\.?\d*/g, m => (Math.round(parseFloat(m) * 2) / 2).toString());
writeFileSync('land.txt', d);
console.log('W', W, 'H', H, 'k', k.toFixed(4), 'ty', ty.toFixed(2), '· path', d.length, 'ตัวอักษร');
for (const [n, lon, lat] of [['Chiang Rai',99.8,19.9],['Bogota',-74,4.7],['Addis',38.7,9],['Sao Paulo',-46.6,-23.5],['London',-0.1,51.5],['Tokyo',139.7,35.7],['Sydney',151,-33.9]]) {
  console.log(' ', n, proj([lon,lat]).map(v=>Math.round(v)).join(','));
}
