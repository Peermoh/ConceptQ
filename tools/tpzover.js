// The puzzle on a tall iPhone: the tray never overlaps the message or the buttons; the backdrop hides the town.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const dev of ['iPhone 14 Pro Max', 'iPhone SE']) {
    const ctx = await b.newContext({ ...devices[dev], deviceScaleFactor: 1 });
    await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 200, streak: 1, day: '' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 1, english: 0 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Test', age: 9, teacher: 'Sparky', toured: true, courses: ['maths'], antics: false })); } });
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(600);
    await p.click('#home [data-nav="house"]'); await p.waitForTimeout(400);
    await p.evaluate(() => { document.getElementById('houseFrame').src = 'world.html?course=maths&v=1&build=0'; }); await p.waitForTimeout(1500);
    const f = p.frames().find(x => /world/.test(x.url())); await f.waitForSelector('.pz-help:not([hidden])');
    const n = await f.$$eval('.pz-piece', e => e.length);
    for (let i = 0; i < n - 2; i++) { await f.click('.pz-help'); await p.waitForTimeout(350); }
    const r = await f.evaluate(() => { const R = e => e.getBoundingClientRect(), pcs = [...document.querySelectorAll('.pz-piece')].map(R), ch = R(document.querySelector('.pz-cheer')), hp = R(document.querySelector('.pz-help')), bd = R(document.querySelector('.pz-board'));
      const hit = (a, c) => a.left < c.right && a.right > c.left && a.top < c.bottom && a.bottom > c.top;
      return { left: pcs.length, overCheer: pcs.some(q => hit(q, ch)), overHelp: pcs.some(q => hit(q, hp)), overBoard: pcs.some(q => hit(q, bd)), cheer: document.querySelector('.pz-cheer').textContent, bg: getComputedStyle(document.querySelector('.pz')).backgroundColor }; });
    console.log(dev, JSON.stringify(r));
    await p.screenshot({ path: 'iso/PO-' + dev.replace(/ /g, '') + '.png' });
    await ctx.close();
  }
  console.log('errors', errs); await b.close();
})();
