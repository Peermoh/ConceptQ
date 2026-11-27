// Congratulations after a lesson, a bigger one after the last lesson of a street, and after a solved puzzle.
const { chromium, devices } = require('playwright');
async function passQuiz(p) {
  await p.click('#startBtn'); await p.waitForTimeout(400); await p.click('#toQuiz'); await p.waitForTimeout(300);
  const nq = +((await p.textContent('#qTag')).match(/of (\d+)/)[1]);
  for (let q = 0; q < nq; q++) {
    for (let k = 0; k < 4; k++) { if (!(await p.$('#opt-' + q + '-' + k))) break; await p.click('#opt-' + q + '-' + k); await p.waitForTimeout(60); if (await p.$('.sheet.is-right')) break; await p.evaluate(qq => window.__undo(qq), q); }
    await p.click('#sheetBtn'); await p.waitForTimeout(120);
  }
}
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const [lesson, tag] of [[2, 'lesson'], [11, 'street']]) {
    const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
    await ctx.addInitScript(n => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: n, english: 0 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 8, toured: true, courses: ['maths'], antics: false })); } }, lesson);
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(600);
    await passQuiz(p); await p.waitForTimeout(900);
    console.log(tag, '| banner:', (await p.textContent('.cq-cel .ban').catch(() => 'NONE')).replace(/\s+/g, ' '), '| big:', await p.$eval('.cq-cel', e => e.classList.contains('big')).catch(() => '-'));
    await p.screenshot({ path: 'iso/CEL-' + tag + '.png' });
    await p.waitForTimeout(3500); console.log('   cleaned up:', !(await p.$('.cq-cel')), '| done screen:', await p.textContent('#doneTitle'));
    if (tag === 'lesson') { // then the puzzle in Number Town
      await p.click('#doneHouse'); await p.waitForTimeout(1500);
      const f = p.frames().find(x => /world/.test(x.url())); await f.waitForSelector('.pz');
      const n = await f.$$eval('.pz-piece', e => e.length);
      for (let i = 0; i < n; i++) { const pc = (await f.$$('.pz-piece'))[0], k = await pc.getAttribute('data-k'); await pc.click(); await f.click('.pz-slot[data-k="' + k + '"]'); await p.waitForTimeout(60); }
      await p.waitForTimeout(700);
      console.log('puzzle | banner:', (await f.textContent('.cq-cel .ban').catch(() => 'NONE')).replace(/\s+/g, ' '));
      await p.screenshot({ path: 'iso/CEL-puzzle.png' });
      await p.waitForTimeout(3200); console.log('   puzzle closed:', !(await f.$('.pz')), '| toast:', await f.textContent('#toast'));
    }
    await ctx.close();
  }
  console.log('errors', errs); await b.close();
})();
