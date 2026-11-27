# Tests

`node tests/run.js` starts a local server for `prototype/` and runs every `*.test.js` here in a real browser
(Chromium through Playwright). `node tests/run.js quiz` runs only the tests whose name contains "quiz".
Each test prints `ok` / `FAIL` lines; the run ends with a PASS/FAIL list and exits non-zero on any failure.

| Test | What it checks |
| --- | --- |
| `journey` | A new user's whole path on a phone and a laptop: welcome, tour, home, Me, a lesson, the full quiz, the house. No errors, failed loads, stuck buttons or sideways overflow. |
| `lesson-audio` | Every lesson in all three courses has recorded narration in both voices, one piece per board step, with cue times in order and inside the audio. Every phonics sound the English quizzes use is recorded. |
| `quizzes` | 200 quizzes per lesson in every course are well-formed. Python-course questions are run in real Python (`tools/verify_generators.py`) and must print the answer marked right. |
| `quiz-voice` | "Read it to me" uses the narrator's recorded voice in Maths and English for both voices, the robot points along, answering stops it, every piece of freshly made questions is recorded, and the phone voice takes over if recordings cannot load. |
| `english-lesson` | The first English lesson plays to the end with the board and caption following, and the quiz button is ready. |
| `backup-voice` | If a lesson recording cannot load, the phone voice reads the sound lines in words (never "ess ess ess"). |
| `voice-picker` | On iPhone, Windows, Chrome and Android voice lists, the phone voice chosen is male and matches the narrator's accent. |
| `scratchpad` | The "Work it out" pad: drawing, undo, eraser, clear, closing, and a separate pad per question. |
| `celebrations` | The cheer starts with the banner and every firework burst gets a bang at the same moment. |

Needs Node, Playwright with Chromium (`npm i -D playwright && npx playwright install chromium`), and python3.
