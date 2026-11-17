# Phonics sample: pure sounds, teaching lines and picture words, in both Nibb voices.
import asyncio, os, json, certifi, edge_tts
certifi.where = lambda: '/root/.ccr/ca-bundle.crt'
PROXY = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
VOICES = {'prabhat': 'en-IN-PrabhatNeural', 'ryan': 'en-GB-RyanNeural'}
# letter: (how to say the pure sound, example word)
SOUNDS = {'s': ('sss', 'sun'), 'a': ('ah', 'ant'), 't': ('tuh', 'tap'), 'p': ('puh', 'pen'), 'i': ('ih', 'ink'),
          'n': ('nnn', 'net'), 'm': ('mmm', 'map'), 'd': ('duh', 'dog'), 'g': ('guh', 'gate'), 'o': ('aw', 'on'),
          'c': ('kuh', 'cat'), 'e': ('eh', 'egg'), 'h': ('hhh', 'hat'), 'b': ('buh', 'bat'), 'u': ('uh', 'up')}
WORDS = ['cat', 'hat', 'bat', 'map', 'pan', 'pin', 'pig', 'dog', 'sun', 'bus', 'cup', 'net', 'hen', 'pen', 'bed', 'pot', 'tap', 'hut', 'bag', 'bun']
jobs = []
for v in VOICES:
    for L, (snd, w) in SOUNDS.items():
        jobs.append((v, 'snd_' + L, snd + '.', '-25%'))
        jobs.append((v, 'say_' + L, '%s says %s, like in %s.' % (L.upper(), snd, w), '-10%'))
    for w in WORDS: jobs.append((v, 'w_' + w, w + '.', '-10%'))
    jobs += [(v, 'q_start', 'Which picture starts with this sound?', '-5%'), (v, 'q_blend', 'Blend the sounds. Which word is it?', '-5%'),
             (v, 'q_miss', 'Which sound is missing?', '-5%'), (v, 'yes', 'Yes! Well done.', '+0%'), (v, 'no', 'Not quite. Listen again.', '+0%')]
sem = asyncio.Semaphore(3)
async def one(v, name, text, rate):
    os.makedirs('audio/' + v, exist_ok=True)
    f = 'audio/%s/%s.mp3' % (v, name)
    if os.path.exists(f) and os.path.getsize(f) > 0: return
    async with sem:
        for t in range(6):
            try: await edge_tts.Communicate(text, VOICES[v], rate=rate, proxy=PROXY).save('audio/%s/%s.mp3' % (v, name)); return
            except Exception as e: last = e; await asyncio.sleep(2 + 2 * t)
        print('FAILED', name, repr(last)[:200])
async def main(): await asyncio.gather(*[one(*j) for j in jobs])
asyncio.run(main())
json.dump({'sounds': SOUNDS, 'words': WORDS}, open('data.json', 'w'))
print(len(jobs), 'clips')
