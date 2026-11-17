# Course switch: Python, Maths and English in one app, each with its own progress.
# Python keeps 'cq-progress' (the House reads it); Maths and English live in 'cq-courses'.
import json, re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:90])
    s = s.replace(a, b)

# --- saving: Python's lesson in cq-progress, the other courses in cq-courses ---
rep("  function saveProgress() { try { localStorage.setItem('cq-progress', JSON.stringify({ v: SAVE_VERSION, current: state.current,",
    "  function saveProgress() { try { if (COURSE) localStorage.setItem('cq-courses', JSON.stringify(courseSave())); localStorage.setItem('cq-progress', JSON.stringify({ v: SAVE_VERSION, current: pyCurrent(),")
rep("    ['cq-progress', 'cq-iso', 'cq-cards'].forEach(", "    ['cq-progress', 'cq-iso', 'cq-cards', 'cq-courses'].forEach(")

# --- floors: work for any course (Python has 4, Maths and English one street each for now) ---
rep("  function floorOf(i) { return i < FLOOR1 ? 1 : i < FLOOR2 ? 2 : i < FLOOR3 ? 3 : 4; }\n  function unlockedFloors() { return [1, 2, 3, 4].filter(function (f) { return state.current >= FLOOR_AT[f - 1]; }); }",
    "  function floorOf(i) { for (var f = 1; f < FLOOR_AT.length - 1; f++) if (i < FLOOR_AT[f]) return f; return FLOOR_AT.length - 1; }\n  function unlockedFloors() { return FLOOR_NAMES.map(function (n, i) { return i + 1; }).filter(function (f) { return state.current >= FLOOR_AT[f - 1]; }); }")

# --- topic icons: an emoji tile ---
rep("    if (key.indexOf('tx:') === 0) { // floor 2: a little code card with the topic's key symbol",
    "    if (key.indexOf('em:') === 0) return '<svg class=\"ti\" width=\"44\" height=\"44\" viewBox=\"0 0 44 44\" aria-hidden=\"true\"><text x=\"22\" y=\"31\" text-anchor=\"middle\" font-size=\"25\">' + key.slice(3) + '</text></svg>';\n"
    "    if (key.indexOf('tx:') === 0) { // floor 2: a little code card with the topic's key symbol")

# --- cards: each card belongs to a course; it joins your deck once that course's lesson is done ---
rep("    CARDS.forEach(function (c) { if (c.l < state.current && !cardState[c.id]) {",
    "    CARDS.forEach(function (c) { if (c.l < doneIn(c.cr || 'py') && !cardState[c.id]) {")
rep("    { id: 'bugs',  name: 'Bug spotting',",
    "    { id: 'g2m',   name: 'Maths',             note: 'Grade 2: Market Street',            bg: '#C3A6FF', ic: '<path d=\"M5 12h14M12 5v14\"/>' },\n"
    "    { id: 'g2e',   name: 'English',           note: 'Grade 2: Picture-book Corner',      bg: '#FF8FC7', ic: '<path d=\"M4 19V6a2 2 0 0 1 2-2h12v15H6a2 2 0 0 0-2 2\"/>' },\n"
    "    { id: 'bugs',  name: 'Bug spotting',")

# --- home: the course tile, the finished-course card, a Room/Lesson eyebrow per course ---
rep("    document.getElementById('cardEyebrow').textContent = FLOOR_NAMES[cf - 1] + ' · ' + (boss ? 'Master Builder' : 'Room ' + (ci - f0 + 1) + ' of ' + (f1 - f0 - 1));",
    "    document.getElementById('cardEyebrow').textContent = FLOOR_NAMES[cf - 1] + ' · ' + (boss ? (COURSE === 'py' ? 'Master Builder' : 'Challenge') : (COURSE === 'py' ? 'Room ' : 'Lesson ') + (ci - f0 + 1) + ' of ' + (f1 - f0 - 1));")
