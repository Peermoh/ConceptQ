# Quiz read-aloud voice

"Read it to me" on Maths and English questions plays the lesson narrator's own recorded voice (Ryan or Prabhat),
so a question never sounds like a different person from the lesson. Phones without a matching voice used to
read questions in whatever voice they had, often a female one.

Maths questions are made fresh each time with random names and numbers (tens of thousands of sentences), so each
sentence is split into word phrases and numbers. Each piece is recorded once, and the app joins them when it plays
(`quizSay`, `quizPieces` and `hearRecorded` in `prototype/index.html`). If a sentence has a piece that was never
recorded (a very large number, for example), that question falls back to the phone's voice.

1. Serve the prototype on port 8765, then `node dump_quiz_texts.js 1500`. This makes 1500 quizzes per lesson and
   writes every text the read-aloud can say to `qtexts.json`.
2. `python3 build_quiz_voice.py` records the missing pieces (cached in `cache/`) and packs them into
   `prototype/audio/quiz/<voice>/*.mp3` (a lesson's own phrases together, numbers in groups of 50) plus
   `prototype/audio/quiz/<voice>.json` (piece -> file, start, end).

Run both again after changing quiz questions or generators. Needs `pip install edge-tts librosa soundfile` and ffmpeg.
