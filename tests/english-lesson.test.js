// The first English lesson plays through in the recorded voice: the board fills step by step, the caption follows,
// nothing sticks out of the board, and the quiz button is ready at the end.
const { check, finish, open, onboard } = require('./lib');
(async () => {
  const { b, p, errs } = await open({ autoplay: true });
  await onboard(p, 'english', '6');
  await p.click('#startBtn'); await p.waitForTimeout(900);
  const steps = await p.$$eval('#learnProg span', s => s.length);
  await p.click('#playBtn'); const t0 = Date.now(); let cut = 0, captions = new Set(), done = false;
  while (Date.now() - t0 < 150000) {
    await p.waitForTimeout(1000);
    const s = await p.evaluate(() => {
      const board = document.getElementById('boardLines'), w = board.getBoundingClientRect();
      return { cut: [...board.querySelectorAll('*')].filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > w.right + 2 || r.left < w.left - 2); }).length,
        cap: document.getElementById('caption').textContent.slice(0, 40), on: document.querySelectorAll('#learnProg span.on').length,
        quiz: !document.getElementById('toQuiz').disabled && document.getElementById('toQuiz').offsetParent !== null };
    });
    cut = Math.max(cut, s.cut); captions.add(s.cap);
    if (s.on === steps && s.quiz) { done = true; break; }
  }
  check(done, `all ${steps} steps played and the quiz button is ready (${Math.round((Date.now() - t0) / 1000)} s)`);
  check(captions.size >= steps, `the caption followed the narration (${captions.size} different captions)`);
  check(!cut, 'nothing sticks out of the board');
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
