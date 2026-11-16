import asyncio, os, re, json, sys, certifi
# behind a TLS-intercepting proxy, point certifi at its CA bundle here
import edge_tts
sys.path.insert(0, '.')
from lesson_content import L
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
VOICES = {'ryan': 'en-GB-RyanNeural', 'prabhat': 'en-IN-PrabhatNeural'}
OUT = 'prototype/audio'
# Variables (the pilot) comes from the page itself
html = open('prototype/index.html').read()
a = html.index('  var BOARD_VARS = ['); b = html.index('\n  ];\n', a); blk = html[a:b]
vsteps = []
for m in re.finditer(r'\{ lines: (\[.*?\]\]),\s*say: ("(?:\\.|[^"\\])*"),\s*cue: (\[[^\]]*\])', blk, re.S):
    vsteps.append((json.loads(m.group(1)), json.loads(m.group(2)), json.loads(m.group(3))))
assert len(vsteps) == 6, len(vsteps)
L = dict(L); L['vars'] = dict(labels=['1. Box', '2. Change', '3. Maths', '4. Two', '5. Kinds', '6. Names'], steps=vsteps)
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def align(text, bounds):
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
async def rec(voice, text, path):
    for attempt in range(4):
        try:
            c = edge_tts.Communicate(text, VOICES[voice], rate='-5%', boundary='WordBoundary', proxy=PROXY)
            bounds = []
            with open(path, 'wb') as f:
                async for ch in c.stream():
                    if ch['type'] == 'audio': f.write(ch['data'])
                    elif ch['type'] == 'WordBoundary': bounds.append((ch['offset'] / 1e7, ch['text']))
            return bounds
        except Exception as e:
            await asyncio.sleep(2 * (attempt + 1)); last = e
    raise last
async def clip(sem, voice, key, i, say):
    # resumable: each clip keeps its word boundaries in a .json next to the .mp3
    mp3 = f'{OUT}/{voice}/{key}-{i+1}.mp3'; side = f'bounds/{voice}-{key}-{i+1}.json'
    if os.path.exists(side) and os.path.getsize(mp3) > 0: return json.load(open(side))
    async with sem:
        b = await rec(voice, say, mp3)
    json.dump(b, open(side, 'w')); return b
async def main():
    times, mism = {}, []
    os.makedirs('bounds', exist_ok=True)
    sem = asyncio.Semaphore(6)
    jobs = []
    for voice in VOICES:
        os.makedirs(f'{OUT}/{voice}', exist_ok=True)
        for key, les in L.items():
            for i, (lines, say, cues) in enumerate(les['steps']):
                jobs.append((voice, key, i, say))
    results = await asyncio.gather(*[clip(sem, *j) for j in jobs])
    got = {(v, k, i): r for (v, k, i, _), r in zip(jobs, results)}
    for voice in VOICES:
        for key, les in L.items():
            for i, (lines, say, cues) in enumerate(les['steps']):
                bounds = got[(voice, key, i)]
                toks, wt = align(say, bounds)
                if len(bounds) != len(toks): mism.append((voice, key, i + 1, len(toks), len(bounds)))
                at = [wt[max(n for n, (p, _) in enumerate(toks) if p <= say.index(c))] for c in cues]
                times.setdefault(key, {}).setdefault(voice, []).append({'at': at, 'wt': wt})
        print(voice, 'done')
    json.dump(times, open('times.json', 'w'))
    json.dump({k: v for k, v in L.items()}, open('lessons.json', 'w'), ensure_ascii=False)
    print('word-count mismatches (spoken words vs service words):', mism or 'none')
asyncio.run(main())
