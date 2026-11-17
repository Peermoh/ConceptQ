// screenshots of quiz questions with the new pictures (one per lesson)
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  for (const [c, n] of [['maths', 0], ['maths', 7], ['maths', 9], ['maths', 11], ['english', 3]]) {
    await p.evaluate(() => localStorage.clear()).catch(() => {});
    await ctx.clearCookies();
    await p.goto('http://localhost:8765/index.html');
    await p.evaluate(a => { localStorage.setItem('cq-courses', JSON.stringify({ course: a[0], maths: a[0] === 'maths' ? a[1] : 0, english: a[0] === 'english' ? a[1] : 0 })); }, [c, n]);
    await p.reload(); await p.waitForTimeout(500);
    await p.click('#startBtn'); await p.waitForTimeout(300); await p.click('#toQuiz'); await p.waitForTimeout(300);
    const nq = +((await p.textContent('#qTag')).match(/of (\d+)/)[1]); let shot = 0;
    for (let q = 0; q < nq; q++) {
      const t = await p.textContent('#qText'), rich = await p.$eval('#qPic', e => e.classList.contains('rich'));
      console.log(c, n, 'Q' + (q + 1), rich ? 'RICH' : '    ', t);
      if (rich && shot < 2) { await p.screenshot({ path: 'iso/Q-' + c + n + '-' + q + '.png' }); shot++; }
      for (let k = 0; k < 4; k++) { if (!(await p.$('#opt-' + q + '-' + k))) break; await p.click('#opt-' + q + '-' + k); await p.waitForTimeout(60); if (await p.$('.sheet.is-right')) break; await p.evaluate(qq => window.__undo(qq), q); }
      await p.click('#sheetBtn'); await p.waitForTimeout(120);
    }
  }
  console.log('errors', errs); await b.close();
})();
