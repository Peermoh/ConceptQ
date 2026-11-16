# Adds (or replaces) one lesson in the app page: board, quiz, lesson record, flashcards, quiz generators, timings.
# Usage: python3 addlesson.py <spec module name>   (the module defines KEY, IDX, META, QUIZ, CARDS, GEN_JS)
import json, re, sys, importlib
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
spec = importlib.import_module(sys.argv[1])
s = open(SRC).read()
J = lambda x: json.dumps(x, ensure_ascii=False)
LES = json.load(open('lessons.json')); TIMES = json.load(open('times.json'))
src2 = open('patch2.py').read(); ns = {}
exec(src2[:src2.index('NEW = {')].replace("s = open(SRC).read()", "s = ''"), ns)
ns['FN'] |= {'str', 'round', 'type', 'sum', 'min', 'max', 'sorted', 'tuple', 'set', 'list', 'dict', 'open', 'def', 'return'}
ns['KW'] |= {'continue', 'del', 'def', 'return', 'try', 'except', 'with', 'as', 'import', 'from', 'None', 'global', 'pass', 'lambda', 'raise'}
hl = ns['hl']
K, N = spec.KEY, spec.KEY.upper()
def block(name, body):
    global s
    head = '  var %s = [' % name
    if head in s:
        a = s.index(head); b = s.index('\n  ];\n', a) + len('\n  ];\n'); s = s[:a] + body + s[b:]
    else:
        i = s.index('  var Q_BOSS = ['); s = s[:i] + body + s[i:]
steps = ',\n'.join('    { lines: %s,\n      say: %s,\n      cue: %s }' % (J(l), J(say), J(c)) for l, say, c in LES[K]['steps'])
block('BOARD_' + N, '  var BOARD_%s = [\n%s\n  ];\n' % (N, steps))
for t, c, o, a, w in spec.QUIZ: assert len(o) == 4 and len(w) == 4 and len(set(o)) == 4, t
qs = ',\n'.join('    { text: %s,\n      code: %s,\n      options: %s, answer: %d,\n      why: %s }' % (J(t), J(hl(c)), J(o), a, J(w)) for t, c, o, a, w in spec.QUIZ)
block('Q_' + N, '  var Q_%s = [\n%s\n  ];\n' % (N, qs))
a = s.index('  var LESSON_TIMES = '); b = s.index(';\n', a); s = s[:a] + '  var LESSON_TIMES = ' + J(TIMES) + s[b:]
M = spec.META
entry = ("    %d: { board: BOARD_%s, quiz: Q_%s, key: '%s', labels: %s,\n         tag: %s, title: %s, topic: %s,\n"
         "         lastBtn: %s, doneTitle: %s, doneCta: %s,\n         doneText: %s }") % (spec.IDX, N, N, K, J(LES[K]['labels']), J(M['tag']), J(M['title']), J(M['topic']), J(M['lastBtn']), J(M['doneTitle']), J(M.get('doneCta', 'See it built')), J(M['doneText']))
# the entry ends on its doneText line: [^\n]* keeps the match from running past it into later lessons
m = re.search(r"    %d: \{ board: BOARD_%s, (?:[^\n]*\n){1,4}?         doneText: [^\n]*\}" % (spec.IDX, N), s)
if m: s = s[:m.start()] + entry + s[m.end():]
else:
    a = s.index('  var LESSON_DATA = {'); b = s.index('\n  };\n', a); s = s[:b] + ',\n' + entry + s[b:]
# flashcards (replace this lesson's cards)
a = s.index('  var CARDS = ['); b = s.index('\n  ];\n', a)
body = s[a:b]
ids = [c[0] for c in spec.CARDS]
lines = [l for l in body.split('\n') if not any(("id: '%s'," % i) in l for i in ids)]
body = '\n'.join(lines).rstrip(',')
body += ',\n' + ',\n'.join("    { id: '%s', c: '%s', l: %d, f: %s, b: %s }" % (i, c, l, J(f), J(bk)) for i, c, l, f, bk in spec.CARDS)
s = s[:a] + body + s[b:]
# quiz generators: replace or add GEN[key]
gstart = s.index('  var GEN = {'); gend = s.index('\n  };\n', gstart)
gen = s[gstart:gend]
key_re = re.compile(r"\n    %s: \[\n.*?\n    \](?=,\n    \w+: \[|\n?$)" % re.escape(K if re.match(r'^\w+$', K) else "'%s'" % K), re.S)
new_g = '\n    %s: [\n%s\n    ]' % (K, spec.GEN_JS.strip('\n'))
if key_re.search(gen): gen = key_re.sub(lambda _: new_g, gen)
else: gen = gen.rstrip() + ',' + new_g
s = s[:gstart] + gen + s[gend:]
open(SRC, 'w').write(s)
# the page must still parse: check its script with node
import subprocess, tempfile
js = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(js)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, 'page script no longer parses:\n' + r.stderr[:600]
print('added', K, 'at', spec.IDX, '| steps', len(LES[K]['steps']), '| quiz', len(spec.QUIZ), '| cards', len(spec.CARDS))
