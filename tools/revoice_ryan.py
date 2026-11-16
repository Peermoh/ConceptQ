# Re-voice every lesson with Microsoft "Ryan" (en-GB-RyanNeural), keeping word timings for the board cues and karaoke.
import asyncio, os, re, json, base64, certifi
# behind a TLS-intercepting proxy, point certifi at its CA bundle here
import edge_tts
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
VOICE, RATE = 'en-GB-RyanNeural', '-5%'
SRC = 'lesson-player.html'  # path to the prototype page whose BOARD_* / VOICE_* data should be re-voiced
LESSONS = ['HELLO', 'VARS', 'NUMS', 'STRINGS', 'INPUT', 'BOOL', 'IF', 'LOOP', 'BOSS']
s = open(SRC).read()
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())

async def speak(text, path):
    c = edge_tts.Communicate(text, VOICE, rate=RATE, boundary='WordBoundary', proxy=PROXY)
    bounds = []
    with open(path, 'wb') as f:
        async for ch in c.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
            elif ch['type'] == 'WordBoundary': bounds.append((ch['offset'] / 1e7, ch['text']))
    return bounds

def word_times(text, bounds):
    # match each spoken word of the sentence to the service's word boundaries, in order
    toks = [(m.start(), m.group()) for m in re.finditer(r'\S+', text)]
    times, j = [], 0
    for pos, tok in toks:
        key = norm(tok)
        if not key: times.append(times[-1] if times else 0.0); continue
        k = j
        while k < len(bounds) and norm(bounds[k][1]) != key and not norm(bounds[k][1]).startswith(key[:3]): k += 1
        if k < len(bounds): times.append(round(bounds[k][0], 2)); j = k + 1
        else: times.append(times[-1] if times else 0.0)
    return toks, times

async def main():
    global s
    report = {}
    for L in LESSONS:
        a = s.index('  var BOARD_%s = [' % L); b = s.index('\n  ];\n', a)
        block = s[a:b]
        steps = list(re.finditer(r"say: ('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"),\s*cue: (\[[^\]]*\]), at: \[[^\]]*\](,\s*wt: \[[^\]]*\])?", block))
        assert steps, L
        clips, newblock, last = [], '', 0
        for i, m in enumerate(steps):
            lit = m.group(1)
            text = json.loads(lit) if lit.startswith('"') else lit[1:-1].replace("\\'", "'")
            cues = json.loads(m.group(2).replace("'", '"'))
            path = f'voice-{L.lower()}{i+1}.mp3'
            bounds = await speak(text, path)
            toks, wt = word_times(text, bounds)
            at = []
            for c in cues:
                ci = text.index(c)
                wi = max(n for n, (p, _) in enumerate(toks) if p <= ci)
                at.append(wt[wi])
            clips.append(path)
            rep = "say: %s,\n      cue: %s, at: %s,\n      wt: %s" % (lit, m.group(2), json.dumps(at), json.dumps(wt))
            newblock += block[last:m.start()] + rep; last = m.end()
            report.setdefault(L, []).append((at, len(wt), len(bounds)))
        newblock += block[last:]
        s = s[:a] + newblock + s[b:]
        va = s.index('  var VOICE_%s = [' % L); vb = s.index('];\n', va) + 3
        s = s[:va] + '  var VOICE_%s = [' % L + ', '.join("'data:audio/mpeg;base64," + base64.b64encode(open(p, 'rb').read()).decode() + "'" for p in clips) + '];\n' + s[vb:]
    open(SRC, 'w').write(s)
    for L, r in report.items(): print(L, [x[0] for x in r], 'words', [x[1] for x in r], 'bounds', [x[2] for x in r])
asyncio.run(main())
