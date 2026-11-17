# First-run welcome (name, age, pick your adventure), one course on Home, "My courses" in Me,
# and picture cards for the courses (welcome, Courses screen).
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- styles ----------------
rep("#houseFrame { flex: 1;", r"""/* ---- course picture cards (welcome, Courses, My courses) ---- */
.cq-cards { display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); width: 100%; }
.cq-card { position: relative; display: flex; flex-direction: column; text-align: left; border: 0; border-radius: 24px; padding: 0; overflow: hidden; color: #2A1330; background: linear-gradient(160deg, var(--c1), var(--c2)); box-shadow: 0 10px 24px rgba(0,0,0,.35); cursor: pointer; font: inherit; transition: transform .15s, box-shadow .15s, outline-color .15s; outline: 4px solid transparent; outline-offset: 3px; }
.cq-card:hover { transform: translateY(-3px); box-shadow: 0 14px 30px rgba(0,0,0,.45); }
.cq-card:focus-visible, .cq-card[aria-pressed="true"] { outline-color: #7CF5C8; }
.cq-card .scene { height: 124px; position: relative; display: grid; place-items: center; font-size: 66px; background: radial-gradient(circle at 50% 130%, rgba(255,255,255,.6), transparent 62%); }
.cq-card .scene .main { filter: drop-shadow(0 6px 8px rgba(0,0,0,.25)); }
.cq-card .scene .b { position: absolute; font-size: 28px; animation: cqFloat 3.2s ease-in-out infinite; }
.cq-card .scene .b1 { left: 12%; top: 18%; } .cq-card .scene .b2 { right: 12%; top: 14%; animation-delay: .7s; } .cq-card .scene .b3 { left: 22%; bottom: 8%; animation-delay: 1.4s; } .cq-card .scene .b4 { right: 20%; bottom: 10%; animation-delay: 2s; }
@keyframes cqFloat { 50% { transform: translateY(-7px) rotate(-4deg); } }
.cq-card .body { flex: 1; padding: 12px 16px 16px; background: rgba(255,246,236,.94); }
.cq-card .k { font-size: 12px; font-weight: 900; letter-spacing: .08em; text-transform: uppercase; opacity: .6; }
.cq-card h3 { margin: 2px 0 4px; font-family: var(--font-display); font-weight: 400; font-size: 25px; line-height: 1.1; }
.cq-card p { margin: 0 0 10px; font-weight: 700; font-size: 14px; line-height: 1.35; opacity: .85; }
.cq-card .tags { display: flex; flex-wrap: wrap; gap: 5px; }
.cq-card .tags span { padding: 4px 9px; border-radius: 999px; background: rgba(42,19,48,.08); font-weight: 800; font-size: 12px; }
.cq-card .ribbon { position: absolute; top: 12px; left: 12px; z-index: 1; background: #FFE07A; color: #2A1330; font-weight: 900; font-size: 12px; padding: 5px 11px; border-radius: 999px; box-shadow: 0 3px 8px rgba(0,0,0,.25); }
.cq-card .ribbon.here { background: #7CF5C8; }
.cq-card.dim { filter: saturate(.4); opacity: .78; }
.cq-card .bar { height: 8px; border-radius: 8px; background: rgba(42,19,48,.12); overflow: hidden; margin-top: 10px; } .cq-card .bar i { display: block; height: 100%; background: #2F8F6B; border-radius: 8px; }
@media (prefers-reduced-motion: reduce) { .cq-card .scene .b { animation: none; } }
/* ---- first-run welcome ---- */
#welcome { background: radial-gradient(circle at 50% 0%, #5B3A8C 0%, #2A1340 55%, #170A24 100%); color: var(--cream, #FFF6EC); overflow: auto; }
.wl { min-height: 100%; max-width: 960px; margin: 0 auto; padding: max(24px, env(safe-area-inset-top)) 18px 32px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center; }
.wl-nibb { width: 120px; height: 110px; animation: cqFloat 3.4s ease-in-out infinite; }
.wl-step { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 14px; animation: wlIn .35s ease-out; }
.wl-step[hidden] { display: none; }
@keyframes wlIn { from { opacity: 0; transform: translateY(12px); } }
.wl h1 { margin: 0; font-family: var(--font-display); font-weight: 400; font-size: clamp(28px, 6vw, 40px); line-height: 1.1; }
.wl p { margin: 0; font-weight: 700; opacity: .8; font-size: 16px; }
.wl input { width: min(340px, 100%); padding: 16px 18px; border-radius: 18px; border: 2.5px solid rgba(255,246,236,.3); background: rgba(255,255,255,.08); color: inherit; font: inherit; font-size: 22px; font-weight: 800; text-align: center; }
.wl input:focus { outline: none; border-color: #FFB547; }
.wl .cta { width: min(340px, 100%); }
.wl-ages { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; width: min(380px, 100%); }
.wl-ages button { aspect-ratio: 1; border-radius: 50%; border: 0; background: rgba(255,255,255,.1); color: inherit; font: inherit; font-size: 24px; font-weight: 900; cursor: pointer; transition: transform .12s, background .12s; }
.wl-ages button:hover, .wl-ages button:focus-visible { background: #FFB547; color: #2A1330; transform: scale(1.06); }
.wl-back { background: none; border: 0; color: inherit; opacity: .7; font: inherit; font-weight: 800; text-decoration: underline; cursor: pointer; padding: 6px; }
/* ---- Home: the course you are on, and a switch when you have joined more than one ---- */
.course-now { display: flex; align-items: center; gap: 10px; margin: 0 0 12px; position: relative; }
.course-now .cn-ic { width: 44px; height: 44px; border-radius: 14px; display: grid; place-items: center; font-size: 26px; background: linear-gradient(160deg, var(--c1), var(--c2)); box-shadow: 0 4px 10px rgba(0,0,0,.3); }
.course-now .cn-t { flex: 1; min-width: 0; }
.course-now .cn-t b { display: block; font-family: var(--font-display); font-weight: 400; font-size: 20px; line-height: 1.1; }
.course-now .cn-t span { font-size: 13px; font-weight: 800; opacity: .75; }
.course-now .cn-sw { flex: 0 0 auto; padding: 8px 12px; border-radius: 999px; border: 1.5px solid rgba(255,255,255,.25); background: rgba(0,0,0,.25); color: inherit; font: inherit; font-weight: 800; font-size: 13px; cursor: pointer; }
.cn-menu { position: absolute; right: 0; top: 52px; z-index: 30; min-width: 220px; background: var(--sheet-bg, #2A1340); border: 1.5px solid var(--line, rgba(255,255,255,.2)); border-radius: 16px; padding: 6px; box-shadow: 0 12px 30px rgba(0,0,0,.45); display: flex; flex-direction: column; }
.cn-menu[hidden] { display: none; }
.cn-menu button { display: flex; align-items: center; gap: 10px; padding: 10px; border: 0; border-radius: 10px; background: none; color: inherit; font: inherit; font-weight: 800; text-align: left; cursor: pointer; }
.cn-menu button:hover, .cn-menu button[aria-current] { background: rgba(255,255,255,.08); }
.cn-menu button span { margin-left: auto; font-size: 12px; opacity: .7; }
/* ---- Me: my courses ---- */
.my-courses { display: flex; flex-direction: column; gap: 8px; }
.my-courses .mc { display: flex; align-items: center; gap: 10px; padding: 10px; border-radius: 16px; background: rgba(255,255,255,.05); }
.my-courses .mc .cn-ic { width: 40px; height: 40px; border-radius: 12px; display: grid; place-items: center; font-size: 22px; background: linear-gradient(160deg, var(--c1), var(--c2)); flex: 0 0 auto; }
.my-courses .mc .t { flex: 1; min-width: 0; } .my-courses .mc .t b { display: block; } .my-courses .mc .t span { font-size: 13px; opacity: .75; font-weight: 700; }
#houseFrame { flex: 1;""")

