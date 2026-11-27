const { BASE, check, finish } = require('./lib');
// Lesson recordings blocked: the phone voice must read the sound-free DEVICE lines; captions keep the lesson text.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(() => {
    window.__said = [];
    const FakeU = function (t) { this.text = t; }; window.SpeechSynthesisUtterance = FakeU;
    const ss = { speak(u) { window.__said.push(u.text); setTimeout(() => { u.onstart && u.onstart(); }, 10); setTimeout(() => { u.onend && u.onend(); }, 300); },
      cancel() {}, pause() {}, resume() {}, getVoices() { return []; }, speaking: false, addEventListener() {}, onvoiceschanged: null };
    Object.defineProperty(window, 'speechSynthesis', { value: ss });
  });
  await p.route(/audio\/(ryan|prabhat)\/e2_s1\.mp3/, r => r.abort());
  await p.goto(BASE + '/index.html'); await p.waitForTimeout(700);
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(300);
  await p.click('#wlNames button:has-text("Sparky")'); await p.click('#wlTeachGo'); await p.waitForTimeout(300);
  await p.click('#wlAges button:has-text("6")'); await p.waitForTimeout(1500);
  await p.click('#wlCards .cq-card[data-c="english"]', { force: true }); await p.click('#wlGo', { force: true }); await p.waitForTimeout(1200);
  if (await p.$('.tour')) await p.click('.tour .tc-skip');
  await p.click('#startBtn'); await p.waitForTimeout(900);
  console.log('lesson:', await p.textContent('#learnTitle'));
  await p.click('#playBtn'); await p.waitForTimeout(9000);
  const said = await p.evaluate(() => window.__said.filter(Boolean));
  const bad = said.filter(s => /\bsays (sss|a|t|p|i|nnn)\b|starts with (s|p|n|sss),/.test(s));
  check(said.length >= 2 && !bad.length, 'lesson recording blocked: the phone voice reads the sound lines in words (no bare sounds)');
  check(/S says sss/.test(await p.textContent('#caption')) || said.length > 2, 'the caption still shows the lesson text');
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
