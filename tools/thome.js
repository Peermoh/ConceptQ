// Full-page screenshots of Home (phone and desktop) for a design review.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [tag, opts] of [['phone', { ...devices['iPhone 13'], deviceScaleFactor: 1 }], ['desk', { viewport: { width: 1366, height: 800 }, deviceScaleFactor: 1 }]]) {
    const ctx = await b.newContext(opts);
    await ctx.addInitScript(() => { localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 120, streak: 3, day: '2026-11-18' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 4, english: 2 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 8, teacher: 'Sparky', toured: true, courses: ['maths', 'english'], antics: false })); });
    const p = await ctx.newPage(); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(1200);
    const h = await p.evaluate(() => document.getElementById('homeScroll').scrollHeight);
    await p.screenshot({ path: 'iso/H-' + tag + '-1.png' });
    await p.evaluate(() => { const s = document.getElementById('homeScroll'); s.scrollTop = s.clientHeight * 0.85; }); await p.waitForTimeout(400);
    await p.screenshot({ path: 'iso/H-' + tag + '-2.png' });
    await p.evaluate(() => { const s = document.getElementById('homeScroll'); s.scrollTop = s.scrollHeight; }); await p.waitForTimeout(400);
    await p.screenshot({ path: 'iso/H-' + tag + '-3.png' });
    console.log(tag, 'home height', h);
    await ctx.close();
  }
  await b.close();
})();
