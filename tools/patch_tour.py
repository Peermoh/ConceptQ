# Guided tour of the app, theme sounds (with a mute switch), a prize hint on the wheel, and the robot as the app logo.
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- styles ----------------
rep("#houseFrame { flex: 1;", r"""/* ---- guided tour: a spotlight on one part of the screen, and the robot explaining it ---- */
.tour { position: fixed; inset: 0; z-index: 80; pointer-events: auto; }
.tour-ring { position: fixed; border-radius: 18px; box-shadow: 0 0 0 4px #FFE07A, 0 0 0 9999px rgba(12,4,20,.72); transition: all .35s cubic-bezier(.3,1.2,.4,1); pointer-events: none; }
.tour-card { position: fixed; left: 16px; right: 16px; max-width: 380px; margin: 0 auto; background: var(--sheet-bg, #2A1340); color: var(--cream, #FFF6EC); border: 2px solid #FFE07A; border-radius: 22px; padding: 14px 16px; box-shadow: 0 14px 34px rgba(0,0,0,.5); transition: top .35s, bottom .35s; }
.tour-card .tc-top { display: flex; gap: 10px; align-items: flex-start; }
.tour-card svg { flex: 0 0 auto; width: 56px; height: 52px; }
.tour-card h3 { margin: 0 0 4px; font-family: var(--font-display); font-weight: 400; font-size: 20px; }
.tour-card p { margin: 0; font-weight: 700; font-size: 15px; line-height: 1.4; }
.tour-card .tc-row { display: flex; align-items: center; gap: 8px; margin-top: 12px; }
.tour-card .tc-dots { flex: 1; display: flex; gap: 5px; }
.tour-card .tc-dots i { width: 7px; height: 7px; border-radius: 50%; background: rgba(255,255,255,.25); }
.tour-card .tc-dots i.on { background: #FFE07A; }
.tour-card button { border: 0; border-radius: 999px; padding: 9px 16px; font: inherit; font-weight: 900; cursor: pointer; }
.tour-card .tc-next { background: #FFB547; color: #2A1330; }
.tour-card .tc-skip { background: none; color: inherit; opacity: .7; text-decoration: underline; padding: 9px 6px; }
/* ---- prize hint on the wheel ---- */
.wheel-hint { margin: 0; text-align: center; font-weight: 700; font-size: 14px; color: var(--muted); }
.wheel-hint button { background: none; border: 0; padding: 0; color: #FFB547; font: inherit; font-weight: 900; text-decoration: underline; cursor: pointer; }
/* ---- the robot as the app logo ---- */
#topAvatar.logo { background: linear-gradient(160deg, #3B2560, #1D1030) !important; padding: 0; overflow: hidden; }
#topAvatar.logo svg { width: 118%; height: 118%; margin: -4% 0 0 -9%; }
#houseFrame { flex: 1;""")

# ---------------- markup ----------------
# sound on/off chip in the top bar
rep("""        <button class="chip scene-btn" id="sceneBtn" aria-label="Change world and weather">""",
    """        <button class="chip" id="soundBtn" type="button" aria-pressed="true" aria-label="Sounds on. Tap to mute"><span id="soundIc" aria-hidden="true">🔊</span></button>
        <button class="chip scene-btn" id="sceneBtn" aria-label="Change world and weather">""")
# the wheel: a hint instead of a big edit button, shown while it spins too
rep("""      <button class="wheel-edit" id="wheelEdit" type="button">✏️ Change prizes</button>""",
    """      <p class="wheel-hint" id="wheelHint">💡 Want different prizes? A grown-up can <button id="wheelEdit" type="button">change them</button>.</p>""")
rep(""".wheel-edit { background: none;""", """.wheel-edit-old { background: none;""")
# Me: sounds toggle and the tour again
rep("""          <label class="toggle"><input type="checkbox" id="setAntics"><span>Nibb naps and does tricks on Home</span></label>""",
    """          <label class="toggle"><input type="checkbox" id="setAntics"><span>Nibb naps and does tricks on Home</span></label>
          <label class="toggle"><input type="checkbox" id="setSounds"><span>Sounds: taps, cheers, and the sounds of your world (rain, birds, crickets…)</span></label>
          <button class="chip-btn" id="tourAgain" type="button">Show me around again</button>""")