# ---------------- markup ----------------
rep("      <div class=\"course-tabs\" id=\"courseTabs\" role=\"group\" aria-label=\"Course\"></div>",
    "      <div class=\"course-now\" id=\"courseTabs\" aria-label=\"Your course\"></div>")
rep("  <section class=\"screen\" id=\"me\" aria-label=\"Me\" hidden>",
r"""  <!-- ================= WELCOME (first visit): name, age, pick your adventure ================= -->
  <section class="screen" id="welcome" aria-label="Welcome" hidden>
    <div class="wl">
      <svg class="wl-nibb" id="wlNibb" data-nibb data-mood="happy" viewBox="0 0 120 110" aria-hidden="true"></svg>
      <div class="wl-step" id="wlName">
        <h1>Hi! I'm Nibb.</h1>
        <p>I'll be your teacher. What's your name?</p>
        <input id="wlNameIn" maxlength="16" autocomplete="nickname" placeholder="Type your name" aria-label="Your name">
        <button class="cta" id="wlNameGo" type="button" disabled>Next</button>
      </div>
      <div class="wl-step" id="wlAge" hidden>
        <h1 id="wlAgeH">How old are you?</h1>
        <p>So I can pick the right lessons for you.</p>
        <div class="wl-ages" id="wlAges" role="group" aria-label="Your age"></div>
        <button class="wl-back" type="button" data-wl="wlName">Back</button>
      </div>
      <div class="wl-step" id="wlPick" hidden>
        <h1>Pick your adventure!</h1>
        <p>Every lesson you finish builds part of your world.</p>
        <div class="cq-cards" id="wlCards"></div>
        <button class="cta" id="wlGo" type="button" disabled>Pick a course</button>
        <button class="wl-back" type="button" data-wl="wlAge">Back</button>
      </div>
    </div>
  </section>

  <section class="screen" id="me" aria-label="Me" hidden>""")
