// Scratchpad tools for Maths: the "Work it out" pad offers the tools that fit the question's lesson
// (a column sum, a number line, counters and plates, a dot grid, fraction shapes, a clock, coins and notes,
// a ruler, tally marks, place-value blocks). Each tool keeps its own state per question; index.html mounts them.
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function sv(tag, attrs) { var e = document.createElementNS(NS, tag); for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }
  function btn(label, onClick, cls, aria) { var b = el('button', 'tl-b' + (cls ? ' ' + cls : ''), label); b.type = 'button'; if (aria) b.setAttribute('aria-label', aria); b.addEventListener('click', onClick); return b; }
  function row(cls) { return el('div', 'tl-row' + (cls ? ' ' + cls : '')); }
  function svgPoint(svg, e) { var r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal; return { x: (e.clientX - r.left) / r.width * vb.width, y: (e.clientY - r.top) / r.height * vb.height }; }
  function niceMax(n) { var s = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 100000]; for (var i = 0; i < s.length; i++) if (n <= s[i]) return s[i]; return 100000; }

  // ---------- column sum: H T O grid, carry boxes, a keypad. The two numbers from the question are written in ----------
  function columns(host, st, ctx) {
    if (!st.init) {
      st.init = true; var ns = ctx.nums.filter(function (n) { return n >= 10 || ctx.nums.length === 2; }).slice(0, 2);
      if (ns.length < 2) ns = ctx.nums.slice(0, 2);
      st.op = /take|left|fewer|less|change|more than|difference|minus|−|subtract|spent|gave away|how many more/i.test(ctx.text) ? '−' : /times|each|groups of|rows of|×/i.test(ctx.text) && ns.length === 2 && Math.min.apply(null, ns) < 10 ? '×' : '+';
      if (st.op === '−' && ns.length === 2 && ns[1] > ns[0]) ns = [ns[1], ns[0]];
      if (st.op === '×' && ns.length === 2 && ns[0] < ns[1]) ns = [ns[1], ns[0]];
      var w = Math.max(3, String(Math.max.apply(null, ns.concat([0]))).length + 1); st.cols = Math.min(6, w);
      st.cells = { carry: {}, a: {}, b: {}, ans: {} };
      ns.forEach(function (n, k) { String(Math.round(n)).split('').reverse().forEach(function (d, i) { if (i < st.cols) st.cells[k ? 'b' : 'a'][i] = d; }); });
      st.sel = ['ans', 0];
    }
    var NAMES = ['O', 'T', 'H', 'Th', 'TTh', 'L'], FULL = ['ones', 'tens', 'hundreds', 'thousands', 'ten thousands', 'lakhs'];
    var wrap = el('div', 'tl-col'), grid = el('div', 'tl-grid'); grid.style.gridTemplateColumns = '40px repeat(' + st.cols + ', minmax(0, 52px))';
    function cell(r, i) {
      var c = el('button', 'tl-cell tl-' + r + (st.sel[0] === r && st.sel[1] === i ? ' sel' : ''), st.cells[r][i] || ''); c.type = 'button';
      c.setAttribute('aria-label', (r === 'carry' ? 'carry' : r === 'ans' ? 'answer' : r === 'a' ? 'top number' : 'bottom number') + ', ' + FULL[i]);
      c.addEventListener('click', function () { st.sel = [r, i]; draw(); }); return c;
    }
    function draw() {
      grid.innerHTML = '';
      grid.appendChild(el('span', 'tl-h', ''));
      for (var i = st.cols - 1; i >= 0; i--) grid.appendChild(el('span', 'tl-h', NAMES[i]));
      ['carry', 'a', 'b', 'ans'].forEach(function (r) {
        if (r === 'b') { var o = btn(st.op, function () { st.op = st.op === '+' ? '−' : st.op === '−' ? '×' : '+'; draw(); }, 'tl-op', 'Change the sign: now ' + st.op); grid.appendChild(o); }
        else grid.appendChild(el('span', 'tl-h', r === 'carry' ? (st.op === '−' ? 'borrow' : 'carry') : r === 'ans' ? '=' : ''));
        for (var i = st.cols - 1; i >= 0; i--) grid.appendChild(cell(r, i));
        if (r === 'b') { var line = el('span', 'tl-line'); line.style.gridColumn = '1 / -1'; grid.appendChild(line); }
      });
    }
    var pad = row('tl-pad');
    '1234567890'.split('').forEach(function (d) { pad.appendChild(btn(d, function () { put(d); }, 'tl-key')); });
    pad.appendChild(btn('⌫', function () { put(''); }, 'tl-key', 'Delete'));
    function put(d) {
      var r = st.sel[0], i = st.sel[1]; st.cells[r][i] = d;
      if (d && r === 'ans' && i < st.cols - 1) st.sel = ['ans', i + 1]; // answers are written right to left
      draw();
    }
    wrap.appendChild(el('p', 'tl-tip', 'Tap a box, then a number. Start with the ones on the right.'));
    wrap.appendChild(grid); wrap.appendChild(pad); host.appendChild(wrap); draw();
  }

  // ---------- number line: tap to hop; each hop shows its size ----------
  function numberline(host, st, ctx) {
    var RANGES = [10, 20, 50, 100, 200, 500, 1000, 10000];
    if (!st.init) { st.init = true; st.hi = niceMax(Math.max(10, Math.max.apply(null, ctx.nums.concat([0])) * 1.05)); st.marks = []; }
    var wrap = el('div', 'tl-col'), top = row(), svg = sv('svg', { viewBox: '0 0 640 190', class: 'tl-svg', role: 'img', 'aria-label': 'Number line' }), out = el('p', 'tl-read');
    var i0 = RANGES.indexOf(st.hi);
    top.appendChild(btn('− zoom', function () { var i = Math.max(0, RANGES.indexOf(st.hi) - 1); st.hi = RANGES[i]; st.marks = []; draw(); }, '', 'Smaller numbers'));
    var lab = el('span', 'tl-lab'); top.appendChild(lab);
    top.appendChild(btn('+ zoom', function () { var i = Math.min(RANGES.length - 1, RANGES.indexOf(st.hi) + 1); st.hi = RANGES[i]; st.marks = []; draw(); }, '', 'Bigger numbers'));
    // ticks and labels at round numbers: at most 25 ticks and about 6 labels
    var NICE = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000];
    function tick() { for (var i = 0; i < NICE.length; i++) if (st.hi / NICE[i] <= 25) return NICE[i]; return st.hi / 20; }
    function labelStep() { if (st.hi <= 10) return 1; if (st.hi <= 20) return 2; for (var i = 0; i < NICE.length; i++) if (st.hi / NICE[i] <= 6) return NICE[i]; return st.hi / 5; }
    function X(v) { return 30 + v / st.hi * 580; }
    function draw() {
      svg.innerHTML = ''; lab.textContent = '0 to ' + st.hi.toLocaleString('en-IN');
      svg.appendChild(sv('line', { x1: 20, y1: 130, x2: 620, y2: 130, stroke: '#FFFDF5', 'stroke-width': 3, 'stroke-linecap': 'round' }));
      var t = tick(), ls = labelStep();
      for (var v = 0; v <= st.hi + 1e-9; v += t) {
        var big = Math.abs(v / ls - Math.round(v / ls)) < 1e-9;
        svg.appendChild(sv('line', { x1: X(v), y1: 122, x2: X(v), y2: 138, stroke: '#FFFDF5', 'stroke-width': big ? 2.5 : 1.5 }));
        if (big) { var tx = sv('text', { x: X(v), y: 162, 'text-anchor': 'middle', fill: '#FFFDF5', 'font-size': 15, 'font-weight': 700 }); tx.textContent = Math.round(v).toLocaleString('en-IN'); svg.appendChild(tx); }
      }
      st.marks.forEach(function (m, i) {
        if (i) { var a = X(st.marks[i - 1]), b = X(m), h = Math.min(90, 18 + Math.abs(b - a) * 0.45);
          svg.appendChild(sv('path', { d: 'M' + a + ' 126 Q' + (a + b) / 2 + ' ' + (126 - h * 1.5) + ' ' + b + ' 126', fill: 'none', stroke: '#FFD866', 'stroke-width': 3 }));
          var d = m - st.marks[i - 1], lt = sv('text', { x: (a + b) / 2, y: 126 - h * 0.78, 'text-anchor': 'middle', fill: '#FFD866', 'font-size': 16, 'font-weight': 800 }); lt.textContent = (d >= 0 ? '+' : '−') + Math.abs(+d.toFixed(2)); svg.appendChild(lt); }
        svg.appendChild(sv('circle', { cx: X(m), cy: 130, r: 8, fill: i ? '#FF9BC8' : '#FFB547' }));
      });
      out.textContent = st.marks.length ? 'Start ' + st.marks[0] + (st.marks.length > 1 ? ' → now at ' + st.marks[st.marks.length - 1] : '. Tap where to hop.') : 'Tap the line where you start, then tap to hop.';
    }
    svg.addEventListener('pointerdown', function (e) { var p = svgPoint(svg, e); if (p.y < 60) return; var t = tick(), v = Math.round(Math.min(st.hi, Math.max(0, (p.x - 30) / 580 * st.hi)) / t) * t; st.marks.push(+v.toFixed(2)); draw(); });
    wrap.appendChild(top); wrap.appendChild(svg); wrap.appendChild(out); host.appendChild(wrap); draw(); void i0;
  }

  // ---------- counters and plates: tap to add, drag to move, drag to the bin to remove, plates count what they hold ----------
  function counters(host, st, ctx) {
    if (!st.init) { st.init = true; st.items = []; st.plates = ctx.plates || 0; }
    var wrap = el('div', 'tl-col'), top = row(), area = el('div', 'tl-area'), out = el('p', 'tl-read'), bin = el('div', 'tl-bin', '🗑️');
    bin.setAttribute('aria-hidden', 'true');
    function addN(n) { for (var i = 0; i < n; i++) { var k = st.items.length; st.items.push({ x: 6 + (k % 10) * 9, y: 8 + Math.floor(k / 10) % 4 * 13 }); } draw(); }
    top.appendChild(btn('+1', function () { addN(1); }, '', 'Add 1 counter'));
    top.appendChild(btn('+5', function () { addN(5); }, '', 'Add 5 counters'));
    top.appendChild(btn('+10', function () { addN(10); }, '', 'Add 10 counters'));
    top.appendChild(el('span', 'tl-lab', 'Plates'));
    top.appendChild(btn('−', function () { st.plates = Math.max(0, st.plates - 1); draw(); }, '', 'One plate fewer'));
    var pn = el('b', 'tl-num'); top.appendChild(pn);
    top.appendChild(btn('+', function () { st.plates = Math.min(10, st.plates + 1); draw(); }, '', 'One more plate'));
    top.appendChild(btn('Deal out', function () { // one at a time into each plate in turn, like sharing by hand
      if (!st.plates) return; var P = plates(), k = 0;
      var have = P.map(function () { return 0; }); st.items.forEach(function (c) { var i = plateOf(c, P); if (i >= 0) have[i]++; });
      st.items.forEach(function (c) { if (plateOf(c, P) < 0) { var i = k % P.length, j = have[i]++, p = P[i], per = Math.max(1, Math.floor((p.r - p.l) / 7)); c.x = p.l + 4 + (j % per) * 7; c.y = 66 + Math.floor(j / per) % 4 * 8; k++; } }); draw();
    }, 'tl-go', 'Deal the loose counters into the plates'));
    // plates: trays across the bottom of the area (x from l to r, y below 58%)
    function plates() { var P = [], n = st.plates, w = 100 / Math.max(1, n); for (var i = 0; i < n; i++) P.push({ l: i * w + 1, r: (i + 1) * w - 1, x: (i + 0.5) * w }); return P; }
    function plateOf(c, P) { if (c.y < 58) return -1; for (var i = 0; i < P.length; i++) if (c.x >= P[i].l && c.x <= P[i].r) return i; return -1; }
    function draw() {
      area.innerHTML = ''; area.appendChild(bin); pn.textContent = st.plates; var P = plates(), cnt = P.map(function () { return 0; });
      P.forEach(function (p) { var d = el('div', 'tl-plate'); d.style.left = p.l + '%'; d.style.width = (p.r - p.l) + '%'; area.appendChild(d); });
      st.items.forEach(function (c, i) {
        var d = el('div', 'tl-ctr'); d.style.left = c.x + '%'; d.style.top = c.y + '%'; var pi = plateOf(c, P); if (pi >= 0) cnt[pi]++;
        d.addEventListener('pointerdown', function (e) { e.stopPropagation(); e.preventDefault(); drag(e, c, d); });
        area.appendChild(d);
      });
      P.forEach(function (p, i) { var n = el('span', 'tl-pc', cnt[i]); n.style.left = p.x + '%'; area.appendChild(n); });
      var loose = st.items.length - cnt.reduce(function (a, b) { return a + b; }, 0);
      out.textContent = st.items.length + ' counter' + (st.items.length === 1 ? '' : 's') + (st.plates ? ' · ' + cnt.join(' / ') + ' on the plates' + (loose ? ' · ' + loose + ' left over' : '') : '');
    }
    function drag(e, c, d) {
      var r = area.getBoundingClientRect(); d.setPointerCapture && d.setPointerCapture(e.pointerId);
      function mv(ev) { c.x = Math.max(2, Math.min(96, (ev.clientX - r.left) / r.width * 100)); c.y = Math.max(3, Math.min(94, (ev.clientY - r.top) / r.height * 100)); d.style.left = c.x + '%'; d.style.top = c.y + '%'; }
      function up(ev) {
        d.removeEventListener('pointermove', mv); d.removeEventListener('pointerup', up);
        var b = bin.getBoundingClientRect(); if (ev.clientX >= b.left - 6 && ev.clientX <= b.right + 6 && ev.clientY >= b.top - 6 && ev.clientY <= b.bottom + 6) st.items.splice(st.items.indexOf(c), 1);
        draw();
      }
      d.addEventListener('pointermove', mv); d.addEventListener('pointerup', up);
    }
    area.addEventListener('pointerdown', function (e) { if (e.target !== area) return; var r = area.getBoundingClientRect(); st.items.push({ x: (e.clientX - r.left) / r.width * 100, y: (e.clientY - r.top) / r.height * 100 }); draw(); });
    wrap.appendChild(top); wrap.appendChild(area); wrap.appendChild(out); host.appendChild(wrap); draw();
  }

  // ---------- dot grid: tap dot to dot to draw straight sides; a mirror line for symmetry ----------
  function dotgrid(host, st) {
    if (!st.init) { st.init = true; st.lines = []; st.from = null; st.mirror = false; }
    var C = 9, R = 6, wrap = el('div', 'tl-col'), top = row(), svg = sv('svg', { viewBox: '0 0 450 300', class: 'tl-svg tl-dots', role: 'img', 'aria-label': 'Dot grid' }), out = el('p', 'tl-read');
    top.appendChild(btn('Lift pen', function () { st.from = null; draw(); }));
    top.appendChild(btn('Undo line', function () { st.lines.pop(); st.from = st.lines.length ? st.lines[st.lines.length - 1][1] : null; draw(); }));
    var mb = btn('Mirror line', function () { st.mirror = !st.mirror; draw(); }); top.appendChild(mb);
    function P(p) { return { x: 25 + p[0] * 50, y: 25 + p[1] * 50 }; }
    function draw() {
      svg.innerHTML = ''; mb.classList.toggle('on', st.mirror); mb.setAttribute('aria-pressed', st.mirror);
      if (st.mirror) svg.appendChild(sv('line', { x1: 225, y1: 5, x2: 225, y2: 295, stroke: '#8FD3FF', 'stroke-width': 2, 'stroke-dasharray': '8 6' }));
      st.lines.forEach(function (l) {
        var a = P(l[0]), b = P(l[1]); svg.appendChild(sv('line', { x1: a.x, y1: a.y, x2: b.x, y2: b.y, stroke: '#FFD866', 'stroke-width': 4, 'stroke-linecap': 'round' }));
        if (st.mirror) svg.appendChild(sv('line', { x1: 450 - a.x, y1: a.y, x2: 450 - b.x, y2: b.y, stroke: '#FF9BC8', 'stroke-width': 3, 'stroke-dasharray': '6 5', 'stroke-linecap': 'round' }));
      });
      for (var y = 0; y < R; y++) for (var x = 0; x < C; x++) {
        var on = st.from && st.from[0] === x && st.from[1] === y, p = P([x, y]);
        var d = sv('circle', { cx: p.x, cy: p.y, r: on ? 9 : 5, fill: on ? '#FFB547' : '#FFFDF5' }); d.dataset.x = x; d.dataset.y = y; svg.appendChild(d);
      }
      out.textContent = st.lines.length ? st.lines.length + ' side' + (st.lines.length === 1 ? '' : 's') + ' drawn' + (st.mirror ? ' · the pink lines are the mirror image' : '') : 'Tap a dot, then another dot to draw a straight side.';
    }
    svg.addEventListener('pointerdown', function (e) {
      var p = svgPoint(svg, e), x = Math.round((p.x - 25) / 50), y = Math.round((p.y - 25) / 50);
      if (x < 0 || y < 0 || x >= C || y >= R) return;
      if (st.from && (st.from[0] !== x || st.from[1] !== y)) st.lines.push([st.from, [x, y]]);
      st.from = [x, y]; draw();
    });
    wrap.appendChild(top); wrap.appendChild(svg); wrap.appendChild(out); host.appendChild(wrap); draw();
  }

  // ---------- fraction shapes: pick a shape and how many equal parts, tap parts to colour them ----------
  function fraction(host, st) {
    if (!st.init) { st.init = true; st.shape = 'circle'; st.parts = 4; st.on = []; }
    var wrap = el('div', 'tl-col'), top = row(), top2 = row(), svg = sv('svg', { viewBox: '0 0 300 220', class: 'tl-svg tl-frac', role: 'img', 'aria-label': 'Fraction shape' }), out = el('p', 'tl-read');
    [['circle', '⚪ Circle'], ['bar', '▭ Bar'], ['square', '⬜ Square']].forEach(function (s) { var b = btn(s[1], function () { st.shape = s[0]; st.on = []; draw(); }); b.dataset.s = s[0]; top.appendChild(b); });
    top2.appendChild(el('span', 'tl-lab', 'Parts'));
    [2, 3, 4, 5, 6, 8, 10].forEach(function (n) { var b = btn(String(n), function () { st.parts = n; st.on = []; draw(); }); b.dataset.n = n; top2.appendChild(b); });
    function draw() {
      svg.innerHTML = ''; var n = st.parts;
      top.querySelectorAll('[data-s]').forEach(function (b) { b.classList.toggle('on', b.dataset.s === st.shape); });
      top2.querySelectorAll('[data-n]').forEach(function (b) { b.classList.toggle('on', +b.dataset.n === n); });
      for (var i = 0; i < n; i++) {
        var on = st.on.indexOf(i) >= 0, attrs = { fill: on ? '#FFB547' : 'rgba(255,253,245,.08)', stroke: '#FFFDF5', 'stroke-width': 2.5 }, s;
        if (st.shape === 'circle') {
          var a0 = i / n * 2 * Math.PI - Math.PI / 2, a1 = (i + 1) / n * 2 * Math.PI - Math.PI / 2, r = 95, cx = 150, cy = 110;
          attrs.d = n === 1 ? '' : 'M' + cx + ' ' + cy + ' L' + (cx + r * Math.cos(a0)) + ' ' + (cy + r * Math.sin(a0)) + ' A' + r + ' ' + r + ' 0 ' + (a1 - a0 > Math.PI ? 1 : 0) + ' 1 ' + (cx + r * Math.cos(a1)) + ' ' + (cy + r * Math.sin(a1)) + ' Z';
          s = sv('path', attrs);
        } else if (st.shape === 'square' && n === 4) { attrs.x = 60 + (i % 2) * 90; attrs.y = 20 + Math.floor(i / 2) * 90; attrs.width = 90; attrs.height = 90; s = sv('rect', attrs); }
        else { var W = st.shape === 'bar' ? 260 : 180, H = st.shape === 'bar' ? 80 : 180, x0 = 150 - W / 2, y0 = 110 - H / 2; attrs.x = x0 + i * W / n; attrs.y = y0; attrs.width = W / n; attrs.height = H; s = sv('rect', attrs); }
        s.dataset.i = i; s.style.cursor = 'pointer'; svg.appendChild(s);
      }
      var k = st.on.length; out.textContent = k + ' of ' + n + ' equal parts coloured = ' + k + '/' + n + (k * 2 === n ? ' = one half' : k * 4 === n ? ' = one quarter' : '');
    }
    svg.addEventListener('pointerdown', function (e) { var i = e.target.dataset && e.target.dataset.i; if (i == null) return; i = +i; var j = st.on.indexOf(i); if (j >= 0) st.on.splice(j, 1); else st.on.push(i); draw(); });
    wrap.appendChild(top); wrap.appendChild(top2); wrap.appendChild(svg); wrap.appendChild(out); host.appendChild(wrap); draw();
  }

  // ---------- clock: drag the hands, or step by 5 minutes / 1 hour; it says the time in words ----------
  function clock(host, st) {
    if (!st.init) { st.init = true; st.t = 3 * 60; }
    var wrap = el('div', 'tl-col'), top = row(), svg = sv('svg', { viewBox: '0 0 220 220', class: 'tl-svg tl-clock', role: 'img', 'aria-label': 'Clock' }), out = el('p', 'tl-read');
    top.appendChild(btn('−1 hour', function () { st.t = (st.t + 660) % 720; draw(); }));
    top.appendChild(btn('−5 min', function () { st.t = (st.t + 715) % 720; draw(); }));
    top.appendChild(btn('+5 min', function () { st.t = (st.t + 5) % 720; draw(); }));
    top.appendChild(btn('+1 hour', function () { st.t = (st.t + 60) % 720; draw(); }));
    function words(h, m) {
      var nh = h % 12 + 1; if (m === 0) return h + " o'clock"; if (m === 30) return 'half past ' + h; if (m === 15) return 'quarter past ' + h; if (m === 45) return 'quarter to ' + nh;
      return m < 30 ? m + ' minutes past ' + h : (60 - m) + ' minutes to ' + nh;
    }
    function hand(len, ang, w, col) { var a = (ang - 90) * Math.PI / 180; return sv('line', { x1: 110, y1: 110, x2: 110 + len * Math.cos(a), y2: 110 + len * Math.sin(a), stroke: col, 'stroke-width': w, 'stroke-linecap': 'round' }); }
    function draw() {
      svg.innerHTML = ''; svg.appendChild(sv('circle', { cx: 110, cy: 110, r: 100, fill: '#FFFDF5', stroke: '#8A5A2B', 'stroke-width': 6 }));
      for (var i = 0; i < 60; i++) { var a = i * 6 * Math.PI / 180, r1 = i % 5 ? 90 : 84; svg.appendChild(sv('line', { x1: 110 + r1 * Math.sin(a), y1: 110 - r1 * Math.cos(a), x2: 110 + 95 * Math.sin(a), y2: 110 - 95 * Math.cos(a), stroke: '#2A1330', 'stroke-width': i % 5 ? 1 : 3 })); }
      for (var n = 1; n <= 12; n++) { var b = n * 30 * Math.PI / 180, t = sv('text', { x: 110 + 70 * Math.sin(b), y: 116 - 70 * Math.cos(b), 'text-anchor': 'middle', 'font-size': 17, 'font-weight': 800, fill: '#2A1330' }); t.textContent = n; svg.appendChild(t); }
      var h = Math.floor(st.t / 60) % 12 || 12, m = st.t % 60;
      svg.appendChild(hand(48, (st.t % 720) / 2, 7, '#2A1330')); svg.appendChild(hand(78, m * 6, 4, '#E0569A'));
      svg.appendChild(sv('circle', { cx: 110, cy: 110, r: 6, fill: '#2A1330' }));
      out.textContent = h + ':' + (m < 10 ? '0' : '') + m + '  ·  ' + words(h, m);
    }
    var dragging = null;
    svg.addEventListener('pointerdown', function (e) {
      var p = svgPoint(svg, e), dx = p.x - 110, dy = p.y - 110, ang = (Math.atan2(dx, -dy) * 180 / Math.PI + 360) % 360, d = Math.hypot(dx, dy);
      dragging = d > 58 ? 'm' : 'h'; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); move(ang);
    });
    function move(ang) {
      if (dragging === 'm') { var m = Math.round(ang / 6) % 60, old = st.t % 60, hrs = Math.floor(st.t / 60); if (old > 45 && m < 15) hrs++; else if (old < 15 && m > 45) hrs--; st.t = ((hrs * 60 + m) % 720 + 720) % 720; }
      else { var hh = Math.floor(ang / 30); st.t = hh * 60 + st.t % 60; }
      draw();
    }
    svg.addEventListener('pointermove', function (e) { if (!dragging) return; var p = svgPoint(svg, e); move((Math.atan2(p.x - 110, -(p.y - 110)) * 180 / Math.PI + 360) % 360); });
    svg.addEventListener('pointerup', function () { dragging = null; });
    wrap.appendChild(top); wrap.appendChild(svg); wrap.appendChild(out); host.appendChild(wrap); draw();
  }

  // ---------- money: tap coins and notes to put them on the tray; it adds them up ----------
  function money(host, st) {
    if (!st.init) { st.init = true; st.items = []; }
    var wrap = el('div', 'tl-col'), top = row('tl-coins'), tray = el('div', 'tl-tray'), out = el('p', 'tl-read tl-big');
    [1, 2, 5, 10, 20, 50, 100, 200, 500].forEach(function (v) { top.appendChild(btn('₹' + v, function () { st.items.push(v); draw(); }, v >= 20 ? 'tl-note' : 'tl-coin', 'Add ₹' + v)); });
    function draw() {
      tray.innerHTML = ''; var sum = 0;
      st.items.forEach(function (v, i) { sum += v; tray.appendChild(btn('₹' + v, function () { st.items.splice(i, 1); draw(); }, v >= 20 ? 'tl-note' : 'tl-coin', 'Take away ₹' + v)); });
      if (!st.items.length) tray.appendChild(el('span', 'tl-tip', 'Tap coins and notes to put them here. Tap one here to take it back.'));
      out.textContent = 'Total: ₹' + sum.toLocaleString('en-IN');
    }
    wrap.appendChild(top); wrap.appendChild(tray); wrap.appendChild(out); host.appendChild(wrap); draw();
  }

  // ---------- ruler: drag the arrow to measure; the unit facts sit beside it ----------
  function ruler(host, st) {
    if (!st.init) { st.init = true; st.len = 5; }
    var wrap = el('div', 'tl-col'), svg = sv('svg', { viewBox: '0 0 640 130', class: 'tl-svg', role: 'img', 'aria-label': 'Ruler' }), out = el('p', 'tl-read tl-big'), facts = el('div', 'tl-facts');
    ['1 m = 100 cm', '1 km = 1000 m', '1 kg = 1000 g', '1 L = 1000 mL', '1 hour = 60 min', '1 day = 24 hours'].forEach(function (f) { facts.appendChild(el('span', null, f)); });
    function X(cm) { return 20 + cm * 40; }
    function draw() {
      svg.innerHTML = ''; svg.appendChild(sv('rect', { x: 8, y: 40, width: 624, height: 70, rx: 8, fill: '#FFD866', stroke: '#8A5A2B', 'stroke-width': 3 }));
      for (var mm = 0; mm <= 150; mm++) { var x = 20 + mm * 4; svg.appendChild(sv('line', { x1: x, y1: 40, x2: x, y2: 40 + (mm % 10 ? (mm % 5 ? 12 : 20) : 30), stroke: '#2A1330', 'stroke-width': mm % 10 ? 1 : 2 }));
        if (mm % 10 === 0) { var t = sv('text', { x: x, y: 96, 'text-anchor': 'middle', 'font-size': 14, 'font-weight': 800, fill: '#2A1330' }); t.textContent = mm / 10; svg.appendChild(t); } }
      svg.appendChild(sv('rect', { x: X(0), y: 14, width: X(st.len) - X(0), height: 14, rx: 7, fill: '#E0569A' }));
      svg.appendChild(sv('path', { d: 'M' + X(st.len) + ' 4 l12 0 l-12 30 l-12 -30 z', fill: '#FFFDF5', stroke: '#E0569A', 'stroke-width': 3 }));
      out.textContent = st.len + ' cm' + (st.len >= 10 ? ' = ' + st.len * 10 + ' mm' : '');
    }
    var drag = false;
    function set(e) { var p = svgPoint(svg, e); st.len = Math.max(0, Math.min(15, Math.round((p.x - 20) / 40 * 2) / 2)); draw(); }
    svg.addEventListener('pointerdown', function (e) { drag = true; svg.setPointerCapture && svg.setPointerCapture(e.pointerId); set(e); });
    svg.addEventListener('pointermove', function (e) { if (drag) set(e); });
    svg.addEventListener('pointerup', function () { drag = false; });
    wrap.appendChild(el('p', 'tl-tip', 'Drag the arrow along the ruler.')); wrap.appendChild(svg); wrap.appendChild(out); wrap.appendChild(facts); host.appendChild(wrap); draw();
  }

  // ---------- tally: tap + to add a mark; every fifth mark crosses the four before it ----------
  function tally(host, st) {
    if (!st.init) { st.init = true; st.rows = [['🍎', 0], ['🍌', 0], ['🍊', 0], ['🍇', 0]]; }
    var wrap = el('div', 'tl-col'), list = el('div', 'tl-tally');
    function draw() {
      list.innerHTML = '';
      st.rows.forEach(function (r, i) {
        var line = el('div', 'tl-trow'); line.appendChild(el('span', 'tl-tico', r[0]));
        var marks = el('span', 'tl-marks'); for (var g = 0; g < Math.ceil(r[1] / 5); g++) { var n = Math.min(5, r[1] - g * 5), s = el('span', 'tl-tg' + (n === 5 ? ' five' : '')); for (var k = 0; k < Math.min(4, n); k++) s.appendChild(el('i')); marks.appendChild(s); }
        line.appendChild(marks); line.appendChild(el('b', 'tl-num', r[1]));
        line.appendChild(btn('−', function () { r[1] = Math.max(0, r[1] - 1); draw(); }, '', 'One fewer ' + r[0]));
        line.appendChild(btn('+', function () { r[1]++; draw(); }, 'tl-go', 'One more ' + r[0]));
        list.appendChild(line);
      });
    }
    wrap.appendChild(list); host.appendChild(wrap); draw();
  }

  // ---------- place value: hundreds, tens and ones blocks; it reads the number back ----------
  function placevalue(host, st, ctx) {
    if (!st.init) { st.init = true; st.big = ctx.nums.some(function (n) { return n >= 1000; }); st.v = { th: 0, h: 0, t: 0, o: 0 }; }
    var wrap = el('div', 'tl-col'), cols = el('div', 'tl-pv'), out = el('p', 'tl-read tl-big'), ex = el('p', 'tl-tip');
    var C = (st.big ? [['th', 'Thousands', 1000]] : []).concat([['h', 'Hundreds', 100], ['t', 'Tens', 10], ['o', 'Ones', 1]]);
    function block(k) { return k === 'th' ? 'tl-bth' : k === 'h' ? 'tl-bh' : k === 't' ? 'tl-bt' : 'tl-bo'; }
    function draw() {
      cols.innerHTML = ''; var total = 0, parts = [];
      C.forEach(function (c) {
        var n = st.v[c[0]]; total += n * c[2]; if (n) parts.push(n + ' ' + c[1].toLowerCase());
        var col = el('div', 'tl-pvc'); col.appendChild(el('b', null, c[1]));
        var box = el('div', 'tl-blocks'); for (var i = 0; i < n; i++) box.appendChild(el('i', block(c[0]))); col.appendChild(box);
        var r = row(); r.appendChild(btn('−', function () { st.v[c[0]] = Math.max(0, n - 1); draw(); }, '', 'One fewer ' + c[1])); r.appendChild(el('b', 'tl-num', n)); r.appendChild(btn('+', function () { st.v[c[0]] = Math.min(9, n + 1); draw(); }, 'tl-go', 'One more ' + c[1])); col.appendChild(r);
        cols.appendChild(col);
      });
      out.textContent = total.toLocaleString('en-IN'); ex.textContent = parts.length ? parts.join(' + ') + ' = ' + total.toLocaleString('en-IN') : 'Add blocks to build a number.';
    }
    wrap.appendChild(cols); wrap.appendChild(out); wrap.appendChild(ex); host.appendChild(wrap); draw();
  }

  var TOOLS = {
    columns: { label: 'Column sum', icon: '🧮', build: columns }, numberline: { label: 'Number line', icon: '📏', build: numberline },
    counters: { label: 'Counters', icon: '🔴', build: counters }, dotgrid: { label: 'Dot grid', icon: '⬡', build: dotgrid },
    fraction: { label: 'Fractions', icon: '🍕', build: fraction }, clock: { label: 'Clock', icon: '🕒', build: clock },
    money: { label: 'Money', icon: '🪙', build: money }, ruler: { label: 'Ruler', icon: '📐', build: ruler },
    tally: { label: 'Tally', icon: '𝍸', build: tally }, placevalue: { label: 'Blocks', icon: '🧱', build: placevalue }
  };
  // which tools fit each lesson (first = opened first)
  var BY_LESSON = {
    m2_groups: ['counters', 'numberline'], m2_shapes: ['dotgrid'], m2_numbers: ['placevalue', 'numberline'], m2_flat: ['dotgrid'], m2_lines: ['dotgrid'],
    m2_addsub: ['columns', 'numberline', 'placevalue'], m2_measure: ['ruler', 'numberline'], m2_share: ['counters'], m2_time: ['clock'],
    m2_money: ['money', 'columns'], m2_data: ['tally'], m2_challenge: ['columns', 'counters', 'money'],
    m3_thousand: ['placevalue', 'numberline'], m3_add: ['columns', 'numberline'], m3_sub: ['columns', 'numberline'], m3_times: ['counters', 'columns', 'numberline'],
    m3_divide: ['counters', 'columns'], m3_fractions: ['fraction', 'counters'], m3_measure: ['ruler', 'columns'], m3_time: ['clock', 'numberline'],
    m3_money: ['money', 'columns'], m3_shapes: ['dotgrid', 'ruler'], m3_data: ['tally', 'columns'], m3_fair: ['columns', 'money', 'counters'],
    m4_lakh: ['placevalue', 'numberline'], m4_mult: ['columns', 'counters'], m4_div: ['columns', 'counters'], m4_frac: ['fraction', 'numberline'],
    m4_dec: ['numberline', 'money', 'columns'], m4_units: ['ruler', 'columns'], m4_area: ['dotgrid', 'columns'], m4_angles: ['dotgrid', 'clock'],
    m4_factors: ['counters', 'columns'], m4_graphs: ['tally', 'columns'], m4_time24: ['clock', 'numberline'], m4_bazaar: ['columns', 'money', 'fraction']
  };
  function forLesson(key, text) {
    var t = (BY_LESSON[key] || []).slice();
    // a question can need a tool its lesson does not usually offer
    if (/o'clock|half past|quarter (to|past)|minutes/i.test(text || '') && t.indexOf('clock') < 0) t.push('clock');
    if (/₹|rupee/i.test(text || '') && t.indexOf('money') < 0) t.push('money');
    return t.filter(function (x) { return TOOLS[x]; });
  }
  function numbersIn(text) { return (String(text || '').replace(/<[^>]+>/g, ' ').replace(/,(?=\d{2})/g, '').match(/\d+(?:\.\d+)?/g) || []).map(Number); }
  function mount(id, host, st, q) {
    host.innerHTML = ''; var text = String((q && q.text) || '').replace(/<[^>]+>/g, ' ');
    var ctx = { text: text, nums: numbersIn(text), plates: (text.match(/(\d+)\s+(?:children|friends|plates|bags|boxes|groups|kids)/i) || [])[1] | 0 };
    TOOLS[id].build(host, st, ctx);
  }
  var css = '\
.scratch-tabs{display:flex;gap:6px;padding:0 12px 8px;overflow-x:auto;scrollbar-width:none}\
.scratch-tabs::-webkit-scrollbar{display:none}\
.scratch-tabs button{flex:none;min-height:38px;padding:0 12px;border-radius:999px;border:2px solid rgba(255,255,255,.22);background:rgba(255,255,255,.06);color:#FFFDF5;font:inherit;font-weight:800;font-size:14px;cursor:pointer;white-space:nowrap}\
.scratch-tabs button[aria-selected=true]{background:#FFFDF5;color:#1F3B2E;border-color:#FFFDF5}\
.scratch-tool{flex:1;min-height:0;overflow:auto;border-top:2px dashed rgba(255,255,255,.12);padding:10px 12px;color:#FFFDF5;touch-action:manipulation}\
.scratch-tool[hidden]{display:none}\
.tl-col{display:flex;flex-direction:column;gap:10px;align-items:stretch;min-height:100%}\
.tl-row{display:flex;flex-wrap:wrap;gap:6px;align-items:center}\
.tl-b{min-height:38px;min-width:38px;padding:0 10px;border-radius:10px;border:2px solid rgba(255,255,255,.25);background:rgba(255,255,255,.08);color:#FFFDF5;font:inherit;font-weight:800;cursor:pointer}\
.tl-b.on,.tl-b.tl-go{background:#FFB547;border-color:#FFB547;color:#2A1330}\
.tl-b:focus-visible,.tl-cell:focus-visible{outline:3px solid #8FD3FF;outline-offset:2px}\
.tl-lab{font-weight:800;opacity:.8;margin:0 4px}.tl-num{min-width:26px;text-align:center;font-size:18px}\
.tl-tip{margin:0;font-size:13px;opacity:.75}.tl-read{margin:0;font-weight:800;font-size:16px;text-align:center;color:#FFD866}.tl-big{font-size:24px}\
.tl-svg{width:100%;max-height:34vh;touch-action:none;user-select:none}.tl-clock{max-height:26vh}.tl-frac{max-height:24vh}\
.tl-grid{display:grid;gap:6px;justify-content:center;align-items:center}\
.tl-h{text-align:center;font-weight:800;font-size:13px;opacity:.7}\
.tl-cell{height:46px;border-radius:10px;border:2px solid rgba(255,255,255,.3);background:rgba(255,255,255,.06);color:#FFFDF5;font:700 24px/1 inherit;cursor:pointer;padding:0}\
.tl-cell.tl-carry{height:30px;font-size:15px;color:#FF9BC8;border-style:dashed}.tl-cell.tl-ans{color:#FFD866}\
.tl-cell.sel{border-color:#FFB547;box-shadow:0 0 0 3px rgba(255,181,71,.35)}\
.tl-op{font-size:22px}.tl-line{height:3px;background:#FFFDF5;border-radius:2px}\
.tl-pad{justify-content:center}.tl-key{min-width:44px;min-height:44px;font-size:18px}\
.tl-area{position:relative;flex:1;min-height:200px;border-radius:14px;background:rgba(255,255,255,.04);touch-action:none;overflow:hidden}\
.tl-ctr{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#FF9BA0,#E0473F);box-shadow:0 2px 0 rgba(0,0,0,.35);cursor:grab;touch-action:none}\
.tl-plate{position:absolute;top:58%;bottom:4%;border-radius:18px;background:rgba(255,253,245,.1);border:3px solid rgba(255,253,245,.5);pointer-events:none}\
.tl-pc{position:absolute;bottom:4px;transform:translateX(-50%);font-weight:800;color:#FFD866}\
.tl-bin{position:absolute;right:6px;top:6px;font-size:26px;opacity:.75;pointer-events:none}\
.tl-coins{justify-content:center}.tl-tray{flex:1;min-height:120px;display:flex;flex-wrap:wrap;gap:6px;align-content:flex-start;padding:8px;border-radius:14px;background:rgba(255,255,255,.04)}\
.tl-coin{border-radius:50%;min-width:46px;min-height:46px;padding:0;background:#E7C16B;color:#3A2A08;border-color:#B48A2F}\
.tl-note{border-radius:6px;min-width:62px;background:#9FD9A8;color:#173D21;border-color:#4F9A5C}\
.tl-facts{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}.tl-facts span{padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.08);font-weight:700;font-size:13px}\
.tl-tally{display:flex;flex-direction:column;gap:8px}.tl-trow{display:flex;align-items:center;gap:8px}\
.tl-tico{font-size:24px;width:32px}.tl-marks{flex:1;display:flex;flex-wrap:wrap;gap:10px;min-height:34px;align-items:center}\
.tl-tg{position:relative;display:inline-flex;gap:4px;height:30px}.tl-tg i{width:3px;height:30px;background:#FFFDF5;border-radius:2px}\
.tl-tg.five::after{content:"";position:absolute;left:-4px;right:-4px;top:13px;height:3px;background:#FFD866;transform:rotate(-28deg)}\
.tl-pv{display:flex;gap:8px;justify-content:center}.tl-pvc{flex:1;max-width:160px;display:flex;flex-direction:column;align-items:center;gap:6px;padding:8px;border-radius:12px;background:rgba(255,255,255,.05)}\
.tl-pvc>b{font-size:13px;opacity:.8}.tl-blocks{min-height:86px;display:flex;flex-wrap:wrap;gap:3px;justify-content:center;align-content:flex-start}\
.tl-blocks i{display:block;background:#8FD3FF;border:1px solid #1F3B2E}.tl-bo{width:12px;height:12px}.tl-bt{width:12px;height:44px;background:#FFB547!important}\
.tl-bh{width:36px;height:36px;background:#FF9BC8!important}.tl-bth{width:40px;height:40px;background:#C3A6FF!important;box-shadow:4px -4px 0 #9A7BE0}\
@media (max-width:420px){.tl-cell{height:42px;font-size:21px}.tl-key{min-width:40px;min-height:42px}.tl-pv{gap:4px}.tl-pvc{padding:6px 4px}}';
  var s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
  window.CQTools = { TOOLS: TOOLS, forLesson: forLesson, mount: mount, numbersIn: numbersIn };
})();
