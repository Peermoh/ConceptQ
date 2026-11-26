# Records the quiz read-aloud ("Read it to me") in the lesson narrators' voices, so a question never sounds
# like a different person from the lesson. Maths questions are made fresh with random names and numbers, so
# sentences are split into word phrases and numbers (the same split as quizPieces() in index.html), each
# recorded once and joined when played.
#   node dump_quiz_texts.js 1500      (prototype served on :8765) -> qtexts.json: every text the quizzes can say
#   python3 build_quiz_voice.py       -> prototype/audio/quiz/<voice>/*.mp3 and prototype/audio/quiz/<voice>.json
import asyncio, os, re, json, subprocess, sys, hashlib, certifi, numpy as np, soundfile as sf, librosa
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'   # this environment's proxy CA
import edge_tts
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(H, '..', '..', 'prototype', 'audio', 'quiz')
CACHE = os.path.join(H, 'cache'); SR = 24000; GAP = 0.25
V = {'ryan': 'en-GB-RyanNeural', 'prabhat': 'en-IN-PrabhatNeural'}; PX = os.environ.get('HTTPS_PROXY')
NUM = re.compile(r'\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?')
def pieces(t):  # must match quizPieces() in index.html
    out, nums = [], NUM.findall(t)
    for i, part in enumerate(NUM.split(t)):
        p = part.strip(' ,;:').lstrip('.').strip()
        if re.search(r'[A-Za-z0-9]', p): out.append(p)   # a lone "?" has nothing to say
        if i < len(nums): out.append(nums[i])
    return out
texts = json.load(open(os.path.join(H, 'qtexts.json')))
words = set(f'Option {c}.' for c in 'ABCD'); nums = set(str(n) for n in range(0, 1501))
for course, per in texts.items():
    for lesson, ts in per.items():
        for t in ts:
            for p in pieces(t): (nums if NUM.fullmatch(p) else words).add(p)
items = sorted(words) + sorted(nums, key=lambda x: (len(x), x))
print(len(words), 'phrases,', len(nums), 'numbers')
async def rec(v, text, path):
    # the service sometimes returns nothing for a very short text ("525"); other forms of it usually work
    for a, say in enumerate([text] * 3 + [text + '.', ', ' + text + ',', text + '!'] * 2):
        try:
            await edge_tts.Communicate(say, V[v], rate='-5%', proxy=PX).save(path + '.part')
            if os.path.getsize(path + '.part') > 1500: os.replace(path + '.part', path); return True
        except Exception: pass
        await asyncio.sleep(1 + a)
    print(f'skipped (no audio): {v} {text!r} - questions with it use the phone voice', flush=True); return False
def cpath(v, t): return os.path.join(CACHE, v, hashlib.sha1(t.encode()).hexdigest()[:16] + '.mp3')
async def record_all():
    sem = asyncio.Semaphore(8); done = [0]
    async def one(v, t):
        p = cpath(v, t)
        if os.path.exists(p): return
        async with sem: await rec(v, t, p)
        done[0] += 1
        if done[0] % 250 == 0: print('recorded', done[0], flush=True)
    for v in V: os.makedirs(os.path.join(CACHE, v), exist_ok=True)
    await asyncio.gather(*[one(v, t) for v in V for t in items])
asyncio.run(record_all())
# Pack the pieces so a question downloads little: each lesson's own phrases together, phrases many lessons share
# in "common", numbers in groups of 50 by value. Every file is cached for the rest of the quiz once fetched.
use = {}
for course, per in texts.items():
    for lesson in sorted(per):
        for t in per[lesson]:
            for p in pieces(t):
                if not NUM.fullmatch(p): use.setdefault(p, []).append(lesson)
groups = {}
for w in sorted(words):
    ls = sorted(set(use.get(w, [])))
    groups.setdefault('common' if not ls or len(ls) >= 3 else ls[0], []).append(w)
for n in sorted(nums, key=lambda x: float(x.replace(',', ''))):
    groups.setdefault('n%d' % (int(float(n.replace(',', ''))) // 50), []).append(n)
files = []
for g, ps in groups.items():
    k = 25 if g.startswith('n') else 10   # numbers are short; question phrases can be long sentences
    for i in range(0, len(ps), k): files.append((f'{g}-{i // k}', ps[i:i + k]))
for v in V:
    out = os.path.join(ROOT, v); os.makedirs(out, exist_ok=True)
    for f in os.listdir(out): os.remove(os.path.join(out, f))
    man = {}
    for fn, grp in files:
        parts, t = [], 0.0
        for txt in grp:
            if not os.path.exists(cpath(v, txt)): continue
            y, _ = librosa.load(cpath(v, txt), sr=SR)
            a, b = librosa.effects.trim(y, top_db=45, frame_length=512, hop_length=128)[1]
            y = y[max(0, a - int(0.05 * SR)):min(len(y), b + int(0.15 * SR))]   # keep air around each piece: a final p or t comes after a short silence
            if parts: parts.append(np.zeros(int(GAP * SR))); t += GAP
            man[txt] = [fn, round(t, 3), round(t + len(y) / SR, 3)]; parts.append(y); t += len(y) / SR
        if not parts: continue
        w = os.path.join(CACHE, f'{v}-{fn}.wav'); sf.write(w, np.concatenate(parts), SR)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', w, '-ac', '1', '-ar', str(SR), '-b:a', '32k', os.path.join(out, fn + '.mp3')], check=True); os.remove(w)
    json.dump(man, open(os.path.join(ROOT, v + '.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
    print(v, len(man), 'pieces in', len(files), 'files')
