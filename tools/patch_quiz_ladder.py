# Maths quizzes: Easy → Medium → Hard order, some answers typed on a number pad (no guessing between 3 choices),
# and a 🌟 challenge question at the end that is a bonus (right: +20 embers; wrong: does not stop a pass).
# Run once on prototype/index.html (each edit checks that its anchor is there exactly once).
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prototype', 'index.html')
h = open(P).read()
def rep(a, b):
    global h
    assert h.count(a) == 1, 'anchor not found once: ' + a[:80]
    h = h.replace(a, b)

rep("""  function makeQuiz(ld) {
    if (ld.fresh) return makeCourseQuiz(ld);""", """  // ---- Maths: a ladder from easy to hard, typed answers, and a bonus challenge question to finish ----
  var NUMRX = /^(₹)?\\s?(\\d[\\d,]*(?:\\.\\d+)?)(?:\\s([A-Za-z]+))?$/;
  function numParts(o) { var m = NUMRX.exec(String(o).trim()); return m ? { pre: m[1] || '', n: +m[2].replace(/,/g, ''), unit: m[3] || '', dec: m[2].indexOf('.') >= 0 } : null; }
  // typed only when every choice is a plain number with the same ₹ / unit (so "4 each, 1 left" stays a choice)
  function typedOK(q) { var r = numParts(q.options[q.answer]); return !!r && q.options.every(function (o) { var p = numParts(o); return p && p.unit === r.unit && p.pre === r.pre; }); }
  function mathsLadder(qs, ld) {
    var lvOf = function (q) { return typeof q.level === 'number' ? q.level : 1; };
    qs.forEach(function (q, i) { q._i = i; });
    qs.sort(function (a, b) { return lvOf(a) - lvOf(b) || a._i - b._i; });
    qs.forEach(function (q) { var L = lvOf(q); if (typedOK(q) && (L === 2 || (L === 1 && Math.random() < 0.5))) q.num = numParts(q.options[q.answer]); });
    var pool = typeof challengeFor === 'function' ? challengeFor(ld.key) : null;
    for (var t = 0; pool && t < 20; t++) {
      QLEVEL = 2; var c = null; try { c = pickOne(pool)(); } catch (e) { c = null; } QLEVEL = 1; if (!c) continue;
      var order = shuffled(c.options.map(function (o, i) { return i; }));
      var cq = { text: c.text, code: c.code, pic: c.pic, level: 3, bonus: true, options: order.map(function (i) { return c.options[i]; }), why: order.map(function (i) { return c.why[i]; }), answer: order.indexOf(c.answer) };
      if (typedOK(cq)) cq.num = numParts(cq.options[cq.answer]);
      qs.push(cq); break;
    }
    return qs;
  }
  // a pass: every question right, except the bonus challenge
  function quizPassed() { return Q.every(function (qq, j) { return qq.bonus || answers[j] === qq.answer; }); }
  function makeQuiz(ld) {
    if (ld.fresh) return COURSE === 'maths' ? mathsLadder(makeCourseQuiz(ld), ld) : makeCourseQuiz(ld);""")

rep("""(typeof q.level === 'number' ? ' · ' + ['⭐ Easy', '⭐⭐ Medium', '⭐⭐⭐ Hard'][q.level] : '')""",
    """(typeof q.level === 'number' ? ' · ' + ['⭐ Easy', '⭐⭐ Medium', '⭐⭐⭐ Hard', '🌟 Challenge (bonus)'][q.level] : '')""")
rep("""prog += '<span class="' + (answers[i] === undefined ? (i === qi ? 'now' : '') : answers[i] === Q[i].answer ? 'on' : 'miss') + '"></span>';""",
    """prog += '<span class="' + (answers[i] === undefined ? (i === qi ? 'now' : '') : answers[i] === Q[i].answer ? 'on' : 'miss') + (Q[i].bonus ? ' bonus' : '') + '"></span>';""")
rep("""    box.innerHTML = '';
    q.options.forEach(function (o, i) {""", """    box.innerHTML = '';
    if (q.num) renderTyped(q, box, done); else q.options.forEach(function (o, i) {""")

