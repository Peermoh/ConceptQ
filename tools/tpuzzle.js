// Puzzle after a lesson (house and town), and the prize editor.
const { chromium, devices } = require('playwright');
async function solve(fr, p, tag) {
  await fr.waitForSelector('.pz', { timeout: 8000 });
  const n = await fr.$$eval('.pz-piece', e => e.length);
  await p.screenshot({ path: 'iso/P-' + tag + '-start.png' });
  for (let i = 0; i < n; i++) { // drag every piece onto its own spot
    const pc = (await fr.$$('.pz-piece'))[0], k = await pc.getAttribute('data-k');
    const slot = await fr.$('.pz-slot[data-k="' + k + '"]'), a = await pc.boundingBox(), b = await slot.boundingBox();
    await p.mouse.move(a.x + a.width / 2, a.y + a.height / 2); await p.mouse.down();
    await p.mouse.move(a.x + 20, a.y + 20, { steps: 3 });
    await p.mouse.move(b.x + b.width / 2, b.y + b.height / 2, { steps: 8 }); await p.mouse.up(); await p.waitForTimeout(150);
    if (i === 1) await p.screenshot({ path: 'iso/P-' + tag + '-mid.png' });
  }
  const left = await fr.$$eval('.pz-piece', e => e.length), cheer = await fr.textContent('.pz-cheer');
  await p.screenshot({ path: 'iso/P-' + tag + '-solved.png' });
  await p.waitForTimeout(1800);
  console.log(tag, '| pieces', n, '| left', left, '|', cheer, '| overlay gone:', !(await fr.$('.pz')));
}
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const [age, dev] of [[7, 'iPhone 13'], [13, null]]) {
    const ctx = await b.newContext(dev ? { ...devices[dev], deviceScaleFactor: 1 } : { viewport: { width: 1366, height: 800 } });
    await ctx.addInitScript(a => { localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: a })); var v = /[?&]v=(\d+)/.exec(location.search); if (v && /house/.test(location.pathname)) localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: +v[1], embers: 0, streak: 1, day: '' })); }, age);
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.goto('http://localhost:8765/house.html?v=7&build=6'); await p.waitForTimeout(800);
    await solve(p.mainFrame(), p, 'house-age' + age);
    console.log('  house bubble:', await p.textContent('#houseBubble'));
    await p.goto('http://localhost:8765/house.html?v=13&build=12'); await p.waitForTimeout(800);
    await solve(p.mainFrame(), p, 'house12-age' + age);
    await p.goto('http://localhost:8765/world.html?course=maths&v=7&build=6'); await p.waitForTimeout(800);
    await solve(p.mainFrame(), p, 'town-age' + age);
    console.log('  toast:', await p.textContent('#toast'));
    await p.goto('http://localhost:8765/world.html?course=english&v=3&build=2'); await p.waitForTimeout(800);
    await p.waitForSelector('.pz-skip', { timeout: 8000 }); await p.click('.pz-skip'); await p.waitForTimeout(1500); console.log('  skip → toast:', await p.textContent('#toast'));
    await ctx.close();
  }
  // the prize editor, opened from the wheel
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 8 })); } });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(700);
  await p.click('#prizeTile'); await p.waitForTimeout(300); await p.click('#wheelEdit'); await p.waitForTimeout(500);
  const q = await p.textContent('#gateQ'), m = q.match(/(\d+) × (\d+)/); await p.fill('#gateIn', String(m[1] * m[2])); await p.click('#gateOk'); await p.waitForTimeout(500);
  console.log('editor rows:', await p.$$eval('#prizeRows li', e => e.length));
  await p.click('#prizeRows li:nth-child(1) .pe-del'); await p.click('#prizeIdeas button:nth-child(1)');
  await p.click('#prizeAdd'); await p.keyboard.type('Swim at the pool'); await p.click('#prizeRows li:last-child .pe-emo');
  await p.screenshot({ path: 'iso/P-prizes.png', fullPage: true });
  await p.click('#prizeSave'); await p.waitForTimeout(300);
  console.log('saved:', await p.evaluate(() => localStorage.getItem('cq-rewards')), '|', await p.textContent('#prizeHint'));
  await p.click('#me [data-nav="home"]'); await p.waitForTimeout(300); await p.click('#prizeTile'); await p.waitForTimeout(300);
  await p.screenshot({ path: 'iso/P-wheel.png' });
  console.log('errors', errs); await b.close();
})();
