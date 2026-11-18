# Badges and a trophy shelf; a plain dark background option for every page.
import re, subprocess, tempfile
D = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/'
SRC = D + 'lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- styles ----------------
rep("#houseFrame { flex: 1;", r"""/* ---- badges: the trophy shelf ---- */
.badge-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(92px, 1fr)); gap: 10px; }
.bdg { display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 10px 6px; border-radius: 16px; background: rgba(255,255,255,.05); text-align: center; }
.bdg .bi { width: 52px; height: 52px; border-radius: 50%; display: grid; place-items: center; font-size: 28px; background: radial-gradient(circle at 35% 30%, #FFE9A8, #FFB547 60%, #D9861A); box-shadow: 0 4px 10px rgba(0,0,0,.3), inset 0 -3px 0 rgba(0,0,0,.15); }
.bdg b { font-size: 12px; line-height: 1.2; }
.bdg small { font-size: 11px; opacity: .7; line-height: 1.2; }
.bdg.locked .bi { background: rgba(255,255,255,.08); filter: grayscale(1); opacity: .45; box-shadow: none; }
.bdg.locked b { opacity: .6; }
.bdg.fresh .bi { animation: bdgNew 1.4s ease-in-out 3; }
@keyframes bdgNew { 50% { transform: scale(1.15) rotate(-6deg); } }
.badge-tile .bdg-row { display: flex; gap: 2px; font-size: 20px; }
/* ---- plain dark background (Make it easier) ---- */
body.plain-dark #home .scene, body.plain-dark #home .fx { display: none !important; }
body.plain-dark, body.plain-dark #home, body.plain-dark .screen { background: #0E0814 !important; }
#houseFrame { flex: 1;""")

# ---------------- markup ----------------
rep("""        <button class="tile dash-tile prize-tile" id="prizeTile" aria-label="Prize wheel">""",
    """        <button class="tile dash-tile badge-tile" id="badgeTile" type="button" aria-label="Badges">
          <span class="row"><b class="tile-t">Badges</b><span class="bdg-row" id="badgeTileIc" aria-hidden="true"></span></span>
          <span class="lbl" id="badgeTileN">0 earned</span>
          <span class="lbl more" id="badgeTileNext">Finish a lesson for your first badge</span>
        </button>
        <button class="tile dash-tile prize-tile" id="prizeTile" aria-label="Prize wheel">""")
rep("""        <section class="panel" aria-labelledby="easyH">""",
    """        <section class="panel" aria-labelledby="badgeH" id="badgePanel">
          <h2 class="sub-h" id="badgeH">My badges</h2>
          <p class="muted small" id="badgeSum"></p>
          <div class="badge-grid" id="badgeGrid"></div>
        </section>
        <section class="panel" aria-labelledby="easyH">""")
rep("""          <label class="toggle"><input type="checkbox" id="ezCalm">""",
    """          <label class="toggle"><input type="checkbox" id="ezDark"><span>Plain dark background on every page (no bright sky)</span></label>
          <label class="toggle"><input type="checkbox" id="ezCalm">""")

# ---------------- plain dark ----------------
rep("      ['easyFont', 'contrast', 'calm'].forEach(function (k) { if (typeof pf[k] === 'boolean') profile[k] = pf[k]; });",
    "      ['easyFont', 'contrast', 'calm', 'plainDark'].forEach(function (k) { if (typeof pf[k] === 'boolean') profile[k] = pf[k]; });")
rep("    b.classList.toggle('easy-font', !!profile.easyFont);", "    b.classList.toggle('plain-dark', !!profile.plainDark);\n    b.classList.toggle('easy-font', !!profile.easyFont);")
rep("document.getElementById('ezCalm').checked = !!profile.calm;", "document.getElementById('ezCalm').checked = !!profile.calm; document.getElementById('ezDark').checked = !!profile.plainDark;")
rep("  [['ezFont', 'easyFont'], ['ezContrast', 'contrast'], ['ezCalm', 'calm']].forEach(", "  [['ezFont', 'easyFont'], ['ezContrast', 'contrast'], ['ezCalm', 'calm'], ['ezDark', 'plainDark']].forEach(")