rep("    if (state.current >= ALL_LESSONS) { // the garden's Master Builder challenge is done: the whole Python course",
    "    if (state.current >= ALL_LESSONS && COURSE !== 'py') { // a whole grade of Maths or English is done\n"
    "      var CP = COURSE_PACKS[COURSE];\n"
    "      if (bt) bt.textContent = 'whole grade';\n"
    "      document.getElementById('cardEyebrow').textContent = FLOOR_NAMES[FLOOR_NAMES.length - 1] + ' · complete';\n"
    "      document.getElementById('cardTitle').textContent = 'You finished ' + CP.grade + ' ' + CP.name + '!';\n"
    "      document.getElementById('cardText').textContent = 'Every lesson done, and ' + CP.place + ' has grown with you. Visit it, or replay any lesson from the path below. ' + CP.grade.replace('2', '3') + ' comes next.';\n"
    "      document.getElementById('ctaText').textContent = 'Visit ' + CP.place;\n"
    "    } else if (state.current >= ALL_LESSONS) { // the garden's Master Builder challenge is done: the whole Python course")
rep("    document.getElementById('pyBar').style.width = Math.round(Math.min(state.current, ALL_LESSONS) / ALL_LESSONS * 100) + '%';\n"
    "    document.getElementById('pyLevel').textContent = 'Python · ' + Math.min(state.current, ALL_LESSONS) + ' of ' + ALL_LESSONS + ' lessons';",
    "    document.getElementById('pyBar').style.width = Math.round(Math.min(state.current, ALL_LESSONS) / ALL_LESSONS * 100) + '%';\n"
    "    document.getElementById('pyLevel').textContent = courseName(COURSE) + ' · ' + Math.min(state.current, ALL_LESSONS) + ' of ' + ALL_LESSONS + ' lessons';\n"
    "    renderCourseTabs();")

# --- the House tab: Python's house, or the course's place (Number Town, Story Library) ---
rep("  function houseSeen() { try { var v = parseInt(localStorage.getItem('cq-house-seen'), 10); return isFinite(v) ? v : 0; } catch (e) { return 0; } }\n"
    "  function markHouseSeen() { try { localStorage.setItem('cq-house-seen', String(state.current)); } catch (e) {} newsDismissed = false; }",
    "  function seenKey() { return COURSE && COURSE !== 'py' ? 'cq-world-seen-' + COURSE : 'cq-house-seen'; }\n"
    "  function houseSeen() { try { var v = parseInt(localStorage.getItem(seenKey()), 10); return isFinite(v) ? v : 0; } catch (e) { return 0; } }\n"
    "  function markHouseSeen() { try { localStorage.setItem(seenKey(), String(state.current)); } catch (e) {} newsDismissed = false; }")
rep("  function renderHouseCard() {\n    var p = state.current, earned = 0, placed = 0;",
    "  function renderHouseCard() {\n    if (COURSE && COURSE !== 'py') { houseWaiting = 0; return 0; } // only the house has items to place\n    var p = pyCurrent(), earned = 0, placed = 0;")
rep("    if (id === 'house') { markHouseSeen(); document.getElementById('houseFrame').src = 'house.html?v=' + state.current + (pendingBuild !== null ? '&build=' + pendingBuild : ''); pendingBuild = null; }",
    "    if (id === 'house') { markHouseSeen(); document.getElementById('houseFrame').src = (COURSE === 'py' ? 'house.html?v=' : 'world.html?course=' + COURSE + '&v=') + state.current + (pendingBuild !== null ? '&build=' + pendingBuild : ''); pendingBuild = null; }")
rep("      nav.querySelectorAll('button').forEach(function (b) { if (b.getAttribute('data-nav') === active)",
    "      var hb = nav.querySelector('[data-nav=\"house\"]'); if (hb && hb.lastChild) hb.lastChild.textContent = COURSE === 'maths' ? 'Town' : COURSE === 'english' ? 'Library' : 'House';\n"
    "      nav.querySelectorAll('button').forEach(function (b) { if (b.getAttribute('data-nav') === active)")

# --- done screen: only Python lessons earn furniture ---
rep("    var ern = EARNS[openLessonIdx] || [],", "    var ern = (COURSE === 'py' && EARNS[openLessonIdx]) || [],")

# --- quiz: pictures, sounds, 2 to 4 options, no empty code box, and a read-aloud button ---
rep("        q.step = (GEN_STEPS[ld.key] || [])[GEN[ld.key].indexOf(gens[g])]; made.push(q);",
    "        if (typeof q.step !== 'number') q.step = (GEN_STEPS[ld.key] || [])[GEN[ld.key].indexOf(gens[g])]; made.push(q);")
