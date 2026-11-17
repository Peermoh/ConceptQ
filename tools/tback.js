// The back buttons: on the puzzle, in Number Town and in the house all return to the Learn tab.
const { chromium, devices } = require('playwright');
const pickCourse = async (p, name) => { const sw = await p.$('#courseTabs .cn-sw'); if (!sw) return; await sw.click(); await p.waitForTimeout(150); const it = await p.$('#courseTabs .cn-menu button:has-text("' + name + '")'); if (it) await it.click(); else await p.click('body'); };
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 7, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 3, english: 0 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 9, courses: ['py', 'maths'] })); } });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  const vis = async () => (await p.evaluate(() => ['home', 'house'].filter(id => !document.getElementById(id).hidden).join()));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(500);
  // 1. puzzle back arrow, right after a lesson (simulate the done button)
  await p.click('#home [data-nav="house"]'); await p.waitForTimeout(500); await p.evaluate(() => { document.getElementById('houseFrame').src = 'world.html?course=maths&v=3&build=2'; }); await p.waitForTimeout(1500);
  let f = p.frames().find(x => /world/.test(x.url())); console.log('frame:', f && f.url().split('/').pop());
  await f.waitForSelector('.pz-back'); await f.click('.pz-back'); await p.waitForTimeout(800); console.log('after puzzle back →', await vis());
  // 2. town back chip
  await p.click('#home [data-nav="house"]'); await p.waitForTimeout(1200); f = p.frames().find(x => /world/.test(x.url()));
  console.log('town back visible:', await f.isVisible('#back')); await f.click('#back'); await p.waitForTimeout(500); console.log('after town back →', await vis());
  // 3. house Lessons chip
  await pickCourse(p, 'Python'); await p.waitForTimeout(300); await p.click('#home [data-nav="house"]'); await p.waitForTimeout(1500);
  f = p.frames().find(x => /house\.html/.test(x.url())); console.log('house lessons visible:', await f.isVisible('#lessonsBtn'));
  await p.screenshot({ path: 'iso/back-house.png' }); await f.click('#lessonsBtn'); await p.waitForTimeout(500); console.log('after house back →', await vis());
  console.log('errors', errs); await b.close();
})();
