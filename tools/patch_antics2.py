# Robot name: no default 'Nibb' suggestion - pick from fresh ideas, roll a surprise, or type your own.
# Shows: only in the empty sky around the robot (never over cards or text), a new dig show, and the rocket ends in smoke.
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- 1. naming the robot ----------------
rep("""        <input id="wlTeachIn" maxlength="14" autocomplete="off" aria-label="Your teacher's name">
        <div class="wl-names" id="wlNames"></div>
        <button class="cta" id="wlTeachGo" type="button">Next</button>""",
    """        <input id="wlTeachIn" maxlength="14" autocomplete="off" aria-label="Your teacher's name" placeholder="Type a name">
        <div class="wl-names" id="wlNames"></div>
        <button class="chip-btn ghost" id="wlRoll" type="button">🎲 Surprise me</button>
        <button class="cta" id="wlTeachGo" type="button" disabled>Next</button>""")
rep("  var TEACHER_IDEAS = ['Nibb', 'Robo', 'Pixel', 'Sparky', 'Bolt', 'Luna', 'Zippy', 'Chip'];",
    "  var TEACHER_IDEAS = ['Robo', 'Pixel', 'Sparky', 'Bolt', 'Luna', 'Zippy', 'Chip', 'Beep'];\n  var TEACHER_MORE = ['Gizmo', 'Nova', 'Tinker', 'Comet', 'Bleep', 'Dot', 'Widget', 'Ziggy', 'Echo', 'Sprocket', 'Bubbles', 'Rusty', 'Orbit', 'Twinkle', 'Cosmo', 'Buzz'];")
rep("""    inp.value = profile.teacher || 'Nibb'; box.innerHTML = '';
    function mark() { box.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.textContent === inp.value.trim())); }); }""",
    """    inp.value = profile.teacher && profile.teacher !== 'Nibb' ? profile.teacher : ''; box.innerHTML = '';
    var go = document.getElementById('wlTeachGo');
    function mark() { box.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.textContent === inp.value.trim())); }); go.disabled = !inp.value.trim(); }
    document.getElementById('wlRoll').onclick = function () { var all = TEACHER_IDEAS.concat(TEACHER_MORE).filter(function (n) { return n !== inp.value; }); inp.value = all[Math.floor(Math.random() * all.length)]; mark(); SFX.play('pop'); };""")
rep("  function wlTeach() { var v = setTeacher(", "  function wlTeach() { if (!document.getElementById('wlTeachIn').value.trim()) return; var v = setTeacher(")

# ---------------- 2. shows stay in the empty sky ----------------
# the free box: the hero area (where Nibb floats) between the top bar and the course banner; the usual bubble hides meanwhile
rep("""  function stageShow(run) {
    var lumi = document.getElementById('homeLumi'), r = lumi.getBoundingClientRect();
    if (!r.width || r.bottom < 0 || r.top > window.innerHeight) return false; // only when Nibb is on screen""",
    """  function freeBox() {
    var hero = document.getElementById('homeHero').getBoundingClientRect(), top = document.querySelector('#home .topbar').getBoundingClientRect().bottom + 6;
    var ct = document.getElementById('courseTabs').getBoundingClientRect(), bottom = (ct.height ? ct.top : hero.bottom) - 6;
    return { left: Math.max(8, hero.left), right: Math.min(window.innerWidth - 8, hero.right), top: Math.max(8, top), bottom: Math.min(window.innerHeight - 8, bottom) };
  }
  function stageShow(run) {
    var lumi = document.getElementById('homeLumi'), r = lumi.getBoundingClientRect(), box = freeBox();
    // only when Nibb is in its own spot in the sky, and that empty space is on screen and big enough
    if (buddyMode !== 'hero' || !r.width || r.top < box.top - 4 || r.bottom > box.bottom + 4 || box.bottom - box.top < r.height + 30 || box.right - box.left < r.width * 2.4) return false;""")
rep("""    function done() { st.remove(); buddy.style.visibility = ''; showing = false; }""",
    """    var hb = document.getElementById('homeBubble'); hb.style.visibility = 'hidden';
    function done() { st.remove(); buddy.style.visibility = ''; hb.style.visibility = ''; showing = false; }""")
