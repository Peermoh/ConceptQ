# 1. Python opens at age 12; younger learners need a grown-up to answer a harder question first.
# 2. The robot's antics on Home every 4 to 10 seconds: dancing, a bath, roaming, in one door and out of another,
#    a rocket that flies in and goes BOOM, plus the naps and tricks it already had.
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

# ---------------- 1. coding from 12 ----------------
rep("    py:      { emoji: '🏠', name: 'Python', world: 'Build your dream house', tag: 'Real code, one room at a time', builds: ['🛋️', '🪜', '🌻', '💡'], c1: '#FFC861', c2: '#FF7A6B', minAge: 8, maxAge: 18, extra: '4 levels' },",
    "    py:      { emoji: '🏠', name: 'Python', world: 'Build your dream house', tag: 'Real code, one room at a time', builds: ['🛋️', '🪜', '🌻', '💡'], c1: '#FFC861', c2: '#FF7A6B', minAge: 12, maxAge: 18, extra: '4 levels' },")
rep("{ id: 'py',    name: 'Python',          ic: 'Py',     bg: '#FFB547', minAge: 8,", "{ id: 'py',    name: 'Python',          ic: 'Py',     bg: '#FFB547', minAge: 12,")
rep("  // join a course (if new) and make it the one on Home", r"""  // Coding is for age 12 and up. A younger learner can still have it, once a grown-up answers a harder question.
  function needsGrownUp(cid) { return cid === 'py' && profile.age < 12 && (profile.courses || []).indexOf('py') < 0; }
  function adultGate(why, then) {
    var a = 12 + Math.floor(Math.random() * 8), b = 6 + Math.floor(Math.random() * 4), c = 3 + Math.floor(Math.random() * 7), ans = a * b + c;
    var ov = document.createElement('div'); ov.className = 'wheel-dlg'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-labelledby', 'agH');
    ov.innerHTML = '<div class="wheel-card"><h2 class="title-xl" id="agH">Grown-ups only</h2><p class="wheel-info"></p>' +
      '<label class="field"><span>What is ' + a + ' × ' + b + ' + ' + c + '?</span><input inputmode="numeric" autocomplete="off" id="agIn"></label>' +
      '<span class="gate-msg" aria-live="polite"></span><button class="cta mint" style="width:100%" type="button" id="agOk">Check</button><button class="cta" style="width:100%" type="button" id="agNo">Not now</button></div>';
    ov.querySelector('.wheel-info').textContent = why;
    document.body.appendChild(ov);
    var inp = ov.querySelector('#agIn'); setTimeout(function () { inp.focus(); }, 30);
    function ok() { if (parseInt(inp.value, 10) === ans) { ov.remove(); then(); } else { ov.querySelector('.gate-msg').textContent = 'Not quite. Ask a grown-up to help.'; inp.select(); } }
    ov.querySelector('#agOk').addEventListener('click', ok);
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') ok(); });
    ov.querySelector('#agNo').addEventListener('click', function () { ov.remove(); });
  }
  function askForCourse(cid, then) {
    if (!needsGrownUp(cid)) { then(); return; }
    adultGate('Coding with Python is made for age 12 and up. A grown-up can still open it for a younger learner.', then);
  }
  // join a course (if new) and make it the one on Home""")
# every place a course can be chosen goes through askForCourse
rep("      var c = courseCard(cid, 'go'); c.addEventListener('click', function () { joinCourse(cid); show('home'); }); cards.appendChild(c);",
    "      var c = courseCard(cid, 'go'); c.addEventListener('click', function () { askForCourse(cid, function () { joinCourse(cid); show('home'); }); }); cards.appendChild(c);")
rep("      btn.addEventListener('click', function () { joinCourse(cid); show('home'); });",
    "      btn.addEventListener('click', function () { askForCourse(cid, function () { joinCourse(cid); show('home'); }); });")
rep("""      c.addEventListener('click', function () {
        wlChoice = cid; box.querySelectorAll('.cq-card').forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
        go.disabled = false; go.textContent = 'Let\\'s go: ' + CQ_COURSES[cid].world + '!';
      });""",
"""      c.addEventListener('click', function () {
        askForCourse(cid, function () {
          wlChoice = cid; box.querySelectorAll('.cq-card').forEach(function (x) { x.setAttribute('aria-pressed', String(x === c)); });
          go.disabled = false; go.textContent = 'Let\\'s go: ' + CQ_COURSES[cid].world + '!';
        });
      });""")
