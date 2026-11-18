# Me → "Make it easier": text size, an easy-read font, high contrast, less movement, voice speed.
# Home fixes: Start visible on a phone's first screen; news shown as a badge on the Town/House tab (the robot no longer
# lands on the lesson card); a star (not a second moon) for the streak; the Courses tile shows the course you are on;
# the Cards tile counts only categories that have cards.
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- settings: styles ----------------
rep("#houseFrame { flex: 1;", r"""/* ---- Make it easier (Me): text size, easy-read font, high contrast, less movement ---- */
body.ts-1 :is(.qtext, #qOptions .opt, .caption, #boardLines, .lesson-card, #readPane, .sheet, .tile, .course-now) { zoom: 1.12; }
body.ts-2 :is(.qtext, #qOptions .opt, .caption, #boardLines, .lesson-card, #readPane, .sheet, .tile, .course-now) { zoom: 1.25; }
body.easy-font, body.easy-font :is(button, input, select, textarea, p, span, b, h1, h2, h3, h4, li, label, div, small, strong) { font-family: 'Atkinson Hyperlegible', 'Lexend', 'Nunito', system-ui, sans-serif !important; letter-spacing: .02em; }
body.easy-font :is(.code, code, .chalk.code, .title-xl, .tile-t) { letter-spacing: 0; }
body.easy-font #board .chalk:not(.title) { font-family: 'Atkinson Hyperlegible', system-ui, sans-serif !important; font-weight: 700; }
body.hi-contrast { --muted: #FFFFFF; --line: rgba(255,255,255,.75); }
body.hi-contrast :is(.tile, .lesson-card, .panel, .opt, .sheet, .course-now, .topic, .wheel-card, .tour-card) { border: 2px solid #FFFFFF !important; background-color: #120818 !important; }
body.hi-contrast :is(.muted, .small, .lbl, .eyebrow, .meta, p) { color: #FFFFFF !important; opacity: 1 !important; }
body.hi-contrast .cta { box-shadow: 0 0 0 3px #FFFFFF !important; }
body.hi-contrast .bubble { background: #FFFFFF !important; color: #000000 !important; }
body.calm *, body.calm *::before, body.calm *::after { animation-duration: .001s !important; animation-iteration-count: 1 !important; transition-duration: .001s !important; scroll-behavior: auto !important; }
.ez-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 4px 0 10px; }
.ez-row button { padding: 8px 14px; border-radius: 999px; border: 2px solid var(--line); background: transparent; color: inherit; font: inherit; font-weight: 800; cursor: pointer; }
.ez-row button[aria-pressed="true"] { background: #FFB547; color: #2A1330; border-color: transparent; }
/* ---- Home: a badge on the House / Town / Library tab when something new was built ---- */
.nav button[data-nav="house"] { position: relative; }
.nav button.has-news::after { content: 'New!'; position: absolute; top: 2px; left: 50%; margin-left: 6px; padding: 1px 6px; border-radius: 999px; background: #7CF5C8; color: #2A1330; font-size: 10px; font-weight: 900; animation: newsPulse 1.6s ease-in-out infinite; }
@keyframes newsPulse { 50% { transform: scale(1.12); } }
/* phones: a smaller sky, so the lesson card and its Start button are on the first screen */
@media (max-width: 600px) and (min-height: 560px) { .home-hero { height: 124px; } }
#houseFrame { flex: 1;""")
rep('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Paytone+One&family=Nunito', '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Paytone+One&family=Nunito')

# ---------------- settings: Me panel ----------------
rep("""        <section class="panel" aria-labelledby="backupH">""",
"""        <section class="panel" aria-labelledby="easyH">
          <h2 class="sub-h" id="easyH">Make it easier</h2>
          <span class="pe-lbl" id="ezSizeL">Text size</span>
          <div class="ez-row" role="group" aria-labelledby="ezSizeL" id="ezSize"><button type="button" data-v="0">Normal</button><button type="button" data-v="1">Large</button><button type="button" data-v="2">Extra large</button></div>
          <span class="pe-lbl" id="ezRateL">Teacher's voice speed</span>
          <div class="ez-row" role="group" aria-labelledby="ezRateL" id="ezRate"><button type="button" data-v="0.85">Slower</button><button type="button" data-v="1">Normal</button><button type="button" data-v="1.15">Faster</button></div>
          <label class="toggle"><input type="checkbox" id="ezFont"><span>Easy-read letters (clearer shapes, more space: helps with dyslexia)</span></label>
          <label class="toggle"><input type="checkbox" id="ezContrast"><span>High contrast (white text and outlines on dark)</span></label>
          <label class="toggle"><input type="checkbox" id="ezCalm"><span>Less movement (no floating, flying or confetti)</span></label>
        </section>
        <section class="panel" aria-labelledby="backupH">""")
rep("      if (typeof pf.autoRead === 'boolean') profile.autoRead = pf.autoRead;",
    "      if (typeof pf.autoRead === 'boolean') profile.autoRead = pf.autoRead;\n      if (pf.ts === 1 || pf.ts === 2) profile.ts = pf.ts;\n      if ([0.85, 1, 1.15].indexOf(pf.rate) >= 0) profile.rate = pf.rate;\n      ['easyFont', 'contrast', 'calm'].forEach(function (k) { if (typeof pf[k] === 'boolean') profile[k] = pf[k]; });")
