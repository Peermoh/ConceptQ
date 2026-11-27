const { BASE } = require('./lib');
// Scratchpad: opens from the quiz, draws with touch, undo/clear/eraser/escape, per-question memory, layout on a phone.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({ ...devices['iPhone 13'] }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : fail++; console.log((c ? '  ok   ' : '  FAIL ') + m); };
  await p.goto(BASE + '/index.html'); await p.waitForTimeout(700);
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(300);
  await p.click('#wlNames button:has-text("Sparky")'); await p.click('#wlTeachGo'); await p.waitForTimeout(300);
  await p.click('#wlAges button:has-text("7")'); await p.waitForTimeout(1500);
  await p.click('#wlCards .cq-card[data-c="maths"]', { force: true }); await p.click('#wlGo', { force: true }); await p.waitForTimeout(1000);
  if (await p.$('.tour')) await p.click('.tour .tc-skip');
  await p.click('#startBtn'); await p.waitForTimeout(700); await p.click('#toQuiz', { force: true }); await p.waitForTimeout(800);
  ok(await p.isVisible('#qWork'), '"Work it out" button is visible on the question');
  await p.click('#qWork'); await p.waitForTimeout(400);
  ok(await p.isVisible('#scratch'), 'pad opens');
  const ink = () => p.evaluate(() => { const c = document.getElementById('scratchCv'), d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data; let n = 0; for (let i = 3; i < d.length; i += 4) if (d[i] > 0) n++; return n; });
  const box = await p.locator('#scratchCv').boundingBox();
  // a finger stroke: touch events via CDP-backed mouse with touch device (pointer events)
  const stroke = async (x1, y1, x2, y2) => { await p.mouse.move(box.x + x1, box.y + y1); await p.mouse.down(); for (let i = 1; i <= 12; i++) await p.mouse.move(box.x + x1 + (x2 - x1) * i / 12, box.y + y1 + (y2 - y1) * i / 12); await p.mouse.up(); };
  await stroke(40, 40, 220, 120); await stroke(60, 160, 260, 60);
  const inked = await ink(); ok(inked > 500, `drawing leaves chalk on the pad (${inked} px)`);
  ok(!(await p.isVisible('#scratchHint')), 'hint hides once drawing starts');
  // page must not scroll while drawing
  ok(await p.evaluate(() => getComputedStyle(document.getElementById('scratchCv')).touchAction === 'none'), 'drawing does not scroll the page (touch-action none)');
  await p.click('#scratchUndo'); await p.waitForTimeout(100); const afterUndo = await ink(); ok(afterUndo > 0 && afterUndo < inked, 'Undo removes the last stroke only');
  await p.click('.scratch .pen.rub'); await stroke(40, 40, 220, 120); const afterRub = await ink(); ok(afterRub < afterUndo, 'rubber erases chalk');
  await p.click('.scratch .pen[data-pen="#FFD866"]'); await stroke(80, 200, 200, 200);
  // question still visible above the pad
  const qt = await p.locator('#qText').boundingBox(), sh = await p.locator('.scratch-sheet').boundingBox();
  ok(qt.y + qt.height <= sh.y + 2, 'question text stays visible above the pad');
  const vw = await p.evaluate(() => innerWidth), bar = await p.evaluate(() => { const r = document.querySelector('.scratch-bar').getBoundingClientRect(); return [...document.querySelectorAll('.scratch-bar *')].every(e => { const q = e.getBoundingClientRect(); return q.right <= r.right + 1 && q.left >= r.left - 1; }); });
  ok(bar, 'pad toolbar fits the phone width');
  await p.keyboard.press('Escape'); await p.waitForTimeout(200); ok(!(await p.isVisible('#scratch')), 'Escape closes the pad');
  ok(await p.evaluate(() => document.activeElement && document.activeElement.id) === 'qWork', 'focus returns to the Work it out button');
  // answer, go to the next question: fresh pad; Back: working kept
  await p.click('#qOptions .opt >> nth=0'); await p.waitForTimeout(500);
  const next = await p.$('#sheetSlot button:visible'); if (next) await next.click(); await p.waitForTimeout(700);
  await p.click('#qWork'); await p.waitForTimeout(300); ok((await ink()) === 0, 'next question starts with a clean pad');
  await p.click('.scratch-btn.done'); await p.waitForTimeout(200);
  if (await p.isVisible('#qBack')) { await p.click('#qBack'); await p.waitForTimeout(500); await p.click('#qWork'); await p.waitForTimeout(300); ok((await ink()) > 0, 'going Back shows that question\'s working again'); await p.click('.scratch-dim', { position: { x: 20, y: 20 } }); await p.waitForTimeout(200); ok(!(await p.isVisible('#scratch')), 'tapping outside closes the pad'); }
  await p.click('#qWork'); await p.click('#scratchClear'); await p.waitForTimeout(100); ok((await ink()) === 0, 'Clear wipes the pad'); await p.keyboard.press('Escape');
  ok(!errs.length, 'no page errors ' + errs.join(' | '));
  console.log(`  ${pass} passed, ${fail} failed`); await b.close(); process.exit(fail ? 1 : 0);
})();
