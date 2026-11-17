// Maths boards: no broken characters while writing, upright font, lines appear while the voice talks;
// the melody on Home, and the fanfare + crackers on a celebration.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { const C = window.AudioContext; window.__osc = 0; window.__noise = 0; window.AudioContext = function () { const c = new C(); const o = c.createOscillator.bind(c), n = c.createBufferSource.bind(c); c.createOscillator = function () { window.__osc++; return o(); }; c.createBufferSource = function () { window.__noise++; return n(); }; return c; }; });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 11, english: 0 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 8, toured: true, courses: ['maths'], antics: false })); } });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(600);
  await p.mouse.click(5, 300); await p.waitForTimeout(6000); // first tap starts sound; listen to Home for a while
  console.log('Home sounds in 6 s: notes', await p.evaluate(() => window.__osc), '| noise', await p.evaluate(() => window.__noise));
  for (const [lesson, step] of [[4, 1], [2, 0], [3, 2], [7, 0]]) {
    await p.evaluate(i => document.querySelectorAll('#topics .topic')[i].click(), lesson); await p.waitForTimeout(400);
    await p.click('#steps button:nth-child(' + (step + 1) + ')'); await p.waitForTimeout(150);
    let broken = 0, frames = 0, firstLineAt = null; const t0 = Date.now();
    for (let t = 0; t < 120; t++) { // 6 s of writing
      const r = await p.evaluate(() => { const txt = [...document.querySelectorAll('#boardLines .chalk span')].map(e => e.textContent).join('\n'); return [/[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?:[^\uD800-\uDBFF]|^)[\uDC00-\uDFFF]|�/.test(txt), txt.length]; });
      frames++; if (r[0]) broken++; if (r[1] && firstLineAt === null) firstLineAt = Date.now() - t0; await p.waitForTimeout(50);
    }
    const font = await p.$eval('#boardLines .chalk:not(.title)', e => getComputedStyle(e).fontFamily).catch(() => '-');
    console.log('lesson', lesson + 1, 'step', step + 1, '| frames with a broken character:', broken + '/' + frames, '| first line after', firstLineAt, 'ms | font:', font.split(',')[0], '| board:', (await p.textContent('#boardLines')).replace(/\s+/g, ' ').slice(0, 70));
    await p.screenshot({ path: 'iso/BD-' + (lesson + 1) + '-' + (step + 1) + '.png' });
    await p.click('#learn .qhead .iconbtn').catch(() => {}); await p.waitForTimeout(200); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(400); await p.mouse.click(5, 300);
  }
  // celebration sounds
  const o0 = await p.evaluate(() => window.__osc), n0 = await p.evaluate(() => window.__noise);
  await p.evaluate(() => CQCelebrate('Congratulations!', 'test')); await p.waitForTimeout(2500);
  console.log('celebration: notes', (await p.evaluate(() => window.__osc)) - o0, '| noise bursts', (await p.evaluate(() => window.__noise)) - n0);
  console.log('errors', errs); await b.close();
})();
