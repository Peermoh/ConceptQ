// Asks the app for every piece its quiz read-aloud can play: it makes N quizzes per Maths and English lesson and
// splits each question and choice the way the app does (quizSay + quizPieces). Writes qpieces.json here:
// { course: { lesson: [piece, ...] } }.   Usage (prototype served on :8765): node dump_quiz_texts.js 1500
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext()).newPage();
  await p.route('**/index.html', async r => { const res = await r.fetch(); let t = await res.text();
    t = t.replace('function makeQuiz(ld) {', `window.__qs = function (c, N) { useCourse(c, true); var out = {};
      Object.keys(LESSON_DATA).forEach(function (k) { var L = LESSON_DATA[k], set = {};
        for (var n = 0; n < N; n++) makeQuiz(L).forEach(function (q) { if (q.snd) return;
          [quizSay(q.text)].concat(q.options.map(function (o) { return quizOptSay(q, o); })).forEach(function (s) { quizPieces(s).forEach(function (pc) { set[pc] = 1; }); }); });
        out[L.key] = Object.keys(set); });
      return out; };
  function makeQuiz(ld) {`);
    await r.fulfill({ response: res, body: t }); });
  await p.goto((process.env.BASE || 'http://localhost:8765') + '/index.html'); await p.waitForTimeout(800);
  const res = {}, N = +process.argv[2] || 300;
  for (const c of ['maths', 'english']) res[c] = await p.evaluate(([c, N]) => window.__qs(c, N), [c, N]);
  fs.writeFileSync(path.join(__dirname, 'qpieces.json'), JSON.stringify(res));
  console.log(Object.entries(res).map(([c, L]) => c + ': ' + new Set(Object.values(L).flat()).size + ' pieces').join(', '));
  await b.close();
})();
