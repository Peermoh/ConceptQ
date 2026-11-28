# Quiz read-aloud: play the recorded pieces through WebAudio, decoded once and scheduled back to back, so a sentence
# built from several files has no pauses while the player loads. The <audio> player stays as the fallback.
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prototype', 'index.html'); h = open(P).read()
def rep(a, b):
    global h
    if b in h: return
    assert h.count(a) == 1, a[:80]; h = h.replace(a, b)
rep("""    var files = []; seq.forEach(function (x) { if (files.indexOf(x.sg[0]) < 0) files.push(x.sg[0]); });
    var live = function () { return playPhon.tok === tok && Q[qi] === q && !document.getElementById('quiz').hidden; };
    var hush = function () { if (QV.owner === tok) qvEl.pause(); }; // a newer reading may own the player now: leave it alone
    Promise.all(""", """    var files = []; seq.forEach(function (x) { if (files.indexOf(x.sg[0]) < 0) files.push(x.sg[0]); });
    var live = function () { return playPhon.tok === tok && Q[qi] === q && !document.getElementById('quiz').hidden; };
    var hush = function () { if (QV.owner === tok) qvEl.pause(); }; // a newer reading may own the player now: leave it alone
    qvStop();
    var ctx = qvContext();
    if (ctx) { // decoded once, then scheduled back to back: no pause while a file loads
      Promise.all(files.map(function (f) { return qvDecode('audio/quiz/' + who + '/' + f + '.mp3'); })).then(function (bufs) {
        if (!live()) return;
        if (ctx.state === 'suspended') try { ctx.resume(); } catch (e) {}
        var t = ctx.currentTime + 0.06, srcs = []; QV.srcs = srcs;
        seq.forEach(function (it, i) {
          var b = bufs[files.indexOf(it.sg[0])], dur = Math.max(0.05, it.sg[2] - it.sg[1]);
          if (i) t += it.first ? 0.38 : 0.03;
          var s = ctx.createBufferSource(); s.buffer = b; s._qv = true; s.connect(ctx.destination); s.start(t, it.sg[1], dur); srcs.push(s);
          if (it.first) (function (k, at) { setTimeout(function () { if (QV.srcs === srcs && live()) qPoint(k - 1); }, Math.max(0, (at - ctx.currentTime) * 1000)); })(it.k, t); // the robot goes to what is being read
          t += dur;
        });
        setTimeout(function () { if (QV.srcs !== srcs) return; QV.srcs = []; if (live() && answers[qi] === undefined) qPoint(-2); }, Math.max(0, (t - ctx.currentTime) * 1000) + 60);
        (function watch() { if (QV.srcs !== srcs) return; if (!live()) { qvStop(); return; } setTimeout(watch, 120); })();
      }).catch(function () { if (live()) deviceRead(); });
      return true;
    }
    Promise.all(""")
rep("""  function hearRecorded(q, man, deviceRead) {""", """  // WebAudio for the read-aloud: one context, each file decoded once
  var qvCtx = null, qvBuf = {};
  function qvContext() { if (!qvCtx) { var AC = window.AudioContext || window.webkitAudioContext; if (AC) try { qvCtx = new AC(); } catch (e) { qvCtx = null; } } return qvCtx; }
  function qvDecode(url) {
    if (!qvBuf[url]) qvBuf[url] = fetch(url).then(function (r) { if (!r.ok) throw new Error('missing'); return r.arrayBuffer(); })
      .then(function (ab) { return new Promise(function (res, rej) { qvCtx.decodeAudioData(ab, res, rej); }); }).catch(function (e) { delete qvBuf[url]; throw e; });
    return qvBuf[url];
  }
  function qvStop() { (QV.srcs || []).forEach(function (s) { try { s.stop(); } catch (e) {} }); QV.srcs = []; try { qvEl.pause(); } catch (e) {} }
  function hearRecorded(q, man, deviceRead) {""")
# the quiz is opened by a tap: wake the audio context then (phones need a tap for it too)
rep("""    quizVoice();
  }""", """    var c = qvContext(); if (c && c.state === 'suspended') try { c.resume(); } catch (e) {}
    quizVoice();
  }""")
# answering or opening the scratchpad already changes playPhon.tok; stop the scheduled pieces at once too
rep("""    try { if (hasTTS) speechSynthesis.cancel(); } catch (e) {} playPhon.tok = {};
    if (COURSE !== 'py') { qBuddyMood(right ? 'cheer' : 'oops');""", """    try { if (hasTTS) speechSynthesis.cancel(); } catch (e) {} playPhon.tok = {}; qvStop();
    if (COURSE !== 'py') { qBuddyMood(right ? 'cheer' : 'oops');""")
rep("""    try { if (hasTTS) speechSynthesis.cancel(); } catch (e) {} playPhon.tok = {}; // quiet while working""",
    """    try { if (hasTTS) speechSynthesis.cancel(); } catch (e) {} playPhon.tok = {}; qvStop(); // quiet while working""")
open(P, 'w').write(h); print('read-aloud on WebAudio')
