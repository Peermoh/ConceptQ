# ConceptQ: design

Status: agreed direction, Phase 1 (Python Beginner) in prototype
Date: 2026-11-15
Prototype: `prototype/index.html` (open in a browser; also published as a private claude.ai artifact)

## Intent

A learning app where a friendly robot teacher explains a concept, asks questions,
and explains *why* a wrong answer is wrong. Progress is shown by building a house:
each topic adds a real part of the house, and connected topics are joined by glowing
wires. It should feel like a game for a 12-year-old and still be credible for an adult.

## Goals

- Learn step by step, beginner to advanced, and remember it (flashcards with spaced repetition).
- Make mistakes feel safe: every wrong option has its own explanation.
- Make progress visible and motivating: the house grows, lights dim when reviews are skipped.
- Cover the full Python syllabus (see `docs/curriculum/python.md`), mapped to PCEP-30-03 and PCAP-31-04.

## Non-goals (for now)

- Accounts, cloud sync, social features.
- Running learners' own Python code in the browser (format leaves room for a "write code" question type later).
- Other subjects (Maths, English, Science, Data Engineering). Each will later be its own house; together they form a village.
- The "paste a prompt into your own AI" quest generator and MCP connection. These come after Python Beginner works.

## Anti-goals

- Copying another app's look or characters (no Duolingo/Pip's Quest/WALL-E look-alikes).
- Collecting personal data from children: nickname, age band and avatar only, stored on the device.
- Pressure mechanics (countdowns, anything that looks like spending money).

## Approaches considered

| Approach | Trade-off | Decision |
|---|---|---|
| Native mobile app | Best device integration, two codebases, app-store friction | Rejected for now |
| Web app usable as a home-screen app (PWA) | One codebase, instant sharing, works on phone and tablet | **Chosen** |
| Lantern path / village map for progress | Pretty but abstract | Replaced by the house |
| House built topic by topic | Concrete, ordered (foundation before roof), teaches dependencies | **Chosen** |

## Decisions made with the owner

### Look and feel
- Mascot: **Nibb**, an original floating robot head (glossy white capsule, dark visor, LED eyes).
  - Two lights orbit close together **above** his head (never across the face).
  - Lights: mint normally, **red + worried eyes + head shake** on a wrong answer, **gold + happy eyes + hop** on a right answer.
  - Tap Nibb for a random funny reaction (spin, dizzy, giggle, boing, wink, heart eyes, shy, loose lights); never the same twice in a row.
- Palette: warm (no blue-night base). UI panels are translucent so they adapt to the world.
- Dynamic scene: 4 worlds (Canyon, Spring, Snowland, Aquarium) x 5 weathers (sunny, cloudy, rainy, stormy, snowy) x time of day (morning, day, sunset, night, or match the device clock).
  - Ambient life: drifting clouds, bird flocks, hot-air balloon, butterflies, petals, fireflies, shooting stars, fish, turtle, jellyfish, rain, snow, lightning.
- Every topic has its own animated icon.
- Home page scrolls as one page; the scene is a rounded card (fixes overlap with the lesson card).

### Teaching
- Lesson screen has two tabs: **Watch Nibb teach** (chalkboard, written stroke by stroke) and **Read it** (cards).
- Narration is recorded once per board step with **ElevenLabs**, voice **Will** (male, friendly), embedded in the app. Device speech is the fallback.
  - Phones only allow audio started by a tap: use **one audio element**, unlocked on the first tap and reused for every step.
- Questions: multiple choice, one explanation per option, first-try answers earn embers.

### Progress: the house
- Ground floor = Beginner, second floor = Intermediate, roof and smart systems = Advanced, rooftop/garden = Expert.
- Each topic's part goes through: blueprint (dashed) → under construction (scaffold, sparkle) → built → lit.
- Interconnections appear as glowing wires when both ends are built, each explaining a real Python fact
  (e.g. Mailbox ↔ Bookshelf: `input()` always returns a string).
- Placement test: skipped floors appear as blueprints that can be "claimed" with a short check.
- Later courses add new floors; other subjects are separate houses (a village).