rep("      return { text: q.text, code: q.code, options: order.map(function (i) { return q.options[i]; }), why: order.map(function (i) { return q.why[i]; }), answer: order.indexOf(q.answer), step: st };",
    "      return { text: q.text, code: q.code, pic: q.pic, snd: q.snd, gap: q.gap, options: order.map(function (i) { return q.options[i]; }), why: order.map(function (i) { return q.why[i]; }), answer: order.indexOf(q.answer), step: st };")
rep("    document.getElementById('qCode').innerHTML = q.code;",
    "    document.getElementById('qCode').innerHTML = q.code; document.getElementById('qCode').hidden = !q.code;\n"
    "    var qp = document.getElementById('qPic'); qp.innerHTML = q.pic || ''; qp.hidden = !q.pic; qp.classList.toggle('long', !!q.pic && q.pic.replace(/<[^>]+>/g, '').length > 14);\n"
    "    var qh = document.getElementById('qHear'); qh.hidden = COURSE === 'py'; qh.textContent = q.snd ? '🔊 Hear it again' : '🔊 Read it to me';\n"
    "    if (q.snd && !done) setTimeout(function () { if (Q[qi] === q) hearQ(q); }, 250);")
rep("      <div class=\"code\" id=\"qCode\"></div>\n      <div class=\"options\" id=\"qOptions\"",
    "      <div class=\"q-pic\" id=\"qPic\" hidden></div>\n      <div class=\"code\" id=\"qCode\"></div>\n      <button class=\"q-hear\" id=\"qHear\" type=\"button\" hidden>🔊 Read it to me</button>\n      <div class=\"options\" id=\"qOptions\"")
rep("#houseFrame { flex: 1;",
    ".q-pic { font-size: 46px; line-height: 1.25; text-align: center; margin: 6px 0 12px; letter-spacing: 2px; white-space: pre-line; word-break: break-word; }\n"
    ".q-pic.long { font-size: 30px; }\n.q-pic s { text-decoration-thickness: 3px; }\n"
    ".q-hear { display: inline-flex; align-items: center; gap: 6px; margin: 0 0 12px; padding: 9px 14px; border-radius: 999px; border: 2px solid var(--line, rgba(255,255,255,.25)); background: transparent; color: inherit; font: inherit; font-weight: 700; cursor: pointer; }\n"
    ".course-tabs { display: flex; gap: 8px; margin: 0 0 12px; overflow-x: auto; scrollbar-width: none; }\n.course-tabs::-webkit-scrollbar { display: none; }\n"
    ".course-tabs button { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; border-radius: 999px; border: 2px solid rgba(255,255,255,.22); background: rgba(0,0,0,.18); color: inherit; font: inherit; font-weight: 700; font-size: 14px; cursor: pointer; }\n"
    ".course-tabs button[aria-pressed=\"true\"] { background: var(--cc, #FFB547); color: #2A1330; border-color: transparent; }\n"
    ".course-tabs .n { font-weight: 600; opacity: .75; font-size: 12px; }\n"
    "#houseFrame { flex: 1;")

# --- home: course chips above the lesson card ---
rep("      <article class=\"lesson-card\">", "      <div class=\"course-tabs\" id=\"courseTabs\" role=\"group\" aria-label=\"Course\"></div>\n      <article class=\"lesson-card\">")

