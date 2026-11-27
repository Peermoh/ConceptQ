// Every lesson in every course has its recorded narration in both voices: one segment per board step, cue times
// for each step, in order and inside the step's audio, and every cue phrase is in the narration text.
// Every phonics sound the English quizzes use exists in both voices' sound sheet.
const { check, finish, open } = require('./lib');
(async () => {
  const { b, p, errs } = await open({ phone: false, hooks: [['  function makeQuiz(ld) {',
    `window.__t = function (c) { useCourse(c, true); var snd = {}; Object.keys(LESSON_DATA).forEach(function (k) { for (var n = 0; n < 60; n++) makeQuiz(LESSON_DATA[k]).forEach(function (q) { (q.snd || []).forEach(function (s) { snd[s] = 1; }); }); });
      return { LD: Object.keys(LESSON_DATA).map(function (k) { var L = LESSON_DATA[k]; return { key: L.key, board: L.board.map(function (s) { return { cue: s.cue || [], say: s.say }; }) }; }), T: LESSON_TIMES, SEG: AUDIO_SEG, PHON: PHON_SEG, snd: Object.keys(snd) }; };`]] });
  for (const c of ['py', 'maths', 'english']) {
    const d = await p.evaluate(c => window.__t(c), c), probs = [];
    for (const L of d.LD) for (const who of ['ryan', 'prabhat']) {
      const T = d.T[L.key] && d.T[L.key][who], S = d.SEG[L.key] && d.SEG[L.key][who];
      if (!S || S.length !== L.board.length) { probs.push(`${L.key}/${who}: ${S ? S.length : 0} recorded steps for ${L.board.length} board steps`); continue; }
      if (!T) { probs.push(`${L.key}/${who}: no cue times`); continue; }
      L.board.forEach((st, i) => {
        const t = T[i], len = S[i][1] - S[i][0], at = `${L.key} step ${i + 1}/${who}`;
        if (!t || !t.at) return probs.push(at + ': no cue times');
        if (st.cue.length && t.at.length !== st.cue.length) probs.push(at + `: ${st.cue.length} cues, ${t.at.length} times`);
        if (t.at.some((x, k) => k && x < t.at[k - 1])) probs.push(at + ': cue times out of order');
        if (t.at.some(x => x > len + 0.3)) probs.push(at + ': a cue comes after the audio ends');
        st.cue.filter(q => st.say.indexOf(q) < 0).forEach(q => probs.push(at + `: cue "${q}" is not in the narration`));
      });
    }
    check(!probs.length, `${c}: ${d.LD.length} lessons have narration and timings in both voices` + (probs.length ? '\n         ' + probs.slice(0, 8).join('\n         ') : ''));
    if (c === 'english') {
      const miss = d.snd.flatMap(s => ['ryan', 'prabhat'].filter(w => !(d.PHON[s] && d.PHON[s][w] && d.PHON[s][w][1] > d.PHON[s][w][0])).map(w => s + '/' + w));
      check(d.snd.length > 20 && !miss.length, `english: all ${d.snd.length} phonics sounds the quizzes use are recorded in both voices ${miss.join(' ')}`);
    }
  }
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