### The house screen (updated 2026-11-15)
- **Home is for status**: next lesson, ground-floor path, a My House card (stage + items waiting), the course list
  (Python live; Web pages and Maths with code marked "Soon"), cards due and streak. The house is not drawn on Home.
- **My House is its own tab**, drawn in 2.5D (isometric) with three zoom levels:
  outside (closed house in a living world) → inside (only the house, no scenery) → one room full screen.
- **It starts as empty land and builds in real building order** (revised 2026-11-16, so nothing appears before
  what holds it up):
  Hello, Python → welcome sign (`print` writes words for everyone to see) · Variables → crates of building
  supplies (`bricks = 100`: a labelled box holding a value) · Numbers → the foundation, measured `10 * 10 = 100` ·
  Strings → walls and roof (a string is a row of letters, like a wall is a row of bricks); you can now go inside ·
  Input → front door and mailbox (how things come in from outside; until then an open doorway) ·
  True / False → lamps · Decisions → garden gate · Loops → stairs · Boss → porch light.
- **Lessons earn furniture**, placed by drag or tap-to-place onto glowing spots:

  | Lesson | Item | Real-life idea it stands for |
  |---|---|---|
  | Hello, Python | Poster `>> hi` | The first thing your program says (builds: welcome sign) |
  | Variables | Desk | Labelled drawers: a name holding a value |
  | Numbers | Sofa | Seats: counting and adding (`seats = 2 + 1`) |
  | Strings | Bookshelf (+ plant bonus for finishing it) | Books are text; a row of letters |
  | Input | Mailbox (outside) | Messages arriving from outside |
  | True / False | 2 lamps | On or off |
  | Decisions | Garden gate (outside, with an `if` sign) | A gate opens only if a condition is True |
  | Loops | Stairs to floor 2 | Repeat a step until you reach the top |
  | Boss | Porch light | Uses everything on the floor |

- Rug: a welcome gift, always available once the walls are up.
- **Placement rules** (physical, never "taste"): any item can go in any room; items can't overlap; nothing covers the
  window or the door; the doorway tile stays clear; a corner bookshelf blocks the first slot of the other wall; a lamp
  can't stand in front of a picture; desk and sofa can be turned. Old saves are re-checked on load.
- Progress is shared through `cq-progress` (lessons finished) and `cq-iso` (placed items). The house page runs in its
  own frame so its styles stay separate from the app.
- Keyboard: tray items are buttons; glowing spots and placed items take focus (Enter places / opens the card).
- Saves carry a version (`v: 2`); saved furniture is re-checked on load (known ids, whole-number positions only).

### Playable lessons in the prototype (2026-11-16)
Hello, Python (door, poster) · Variables (foundation, desk) · Numbers (walls, sofa) · Strings (bookshelf) ·
Input (mailbox) · True / False (2 lamps) · Decisions (garden gate) · Loops (staircase, shown from inside) ·
Boss (porch light). After the boss, Home shows "ground floor complete"; finished lessons can be replayed from the path.
Each lesson is data: board lines with spoken cues and recorded timings, narration (ElevenLabs, voice Will,
recorded with word timestamps), a Read-it pane, 3 questions with a reason for every option, and done-screen text.

### Cards and Me tabs (2026-11-16)
- **Cards:** each finished lesson adds 3 flashcards (27 for the ground floor), grouped into 6 categories by the
  kind of thinking they practise: Talking to Python (3), Boxes & names (2), Text & numbers (5),
  Maths & comparing (6), Choices & loops (7), Bug spotting (4). Review all due cards or one category. Leitner boxes 1-5 with gaps of
  0, 1, 3, 7 and 16 days; "Got it" moves a card up a box, "Again" sends it to box 1 and back into the current
  session. Stored in `cq-cards` and re-checked on load. Home's cards tile shows the real number due.