# --- Courses screen: a big card per live course ---
a = s.index("    // the live course, with its four levels (one per floor of the house)")
b = s.index("    card.appendChild(go); body.appendChild(card);", a) + len("    card.appendChild(go); body.appendChild(card);")
s = s[:a] + r"""    // the live courses, each with its levels: Python's four floors, a grade per street for Maths and English
    ['py', 'maths', 'english'].forEach(function (cid) {
      var meta = cid === 'py' ? COURSES[0] : COURSE_PACKS[cid], P = cid === 'py' ? PY_PACK : COURSE_PACKS[cid], at = P.floorAt, done = doneIn(cid);
      var card = el('article', 'course-big');
      var head = el('div', 'cb-head'), ic = el('span', 'c-ic', meta.ic || meta.icon); ic.style.background = meta.bg;
      var ht = el('div', 'cb-t'); ht.appendChild(el('b', null, cid === 'py' ? meta.name : meta.name + ' · ' + meta.place));
      ht.appendChild(el('span', null, cid === 'py' ? meta.blurb : cid === 'maths' ? 'NCERT Maths, one street of Number Town per grade. Numbers, shapes, money and time with pictures.' : 'Phonics first, then words, sentences and stories. One wing of the Story Library per grade.'));
      head.appendChild(ic); head.appendChild(ht); card.appendChild(head);
      var lv = el('ol', 'levels-list'), levels = cid === 'py' ? PY_LEVELS : P.levels.concat([['Grades 3 to 5', cid === 'maths' ? 'Park, Railway Station, Farm' : 'Poem Garden, Story Wing, Treehouse', 'Planned: coming next']]);
      levels.forEach(function (L, i) {
        var real = i < at.length - 1, open = real && done >= at[i], lo = at[i], n = real ? at[i + 1] - at[i] : 1;
        var li = el('li', 'lvl' + (open ? ' on' : ' locked'));
        var t = el('div', 'lvl-t'); t.appendChild(el('b', null, L[0] + ' · ' + L[1])); t.appendChild(el('span', null, L[2]));
        li.appendChild(t);
        if (open) { var dn = Math.max(0, Math.min(done - lo, n)), bar = el('span', 'bar'), fill = el('i'); fill.style.width = Math.round(dn / n * 100) + '%'; bar.appendChild(fill); li.appendChild(bar); li.appendChild(el('span', 'lvl-n', dn + ' of ' + n + ' lessons')); }
        else li.appendChild(el('span', 'lvl-n', real ? 'Opens after the ' + (cid === 'py' ? FLOOR_NAME_PY[i - 1] : P.floorNames[i - 1]).toLowerCase() : 'Coming later'));
        lv.appendChild(li);
      });
      card.appendChild(lv);
      var total = at[at.length - 1], here = COURSE === cid;
      var go = el('button', 'cta', done >= total ? (cid === 'py' ? 'Visit my house' : 'Visit ' + meta.place) : (done ? 'Continue: ' : 'Start: ') + P.lessons[done].title.replace(/^the /, ''));
      go.addEventListener('click', function () { if (!here) useCourse(cid); show('home'); document.getElementById('startBtn').click(); });
      card.appendChild(go); body.appendChild(card);
    });""" + s[b:]

# --- the course switch itself, run before the first lesson opens ---
rep("  openLesson(LESSON_DATA[state.current] ? state.current : 3);\n  applyLessonPrefs(); saveProgress();",
r"""  // ================= courses: Python, Maths and English, each with its own progress =================
  // Swapping a course swaps the lesson list, lesson records, topics and floors the screens read,
  // and state.current becomes that course's next lesson. Python's progress stays in cq-progress.
  openLesson(LESSON_DATA[state.current] ? state.current : 3);
  var FLOOR_NAME_PY = FLOOR_NAMES.slice();
  var PY_PACK = { lessons: lessons, data: LESSON_DATA, topics: TOPICS, floorAt: FLOOR_AT, floorNames: FLOOR_NAMES };
  var courseDone = { py: state.current, maths: 0, english: 0 };
  try { var cs = JSON.parse(localStorage.getItem('cq-courses') || 'null');
    if (cs && typeof cs === 'object' && !Array.isArray(cs)) {
      ['maths', 'english'].forEach(function (c) { var n = cs[c], P = COURSE_PACKS[c]; if (typeof n === 'number' && n >= 0 && n <= P.lessons.length) courseDone[c] = Math.floor(n); });
      if (cs.course === 'maths' || cs.course === 'english') COURSE = cs.course;
    } } catch (e) {}
  if (!COURSE) COURSE = 'py';
  var startCourse = COURSE; COURSE = 'py'; if (startCourse !== 'py') useCourse(startCourse, true);
  if (LESSON_DATA[Math.min(state.current, ALL_LESSONS - 1)]) openLesson(Math.min(state.current, ALL_LESSONS - 1));
  applyLessonPrefs(); saveProgress();""")