rep("""        <section class="panel" aria-labelledby="prizeH">""",
"""        <section class="panel" aria-labelledby="myCoursesH">
          <h2 class="sub-h" id="myCoursesH">My courses</h2>
          <div class="my-courses" id="myCourses"></div>
        </section>
        <section class="panel" aria-labelledby="prizeH">""")

# ---------------- script ----------------
rep("  var screens = ['home', 'house', 'courses', 'cards', 'me', 'learn', 'quiz', 'qresult', 'done'];",
    "  var screens = ['home', 'house', 'courses', 'cards', 'me', 'learn', 'quiz', 'qresult', 'done', 'welcome'];")
# first visit: no profile and no progress saved yet
rep("  function saveProfile() { try { localStorage.setItem('cq-profile', JSON.stringify(profile)); } catch (e) {} }",
r"""  var FIRST_RUN = false; try { FIRST_RUN = !localStorage.getItem('cq-profile') && !localStorage.getItem('cq-progress'); } catch (e) {}
  // the courses this learner has joined (Home shows the current one; Me lists them all)
  profile.courses = null;
  try { var pfc = JSON.parse(localStorage.getItem('cq-profile') || 'null'); if (pfc && Array.isArray(pfc.courses)) profile.courses = pfc.courses.filter(function (c) { return c === 'py' || c === 'maths' || c === 'english'; }); } catch (e) {}
  function saveProfile() { try { localStorage.setItem('cq-profile', JSON.stringify(profile)); } catch (e) {} }""")
