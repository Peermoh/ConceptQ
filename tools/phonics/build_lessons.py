# Re-records the English lessons that teach sounds, dropping the phonics clips into each sentence,
# then rebuilds audio/<voice>/<key>.mp3, AUDIO_SEG and LESSON_TIMES for those lessons.
import asyncio, os, re, sys, json, subprocess, numpy as np, soundfile as sf, librosa
sys.path.insert(0, '/home/user/ConceptQ/tools/phonics'); from sound_lines import LINES, SAY_FIX
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import importlib.util
spec = importlib.util.spec_from_file_location('s2', H + '/build_sounds.py'); 
SR = 24000; GAP = 0.6; PH = 'this'
src = open('/home/user/ConceptQ/prototype/index.html').read()
LES = {l['key']: l for l in json.load(open(H + '/english.json'))}
import certifi; certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
V = {'ryan': 'en-GB-RyanNeural', 'prabhat': 'en-IN-PrabhatNeural'}; PX = os.environ.get('HTTPS_PROXY')
async def rec(v, text, path):
    for a in range(6):
        try:
            c = edge_tts.Communicate(text, V[v], rate='-5%', boundary='WordBoundary', proxy=PX); b = []
            with open(path, 'wb') as f:
                async for ch in c.stream():
                    if ch['type'] == 'audio': f.write(ch['data'])
                    elif ch['type'] == 'WordBoundary': b.append((ch['offset'] / 1e7, ch['duration'] / 1e7, ch['text']))
            if b and os.path.getsize(path) > 2000: return b
        except Exception: pass
        await asyncio.sleep(2 + 2 * a)
    raise RuntimeError('no audio ' + text)
norm = lambda w: re.sub(r'[^a-z0-9]', '', w.lower())
def align(text, bounds):  # same rule as tools/record_voices.py
    toks = [(m.start(), m.group()) for m in re.finditer(r'\S+', text)]
    times, j = [], 0
    for pos, tok in toks:
        key = norm(tok)
        if not key: times.append(times[-1] if times else 0.0); continue
        k = j
        while k < len(bounds) and norm(bounds[k][2]) != key and not norm(bounds[k][2]).startswith(key[:3]): k += 1
        if k < len(bounds): times.append(bounds[k][0]); j = k + 1
        else: times.append(times[-1] if times else 0.0)
    return toks, times
def steps():
    for key, rows in LINES.items():
        for i, st in enumerate(LES[key]['board']):
            say, cues = st['say'], list(st['cue'])
            if (key, i) in SAY_FIX:
                o, n = SAY_FIX[(key, i)]; assert o in say; say = say.replace(o, n)
                cues = [c if c in say else c.replace('The sounds', 'The letters') for c in cues]
            t = rows.get(i)
            yield key, i, say, cues, t
async def main():
    sem = asyncio.Semaphore(6); jobs = []
    for v in V:
        for key, i, say, cues, t in steps():
            spoken = re.sub(r'\{(\w+)\}', PH, t) if t else say
            jobs.append((v, key, i, spoken))
    async def one(v, key, i, spoken):
        p = f'{H}/nar/{v}-{key}-{i}.mp3'
        if os.path.exists(p + '.json') and json.load(open(p + '.json'))['text'] == spoken: return json.load(open(p + '.json'))['b']
        async with sem: b = await rec(v, spoken, p)
        json.dump({'text': spoken, 'b': b}, open(p + '.json', 'w')); return b
    B = dict(((j[0], j[1], j[2]), r) for j, r in zip(jobs, await asyncio.gather(*[one(*j) for j in jobs])))
    times, seg, report = {}, {}, []
    for v in V:
        clips = {f[len(v) + 1:-4]: librosa.load(f'{H}/mk2/out/{f}', sr=SR)[0] for f in os.listdir(H + '/mk2/out') if f.startswith(v + '-')}
        per = {}
        for key, i, say, cues, t in steps():
            y, _ = librosa.load(f'{H}/nar/{v}-{key}-{i}.mp3', sr=SR); b = B[(v, key, i)]
            spoken = re.sub(r'\{(\w+)\}', PH, t) if t else say
            toks, wt = align(spoken, b)
            stoks = [(m.start(), m.group()) for m in re.finditer(r'\S+', say)]
            assert len(stoks) == len(toks), (key, i, len(stoks), len(toks))
            out, shifts = y, []
            if t:
                names = re.findall(r'\{(\w+)\}', t)
                phb = [k for k, x in enumerate(b) if norm(x[2]) == PH]
                assert len(phb) == len(names), (key, i, phb, names)
                pieces, last = [], 0.0
                for (k, nm) in zip(phb, names):
                    off, dur = b[k][0], b[k][1]
                    # end of the placeholder: the next word's start if it runs straight on, else where the sound dies away
                    nxt = b[k + 1][0] if k + 1 < len(b) else len(y) / SR
                    e = off + dur
                    rms = librosa.feature.rms(y=y[int(e * SR):int(nxt * SR)], frame_length=240, hop_length=120)[0]
                    thr = 0.08 * np.abs(y).max()
                    q = np.where(rms < thr * 0.35)[0]
                    end = e + (q[0] * 120 / SR if len(q) else (nxt - e))
                    end = min(end, nxt)
                    c = clips[nm]; pad = np.zeros(int(0.05 * SR))
                    # match the clip's loudness to this sentence (hissing sounds a little quieter, as in speech)
                    act = lambda z: np.sqrt(np.mean(np.square(z[np.abs(z) > 0.02 * np.abs(z).max()])) + 1e-12)
                    c = c * (act(y) / act(c)) * (0.6 if nm in ('s', 'f', 'th', 'sh', 'h') else 0.9)
                    pieces += [y[int(last * SR):int(off * SR)], pad, c]
                    shifts.append((off, end, 0.05 + len(c) / SR))
                    last = end
                pieces.append(y[int(last * SR):]); out = np.concatenate(pieces)
            def remap(tm):
                d = 0.0
                for s0, e0, L in shifts:
                    if tm >= e0 - 1e-6: d += L - (e0 - s0)
                    elif tm >= s0 - 1e-6: return s0 + d + 0.05
                return tm + d
            nwt = [round(remap(x), 2) for x in wt]
            at = [nwt[max(n for n, (p, _) in enumerate(stoks) if p <= say.index(c))] for c in cues]
            per.setdefault(key, []).append((out, {'at': at, 'wt': nwt}))
        for key, rows in per.items():
            parts, sg, tcur = [], [], 0.0
            for n, (a, tt) in enumerate(rows):
                if n: parts.append(np.zeros(int(GAP * SR))); tcur += GAP
                sg.append([round(tcur, 3), round(tcur + len(a) / SR, 3)]); parts.append(a); tcur += len(a) / SR
                times.setdefault(key, {})[v] = [r[1] for r in rows]
            full = np.concatenate(parts); w = f'{H}/nar/full-{v}-{key}.wav'; sf.write(w, full, SR)
            os.makedirs(f'{H}/nar/mp3/{v}', exist_ok=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', w, '-ac', '1', '-ar', '24000', '-b:a', '48k', f'{H}/nar/mp3/{v}/{key}.mp3'], check=True)
            seg.setdefault(key, {})[v] = sg
    json.dump({'times': times, 'seg': seg}, open(f'{H}/nar/result.json', 'w'))
    print('built', {k: {v: len(x) for v, x in d.items()} for k, d in seg.items()})
asyncio.run(main())
