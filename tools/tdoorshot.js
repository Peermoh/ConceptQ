const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 3, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 13, teacher: 'Robo', toured: true, courses: ['py'], antics: false })); });
  const p = await ctx.newPage(); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(900);
  await p.evaluate(() => window.__show('doors'));
  for (const t of [700, 1700, 2900]) { await p.waitForTimeout(t === 700 ? 700 : t === 1700 ? 1000 : 1200); await p.screenshot({ path: 'iso/D-' + t + '.png', clip: { x: 0, y: 60, width: 390, height: 300 } }); }
  await b.close(); })();