# the course cards
rep("  var PY_LEVELS = [",
r"""  // how each course looks on its picture card
  var CQ_COURSES = {
    py:      { emoji: '🏠', name: 'Python', world: 'Build your dream house', tag: 'Real code, one room at a time', builds: ['🛋️', '🪜', '🌻', '💡'], c1: '#FFC861', c2: '#FF7A6B', minAge: 8, maxAge: 18, extra: '4 levels' },
    maths:   { emoji: '🏙️', name: 'Maths', world: 'Grow Number Town', tag: 'Count, share and shop on Market Street', builds: ['🍎', '🧱', '🕰️', '🪙'], c1: '#C3A6FF', c2: '#7C5CE0', minAge: 6, maxAge: 9, extra: 'Grade 2' },
    english: { emoji: '📚', name: 'English', world: 'Fill the Story Library', tag: 'Letter sounds, words and stories', builds: ['🔤', '📖', '🎭', '🐱'], c1: '#FFB0D8', c2: '#E0569A', minAge: 5, maxAge: 9, extra: 'Phonics first' }
  };
  function courseFits(cid) { var m = CQ_COURSES[cid]; return profile.age >= m.minAge && profile.age <= m.maxAge; }
  function courseTotal(cid) { var P = cid === 'py' ? PY_PACK : COURSE_PACKS[cid]; return P.floorAt[P.floorAt.length - 1]; }
  // a big picture card; mode 'pick' (welcome), 'go' (Courses screen)
  function courseCard(cid, mode) {
    var m = CQ_COURSES[cid], b = document.createElement('button'), n = courseTotal(cid), done = mode === 'pick' ? 0 : Math.min(doneIn(cid), n);
    var joined = (profile.courses || []).indexOf(cid) >= 0, fit = courseFits(cid);
    b.type = 'button'; b.className = 'cq-card' + (fit || joined ? '' : ' dim'); b.dataset.c = cid;
    b.style.setProperty('--c1', m.c1); b.style.setProperty('--c2', m.c2);
    var ribbon = mode !== 'pick' && COURSE === cid ? '<span class="ribbon here">You are here</span>' : fit ? '<span class="ribbon">⭐ Perfect for you</span>' : '';
    b.innerHTML = ribbon + '<div class="scene" aria-hidden="true"><span class="main">' + m.emoji + '</span>' + m.builds.map(function (x, i) { return '<span class="b b' + (i + 1) + '">' + x + '</span>'; }).join('') + '</div>' +
      '<div class="body"><div class="k">' + m.name + '</div><h3>' + m.world + '</h3><p>' + m.tag + '</p><div class="tags"><span>' + n + ' lessons</span><span>' + m.extra + '</span><span>' + (m.maxAge >= 18 ? 'Age ' + m.minAge + '+' : 'Age ' + m.minAge + '–' + m.maxAge) + '</span></div>' +
      (mode !== 'pick' && joined ? '<div class="bar" aria-hidden="true"><i style="width:' + Math.round(done / n * 100) + '%"></i></div>' : '') + '</div>';
    b.setAttribute('aria-label', m.name + ': ' + m.world + '. ' + n + ' lessons. ' + (fit ? 'Perfect for your age.' : 'For age ' + m.minAge + (m.maxAge >= 18 ? ' and up.' : ' to ' + m.maxAge + '.')) + (mode !== 'pick' && joined ? ' ' + done + ' of ' + n + ' done.' : ''));
    return b;
  }
  // join a course (if new) and make it the one on Home
  function joinCourse(cid) {
    if (!profile.courses) profile.courses = [];
    if (profile.courses.indexOf(cid) < 0) profile.courses.push(cid);
    saveProfile(); useCourse(cid);
  }
  var PY_LEVELS = [""")
