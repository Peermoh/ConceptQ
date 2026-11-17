# Maths/English quizzes: 4 fresh questions at mixed levels + 1 hand-written, no repeats for about 5 tries,
# a level badge, read-aloud in the narrator's voice (Prabhat / Ryan when the device has it) with "Option A, B, C",
# a livelier prize wheel, and embers the puzzle can spend to place a piece.
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- quiz mix and memory ----------------
rep("  function makeQuiz(ld) {\n",
r"""  // ---- Maths and English: 4 fresh questions (easy, medium, hard and one more) + 1 hand-written, chosen so a question
  // does not come back for about five tries. Recently asked questions are remembered per lesson in cq-qhist.
  function qHist(key, add) {
    var h = {}; try { h = JSON.parse(localStorage.getItem('cq-qhist') || '{}') || {}; } catch (e) {}
    if (!Array.isArray(h[key])) h[key] = [];
    if (add) { h[key] = h[key].concat(add).slice(-30); try { localStorage.setItem('cq-qhist', JSON.stringify(h)); } catch (e) {} }
    return h[key];
  }
  function qid(q) { return q.text + '|' + q.options[0]; }
  function makeCourseQuiz(ld) {
    var hist = qHist(ld.key), gens = GEN[ld.key] || [], made = [], usedGen = [], ids = {}, n = ld.size || 5, nFresh = Math.min(n - 1, gens.length ? 4 : 0);
    var levels = shuffled([0, 1, 2, Math.floor(Math.random() * 3)]);
    for (var k = 0; k < nFresh; k++) {
      var best = null, bestScore = -1;
      // try every generator in a fresh order: prefer one not used yet in this quiz, and a question not asked recently
      var order = shuffled(gens.slice());
      for (var t = 0; t < 30; t++) {
        var g = order[t % order.length]; QLEVEL = levels[k]; LVUSED = false;
        var q = null; try { q = g(); } catch (e) { q = null; }
        if (!q || ids[qid(q)]) continue;
        var score = (usedGen.indexOf(g) < 0 ? 2 : 0) + (hist.indexOf(qid(q)) < 0 ? 3 : 0);
        if (score > bestScore) { best = q; best._g = g; best.level = LVUSED ? levels[k] : null; bestScore = score; }
        if (score === 5) break;
      }
      if (!best) continue;
      if (typeof best.step !== 'number') best.step = (GEN_STEPS[ld.key] || [])[gens.indexOf(best._g)];
      made.push(best); usedGen.push(best._g); ids[qid(best)] = 1;
    }
    QLEVEL = 1;
    // the hand-written ones: whichever was asked longest ago (never asked counts as oldest)
    var hand = ld.quiz.map(function (q, i) { var at = hist.lastIndexOf(qid(q)); return { q: q, at: at < 0 ? -1 - Math.random() : at, i: i }; })
      .sort(function (a, b) { return a.at - b.at; }).slice(0, n - made.length).map(function (x) { return x.q; });
    var all = shuffled(made.concat(hand));
    qHist(ld.key, all.map(qid));
    return all.map(function (q) {
      var order = shuffled(q.options.map(function (o, i) { return i; }));
      var st = typeof q.step === 'number' ? q.step : (Q_STEPS[ld.key] || [])[ld.quiz.indexOf(q)];
      return { text: q.text, code: q.code, pic: q.pic, snd: q.snd, gap: q.gap, level: q.level, options: order.map(function (i) { return q.options[i]; }), why: order.map(function (i) { return q.why[i]; }), answer: order.indexOf(q.answer), step: st };
    });
  }
  function makeQuiz(ld) {
    if (ld.fresh) return makeCourseQuiz(ld);
""")
# level badge next to "Question 1 of 5"
rep("    document.getElementById('qTag').textContent = 'Question ' + (qi + 1) + ' of ' + Q.length + (done ? ' · your answer' : '');",
    "    document.getElementById('qTag').textContent = 'Question ' + (qi + 1) + ' of ' + Q.length + (typeof q.level === 'number' ? ' · ' + ['⭐ Easy', '⭐⭐ Medium', '⭐⭐⭐ Hard'][q.level] : '') + (done ? ' · your answer' : '');")

