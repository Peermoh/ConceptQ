# Phonics audio (English course)

Edge's free voices (Ryan, Prabhat) read short spellings like "sss", "mmm" or "puh" as letter names
("ess ess ess", "em", "pee you aitch"). So every phonics sound is **cut from a real word** that the same voice
says ("s" from "sun", "a" from "at"), and placed into the recorded lesson sentence where the sound goes.

1. `build_sounds.py`: records "Listen, sun, listen." per sound (`srcwords.json`), finds the phonemes with a
   wav2vec2 phoneme recogniser (`facebook/wav2vec2-lv-60-espeak-cv-ft`), cuts the sound, holds long sounds
   (sss, mmm) to about 0.5 s, and checks each clip inside a sentence. Output: `mk2/out/<voice>-<sound>.wav`.
2. `build_lessons.py`: records each line in `sound_lines.py` with the word "this" where a sound goes, swaps in
   the clip, and rebuilds the lesson mp3, `AUDIO_SEG` and `LESSON_TIMES` (written to `nar/result.json`).
   Needs `english.json` from `node dump_english.js` (with the prototype served on port 8765).
3. `build_sheet.py`: rebuilds `audio/phonics-<voice>.mp3` (quiz prompts, sound clips, every quiz word) and
   `PHON_SEG` (`mk2/phon_seg.json`).

Needs: `pip install edge-tts torch transformers librosa soundfile`, plus ffmpeg. Results are copied into
`prototype/index.html` and `prototype/audio/` by hand (see the patch step in the git history).
