const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ ...devices['iPhone 13'] });
  await ctx.addInitScript(() => { localStorage.setItem('cq-courses', JSON.stringify({ course: 'english', maths: 0, english: 3 })); });
  const p = await ctx.newPage(); const req = []; p.on('request', r => { if (/phonics/.test(r.url())) req.push(r.url().split('/').pop()); });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(600);
  await p.click('#startBtn'); await p.waitForTimeout(400); await p.click('#toQuiz'); await p.waitForTimeout(300);
  // watch the media element that plays phonics: sample its time while the first sound question plays
  for (let q = 0; q < 5; q++) {
    const t = await p.textContent('#qText'), hear = await p.textContent('#qHear');
    if (/again/.test(hear)) {
      const samples = [];
      for (let i = 0; i < 12; i++) { samples.push(await p.evaluate(() => { const a = [...document.querySelectorAll('audio')]; return window.__phon(); })); await p.waitForTimeout(150); }
      console.log('Q', t, '| requests', req.join(','), '|', JSON.stringify(samples));
    }
    for (let k = 0; k < 3; k++) { await p.click('#opt-' + q + '-' + k); await p.waitForTimeout(80); if (await p.$('.sheet.is-right')) break; await p.evaluate(qq => window.__undo(qq), q); }
    await p.click('#sheetBtn'); await p.waitForTimeout(150);
  }
  await b.close();
})();
