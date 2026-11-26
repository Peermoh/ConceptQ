const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext()).newPage();
  await p.route('**/index.html', async r => { const res = await r.fetch(); let t = await res.text();
    t = t.replace('function makeQuiz(ld) {', 'window.__qs = function (c, N) { useCourse(c, true); var out = {}; Object.keys(LESSON_DATA).forEach(function (k) { var L = LESSON_DATA[k]; for (var n = 0; n < N; n++) makeQuiz(L).forEach(function (q) { if (q.snd) return; [quizSay(q.text)].concat(q.options.map(function (o) { return quizSay(o); })).forEach(function (s) { (out[L.key] = out[L.key] || {})[s] = 1; }); }); }); return out; };\n  function makeQuiz(ld) {');
    await r.fulfill({ response: res, body: t }); });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(800);
  const res = {};
  for (const c of ['maths', 'english']) for (const N of [+process.argv[2] || 300]) res[c] = await p.evaluate(([c, N]) => window.__qs(c, N), [c, N]);
  fs.writeFileSync(process.cwd() + '/qtexts.json', JSON.stringify(res));
  await b.close();
})();
