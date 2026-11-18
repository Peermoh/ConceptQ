// Build-it-yourself puzzle, shared by house.html and world.html.
// After a lesson, the new part of the house / town is cut into square pieces of the scene around it;
// the learner drags (or taps) each piece into its place, and then the page plays its normal build moment.
//   CQPuzzle.start({ svg: rootSvg, parts: [elements], title: 'Build the fruit stall!', onDone: fn })
// Pieces: 9 for age 8 and under, 12 up to 11, 16 from 12 (age from the app's cq-profile).
// Inside the app, 10 embers place one piece for you (the app checks and spends them).
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  function css() {
    if (document.getElementById('pzCss')) return;
    var st = document.createElement('style'); st.id = 'pzCss';
    st.textContent =
      '.pz{position:fixed;inset:0;z-index:50;display:flex;flex-direction:column;align-items:center;gap:12px;padding:max(14px,env(safe-area-inset-top)) 16px max(14px,env(safe-area-inset-bottom));background:rgba(20,8,28,.9);color:#FFF6EC;font-family:Nunito,system-ui,sans-serif;overflow:auto;touch-action:none;animation:pzIn .3s ease-out}' +
      '@keyframes pzIn{from{opacity:0}}' +
      '.pz h2{margin:6px 0 0;font-size:21px;font-weight:900;text-align:center}' +
      '.pz p{margin:0;font-size:14px;font-weight:700;opacity:.8;text-align:center}' +
      '.pz-main{display:flex;flex-wrap:wrap;gap:16px;justify-content:center;align-items:center;flex:1;min-height:0}' +
      '.pz-board{position:relative;background:#2A1330;border:4px solid #FFB547;border-radius:14px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.4)}' +
      '.pz-ghost{position:absolute;inset:0;opacity:.16;filter:grayscale(1)}' +
      '.pz-slot{position:absolute;border:1.5px dashed rgba(255,246,236,.35);box-sizing:border-box;background:none;padding:0;cursor:pointer}' +
      '.pz-slot.hint{border-color:#7CF5C8;border-style:solid;background:rgba(124,245,200,.18)}' +
      '.pz-tray{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;align-content:center;max-width:min(560px,100%)}' +
      '.pz-piece{position:relative;flex:0 0 auto;border:2.5px solid #FFF6EC;border-radius:8px;overflow:hidden;background:#2A1330;padding:0;cursor:grab;box-shadow:0 6px 14px rgba(0,0,0,.4);touch-action:none;transition:transform .15s}' +
      '.pz-piece svg,.pz-ghost svg,.pz-slot svg{display:block;width:100%;height:100%;pointer-events:none}' +
      '.pz-piece.sel{border-color:#7CF5C8;transform:scale(1.06)}' +
      '.pz-piece.drag{position:fixed;z-index:60;cursor:grabbing;transform:scale(1.08);transition:none}' +
      '.pz-piece.shake{animation:pzShake .35s}@keyframes pzShake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}' +
      '.pz-placed{position:absolute;animation:pzSnap .3s cubic-bezier(.3,1.5,.5,1)}@keyframes pzSnap{from{transform:scale(1.2)}}' +
      '.pz-board.done{border-color:#7CF5C8;box-shadow:0 0 0 6px rgba(124,245,200,.35),0 10px 30px rgba(0,0,0,.4)}' +
      '.pz-board.done .pz-placed{outline:none}' +
      '.pz-back{position:absolute;left:12px;top:max(12px,env(safe-area-inset-top));width:42px;height:42px;border-radius:12px;border:1.5px solid rgba(255,246,236,.35);background:rgba(255,255,255,.08);color:#FFF6EC;font-size:22px;font-weight:900;cursor:pointer}' +
      '.pz-help{border:0;border-radius:999px;padding:10px 16px;background:#FFB547;color:#2A1330;font:inherit;font-weight:900;font-size:14px;cursor:pointer}' +
      '.pz-help:disabled{opacity:.45;cursor:default}' +
      '.pz-skip{background:none;border:0;color:#FFF6EC;opacity:.7;font:inherit;font-weight:800;font-size:14px;text-decoration:underline;cursor:pointer;padding:8px}' +
      '.pz-cheer{font-size:26px;font-weight:900;color:#7CF5C8;min-height:34px;text-align:center}' +
      '@media (prefers-reduced-motion:reduce){.pz,.pz-placed,.pz-piece.shake{animation:none}}';
    document.head.appendChild(st);
  }
  function grid() {
    var age = 9; try { var p = JSON.parse(localStorage.getItem('cq-profile') || 'null'); if (p && typeof p.age === 'number') age = p.age; } catch (e) {}
    return age <= 8 ? [3, 3] : age <= 11 ? [4, 3] : [4, 4];
  }
  // the part's box in the root svg's own units
  function regionOf(svg, parts, cols, rows) {
    var inv = svg.getScreenCTM().inverse(), x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    parts.forEach(function (el) {
      var r = el.getBoundingClientRect(); if (!r.width && !r.height) return;
      [[r.left, r.top], [r.right, r.bottom]].forEach(function (c) {
        var pt = svg.createSVGPoint(); pt.x = c[0]; pt.y = c[1]; pt = pt.matrixTransform(inv);
        x0 = Math.min(x0, pt.x); y0 = Math.min(y0, pt.y); x1 = Math.max(x1, pt.x); y1 = Math.max(y1, pt.y);
      });
    });
    if (x0 > x1) return null;
    var vb = svg.viewBox.baseVal, minSide = Math.min(vb.width, vb.height) * 0.42;
    var w = Math.max(x1 - x0, 10) * 1.3, h = Math.max(y1 - y0, 10) * 1.3, aspect = cols / rows;
    w = Math.max(w, minSide * aspect); h = Math.max(h, minSide);
    if (w / h > aspect) h = w / aspect; else w = h * aspect;
    var cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    return { x: cx - w / 2, y: cy - h / 2, w: w, h: h };
  }
  function pic(src, vb) {
    var s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', vb.join(' ')); s.setAttribute('preserveAspectRatio', 'none');
    s.innerHTML = src; return s;
  }
  function start(o) {
    var svg = o.svg, parts = o.parts.filter(Boolean), done = o.onDone || function () {};
    if (!svg || !parts.length || !svg.getScreenCTM) { done(); return; }
    var g = grid(), cols = g[0], rows = g[1], R = regionOf(svg, parts, cols, rows);
    if (!R) { done(); return; }
    css();
    // the scene as it will look once built (animation classes removed so nothing is mid-flight)
    var src = svg.innerHTML.replace(/\b(build-drop|build-rise|roof-lift|roof-drop|pop|arrive|puff)\b/g, '');
    parts.forEach(function (el) { el.style.visibility = 'hidden'; });
    var tw = R.w / cols, th = R.h / rows;
    var maxW = Math.min(window.innerWidth - 32, 420), maxH = Math.min(window.innerHeight * 0.42, 360);
    var bw = Math.min(maxW, maxH * cols / rows), bh = bw * rows / cols, pw = bw / cols, ph = bh / rows;
    var ov = document.createElement('div'); ov.className = 'pz'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-label', o.title || 'Build it');
    ov.innerHTML = '<button class="pz-back" type="button" aria-label="Back to lessons">'+'\u2190'+'</button><h2></h2><p>Drag each piece into its place. You can also tap a piece, then tap its spot.</p><div class="pz-main"><div class="pz-board"></div><div class="pz-tray"></div></div><div class="pz-cheer" aria-live="polite"></div><button class="pz-help" type="button" hidden>✨ Place a piece · 10 🔥</button><button class="pz-skip" type="button">Let Nibb build it</button>';
    ov.querySelector('h2').textContent = o.title || 'Build it!';
    document.body.appendChild(ov);
    var board = ov.querySelector('.pz-board'), tray = ov.querySelector('.pz-tray'), cheer = ov.querySelector('.pz-cheer');
    board.style.width = bw + 'px'; board.style.height = bh + 'px';
    var ghost = document.createElement('div'); ghost.className = 'pz-ghost'; ghost.appendChild(pic(src, [R.x, R.y, R.w, R.h])); board.appendChild(ghost);
    var placed = 0, total = cols * rows, sel = null, slots = [];
    for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) {
      var sl = document.createElement('button'); sl.type = 'button'; sl.className = 'pz-slot'; sl.dataset.k = r * cols + c;
      sl.setAttribute('aria-label', 'Spot ' + (r + 1) + ', ' + (c + 1));
      sl.style.left = c * pw + 'px'; sl.style.top = r * ph + 'px'; sl.style.width = pw + 'px'; sl.style.height = ph + 'px';
      sl.addEventListener('click', function () { if (sel) tryPlace(sel, +this.dataset.k); });
      board.appendChild(sl); slots.push(sl);
    }
    var order = []; for (var k = 0; k < total; k++) order.push(k);
    for (var i = order.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = order[i]; order[i] = order[j]; order[j] = t; }
    if (order.every(function (v, i2) { return v === i2; })) order.reverse();
    var ts = Math.min(pw * 0.85, 96, (Math.min(window.innerWidth - 32, 560) - 30) / Math.min(total, 5)), tsh = ts * ph / pw;
    order.forEach(function (k, n) {
      var c2 = k % cols, r2 = Math.floor(k / cols), b = document.createElement('button');
      b.type = 'button'; b.className = 'pz-piece'; b.dataset.k = k; b.setAttribute('aria-label', 'Piece ' + (n + 1));
      b.style.width = ts + 'px'; b.style.height = tsh + 'px';
      b.appendChild(pic(src, [R.x + c2 * tw, R.y + r2 * th, tw, th]));
      tray.appendChild(b); drag(b);
    });
    tray.style.minHeight = tray.offsetHeight + 'px';
    function tryPlace(b, slot) {
      var k = +b.dataset.k;
      if (slot !== k) { b.classList.remove('drag', 'sel'); b.style.left = b.style.top = ''; b.classList.add('shake'); setTimeout(function () { b.classList.remove('shake'); }, 400); sel = null; hint(-1);
        if (b.wrongs = (b.wrongs || 0) + 1, b.wrongs >= 2) hint(k); return; }
      var c3 = k % cols, r3 = Math.floor(k / cols), p = document.createElement('div'); p.className = 'pz-placed';
      p.style.left = c3 * pw + 'px'; p.style.top = r3 * ph + 'px'; p.style.width = pw + 'px'; p.style.height = ph + 'px';
      p.appendChild(pic(src, [R.x + c3 * tw, R.y + r3 * th, tw, th])); board.appendChild(p);
      slots[k].remove(); b.remove(); sel = null; hint(-1); placed++;
      cheer.textContent = placed < total ? ['Nice!', 'Yes!', 'Good one!', 'Keep going!'][placed % 4] : '';
      if (placed === total) { if (help) help.hidden = true; finish(true); }
    }
    function hint(k) { slots.forEach(function (s) { s.classList.toggle('hint', +s.dataset.k === k); }); }
    function drag(b) {
      var sx, sy, moved, ox, oy;
      b.addEventListener('pointerdown', function (e) {
        e.preventDefault(); sx = e.clientX; sy = e.clientY; moved = false;
        var r0 = b.getBoundingClientRect(); ox = e.clientX - r0.left; oy = e.clientY - r0.top;
        b.setPointerCapture(e.pointerId);
      });
      b.addEventListener('pointermove', function (e) {
        if (sx == null) return;
        if (!moved && Math.hypot(e.clientX - sx, e.clientY - sy) < 6) return;
        if (!moved && !b._ph) { b._ph = document.createElement('span'); b._ph.style.cssText = 'flex:0 0 auto;visibility:hidden;width:' + ts + 'px;height:' + tsh + 'px'; b.parentNode.insertBefore(b._ph, b); }
        moved = true; b.classList.add('drag'); b.style.width = pw + 'px'; b.style.height = ph + 'px';
        b.style.left = (e.clientX - ox * pw / ts) + 'px'; b.style.top = (e.clientY - oy * ph / tsh) + 'px';
      });
      b.addEventListener('pointerup', function (e) {
        if (sx == null) return; sx = null;
        if (!moved) { // a tap: select it, then tap a spot
          tray.querySelectorAll('.sel').forEach(function (x) { x.classList.remove('sel'); });
          sel = b; b.classList.add('sel'); return;
        }
        var br = board.getBoundingClientRect(), r1 = b.getBoundingClientRect(), cx = r1.left + r1.width / 2 - br.left, cy = r1.top + r1.height / 2 - br.top;
        if (b._ph) { b._ph.remove(); b._ph = null; }
        b.style.width = ts + 'px'; b.style.height = tsh + 'px';
        if (cx < 0 || cy < 0 || cx > bw || cy > bh) { b.classList.remove('drag'); b.style.left = b.style.top = ''; return; }
        tryPlace(b, Math.floor(cy / ph) * cols + Math.floor(cx / pw));
      });
      b.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tray.querySelectorAll('.sel').forEach(function (x) { x.classList.remove('sel'); }); sel = b; b.classList.add('sel'); slots[0] && slots[0].focus(); } });
    }
    function finish(solved) {
      if (solved) { board.classList.add('done'); cheer.textContent = 'You built it!'; if (window.CQCelebrate) CQCelebrate('Congratulations!', 'You built it, piece by piece!'); }
      if (solved && window.parent !== window) window.parent.postMessage({ cq: 'solved' }, '*'); // counts towards the puzzle badges
      setTimeout(function () {
        ov.style.transition = 'opacity .35s'; ov.style.opacity = 0;
        setTimeout(function () { ov.remove(); window.removeEventListener('message', onMsg); parts.forEach(function (el) { el.style.visibility = ''; }); done(solved); }, 350);
      }, solved ? 2600 : 0);
    }
    ov.querySelector('.pz-skip').addEventListener('click', function () { finish(false); });
    // spend 10 embers to place one piece (only inside the app, which holds the embers)
    var help = ov.querySelector('.pz-help'), COST = 10, embers = 0, waiting = null;
    function onMsg(e) {
      if (e.source !== window.parent || !e.data) return;
      if (e.data.cq === 'embers' || e.data.cq === 'spent') { embers = e.data.n; help.hidden = false; help.disabled = embers < COST || placed >= total; help.title = 'You have ' + embers + ' embers'; }
      if (e.data.cq === 'spent' && e.data.id === waiting) {
        waiting = null;
        if (!e.data.ok) { cheer.textContent = 'Not enough embers yet. Finish lessons to earn more!'; return; }
        var left = [].slice.call(tray.querySelectorAll('.pz-piece')); if (!left.length) return;
        var pc = left[Math.floor(Math.random() * left.length)]; tryPlace(pc, +pc.dataset.k); cheer.textContent = '✨ Placed for ' + COST + ' embers!';
      }
    }
    if (window.parent !== window) {
      window.addEventListener('message', onMsg);
      window.parent.postMessage({ cq: 'embers?' }, '*');
      help.addEventListener('click', function () { if (waiting || placed >= total) return; waiting = 'p' + Date.now(); help.disabled = true; window.parent.postMessage({ cq: 'spend', n: COST, id: waiting }, '*'); });
    }
    ov.querySelector('.pz-back').addEventListener('click', function () { finish(false); if (window.parent !== window) window.parent.postMessage({ cq: 'home' }, '*'); });
    if (window.parent === window) ov.querySelector('.pz-back').hidden = true;
  }
  window.CQPuzzle = { start: start };
})();

