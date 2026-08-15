/* ===== demo dashboard — ข้อมูลจำลองทั้งหมด ไม่ใช่ของจริง ===== */
(function () {
  var D = window.__VAULT_DEMO__;
  if (!D) return;
  var places = D.places, totals = D.totals;

  /* --- แปลงพิกัดจริงเป็นพิกัดบนภาพ equirectangular --- */
  var K = 152.7887, TX = 480, TY = 165.33, RAD = Math.PI / 180;
  function px(lon) { return TX + K * lon * RAD; }
  function py(lat) { return TY - K * lat * RAD; }

  var svg = document.getElementById('dm-map');
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, attrs, parent) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }

  var gEdge = el('g', {}, svg), gNode = el('g', {}, svg);

  /* --- เส้นการค้า จากแหล่งปลูกไปตลาด สร้างแบบตายตัวจากขนาดของทั้งสองฝั่ง --- */
  var origins = places.filter(function (p) { return p.role === 'origin'; });
  var markets = places.filter(function (p) { return p.role === 'market'; });
  origins.sort(function (a, b) { return b.c.farmers - a.c.farmers; });
  markets.sort(function (a, b) { return b.c.roasters - a.c.roasters; });

  var edges = [];
  origins.forEach(function (o, i) {
    var n = o.c.farmers > 300 ? 3 : o.c.farmers > 100 ? 2 : 1;
    for (var j = 0; j < n; j++) {
      var m = markets[(i * 3 + j * 2) % markets.length];
      edges.push({ o: o, m: m });
    }
  });

  edges.forEach(function (e) {
    var x1 = px(e.o.lon), y1 = py(e.o.lat), x2 = px(e.m.lon), y2 = py(e.m.lat);
    var mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - Math.abs(x2 - x1) * .10 - 8;
    e.node = el('path', {
      'class': 'dm-edge',
      d: 'M' + x1.toFixed(1) + ' ' + y1.toFixed(1) + ' Q' + mx.toFixed(1) + ' ' +
         my.toFixed(1) + ' ' + x2.toFixed(1) + ' ' + y2.toFixed(1)
    }, gEdge);
  });

  /* --- จุดผู้ร่วมสร้างคลัง --- */
  function total(p) {
    var t = 0; for (var k in p.c) t += p.c[k]; return t;
  }
  // ป้ายชื่อ ใส่เฉพาะจุดใหญ่ และเว้นจุดที่จะไปทับป้ายที่วางไว้แล้ว
  var labelled = [];
  function canLabel(p, t) {
    if (t < 150) return false;
    var x = px(p.lon), y = py(p.lat);
    for (var i = 0; i < labelled.length; i++) {
      if (Math.abs(labelled[i][0] - x) < 62 && Math.abs(labelled[i][1] - y) < 11) return false;
    }
    labelled.push([x, y]);
    return true;
  }

  places.slice().sort(function (a, b) { return total(b) - total(a); }).forEach(function (p) {
    var t = total(p);
    var r = Math.max(3.4, Math.min(15, Math.sqrt(t) * .78));
    var g = el('g', { 'class': 'dm-node ' + p.role, tabindex: '0', role: 'button',
                      'aria-label': p.n + ' — ' + t + ' participants' }, gNode);
    p.circle = el('circle', { cx: px(p.lon).toFixed(1), cy: py(p.lat).toFixed(1),
                              r: r.toFixed(1) }, g);
    if (canLabel(p, t)) {
      el('text', { x: (px(p.lon) + r + 3).toFixed(1), y: (py(p.lat) + 2.6).toFixed(1) }, g)
        .textContent = p.n;
    }
    p.g = g; p.r = r; p.total = t;
    g.addEventListener('click', function () { select(p); });
    g.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); select(p); }
    });
  });

  /* --- แผงรายละเอียด --- */
  var panel = document.getElementById('dm-panel');
  var selected = null, minScore = 0;

  function rows(list) {
    return '<div class="dm-rows">' + list.map(function (r) {
      return '<div class="dm-row"><span class="a">' + r[0] + '</span><span class="b">' + r[1] + '</span></div>';
    }).join('') + '</div>';
  }

  function overview() {
    selected = null;
    places.forEach(function (p) { p.g.classList.remove('sel'); });
    edges.forEach(function (e) { e.node.classList.remove('hi'); });
    panel.innerHTML =
      '<div class="k">The vault today</div>' +
      '<h3>5,000 contributors</h3>' +
      '<div class="sub">43 origins and markets · simulated</div>' +
      rows([
        ['Farmers', '<b>' + totals.farmers.toLocaleString() + '</b> · 80%'],
        ['Roasters', '<b>' + totals.roasters.toLocaleString() + '</b> · 10%'],
        ['Cooperatives', '<b>' + totals.coops + '</b>'],
        ['Mills &amp; washing stations', '<b>' + totals.mills + '</b>'],
        ['Exporters &amp; importers', '<b>' + totals.exporters + '</b>'],
        ['Cafés', '<b>' + totals.cafes + '</b>'],
        ['Researchers', '<b>' + totals.researchers + '</b>'],
        ['Certifiers', '<b>' + totals.certifiers + '</b>']
      ]) +
      '<p class="dm-note">Select any point on the map to see what that origin has ' +
      'put into the vault, and which roasters its profile matches.</p>';
  }

  function select(p) {
    selected = p;
    places.forEach(function (q) { q.g.classList.toggle('sel', q === p); });
    edges.forEach(function (e) { e.node.classList.toggle('hi', e.o === p || e.m === p); });

    var linked = edges.filter(function (e) { return e.o === p || e.m === p; })
      .map(function (e) { return e.o === p ? e.m.n : e.o.n; });
    var uniq = linked.filter(function (v, i) { return linked.indexOf(v) === i; });

    if (p.role === 'origin') {
      var lots = Math.round(p.c.farmers * 2.4);
      panel.innerHTML =
        '<div class="k">Origin</div><h3>' + p.n + '</h3>' +
        '<div class="sub">' + p.alt + ' · ' + p.proc + '</div>' +
        rows([
          ['Contributors', '<b>' + p.total.toLocaleString() + '</b>'],
          ['Farmers', '<b>' + p.c.farmers.toLocaleString() + '</b>'],
          ['Cooperatives / mills', '<b>' + (p.c.coops + p.c.mills) + '</b>'],
          ['Lots on record', '<b>' + lots.toLocaleString() + '</b>'],
          ['Mean cup score', '<b>' + p.score.toFixed(1) + '</b>'],
          ['Traceable to plot', '<b>' + (72 + (p.c.mills % 9) * 3) + '%</b>'],
          ['Flavour profile', p.notes]
        ]) +
        '<p class="dm-note">Buying this origin today means reading ' +
        uniq.length + ' verified routes into ' + uniq.slice(0, 3).join(', ') +
        (uniq.length > 3 ? ' and ' + (uniq.length - 3) + ' more' : '') + '.</p>' +
        '<button class="dm-act" data-act="match">Match this profile to roasters</button>' +
        '<button class="dm-act ghost" data-act="back">Back to overview</button>';
    } else {
      panel.innerHTML =
        '<div class="k">Market</div><h3>' + p.n + '</h3>' +
        '<div class="sub">roasters, cafés and importers</div>' +
        rows([
          ['Contributors', '<b>' + p.total.toLocaleString() + '</b>'],
          ['Roasters', '<b>' + p.c.roasters + '</b>'],
          ['Cafés', '<b>' + p.c.cafes + '</b>'],
          ['Importers', '<b>' + p.c.exporters + '</b>'],
          ['Origins sourced', '<b>' + uniq.length + '</b>'],
          ['Cupping results shared', '<b>' + (p.c.roasters * 34).toLocaleString() + '</b>']
        ]) +
        '<p class="dm-note">Every cupping result added here sharpens the ' +
        'benchmark a farmer sees on the other side of the map.</p>' +
        '<button class="dm-act ghost" data-act="back">Back to overview</button>';
    }
  }

  panel.addEventListener('click', function (ev) {
    var b = ev.target.closest('[data-act]');
    if (!b) return;
    if (b.dataset.act === 'back') return overview();
    if (b.dataset.act === 'match' && selected) {
      setLayer('match');
      document.querySelectorAll('.dm-tool[data-layer]').forEach(function (t) {
        t.classList.toggle('on', t.dataset.layer === 'match');
      });
    }
  });

  /* --- การหรี่จุดกับขนาดจุด รวมเงื่อนไขไว้ที่เดียว กันสองปุ่มแย่งกันสั่ง --- */
  var roleView = null;

  function radius(p) {
    var v = roleView ? p.c[roleView] : p.total;
    return Math.max(3.4, Math.min(15, Math.sqrt(v) * (roleView ? 1.9 : .78)));
  }

  function refresh() {
    places.forEach(function (p) {
      var byScore = p.role === 'origin' && p.score < minScore;
      var byRole = roleView && !p.c[roleView];
      p.g.classList.toggle('dim', !!(byScore || byRole));
      p.circle.setAttribute('r', radius(p).toFixed(1));
    });
  }

  function setLayer(name) {
    gEdge.style.display = (name === 'people') ? 'none' : '';
    edges.forEach(function (e) {
      var show = true;
      if (name === 'match' && selected) show = (e.o === selected || e.m === selected);
      if (name === 'quality') show = e.o.score >= 85;
      e.node.style.display = show ? '' : 'none';
      e.node.classList.toggle('hi', name === 'match' && selected &&
        (e.o === selected || e.m === selected));
    });
  }

  document.querySelectorAll('.dm-tool[data-layer]').forEach(function (t) {
    t.addEventListener('click', function () {
      document.querySelectorAll('.dm-tool[data-layer]').forEach(function (x) {
        x.classList.toggle('on', x === t);
      });
      setLayer(t.dataset.layer);
    });
  });

  var slider = document.getElementById('dm-score');
  if (slider) {
    slider.addEventListener('input', function () {
      minScore = parseFloat(slider.value);
      document.getElementById('dm-score-v').textContent =
        minScore === 0 ? 'any' : minScore.toFixed(1) + '+';
      refresh();
    });
  }

  /* --- ปุ่มสถิติด้านบน ใช้เน้นกลุ่มบทบาท --- */
  document.querySelectorAll('.dm-stat[data-role]').forEach(function (s) {
    function toggle() {
      var was = s.classList.contains('on');
      document.querySelectorAll('.dm-stat').forEach(function (x) { x.classList.remove('on'); });
      roleView = was ? null : s.dataset.role;
      if (!was) s.classList.add('on');
      refresh();
    }
    s.addEventListener('click', toggle);
    s.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); toggle(); }
    });
  });

  overview();
  setLayer('trade');
})();
