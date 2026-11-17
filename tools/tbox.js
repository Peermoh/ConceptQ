const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch();
  for (const dev of ['iPhone 13', null]) {
    const ctx = await b.newContext(dev ? { ...devices[dev] } : { viewport: { width: 1366, height: 800 } });
    await ctx.addInitScript(() => { localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 3, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 13, toured: true, courses: ['py'], antics: false })); });
    const p = await ctx.newPage(); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(900);
    console.log(dev || 'desktop', await p.evaluate(() => { const R = e => { const r = document.querySelector(e).getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)].join(','); };
      return 'hero ' + R('#homeHero') + ' | lumi ' + R('#homeLumi') + ' | topbar ' + R('#home .topbar') + ' | course ' + R('#courseTabs') + ' | bubble ' + R('#homeBubble'); }));
    await ctx.close(); }
  await b.close(); })();
