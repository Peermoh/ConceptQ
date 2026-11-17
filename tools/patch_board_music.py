# Board: write whole characters (emoji never break), an upright rounded font for Maths/English (| / — ⌒ ● ▲ look right),
# 'Read it' without Python comment marks for Maths/English; a gentle music-box melody on Home (Music switch),
# and a congratulations fanfare with firecrackers for the celebrations.
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- board ----------------
rep("""    for (var i = (from && from.c ? from.c + 1 : 1); i <= text.length; i++) {
      if (tok !== lesson.token) return false;
      span.textContent = text.slice(0, i);
      lesson.pos.c = i;
      if (i === 1 || i % 2 === 0 || i === text.length) teacherTo(cur);""",
"""    // whole characters, never half of one: an emoji is several code units (🐚, 🏙️, 👩‍🏫), and half of it shows as a broken box
    var chars = graphemes(text);
    for (var i = (from && from.c ? from.c + 1 : 1); i <= chars.length; i++) {
      if (tok !== lesson.token) return false;
      span.textContent = chars.slice(0, i).join('');
      lesson.pos.c = i;
      if (i === 1 || i % 2 === 0 || i === chars.length) teacherTo(cur);""")
rep("  async function writeLine(box, kind, text, tok, perChar, from) {",
    """  var segmenter = null; try { segmenter = new Intl.Segmenter(undefined, { granularity: 'grapheme' }); } catch (e) {}
  function graphemes(t) { if (segmenter) { var out = []; for (var it of segmenter.segment(t)) out.push(it.segment); return out; } return Array.from(t); }
  async function writeLine(box, kind, text, tok, perChar, from) {""")
# Maths and English boards: an upright, rounded font (the slanted chalk font made | look like /, and has no ▮ ● ▲ ■ ⌒)
rep(".chalk { font-family: 'Caveat', 'Patrick Hand', cursive;",
    "#board.kids .chalk:not(.title) { font-family: 'Nunito', system-ui, sans-serif; font-weight: 800; font-size: 23px; letter-spacing: .5px; }\n#board.kids .chalk.code { font-family: 'Nunito', system-ui, sans-serif; font-weight: 900; }\n.chalk { font-family: 'Caveat', 'Patrick Hand', cursive;")
rep("  function openLesson(n) {\n    LD = LESSON_DATA[n]; openLessonIdx = n;",
    "  function openLesson(n) {\n    LD = LESSON_DATA[n]; openLessonIdx = n;\n    document.getElementById('board').classList.toggle('kids', COURSE !== 'py');")
# Read it: plain lines for Maths and English (the # marks are Python comments)
rep("""        if (l[0] === 'code') code.appendChild(document.createTextNode(l[1]));""",
    """        if (COURSE !== 'py') { code.appendChild(document.createTextNode(l[1].replace(/^→\\s*/, ''))); return; }
        if (l[0] === 'code') code.appendChild(document.createTextNode(l[1]));""")
rep("  function sayAsCode(say) { // the narration with spoken code written as code, for reading",
    "  function sayAsCode(say) { // the narration with spoken code written as code, for reading\n    if (COURSE !== 'py') return say;")

# ---------------- sounds: a music-box melody on Home, and a fanfare with firecrackers ----------------
rep("      fire: function () {",
"""      // congratulations: a bright fanfare, then a string of firecrackers
      fanfare: function () {
        [[523, 0, 0.18], [523, 0.16, 0.12], [523, 0.28, 0.12], [698, 0.42, 0.5], [880, 0.95, 0.22], [784, 1.15, 0.2], [880, 1.35, 0.22], [1047, 1.6, 0.9]].forEach(function (n) {
          tone(n[0], n[2], 'sawtooth', 0.05, n[1]); tone(n[0], n[2], 'triangle', 0.1, n[1]); tone(n[0] * 2, n[2], 'sine', 0.03, n[1]);
        });
        [262, 330, 392].forEach(function (f) { tone(f, 1.0, 'triangle', 0.05, 1.6); }); // a warm chord under the last note
      },
      crackers: function () { // pop-pop-pop: short, sharp bursts at random moments
        for (var i = 0; i < 14; i++) (function (d) {
          var n = noise(), f = ctx.createBiquadFilter(), g = ctx.createGain(), t = ctx.currentTime + d; f.type = 'bandpass'; f.frequency.value = 1500 + Math.random() * 3500; f.Q.value = 0.8;
          g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.35, t + 0.004); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.07 + Math.random() * 0.05);
          n.connect(f); f.connect(g); g.connect(master); n.start(t); n.stop(t + 0.15);
        })(0.2 + Math.random() * 1.8 + (i < 4 ? 0 : 0.3));
      },
      fire: function () {""")