- **Me:** name, age (5-18+, sets "for age X" and hides courses above the learner's age), avatar colour,
  lesson voice/caption defaults, Nibb's idle antics on/off, real stats, and a two-tap "Start over".
  Stored in `cq-profile`.
- **Day streak** is real: opening the app on the next day adds one; missing a day starts again at 1.

### Narration voices (2026-11-16)
- Two voices; the learner picks one in Me: **Ryan** (`en-GB-RyanNeural`, British English, default) or
  **Prabhat** (`en-IN-PrabhatNeural`, Indian English). Both are free Microsoft neural voices.
- Each step's narration reads its board lines aloud ("We write: pens equals three"), so voice and board match.
- Audio is one MP3 per step per voice in `prototype/audio/<voice>/<lesson>-<step>.mp3`, loaded when a lesson
  opens (the page itself is ~0.25 MB). Per-word timings for both voices are in `LESSON_TIMES` and drive the board
  cues and the karaoke caption. `tools/lesson_content.py` holds the lesson text; `tools/record_voices.py`
  regenerates the audio and timings (for the published app, regenerate through Azure Speech).
- A mute button beside Play/Stop turns the voice off instantly (the board carries on at reading pace); the choice
  is remembered and matches the "Nibb reads lessons out loud" setting.
- Lessons are 4-6 steps each (50 steps in total) with 4-6 quiz questions; Read it is generated from the steps.

### Data
- Progress on the device only (localStorage/IndexedDB) with export/import backup, because iOS can clear site data after ~7 days unless the app is added to the home screen.
- Lesson content in data files, not code, using one level format that AI-generated quests will reuse later. Each file carries a format version.

## Phase plan

1. **Phase 1:** Python Beginner (ground floor B1–B8 + boss) playable end to end. Prototype has the full shell and one lesson (B4 Strings).
2. Phase 1b: Python Intermediate (second floor).
3. Phase 2: placement quiz, notebook, flashcard review screen, age-adapted second tone.
4. Phase 3: Advanced and Expert, then other subjects, then the AI-paste quest generator.

## Left to the builder

- Framework choice for the production app (React + Vite proposed).
- Exact level-file schema (decide after one full floor is played, then version it).
- Accessibility pass (contrast in light worlds, reduced motion already respected).

## Production notes from the prototype review (2026-11-15)

- **Fonts:** bundle fonts with the app instead of loading Google Fonts, so no child's IP address
  or browser details go to a third party (matches "personal data stays on the device").
- **Accessibility:** real tab panels (`aria-controls`), status badges that screen readers announce,
  Nibb exposed as a button, and step buttons that keep keyboard focus when they re-render.
  The prototype's topic tiles and bottom navigation are not wired yet.
- **Audio:** recorded clip first; if the device refuses or cannot decode it, fall back to device speech.
  Turning the voice off finishes the current step immediately.
- **Saved settings:** treat anything read from storage as untrusted; accept only known values.
- **Wires:** every wire is tappable and states its Python fact (prototype: Mailbox ↔ Bookshelf,
  Switches ↔ Doors, Foundation ↔ Walls).

### Floor 2 (Intermediate) — started 2026-11-16
- Storyboard: `docs/storyboards/floor2.html`. 11 lessons + boss (Lists and Functions are split in two); the roof is lifted
  on a crane in Lists I and lowered back onto floor 2 at Sets, once the walls are up.
- **Lists I is playable** (lesson 10 of 21): 8 steps, 8 questions, 5 cards in the new Collections category.
  Build moment: the crane lifts the roof and five floor beams are laid. Its item (wardrobe) waits for the floor-2 walls.
- Home shows the floor you are building, with a switch to look at the other floor. Rooms not written yet say
  "opens in the next build". Progress saves now accept 0–21 lessons.
- Ground-floor lessons were widened to cover every beginner concept (67 steps in total, 7–9 per lesson).

### Fresh quizzes and items moving in (2026-11-16)
- **A quiz is built new every time it starts** (`makeQuiz`): about half the questions come from generators with
  new values (lists, words, numbers, ranges), the rest from the hand-written pool; question order and answer order
  are shuffled. A hand-written question is skipped when a fresh one already tests the same thing (pop, slices, %…).
  Every generator's right answer was checked against real Python (1,192 samples, 0 wrong):
  `tools/check_generators.js` + Python, and `tools/check_quizzes.js` builds 300 quizzes per lesson.
- **New furniture is carried inside** at the build moment: Nibb places it on a free spot in a room that suits it,
  it drops in, and the learner can still move it. When Strings raises the walls, everything that was waiting moves in.
- **Wardrobe** (Lists I) is a living item: its clothes are a list with positions; Try it does `pop()` then `append()`.
  It sits on the ground floor until floor 2 has walls.

### Floor 2 complete (2026-11-16)
All 12 Intermediate lessons are playable (21 lessons in total, 0–20). Each has board steps in both voices, a
quiz built fresh every time (hand-written questions + generators checked against real Python: 2,884 samples,
0 wrong), flashcards (new categories: Collections, Recipes), a build moment and a living item:

| # | Lesson | Builds | Item (what tapping it shows) |
|---|---|---|---|
| 9 | Lists I | crane lifts the roof; floor beams | Wardrobe: clothes[i], pop / append |
| 10 | Lists II | floorboards in rows | Shoe rack: rack[row][col], nested loop |
| 11 | Tuples | four corner posts | Glass cabinet: shelf[0] = … → TypeError |
| 12 | Sets | floor-2 walls; roof lowered; upstairs opens | Toy box: a repeat teddy bounces out |
| 13 | Dictionaries | name plates on upstairs doors | Key rack: keys["attic"] → KeyError, then .get() |
| 14 | String tools | wallpaper ("◆" * 8) | Notice board: .upper(), .split(), [::-1] |
| 15 | Functions I | kitchen sink + stove | Kettle: make_tea(sugar) |
| 16 | Functions II | oven | Toaster: toast(2, level=3) default |
| 17 | Errors | smoke alarm arrives | Smoke alarm: try / except ValueError |
| 18 | Files | attic window lights up | Filing cabinet: "a" adds, "w" wipes |
| 19 | Modules | toolbox arrives | Toolbox: math.sqrt, ceil, floor, randint, choice |
| 20 | Boss | balcony with party lights | — |

- Inside view has a Downstairs/Upstairs switch; upstairs rooms: bedroom, landing (top of the stairs), kitchen,
  playroom. Kitchen fixtures block their tiles and the wall above them. Room labels sit off the floor.
- New items are carried in by Nibb at the build moment (moveIn), into a room that suits them.
- Tools: `tools/addlesson.py` adds a lesson from a `spec_*.py`; `tools/check_quizzes.js` + `tools/verify_generators.py`
  check every quiz and every generator against Python.

### Review round (2026-11-16)
- **Quiz:** one answer per question; Back shows earlier answers with their explanation. A lesson finishes only when
  every answer is right; otherwise a results screen lists the steps to look at again (each question is tagged with
  the step it tests: `Q_STEPS` / `GEN_STEPS`), each with "Watch it again", plus "Try a new quiz" (fresh questions).
- **"Boss" is now the Master Builder challenge** everywhere (path label "Challenge"; narration re-recorded).
- **Desktop:** the topic row stays horizontal and scrolls with arrow buttons, the mouse wheel, or click-and-drag.
- **House:** new things are placed against a wall and away from other furniture; upstairs outer walls have windows,
  not doors; the kitchen door is off the counter wall; the balcony has a glass door; items arrive faster.

### Prize wheel and the Learn tab (2026-11-16)
- The bottom tab "Home" is now **Learn** (open-book icon), so it is not confused with **House**.
- **Prize wheel:** embers fill a prize jar (default 200 embers, about 2–3 lessons; a grown-up can pick 100/200/300/500).
  Each full jar is one spin. Prizes are real-life treats: suggested lists for kids (TV time, favourite takeaway, pick
  dinner…), teens and adults ("treat yourself": a coffee, an episode of your show…), chosen by age in Me.
  Under-18s need a grown-up check (a times-table question) to change the prizes; kids see "Show this to a grown-up to
  claim your prize". The last 30 wins are kept. Stored in `cq-rewards` (`v: 1`), re-checked on load.
- The Learn dashboard has a Prize wheel tile (jar progress, glows when a spin is ready); the done screen shows the jar.
- Floor 3 (Advanced) storyboard: `docs/storyboards/floor3.html` (loft conversion + smart home, 13 lessons + challenge).
