// Guided tour (after the welcome), sounds on/off, the wheel's prize hint, and the robot logo.
const { chromium, devices } = require('playwright');
const desk = process.argv[2] === 'desktop';
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }); const errs = [];
  const ctx = await b.newContext(desk ? { viewport: { width: 1366, height: 800 }, deviceScaleFactor: 1 } : { ...devices['iPhone 13'], deviceScaleFactor: 1 });
  // count the sounds the page makes: wrap AudioContext so oscillators and noise sources are counted
  await ctx.addInitScript(() => { const C = window.AudioContext; window.__snd = 0; window.AudioContext = function () { const c = new C(); const o = c.createOscillator.bind(c), n = c.createBufferSource.bind(c); c.createOscillator = function () { window.__snd++; return o(); }; c.createBufferSource = function () { window.__snd++; return n(); }; return c; }; });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  const tag = desk ? 'desk' : 'phone';
  await p.goto('http://localhost:8765/index.html?tour'); await p.waitForTimeout(600);
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(200);
  await p.fill('#wlTeachIn', 'Sparky'); await p.click('#wlTeachGo'); await p.waitForTimeout(200);
  await p.click('#wlAges button:has-text("7")'); await p.waitForTimeout(300);
  await p.click('#wlCards .cq-card[data-c="maths"]'); await p.click('#wlGo'); await p.waitForTimeout(1300);
  console.log('logo:', await p.getAttribute('#topAvatar', 'aria-label'), '| top:', await p.textContent('#greet'), '/', await p.textContent('#topName'), '| title:', await p.title(), '| favicon:', !!(await p.$('link[rel="icon"][href^="data:image/svg"]')));
  const steps = [];
  for (let i = 0; i < 12; i++) {
    if (!(await p.$('.tour'))) break;
    steps.push(await p.textContent('.tour-card h3'));
    if (i === 0 || i === 3 || i === 5) await p.screenshot({ path: 'iso/TT-' + tag + '-' + i + '.png' });
    await p.click('.tc-next'); await p.waitForTimeout(450);
  }
  console.log('tour steps (' + steps.length + '):', steps.join(' → '), '| tour gone:', !(await p.$('.tour')));
  console.log('sounds so far:', await p.evaluate(() => window.__snd));
  // sounds off: the world's sound stops and no new sounds play
  await p.click('#soundBtn'); await p.waitForTimeout(300);
  const before = await p.evaluate(() => window.__snd); await p.click('#coursesTile'); await p.waitForTimeout(1500); await p.click('#courses [data-go="home"]').catch(() => {}); await p.waitForTimeout(1500);
  console.log('muted: icon', await p.textContent('#soundIc'), '| new sounds while muted:', (await p.evaluate(() => window.__snd)) - before, '| saved:', await p.evaluate(() => JSON.parse(localStorage.getItem('cq-profile')).sounds));
  await p.click('#soundBtn'); await p.waitForTimeout(300);
  // wheel hint, also while spinning (give two spins' worth of embers)
  await p.evaluate(() => { const s = JSON.parse(localStorage.getItem('cq-progress')); s.embers = 500; localStorage.setItem('cq-progress', JSON.stringify(s)); }); await p.reload(); await p.waitForTimeout(800);
  await p.click('#prizeTile'); await p.waitForTimeout(300);
  await p.click('#wheelSpin'); await p.waitForTimeout(1200);
  console.log('wheel hint while spinning:', await p.isVisible('#wheelHint'), '|', await p.textContent('#wheelHint'));
  await p.screenshot({ path: 'iso/TT-' + tag + '-wheel.png' });
  await p.waitForTimeout(3500); console.log('won:', await p.textContent('#wheelPrize'));
  await p.click('#wheelEdit'); await p.waitForTimeout(500); console.log('edit → Me with grown-up check:', await p.isVisible('#me'), await p.isVisible('#gateBox'));
  // Me: replay the tour
  await p.fill('#gateIn', '0').catch(() => {}); await p.click('#gateCancel').catch(() => {});
  console.log('me sounds toggle:', await p.isChecked('#setSounds'));
  await p.click('#tourAgain'); await p.waitForTimeout(600); console.log('tour again:', await p.textContent('.tour-card h3'));
  await p.click('.tc-skip'); await p.waitForTimeout(200);
  console.log('errors', errs); await b.close();
})();