# the melody: a quiet music box playing a slow pentatonic tune, on Home and in the house / town, when Music is on
rep("    return { play: play, ambient: ambient, stop: stopAmb, unlock: function () { tapped = true; if (on()) ac(); } };",
r"""    // a quiet music-box tune (pentatonic, so any two notes sound nice together), looping slowly
    var mus = null;
    function musicOn() { return profile.sounds !== false && profile.music !== false; }
    function stopMusic() { if (mus) { clearTimeout(mus.t); mus = null; } }
    function music() {
      if (mus || !musicOn() || !ac()) return;
      var SCALE = [523, 587, 659, 784, 880, 1047, 1175, 1319], PHRASES = [[0, 2, 4, 3, 2, 1, 0], [4, 5, 7, 5, 4, 2, 3], [2, 3, 4, 6, 5, 4, 2], [7, 6, 4, 5, 3, 2, 0]], k = 0;
      mus = { t: 0 };
      (function phrase() {
        if (!mus || !musicOn()) { mus = null; return; }
        var ph = PHRASES[k++ % PHRASES.length], beat = 0.42;
        ph.forEach(function (n, i) {
          var t = i * beat + (i % 2 ? 0.04 : 0); tone(SCALE[n], 1.1, 'sine', 0.035, t); tone(SCALE[n] * 2, 0.5, 'sine', 0.008, t); // a soft bell with a little shine
          if (i % 2 === 0) tone(SCALE[n] / 2, 1.4, 'triangle', 0.018, t); // a low note underneath
        });
        mus.t = setTimeout(phrase, (ph.length * beat + 1.6 + Math.random() * 1.2) * 1000);
      })();
    }
    return { play: play, ambient: ambient, stop: stopAmb, music: music, stopMusic: stopMusic, unlock: function () { tapped = true; if (on()) ac(); } };""")
rep("    if (where && profile.sounds !== false) SFX.ambient(scene.world, scene.weather, currentTime()); else SFX.stop();",
    "    if (where && profile.sounds !== false) SFX.ambient(scene.world, scene.weather, currentTime()); else SFX.stop();\n    if (where && profile.sounds !== false && profile.music !== false) SFX.music(); else SFX.stopMusic();")
# Music switch in Me (sounds switch still turns everything off)
rep("""          <button class="chip-btn" id="tourAgain" type="button">Show me around again</button>""",
    """          <label class="toggle"><input type="checkbox" id="setMusic"><span>Music: a soft music-box tune on Home</span></label>
          <button class="chip-btn" id="tourAgain" type="button">Show me around again</button>""")
rep("    var t = document.getElementById('setSounds'); if (t) t.checked = onn;",
    "    var t = document.getElementById('setSounds'); if (t) t.checked = onn;\n    var m = document.getElementById('setMusic'); if (m) { m.checked = profile.music !== false; m.disabled = !onn; }")
rep("  document.getElementById('setSounds').addEventListener('change', function (e) { setSounds(e.target.checked); });",
    "  document.getElementById('setSounds').addEventListener('change', function (e) { setSounds(e.target.checked); });\n  document.getElementById('setMusic').addEventListener('change', function (e) { profile.music = e.target.checked; saveProfile(); sceneSound(); });")
rep("      if (typeof pf.sounds === 'boolean') profile.sounds = pf.sounds;", "      if (typeof pf.sounds === 'boolean') profile.sounds = pf.sounds;\n      if (typeof pf.music === 'boolean') profile.music = pf.music;")
# celebrations play the fanfare and the crackers (the puzzle frame asks the app)
rep("  window.CQBoom = function () { SFX.play('fire'); };", "  window.CQBoom = function () { SFX.play('fire'); };\n  window.CQCheer = function () { SFX.play('fanfare'); SFX.play('crackers'); };")
rep("    if (e.data.cq === 'fire') SFX.play('fire');", "    if (e.data.cq === 'fire') SFX.play('fire');\n    if (e.data.cq === 'cheer') { SFX.play('fanfare'); SFX.play('crackers'); }")
# the done screen already plays 'win'; the celebration replaces it with the fanfare
rep("    show('done'); SFX.play('win');\n", "    show('done');\n")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
