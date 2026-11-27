// Every 100 ms during each show: does anything that moves overlap the speech bubble, or go below the course banner?
const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const errs = [];
  for (const dev of ['iPhone 13', 'iPhone SE', null]) {
    const ctx = await b.newContext(dev ? { ...devices[dev], deviceScaleFactor: 1 } : { viewport: { width: 1366, height: 800 }, deviceScaleFactor: 1 });
    await ctx.addInitScript(() => { localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 3, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 13, teacher: 'Robo', toured: true, courses: ['py'], antics: false })); });
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(900);
    const res = [];
    for (const name of ['dance', 'bath', 'roam', 'doors', 'rocket', 'dig']) {
      for (let run = 0; run < 3; run++) { // shows are random: try each a few times
        await p.evaluate(() => { document.getElementById('homeScroll').scrollTop = 0; }); await p.waitForTimeout(200);
        if (!(await p.evaluate(n => window.__show(n), name))) { res.push(name + ':not-started'); continue; }
        let hit = 0, below = 0, frames = 0;
        for (let t = 0; t < 46; t++) {
          const r = await p.evaluate(() => { const st = document.querySelector('.antics'); if (!st) return null; const say = st.querySelector('.say'), lim = document.getElementById('courseTabs').getBoundingClientRect().top;
            const sr = say && say.style.opacity !== '0' ? say.getBoundingClientRect() : null; let h = 0, bl = 0;
            // only the part that can be seen: the moving layer is clipped (inset top right bottom left)
            const lay = st.firstElementChild, nums = ((lay.style.clipPath.match(/inset\(([^r)]*)/) || [])[1] || '').trim().split(/\s+/).filter(Boolean).map(parseFloat);
            const m = nums.length ? [nums[0], nums[1] ?? nums[0], nums[2] ?? nums[0], nums[3] ?? (nums[1] ?? nums[0])] : []; // CSS shorthand: 1 to 4 values
            const vis = m.length ? { top: m[0], right: innerWidth - m[1], bottom: innerHeight - m[2], left: m[3] } : { top: 0, left: 0, right: innerWidth, bottom: innerHeight };
            st.querySelectorAll('.actor, .prop').forEach(e => { if (getComputedStyle(e).opacity < 0.15) return; const r0 = e.getBoundingClientRect();
              const q = { left: Math.max(r0.left, vis.left), right: Math.min(r0.right, vis.right), top: Math.max(r0.top, vis.top), bottom: Math.min(r0.bottom, vis.bottom) }; q.width = q.right - q.left; if (q.width <= 0 || q.bottom <= q.top) return;
              if (sr && q.left < sr.right - 2 && q.right > sr.left + 2 && q.top < sr.bottom - 2 && q.bottom > sr.top + 2) h++; if (q.top > lim) bl++; });
            return [h, bl]; });
          if (!r) break; frames++; if (r[0]) hit++; if (r[1]) below++; await p.waitForTimeout(100);
        }
        res.push(name + ':' + hit + '/' + frames + (below ? ' below' + below : ''));
        await p.waitForTimeout(800);
      }
    }
    console.log(dev || 'desktop', '| overlap frames per run:', res.join('  '));
    await ctx.close();
  }
  console.log('errors', errs); await b.close(); })();
