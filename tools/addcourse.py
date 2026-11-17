# Writes the Maths and English courses into the app page, between two marker comments:
# their boards, lesson records, topics, quiz generators, question step tags and flashcards.
# Usage: python3 addcourse.py        (re-run after editing content_g2.py or spec_g2.py)
import json, re, sys, subprocess, tempfile
sys.path.insert(0, '.')
from content_g2 import L
import spec_g2 as S
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
J = lambda x: json.dumps(x, ensure_ascii=False)
START, END = '  // ==== COURSE PACKS (written by deep/addcourse.py) ====\n', '  // ==== END COURSE PACKS ====\n'

def course_js(C):
    out, data, lessons, topics, gens, qsteps, gsteps, cards = [], [], [], [], [], {}, {}, []
    n = len(C['lessons'])
    for i, les in enumerate(C['lessons']):
        k = les['key']; N = 'BOARD_' + k.upper()
        steps = L[k]['steps']
        out.append('  var %s = [\n%s\n  ];' % (N, ',\n'.join('    { lines: %s, say: %s, cue: %s }' % (J(l), J(say), J(c)) for l, say, c in steps)))
        quiz = []
        for q in les['quiz']:
            assert 2 <= len(q['opts']) <= 4 and len(set(o[0] for o in q['opts'])) == len(q['opts']), (k, q['text'])
            assert 0 <= q['step'] < len(steps), (k, q['text'], q['step'])
            e = {'text': q['text'], 'code': '', 'options': [o[0] for o in q['opts']], 'answer': 0, 'why': [o[1] for o in q['opts']]}
            if q['pic']: e['pic'] = q['pic']
            if q['snd']: e['snd'] = q['snd']
            quiz.append(e)
        qsteps[k] = [q['step'] for q in les['quiz']]
        ch = les.get('challenge')
        room = 'Challenge' if ch else 'Lesson %d of %d' % (i + 1, n - 1)
        data.append('    %d: { board: %s, quiz: %s, size: 5, fresh: 3, key: %s, labels: %s,\n         tag: %s, title: %s, topic: %s,\n         lastBtn: %s, doneTitle: %s, doneCta: %s,\n         doneText: %s }' % (
            i, N, J(quiz), J(k), J(L[k]['labels']), J(C['floors'][0][0] + ' · ' + room), J(les['title'][0].upper() + les['title'][1:]), J(les['title'].replace('the ', '', 1) if ch else les['title'].lower()),
            J('Open the ' + les['part']), J('The ' + les['part'] + (' are' if les['part'].endswith('s') else ' is') + ' ready!'), J('See it built'), J(les['done'])))
        lessons.append({'title': les['title'], 'part': les['part'], 'card': les['title'][0].upper() + les['title'][1:], 'text': les['text']})
        topics.append({'key': les['icon'], 'name': les['title'].replace('the ', '').replace(' challenge', '') if ch else les['title'], 'bg': les['bg']})
        gens.append((k, [g[0].strip() for g in les['gen']]))
        gsteps[k] = [g[1] for g in les['gen']]
        for j, (f, b) in enumerate(les['cards']):
            cards.append("    { id: '%s_%d', c: '%s', l: %d, cr: '%s', f: %s, b: %s }" % (k, j + 1, 'g2m' if C['id'] == 'maths' else 'g2e', i, C['id'], J(f), J(b)))
    at, names = [0], []
    for name, cnt in C['floors']: at.append(at[-1] + cnt); names.append(name)
    assert at[-1] == n
    pack = ('  COURSE_PACKS.%s = { name: %s, place: %s, grade: %s, icon: %s, bg: %s, floorAt: %s, floorNames: %s, levels: %s,\n    lessons: %s,\n    topics: %s,\n    data: {\n%s\n    } };'
            % (C['id'], J(C['name']), J(C['place']), J(C['grade']), J(C['icon']), J(C['bg']), J(at), J(names), J(C['levels']),
               J(lessons), J(topics), ',\n'.join(data)))
    return '\n'.join(out), pack, gens, qsteps, gsteps, cards

blocks, packs, gens, qs, gs, cards = [], [], [], {}, {}, []
for C in (S.MATHS, S.ENGLISH):
    b, p, g, q, st, c = course_js(C); blocks.append(b); packs.append(p); gens += g; qs.update(q); gs.update(st); cards += c
js = (START +
      '  // a question can show a picture (pic) and play sounds (snd: clips from the phonics sound sheet)\n'
      '  function mq(text, pic, pairs) { var q = mk(text, \'\', pairs); if (q && pic) q.pic = pic; return q; }\n'
      '  function an(w) { return (/^[aeiou]/i.test(w) ? \'an \' : \'a \') + w; }\n' +
      '  // pictures that show what the words say: groups in their basket / box / bundle, loose things in rows, coins as chips\n'
      '  function rpt(t, n) { return new Array(n + 1).join(t); }\n'
      '  function grp(n, k, item, box) { var s = \'\'; for (var i = 0; i < n; i++) s += \'<span class="qg">\' + (box ? \'<i>\' + box + \'</i>\' : \'\') + (k <= 6 ? rpt(item, k) : k <= 10 ? \'<span class="qgrid">\' + rpt(\'<span>\' + item + \'</span>\', k) + \'</span>\' : item + \'<b class="qn">×\' + k + \'</b>\') + \'</span>\'; return s; }\n'
      '  function many(n, item) { if (n > 20) return \'<span class="qg">\' + item + \'<b class="qn">×\' + n + \'</b></span>\'; var s = \'\'; for (var i = 0; i < n; i += 5) s += \'<span class="qrow">\' + rpt(item, Math.min(5, n - i)) + \'</span>\'; return s; }\n'
      '  function kids(n) { return \'<span class="qg qk">\' + rpt(\'🧒\', n) + \'</span>\'; }\n'
      '  function coins(list) { return list.map(function (v) { return \'<span class="qc\' + (v >= 20 ? \' note\' : \'\') + \'">₹\' + v + \'</span>\'; }).join(\'\'); }\n' +
      S.JS_EN % {'PIC': J(S.PIC)} + '\n' +
      '  var PHON_SEG = ' + open('phon_seg.json').read() + ';\n' +
      '\n'.join(blocks) + '\n  var COURSE_PACKS = {};\n' + '\n'.join(packs) + '\n' +
      ''.join('  GEN.%s = [\n%s\n  ];\n' % (k, ',\n'.join('    ' + x for x in srcs)) for k, srcs in gens) +
      '  Object.assign(Q_STEPS, %s);\n  Object.assign(GEN_STEPS, %s);\n' % (J(qs), J(gs)) +
      '  CARDS.push(\n' + ',\n'.join(cards) + '\n  );\n' + END)
s = open(SRC).read()
if START in s:
    a = s.index(START); b = s.index(END) + len(END); s = s[:a] + js + s[b:]
else:
    i = s.index('  function makeQuiz(ld) {'); s = s[:i] + js + s[i:]
open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, 'page script no longer parses:\n' + r.stderr[:800]
print('courses written:', ', '.join('%s %d lessons' % (C['id'], len(C['lessons'])) for C in (S.MATHS, S.ENGLISH)), '| cards', len(cards))