# ---------------- script ----------------
# sound preference
rep("      if (Object.prototype.hasOwnProperty.call(NARRATORS, pf.narrator)) profile.narrator = pf.narrator;",
    "      if (Object.prototype.hasOwnProperty.call(NARRATORS, pf.narrator)) profile.narrator = pf.narrator;\n      if (typeof pf.sounds === 'boolean') profile.sounds = pf.sounds;\n      if (pf.toured === true) profile.toured = true;")
# logo: the robot in the top bar, the robot's name next to it, and as the tab icon and title
rep("""    document.getElementById('topName').textContent = profile.name;""",
    r"""    var tn = window.CQ_TEACHER || profile.teacher || 'Nibb';
    document.getElementById('topName').textContent = tn;
    var gr = document.getElementById('greet'); if (gr && !/, /.test(gr.textContent)) gr.textContent = gr.textContent + ', ' + profile.name;
    document.title = tn + ' · ConceptQ';
    setLogo();""")
rep("""    ['topAvatar', 'meAvatar'].forEach(function (id) { var a = document.getElementById(id); a.textContent = profile.name.charAt(0).toUpperCase(); a.style.background = profile.color; });""",
    """    ['meAvatar'].forEach(function (id) { var a = document.getElementById(id); a.textContent = profile.name.charAt(0).toUpperCase(); a.style.background = profile.color; });""")
rep("  function applyProfile() {", r"""  // the app logo is the robot teacher: in the top bar and as the browser tab icon
  var logoDone = false;
  function setLogo() {
    var a = document.getElementById('topAvatar'); if (!a || logoDone) return;
    a.className += ' logo'; a.innerHTML = '<svg viewBox="0 0 120 110" aria-hidden="true">' + lumiSVG('happy') + '</svg>'; a.removeAttribute('aria-hidden');
    a.setAttribute('role', 'img'); a.setAttribute('aria-label', 'Nibb, your robot teacher');
    try {
      var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 110"><rect width="120" height="110" rx="26" fill="#2A1340"/>' + lumiSVG('happy').replace(/class="[^"]*"/g, '') + '</svg>';
      var l = document.querySelector('link[rel="icon"]') || document.createElement('link'); l.rel = 'icon'; l.type = 'image/svg+xml';
      l.href = 'data:image/svg+xml,' + encodeURIComponent(svg); document.head.appendChild(l);
    } catch (e) {}
    logoDone = true;
  }
  function applyProfile() {""")
rep("    document.getElementById('greet').textContent = greet;", "    document.getElementById('greet').textContent = greet + ', ' + profile.name;")

