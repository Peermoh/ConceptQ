// Test-only hook: dump every English lesson (board + say) and 60 generated quizzes per lesson to JSON for checking.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext()).newPage();
  await p.route('**/index.html', async r => { const res = await r.fetch(); let t = await res.text();
    t = t.replace('function voiceLang() {', `window.__eng = function (course, n) { useCourse(course, true);
      var out = [];
      Object.keys(LESSON_DATA).forEach(function (k) { var L = LESSON_DATA[k]; LD = L;
        var quizzes = []; for (var i = 0; i < n; i++) { try { quizzes.push(makeQuiz(L)); } catch (e) { quizzes.push({ err: String(e) }); } }
        out.push({ idx: k, key: L.key, title: L.title, tag: L.tag, topic: L.topic,
          board: L.board.map(function (s) { return { say: s.say, cue: s.cue, lines: s.lines }; }),
          quizzes: quizzes.map(function (Q) { return Q.err ? Q : Q.map(function (q) { return { text: q.text, options: q.options, answer: q.answer, why: q.why, snd: q.snd, pic: q.pic ? q.pic.replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim().slice(0, 80) : '', spoken: speakText(q.text), spokenOpts: q.options.map(function (o) { return speakText(o); }) }; }); }) });
      });
      return out; };
    function voiceLang() {`);
    await r.fulfill({ response: res, body: t }); });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(1000);
  const course = process.argv[2] || 'english';
  const d = await p.evaluate(c => window.__eng(c, 60), course);
  fs.writeFileSync(__dirname + '/' + course + '.json', JSON.stringify(d, null, 1));
  console.log(course, 'lessons:', d.length, 'quizzes per lesson:', d[0] && d[0].quizzes.length, 'page errors:', errs);
  await b.close();
})();
