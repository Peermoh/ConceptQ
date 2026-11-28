// Builds 200 quizzes per lesson in every course: no errors, the right number of questions, an answer that is one of
// the choices, an explanation per choice, no repeated choices. Python course: every generated question's code is
// run in real Python and must print what the quiz marks as right (tools/verify_generators.py).
const { check, finish, open } = require('./lib'); const fs = require('fs'), os = require('os'), path = require('path'), { spawnSync } = require('child_process');
(async () => {
  const { b, p, errs } = await open({ phone: false, hooks: [['  function makeQuiz(ld) {',
    `window.__q = function (c, N) { useCourse(c, true); var probs = [], n = 0, plain = function (s) { return String(s || '').replace(/<[^>]+>/g, '').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&'); }, samples = [];
      Object.keys(LESSON_DATA).forEach(function (k) { var L = LESSON_DATA[k], want = L.size || L.quiz.length;
        for (var r = 0; r < N; r++) { var quiz; try { quiz = makeQuiz(L); } catch (e) { probs.push(L.key + ': ' + e); break; }
          var bonus = quiz.filter(function (q) { return q.bonus; }).length;
          if (quiz.length - bonus !== want) probs.push(L.key + ': ' + (quiz.length - bonus) + ' questions, expected ' + want);
          if (c === 'maths' && (bonus !== 1 || !quiz[quiz.length - 1].bonus)) probs.push(L.key + ': the quiz should end with one bonus challenge');
          if (c === 'maths') { var lvs = quiz.filter(function (q) { return !q.bonus; }).map(function (q) { return typeof q.level === 'number' ? q.level : 1; }); if (lvs.some(function (x, i) { return i && x < lvs[i - 1]; })) probs.push(L.key + ': questions are not easy to hard: ' + lvs.join(',')); }
          quiz.forEach(function (q) { n++; var at = L.key + ': "' + plain(q.text).slice(0, 50) + '"';
            if (!(q.answer >= 0 && q.answer < q.options.length)) probs.push(at + ' answer is not one of the choices');
            if (q.why.length !== q.options.length) probs.push(at + ' needs one explanation per choice');
            if (new Set(q.options).size !== q.options.length) probs.push(at + ' has a repeated choice: ' + q.options.join(' / '));
            if (!plain(q.text).trim() && !q.snd) probs.push(at + ' has no question text');
            if (q.num) { var r = numParts(q.options[q.answer]); if (!r || r.n !== q.num.n) probs.push(at + ' typed answer does not match the right choice'); } }); } });
      var pyKeys = Object.keys(LESSON_DATA).map(function (k) { return LESSON_DATA[k].key; });
      if (c === 'py') Object.keys(GEN).filter(function (key) { return pyKeys.indexOf(key) >= 0; }).forEach(function (key) { GEN[key].forEach(function (g, gi) { for (var i = 0; i < 40; i++) { var q = g(); if (q) samples.push({ key: key, gi: gi, text: q.text, code: plain(q.code), right: q.options[q.answer], uniq: new Set(q.options).size }); } }); });
      return { n: n, probs: probs.filter(function (x, i, a) { return a.indexOf(x) === i; }), samples: samples }; };`]] });
  for (const c of ['py', 'maths', 'english']) {
    const d = await p.evaluate(c => window.__q(c, 200), c);
    check(!d.probs.length, `${c}: ${d.n} questions made, all well-formed` + (d.probs.length ? '\n         ' + d.probs.slice(0, 8).join('\n         ') : ''));
    if (c === 'py') {
      const f = path.join(os.tmpdir(), 'cq-py-samples.json'); fs.writeFileSync(f, JSON.stringify(d.samples));
      const r = spawnSync('python3', [path.join(__dirname, '..', 'tools', 'verify_generators.py'), f], { encoding: 'utf8' });
      const last = (r.stdout || '').trim().split('\n').pop();
      check(r.status === 0 && /wrong 0$/.test(last), `py: generated questions checked in real Python (${last})` + (/wrong 0$/.test(last) ? '' : '\n' + (r.stdout || r.stderr).split('\n').slice(0, 8).join('\n')));
    }
  }
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
