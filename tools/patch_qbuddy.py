# A small robot on the question screen: while a question is read out it glides to each choice in turn
# (A, B, C — every choice, so it never gives the answer away) and that choice lights up; it cheers or says
# "oops" after an answer. Questions are read out automatically for age 8 and under (switch in Me).
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep(".q-hear { display: inline-flex;", r""".q-buddy { position: fixed; z-index: 30; width: 52px; height: 48px; pointer-events: none; transition: left .45s cubic-bezier(.3,1.3,.5,1), top .45s cubic-bezier(.3,1.3,.5,1), transform .3s; filter: drop-shadow(0 4px 6px rgba(0,0,0,.35)); }
.q-buddy svg { width: 100%; height: 100%; display: block; }
.q-buddy[hidden] { display: none; }
.q-buddy.bob svg { animation: qbBob 1.2s ease-in-out infinite; }
@keyframes qbBob { 50% { transform: translateY(-4px); } }
#qOptions .opt.reading { outline: 3px solid #FFE07A; outline-offset: 2px; box-shadow: 0 0 0 6px rgba(255,224,122,.18); transition: outline-color .2s; }
#qText.reading { text-shadow: 0 0 12px rgba(255,224,122,.45); }
@media (prefers-reduced-motion: reduce) { .q-buddy { transition: none; } .q-buddy.bob svg { animation: none; } }
.q-hear { display: inline-flex;""")
rep("""      <button class="q-hear" id="qHear" type="button" hidden>🔊 Read it to me</button>""",
    """      <button class="q-hear" id="qHear" type="button" hidden>🔊 Read it to me</button>
      <div class="q-buddy" id="qBuddy" aria-hidden="true" hidden><svg viewBox="0 0 120 110"></svg></div>""")

# Me: read questions out loud automatically
rep("""          <label class="toggle"><input type="checkbox" id="setMusic">""",
    """          <label class="toggle"><input type="checkbox" id="setAutoRead"><span>Read Maths and English questions out loud by themselves (on for age 8 and under)</span></label>
          <label class="toggle"><input type="checkbox" id="setMusic">""")
rep("      if (typeof pf.music === 'boolean') profile.music = pf.music;", "      if (typeof pf.music === 'boolean') profile.music = pf.music;\n      if (typeof pf.autoRead === 'boolean') profile.autoRead = pf.autoRead;")
rep("  document.getElementById('setMusic').addEventListener('change',",
    "  function autoRead() { return typeof profile.autoRead === 'boolean' ? profile.autoRead : profile.age <= 8; }\n  document.getElementById('setAutoRead').addEventListener('change', function (e) { profile.autoRead = e.target.checked; saveProfile(); });\n  document.getElementById('setMusic').addEventListener('change',")
rep("    var m = document.getElementById('setMusic'); if (m) { m.checked = profile.music !== false; m.disabled = !onn; }",
    "    var m = document.getElementById('setMusic'); if (m) { m.checked = profile.music !== false; m.disabled = !onn; }\n    var ar = document.getElementById('setAutoRead'); if (ar) ar.checked = autoRead();")

# the robot: where it stands (next to the read button), where it goes while reading (beside each choice in turn)
rep("  function hearQ(q) {", r"""  var qBud = document.getElementById('qBuddy'), qBudAt = -2;
  function qBuddyMood(m) { qBud.querySelector('svg').innerHTML = lumiSVG(m || 'happy'); }
  // -2: resting by the read button; -1: the question; 0, 1, 2…: that choice
  function qPoint(i) {
    if (document.getElementById('quiz').hidden || COURSE === 'py') { qBud.hidden = true; return; }
    qBud.hidden = false; qBudAt = i;
    document.querySelectorAll('#qOptions .opt').forEach(function (o, k) { o.classList.toggle('reading', k === i); });
    document.getElementById('qText').classList.toggle('reading', i === -1);
    var tgt = i >= 0 ? document.querySelectorAll('#qOptions .opt')[i] : i === -1 ? document.getElementById('qText') : document.getElementById('qHear');
    if (!tgt) return;
    var r = tgt.getBoundingClientRect(), x, y;
    if (i >= 0) { x = r.right - 58; y = r.top + (r.height - 48) / 2; qBud.style.transform = 'scaleX(-1)'; }      // inside the choice, at its right end, facing it
    else if (i === -1) { x = Math.min(window.innerWidth - 60, r.right + 6); y = r.top - 6; qBud.style.transform = 'scaleX(-1)'; }
    else { x = r.right + 10; y = r.top + (r.height - 48) / 2; qBud.style.transform = ''; }                      // resting by the read button
    qBud.style.left = Math.max(4, Math.min(window.innerWidth - 56, x)) + 'px'; qBud.style.top = Math.max(4, y) + 'px';
    qBud.classList.toggle('bob', i >= -1);
  }
  window.addEventListener('resize', function () { if (!qBud.hidden) qPoint(qBudAt); });
  document.getElementById('quiz').addEventListener('scroll', function () { if (!qBud.hidden) qPoint(qBudAt); }, true);
  function hearQ(q) {""")
# reading: each part points the robot at what is being read; phonics sounds point at the question
rep("    if (q.snd) { playPhon(q.snd, q.gap); return; }\n    if (!hasTTS) return;",
    "    if (q.snd) { qPoint(-1); playPhon(q.snd, q.gap); setTimeout(function () { if (Q[qi] === q && answers[qi] === undefined) qPoint(-2); }, 2600); return; }\n    if (!hasTTS) return;")
rep("""      parts.forEach(function (t) { // one sentence at a time, so each option gets its own clear pause
        var u = new SpeechSynthesisUtterance(t); if (v) { u.voice = v; u.lang = v.lang; } else u.lang = profile.narrator === 'ryan' ? 'en-GB' : 'en-IN';""",
    """      parts.forEach(function (t, k) { // one sentence at a time, so each option gets its own clear pause
        var u = new SpeechSynthesisUtterance(t); if (v) { u.voice = v; u.lang = v.lang; } else u.lang = profile.narrator === 'ryan' ? 'en-GB' : 'en-IN';
        u.onstart = function () { if (Q[qi] === q) qPoint(k - 1); }; // the robot goes to what is being read
        if (k === parts.length - 1) u.onend = function () { if (Q[qi] === q && answers[qi] === undefined) qPoint(-2); };""")
# a new question: robot by the read button; read it out by itself when that is on
rep("    if (q.snd && !done) setTimeout(function () { if (Q[qi] === q) hearQ(q); }, 250);",
    "    qBuddyMood('happy'); setTimeout(function () { qPoint(-2); }, 30);\n    if (!done && COURSE !== 'py' && (q.snd || autoRead())) setTimeout(function () { if (Q[qi] === q && answers[qi] === undefined) hearQ(q); }, 450);")
# after an answer: stop reading, cheer or 'oops' by the chosen choice
rep("    if (right) { firstTry++; earned += 10; burst(btn); }\n    SFX.play(right ? 'right' : 'wrong');",
    "    if (right) { firstTry++; earned += 10; burst(btn); }\n    SFX.play(right ? 'right' : 'wrong');\n    try { if (hasTTS) speechSynthesis.cancel(); } catch (e) {} playPhon.tok = {};\n    if (COURSE !== 'py') { qBuddyMood(right ? 'cheer' : 'oops'); qPoint(i); document.querySelectorAll('#qOptions .opt').forEach(function (o) { o.classList.remove('reading'); }); }")
# leaving the quiz hides it
rep("  function show(id) {\n", "  function show(id) {\n    var qb = document.getElementById('qBuddy'); if (qb && id !== 'quiz') qb.hidden = true;\n")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
