# Grade 2 phonics clips (pure sounds, picture words, question prompts) in both Nibb voices,
# trimmed and joined into one sound sheet per voice: lantern/audio/phonics-<voice>.mp3 + deep/phon_seg.json
import asyncio, os, sys, json, shutil, subprocess, certifi
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
import edge_tts
sys.path.insert(0, '../deep'); import spec_g2 as S
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
VOICES = {'prabhat': 'en-IN-PrabhatNeural', 'ryan': 'en-GB-RyanNeural'}
jobs = []
for v in VOICES:
    for L, (snd, w) in S.SOUNDS.items(): jobs.append((v, 'snd_' + L, snd + '.', '-25%'))
    for w in S.PIC: jobs.append((v, 'w_' + w, w + '.', '-10%'))
    jobs += [(v, 'q_start', 'Which picture starts with this sound?', '-5%'), (v, 'q_blend', 'Blend the sounds. Which word is it?', '-5%'), (v, 'q_miss', 'Which sound is missing?', '-5%')]
sem = asyncio.Semaphore(3)
async def one(v, name, text, rate):
    os.makedirs('clips/' + v, exist_ok=True)
    f = 'clips/%s/%s.mp3' % (v, name)
    if os.path.exists(f) and os.path.getsize(f) > 0: return
    old = 'audio/%s/%s.mp3' % (v, name)
    if os.path.exists(old) and name not in ('snd_k',): shutil.copy(old, f); return   # reuse the sample's clip
    async with sem:
        for t in range(6):
            try: await edge_tts.Communicate(text, VOICES[v], rate=rate, proxy=PROXY).save(f); return
            except Exception as e: last = e; await asyncio.sleep(2 + 2 * t)
        print('FAILED', name, repr(last)[:200])
async def main(): await asyncio.gather(*[one(*j) for j in jobs])
asyncio.run(main())
# trim silence at both ends, then join with a short gap, recording where each clip sits
def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).strip())
OUT = '../lantern/audio'; seg = {}; GAP = 0.3
for v in VOICES:
    names = sorted(set(j[1] for j in jobs if j[0] == v)); os.makedirs('trim/' + v, exist_ok=True)
    t, files = 0.0, []
    for n in names:
        src, dst = 'clips/%s/%s.mp3' % (v, n), 'trim/%s/%s.wav' % (v, n)
        if not os.path.exists(dst):
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,apad=pad_dur=%s' % GAP, '-ac', '1', '-ar', '24000', dst], check=True)
        d = dur(dst); seg.setdefault(n, {})[v] = [round(t, 3), round(t + d - GAP, 3)]; t += d; files.append(dst)
    lst = 'trim/%s.txt' % v; open(lst, 'w').write(''.join("file '%s'\n" % os.path.abspath(f) for f in files))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c:a', 'libmp3lame', '-b:a', '48k', '%s/phonics-%s.mp3' % (OUT, v)], check=True)
    print(v, len(files), 'clips,', round(t, 1), 's, sheet', round(dur('%s/phonics-%s.mp3' % (OUT, v)), 1), 's')
json.dump(seg, open('../deep/phon_seg.json', 'w'), separators=(',', ':'))
