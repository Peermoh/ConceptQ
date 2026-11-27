// Shared helpers for the browser tests. BASE is set by run.js (a local server for ../prototype).
const { chromium, devices } = require('playwright');
const BASE = process.env.BASE || 'http://localhost:8765';
let pass = 0, fail = 0;
function check(ok, msg) { ok ? pass++ : fail++; console.log((ok ? '  ok   ' : '  FAIL ') + msg); return ok; }
function finish() { console.log(`  ${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0); }
// hooks: [[text in index.html, text to put before it], ...] - test-only lines that expose app internals
async function open({ phone = true, hooks = [], init = null, autoplay = false } = {}) {
  const b = await chromium.launch(autoplay ? { args: ['--autoplay-policy=no-user-gesture-required'] } : {});
  const ctx = await b.newContext(phone ? { ...devices['iPhone 13'] } : { viewport: { width: 1280, height: 800 } });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  if (init) await p.addInitScript(init);
  if (hooks.length) await p.route('**/index.html', async r => {
    const res = await r.fetch(); let t = await res.text();
    for (const [at, add] of hooks) { if (!t.includes(at)) throw new Error('hook anchor not found: ' + at); t = t.replace(at, add + '\n' + at); }
    await r.fulfill({ response: res, body: t });
  });
  await p.goto(BASE + '/index.html'); await p.waitForTimeout(700);
  return { b, p, errs };
}
// the real first-run flow: name, robot name, age, course
async function onboard(p, course = 'maths', age = '7') {
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(300);
  await p.click('#wlNames button:has-text("Sparky")'); await p.click('#wlTeachGo'); await p.waitForTimeout(300);
  await p.click(`#wlAges button:has-text("${age}")`); await p.waitForTimeout(1500);
  await p.click(`#wlCards .cq-card[data-c="${course}"]`, { force: true }); await p.click('#wlGo', { force: true }); await p.waitForTimeout(1200);
  if (await p.$('.tour')) await p.click('.tour .tc-skip');
}
async function setNarrator(p, who) {
  const key = await p.evaluate(() => Object.keys(localStorage).find(k => /profile/.test(k)));
  await p.evaluate(([k, w]) => { const pr = JSON.parse(localStorage.getItem(k)); pr.narrator = w; localStorage.setItem(k, JSON.stringify(pr)); }, [key, who]);
  await p.reload(); await p.waitForTimeout(1200); if (await p.$('.tour')) await p.click('.tour .tc-skip');
}
module.exports = { BASE, check, finish, open, onboard, setNarrator, devices };