# ---------------- read aloud: the narrator's voice when the device has it, and the options as A, B, C ----------------
a = s.index("  function hearQ(q) {"); b = s.index("  document.getElementById('qHear').addEventListener")
s = s[:a] + r"""  // the clearest voice on this device: the narrator's own (Microsoft Prabhat / Ryan, on Edge and Windows), else another
  // natural Indian or British English voice, else any English voice
  function pickVoice() {
    if (!hasTTS) return null;
    var vs = speechSynthesis.getVoices() || [], want = profile.narrator === 'ryan' ? 'ryan' : 'prabhat', lang = want === 'ryan' ? 'en-GB' : 'en-IN';
    function f(test) { for (var i = 0; i < vs.length; i++) if (test(vs[i])) return vs[i]; return null; }
    return f(function (v) { return v.name.toLowerCase().indexOf(want) >= 0; }) ||
      f(function (v) { return v.lang.replace('_', '-') === lang && /natural|online|neural/i.test(v.name); }) ||
      f(function (v) { return v.lang.replace('_', '-') === lang && /google/i.test(v.name); }) ||
      f(function (v) { return v.lang.replace('_', '-') === lang; }) ||
      f(function (v) { return /^en[-_](IN|GB)/.test(v.lang) && /natural|online|google/i.test(v.name); }) ||
      f(function (v) { return /^en/.test(v.lang); });
  }
  function speakText(t) { return t.replace(/<[^>]+>/g, ' ').replace(/[\u{1F000}-\u{1FFFF}☀-➿️‍]/gu, '').replace(/_+/g, ' blank ').replace(/₹\s?(\d+)/g, '$1 rupees').replace(/×/g, ' times ').replace(/÷/g, ' shared by ').replace(/−/g, ' minus ').replace(/\s+/g, ' ').trim(); }
  function hearQ(q) {
    if (q.snd) { playPhon(q.snd, q.gap); return; }
    if (!hasTTS) return;
    try {
      speechSynthesis.cancel();
      var v = pickVoice(), parts = [speakText(q.text)].concat(q.options.map(function (o, i) { return 'Option ' + 'ABCD'[i] + '. ' + speakText(o) + '.'; }));
      parts.forEach(function (t) { // one sentence at a time, so each option gets its own clear pause
        var u = new SpeechSynthesisUtterance(t); if (v) { u.voice = v; u.lang = v.lang; } else u.lang = profile.narrator === 'ryan' ? 'en-GB' : 'en-IN';
        u.rate = 0.86; u.pitch = 1; speechSynthesis.speak(u);
      });
    } catch (e) {}
  }
""" + s[b:]

# ---------------- the prize wheel: where it stops, how many turns and how long all vary ----------------
rep("    var list = prizeList(), n = list.length, pick = Math.floor(Math.random() * n), seg = 360 / n;",
    "    // a fair, lively spin: the prize, the spot inside its slice, the number of turns and the time all vary (crypto random when the browser has it)\n    function rnd() { try { var a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] / 4294967296; } catch (e) { return Math.random(); } }\n    var list = prizeList(), n = list.length, pick = Math.floor(rnd() * n), seg = 360 / n, turns = 4 + Math.floor(rnd() * 4), secs = 3.5 + rnd() * 1.5;")
rep("    wheelAngle = base + 360 * 5 + target + (Math.random() - 0.5) * seg * 0.6;", "    wheelAngle = base + 360 * turns + target + (rnd() - 0.5) * seg * 0.84;")
rep("    g.style.transition = still ? 'none' : 'transform 4s cubic-bezier(.15,.75,.15,1)';", "    g.style.transition = still ? 'none' : 'transform ' + secs.toFixed(2) + 's cubic-bezier(.15,.75,.15,1)';")
rep("    }, still ? 50 : 4100);\n  });", "    }, still ? 50 : secs * 1000 + 100);\n  });")

# ---------------- embers the puzzle can spend (the puzzle runs in the house / world frame) ----------------
rep("  window.addEventListener('message', function (e) { var f = document.getElementById('houseFrame'); if (f && e.source === f.contentWindow && e.data && e.data.cq === 'home') show('home'); });",
r"""  window.addEventListener('message', function (e) {
    var f = document.getElementById('houseFrame'); if (!f || e.source !== f.contentWindow || !e.data) return;
    if (e.data.cq === 'home') show('home');
    // the puzzle asks how many embers there are, and spends some to place a piece
    if (e.data.cq === 'embers?') f.contentWindow.postMessage({ cq: 'embers', n: state.embers }, '*');
    if (e.data.cq === 'spend' && typeof e.data.n === 'number' && e.data.n > 0 && e.data.n <= 100) {
      var ok = state.embers >= e.data.n; if (ok) { state.embers -= e.data.n; saveProgress(); }
      f.contentWindow.postMessage({ cq: 'spent', ok: ok, n: state.embers, id: e.data.id }, '*');
    }
  });""")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