# Courses screen: picture cards instead of the plain list
a = s.index("    // the live courses, each with its levels: Python's four floors, a grade per street for Maths and English")
b = s.index("    // more courses for this age, then the ones for older learners")
s = s[:a] + r"""    // the live courses as picture cards: tap one to go to it (joining it if it is new)
    body.appendChild(el('p', 'muted small', 'Tap a course to go to it. Your progress in each course is kept.'));
    var cards = el('div', 'cq-cards');
    ['py', 'maths', 'english'].sort(function (x, y) { return (courseFits(y) - courseFits(x)); }).forEach(function (cid) {
      var c = courseCard(cid, 'go'); c.addEventListener('click', function () { joinCourse(cid); show('home'); }); cards.appendChild(c);
    });
    body.appendChild(cards);
""" + s[b:]
# Home: the current course, and a switch menu when more than one is joined
a = s.index("  function renderCourseTabs() {")
b = s.index("\n  }", s.index("row.appendChild(b);", a)) + 4
s = s[:a] + r"""  function renderCourseTabs() {
    var row = document.getElementById('courseTabs'); if (!row || !COURSE_PACKS || !PY_PACK || !COURSE) return;
    var m = CQ_COURSES[COURSE], n = courseTotal(COURSE), joined = (profile.courses || [COURSE]).filter(function (c) { return CQ_COURSES[c]; });
    row.style.setProperty('--c1', m.c1); row.style.setProperty('--c2', m.c2);
    row.innerHTML = '<span class="cn-ic" aria-hidden="true">' + m.emoji + '</span><span class="cn-t"><b></b><span></span></span>' +
      (joined.length > 1 ? '<button class="cn-sw" type="button" aria-haspopup="true" aria-expanded="false">⇄ Switch</button><div class="cn-menu" role="menu" hidden></div>' : '');
    row.querySelector('.cn-t b').textContent = m.world;
    row.querySelector('.cn-t span').textContent = m.name + ' · ' + Math.min(state.current, n) + ' of ' + n + ' lessons';
    var sw = row.querySelector('.cn-sw'); if (!sw) return;
    var menu = row.querySelector('.cn-menu');
    joined.forEach(function (cid) {
      var mm = CQ_COURSES[cid], it = document.createElement('button'); it.type = 'button'; it.setAttribute('role', 'menuitem');
      if (cid === COURSE) it.setAttribute('aria-current', 'true');
      it.innerHTML = mm.emoji + ' ' + mm.name + '<span>' + Math.min(doneIn(cid), courseTotal(cid)) + '/' + courseTotal(cid) + '</span>';
      it.addEventListener('click', function () { menu.hidden = true; if (cid !== COURSE) { useCourse(cid); refreshHome(); } });
      menu.appendChild(it);
    });
    sw.addEventListener('click', function (e) { e.stopPropagation(); menu.hidden = !menu.hidden; sw.setAttribute('aria-expanded', String(!menu.hidden)); });
    document.addEventListener('click', function close() { menu.hidden = true; document.removeEventListener('click', close); });
  }
  // Me: every course, joined ones first, with Switch or Add
  function renderMyCourses() {
    var box = document.getElementById('myCourses'); if (!box || !COURSE) return; box.innerHTML = '';
    var all = ['py', 'maths', 'english'], joined = profile.courses || [COURSE];
    all.sort(function (x, y) { return (joined.indexOf(y) >= 0) - (joined.indexOf(x) >= 0); }).forEach(function (cid) {
      var m = CQ_COURSES[cid], n = courseTotal(cid), on = joined.indexOf(cid) >= 0, row = document.createElement('div');
      row.className = 'mc'; row.style.setProperty('--c1', m.c1); row.style.setProperty('--c2', m.c2);
      row.innerHTML = '<span class="cn-ic" aria-hidden="true">' + m.emoji + '</span><span class="t"><b>' + m.name + ' · ' + m.world + '</b><span>' + (on ? Math.min(doneIn(cid), n) + ' of ' + n + ' lessons' : n + ' lessons · ' + (courseFits(cid) ? '⭐ perfect for your age' : 'age ' + m.minAge + (m.maxAge >= 18 ? '+' : '–' + m.maxAge))) + '</span></span>';
      var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'chip-btn' + (cid === COURSE ? ' ghost' : '');
      btn.textContent = cid === COURSE ? 'Current' : on ? 'Switch' : '+ Add';
      btn.disabled = cid === COURSE;
      btn.addEventListener('click', function () { joinCourse(cid); show('home'); });
      row.appendChild(btn); box.appendChild(row);
    });
  }""" + s[b:]