# the card says when a grown-up is needed
rep("""(m.maxAge >= 18 ? 'Age ' + m.minAge + '+' : 'Age ' + m.minAge + '–' + m.maxAge) + '</span></div>' +""",
    """(m.maxAge >= 18 ? 'Age ' + m.minAge + '+' : 'Age ' + m.minAge + '–' + m.maxAge) + '</span>' + (needsGrownUp(cid) ? '<span>🔒 Ask a grown-up</span>' : '') + '</div>' +""")

# ---------------- 2. antics ----------------
rep("#houseFrame { flex: 1;", r"""/* ---- the robot's antics: a copy of the robot acts out a little show over the page ---- */
.antics { position: fixed; inset: 0; z-index: 40; pointer-events: none; overflow: hidden; }
.antics .actor { position: absolute; width: 96px; height: 88px; will-change: transform; }
.antics .actor svg { width: 100%; height: 100%; display: block; }
.antics .prop { position: absolute; font-size: 54px; line-height: 1; will-change: transform, opacity; }
.antics .prop.small { font-size: 26px; }
.antics .boom { font-size: 120px; }
#houseFrame { flex: 1;""")
rep("  // every 4 to 15 quiet seconds Nibb does something: naps under a blanket, or one of his tricks\n  var idleTimer = 0;\n  function scheduleIdle() { clearTimeout(idleTimer); idleTimer = setTimeout(doIdle, 4000 + Math.random() * 11000); }",
r"""  // every 4 to 10 quiet seconds Nibb does something: a nap, a trick, or one of the bigger shows below
  var idleTimer = 0, showing = false;
  function scheduleIdle() { clearTimeout(idleTimer); idleTimer = setTimeout(doIdle, 4000 + Math.random() * 6000); }
  // ---- the shows: a copy of Nibb acts them out on a layer over the page, then the real Nibb comes back ----
  function busyScreen() { return document.querySelector('.tour, .wheel-dlg:not([hidden]), .pz') || !document.getElementById('wheelDlg').hidden; }
  function stageShow(run) {
    var lumi = document.getElementById('homeLumi'), r = lumi.getBoundingClientRect();
    if (!r.width || r.bottom < 0 || r.top > window.innerHeight) return false; // only when Nibb is on screen
    showing = true;
    var st = document.createElement('div'); st.className = 'antics'; st.setAttribute('aria-hidden', 'true'); document.body.appendChild(st);
    var actor = document.createElement('div'); actor.className = 'actor'; actor.innerHTML = '<svg viewBox="0 0 120 110">' + lumiSVG('happy') + '</svg>';
    actor.style.width = r.width + 'px'; actor.style.height = r.height + 'px'; actor.style.left = r.left + 'px'; actor.style.top = r.top + 'px';
    st.appendChild(actor); buddy.style.visibility = 'hidden';
    function prop(txt, x, y, cls) { var p = document.createElement('div'); p.className = 'prop' + (cls ? ' ' + cls : ''); p.textContent = txt; p.style.left = x + 'px'; p.style.top = y + 'px'; st.appendChild(p); return p; }
    function done() { st.remove(); buddy.style.visibility = ''; showing = false; }
    try { run({ st: st, actor: actor, r: r, prop: prop, done: done, W: window.innerWidth, H: window.innerHeight }); } catch (e) { done(); }
    return true;
  }
  function anim(el, frames, ms, ease) { return el.animate(frames, { duration: ms, easing: ease || 'ease-in-out', fill: 'forwards' }); }
  var SHOWS = {
    dance: function (k) {
      homeSay(['Dance break!', 'Can\'t stop the beat!', 'Robot moves, activate!'][Math.floor(Math.random() * 3)]);
      anim(k.actor, [0, 1, 2, 3, 4, 5, 6, 7, 8].map(function (i) { return { transform: 'translateY(' + (i % 2 ? -18 : 0) + 'px) rotate(' + [0, -14, 0, 14, 0, -14, 0, 14, 0][i] + 'deg) scaleX(' + (i > 3 && i < 8 ? -1 : 1) + ')' }; }), 2600);
      for (var i = 0; i < 6; i++) (function (i) { var n = k.prop(['🎵', '🎶'][i % 2], k.r.left + k.r.width / 2 + (i % 2 ? 20 : -40), k.r.top, 'small'); anim(n, [{ opacity: 0, transform: 'translate(0,0)' }, { opacity: 1, offset: 0.2 }, { opacity: 0, transform: 'translate(' + (i % 2 ? 30 : -30) + 'px,-90px) rotate(' + (i % 2 ? 20 : -20) + 'deg)' }], 1300).startTime = document.timeline.currentTime + i * 380; })(i);
      [523, 659, 784, 659, 523, 784, 880, 784].forEach(function (f, i) { setTimeout(function () { SFX.play('tick'); }, i * 320); });
      setTimeout(k.done, 2800);
    },
    bath: function (k) {
      homeSay(['Rub-a-dub-dub, a robot in a tub!', 'Bath time! Even robots need a polish.', 'Bubbles! So many bubbles!'][Math.floor(Math.random() * 3)]);
      var cx = k.r.left + k.r.width / 2, by = k.r.top + k.r.height * 0.55;
      var tub = k.prop('🛁', cx - 44, by - 6); tub.style.fontSize = '88px'; anim(tub, [{ opacity: 0, transform: 'scale(.3)' }, { opacity: 1, transform: 'scale(1)' }], 400, 'cubic-bezier(.3,1.5,.5,1)');
      anim(k.actor, [{ transform: 'translateY(0) scale(1)' }, { transform: 'translateY(26px) scale(.78)', offset: 0.15 }, { transform: 'translateY(22px) scale(.78) rotate(-6deg)', offset: 0.35 }, { transform: 'translateY(26px) scale(.78) rotate(6deg)', offset: 0.6 }, { transform: 'translateY(24px) scale(.78)', offset: 0.85 }, { transform: 'translateY(0) scale(1)' }], 3600);
      var duck = k.prop('🦆', cx + 22, by + 4, 'small'); anim(duck, [{ opacity: 0 }, { opacity: 1, offset: 0.15 }, { transform: 'translateX(-30px)', offset: 0.6 }, { opacity: 1, offset: 0.85 }, { opacity: 0, transform: 'translateX(-10px)' }], 3600);
      for (var i = 0; i < 9; i++) (function (i) { var b = k.prop('🫧', cx - 40 + Math.random() * 80, by, 'small'); b.style.opacity = 0; anim(b, [{ opacity: 0, transform: 'translateY(0) scale(.5)' }, { opacity: 1, offset: 0.2 }, { opacity: 0, transform: 'translateY(-' + (60 + Math.random() * 60) + 'px) scale(1.2)' }], 1400).startTime = document.timeline.currentTime + 200 + i * 300; })(i);
      for (var j = 0; j < 4; j++) setTimeout(function () { SFX.play('pop'); }, 400 + j * 700);
      setTimeout(function () { anim(tub, [{ opacity: 1 }, { opacity: 0, transform: 'scale(.5)' }], 300); }, 3300);
      setTimeout(k.done, 3700);
    },
    roam: function (k) {
      homeSay(['Just stretching my wings!', 'Wheee!', 'Exploring!'][Math.floor(Math.random() * 3)]);
      var pts = [[0, 0]], x0 = k.r.left, y0 = k.r.top;
      for (var i = 0; i < 4; i++) pts.push([Math.random() * (k.W - k.r.width) - x0, Math.max(60, Math.random() * (k.H * 0.6)) - y0]);
      pts.push([0, 0]);
      anim(k.actor, pts.map(function (p, i) { return { transform: 'translate(' + p[0] + 'px,' + p[1] + 'px) rotate(' + (i % 2 ? 12 : -12) + 'deg)' }; }), 4200);
      SFX.play('whoosh'); setTimeout(function () { SFX.play('whoosh'); }, 2000);
      setTimeout(k.done, 4300);
    },
    doors: function (k) {
      homeSay(['Knock knock! Who\'s there? Me!', 'I know a shortcut...', 'Be right back!'][Math.floor(Math.random() * 3)]);
      var left = k.r.left > k.W / 2, d1x = left ? Math.max(8, k.r.left - 90) : Math.min(k.W - 70, k.r.right + 30), d1y = k.r.top + 10;
      var d2x = left ? Math.min(k.W - 74, k.W * 0.82) : Math.max(8, k.W * 0.08), d2y = Math.max(70, Math.min(k.H - 220, k.r.top + (Math.random() < 0.5 ? -140 : 160)));
      var d1 = k.prop('🚪', d1x, d1y), d2 = k.prop('🚪', d2x, d2y); [d1, d2].forEach(function (d) { d.style.fontSize = '70px'; d.style.opacity = 0; });
      anim(d1, [{ opacity: 0, transform: 'scale(.4)' }, { opacity: 1, transform: 'scale(1)' }], 300);
      var dx1 = d1x - k.r.left, dy1 = d1y - k.r.top, dx2 = d2x - k.r.left, dy2 = d2y - k.r.top;
      anim(k.actor, [{ transform: 'translate(0,0) scale(1)', opacity: 1 }, { transform: 'translate(' + dx1 + 'px,' + dy1 + 'px) scale(.55)', opacity: 1, offset: 0.25 }, { transform: 'translate(' + dx1 + 'px,' + dy1 + 'px) scale(.2)', opacity: 0, offset: 0.33 },
        { transform: 'translate(' + dx2 + 'px,' + dy2 + 'px) scale(.2)', opacity: 0, offset: 0.55 }, { transform: 'translate(' + dx2 + 'px,' + dy2 + 'px) scale(.7)', opacity: 1, offset: 0.65 }, { transform: 'translate(0,0) scale(1)', opacity: 1 }], 4200);
      setTimeout(function () { SFX.play('tick'); anim(d1, [{ opacity: 1 }, { opacity: 0, transform: 'scale(.4)' }], 300); anim(d2, [{ opacity: 0, transform: 'scale(.4)' }, { opacity: 1, transform: 'scale(1)' }], 300); }, 1450);
      setTimeout(function () { SFX.play('pop'); homeSay('Ta-da! Out the other door!'); }, 2650);
      setTimeout(function () { anim(d2, [{ opacity: 1 }, { opacity: 0, transform: 'scale(.4)' }], 300); }, 3200);
      setTimeout(k.done, 4300);
    },
    rocket: function (k) {
      var cx = k.r.left + k.r.width / 2, cy = k.r.top + k.r.height / 2, fromLeft = cx > k.W / 2, sx = fromLeft ? -80 : k.W + 20, sy = Math.max(20, cy - 220);
      var rk = k.prop('🚀', sx, sy); rk.style.fontSize = '58px';
      var ang = Math.atan2(cy - sy, (cx - 29) - sx) * 180 / Math.PI + 45; // the emoji points up and to the right
      homeSay('Uh oh... is that a rocket?!');
      anim(rk, [{ transform: 'translate(0,0) rotate(' + ang + 'deg)' }, { transform: 'translate(' + (cx - 29 - sx) + 'px,' + (cy - 29 - sy) + 'px) rotate(' + ang + 'deg)' }], 1300, 'ease-in');
      SFX.play('whoosh'); setTimeout(function () { SFX.play('whoosh'); }, 600);
      setTimeout(function () {
        rk.remove();
        var b = k.prop('💥', cx - 60, cy - 70, 'boom'); anim(b, [{ transform: 'scale(.2)', opacity: 1 }, { transform: 'scale(1.3)', opacity: 1, offset: 0.4 }, { transform: 'scale(1.6)', opacity: 0 }], 900, 'ease-out');
        for (var i = 0; i < 6; i++) { var sm = k.prop(['💨', '⭐', '✨'][i % 3], cx - 12, cy - 12, 'small'), a = i / 6 * 6.28; anim(sm, [{ transform: 'translate(0,0)', opacity: 1 }, { transform: 'translate(' + Math.cos(a) * 90 + 'px,' + Math.sin(a) * 90 + 'px)', opacity: 0 }], 900, 'ease-out'); }
        boom(); k.actor.style.filter = 'brightness(.35) saturate(.4)';
        anim(k.actor, [{ transform: 'translate(0,0)' }, { transform: 'translate(-6px,2px) rotate(-8deg)' }, { transform: 'translate(6px,-2px) rotate(8deg)' }, { transform: 'translate(-4px,0) rotate(-4deg)' }, { transform: 'translate(0,0)' }], 700);
        homeSay(['BOOM! ...I\'m okay!', 'Ka-BOOM! Who ordered that?', 'Cough cough... that was NOT in the lesson plan.'][Math.floor(Math.random() * 3)]);
        setTimeout(function () { k.actor.style.transition = 'filter .8s'; k.actor.style.filter = ''; anim(k.actor, [{ transform: 'scale(1)' }, { transform: 'scale(1.15) rotate(10deg)' }, { transform: 'scale(1)' }], 600); }, 1400);
        setTimeout(k.done, 2400);
      }, 1300);
    }
  };
  // the BOOM itself (a burst of low noise), only when sounds are on
  function boom() { SFX.play('whoosh'); SFX.play('wrong'); }
  function playShow() {
    var names = Object.keys(SHOWS), n = names[Math.floor(Math.random() * names.length)];
    if (n === playShow.last) n = names[(names.indexOf(n) + 1) % names.length]; playShow.last = n;
    return stageShow(SHOWS[n]);
  }""")
rep("    if (!profile.antics || document.getElementById('home').hidden || document.hidden || lumi._act || sleeping) { scheduleIdle(); return; }\n    if (Math.random() < 0.4) napBuddy(); else playAct(lumi);",
    "    if (!profile.antics || still || document.getElementById('home').hidden || document.hidden || lumi._act || sleeping || showing || busyScreen()) { scheduleIdle(); return; }\n    var roll = Math.random();\n    if (roll < 0.2) napBuddy(); else if (roll < 0.4 || !playShow()) playAct(lumi);")
rep("<span>Nibb naps and does tricks on Home</span>", "<span>Nibb naps, dances, takes baths and does tricks on Home</span>")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