rep("""  function pick(i, btn) {
    var q = Q[qi];
    answers[qi] = i;
    var right = i === q.answer;
    if (right) { firstTry++; earned += 10; burst(btn); }""", """  // a typed answer: a number pad instead of choices
  function renderTyped(q, box, done) {
    var v = done ? (q.typed || '') : '', wrap = document.createElement('div'), show = document.createElement('div'), keys = document.createElement('div');
    wrap.className = 'qtype'; show.className = 'qtype-show'; keys.className = 'qtype-keys';
    var dec = q.options.some(function (o) { var p = numParts(o); return p && p.dec; });
    function paint() {
      show.innerHTML = '';
      if (q.num.pre) show.appendChild(document.createTextNode(q.num.pre));
      var s = document.createElement('b'); s.textContent = v || '?'; if (!v) s.className = 'empty'; show.appendChild(s);
      if (q.num.unit) show.appendChild(document.createTextNode(' ' + q.num.unit));
      var ok = keys.querySelector('.ok'); if (ok) ok.disabled = !v;
    }
    function press(d) { if (d === 'del') v = v.slice(0, -1); else if (v.length < 8 && !(d === '.' && v.indexOf('.') >= 0)) v += d; paint(); }
    function check() { if (!v) return; document.removeEventListener('keydown', onKey); typedAnswer(q, v, show, keys); }
    function onKey(e) {
      if (Q[qi] !== q || answers[qi] !== undefined || document.getElementById('quiz').hidden || !document.getElementById('scratch').hidden) { if (Q[qi] !== q || answers[qi] !== undefined) document.removeEventListener('keydown', onKey); return; }
      if (/^[0-9]$/.test(e.key) || (dec && e.key === '.')) press(e.key); else if (e.key === 'Backspace') press('del'); else if (e.key === 'Enter') check(); else return;
      e.preventDefault();
    }
    wrap.appendChild(show);
    if (done) {
      show.classList.add(answers[qi] === q.answer ? 'right' : 'wrong');
    } else {
      '123456789'.split('').concat([dec ? '.' : 'del', '0', dec ? 'del' : 'ok']).forEach(function (d) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'qkey' + (d === 'ok' ? ' ok' : '');
        b.textContent = d === 'del' ? '⌫' : d === 'ok' ? '✓ Check' : d; b.setAttribute('aria-label', d === 'del' ? 'Delete' : d === 'ok' ? 'Check my answer' : d);
        b.addEventListener('click', function () { d === 'ok' ? check() : press(d); }); keys.appendChild(b);
      });
      if (dec) { var ok = document.createElement('button'); ok.type = 'button'; ok.className = 'qkey ok wide'; ok.textContent = '✓ Check'; ok.addEventListener('click', check); keys.appendChild(ok); }
      wrap.appendChild(keys); document.addEventListener('keydown', onKey);
    }
    box.appendChild(wrap); paint();
  }
  function typedAnswer(q, v, show, keys) {
    var n = parseFloat(v), i = -1;
    q.options.forEach(function (o, k) { var p = numParts(o); if (p && Math.abs(p.n - n) < 1e-9) i = k; });
    q.typed = v; keys.hidden = true;
    show.classList.add(i === q.answer ? 'right' : 'wrong');
    pick(i, show);
  }
  function pick(i, btn) {
    var q = Q[qi];
    answers[qi] = i;
    var right = i === q.answer;
    if (right) { firstTry++; earned += q.bonus ? 20 : 10; burst(btn); }""")