# the show's own bubble sits inside the free box
rep("""      var x = r.left + r.width + 8, w = Math.min(220, window.innerWidth - 24); if (x + w > window.innerWidth - 12) x = Math.max(12, r.left - w - 8);
      bubble.style.left = x + 'px'; bubble.style.top = Math.max(12, r.top - 10) + 'px';""",
    """      var w = Math.min(200, box.right - box.left - 16); bubble.style.maxWidth = w + 'px';
      var x = r.left + r.width + 8; if (x + w > box.right) x = Math.max(box.left, r.left - w - 8);
      if (x + w > box.right && x <= box.left) x = box.left; // narrow: above Nibb instead
      bubble.style.left = x + 'px'; bubble.style.top = Math.max(box.top, r.top - 6) + 'px';""")
rep("    try { run({ st: st, actor: actor, r: r, prop: prop, done: done, say: say, W: window.innerWidth, H: window.innerHeight }); } catch (e) { done(); }",
    "    // keep everything in the free box: nothing crosses the cards or text below\n    st.style.clipPath = 'inset(' + box.top + 'px ' + (window.innerWidth - box.right) + 'px ' + (window.innerHeight - box.bottom) + 'px ' + box.left + 'px round 18px)';\n    try { run({ st: st, actor: actor, r: r, prop: prop, done: done, say: say, box: box, W: window.innerWidth, H: window.innerHeight }); } catch (e) { done(); }")
# roam: points inside the box
rep("      for (var i = 0; i < 4; i++) pts.push([Math.random() * (k.W - k.r.width) - x0, Math.max(60, Math.random() * (k.H * 0.6)) - y0]);",
    "      for (var i = 0; i < 4; i++) pts.push([k.box.left + Math.random() * Math.max(0, k.box.right - k.box.left - k.r.width) - x0, k.box.top + Math.random() * Math.max(0, k.box.bottom - k.box.top - k.r.height) - y0]);")
# doors: both inside the box, on opposite sides
rep("""      var left = k.r.left > k.W / 2, d1x = left ? Math.max(8, k.r.left - 90) : Math.min(k.W - 70, k.r.right + 30), d1y = k.r.top + 10;
      var d2x = left ? Math.min(k.W - 74, k.W * 0.82) : Math.max(8, k.W * 0.08), d2y = Math.max(70, Math.min(k.H - 220, k.r.top + (Math.random() < 0.5 ? -140 : 160)));""",
    """      var B = k.box, mid = (B.left + B.right) / 2, left = k.r.left + k.r.width / 2 > mid;
      var d1x = left ? Math.max(B.left + 4, k.r.left - 80) : Math.min(B.right - 64, k.r.right + 16), d1y = Math.min(B.bottom - 80, k.r.top + 6);
      var d2x = left ? B.left + 6 : B.right - 66, d2y = B.top + Math.random() * Math.max(0, B.bottom - B.top - 80);""")
