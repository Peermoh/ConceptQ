// Maths quizzes: questions go from easy to hard, some answers are typed on a number pad, and a 🌟 bonus challenge
// ends every quiz. A wrong bonus never stops a pass; a right one is worth 20 embers.
const { check, finish, open, onboard } = require('./lib');
(async () => {
  const { b, p, errs } = await open({ hooks: [['  function renderQ() {', `window.__Q = function () { return Q.map(function (q) { return { level: q.level, bonus: !!q.bonus, num: q.num || null, answer: q.options[q.answer], options: q.options }; }); }; window.__qi = function () { return qi; };`]] });
  await onboard(p, 'maths');
  // a few quizzes, so a typed question turns up
  let typedSeen = false, passedWithWrongBonus = false;
  for (let round = 0; round < 6 && !(typedSeen && passedWithWrongBonus); round++) {
    await p.goto(p.url()); await p.waitForTimeout(900); if (await p.$('.tour')) await p.click('.tour .tc-skip');
    await p.click('#startBtn'); await p.waitForTimeout(700); await p.click('#toQuiz', { force: true }); await p.waitForTimeout(700);
    const Q = await p.evaluate(() => window.__Q());
    if (round === 0) {
      const lv = Q.filter(q => !q.bonus).map(q => q.level == null ? 1 : q.level);
      check(lv.every((x, i) => !i || x >= lv[i - 1]), 'questions go from easy to hard: ' + lv.join(' → '));
      check(Q.length === 6 && Q[5].bonus && Q.filter(q => q.bonus).length === 1, 'the quiz ends with one bonus challenge');
    }
    for (let i = 0; i < Q.length; i++) {
      const q = Q[i];
      if (i === Q.length - 1) check((await p.textContent('#qTag')).includes('🌟 Challenge'), 'the last question is marked 🌟 Challenge (bonus)');
      if (q.num) {
        typedSeen = true;
        check(await p.isVisible('.qtype-keys') && !(await p.$('#qOptions .opt')), `typed question (${q.answer}): a number pad, no choices to guess from`);
        check(await p.isDisabled('.qkey.ok'), 'Check waits until a number is typed');
        const digits = String(q.num.n);
        if (q.bonus) { await p.click('.qkey >> text="9"'); await p.click('.qkey.ok'); } // get the bonus wrong on purpose
        else { for (const d of digits) await p.click(`.qtype-keys .qkey >> text="${d}"`); await p.click('.qkey.ok'); }
        await p.waitForTimeout(250);
        if (!q.bonus) check(await p.isVisible('.qtype-show.right') && /Yes|cracked/.test(await p.textContent('#sheetSlot')), 'typing the right number is marked right');
      } else {
        const opts = await p.$$('#qOptions .opt'); let pickIdx = q.options.indexOf(q.answer);
        if (q.bonus) pickIdx = (pickIdx + 1) % q.options.length; // wrong on purpose
        await opts[pickIdx].click(); await p.waitForTimeout(250);
      }
      if (q.bonus) check(/Good try/.test(await p.textContent('#sheetSlot')) && /bonus/.test(await p.textContent('#sheetSlot')), 'a wrong bonus says it does not stop you finishing');
      const btn = await p.$('#sheetBtn'); const label = await btn.textContent(); await btn.click(); await p.waitForTimeout(700);
      if (q.bonus) {
        const onResults = await p.isVisible('#qresult');
        check(!onResults, `every question right but the bonus: the lesson is passed (button "${label}")`);
        passedWithWrongBonus = !onResults;
        await p.waitForTimeout(1500);
      }
    }
  }
  check(typedSeen, 'typed-answer questions turn up in maths quizzes');
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
