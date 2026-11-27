// Replays a 9-piece puzzle (age 7) and logs each drop, to see why the last piece does not snap in.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 7 })); });
  const p = await ctx.newPage(); await p.goto('http://localhost:8765/world.html?course=maths&v=7&build=6'); await p.waitForSelector('.pz');
  const n = await p.$$eval('.pz-piece', e => e.length);
  for (let i = 0; i < n; i++) {
    const pc = (await p.$$('.pz-piece'))[0], k = await pc.getAttribute('data-k'), slot = await p.$('.pz-slot[data-k="' + k + '"]');
    const a = await pc.boundingBox(), s = await slot.boundingBox();
    const ov = await p.evaluate(() => [document.querySelector('.pz').scrollTop, document.querySelector('.pz').scrollHeight, innerHeight]);
    await p.mouse.move(a.x + a.width / 2, a.y + a.height / 2); await p.mouse.down(); await p.mouse.move(a.x + 20, a.y + 20, { steps: 3 });
    await p.mouse.move(s.x + s.width / 2, s.y + s.height / 2, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(150);
    console.log(i, 'k', k, 'piece', Math.round(a.x), Math.round(a.y), Math.round(a.width), 'slot', Math.round(s.x), Math.round(s.y), Math.round(s.width), 'overlay scroll', ov.join('/'), '→ left', await p.$$eval('.pz-piece', e => e.length));
  }
  await b.close();
})();
