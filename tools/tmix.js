// Quiz mix (levels), no repeats over 5 tries, what the read-aloud says, and the puzzle with embers.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  // capture what speech synthesis is asked to say
  await ctx.addInitScript(() => { window.__said = []; const S = window.speechSynthesis; if (S) { S.speak = function (u) { window.__said.push(u.text + (u.voice ? ' [' + u.voice.name + ']' : '') + ' @' + u.rate); }; S.cancel = function () {}; } });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 3, embers: 35, streak: 1, day: '' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 6, english: 4 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 9, toured: true, courses: ['maths', 'english'], antics: false })); } });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(700);
  for (const [lesson, label] of [[0, 'm2_groups']]) {
    const seen = []; let levels = [];
    for (let attempt = 0; attempt < 5; attempt++) {
      await p.evaluate(i => { openLesson(i); }, lesson).catch(() => {});
      await p.evaluate(i => document.querySelectorAll('#topics .topic')[i].click(), lesson); await p.waitForTimeout(300);
      await p.click('#toQuiz'); await p.waitForTimeout(250);
      const qs = [];
      for (let q = 0; q < 5; q++) {
        qs.push((await p.textContent('#qText')).trim()); levels.push(((await p.textContent('#qTag')).match(/(Easy|Medium|Hard)/) || ['', '-'])[1]);
        if (attempt === 0 && q === 0) { await p.click('#qHear'); await p.waitForTimeout(200); }
        await p.click('#opt-' + q + '-0'); await p.waitForTimeout(60); await p.click('#sheetBtn'); await p.waitForTimeout(80);
      }
      seen.push(qs);
      await p.click('[data-nav="home"]').catch(() => {}); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(500);
    }
    // a question 'repeats' if its exact text came up in any of the 4 tries before
    let rep = 0, total = 0; seen.forEach((qs, i) => qs.forEach(t => { total++; if (seen.slice(Math.max(0, i - 4), i).some(prev => prev.includes(t))) rep++; }));
    const lv = {}; levels.forEach(l => lv[l] = (lv[l] || 0) + 1);
    console.log(label, '| 5 tries, 25 questions | repeats within the last 4 tries:', rep, '| levels:', JSON.stringify(lv));
    console.log('   try 1:', seen[0].join(' / ').slice(0, 220));
    console.log('   try 2:', seen[1].join(' / ').slice(0, 220));
  }
  console.log('read aloud:', (await p.evaluate(() => window.__said)).slice(0, 5).join(' | '));
  // puzzle in Number Town: pieces for a 9-year-old, and placing one with embers
  await p.click('#home [data-nav="house"]'); await p.waitForTimeout(400);
  await p.evaluate(() => { document.getElementById('houseFrame').src = 'world.html?course=maths&v=6&build=5'; }); await p.waitForTimeout(1500);
  const f = p.frames().find(x => /world/.test(x.url())); await f.waitForSelector('.pz-help:not([hidden])', { timeout: 5000 });
  const n0 = await f.$$eval('.pz-piece', e => e.length);
  console.log('puzzle pieces:', n0, '| help button:', await f.textContent('.pz-help'), '| enabled:', !(await f.isDisabled('.pz-help')));
  await f.click('.pz-help'); await p.waitForTimeout(500);
  console.log('after 1 help: pieces left', await f.$$eval('.pz-piece', e => e.length), '|', await f.textContent('.pz-cheer'), '| embers now', await p.evaluate(() => JSON.parse(localStorage.getItem('cq-progress')).embers));
  await f.click('.pz-help'); await p.waitForTimeout(500); await f.click('.pz-help').catch(() => {}); await p.waitForTimeout(500);
  console.log('after 3 tries (35 embers): pieces left', await f.$$eval('.pz-piece', e => e.length), '| help enabled:', !(await f.isDisabled('.pz-help')), '| embers', await p.evaluate(() => JSON.parse(localStorage.getItem('cq-progress')).embers));
  await p.screenshot({ path: 'iso/PZ-help.png' });
  console.log('errors', errs); await b.close();
})();
