# Quiz read-aloud voice

"Read it to me" on Maths and English questions plays the lesson narrator's own recorded voice (Ryan or Prabhat),
so a question never sounds like a different person from the lesson. Phones without a matching voice used to
read questions in whatever voice they had, often a female one.

Maths questions are made fresh each time with random names and numbers, so the app splits every sentence into
recorded pieces and joins them when it plays (`quizSay`, `quizPieces`, `numPieces` and `hearRecorded` in
`prototype/index.html`):

- `quizSay` turns notation into words: ₹12.50 → "12 rupees 50 paise", 3/4 → "3 quarters", 15:00 → "15 hundred",
  12 r 2 → "12 remainder 2", 5 cm → "5 centimetres", + → "plus".
- `quizPieces` cuts the sentence at its numbers; `numPieces` builds big numbers from parts:
  46,215 → "46", "thousand", "215"; 3,40,000 → "3", "lakh", "40", "thousand"; 2.5 → "2", "point", "5".
- Numbers 0 to 999 are always recorded. A sentence with a piece that was never recorded falls back to the phone voice.

1. Serve the prototype on port 8765, then `node dump_quiz_texts.js 1500`. The app makes 1500 quizzes per lesson
   and lists every piece its read-aloud can play in `qpieces.json`.
2. `python3 build_quiz_voice.py` records the missing pieces (cached in `cache/`) and packs them into
   `prototype/audio/quiz/<voice>/*.mp3` (a lesson's own phrases together, numbers in groups of 50) plus
   `prototype/audio/quiz/<voice>.json` (piece → file, start, end).

Run both again after changing quiz questions or generators. Needs `pip install edge-tts librosa soundfile` and ffmpeg.
