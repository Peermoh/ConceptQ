# Records the Grade 4 Maths narration in both voices (edge-tts, the same voices and speed as every other lesson),
# joins each lesson's steps into audio/<voice>/<key>.mp3 (0.6 s apart) and writes their AUDIO_SEG and
# LESSON_TIMES (cue and word times from the service's word boundaries) into prototype/index.html.
# Re-run after changing a lesson's narration; unchanged steps are reused.   Usage: python3 tools/record_maths_g4.py
import asyncio, json, os, re, subprocess, sys, certifi
if os.path.exists('/root/.ccr/ca-bundle.crt'): certifi.where = lambda: '/root/.ccr/ca-bundle.crt'   # a proxy's certificate, where there is one
import edge_tts, numpy as np, soundfile as sf, librosa
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from maths_g4_content import LESSONS
ROOT = os.path.join(H, '..', 'prototype'); CACHE = os.path.join(H, 'cache_g4'); SR = 24000; GAP = 0.6
V = {'ryan': 'en-GB-RyanNeural', 'prabhat': 'en-IN-PrabhatNeural'}; PX = os.environ.get('HTTPS_PROXY')

async def rec(v, text, path):
    for a in range(8):
        try:
            c = edge_tts.Communicate(text, V[v], rate='-5%', boundary='WordBoundary', proxy=PX); b = []
            with open(path + '.part', 'wb') as f:
                async for ch in c.stream():
                    if ch['type'] == 'audio': f.write(ch['data'])
                    elif ch['type'] == 'WordBoundary': b.append((ch['offset'] / 1e7, ch['duration'] / 1e7, ch['text']))
            if b and os.path.getsize(path + '.part') > 2000: os.replace(path + '.part', path); return b
        except Exception: pass
        await asyncio.sleep(2 + 2 * a)
    raise RuntimeError('no audio for ' + text[:60])

norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def align(text, bounds):  # one time per word of the narration (the same rule as tools/record_voices.py)
    toks = [(m.start(), m.group()) for m in re.finditer(r'\S+', text)]; times, j = [], 0
    for pos, tok in toks:
        key = norm(tok)
        if not key: times.append(times[-1] if times else 0.0); continue
        k = j
        while k < len(bounds) and norm(bounds[k][2]) != key and not norm(bounds[k][2]).startswith(key[:3]): k += 1
        if k < len(bounds): times.append(round(bounds[k][0], 2)); j = k + 1
        else: times.append(times[-1] if times else 0.0)
    return toks, times

async def main():
    sem = asyncio.Semaphore(6); jobs = []
    for v in V:
        os.makedirs(os.path.join(CACHE, v), exist_ok=True)
        for L in LESSONS:
            for i, (lines, say, cues) in enumerate(L['steps']): jobs.append((v, L['key'], i, say))
    async def one(v, key, i, say):
        p = os.path.join(CACHE, v, '%s-%d.mp3' % (key, i)); j = p + '.json'
        if os.path.exists(j) and json.load(open(j))['text'] == say: return json.load(open(j))['b']
        async with sem: b = await rec(v, say, p)
        json.dump({'text': say, 'b': b}, open(j, 'w')); return b
    B = dict(((x[0], x[1], x[2]), r) for x, r in zip(jobs, await asyncio.gather(*[one(*x) for x in jobs])))
    seg, times = {}, {}
    for v in V:
        for L in LESSONS:
            parts, t, sg, tt = [], 0.0, [], []
            for i, (lines, say, cues) in enumerate(L['steps']):
                y, _ = librosa.load(os.path.join(CACHE, v, '%s-%d.mp3' % (L['key'], i)), sr=SR)
                toks, wt = align(say, B[(v, L['key'], i)])
                at = [wt[max(n for n, (p, _) in enumerate(toks) if p <= say.index(c))] for c in cues]
                if parts: parts.append(np.zeros(int(GAP * SR))); t += GAP
                sg.append([round(t, 3), round(t + len(y) / SR, 3)]); tt.append({'at': at, 'wt': wt}); parts.append(y); t += len(y) / SR
            w = os.path.join(CACHE, '%s-%s.wav' % (v, L['key'])); sf.write(w, np.concatenate(parts), SR)
            os.makedirs(os.path.join(ROOT, 'audio', v), exist_ok=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', w, '-ac', '1', '-ar', '24000', '-b:a', '48k', os.path.join(ROOT, 'audio', v, L['key'] + '.mp3')], check=True); os.remove(w)
            seg.setdefault(L['key'], {})[v] = sg; times.setdefault(L['key'], {})[v] = tt
    P = os.path.join(ROOT, 'index.html'); h = open(P).read()
    for var, upd in (('AUDIO_SEG', seg), ('LESSON_TIMES', times)):
        m = re.search(r'(var ' + var + r' = )(\{.*?\});\n', h); d = json.loads(m.group(2))
        for k, val in upd.items(): d[k] = {**d.get(k, {}), **val}
        h = h[:m.start(2)] + json.dumps(d, separators=(',', ':'), ensure_ascii=False) + h[m.end(2):]
    open(P, 'w').write(h)
    print('narration recorded:', len(LESSONS), 'lessons x', len(V), 'voices')
asyncio.run(main())
