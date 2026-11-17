// First visit: name → age → pick a course → Home shows only that course; then My courses adds a second one,
// the Home switch appears, and the Courses screen shows the picture cards. Also: an existing learner skips the welcome.
const { chromium, devices } = require('playwright');
const desk = process.argv[2] === 'desktop';
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext(desk ? { viewport: { width: 1366, height: 800 }, deviceScaleFactor: 1 } : { ...devices['iPhone 13'], deviceScaleFactor: 1 });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const tag = desk ? 'desk' : 'phone';
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(700);
  console.log('welcome visible:', await p.isVisible('#welcome'), '| home visible:', await p.isVisible('#home'));
  await p.screenshot({ path: 'iso/W1-' + tag + '.png' });
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(300);
  console.log('age title:', await p.textContent('#wlAgeH'), '| age buttons', await p.$$eval('#wlAges button', e => e.length));
  await p.screenshot({ path: 'iso/W2-' + tag + '.png' });
  await p.click('#wlAges button:has-text("7")'); await p.waitForTimeout(400);
  console.log('cards:', (await p.$$eval('#wlCards .cq-card', e => e.map(x => x.dataset.c + (x.querySelector('.ribbon') ? '★' : '') + (x.classList.contains('dim') ? '(dim)' : '')))).join(' '), '| go disabled:', await p.isDisabled('#wlGo'));
  await p.screenshot({ path: 'iso/W3-' + tag + '.png', fullPage: true });
  await p.click('#wlCards .cq-card[data-c="maths"]'); await p.waitForTimeout(200);
  console.log('go:', await p.textContent('#wlGo'));
  await p.click('#wlGo'); await p.waitForTimeout(600);
  console.log('home:', await p.isVisible('#home'), '| greet:', await p.textContent('#topName'), '| course:', (await p.textContent('#courseTabs')).replace(/\s+/g, ' '), '| switch shown:', !!(await p.$('#courseTabs .cn-sw')), '| card:', await p.textContent('#cardTitle'));
  await p.screenshot({ path: 'iso/W4-' + tag + '.png' });
  // Me → My courses → add English
  await p.click('#home [data-nav="me"]'); await p.waitForTimeout(400);
  console.log('my courses:', (await p.$$eval('#myCourses .mc', e => e.map(x => x.innerText.replace(/\s+/g, ' ')))).join(' || '));
  await p.screenshot({ path: 'iso/W5-' + tag + '.png', fullPage: true });
  await p.click('#myCourses .mc:has-text("English") button'); await p.waitForTimeout(500);
  console.log('after add:', (await p.textContent('#courseTabs')).replace(/\s+/g, ' '), '| switch shown:', !!(await p.$('#courseTabs .cn-sw')));
  await p.click('#courseTabs .cn-sw'); await p.waitForTimeout(200);
  console.log('menu:', (await p.textContent('#courseTabs .cn-menu')).replace(/\s+/g, ' '));
  await p.screenshot({ path: 'iso/W6-' + tag + '.png' });
  await p.click('#courseTabs .cn-menu button:has-text("Maths")'); await p.waitForTimeout(400);
  console.log('switched to:', (await p.textContent('#courseTabs .cn-t')).replace(/\s+/g, ' '));
  // Courses screen
  await p.click('#coursesTile'); await p.waitForTimeout(400);
  console.log('courses screen cards:', await p.$$eval('#coursesBody .cq-card', e => e.length));
  await p.screenshot({ path: 'iso/W7-' + tag + '.png', fullPage: true });
  await p.reload(); await p.waitForTimeout(700);
  console.log('after reload → welcome:', await p.isVisible('#welcome'), '| home:', await p.isVisible('#home'), '|', (await p.textContent('#courseTabs .cn-t')).replace(/\s+/g, ' '));
  console.log('profile:', await p.evaluate(() => localStorage.getItem('cq-profile')));
  // an existing Python learner (no profile yet) skips the welcome and keeps Python
  const c2 = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await c2.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 12, embers: 0, streak: 1, day: '' })); } });
  const p2 = await c2.newPage(); p2.on('pageerror', e => errs.push(e.message));
  await p2.goto('http://localhost:8765/index.html'); await p2.waitForTimeout(700);
  console.log('existing learner → welcome:', await p2.isVisible('#welcome'), '|', (await p2.textContent('#courseTabs .cn-t')).replace(/\s+/g, ' '), '| card:', await p2.textContent('#cardTitle'));
  console.log('errors', errs); await b.close();
})();
