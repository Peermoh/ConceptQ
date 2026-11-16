import json, re, subprocess
p='/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'; s=open(p).read()
Q_STEPS = {'hello':[0,1,4,2,3,5],'vars':[0,1,3,3,5,5,6,7],'nums':[0,2,7,3,4,5,1,6],'strings':[1,2,0,3,5,8,4,4,7,6],
 'input':[1,1,2,3,1,5],'bool':[2,1,5,2,5,4,3],'if':[0,1,2,3,4,2,5,6],'loop':[0,1,5,2,3,6,4,7,8],'boss':[0,1,2,3],
 'lists1':[1,1,2,4,3,5,6,1],'lists2':[0,2,3,5,5,6,7,3],'tuples':[1,2,4,3,5,1,6],'sets':[1,2,3,5,6,7,4],
 'dicts':[1,2,2,3,6,7,8],'strtools':[1,2,2,3,4,6,0,7],'func1':[0,0,2,3,4,1,1],'func2':[0,1,3,4,6,2,8],
 'errors':[0,0,2,2,4,1,6],'files':[3,2,1,5,6,4,7],'modules':[1,2,5,0,3,6,4],'boss2':[1,2,4,3,0]}
GEN_STEPS = {'hello':[2,3,1],'vars':[1,6,3],'nums':[3,2,5,4,1],'strings':[3,4,2,4,6],'input':[2,1],'bool':[2,4],'if':[2,1],
 'loop':[2,4,6],'lists1':[1,1,4,5,6,2],'lists2':[2,2,3,6,4,5],'tuples':[1,4,1,5],'sets':[1,5,3,4],'dicts':[1,2,3,8,6],
 'strtools':[1,2,4,6,6,7],'func1':[2,4,0,1],'func2':[0,4,6,3,8],'errors':[2,4,0],'files':[5,5,4],'modules':[1,2,3],'boss2':[1,2]}
for N,key in re.findall(r"board: BOARD_\w+, quiz: (Q_\w+), key: '(\w+)'", s):
    a=s.index('  var %s = ['%N); b=s.index('\n  ];\n',a); n=len(re.findall(r'(?m)^\s*(?:\{ )?text: ', s[a:b]))
    assert n==len(Q_STEPS[key]), (key,n,len(Q_STEPS[key]))
g0=s.index('  var GEN = {'); g1=s.index('\n  };\n  function makeQuiz',g0); gen=s[g0:g1]
for key,steps in GEN_STEPS.items():
    m=re.search(r"\n    '?%s'?: \[\n(.*?)\n    \](?=,\n|$)"%re.escape(key), gen, re.S)
    n=len(re.findall(r'^      function \(\)', m.group(1), re.M))
    assert n==len(steps), (key,n,len(steps))
def rep(o,n):
    global s
    assert s.count(o)==1,o[:70]; s=s.replace(o,n)
rep("  function makeQuiz(ld) {", "  // the lesson step each question tests (0-based): hand-written questions in order, then each generator\n  var Q_STEPS = "+json.dumps(Q_STEPS)+";\n  var GEN_STEPS = "+json.dumps(GEN_STEPS)+";\n  function makeQuiz(ld) {")
rep("        made.push(q); if (tp >= 0) taken.push(tp); break;", "        q.step = (GEN_STEPS[ld.key] || [])[GEN[ld.key].indexOf(gens[g])]; made.push(q); if (tp >= 0) taken.push(tp); break;")
rep("      return { text: q.text, code: q.code, options: order.map(function (i) { return q.options[i]; }), why: order.map(function (i) { return q.why[i]; }), answer: order.indexOf(q.answer) };",
    "      var st = typeof q.step === 'number' ? q.step : (Q_STEPS[ld.key] || [])[ld.quiz.indexOf(q)];\n      return { text: q.text, code: q.code, options: order.map(function (i) { return q.options[i]; }), why: order.map(function (i) { return q.why[i]; }), answer: order.indexOf(q.answer), step: st };")
rep("  function stepFor(q) {", "  function stepFor(q) {\n    if (typeof q.step === 'number' && q.step < BOARD.length) return q.step; // tagged by hand")
open(p,'w').write(s)
js=re.search(r'<script>(.*?)</script>', s, re.S).group(1); open('/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/iso/sc0.js','w').write(js)
r=subprocess.run(['node','--check','/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/iso/sc0.js'],capture_output=True,text=True); assert r.returncode==0, r.stderr
print('tagged; page parses')
