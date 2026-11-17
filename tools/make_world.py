# Builds lantern/world.html (Number Town and the Story Library) from the template, the Grade 2 spec
# and the storyboard's pictures and everyday examples.
import json, re, subprocess, sys
sys.path.insert(0, '.'); import spec_g2 as S
SB = '../mathseng/maths-english-storyboard.html'
sb = open(SB).read()
js = ''.join(re.search(r'(var %s = \{.*?\n\};)' % n, sb, re.S).group(1) + '\n' for n in ('VIS',))
js += re.search(r'(var M = \{.*?\n\};)', sb, re.S).group(1) + '\n' + re.search(r'(var E = \{.*?\n\};)', sb, re.S).group(1) + '\n'
sbd = json.loads(subprocess.check_output(['node', '-e', js + 'console.log(JSON.stringify({VIS: VIS, M: M[2], E: E[2]}))']))
D = {}
for C, vis, rows in ((S.MATHS, sbd['VIS']['M2'], sbd['M'][2]), (S.ENGLISH, sbd['VIS']['E2'], sbd['E'][1])):
    assert len(vis) == len(C['lessons']) == len(rows), (C['id'], len(vis), len(rows))
    D[C['id']] = {'place': C['place'], 'street': C['floors'][0][0], 'grade': C['grade'],
                  'items': [{'title': L['title'], 'part': L['part'], 'vis': vis[i][0], 'example': rows[i][3].replace(' Tap a letter to hear it.', '')} for i, L in enumerate(C['lessons'])]}
t = open('../lantern/world.template.html').read()
open('../lantern/world.html', 'w').write(t.replace('/*DATA*/null', json.dumps(D, ensure_ascii=False)))
print('world.html:', {k: len(v['items']) for k, v in D.items()})