rep("  var state = { current: 0, embers: 0 };",
r"""  var state = { current: 0, embers: 0 };
  var COURSE = null, courseDone = null; // the course on screen ('py', 'maths', 'english'), and each course's next lesson; set up at the end
  function pyCurrent() { return !COURSE || COURSE === 'py' ? state.current : courseDone.py; }
  function doneIn(c) { return !COURSE || c === COURSE ? (c === (COURSE || 'py') ? state.current : 0) : courseDone[c] || 0; }
  function courseSave() { var o = { course: COURSE }; ['maths', 'english'].forEach(function (c) { o[c] = doneIn(c); }); return o; }
  function courseName(c) { return c === 'py' ? 'Python' : COURSE_PACKS[c].grade + ' ' + COURSE_PACKS[c].name; }
  function useCourse(id, quiet) {
    if (id === COURSE) return;
    courseDone[COURSE] = state.current;
    var P = id === 'py' ? PY_PACK : COURSE_PACKS[id];
    COURSE = id; lessons = P.lessons; LESSON_DATA = P.data; TOPICS = P.topics; FLOOR_AT = P.floorAt; FLOOR_NAMES = P.floorNames; ALL_LESSONS = P.floorAt[P.floorAt.length - 1];
    state.current = courseDone[id]; pathFloor = null;
    var nav = document.querySelectorAll('[data-navbar] [data-nav="house"]'); nav.forEach(function (b) { if (b.lastChild) b.lastChild.textContent = id === 'maths' ? 'Town' : id === 'english' ? 'Library' : 'House'; });
    if (!quiet) { saveProgress(); if (LESSON_DATA[Math.min(state.current, ALL_LESSONS - 1)]) openLesson(Math.min(state.current, ALL_LESSONS - 1)); }
  }
  function renderCourseTabs() {
    var row = document.getElementById('courseTabs'); if (!row || !COURSE_PACKS || !PY_PACK) return;
    row.innerHTML = '';
    [['py', '🐍', 'Python', '#FFB547'], ['maths', COURSE_PACKS.maths.icon, 'Maths', COURSE_PACKS.maths.bg], ['english', COURSE_PACKS.english.icon, 'English', COURSE_PACKS.english.bg]].forEach(function (c) {
      var b = document.createElement('button'), P = c[0] === 'py' ? PY_PACK : COURSE_PACKS[c[0]], n = P.floorAt[P.floorAt.length - 1];
      b.type = 'button'; b.setAttribute('aria-pressed', COURSE === c[0] ? 'true' : 'false'); b.style.setProperty('--cc', c[3]);
      b.innerHTML = '<span aria-hidden="true">' + c[1] + '</span>' + c[2] + ' <span class="n">' + Math.min(doneIn(c[0]), n) + '/' + n + '</span>';
      b.setAttribute('aria-label', c[2] + ', ' + Math.min(doneIn(c[0]), n) + ' of ' + n + ' lessons done');
      b.addEventListener('click', function () { if (COURSE === c[0]) return; useCourse(c[0]); refreshHome(); });
      row.appendChild(b);
    });
  }""")

# --- quiz: play a question's sounds from the phonics sheet, or read it aloud with the device voice ---
rep("  function startQuiz() {",
r"""  var phonEl = new Audio(); phonEl.preload = 'auto';
  function playPhon(names, gap) {
    var who = profile.narrator === 'ryan' ? 'ryan' : 'prabhat', url = 'audio/phonics-' + who + '.mp3', i = 0, tok = {};
    playPhon.tok = tok;
    try { if (hasTTS) speechSynthesis.cancel(); } catch (e) {}
    loadClip(url).then(function (u) {
      if (phonEl._src !== u) { phonEl.src = u; phonEl._src = u; }
      (function next() {
        if (playPhon.tok !== tok || i >= names.length) return;
        var sg = PHON_SEG[names[i++]]; sg = sg && sg[who]; if (!sg) { next(); return; }
        phonEl.currentTime = sg[0]; var p = phonEl.play(); if (p && p.catch) p.catch(function () {});
        (function watch() { if (playPhon.tok !== tok) return; if (phonEl.currentTime >= sg[1] || phonEl.ended) { phonEl.pause(); setTimeout(next, gap || 150); } else requestAnimationFrame(watch); })();
      })();
    }).catch(function () {});
  }
  function hearQ(q) {
    if (q.snd) { playPhon(q.snd, q.gap); return; }
    if (!hasTTS) return;
    try { speechSynthesis.cancel(); var u = new SpeechSynthesisUtterance(q.text.replace(/_+/g, ' blank ') + ' ' + q.options.map(function (o) { return o.replace(/[\u{1F000}-\u{1FFFF}☀-➿️]/gu, ''); }).join(', or, '));
      u.lang = profile.narrator === 'ryan' ? 'en-GB' : 'en-IN'; u.rate = 0.9; speechSynthesis.speak(u); } catch (e) {}
  }
  document.getElementById('qHear').addEventListener('click', function () { if (Q && Q[qi]) hearQ(Q[qi]); });
  function startQuiz() {""")
open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
