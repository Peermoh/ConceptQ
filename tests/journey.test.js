// A new user's whole journey on a phone and a laptop: welcome, tour, home, Me, a lesson, the full quiz, the house.
// Fails on any page error, failed load, button that cannot be pressed, stuck quiz or content sticking out sideways.
const { chromium, devices } = require('playwright'); const { BASE, check, finish } = require('./lib');
const URL = BASE + '/index.html';
const found = [];
const note = (dev, where, what) => { found.push(`[${dev}] ${where}: ${what}`); console.log(`         [${dev}] ${where}: ${what}`); };

async function overflow(p, dev, where) {
  const o = await p.evaluate(() => {
    const w = window.innerWidth, out = [];
    if (document.documentElement.scrollWidth > w + 1) out.push('page scrolls sideways (' + document.documentElement.scrollWidth + ' > ' + w + ')');
    document.querySelectorAll('.screen:not([hidden]) *').forEach(el => {
      const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
      if (r.width && r.right > w + 2 && cs.position !== 'fixed' && el.offsetParent && !el.closest('[style*="overflow"]') && out.length < 6)
        out.push((el.id ? '#' + el.id : el.tagName.toLowerCase() + '.' + (el.className.baseVal ?? el.className)).slice(0, 50) + ' sticks out right by ' + Math.round(r.right - w) + 'px');
    });
    return out;
  });
  o.forEach(x => note(dev, where, x));
}
async function shot() {} // set SHOTS=1 to keep screenshots (not needed for the check)
async function tryClick(p, sel, dev, where, t = 4000) {
  try { await p.click(sel, { timeout: t }); return true; }
  catch (e) { note(dev, where, `could not click ${sel}: ` + (e.message.match(/(intercepts pointer events|not visible|detached|Timeout[^\n]*)/) || [''])[0]); return false; }
}

async function run(dev, ctxOpts) {
  const b = await chromium.launch();
  const ctx = await b.newContext(ctxOpts);
  const p = await ctx.newPage();
  p.on('pageerror', e => note(dev, 'JS error', e.message.split('\n')[0]));
  p.on('console', m => { if (m.type() === 'error') note(dev, 'console', m.text().slice(0, 160)); });
  p.on('response', r => { if (r.status() >= 400) note(dev, 'load', r.status() + ' ' + r.url().replace(BASE + '/', '')); });
  p.on('requestfailed', r => { const f = r.failure() && r.failure().errorText; if (f && !/ERR_ABORTED/.test(f)) note(dev, 'load', 'failed ' + r.url().replace(BASE + '/', '') + ' ' + f); });

  await p.goto(URL); await p.waitForTimeout(800); await shot(p, dev, '01-welcome'); await overflow(p, dev, 'welcome');
  // welcome flow
  await p.fill('#wlNameIn', 'Mia'); await tryClick(p, '#wlNameGo', dev, 'welcome name'); await p.waitForTimeout(400);
  await tryClick(p, '#wlNames button:has-text("Sparky")', dev, 'welcome robot chip'); await p.waitForTimeout(200);
  await tryClick(p, '#wlTeachGo', dev, 'welcome robot name'); await p.waitForTimeout(400);
  await tryClick(p, '#wlAges button:has-text("7")', dev, 'welcome age'); await p.waitForTimeout(1800);
  await shot(p, dev, '02-pick'); await overflow(p, dev, 'welcome pick');
  await tryClick(p, '#wlCards .cq-card >> nth=0', dev, 'welcome course card'); await tryClick(p, '#wlGo', dev, 'welcome go'); await p.waitForTimeout(1200);
  // tour: walk every step
  let steps = 0;
  while (await p.$('.tour') && steps < 15) { await shot(p, dev, '03-tour-' + steps); if (!await tryClick(p, '.tour .tc-next', dev, 'tour step ' + steps)) break; steps++; await p.waitForTimeout(350); }
  if (await p.$('.tour')) note(dev, 'tour', 'tour still open after ' + steps + ' steps');
  await p.waitForTimeout(500); await shot(p, dev, '04-home'); await overflow(p, dev, 'home');
  // me screen
  if (await tryClick(p, '#home [data-nav="me"]', dev, 'home -> me')) { await p.waitForTimeout(600); await shot(p, dev, '05-me'); await overflow(p, dev, 'me'); await tryClick(p, '#me [data-navbar] [data-nav="home"]', dev, 'me -> learn tab'); await p.waitForTimeout(700); }
  // lesson
  if (await tryClick(p, '#startBtn', dev, 'start lesson')) {
    await p.waitForTimeout(1500); await shot(p, dev, '06-lesson'); await overflow(p, dev, 'lesson');
    await tryClick(p, '#tabRead', dev, 'lesson read tab'); await p.waitForTimeout(500); await shot(p, dev, '07-read'); await overflow(p, dev, 'lesson read');
    if (await tryClick(p, '#toQuiz', dev, 'go to quiz')) {
      await p.waitForTimeout(1000); await shot(p, dev, '08-quiz'); await overflow(p, dev, 'quiz');
      for (let q = 0; q < 25; q++) {
        if (!await p.isVisible('#quiz')) break;
        const opt = await p.$('#qOptions button:not([disabled]):visible');
        if (opt) { await opt.click().catch(() => {}); await p.waitForTimeout(700); }
        const nxt = await p.$('#quiz button:visible:has-text("Next"), #quiz button:visible:has-text("Continue"), #quiz button:visible:has-text("Got it"), #sheetSlot button:visible');
        if (nxt) { await nxt.click().catch(() => {}); await p.waitForTimeout(600); }
        if (!opt && !nxt) { note(dev, 'quiz', 'stuck on question ' + q + ' (no answer or next button)'); await shot(p, dev, '09-quiz-stuck'); break; }
      }
      await p.waitForTimeout(1200); await shot(p, dev, '10-after-quiz');
      const vis = await p.evaluate(() => [...document.querySelectorAll('.screen')].filter(s => !s.hidden && s.getClientRects().length).map(s => s.id));
      if (!vis.length) note(dev, 'after quiz', 'no screen visible');
      await overflow(p, dev, 'after quiz');
    }
  }
  // house + world iframes
  await p.goto(URL); await p.waitForTimeout(800);
  if (await tryClick(p, '#home [data-nav="house"] >> nth=0', dev, 'home -> house')) {
    await p.waitForTimeout(2500); await shot(p, dev, '11-house');
    const fr = p.frames().find(f => /house|world/.test(f.url()));
    if (!fr) note(dev, 'house', 'no house/world frame loaded');
  }
  await b.close();
}

(async () => {
  await run('phone', { ...devices['iPhone 13'], deviceScaleFactor: 1 });
  check(!found.length, 'phone: the whole journey works');
  const n = found.length; await run('laptop', { viewport: { width: 1280, height: 800 } });
  check(found.length === n, 'laptop: the whole journey works');
  finish();
})();
