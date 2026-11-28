# Builds Grade 4 Maths (Number Town · Market Square) from tools/maths_g4_content.py:
#  1. checks every lesson (one cue per board line, cues in the narration and in order, 3 different choices)
#  2. writes tools/maths_g4_data.js (boards, lesson records, question steps, flashcards), which
#     tools/add_maths_extra.py puts into the page together with maths_g4_gens.js and maths_extra.js
#  3. adds the 12 buildings to prototype/world.html, the Grade 4 flashcard group, the course card's ages,
#     and the age-based starting grade
# Narration is recorded separately by tools/record_maths_g4.py.   Usage: python3 tools/build_maths_g4.py
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from maths_g4_content import LESSONS, FLOOR, WORLD, BARS
ROOT = os.path.join(H, '..', 'prototype'); J = lambda x: json.dumps(x, ensure_ascii=False)
START_AT = 24  # Grade 4 lessons come after Grade 2 (12) and Grade 3 (12)

def bars_pic(rows, per=10):  # the same picture as barsPic() in maths_g4_gens.js
    top = max(r[1] for r in rows); lines = -(-top // per); u = 16
    ax = ''.join('<b style="bottom:%dpx">%d</b>' % (k * u, k * per) for k in range(lines + 1))
    bars = ''.join('<i style="height:%dpx"></i>' % round(r[1] / per * u) for r in rows); labs = ''.join('<b>%s</b>' % r[0] for r in rows)
    return '<span class="qgraph"><span class="qplot" style="height:%dpx"><span class="qax">%s</span>%s</span><span class="qlab">%s</span></span>' % (lines * u, ax, bars, labs)

# ---- 1. checks ----
problems = []
for L in LESSONS:
    k = L['key']
    assert len(L['steps']) == len(L['labels']) == 5, k
    for i, (lines, say, cues) in enumerate(L['steps']):
        if len(cues) != len(lines): problems.append('%s step %d: %d board lines but %d cues' % (k, i + 1, len(lines), len(cues)))
        pos = [say.find(c) for c in cues]
        if -1 in pos: problems.append('%s step %d: cue not in the narration: %s' % (k, i + 1, [c for c, p in zip(cues, pos) if p < 0]))
        elif pos != sorted(pos): problems.append('%s step %d: cues out of order %s' % (k, i + 1, cues))
    for q in L['quiz']:
        if len(set(o[0] for o in q['opts'])) != len(q['opts']) or len(q['opts']) != 3: problems.append('%s: choices not 3 different: %s' % (k, q['text']))
        if not 0 <= q['step'] < 5: problems.append('%s: bad step for %s' % (k, q['text']))
if problems: sys.exit('Fix these first:\n  ' + '\n  '.join(problems))

# ---- 2. page data ----
out = ['  // ---- Grade 4 (Market Square): written by tools/build_maths_g4.py from tools/maths_g4_content.py ----']
data, lessons, topics, qsteps, cards = [], [], [], {}, []
n = len(LESSONS)
for i, L in enumerate(LESSONS):
    k, N = L['key'], 'BOARD_' + L['key'].upper()
    out.append('  var %s = [\n%s\n  ];' % (N, ',\n'.join('    { lines: %s, say: %s, cue: %s }' % (J(l), J(s), J(c)) for l, s, c in L['steps'])))
    quiz = []
    for q in L['quiz']:
        e = {'text': q['text'], 'code': '', 'options': [o[0] for o in q['opts']], 'answer': 0, 'why': [o[1] for o in q['opts']]}
        if q['pic']: e['pic'] = bars_pic(BARS) if q['pic'] == 'BARS' else q['pic']
        quiz.append(e)
    qsteps[k] = [q['step'] for q in L['quiz']]
    ch = L.get('challenge')
    room = 'Challenge' if ch else 'Lesson %d of %d' % (i + 1, n - 1)
    title = L['title'][0].upper() + L['title'][1:]
    data.append('    P.data[%d] = { board: %s, quiz: %s, size: 5, fresh: 3, key: %s, labels: %s,\n      tag: %s, title: %s, topic: %s,\n      lastBtn: %s, doneTitle: %s, doneCta: "See it built",\n      doneText: %s };' % (
        START_AT + i, N, J(quiz), J(k), J(L['labels']), J(FLOOR[0] + ' · ' + room), J(title),
        J(L['title'].replace('the ', '', 1) if ch else L['title'].lower()), J('Open the ' + L['part']),
        J('The ' + L['part'] + (' are' if L['part'].endswith('s') else ' is') + ' ready!'), J(L['done'])))
    lessons.append({'title': L['title'], 'part': L['part'], 'card': title, 'text': L['text']})
    topics.append({'key': L['icon'], 'name': L['title'].replace('the ', '').replace(' challenge', '') if ch else L['title'], 'bg': L['bg']})
    for j, (f, b) in enumerate(L['cards']):
        cards.append("    { id: '%s_%d', c: 'g4m', l: %d, cr: 'maths', f: %s, b: %s }" % (k, j + 1, START_AT + i, J(f), J(b)))
out.append('''  (function () { // add Market Square to the Maths course (once)
    var P = COURSE_PACKS.maths; if (P.floorAt.length > 3) return;
    P.floorAt.push(%d); P.floorNames.push(%s); P.grade = "Grades 2–4"; P.levels.push(%s);
    %s.forEach(function (l) { P.lessons.push(l); });
    %s.forEach(function (t) { P.topics.push(t); });
%s
  })();
  Object.assign(Q_STEPS, %s);
  CARDS.push(
%s
  );''' % (START_AT + n, J(FLOOR[0]), J(list(FLOOR[1:]) if False else [FLOOR[1], FLOOR[0], FLOOR[2]]), J(lessons), J(topics), '\n'.join(data), J(qsteps), ',\n'.join(cards)))
open(os.path.join(H, 'maths_g4_data.js'), 'w').write('\n'.join(out) + '\n')

# add_maths_extra.py puts these files into the page, in this order
s = open(os.path.join(H, 'add_maths_extra.py')).read()
s = s.replace("for f in ['maths_g4.js', 'maths_extra.js']", "for f in ['maths_g4_data.js', 'maths_g4_gens.js', 'maths_extra.js']")
open(os.path.join(H, 'add_maths_extra.py'), 'w').write(s)
subprocess.run([sys.executable, os.path.join(H, 'add_maths_extra.py')], check=True)

# ---- 3. the rest of the page ----
P = os.path.join(ROOT, 'index.html'); h = open(P).read()
def rep(a, b, once=True):
    global h
    if b in h: return  # already done
    assert h.count(a) == 1, 'anchor not found once: ' + a[:90]
    h = h.replace(a, b)
rep("""    { id: 'g3m',   name: 'Maths 3',           note: 'Grade 3: Garden Lane',              bg: '#B8F27C', ic: '<path d="M6 6l12 12M18 6L6 18"/>' },""",
    """    { id: 'g3m',   name: 'Maths 3',           note: 'Grade 3: Garden Lane',              bg: '#B8F27C', ic: '<path d="M6 6l12 12M18 6L6 18"/>' },
    { id: 'g4m',   name: 'Maths 4',           note: 'Grade 4: Market Square',            bg: '#FFC861', ic: '<path d="M4 12h16M12 4v16M6 6l12 12"/>' },""")
m = re.search(r"    maths:   \{ emoji: '🏙️', name: 'Maths', world: 'Grow Number Town', tag: '[^']*',(.*?)minAge: 6, maxAge: 10, extra: 'Grades 2–3' \},", h)
if m:
    h = h.replace(m.group(0), "    maths:   { emoji: '🏙️', name: 'Maths', world: 'Grow Number Town', tag: 'Market Street, Garden Lane, then Market Square (Grades 2–4)'," + m.group(1) + "minAge: 6, maxAge: 11, extra: 'Grades 2–4' },")
rep("""  function joinCourse(cid) {
    if (!profile.courses) profile.courses = [];
    if (profile.courses.indexOf(cid) < 0) profile.courses.push(cid);""", """  function joinCourse(cid) {
    if (!profile.courses) profile.courses = [];
    var isNew = profile.courses.indexOf(cid) < 0;
    if (isNew) profile.courses.push(cid);
    // Maths starts at the child's own grade: age 8 at Grade 3, age 9 and up at Grade 4 (the earlier streets stay open to visit)
    if (isNew && cid === 'maths' && COURSE !== 'maths' && !courseDone.maths) { var at = COURSE_PACKS.maths.floorAt; courseDone.maths = profile.age >= 9 ? at[2] || 0 : profile.age >= 8 ? at[1] : 0; }""")
rep("""#qProgress span.bonus {""", """.qgraph { display: inline-flex; flex-direction: column; gap: 4px; padding: 8px 10px 0 38px; position: relative; }
.qplot { position: relative; display: flex; align-items: flex-end; gap: 14px; padding: 0 10px; border-left: 2px solid currentColor; border-bottom: 2px solid currentColor;
  background: repeating-linear-gradient(to top, rgba(255,241,226,.22) 0 1px, transparent 1px 16px); }
.qplot i { display: block; width: 30px; background: #FFB547; border-radius: 4px 4px 0 0; }
.qax { position: absolute; left: -36px; top: 0; bottom: 0; width: 30px; } .qax b { position: absolute; right: 0; font-size: 11px; font-weight: 700; transform: translateY(50%); }
.qlab { display: flex; gap: 14px; padding: 0 12px; } .qlab b { width: 30px; text-align: center; font-size: 12px; font-weight: 700; }
#qProgress span.bonus {""")
open(P, 'w').write(h)

# ---- 4. the town ----
W = os.path.join(ROOT, 'world.html'); w = open(W).read()
m = re.search(r'  var DATA = (\{.*?\});\n', w); D = json.loads(m.group(1)); M = D['maths']
M['items'] = [it for it in M['items'] if it.get('street') != FLOOR[0]]
for L in LESSONS:
    v, ex = WORLD[L['key']]
    M['items'].append({'title': L['title'][0].upper() + L['title'][1:], 'part': L['part'], 'vis': v, 'example': ex, 'street': FLOOR[0]})
M['grade'] = 'Grades 2–4'
w = w.replace(m.group(1), json.dumps(D, ensure_ascii=False), 1)
old_sub = "(C.items[Math.max(0, v - 1)] && /Garden/.test(C.items[Math.max(0, v - 1)].street) ? 'Grade 3' : C.grade.replace('Grades 2–3', 'Grade 2'))"
if old_sub in w:
    w = w.replace(old_sub, "(({ 'Garden Lane': 'Grade 3', 'Market Square': 'Grade 4', 'Market Street': 'Grade 2' })[(C.items[Math.max(0, v - 1)] || {}).street] || C.grade.replace(/Grades 2–\\d/, 'Grade 2'))")
draw = open(os.path.join(H, 'maths_g4_world.js')).read()
if '// ---- Market Square (Grade 4) ----' not in w:
    a = "\n    ],\n    english: ["
    assert w.count(a) == 1
    i = w.index(a); w = w[:i] + ',\n' + draw.rstrip('\n') + w[i:]
open(W, 'w').write(w)
print('Grade 4 built: %d lessons, %d flashcards; town has %d buildings' % (n, len(cards), len(M['items'])))
