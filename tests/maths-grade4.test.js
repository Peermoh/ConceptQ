// Grade 4 Maths (Market Square): a 10-year-old starts there, its first lesson plays in the recorded voice,
// the town has its new street, a 7-year-old still starts at Grade 2, and the Grade 4 cards exist.
const { check, finish, open, onboard, BASE } = require('./lib');
(async () => {
  let { b, p, errs } = await open({ autoplay: true });
  await onboard(p, 'maths', '10');
  const title = await p.evaluate(() => { const t = document.querySelector('#home .course-now b, #home h1, #home h2'); return document.getElementById('home').innerText; });
  check(/one lakh|Numbers to one lakh/i.test(title), 'a 10-year-old starts Maths at Grade 4 (Numbers to one lakh)');
  await p.waitForTimeout(1500); check(!(await p.$('.cq-cel')), 'no badges for the Grade 2 and 3 lessons that were skipped');
  await p.click('#startBtn'); await p.waitForTimeout(900);
  check(/Numbers to one lakh/.test(await p.textContent('#learnTitle')) && /Market Square/.test(await p.textContent('#learnTag')), 'the first Grade 4 lesson opens: ' + (await p.textContent('#learnTag')));
  await p.click('#playBtn'); await p.waitForTimeout(9000);
  const prog = await p.$$eval('#learnProg span.on', s => s.length), cap = await p.textContent('#caption');
  check(prog >= 1 && /Market Square|Ten hundreds|town hall/.test(cap), `the narration plays and the caption follows (${prog} step${prog === 1 ? '' : 's'} done)`);
  check(!(await p.$('.cq-cel')) && !(await p.evaluate(() => { try { return JSON.parse(localStorage.getItem('cq-badges') || '{}').got || {}; } catch (e) { return {}; } }))['l10'], 'still no "Ten lessons" badge after the lesson starts');
  await p.click('#playBtn').catch(() => {});
  const t0 = await p.evaluate(() => [...document.querySelectorAll('#boardLines > *')].map(e => e.textContent.trim()).filter(Boolean).join(' | '));
  check(/thousand/.test(t0), 'the board shows the lesson: ' + t0.slice(0, 80));
  await b.close();

  ({ b, p, errs } = await open({ autoplay: true }));
  await onboard(p, 'maths', '7');
  check(/Counting in groups/i.test(await p.evaluate(() => document.getElementById('home').innerText)), 'a 7-year-old still starts at Grade 2 (Counting in groups)');
  await b.close();

  ({ b, p, errs } = await open({}));
  await p.goto(BASE + '/world.html?course=maths&v=36'); await p.waitForTimeout(1200);
  const w = await p.evaluate(() => ({ n: document.querySelectorAll('#street .item').length, sub: document.getElementById('sub').textContent }));
  check(w.n === 36 && /Market Square · Grade 4/.test(w.sub), `the town has 36 buildings and the new street is named (${w.n}, "${w.sub}")`);
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
