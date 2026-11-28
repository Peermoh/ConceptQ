# Children who start Maths at their own grade (age 8: Grade 3, 9+: Grade 4) do not earn badges for the lessons
# they skipped: profile.start remembers where each course began, and lesson counts and street badges leave it out.
import os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'prototype', 'index.html'); h = open(P).read()
def rep(a, b):
    global h
    if b in h: return
    assert h.count(a) == 1, a[:80]; h = h.replace(a, b)
rep("""      if (pf.toured === true) profile.toured = true;""",
    """      if (pf.toured === true) profile.toured = true;
      if (pf.start && typeof pf.start === 'object') { profile.start = {}; ['maths'].forEach(function (c) { if (Number.isInteger(pf.start[c]) && pf.start[c] >= 0 && pf.start[c] <= 100) profile.start[c] = pf.start[c]; }); }""")
rep("""courseDone.maths = profile.age >= 9 ? at[2] || 0 : profile.age >= 8 ? at[1] : 0; }""",
    """courseDone.maths = profile.age >= 9 ? at[2] || 0 : profile.age >= 8 ? at[1] : 0; profile.start = profile.start || {}; profile.start.maths = courseDone.maths; saveProfile(); }""")
rep("""  function totalLessons() { return ['py', 'maths', 'english'].reduce(function (t, c) { return t + Math.min(doneIn(c), courseTotal(c)); }, 0); }""",
    """  // lessons actually done: a course started part-way (at the child's grade) does not count the lessons before it
  function startOf(c) { return (profile.start && profile.start[c]) || 0; }
  function totalLessons() { return ['py', 'maths', 'english'].reduce(function (t, c) { return t + Math.max(0, Math.min(doneIn(c), courseTotal(c)) - startOf(c)); }, 0); }""")
rep("""function () { return doneIn(cc[0]) >= P.floorAt[f + 1]; }]);""",
    """function () { return doneIn(cc[0]) >= P.floorAt[f + 1] && startOf(cc[0]) < P.floorAt[f + 1]; }]);""")
rep("""function () { return ['py', 'maths', 'english'].filter(function (c) { return doneIn(c) > 0; }).length >= 2; }]""",
    """function () { return ['py', 'maths', 'english'].filter(function (c) { return doneIn(c) > startOf(c); }).length >= 2; }]""")
open(P, 'w').write(h); print('start grade: no badges for skipped lessons')
