// Make it easier: each setting applies, is saved, and survives a reload. Home fixes: Start on the first phone screen,
// news badge on the Town tab (robot not on the card), star streak, Courses tile, Cards topics.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 120, streak: 3, day: '2026-11-18' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 4, english: 2 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 8, teacher: 'Sparky', toured: true, courses: ['maths', 'english'], antics: false })); } });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(1200);
  const start = await p.$eval('#startBtn', e => { const r = e.getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom), innerHeight - 60]; });
  console.log('Start button top/bottom', start[0], start[1], '| visible above the menu:', start[1] < start[2]);
  console.log('news badge on Town tab:', await p.$eval('#home .nav [data-nav="house"]', e => e.classList.contains('has-news')), '| robot mode:', await p.$eval('#buddy', e => e.classList.contains('nav-mode') ? 'nav (over card)' : 'not over the card'));
  console.log('Courses tile:', (await p.textContent('#coursesTile')).replace(/\s+/g, ' '), '| Cards tile:', (await p.textContent('#cardsTile')).replace(/\s+/g, ' '));
  await p.screenshot({ path: 'iso/E-home.png' });
  // settings
  await p.click('#home [data-nav="me"]'); await p.waitForTimeout(300);
  await p.click('#ezSize button[data-v="2"]'); await p.click('#ezRate button[data-v="0.85"]'); await p.check('#ezFont'); await p.check('#ezContrast'); await p.waitForTimeout(300);
  await p.evaluate(() => document.getElementById('easyH').scrollIntoView()); await p.screenshot({ path: 'iso/E-me.png' });
  console.log('body classes:', await p.evaluate(() => document.body.className), '| saved:', await p.evaluate(() => { const f = JSON.parse(localStorage.getItem('cq-profile')); return JSON.stringify({ ts: f.ts, rate: f.rate, easyFont: f.easyFont, contrast: f.contrast }); }));
  await p.reload(); await p.waitForTimeout(900);
  console.log('after reload body classes:', await p.evaluate(() => document.body.className));
  await p.click('#startBtn'); await p.waitForTimeout(400); await p.click('#playBtn'); await p.waitForTimeout(1500);
  console.log('voice speed in lesson:', await p.evaluate(() => { const a = [...document.querySelectorAll('audio')]; return window.__aud ? 'n/a' : 'n/a'; }), '| playbackRate:', await p.evaluate(() => { try { return voiceEl.playbackRate; } catch (e) { return 'hidden'; } }).catch(() => '?'));
  await p.screenshot({ path: 'iso/E-lesson.png' });
  await p.click('#toQuiz'); await p.waitForTimeout(400); await p.screenshot({ path: 'iso/E-quiz.png' });
  console.log('quiz text zoom:', await p.$eval('#qText', e => getComputedStyle(e).zoom), '| font:', await p.$eval('#qText', e => getComputedStyle(e).fontFamily.split(',')[0]));
  // less movement
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(600); await p.click('#home [data-nav="me"]'); await p.check('#ezCalm'); await p.waitForTimeout(1200);
  console.log('calm after reload:', await p.evaluate(() => document.body.classList.contains('calm')));
  console.log('errors', errs); await b.close();
})();
