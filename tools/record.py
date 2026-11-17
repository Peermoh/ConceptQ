import asyncio, os, re, json, sys, certifi
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'   # this environment's proxy CA
import edge_tts
sys.path.insert(0, '.')
from content_g2 import L
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
VOICES = {'ryan': 'en-GB-RyanNeural', 'prabhat': 'en-IN-PrabhatNeural'}
OUT = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/audio_steps'  # per-step clips; deep/combine.py joins them into lantern/audio/<voice>/<key>.mp3
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def align(text, bounds):
    toks = [(m.start(), m.group()) for m in re.finditer(r'\S+', text)]
    times, j = [], 0
    for pos, tok in toks:
        key = norm(tok)
        if not key: times.append(times[-1] if times else 0.0); continue
        k = j
        while k < len(bounds) and k < j + 4 and norm(bounds[k][1]) != key and not (len(key) >= 3 and norm(bounds[k][1]).startswith(key[:3])): k += 1
        if k >= j + 4: k = len(bounds)  # not found nearby: keep the previous time, do not jump ahead
        if k < len(bounds): times.append(round(bounds[k][0], 2)); j = k + 1
        else: times.append(times[-1] if times else 0.0)
    return toks, times
def rate_for(key): return '-22%' if key.startswith(('m2_', 'e2_')) else '-5%'   # Grade 2 is read more slowly
async def rec(voice, text, path, rate='-5%'):
    for attempt in range(4):
        try:
            c = edge_tts.Communicate(text, VOICES[voice], rate=rate, boundary='WordBoundary', proxy=PROXY)
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
        b = await rec(voice, say, mp3, rate_for(key))
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
