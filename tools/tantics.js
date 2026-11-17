// Age gate for coding (under 12 needs a grown-up), and the robot's shows on Home.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  // ---- welcome as a 9-year-old: Python needs a grown-up ----
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(500);
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(200); await p.click('#wlTeachGo'); await p.waitForTimeout(200);
  await p.click('#wlAges button:has-text("9")'); await p.waitForTimeout(300);
  console.log('py card tags:', await p.textContent('#wlCards .cq-card[data-c="py"] .tags'), '| dim:', await p.$eval('#wlCards .cq-card[data-c="py"]', e => e.classList.contains('dim')));
  await p.click('#wlCards .cq-card[data-c="py"]'); await p.waitForTimeout(300);
  const q = await p.textContent('label[for], .wheel-card .field span').catch(() => '');
  console.log('gate shown:', await p.isVisible('#agIn'), '|', await p.textContent('.wheel-card .field span'));
  await p.screenshot({ path: 'iso/A-gate.png' });
  await p.fill('#agIn', '1'); await p.click('#agOk'); await p.waitForTimeout(200);
  console.log('wrong answer:', await p.textContent('.wheel-card .gate-msg'), '| py chosen:', await p.$eval('#wlCards .cq-card[data-c="py"]', e => e.getAttribute('aria-pressed')));
  const m = (await p.textContent('.wheel-card .field span')).match(/(\d+) × (\d+) \+ (\d+)/);
  await p.fill('#agIn', String(+m[1] * +m[2] + +m[3])); await p.click('#agOk'); await p.waitForTimeout(200);
  console.log('right answer → py chosen:', await p.$eval('#wlCards .cq-card[data-c="py"]', e => e.getAttribute('aria-pressed')), '| go:', await p.textContent('#wlGo'));
  // maths needs no gate
  await p.click('#wlCards .cq-card[data-c="maths"]'); await p.waitForTimeout(200); console.log('maths chosen without gate:', !(await p.$('#agIn')), await p.textContent('#wlGo'));
  await p.click('#wlGo'); await p.waitForTimeout(800);
  // Me: adding Python asks again (not joined yet)
  await p.click('#home [data-nav="me"]'); await p.waitForTimeout(300);
  await p.click('#myCourses .mc:has-text("Python") button'); await p.waitForTimeout(300);
  console.log('Me add python → gate:', await p.isVisible('#agIn')); await p.click('#agNo'); await p.waitForTimeout(200);
  console.log('cancelled → still on Me, course:', await p.isVisible('#me'));
  // ---- the shows ----
  await p.uncheck('#setAntics'); await p.click('#me [data-nav="home"]'); await p.waitForTimeout(600);
  for (const name of ['dance', 'bath', 'roam', 'doors', 'rocket']) {
    const ok = await p.evaluate(n => window.__show(n), name);
    await p.waitForTimeout(name === 'rocket' ? 1500 : 1200);
    const props = await p.$$eval('.antics .prop', e => e.map(x => x.textContent).join(''));
    console.log(name, '| started:', ok, '| props now:', props, '| says:', await p.$eval('.antics .say', e => e.textContent).catch(() => '-'));
    await p.screenshot({ path: 'iso/S-' + name + '.png' });
    await p.waitForTimeout(4200);
    console.log('   ended cleanly:', !(await p.$('.antics')), '| robot visible again:', await p.$eval('#buddy', e => e.style.visibility !== 'hidden'));
  }
  await p.click('#home [data-nav="me"]'); await p.check('#setAntics'); await p.click('#me [data-nav="home"]'); await p.waitForTimeout(300);
  // they happen by themselves too: watch 25 s of idle Home
  const seen = new Set(); const t0 = Date.now();
  while (Date.now() - t0 < 25000) { const s = await p.evaluate(() => document.querySelector('.antics') ? 'show' : document.getElementById('buddy').classList.contains('sleeping') ? 'nap' : (document.getElementById('homeLumi')._act ? 'trick' : '')); if (s) seen.add(s); await p.waitForTimeout(400); }
  console.log('in 25 s of idle time saw:', [...seen].join(', '));
  console.log('errors', errs); await b.close();
})();
