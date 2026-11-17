const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 3, embers: 20000, streak: 1, day: '' })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 9, toured: true, courses: ['maths'], antics: false })); } });
  const p = await ctx.newPage(); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(700);
  await p.click('#prizeTile'); await p.waitForTimeout(300);
  const wins = [], ends = [];
  for (let i = 0; i < 12; i++) {
    await p.click("#wheelSpin"); await p.waitForTimeout(5300);
    wins.push(await p.textContent('#wheelPrize'));
    ends.push(await p.evaluate(() => { const m = getComputedStyle(document.getElementById('wheelG')).transform; const v = m.match(/matrix\(([^)]+)\)/)[1].split(',').map(Number); return Math.round(Math.atan2(v[1], v[0]) * 180 / Math.PI); }));
  }
  const c = {}; wins.forEach(w => c[w] = (c[w] || 0) + 1);
  console.log('prizes won:', JSON.stringify(c)); console.log('stop angles:', ends.join(' '));
  await b.close(); })();