// The robot teacher's name is the learner's choice (cq-profile.teacher, 'Nibb' by default).
// Every bit of text that says Nibb (labels, captions, buttons, aria-labels) shows the chosen name instead.
// CQSetTeacher(name) changes it live; text already showing an earlier chosen name is updated too.
(function () {
  var name = 'Nibb', old = ['Nibb'], RX = null, ATTRS = ['aria-label', 'title', 'placeholder', 'alt'], observer = null;
  function clean(t) { return String(t || '').replace(/[\u0000-\u001f<>&"\\]/g, '').trim().slice(0, 14); }
  try { var p = JSON.parse(localStorage.getItem('cq-profile') || 'null'); if (p && clean(p.teacher)) name = clean(p.teacher); } catch (e) {}
  function esc(t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function build() { var olds = old.filter(function (o) { return o !== name; }); RX = olds.length ? new RegExp('\\b(' + olds.map(esc).join('|') + ')\\b', 'g') : null; }
  function has(v) { if (!RX || !v) return false; RX.lastIndex = 0; return RX.test(v); }
  function fixText(n) { if (has(n.nodeValue)) { RX.lastIndex = 0; n.nodeValue = n.nodeValue.replace(RX, name); } }
  function fixEl(el) { ATTRS.forEach(function (a) { var v = el.getAttribute && el.getAttribute(a); if (has(v)) { RX.lastIndex = 0; el.setAttribute(a, v.replace(RX, name)); } }); }
  function fix(root) {
    if (!root || !RX) return;
    if (root.nodeType === 3) { fixText(root); return; }
    if (root.nodeType !== 1) return;
    if (/^(SCRIPT|STYLE)$/.test(root.tagName)) return;
    fixEl(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), t;
    while ((t = w.nextNode())) { var pt = t.parentNode; if (pt && /^(SCRIPT|STYLE)$/.test(pt.tagName)) continue; fixText(t); }
    root.querySelectorAll('[aria-label],[title],[placeholder],[alt]').forEach(fixEl);
  }
  function apply() {
    build(); if (!RX || !document.body) return;
    if (has(document.title)) { RX.lastIndex = 0; document.title = document.title.replace(RX, name); }
    fix(document.body);
    if (!observer) {
      observer = new MutationObserver(function (ms) { ms.forEach(function (m) {
        if (m.type === 'characterData') fixText(m.target); else if (m.type === 'attributes') fixEl(m.target); else m.addedNodes.forEach(fix);
      }); });
      observer.observe(document.body, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ATTRS });
    }
  }
  window.CQ_TEACHER = name;
  window.CQSetTeacher = function (n) { n = clean(n) || 'Nibb'; if (old.indexOf(name) < 0) old.push(name); name = n; window.CQ_TEACHER = n; apply(); };
  if (document.body) apply(); else document.addEventListener('DOMContentLoaded', apply);
})();

// Congratulations: firework blasts, falling confetti and a big banner, over everything for a moment.
// CQCelebrate(title, sub, big) — big = a longer show with more fireworks (a whole street or floor finished).
(function () {
  var COLORS = ['#FFB547', '#FF7A6B', '#7CF5C8', '#9FE3FF', '#C3A6FF', '#FF8FC7', '#FFE07A', '#FFFFFF'];
  function css() {
    if (document.getElementById('cqCelCss')) return;
    var st = document.createElement('style'); st.id = 'cqCelCss';
    st.textContent = '.cq-cel{position:fixed;inset:0;z-index:100;pointer-events:none}' +
      '.cq-cel canvas{position:absolute;inset:0;width:100%;height:100%}' +
      '.cq-cel .ban{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%) scale(.3);opacity:0;text-align:center;padding:18px 26px;border-radius:26px;background:linear-gradient(160deg,#FFC861,#FF7A6B);color:#2A1330;box-shadow:0 18px 40px rgba(0,0,0,.45);animation:cqBan 2.6s cubic-bezier(.3,1.5,.5,1) forwards;max-width:calc(100% - 40px)}' +
      '.cq-cel.big .ban{animation-duration:3.6s}' +
      '.cq-cel .ban b{display:block;font-size:clamp(26px,7vw,40px);line-height:1.1}' +
      '.cq-cel .ban span{display:block;margin-top:4px;font-weight:800;font-size:15px}' +
      '@keyframes cqBan{0%{opacity:0;transform:translate(-50%,-50%) scale(.3) rotate(-8deg)}12%{opacity:1;transform:translate(-50%,-50%) scale(1.08) rotate(2deg)}20%{transform:translate(-50%,-50%) scale(1) rotate(0)}85%{opacity:1;transform:translate(-50%,-50%) scale(1)}100%{opacity:0;transform:translate(-50%,-60%) scale(.9)}}' +
      '@media (prefers-reduced-motion:reduce){.cq-cel canvas{display:none}.cq-cel .ban{animation:none;opacity:1;transform:translate(-50%,-50%)}}';
    document.head.appendChild(st);
  }
  window.CQCelebrate = function (title, sub, big) {
    css();
    var still = (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) || document.body.classList.contains('calm');
    var root = document.createElement('div'); root.className = 'cq-cel' + (big ? ' big' : ''); root.setAttribute('role', 'status');
    var cv = document.createElement('canvas'), ban = document.createElement('div'); ban.className = 'ban';
    var bt = document.createElement('b'); bt.textContent = title || 'Congratulations!'; ban.appendChild(bt);
    // the app's chunky display font when there is one, else a heavy system font
    var df = getComputedStyle(document.documentElement).getPropertyValue('--font-display').trim();
    bt.style.fontFamily = df || 'system-ui, -apple-system, "Segoe UI", sans-serif'; bt.style.fontWeight = df ? '400' : '900';
    if (sub) { var bs = document.createElement('span'); bs.textContent = sub; ban.appendChild(bs); }
    root.appendChild(cv); root.appendChild(ban); document.body.appendChild(root);
    var life = big ? 3800 : 2800;
    if (window.CQCheer) window.CQCheer(); // the fanfare and the firecrackers
    setTimeout(function () { root.remove(); }, life);
    if (still) return;
    var dpr = window.devicePixelRatio || 1, W = innerWidth, H = innerHeight, ctx = cv.getContext('2d');
    cv.width = W * dpr; cv.height = H * dpr; ctx.scale(dpr, dpr);
    var parts = [], t0 = performance.now(), last = t0;
    // a firework: a ring of sparks that fly out, slow down and fall
    function blast(x, y) {
      var n = 46 + Math.floor(Math.random() * 20), col = COLORS[Math.floor(Math.random() * COLORS.length)], col2 = COLORS[Math.floor(Math.random() * COLORS.length)];
      for (var i = 0; i < n; i++) { var a = i / n * Math.PI * 2 + Math.random() * 0.2, sp = 160 + Math.random() * 260;
        parts.push({ k: 'spark', x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: 1.1 + Math.random() * 0.5, age: 0, c: i % 3 ? col : col2, r: 2 + Math.random() * 1.8 }); }
      parts.push({ k: 'flash', x: x, y: y, age: 0, life: 0.35 });
    }
    // confetti: little paper strips that tumble down
    for (var i = 0; i < (big ? 170 : 110); i++) parts.push({ k: 'conf', x: Math.random() * W, y: -20 - Math.random() * H * 0.6, vx: (Math.random() - 0.5) * 80, vy: 90 + Math.random() * 160, rot: Math.random() * 6, vr: (Math.random() - 0.5) * 10, w: 6 + Math.random() * 6, h: 10 + Math.random() * 8, c: COLORS[Math.floor(Math.random() * COLORS.length)], age: 0, life: 9 });
    var shots = big ? [0, 250, 520, 800, 1100, 1450, 1800, 2200] : [0, 300, 650, 1000];
    shots.forEach(function (d) { setTimeout(function () { blast(W * (0.18 + Math.random() * 0.64), H * (0.14 + Math.random() * 0.36)); if (window.CQBoom) window.CQBoom(); }, d); });
    (function frame(now) {
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      ctx.clearRect(0, 0, W, H);
      for (var i = parts.length - 1; i >= 0; i--) {
        var p = parts[i]; p.age += dt; if (p.age > p.life) { parts.splice(i, 1); continue; }
        if (p.k === 'flash') { var g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 90); g.addColorStop(0, 'rgba(255,255,230,' + (0.8 * (1 - p.age / p.life)) + ')'); g.addColorStop(1, 'rgba(255,255,230,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, 90, 0, 6.3); ctx.fill(); continue; }
        if (p.k === 'spark') { p.vx *= 0.96; p.vy = p.vy * 0.96 + 260 * dt; p.x += p.vx * dt; p.y += p.vy * dt;
          ctx.globalAlpha = Math.max(0, 1 - p.age / p.life); ctx.fillStyle = p.c; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.3); ctx.fill();
          ctx.globalAlpha *= 0.4; ctx.beginPath(); ctx.arc(p.x - p.vx * 0.03, p.y - p.vy * 0.03, p.r * 0.8, 0, 6.3); ctx.fill(); ctx.globalAlpha = 1; continue; }
        p.x += p.vx * dt + Math.sin(now / 300 + p.rot) * 0.6; p.y += p.vy * dt; p.rot += p.vr * dt;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.scale(1, Math.cos(now / 160 + p.rot)); ctx.fillStyle = p.c; ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h); ctx.restore();
      }
      if (now - t0 < life && root.isConnected) requestAnimationFrame(frame);
    })(t0);
  };
})();

// in the house / town frame, the app plays the firework sounds (it holds the sound switch)
if (window.parent !== window) { window.CQBoom = function () { window.parent.postMessage({ cq: 'fire' }, '*'); }; window.CQCheer = function () { window.parent.postMessage({ cq: 'cheer' }, '*'); }; }
