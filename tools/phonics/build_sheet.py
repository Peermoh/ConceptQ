# Rebuilds audio/phonics-<voice>.mp3: the quiz prompts (kept), the new sound clips, and every quiz word re-recorded whole.
import asyncio, os, re, sys, json, subprocess, numpy as np, soundfile as sf, librosa
H = os.path.dirname(os.path.abspath(__file__)); sys.argv = sys.argv[:1]
import importlib.util; sp = importlib.util.spec_from_file_location('s2', H + '/build_sounds.py')
src = open(H + '/build_sounds.py').read().split("async def main(")[0]; G = {'__file__': H + '/build_sounds.py'}; exec(src, G)
SR, GAP = 24000, 0.3
html = open('/home/user/ConceptQ/prototype/index.html').read()
P = json.loads(re.search(r'var PHON_SEG = (\{.*?\});\n', html).group(1))
words = [k[2:] for k in P if k.startswith('w_')]
async def go():
    items = [(v, f'Listen, {w}, listen.', f'{H}/mk2/w-{v}-{w}.mp3') for v in G['V'] for w in words]
    return dict(((i[0], i[2]), r) for i, r in zip(items, await G['recmany'](items)))
B = asyncio.run(go())
newseg = {}; report = []
for v in G['V']:
    old, _ = librosa.load(f'/home/user/ConceptQ/prototype/audio/phonics-{v}.mp3', sr=SR)
    fy, _ = librosa.load(f'{H}/mk2/frame-{v}.mp3', sr=SR); fb = json.load(open(f'{H}/mk2/frame-{v}.mp3.json'))
    ts, te = G['word_span'](fy, fb, 'this'); pre, post = fy[:int(ts * SR)], fy[int(te * SR):]
    parts, t = [], 0.0
    for k in P:
        if k.startswith('q_'): a = old[int(P[k][v][0] * SR):int(P[k][v][1] * SR)]
        elif k.startswith('snd_'):
            n = {'c': 'k'}.get(k[4:], k[4:]); a, _ = librosa.load(f'{H}/mk2/out/{v}-{n}.wav', sr=SR)
        else:
            w = k[2:]; y, _ = librosa.load(f'{H}/mk2/w-{v}-{w}.mp3', sr=SR)
            s0, s1 = G['word_span'](y, B[(v, f'{H}/mk2/w-{v}-{w}.mp3')], w)
            a = G['fade'](y[max(0, int((s0 - 0.01) * SR)):int((s1 + 0.03) * SR)], 5, 25)
            got = G['ipa'](np.concatenate([pre, G['sil'](0.06), a, G['sil'](0.06), post]))
            report.append(f'{v[:2]} {w:7} {len(a)/SR:.2f}s | ' + got.replace('h ɪ ɹ ɪ t k ʌ m z ', '').replace(' ɪ z ð æ t ɹ aɪ t', ''))
        if parts: parts.append(np.zeros(int(GAP * SR))); t += GAP
        newseg.setdefault(k, {})[v] = [round(t, 3), round(t + len(a) / SR, 3)]; parts.append(a); t += len(a) / SR
    w = f'{H}/mk2/phonics-{v}.wav'; sf.write(w, np.concatenate(parts), SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', w, '-ac', '1', '-ar', '24000', '-b:a', '48k', f'{H}/mk2/phonics-{v}.mp3'], check=True)
json.dump(newseg, open(f'{H}/mk2/phon_seg.json', 'w'))
print('\n'.join(report))