# ---- the sound engine: made in the browser, no files ----
rep("  // ================= Nibb follows you and keeps busy =================", r"""  // ================= sounds =================
  // Small sounds for taps, right and wrong answers, wins and the wheel, plus the sound of your world on Home
  // and in your house / town: birds by day, crickets at night, rain, wind, snow chimes, bubbles in the aquarium.
  // All made with Web Audio (no files). Off with the speaker chip, or in Me.
  var SFX = (function () {
    var ctx = null, master = null, amb = null, nbuf = null;
    function on() { return profile.sounds !== false; }
    function ac() {
      if (!ctx) { var C = window.AudioContext || window.webkitAudioContext; if (!C) return null; ctx = new C(); master = ctx.createGain(); master.gain.value = 0.55; master.connect(ctx.destination); }
      if (ctx.state === 'suspended') ctx.resume();
      return ctx;
    }
    function noise() { if (!nbuf) { nbuf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate); var d = nbuf.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; } var n = ctx.createBufferSource(); n.buffer = nbuf; n.loop = true; return n; }
    function tone(f, dur, type, vol, at, f2, dest) {
      var t = (at || 0) + ctx.currentTime, o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type || 'sine'; o.frequency.setValueAtTime(f, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + dur);
      g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol || 0.15, t + 0.012); g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
      o.connect(g); g.connect(dest || master); o.start(t); o.stop(t + dur + 0.05);
    }
    var UI = {
      tap: function () { tone(880, 0.06, 'sine', 0.05); },
      right: function () { [523, 659, 784].forEach(function (f, i) { tone(f, 0.22, 'triangle', 0.13, i * 0.08); }); tone(1568, 0.3, 'sine', 0.05, 0.24); },
      wrong: function () { tone(330, 0.16, 'triangle', 0.12, 0, 260); tone(247, 0.22, 'triangle', 0.1, 0.13, 196); },
      win: function () { [523, 659, 784, 1047].forEach(function (f, i) { tone(f, 0.3, 'triangle', 0.13, i * 0.1); }); [1319, 1568, 2093].forEach(function (f, i) { tone(f, 0.25, 'sine', 0.05, 0.45 + i * 0.07); }); },
      tick: function () { tone(1400, 0.03, 'square', 0.03); },
      pop: function () { tone(500, 0.09, 'sine', 0.1, 0, 900); },
      whoosh: function () { var n = noise(), f = ctx.createBiquadFilter(), g = ctx.createGain(), t = ctx.currentTime; f.type = 'bandpass'; f.Q.value = 1; f.frequency.setValueAtTime(300, t); f.frequency.exponentialRampToValueAtTime(2400, t + 0.35); g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(0.12, t + 0.1); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.4); n.connect(f); f.connect(g); g.connect(master); n.start(t); n.stop(t + 0.45); }
    };
    function play(name) { if (!on() || !ac() || !UI[name]) return; try { UI[name](); } catch (e) {} }
    // the world's own sound, looping quietly until stopped
    function stopAmb() { if (!amb) return; var a = amb; amb = null; try { a.gain.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.3); } catch (e) {} a.timers.forEach(clearTimeout); setTimeout(function () { a.nodes.forEach(function (n) { try { n.stop(); } catch (e) {} try { n.disconnect(); } catch (e) {} }); }, 1500); }
    function ambient(world, weather, time) {
      var key = world + '/' + weather + '/' + time;
      if (amb && amb.key === key) return;
      stopAmb();
      if (!on() || !ac()) return;
      var g = ctx.createGain(), a = { key: key, gain: g, nodes: [], timers: [] }; g.gain.value = 0.0001; g.connect(master); g.gain.setTargetAtTime(1, ctx.currentTime, 0.8); amb = a;
      function bed(type, freq, q, vol, lfo) { // filtered noise: rain, wind, the sea
        var n = noise(), f = ctx.createBiquadFilter(), v = ctx.createGain(); f.type = type; f.frequency.value = freq; f.Q.value = q; v.gain.value = vol;
        n.connect(f); f.connect(v); v.connect(g); n.start(); a.nodes.push(n);
        if (lfo) { var o = ctx.createOscillator(), og = ctx.createGain(); o.frequency.value = lfo; og.gain.value = vol * 0.8; o.connect(og); og.connect(v.gain); o.start(); a.nodes.push(o); }
      }
      function every(lo, hi, fn) { (function next() { a.timers.push(setTimeout(function () { if (amb !== a) return; try { fn(); } catch (e) {} next(); }, lo + Math.random() * (hi - lo))); })(); }
      function at(f, dur, type, vol, delay, f2) { tone(f, dur, type, vol, delay, f2, g); }
      var wet = weather === 'rain' || weather === 'storm', night = time === 'night';
      if (world === 'ocean') { // aquarium: a slow sea swell and rising bubbles
        bed('lowpass', 380, 0.7, 0.05, 0.08);
        every(700, 2600, function () { var b = 2 + Math.floor(Math.random() * 4); for (var i = 0; i < b; i++) at(280 + Math.random() * 300, 0.12, 'sine', 0.035, i * 0.09, 900 + Math.random() * 500); });
        return;
      }
      if (wet) bed('lowpass', weather === 'storm' ? 900 : 1400, 0.4, weather === 'storm' ? 0.09 : 0.06);
      if (weather === 'storm') every(7000, 14000, function () { var n = noise(), f = ctx.createBiquadFilter(), v = ctx.createGain(), t = ctx.currentTime; f.type = 'lowpass'; f.frequency.value = 110; v.gain.setValueAtTime(0.0001, t); v.gain.exponentialRampToValueAtTime(0.5, t + 0.15); v.gain.exponentialRampToValueAtTime(0.0001, t + 2.6); n.connect(f); f.connect(v); v.connect(g); n.start(t); n.stop(t + 2.7); });
      if (weather === 'wind' || world === 'canyon' && !wet) bed('bandpass', 420, 0.8, weather === 'wind' ? 0.07 : 0.02, 0.13);
      if (weather === 'snow' || world === 'snow') { bed('bandpass', 900, 0.6, 0.015, 0.1); every(3500, 8000, function () { at([1568, 1760, 2093, 2349][Math.floor(Math.random() * 4)], 1.2, 'sine', 0.025); }); }
      if (night) every(500, 1300, function () { for (var i = 0; i < 3; i++) at(4300 + Math.random() * 300, 0.035, 'sine', 0.02, i * 0.06); }); // crickets
      else if (!wet && world !== 'snow' && weather !== 'snow') every(world === 'spring' ? 900 : 2200, world === 'spring' ? 3200 : 6000, function () { // birds
        var f = 2200 + Math.random() * 1600, n = 2 + Math.floor(Math.random() * 3); for (var i = 0; i < n; i++) at(f, 0.09, 'sine', 0.03, i * 0.12, f * (1.25 + Math.random() * 0.3));
      });
    }
    return { play: play, ambient: ambient, stop: stopAmb, unlock: function () { if (on()) ac(); } };
  })();
  function sceneSound() {
    var where = ['home', 'house'].filter(function (id) { return !document.getElementById(id).hidden; })[0];
    if (where && profile.sounds !== false) SFX.ambient(scene.world, scene.weather, currentTime()); else SFX.stop();
  }
  function renderSoundBtn() {
    var b = document.getElementById('soundBtn'), onn = profile.sounds !== false; if (!b) return;
    document.getElementById('soundIc').textContent = onn ? '🔊' : '🔇';
    b.setAttribute('aria-pressed', String(onn)); b.setAttribute('aria-label', onn ? 'Sounds on. Tap to mute' : 'Sounds off. Tap to turn on');
    var t = document.getElementById('setSounds'); if (t) t.checked = onn;
  }
  function setSounds(onn) { profile.sounds = onn; saveProfile(); renderSoundBtn(); if (onn) { SFX.unlock(); SFX.play('pop'); } sceneSound(); }
  document.getElementById('soundBtn').addEventListener('click', function () { setSounds(profile.sounds === false); });
  document.getElementById('setSounds').addEventListener('change', function (e) { setSounds(e.target.checked); });
  // browsers only allow sound after a tap: start the world's sound on the first one
  document.addEventListener('pointerdown', function first() { SFX.unlock(); setTimeout(sceneSound, 50); document.removeEventListener('pointerdown', first, true); }, true);
  // a soft tap on the main buttons
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.cta, [data-nav], .topic, .chip, .cq-card, .chip-btn'); if (b && b.id !== 'soundBtn') SFX.play('tap'); });
  renderSoundBtn();

  // ================= Nibb follows you and keeps busy =================""")
