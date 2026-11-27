// Naming the robot teacher: in the welcome, then everywhere (app, lesson, puzzle, house), then renamed in Me.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  const count = async (fr, word) => fr.evaluate(w => (document.body.innerText.match(new RegExp('\\b' + w + '\\b', 'g')) || []).length + [...document.querySelectorAll('[aria-label]')].filter(e => e.getAttribute('aria-label').indexOf(w) >= 0).length, word);
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(600);
  console.log('step 1:', await p.textContent('#wlName h1'));
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(300);
  console.log('step 2:', await p.textContent('#wlTeachH'), '| prefilled:', await p.inputValue('#wlTeachIn'), '| ideas:', (await p.textContent('#wlNames')).replace(/\s+/g, ' '));
  await p.click('#wlNames button:has-text("Sparky")'); await p.waitForTimeout(100);
  await p.screenshot({ path: 'iso/T-welcome.png' });
  await p.click('#wlTeachGo'); await p.waitForTimeout(300);
  await p.click('#wlAges button:has-text("7")'); await p.waitForTimeout(300);
  await p.click('#wlCards .cq-card[data-c="maths"]'); await p.click('#wlGo'); await p.waitForTimeout(600);
  console.log('home: Nibb', await count(p, 'Nibb'), '| Sparky', await count(p, 'Sparky'), '| lumi label:', await p.getAttribute('#homeLumi', 'aria-label'));
  await p.click('#startBtn'); await p.waitForTimeout(500);
  console.log('lesson caption:', await p.textContent('#caption'), '| mute label:', await p.getAttribute('#muteBtn', 'aria-label'));
  await p.click('#learn .qhead button').catch(() => {}); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(500);
  // town puzzle shows the name too
  await p.click('#home [data-nav="house"]'); await p.waitForTimeout(400);
  await p.evaluate(() => { localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 1, english: 0 })); document.getElementById('houseFrame').src = 'world.html?course=maths&v=1&build=0'; }); await p.waitForTimeout(1500);
  let f = p.frames().find(x => /world/.test(x.url())); await f.waitForSelector('.pz-skip');
  console.log('puzzle skip:', await f.textContent('.pz-skip'));
  await p.screenshot({ path: 'iso/T-puzzle.png' });
  await f.click('.pz-skip'); await p.waitForTimeout(800);
  // house bubble
  await p.evaluate(() => { localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 0, streak: 1, day: '' })); document.getElementById('houseFrame').src = 'house.html?v=0'; }); await p.waitForTimeout(1500);
  f = p.frames().find(x => /house\.html/.test(x.url()));
  console.log('house: Nibb', await count(f, 'Nibb'), '| Sparky', await count(f, 'Sparky'));
  // rename in Me: live everywhere
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(500);
  await p.click('#home [data-nav="me"]'); await p.waitForTimeout(300);
  console.log('me field:', await p.inputValue('#meTeacher'), '| voice label:', await p.textContent('#narrLbl'));
  await p.fill('#meTeacher', 'Bolt'); await p.press('#meTeacher', 'Tab'); await p.waitForTimeout(300);
  console.log('after rename: voice label:', await p.textContent('#narrLbl'), '| Sparky left', await count(p, 'Sparky'), '| Nibb left', await count(p, 'Nibb'));
  await p.screenshot({ path: 'iso/T-me.png' });
  await p.click('#me [data-nav="home"]'); await p.waitForTimeout(300); await p.click('#startBtn'); await p.waitForTimeout(400);
  console.log('lesson after rename:', await p.textContent('#caption'));
  console.log('saved:', await p.evaluate(() => JSON.parse(localStorage.getItem('cq-profile')).teacher));
  console.log('errors', errs); await b.close();
})();
