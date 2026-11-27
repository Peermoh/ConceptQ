// Badges: a perfect lesson and a built puzzle award badges with a celebration; the shelf and the tile; old learners
// get earned badges quietly. Plain dark background on Home, the town and the house.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 0, streak: 3, day: new Date().toISOString().slice(0, 10) })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 0, english: 0 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 8, teacher: 'Sparky', toured: true, courses: ['maths'], antics: false })); localStorage.setItem('cq-badges', JSON.stringify({ got: {}, n: {} })); } });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  const banners = []; await p.exposeFunction('__ban', t => banners.push(t));
  await p.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => new MutationObserver(() => { const b = document.querySelector('.cq-cel .ban'); if (b && !b._seen) { b._seen = 1; window.__ban(b.textContent); } }).observe(document.body, { childList: true, subtree: true })); });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(800);
  console.log('tile at start:', (await p.textContent('#badgeTile')).replace(/\s+/g, ' '), '| badges so far:', banners.join(' / ') || 'none');
  // a perfect quiz on lesson 1
  await p.click('#startBtn'); await p.waitForTimeout(300); await p.click('#toQuiz'); await p.waitForTimeout(250);
  for (let q = 0; q < 5; q++) { for (let k = 0; k < 4; k++) { if (!(await p.$('#opt-' + q + '-' + k))) break; const right = await p.evaluate(([qq, kk]) => Q[qq] && Q[qq].answer === kk, [q, k]).catch(() => null); if (right === null) { await p.click('#opt-' + q + '-' + k); if (await p.$('.sheet.is-right')) break; await p.evaluate(qq => window.__undo(qq), q); continue; } if (right) { await p.click('#opt-' + q + '-' + k); break; } } await p.click('#sheetBtn'); await p.waitForTimeout(120); }
  await p.waitForTimeout(8000);
  console.log('after a perfect first lesson, banners:', banners.join(' / '));
  // build its puzzle
  await p.click('#doneHouse'); await p.waitForTimeout(1500);
  const f = p.frames().find(x => /world/.test(x.url())); await f.waitForSelector('.pz');
  const n = await f.$$eval('.pz-piece', e => e.length);
  for (let i = 0; i < n; i++) { const pc = (await f.$$('.pz-piece'))[0], k = await pc.getAttribute('data-k'); await pc.click(); await f.click('.pz-slot[data-k="' + k + '"]'); await p.waitForTimeout(40); }
  await p.waitForTimeout(7000);
  console.log('after building the puzzle, banners:', banners.slice(-2).join(' / '));
  // the shelf
  await p.click('#house [data-nav="home"]').catch(() => p.click('[data-nav="home"]')); await p.waitForTimeout(500);
  console.log('tile now:', (await p.textContent('#badgeTile')).replace(/\s+/g, ' '));
  await p.click('#badgeTile'); await p.waitForTimeout(800);
  console.log('shelf:', await p.textContent('#badgeSum'), '| earned:', await p.$$eval('#badgeGrid .bdg:not(.locked) b', e => e.map(x => x.textContent).join(', ')), '| locked:', await p.$$eval('#badgeGrid .bdg.locked', e => e.length));
  await p.screenshot({ path: 'iso/BG-shelf.png' });
  // plain dark everywhere
  await p.check('#ezDark'); await p.waitForTimeout(300); await p.click('#me [data-nav="home"]'); await p.waitForTimeout(600); await p.screenshot({ path: 'iso/BG-dark-home.png' });
  await p.click('#home [data-nav="house"]'); await p.waitForTimeout(1500); await p.screenshot({ path: 'iso/BG-dark-town.png' });
  // an old learner: badges they already deserve are added quietly
  const c2 = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await c2.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 12, embers: 600, streak: 1, day: '' })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Ravi', age: 13, toured: true, courses: ['py'], antics: false })); } });
  const p2 = await c2.newPage(); p2.on('pageerror', e => errs.push(e.message)); const b2 = []; await p2.exposeFunction('__ban', t => b2.push(t));
  await p2.addInitScript(() => { document.addEventListener('DOMContentLoaded', () => new MutationObserver(() => { const b = document.querySelector('.cq-cel .ban'); if (b && !b._seen) { b._seen = 1; window.__ban(b.textContent); } }).observe(document.body, { childList: true, subtree: true })); });
  await p2.goto('http://localhost:8765/index.html'); await p2.waitForTimeout(2500);
  console.log('old learner: celebrations on load:', b2.length, '| tile:', (await p2.textContent('#badgeTile')).replace(/\s+/g, ' '));
  console.log('errors', errs); await b.close();
})();
