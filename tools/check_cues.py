# Reports every step whose cue count does not match its line count, or whose cues are out of order.
import sys, re
src = open('content_f2.py').read(); keys = sys.argv[1:]
bad = []
def lesson(key, steps):
    if keys and key not in keys: return
    for i, (label, lines, say, cue) in enumerate(steps):
        pos, order = -1, True
        for c in cue:
            p = say.find(c)
            if p <= pos: order = False
            pos = max(pos, p)
        if len(lines) != len(cue) or not order: bad.append((key, i + 1, label, len(lines), len(cue), order))
body = src[src.index("lesson('lists1'"):src.rindex("if __name__ == ")]
exec(body, {'lesson': lesson})
for b in bad: print(b)
print(len(bad), 'problems')
