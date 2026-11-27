const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch();
  for (const d of ['iPhone 13', 'iPhone SE']) { const ctx = await b.newContext({ ...devices[d], deviceScaleFactor: 1 });
    await ctx.addInitScript(() => { localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 3, embers: 120, streak: 4, day: '' })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 9, teacher: 'Sparky', toured: true, courses: ['py'] })); });
    const p = await ctx.newPage(); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(700);
    const r = await p.evaluate(() => { const vw = window.innerWidth; return [...document.querySelectorAll('#home .topbar .chip, #home .topbar .brand')].map(e => { const x = e.getBoundingClientRect(); return Math.round(x.left) + '-' + Math.round(x.right); }).join(' ') + ' | vw ' + vw; });
    console.log(d, r); await p.screenshot({ path: 'iso/top-' + d.replace(' ', '') + '.png', clip: { x: 0, y: 0, width: 390, height: 80 } }); await ctx.close(); }
  await b.close(); })();
