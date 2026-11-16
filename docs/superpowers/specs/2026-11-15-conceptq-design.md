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
- **It starts as empty land.** Hello, Python sets the front door, Variables pours the foundation, Numbers raises the walls.
  Only then can you go inside.
- **Lessons earn furniture**, placed by drag or tap-to-place onto glowing spots:

  | Lesson | Item | Real-life idea it stands for |
  |---|---|---|
  | Hello, Python | Poster `>> hi` | The first thing your program says |
  | Variables | Desk | Labelled drawers: a name holding a value |
  | Numbers | Sofa | Seats: counting and adding (`seats = 2 + 1`) |
  | Strings | Bookshelf (+ plant bonus for finishing it) | Books are text; a row of letters |
  | Input | Mailbox (outside) | Messages arriving from outside |
  | True / False | 2 lamps | On or off |
  | Decisions | Inside doors | A door opens only if a condition is True |
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
Input (mailbox) · True / False (2 lamps).
Each lesson is data: board lines with spoken cues and recorded timings, narration (ElevenLabs, voice Will,
recorded with word timestamps), a Read-it pane, 3 questions with a reason for every option, and done-screen text.

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