rep("  function autoRead() {", r"""  // ---- Make it easier ----
  function applyEasy() {
    var b = document.body;
    b.classList.toggle('ts-1', profile.ts === 1); b.classList.toggle('ts-2', profile.ts === 2);
    b.classList.toggle('easy-font', !!profile.easyFont); b.classList.toggle('hi-contrast', !!profile.contrast); b.classList.toggle('calm', !!profile.calm);
    if (profile.calm) still = true;
    try { voiceEl.playbackRate = profile.rate || 1; voiceEl.defaultPlaybackRate = profile.rate || 1; } catch (e) {}
    document.querySelectorAll('#ezSize button').forEach(function (x) { x.setAttribute('aria-pressed', String(+x.dataset.v === (profile.ts || 0))); });
    document.querySelectorAll('#ezRate button').forEach(function (x) { x.setAttribute('aria-pressed', String(+x.dataset.v === (profile.rate || 1))); });
    document.getElementById('ezFont').checked = !!profile.easyFont; document.getElementById('ezContrast').checked = !!profile.contrast; document.getElementById('ezCalm').checked = !!profile.calm;
  }
  document.querySelectorAll('#ezSize button').forEach(function (x) { x.addEventListener('click', function () { profile.ts = +x.dataset.v; saveProfile(); applyEasy(); }); });
  document.querySelectorAll('#ezRate button').forEach(function (x) { x.addEventListener('click', function () { profile.rate = +x.dataset.v; saveProfile(); applyEasy(); }); });
  [['ezFont', 'easyFont'], ['ezContrast', 'contrast'], ['ezCalm', 'calm']].forEach(function (p) {
    document.getElementById(p[0]).addEventListener('change', function (e) { profile[p[1]] = e.target.checked; saveProfile(); applyEasy(); if (p[1] === 'calm' && !e.target.checked) location.reload(); });
  });
  function autoRead() {""")
rep("  renderSoundBtn();\n", "  renderSoundBtn();\n  applyEasy();\n")
# the voice speed holds for every step (each step sets a new source)
rep("  function applyNarrator() {", "  function applyNarrator() {\n    try { voiceEl.playbackRate = profile.rate || 1; voiceEl.defaultPlaybackRate = profile.rate || 1; } catch (e) {}")

# ---------------- Home fixes ----------------
# news: a badge on the House/Town/Library tab instead of the robot flying onto the lesson card
rep("    if (houseNews()) { moveBuddy('nav'); return; }\n    moveBuddy(", "    document.querySelectorAll('.nav [data-nav=\"house\"]').forEach(function (b) { b.classList.toggle('has-news', houseNews()); });\n    moveBuddy(")
rep("  function markHouseSeen() { try { localStorage.setItem(seenKey(), String(state.current)); } catch (e) {} newsDismissed = false; }",
    "  function markHouseSeen() { try { localStorage.setItem(seenKey(), String(state.current)); } catch (e) {} newsDismissed = false; document.querySelectorAll('.nav [data-nav=\"house\"]').forEach(function (b) { b.classList.remove('has-news'); }); }")
# the streak: a star, so it is not a second moon next to the night-time world button
rep("""        <span class="chip" title="Nights in a row">
          <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="#F2C6E0"/></svg>""",
    """        <span class="chip" title="Days in a row">
          <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z" fill="#FFE07A"/></svg>""")
# the Courses tile: the course you are on, not other courses' icons
rep("""<span class="c-stack" aria-hidden="true"><i class="c-ic py">Py</i><i class="c-ic web">&lt;/&gt;</i><i class="c-ic math">÷</i></span>""",
    """<span class="c-stack" aria-hidden="true" id="coursesIc"></span>""")
rep("    var more = COURSES.filter(function (c) { return !c.live && profile.age >= c.minAge; }).length;\n    document.getElementById('coursesMore').textContent = more ? '+' + more + ' more to explore' : 'See all courses';",
    "    document.getElementById('coursesMore').textContent = 'See all courses';\n    var ci = document.getElementById('coursesIc'); if (ci && typeof CQ_COURSES !== 'undefined' && COURSE && CQ_COURSES[COURSE]) ci.textContent = CQ_COURSES[COURSE].emoji;")
# the Cards tile and screen: only the categories that have cards
rep("    document.getElementById('cardsCats').textContent = !tot ? 'Each lesson adds 3' : learnedCount() + ' of ' + tot + ' learned · ' + CATS.length + ' categories';",
    "    document.getElementById('cardsCats').textContent = !tot ? 'Each lesson adds 3' : learnedCount() + ' of ' + tot + ' learned · ' + usedCats() + (usedCats() === 1 ? ' topic' : ' topics');")
rep("      ? due.length + ' to review now · ' + learnedCount() + ' of ' + total + ' learned well · ' + CATS.length + ' categories'",
    "      ? due.length + ' to review now · ' + learnedCount() + ' of ' + total + ' learned well · ' + usedCats() + (usedCats() === 1 ? ' topic' : ' topics')")
rep("  function learnedCount() {", "  function usedCats() { var u = {}; CARDS.forEach(function (c) { if (cardState[c.id]) u[c.c] = 1; }); return Object.keys(u).length; }\n  function learnedCount() {")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