# ---------------- badges ----------------
rep("  // ---- Make it easier ----", r"""  // ================= badges =================
  // Each badge has a test on what the learner has done; cq-badges keeps when each was earned, plus a few counts
  // (puzzles built, perfect quizzes) that are not kept anywhere else.
  var BADGES = [];
  function bdgStore() { var b = null; try { b = JSON.parse(localStorage.getItem('cq-badges') || 'null'); } catch (e) {} if (!b || typeof b !== 'object') b = {}; if (!b.got) b.got = {}; if (!b.n) b.n = {}; return b; }
  function bdgSave(b) { try { localStorage.setItem('cq-badges', JSON.stringify(b)); } catch (e) {} }
  function bdgCount(k) { var b = bdgStore(); b.n[k] = (b.n[k] || 0) + 1; bdgSave(b); checkBadges(); }
  function totalLessons() { return ['py', 'maths', 'english'].reduce(function (t, c) { return t + Math.min(doneIn(c), courseTotal(c)); }, 0); }
  function buildBadges() {
    var n = function (k) { return bdgStore().n[k] || 0; };
    BADGES = [
      ['first', '🌱', 'First lesson', 'Finish any lesson', function () { return totalLessons() >= 1; }],
      ['l5', '📗', 'Five lessons', 'Finish 5 lessons', function () { return totalLessons() >= 5; }],
      ['l10', '📚', 'Ten lessons', 'Finish 10 lessons', function () { return totalLessons() >= 10; }],
      ['l25', '🎓', 'Super learner', 'Finish 25 lessons', function () { return totalLessons() >= 25; }],
      ['perfect', '🎯', 'Bullseye', 'Get every answer right first time', function () { return n('perfect') >= 1; }],
      ['perfect5', '🏹', 'Sharp shooter', '5 perfect quizzes', function () { return n('perfect') >= 5; }],
      ['puzzle', '🧩', 'Builder', 'Build your first puzzle', function () { return n('puzzle') >= 1; }],
      ['puzzle5', '🏗️', 'Puzzle master', 'Build 5 puzzles', function () { return n('puzzle') >= 5; }],
      ['s3', '⭐', 'On a roll', 'Learn 3 days in a row', function () { return (state.streak || 0) >= 3; }],
      ['s7', '🌟', 'Week star', 'Learn 7 days in a row', function () { return (state.streak || 0) >= 7; }],
      ['cards', '🃏', 'Memory champ', 'Learn 10 flashcards well', function () { return learnedCount() >= 10; }],
      ['embers', '🔥', 'Ember collector', 'Collect 500 embers', function () { return state.embers >= 500; }],
      ['prize', '🎁', 'Prize winner', 'Win a prize on the wheel', function () { return rewards && rewards.wins && rewards.wins.length >= 1; }],
      ['explorer', '🧭', 'Explorer', 'Try two different courses', function () { return ['py', 'maths', 'english'].filter(function (c) { return doneIn(c) > 0; }).length >= 2; }]
    ];
    // one badge for each street or floor finished
    [['maths', '🏙️'], ['english', '📚'], ['py', '🏠']].forEach(function (cc) {
      var P = cc[0] === 'py' ? PY_PACK : COURSE_PACKS[cc[0]];
      P.floorNames.forEach(function (nm, f) {
        BADGES.push(['floor-' + cc[0] + '-' + f, cc[1], nm + ' done', 'Finish every lesson in ' + nm, function () { return doneIn(cc[0]) >= P.floorAt[f + 1]; }]);
      });
    });
  }
  var badgeQueue = [];
  // award new badges; celebrate them one at a time (after any celebration already on screen)
  function checkBadges(quiet) {
    if (!BADGES.length) buildBadges();
    var b = bdgStore(), fresh = [];
    BADGES.forEach(function (bd) { if (!b.got[bd[0]]) { var ok = false; try { ok = bd[4](); } catch (e) {} if (ok) { b.got[bd[0]] = Date.now(); fresh.push(bd); } } });
    if (!fresh.length) return;
    bdgSave(b); renderBadgeTile();
    if (quiet) return;
    fresh.forEach(function (bd) { badgeQueue.push(bd); });
    if (badgeQueue.length === fresh.length) setTimeout(nextBadge, document.querySelector('.cq-cel') ? 3300 : 300);
  }
  function nextBadge() {
    var bd = badgeQueue.shift(); if (!bd) return;
    if (document.querySelector('.cq-cel')) { badgeQueue.unshift(bd); setTimeout(nextBadge, 700); return; }
    CQCelebrate('🏅 New badge!', bd[1] + ' ' + bd[2] + ': ' + bd[3].charAt(0).toLowerCase() + bd[3].slice(1));
    if (badgeQueue.length) setTimeout(nextBadge, 3200);
  }
  function renderBadgeTile() {
    if (!BADGES.length) buildBadges();
    var got = bdgStore().got, earned = BADGES.filter(function (bd) { return got[bd[0]]; }).sort(function (a, c) { return got[c[0]] - got[a[0]]; });
    var t = document.getElementById('badgeTileN'); if (!t) return;
    t.textContent = earned.length + ' of ' + BADGES.length + ' earned';
    document.getElementById('badgeTileIc').textContent = earned.slice(0, 3).map(function (bd) { return bd[1]; }).join('') || '🏅';
    var next = BADGES.filter(function (bd) { return !got[bd[0]]; })[0];
    document.getElementById('badgeTileNext').textContent = next ? 'Next: ' + next[3] : 'You have every badge!';
  }
  function renderBadges() {
    if (!BADGES.length) buildBadges();
    var got = bdgStore().got, grid = document.getElementById('badgeGrid'); grid.innerHTML = '';
    var list = BADGES.filter(function (bd) { return got[bd[0]]; }).sort(function (a, c) { return got[c[0]] - got[a[0]]; }).concat(BADGES.filter(function (bd) { return !got[bd[0]]; }));
    list.forEach(function (bd) {
      var on = !!got[bd[0]], el = document.createElement('div'); el.className = 'bdg' + (on ? '' : ' locked') + (on && Date.now() - got[bd[0]] < 60000 ? ' fresh' : '');
      el.innerHTML = '<span class="bi" aria-hidden="true"></span><b></b><small></small>';
      el.querySelector('.bi').textContent = bd[1]; el.querySelector('b').textContent = bd[2];
      el.querySelector('small').textContent = on ? new Date(got[bd[0]]).toLocaleDateString() : bd[3];
      el.setAttribute('aria-label', bd[2] + (on ? ', earned' : ', not yet: ' + bd[3]));
      grid.appendChild(el);
    });
    var nOn = BADGES.filter(function (bd) { return got[bd[0]]; }).length;
    document.getElementById('badgeSum').textContent = nOn ? nOn + ' of ' + BADGES.length + ' badges. Keep going!' : 'Badges show here as you learn. Finish a lesson for your first one!';
  }
  document.getElementById('badgeTile').addEventListener('click', function () { show('me'); setTimeout(function () { document.getElementById('badgePanel').scrollIntoView({ block: 'start', behavior: still ? 'auto' : 'smooth' }); }, 80); });

  // ---- Make it easier ----""")
