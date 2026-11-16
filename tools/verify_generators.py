# Runs every generated question's code in real Python and compares the output with the answer marked right.
# Usage: python3 verify.py <samples.json> [only_key ...]
import json, subprocess, re, sys
qs = json.load(open(sys.argv[1])); only = set(sys.argv[2:])
bad = checked = 0
for q in qs:
    if only and q['key'] not in only: continue
    code, text, right = q['code'], q['text'], q['right']
    if q['uniq'] != 4: print('DUPLICATE OPTIONS', q); bad += 1; continue
    stdin = ''
    m = re.match(r'You type (\S+)\.', text)
    if m: stdin = m.group(1) + '\n'
    m2 = re.match(r'What is (\w+) (now|at the end)\?', text)
    if m2: code += '\nprint(%s)' % m2.group(1)
    m3 = re.match(r'What does (\w+) hold\?', text)
    if m3: code += '\nprint(repr(%s))' % m3.group(1)
    r = subprocess.run(['python3', '-I', '-c', code], input=stdin, capture_output=True, text=True, cwd='/tmp')
    if r.returncode == 0: got = ' '.join(r.stdout.split('\n')).strip()
    else:
        err = (r.stderr.strip().split('\n') or [''])[-1].split(':')[0]   # e.g. IndexError
        got = right if right in ('An error', 'An ' + err, 'A ' + err) else 'An ' + err
    if text.startswith('What shows on the screen first'): got = r.stdout.split('\n')[0]
    checked += 1
    if got != right: bad += 1; print('MISMATCH', q['key'], q['gi'], repr(code), '| python:', got, '| marked:', right)
print('checked', checked, 'wrong', bad)
