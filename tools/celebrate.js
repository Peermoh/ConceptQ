
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
    var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
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
