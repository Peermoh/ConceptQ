// Build-it-yourself puzzle, shared by house.html and world.html.
// After a lesson, the new part of the house / town is cut into square pieces of the scene around it;
// the learner drags (or taps) each piece into its place, and then the page plays its normal build moment.
//   CQPuzzle.start({ svg: rootSvg, parts: [elements], title: 'Build the fruit stall!', onDone: fn })
// Pieces: 4 for age 8 and under, 6 up to 11, 9 from 12 (age from the app's cq-profile).
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
      '.pz-skip{background:none;border:0;color:#FFF6EC;opacity:.7;font:inherit;font-weight:800;font-size:14px;text-decoration:underline;cursor:pointer;padding:8px}' +
      '.pz-cheer{font-size:26px;font-weight:900;color:#7CF5C8;min-height:34px;text-align:center}' +
      '@media (prefers-reduced-motion:reduce){.pz,.pz-placed,.pz-piece.shake{animation:none}}';
    document.head.appendChild(st);
  }
  function grid() {
    var age = 9; try { var p = JSON.parse(localStorage.getItem('cq-profile') || 'null'); if (p && typeof p.age === 'number') age = p.age; } catch (e) {}
    return age <= 8 ? [2, 2] : age <= 11 ? [3, 2] : [3, 3];
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
    ov.innerHTML = '<button class="pz-back" type="button" aria-label="Back to lessons">'+'\u2190'+'</button><h2></h2><p>Drag each piece into its place. You can also tap a piece, then tap its spot.</p><div class="pz-main"><div class="pz-board"></div><div class="pz-tray"></div></div><div class="pz-cheer" aria-live="polite"></div><button class="pz-skip" type="button">Let Nibb build it</button>';
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
    function tryPlace(b, slot) {
      var k = +b.dataset.k;
      if (slot !== k) { b.classList.remove('drag', 'sel'); b.style.left = b.style.top = ''; b.classList.add('shake'); setTimeout(function () { b.classList.remove('shake'); }, 400); sel = null; hint(-1);
        if (b.wrongs = (b.wrongs || 0) + 1, b.wrongs >= 2) hint(k); return; }
      var c3 = k % cols, r3 = Math.floor(k / cols), p = document.createElement('div'); p.className = 'pz-placed';
      p.style.left = c3 * pw + 'px'; p.style.top = r3 * ph + 'px'; p.style.width = pw + 'px'; p.style.height = ph + 'px';
      p.appendChild(pic(src, [R.x + c3 * tw, R.y + r3 * th, tw, th])); board.appendChild(p);
      slots[k].remove(); b.remove(); sel = null; hint(-1); placed++;
      cheer.textContent = placed < total ? ['Nice!', 'Yes!', 'Good one!', 'Keep going!'][placed % 4] : '';
      if (placed === total) finish(true);
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
        b.style.width = ts + 'px'; b.style.height = tsh + 'px';
        if (cx < 0 || cy < 0 || cx > bw || cy > bh) { b.classList.remove('drag'); b.style.left = b.style.top = ''; return; }
        tryPlace(b, Math.floor(cy / ph) * cols + Math.floor(cx / pw));
      });
      b.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tray.querySelectorAll('.sel').forEach(function (x) { x.classList.remove('sel'); }); sel = b; b.classList.add('sel'); slots[0] && slots[0].focus(); } });
    }
    function finish(solved) {
      if (solved) { board.classList.add('done'); cheer.textContent = 'You built it!'; }
      setTimeout(function () {
        ov.style.transition = 'opacity .35s'; ov.style.opacity = 0;
        setTimeout(function () { ov.remove(); parts.forEach(function (el) { el.style.visibility = ''; }); done(solved); }, 350);
      }, solved ? 1100 : 0);
    }
    ov.querySelector('.pz-skip').addEventListener('click', function () { finish(false); });
    ov.querySelector('.pz-back').addEventListener('click', function () { finish(false); if (window.parent !== window) window.parent.postMessage({ cq: 'home' }, '*'); });
    if (window.parent === window) ov.querySelector('.pz-back').hidden = true;
  }
  window.CQPuzzle = { start: start };
})();