# sounds in the quiz, the done screen and the wheel
rep("    if (right) { firstTry++; earned += 10; burst(btn); }", "    if (right) { firstTry++; earned += 10; burst(btn); }\n    SFX.play(right ? 'right' : 'wrong');")
rep("    show('done');\n  }", "    show('done'); SFX.play('win');\n  }")
rep("    g.style.transform = 'rotate(' + wheelAngle + 'deg)';\n    setTimeout(function () {",
    "    g.style.transform = 'rotate(' + wheelAngle + 'deg)';\n    // ticks that slow down with the wheel\n    if (!still) { var tk = 0; (function tick(d) { if (tk++ > 40 || d > 600) return; SFX.play('tick'); setTimeout(function () { tick(d * 1.09); }, d); })(45); }\n    setTimeout(function () {\n      SFX.play('win');")
# the world's sound follows the screen and the scene
rep("    if (id === 'home') refreshHome();", "    if (id === 'home') refreshHome();\n    if (typeof sceneSound === 'function') setTimeout(sceneSound, 0);")
rep("          renderPicker(); buildScene(); drawNodes();\n", "          renderPicker(); buildScene(); drawNodes(); if (typeof sceneSound === 'function') sceneSound();\n")

# ---- the guided tour ----
rep("  // ---- first visit: name, age, then pick your adventure ----", r"""  // ================= guided tour: what each part of the app does =================
  // Shown once after the welcome (and once for learners from before); Me → "Show me around again" replays it.
  function tourSteps() {
    var place = COURSE === 'maths' ? 'Town' : COURSE === 'english' ? 'Library' : 'House';
    return [
      ['#courseTabs', 'Your course', 'This is the course you are doing. When you add another course in Me, a Switch button appears here.'],
      ['#startBtn', 'Start a lesson', 'Tap here for your next lesson. Nibb teaches it on the board, out loud, then asks a few questions.'],
      ['#topics', 'Your path', 'All the lessons, in order. Done ones get a tick. Tap one to play it again.'],
      ['[data-nav="house"]', 'Your ' + place.toLowerCase(), 'Every lesson builds something. After a lesson you build it yourself, like a puzzle, and it appears here.'],
      ['[data-nav="cards"]', 'Flashcards', 'Cards help you remember what you learned. A few minutes a day is plenty.'],
      ['#prizeTile', 'Prize wheel', 'Lessons give you embers. Fill the jar, then spin the wheel to win a prize a grown-up picks.'],
      ['#sceneBtn', 'Your world', 'Change the world, the weather and the time of day. Your house or town changes too.'],
      ['#soundBtn', 'Sounds', 'Birds, rain and cheers. Tap here to turn sounds off or on.'],
      ['[data-nav="me"]', 'Me', 'Your name, Nibb\'s name, your courses, prizes and settings. You can watch this tour again there.']
    ];
  }
  function startTour() {
    show('home'); document.getElementById('homeScroll') && (document.getElementById('homeScroll').scrollTop = 0);
    var steps = tourSteps().filter(function (st) { var el = document.querySelector('#home ' + st[0]) || document.querySelector(st[0]); return el && el.getClientRects().length; }), k = 0;
    var ov = document.createElement('div'); ov.className = 'tour'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Tour of the app');
    ov.innerHTML = '<div class="tour-ring"></div><div class="tour-card"><div class="tc-top"><svg viewBox="0 0 120 110" aria-hidden="true">' + lumiSVG('happy') + '</svg><div><h3></h3><p></p></div></div><div class="tc-row"><span class="tc-dots"></span><button class="tc-skip" type="button">Skip</button><button class="tc-next" type="button">Next</button></div></div>';
    document.body.appendChild(ov);
    var ring = ov.querySelector('.tour-ring'), card = ov.querySelector('.tour-card');
    function end() { ov.remove(); profile.toured = true; saveProfile(); window.removeEventListener('resize', place); }
    function place() {
      var st = steps[k], el = document.querySelector('#home ' + st[0]) || document.querySelector(st[0]);
      el.scrollIntoView({ block: 'center', behavior: 'instant' in document.documentElement.style ? 'instant' : 'auto' });
      var r = el.getBoundingClientRect(), pad = 6;
      ring.style.left = (r.left - pad) + 'px'; ring.style.top = (r.top - pad) + 'px'; ring.style.width = (r.width + pad * 2) + 'px'; ring.style.height = (r.height + pad * 2) + 'px';
      var below = r.top + r.height / 2 < window.innerHeight / 2;
      card.style.top = below ? Math.min(window.innerHeight - 200, r.bottom + 16) + 'px' : 'auto';
      card.style.bottom = below ? 'auto' : Math.min(window.innerHeight - 200, window.innerHeight - r.top + 16) + 'px';
      card.querySelector('h3').textContent = st[1]; card.querySelector('p').textContent = st[2];
      card.querySelector('.tc-dots').innerHTML = steps.map(function (x, i) { return '<i class="' + (i === k ? 'on' : '') + '"></i>'; }).join('');
      card.querySelector('.tc-next').textContent = k === steps.length - 1 ? 'Let\'s learn!' : 'Next';
      card.querySelector('.tc-next').focus({ preventScroll: true });
    }
    card.querySelector('.tc-next').addEventListener('click', function () { if (++k >= steps.length) { end(); SFX.play('win'); } else { SFX.play('whoosh'); place(); } });
    card.querySelector('.tc-skip').addEventListener('click', end);
    ov.addEventListener('keydown', function (e) { if (e.key === 'Escape') end(); });
    window.addEventListener('resize', place);
    setTimeout(place, 60);
  }
  document.getElementById('tourAgain').addEventListener('click', startTour);

  // ---- first visit: name, age, then pick your adventure ----""")
rep("    profile.courses = []; joinCourse(wlChoice); profile.onboarded = true; saveProfile(); saveProgress(); show('home');",
    "    profile.courses = []; joinCourse(wlChoice); profile.onboarded = true; saveProfile(); saveProgress(); show('home'); applyProfile();\n    setTimeout(startTour, 700);")
rep("  if (FIRST_RUN) startWelcome(); else show('home');",
    "  if (FIRST_RUN) startWelcome(); else { show('home'); if (!profile.toured && !/[?&]notour\\b/.test(location.search)) setTimeout(startTour, 1200); }")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
