# Quiz read-aloud: say Grade 4 notation properly and build big numbers from recorded parts.
#   ₹12.50 → "12 rupees 50 paise", 3/4 → "3 quarters", 15:00 → "15 hundred", 3:00 p.m. → "3 p.m.", 12 r 2 → "12 remainder 2",
#   1 h 30 min → "1 hour 30 minutes", 5 cm → "5 centimetres", 46,215 → "46" "thousand" "215", 2.5 → "2" "point" "5".
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prototype', 'index.html'); h = open(P).read()
def rep(a, b):
    global h
    if b in h: return
    assert h.count(a) == 1, a[:80]; h = h.replace(a, b)
rep("""  function quizSay(t) {
    // the robot's name is the child's own choice, so it is read as "your robot" (that is always recorded)
    var nm = String(window.CQ_TEACHER || 'Nibb').replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
    t = speakText(t)""", """  var FRAC = { 2: ['half', 'halves'], 3: ['third', 'thirds'], 4: ['quarter', 'quarters'], 5: ['fifth', 'fifths'], 6: ['sixth', 'sixths'], 7: ['seventh', 'sevenths'],
    8: ['eighth', 'eighths'], 9: ['ninth', 'ninths'], 10: ['tenth', 'tenths'], 12: ['twelfth', 'twelfths'] };
  var UNIT = { km: 'kilometres', cm: 'centimetres', mm: 'millimetres', mL: 'millilitres', kg: 'kilograms', m: 'metres', g: 'grams', L: 'litres' };
  function quizSay(t) {
    // the robot's name is the child's own choice, so it is read as "your robot" (that is always recorded)
    var nm = String(window.CQ_TEACHER || 'Nibb').replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
    t = String(t).replace(/(\\d),(?=\\d)/g, '$1') // 46,215 → 46215: big numbers are built from parts in quizPieces
      .replace(/₹\\s?(\\d+)\\.(\\d{2})\\b/g, function (m, r, p) { return '₹' + r + (+p ? ' ' + (+p) + ' paise' : ''); })
      .replace(/_+\\s*\\/\\s*(\\d+)/g, '__ over $1')
      .replace(/(\\d+)\\s*\\/\\s*(\\d+)/g, function (m, a, b) { var w = FRAC[+b]; return w ? a + ' ' + (+a === 1 ? w[0] : w[1]) : a + ' over ' + b; })
      .replace(/(\\d{1,2}):00\\s?(a\\.m\\.|p\\.m\\.)/g, '$1 $2').replace(/\\b0(\\d):/g, '$1:').replace(/(\\d{1,2}):00\\b/g, '$1 hundred')
      .replace(/(\\d) r (\\d)/g, '$1 remainder $2').replace(/\\b1 h\\b/g, '1 hour').replace(/(\\d) h\\b/g, '$1 hours').replace(/(\\d) min\\b/g, '$1 minutes')
      .replace(/square cm\\b/g, 'square centimetres')
      .replace(/how many (km|cm|mm|mL|kg|m|g|L)\\b/g, function (m, u) { return 'how many ' + UNIT[u]; }).replace(/(\\d)-hour\\b/g, '$1 hour')
      .replace(/(\\d)\\s?(km|cm|mm|mL|kg|m|g|L)\\b/g, function (m, d, u) { return d + ' ' + UNIT[u]; });
    t = speakText(t)""")
rep("""  var QNUM = /\\d{1,3}(?:,\\d{3})+|\\d+(?:\\.\\d+)?/g;
  function quizPieces(t) { // must match pieces() in tools/quizvoice/build_quiz_voice.py
    var nums = t.match(QNUM) || [], out = [];
    t.split(/\\d{1,3}(?:,\\d{3})+|\\d+(?:\\.\\d+)?/).forEach(function (p, i) {
      p = p.replace(/^[ ,;:]+|[ ,;:]+$/g, '').replace(/^\\.+/, '').trim();
      if (/[A-Za-z0-9]/.test(p)) out.push(p); if (i < nums.length) out.push(nums[i]); // a lone "?" has nothing to say
    });
    return out;
  }""", """  var QNUM = /\\d+(?:\\.\\d+)?/g;
  // a number as recorded pieces: 0 to 999 are recorded whole; bigger ones are built: 46215 → 46, thousand, 215
  function numPieces(s) {
    if (s.indexOf('.') >= 0) { var d = s.split('.'); return numPieces(d[0]).concat(['point'], d[1].split('')); }
    var n = +s, out = []; if (n < 1000) return [String(n)];
    if (n >= 100000) { out.push(String(Math.floor(n / 100000)), 'lakh'); n %= 100000; }
    if (n >= 1000) { out.push(String(Math.floor(n / 1000)), 'thousand'); n %= 1000; }
    if (n) out.push(String(n));
    return out;
  }
  function quizPieces(t) { // tools/quizvoice records exactly the pieces this makes (dump_quiz_texts.js asks the page)
    var nums = t.match(QNUM) || [], out = [];
    t.split(/\\d+(?:\\.\\d+)?/).forEach(function (p, i) {
      p = p.replace(/^[ ,;:]+|[ ,;:]+$/g, '').replace(/^\\.+/, '').trim();
      if (/[A-Za-z0-9]/.test(p)) out.push(p); if (i < nums.length) out = out.concat(numPieces(nums[i])); // a lone "?" has nothing to say
    });
    return out;
  }""")
open(P, 'w').write(h); print('quiz read-aloud: notation and big numbers')
