# Puts tools/maths_extra.js (and tools/maths_g4.js when present) into the app page, just before the end of the
# course packs. Safe to run again: it replaces what it put there last time.  Usage: python3 tools/add_maths_extra.py
import os, re, subprocess, tempfile
H = os.path.dirname(os.path.abspath(__file__)); PAGE = os.path.join(H, '..', 'prototype', 'index.html')
START, END, PACKS_END = '  // ==== MATHS EXTRA (tools/add_maths_extra.py) ====\n', '  // ==== END MATHS EXTRA ====\n', '  // ==== END COURSE PACKS ====\n'
body = ''.join(open(os.path.join(H, f)).read() for f in ['maths_g4_data.js', 'maths_g4_gens.js', 'maths_extra.js'] if os.path.exists(os.path.join(H, f)))
s = open(PAGE).read()
if START in s: s = s[:s.index(START)] + s[s.index(END) + len(END):]
s = s.replace(PACKS_END, START + body + END + PACKS_END, 1)
code = re.search(r'<script>\n\(function \(\) \{\n(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write('(function () {\n' + code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, 'page script no longer parses:\n' + r.stderr[:800]
open(PAGE, 'w').write(s); print('maths extra written,', body.count('addGen('), 'generators,', body.count('addChal('), 'challenge questions')