rep("""    var text = q.why[i] + (right ? '' : '<span class="fix">The answer is <b>' + esc2(q.options[q.answer]) + '</b>: ' + q.why[q.answer] + '</span>');
    var label = !last ? 'Next question' : allAnswered() ? (Q.every(function (qq, j) { return answers[j] === qq.answer; }) ? LD.lastBtn : 'See my results') : 'Next question';
    sheet(right, right ? 'Yes, that\\'s it!' : 'Not quite', text, label);""",
"""    var said = i >= 0 ? q.why[i] : 'You wrote <b>' + esc2((q.num.pre || '') + q.typed + (q.num.unit ? ' ' + q.num.unit : '')) + '</b>.';
    var text = said + (right ? '' : '<span class="fix">The answer is <b>' + esc2(q.options[q.answer]) + '</b>: ' + q.why[q.answer] + '</span>') + (q.bonus && !right ? '<span class="fix">The 🌟 challenge is a bonus: it does not stop you finishing.</span>' : '');
    var label = !last ? 'Next question' : allAnswered() ? (quizPassed() ? LD.lastBtn : 'See my results') : 'Next question';
    sheet(right, right ? (q.bonus ? '🌟 Challenge cracked! +20' : 'Yes, that\\'s it!') : (q.bonus ? 'Good try!' : 'Not quite'), text, label);""")
rep("""      if (Q.every(function (qq, j) { return answers[j] === qq.answer; })) finish(); else showResults();""",
    """      if (quizPassed()) finish(); else showResults();""")
rep("""    Q.forEach(function (q, j) { if (answers[j] !== q.answer) { var si = stepFor(q); if (!seen[si]) { seen[si] = 1; wrong.push({ step: si, q: q }); } } });
    var right = Q.filter(function (q, j) { return answers[j] === q.answer; }).length;
    document.getElementById('rTitle').textContent = right + ' of ' + Q.length + ' right. Almost there!';""",
"""    Q.forEach(function (q, j) { if (!q.bonus && answers[j] !== q.answer) { var si = stepFor(q); if (!seen[si]) { seen[si] = 1; wrong.push({ step: si, q: q }); } } });
    var counted = Q.filter(function (q) { return !q.bonus; }), right = counted.filter(function (q) { return answers[Q.indexOf(q)] === q.answer; }).length;
    document.getElementById('rTitle').textContent = right + ' of ' + counted.length + ' right. Almost there!';""")

# the read-aloud does not read choices that are not on screen
rep("""parts = [quizPieces(quizSay(q.text))].concat(q.options.map(function (o, i) {""", """parts = [quizPieces(quizSay(q.text))].concat((q.num && answers[qi] === undefined ? [] : q.options).map(function (o, i) {""")
rep("""parts = [quizSay(q.text)].concat(q.options.map(function (o, i) {""", """parts = [quizSay(q.text)].concat((q.num && answers[qi] === undefined ? [] : q.options).map(function (o, i) {""")

# styles: the number pad and the bonus dot in the progress bar
rep(""".scratch-pens[hidden], .scratch-btn[hidden], #scratchCv[hidden] { display: none; }""", """.scratch-pens[hidden], .scratch-btn[hidden], #scratchCv[hidden] { display: none; }
.qtype { display: flex; flex-direction: column; align-items: center; gap: 12px; }
.qtype-show { min-width: 180px; padding: 10px 22px; border-radius: 16px; border: 3px solid rgba(255,255,255,.35); background: rgba(255,255,255,.08); font: 800 34px/1.1 var(--font-display, inherit); text-align: center; color: var(--cream, #FFF1E2); }
.qtype-show b { font-weight: inherit; } .qtype-show b.empty { opacity: .35; }
.qtype-show.right { border-color: #5FD39A; background: rgba(95,211,154,.16); } .qtype-show.wrong { border-color: #FF7A6B; background: rgba(255,122,107,.16); }
.qtype-keys { display: grid; grid-template-columns: repeat(3, 72px); gap: 8px; } .qtype-keys[hidden] { display: none; }
.qkey { min-height: 52px; border-radius: 14px; border: 2px solid rgba(255,255,255,.25); background: rgba(255,255,255,.1); color: var(--cream, #FFF1E2); font: 800 22px/1 inherit; cursor: pointer; }
.qkey.ok { background: #FFB547; border-color: #FFB547; color: #2A1330; font-size: 16px; } .qkey.ok:disabled { opacity: .45; cursor: default; } .qkey.wide { grid-column: 1 / -1; }
.qkey:focus-visible { outline: 3px solid #8FD3FF; outline-offset: 2px; }
#qProgress span.bonus { border-radius: 3px; transform: rotate(45deg) scale(.85); }""")
open(P, 'w').write(h)
print('quiz ladder in place')
