// "Read it to me" on Maths and English questions plays the narrator's recorded voice (never the phone's), the robot
// points at each choice as it is read, answering stops it, and every piece freshly made quizzes need is recorded.
const { check, finish, open, onboard, setNarrator } = require('./lib');
const HOOKS = [
  ["  function quizSay(t) {", "  window.__qv = function () { return qvEl; }; window.__qvBusy = function () { return !!(QV.srcs && QV.srcs.length) || !qvEl.paused; };"],
  ["  function makeQuiz(ld) {", `window.__cover = function (N) { var miss = {}, n = 0; return quizVoice().then(function (m) { Object.keys(LESSON_DATA).forEach(function (k) { for (var i = 0; i < N; i++) makeQuiz(LESSON_DATA[k]).forEach(function (q) { if (q.snd) return; n++; [quizSay(q.text)].concat(q.options.map(function (o) { return quizOptSay(q, o); })).forEach(function (s) { quizPieces(s).forEach(function (pc) { if (!m[pc]) miss[pc] = 1; }); }); }); }); return { n: n, missing: Object.keys(miss) }; }); };`]];
const INIT = () => {
  window.__said = []; window.__plays = 0;
  window.SpeechSynthesisUtterance = function (t) { this.text = t; };
  Object.defineProperty(window, 'speechSynthesis', { value: { speak(u) { window.__said.push(u.text); setTimeout(() => u.onend && u.onend(), 50); }, cancel() {}, getVoices() { return []; }, addEventListener() {} } });
  const pl = HTMLMediaElement.prototype.play;
  HTMLMediaElement.prototype.play = function () { if (window.__qv && this === window.__qv() && !this.muted) window.__plays++; return pl.apply(this, arguments); };
  const st = AudioBufferSourceNode.prototype.start;
  AudioBufferSourceNode.prototype.start = function () { if (this._qv) window.__plays++; return st.apply(this, arguments); };
};
(async () => {
  for (const [course, who] of [['maths', 'prabhat'], ['english', 'ryan'], ['maths', 'ryan'], ['english', 'prabhat']]) {
    const { b, p, errs } = await open({ autoplay: true, hooks: HOOKS, init: INIT });
    await onboard(p, course); await setNarrator(p, who);
    await p.click('#startBtn'); await p.waitForTimeout(700); await p.click('#toQuiz', { force: true }); await p.waitForTimeout(700);
    let read = 0;
    for (let n = 0; n < 5 && read < 2; n++) {
      if ((await p.textContent('#qHear')).includes('again')) { // a phonics question: its sounds are recorded separately
        await p.click('#qOptions .opt >> nth=0'); await p.waitForTimeout(300); const nx = await p.$('#sheetSlot button:visible'); if (!nx) break; await nx.click(); await p.waitForTimeout(600); continue;
      }
      await p.evaluate(() => { window.__said = []; window.__plays = 0; });
      await p.click('#qHear'); const seen = new Set();
      for (let t = 0; t < 36; t++) { await p.waitForTimeout(250); seen.add(await p.evaluate(() => [...document.querySelectorAll('#qOptions .opt')].findIndex(o => o.classList.contains('reading')))); }
      const r = await p.evaluate(() => ({ said: window.__said.length, plays: window.__plays }));
      const text = (await p.textContent('#qText')).slice(0, 50), typed = await p.isVisible('.qtype-keys');
      if (typed) check(r.plays >= 1 && r.said === 0, `${course}/${who}: typed question "${text}" read in the recorded voice (the question only: there are no choices to read)`);
      else check(r.plays > 2 && r.said === 0 && seen.has(0) && seen.has(1), `${course}/${who}: "${text}" read in the recorded voice, the robot points along` + (r.plays > 2 && r.said === 0 && seen.has(0) && seen.has(1) ? "" : ` [pieces ${r.plays}, phone ${r.said}, robot at ${[...seen].join(",")}]`));
      if (typed) { await p.click('.qtype-keys .qkey >> nth=0'); await p.click('.qkey.ok'); } else await p.click('#qOptions .opt >> nth=0');
      await p.waitForTimeout(300);
      check(!(await p.evaluate(() => window.__qvBusy())), `${course}/${who}: answering stops the reading`);
      read++; const nx = await p.$('#sheetSlot button:visible'); if (!nx) break; await nx.click(); await p.waitForTimeout(600);
    }
    const cov = await p.evaluate(n => window.__cover(n), course === 'maths' ? 200 : 300);
    check(!cov.missing.length, `${course}/${who}: all pieces of ${cov.n} freshly made questions are recorded ${cov.missing.slice(0, 8).join(' | ')}`);
    check(!errs.length, 'no page errors ' + errs.join(' | '));
    await b.close();
  }
  // recordings unreachable: the phone voice takes over
  const { b, p } = await open({ autoplay: true, hooks: HOOKS, init: INIT });
  await p.route(/audio\/quiz\//, r => r.abort());
  await onboard(p, 'maths'); await p.click('#startBtn'); await p.waitForTimeout(700); await p.click('#toQuiz', { force: true }); await p.waitForTimeout(700);
  await p.evaluate(() => { window.__said = []; }); await p.click('#qHear'); await p.waitForTimeout(1500);
  check(await p.evaluate(() => window.__said.length) > 0, 'quiz recordings blocked: the phone voice reads the question instead');
  await b.close(); finish();
})();