rep("  function renderMe() {\n    renderMyCourses();", "  function renderMe() {\n    renderMyCourses(); checkBadges(true); renderBadges();")
# when to check: after a lesson (a perfect quiz counts), a puzzle, the wheel, card reviews, and on Home
rep("    var endOfFloor = FLOOR_AT.indexOf(openLessonIdx + 1) > 0;",
    "    if (firstTry === Q.length) bdgCount('perfect'); else checkBadges();\n    var endOfFloor = FLOOR_AT.indexOf(openLessonIdx + 1) > 0;")
rep("    if (e.data.cq === 'fire') SFX.play('fire');", "    if (e.data.cq === 'fire') SFX.play('fire');\n    if (e.data.cq === 'solved') bdgCount('puzzle');")
rep("      rewards.used++; rewards.wins.push({ p: list[pick], t: Date.now() }); rewards.wins = rewards.wins.slice(-30); saveRewards();",
    "      rewards.used++; rewards.wins.push({ p: list[pick], t: Date.now() }); rewards.wins = rewards.wins.slice(-30); saveRewards(); setTimeout(checkBadges, 2500);")
rep("    renderHouseCard(); renderHomeTiles(); applyProfile();", "    renderHouseCard(); renderHomeTiles(); applyProfile(); if (typeof renderBadgeTile === 'function' && PY_PACK) { checkBadges(); renderBadgeTile(); }")
rep("  function renderCards() {\n", "  function renderCards() {\n    if (typeof checkBadges === 'function' && PY_PACK) setTimeout(checkBadges, 300);\n")
# learners from before: badges they already deserve are added quietly (no pile of celebrations)
rep("  if (FIRST_RUN) startWelcome(); else {", "  try { if (!localStorage.getItem('cq-badges') && !FIRST_RUN) checkBadges(true); } catch (e) {}\n  if (FIRST_RUN) startWelcome(); else {")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]

# ---------------- the puzzle tells the app it was solved ----------------
p = D + 'puzzle.js'; ps = open(p).read()
a = "      if (solved) { board.classList.add('done'); cheer.textContent = 'You built it!'; if (window.CQCelebrate) CQCelebrate('Congratulations!', 'You built it, piece by piece!'); }"
assert ps.count(a) == 1
ps = ps.replace(a, a + "\n      if (solved && window.parent !== window) window.parent.postMessage({ cq: 'solved' }, '*'); // counts towards the puzzle badges")
open(p, 'w').write(ps)

# ---------------- plain dark in the house and in the town / library: night, without stars or moon glare ----------------
for f, var in (('house.html', 'houseTime'), ('world.template.html', 'time')):
    ws = open(D + f).read()
    a = "    %s = { morning: 1, day: 1, sunset: 1, night: 1 }[t] ? t : 'day';" % var
    assert ws.count(a) == 1, f
    ws = ws.replace(a, a + "\n    try { var pfd = JSON.parse(localStorage.getItem('cq-profile') || 'null'); if (pfd && pfd.plainDark) %s = 'night'; } catch (e) {} // plain dark background (Me > Make it easier)" % var)
    open(D + f, 'w').write(ws)
print('patched')