# rocket: comes in from the side of the box, and puffs into smoke instead of exploding
a = s.index("    rocket: function (k) {"); b = s.index("  // the BOOM itself")
s = s[:a] + r"""    rocket: function (k) {
      var B = k.box, cx = k.r.left + k.r.width / 2, cy = k.r.top + k.r.height / 2, fromLeft = cx > (B.left + B.right) / 2, sx = fromLeft ? B.left - 60 : B.right, sy = B.top + 4;
      var rk = k.prop('🚀', sx, sy); rk.style.fontSize = '50px';
      var ang = Math.atan2(cy - sy, (cx - 25) - sx) * 180 / Math.PI + 45; // the emoji points up and to the right
      k.say('Uh oh... is that a rocket?!');
      anim(rk, [{ transform: 'translate(0,0) rotate(' + ang + 'deg)' }, { transform: 'translate(' + (cx - 25 - sx) + 'px,' + (cy - 25 - sy) + 'px) rotate(' + ang + 'deg)' }], 1300, 'ease-in');
      SFX.play('whoosh');
      setTimeout(function () {
        rk.remove();
        // a big soft cloud of smoke, not an explosion
        for (var i = 0; i < 9; i++) { var c = k.prop(i % 3 ? '☁️' : '💨', cx - 22 + (Math.random() - 0.5) * 30, cy - 26 + (Math.random() - 0.5) * 24), a2 = Math.random() * 6.28, d = 25 + Math.random() * 45;
          c.style.fontSize = (34 + Math.random() * 22) + 'px'; c.style.filter = 'grayscale(1) brightness(.85)';
          anim(c, [{ transform: 'translate(0,0) scale(.3)', opacity: .95 }, { transform: 'translate(' + Math.cos(a2) * d + 'px,' + (Math.sin(a2) * d - 30) + 'px) scale(1.4)', opacity: .9, offset: 0.4 }, { transform: 'translate(' + Math.cos(a2) * d * 1.4 + 'px,' + (Math.sin(a2) * d - 70) + 'px) scale(1.8)', opacity: 0 }], 2200, 'ease-out'); }
        SFX.play('whoosh'); k.actor.style.filter = 'brightness(.45) saturate(.3)';
        anim(k.actor, [{ transform: 'translate(0,0)' }, { transform: 'translate(-5px,1px) rotate(-6deg)' }, { transform: 'translate(5px,-1px) rotate(6deg)' }, { transform: 'translate(-3px,0) rotate(-3deg)' }, { transform: 'translate(0,0)' }], 700);
        k.say(['Cough cough! Who ordered the smoke?', 'Puff! ...I\'m okay! Just a bit sooty.', 'Cough... that was NOT in the lesson plan.'][Math.floor(Math.random() * 3)]);
        setTimeout(function () { k.actor.style.transition = 'filter .9s'; k.actor.style.filter = ''; anim(k.actor, [{ transform: 'scale(1)' }, { transform: 'scale(1.12) rotate(10deg)' }, { transform: 'scale(1)' }], 600); }, 1500);
        setTimeout(k.done, 2500);
      }, 1300);
    },
    dig: function (k) {
      var cx = k.r.left + k.r.width / 2, gy = Math.min(k.box.bottom - 34, k.r.bottom - 6);
      k.say(['Dig, dig, dig! I think there\'s treasure here!', 'X marks the spot!', 'Digging for buried treasure!'][Math.floor(Math.random() * 3)]);
      var hole = k.prop('🕳️', cx - 26, gy - 14); hole.style.fontSize = '52px'; anim(hole, [{ opacity: 0, transform: 'scale(.3)' }, { opacity: 1, transform: 'scale(1)' }], 500);
      var sh = k.prop('⛏️', cx + 14, k.r.top + 10, 'small'); sh.style.fontSize = '34px';
      anim(sh, [0, 1, 2, 3, 4, 5, 6, 7].map(function (i) { return { transform: 'rotate(' + (i % 2 ? 40 : -20) + 'deg) translateY(' + (i % 2 ? 14 : 0) + 'px)' }; }), 2400);
      anim(k.actor, [0, 1, 2, 3, 4, 5, 6, 7].map(function (i) { return { transform: 'translateY(' + (i % 2 ? 8 : 0) + 'px) rotate(' + (i % 2 ? 6 : 0) + 'deg)' }; }), 2400);
      for (var i = 0; i < 10; i++) (function (i) { var d = k.prop(['🟫', '🪨', '🟤'][i % 3], cx - 8, gy - 6, 'small'); d.style.fontSize = '14px'; d.style.opacity = 0;
        var dx = (i % 2 ? 1 : -1) * (20 + Math.random() * 40); anim(d, [{ opacity: 1, transform: 'translate(0,0)' }, { opacity: 1, transform: 'translate(' + dx / 2 + 'px,-40px)', offset: 0.5 }, { opacity: 0, transform: 'translate(' + dx + 'px,0)' }], 700).startTime = document.timeline.currentTime + i * 220; })(i);
      for (var j = 0; j < 5; j++) setTimeout(function () { SFX.play('tick'); }, j * 480);
      setTimeout(function () {
        var found = ['💎', '🦴', '🪙', '🗝️', '🧸'][Math.floor(Math.random() * 5)], t = k.prop(found, cx - 22, gy - 20); t.style.fontSize = '44px';
        anim(t, [{ transform: 'translateY(0) scale(.4)', opacity: 0 }, { transform: 'translateY(-60px) scale(1.2)', opacity: 1, offset: 0.5 }, { transform: 'translateY(-50px) scale(1)', opacity: 1 }], 800, 'cubic-bezier(.3,1.5,.5,1)');
        SFX.play('right'); sh.remove();
        k.say({ '💎': 'A diamond! Shiny!', '🦴': 'A bone?! Who buried this?', '🪙': 'A gold coin! I\'m rich!', '🗝️': 'A key! I wonder what it opens...', '🧸': 'My old teddy! I missed you!' }[found]);
        anim(k.actor, [{ transform: 'translateY(0)' }, { transform: 'translateY(-16px)' }, { transform: 'translateY(0)' }], 500);
      }, 2500);
      setTimeout(k.done, 4300);
    }
  };
""" + s[b:]
rep("  function boom() { SFX.play('whoosh'); SFX.play('wrong'); }", "  function boom() { SFX.play('whoosh'); }")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
