# Phonics sound clips cut from real words said by the same voice, checked by a phoneme recogniser in context.
import asyncio, os, sys, json, certifi, numpy as np, soundfile as sf, librosa, torch, warnings; warnings.filterwarnings('ignore')
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
from transformers import AutoProcessor, Wav2Vec2ForCTC
D = os.path.dirname(os.path.abspath(__file__)) + '/mk2'
V = {'ryan': 'en-GB-RyanNeural', 'prabhat': 'en-IN-PrabhatNeural'}
PX = os.environ.get('HTTPS_PROXY'); SR = 24000
SRC = json.load(open(os.path.dirname(os.path.abspath(__file__)) + '/srcwords.json'))
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
async def recmany(items):
    sem = asyncio.Semaphore(6)
    async def one(v, text, p):
        if os.path.exists(p + '.json'): return json.load(open(p + '.json'))
        async with sem: b = await rec(v, text, p)
        json.dump(b, open(p + '.json', 'w')); return b
    return await asyncio.gather(*[one(*i) for i in items])
proc = AutoProcessor.from_pretrained('facebook/wav2vec2-lv-60-espeak-cv-ft'); model = Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-lv-60-espeak-cv-ft').eval()
BL = proc.tokenizer.pad_token_id
def spikes(y):
    y16 = librosa.resample(y, orig_sr=SR, target_sr=16000)
    with torch.no_grad(): lg = model(proc(y16, sampling_rate=16000, return_tensors='pt').input_values).logits[0]
    ids = lg.argmax(-1).tolist(); fs = len(y16) / 16000 / len(ids); out, prev = [], None
    for t, i in enumerate(ids):
        tok = proc.tokenizer.convert_ids_to_tokens(i)
        if i != BL and i != prev and tok.strip(): out.append((t * fs, tok))
        prev = i
    return out
def ipa(y): return ' '.join(t for _, t in spikes(y))
def fade(y, ms=8, out_ms=45):
    # quick fade in; a long, soft fade out so the clip does not end with a click that sounds like a 't'
    y = y.copy(); n = int(SR * ms / 1000); y[:n] *= np.linspace(0, 1, n)
    m = min(len(y) // 2, int(SR * out_ms / 1000)); y[-m:] *= np.cos(np.linspace(0, np.pi / 2, m)) ** 2; return y
def sil(s): return np.zeros(int(SR * s))
def word_span(y, b, word):
    off, dur, _ = [x for x in b if x[2].lower().strip('.,') == word.lower()][0]
    iv = librosa.effects.split(y, top_db=48, frame_length=256, hop_length=64)
    c = int((off + dur / 2) * SR)
    best = min(iv, key=lambda ab: 0 if ab[0] <= c <= ab[1] else min(abs(ab[0] - c), abs(ab[1] - c)))
    return best[0] / SR, best[1] / SR
def cut(y, b, word, k, kind, tail):
    ws, we = word_span(y, b, word)
    sp = [(t, p) for t, p in spikes(y) if ws - 0.03 <= t <= we + 0.03]
    if kind == 'name': return y[int(ws * SR):int(we * SR) + int(0.02 * SR)], sp
    if k == 0: st = ws
    else: st = (sp[k - 1][0] + sp[k][0]) / 2 + 0.02
    if kind == 'stop':
        en = sp[k + 1][0] + tail           # consonant + a little of the vowel: "tuh"
        seg = y[int(st * SR):int(en * SR)]; seg = seg * np.linspace(1, 0.1, len(seg)) ** 1.2
        return seg, sp
    if kind == 'vow':
        en = sp[k + 1][0] - 0.07 if k + 1 < len(sp) else we
        seg = y[int(st * SR):int(en * SR)]
        if len(seg) / SR < 0.2: seg = librosa.effects.time_stretch(seg, rate=max(0.7, len(seg) / SR / 0.22))
        return seg, sp
    en = (sp[k + 1][0] - 0.035) if k + 1 < len(sp) else we
    seg = y[int(st * SR):int(en * SR)]
    return hold(seg, 0.5), sp
def hold(seg, target):
    # lengthen a steady sound (sss, mmm) by repeating its middle, cross-fading each join (equal power)
    if len(seg) / SR >= target: return seg
    a, b = int(len(seg) * 0.25), int(len(seg) * 0.8); mid = seg[a:b]; x = int(min(0.02 * SR, len(mid) * 0.3))
    if len(mid) < 2.5 * x or x < 16: return librosa.effects.time_stretch(seg, rate=max(0.4, len(seg) / SR / target))
    out = seg[:b].copy(); fi = np.sin(np.linspace(0, np.pi / 2, x)); fo = np.cos(np.linspace(0, np.pi / 2, x))
    while len(out) + len(seg) - b < target * SR:
        out[-x:] = out[-x:] * fo + mid[:x] * fi; out = np.concatenate([out, mid[x:]])
    tail = seg[b:]; out[-x:] = out[-x:] * fo + tail[:x] * fi if len(tail) >= x else out[-x:]
    return np.concatenate([out, tail[x:]]) if len(tail) >= x else out
async def main(only=None):
    items, keys = [], []
    for v in V:
        for snd, (word, k, kind, tail) in SRC.items():
            if only and snd not in only: continue
            items.append((v, f'Listen, {word}, listen.', f'{D}/src-{v}-{word}.mp3')); keys.append((v, snd))
        items.append((v, 'Here it comes, this, is that right?', f'{D}/frame-{v}.mp3')); keys.append((v, '_frame'))
    B = dict(zip(keys, await recmany(items)))
    os.makedirs(f'{D}/out', exist_ok=True); res = {}
    for v in V:
        fy, _ = librosa.load(f'{D}/frame-{v}.mp3', sr=SR); fb = B[(v, '_frame')]
        ts, te = word_span(fy, fb, 'this')
        pre, post = fy[:int(ts * SR)], fy[int(te * SR):]
        for snd, (word, k, kind, tail) in SRC.items():
            if only and snd not in only: continue
            if v == 'prabhat' and snd == 'th': kind, tail = 'stop', 0.07   # Indian English says a dental 'th', a short sound
            y, _ = librosa.load(f'{D}/src-{v}-{word}.mp3', sr=SR)
            seg, sp = cut(y, B[(v, snd)], word, k, kind, tail)
            seg = fade(seg / (np.abs(seg).max() + 1e-9) * 0.6)
            sf.write(f'{D}/out/{v}-{snd}.wav', seg, SR)
            test = np.concatenate([pre, sil(0.06), seg, sil(0.06), post]); sf.write(f'{D}/out/test-{v}-{snd}.wav', test, SR)
            got = ipa(test); res[f'{v}-{snd}'] = got
            z = librosa.feature.zero_crossing_rate(seg, frame_length=512, hop_length=256).mean()
            print(f'{v[:2]} {snd:3} {word:6} word=[{" ".join(p for _, p in sp)}] {len(seg)/SR:.2f}s zcr={z:.2f} | {got}', flush=True)
    json.dump(res, open(f'{D}/res.json', 'w'), ensure_ascii=False)
asyncio.run(main(sys.argv[1:] or None))
