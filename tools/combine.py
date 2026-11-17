# Joins each lesson's per-step clips into one file per voice, with a short silence between steps,
# and writes the step offsets the app uses to play one step at a time (AUDIO_SEG).
import json, os, subprocess, re, collections
A = 'lantern/audio_steps'; GAP = 0.6; OUT = 'lantern/audio'
def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]).strip())
seg = collections.defaultdict(dict)
# ONLY=key1,key2 rebuilds just those lessons and keeps the rest of audio_seg.json
ONLY = set(filter(None, os.environ.get('ONLY', '').split(',')))
if ONLY:
    for k, v in json.load(open('deep/audio_seg.json')).items(): seg[k] = v
for who in ('ryan', 'prabhat'):
    os.makedirs(f'{OUT}/{who}', exist_ok=True)
    keys = collections.defaultdict(list)
    for f in os.listdir(f'{A}/{who}'):
        m = re.match(r'(.+)-(\d+)\.mp3$', f); keys[m.group(1)].append(int(m.group(2)))
    for k, ns in sorted(keys.items()):
        if ONLY and k not in ONLY: continue
        ns.sort(); assert ns == list(range(1, len(ns) + 1)), (k, ns)
        files = [f'{A}/{who}/{k}-{n}.mp3' for n in ns]
        t, offs = 0.0, []
        for f in files: d = dur(f); offs.append([round(t, 3), round(t + d, 3)]); t += d + GAP
        inp = sum((['-i', f] for f in files), [])
        fc = ''.join(f'[{i}:a]apad=pad_dur={GAP}[p{i}];' for i in range(len(files))) + ''.join(f'[p{i}]' for i in range(len(files))) + f'concat=n={len(files)}:v=0:a=1[o]'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', *inp, '-filter_complex', fc, '-map', '[o]', '-ac', '1', '-ar', '24000', '-c:a', 'libmp3lame', '-b:a', '48k', f'{OUT}/{who}/{k}.mp3'], check=True)
        seg[k][who] = offs
        print(who, k, len(files), round(t, 1), round(dur(f'{OUT}/{who}/{k}.mp3'), 1))
json.dump(seg, open('deep/audio_seg.json', 'w'), separators=(',', ':'))