rep("  function renderMe() {", "  function renderMe() {\n    renderMyCourses();")
# useCourse also records the course as joined
rep("    var P = id === 'py' ? PY_PACK : COURSE_PACKS[id];\n    COURSE = id;",
    "    var P = id === 'py' ? PY_PACK : COURSE_PACKS[id];\n    if (profile.courses && profile.courses.indexOf(id) < 0) { profile.courses.push(id); saveProfile(); }\n    COURSE = id;")

# ---------------- welcome flow, and start-up ----------------
rep("  show('home');\n})();",
r"""  // ---- first visit: name, age, then pick your adventure ----
  function wlStep(id) { ['wlName', 'wlAge', 'wlPick'].forEach(function (s2) { document.getElementById(s2).hidden = s2 !== id; }); var f = document.querySelector('#' + id + ' input, #' + id + ' button'); if (f) setTimeout(function () { f.focus(); }, 50); }
  var wlChoice = null;
  function startWelcome() {
    document.getElementById('wlNibb').innerHTML = lumiSVG('happy');
    var ages = document.getElementById('wlAges'); ages.innerHTML = '';
    for (var a = 5; a <= 18; a++) (function (age) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = age === 18 ? '18+' : age; b.setAttribute('aria-label', age === 18 ? '18 or older' : age + ' years old');
      b.addEventListener('click', function () { profile.age = age; saveProfile(); renderPick(); wlStep('wlPick'); });
      ages.appendChild(b);
    })(a);
    show('welcome'); wlStep('wlName');
  }
  function renderPick() {
    var box = document.getElementById('wlCards'); box.innerHTML = ''; wlChoice = null;
    var go = document.getElementById('wlGo'); go.disabled = true; go.textContent = 'Pick a course';
    ['maths', 'english', 'py'].sort(function (x, y) { return courseFits(y) - courseFits(x); }).forEach(function (cid) {
      var c = courseCard(cid, 'pick');
      c.setAttribute('aria-pressed', 'false');
      c.addEventListener('click', function () {
        wlChoice = cid; box.querySelectorAll('.cq-card').forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
        go.disabled = false; go.textContent = 'Let\'s go: ' + CQ_COURSES[cid].world + '!';
      });
      box.appendChild(c);
    });
  }
  var wlIn = document.getElementById('wlNameIn');
  wlIn.addEventListener('input', function () { document.getElementById('wlNameGo').disabled = !wlIn.value.trim(); });
  function wlName() { var nm = wlIn.value.replace(/[\u0000-\u001f<>]/g, '').trim().slice(0, 16); if (!nm) return; profile.name = nm; saveProfile(); applyProfile(); document.getElementById('wlAgeH').textContent = 'How old are you, ' + nm + '?'; wlStep('wlAge'); }
  document.getElementById('wlNameGo').addEventListener('click', wlName);
  wlIn.addEventListener('keydown', function (e) { if (e.key === 'Enter') wlName(); });
  document.querySelectorAll('[data-wl]').forEach(function (b) { b.addEventListener('click', function () { wlStep(b.getAttribute('data-wl')); }); });
  document.getElementById('wlGo').addEventListener('click', function () {
    if (!wlChoice) return;
    profile.courses = []; joinCourse(wlChoice); profile.onboarded = true; saveProfile(); saveProgress(); show('home');
  });
  // learners from before this screen existed: their joined courses are the ones with progress, plus the one on screen
  if (!profile.courses && !FIRST_RUN) {
    profile.courses = ['py', 'maths', 'english'].filter(function (c) { return c === COURSE || doneIn(c) > 0; });
    saveProfile();
  }
  if (FIRST_RUN) startWelcome(); else show('home');
})();""")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
