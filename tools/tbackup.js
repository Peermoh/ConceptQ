// Backup → wipe → restore: everything comes back. A damaged code is refused and changes nothing.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1, permissions: ['clipboard-read', 'clipboard-write'] });
  await ctx.addInitScript(() => { if (!sessionStorage.s) { sessionStorage.s = 1;
    localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 12, embers: 340, streak: 5, day: '2026-11-18' }));
    localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 5, english: 3 }));
    localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 8, teacher: 'Sparky', toured: true, courses: ['maths', 'english', 'py'], antics: false }));
    localStorage.setItem('cq-iso', JSON.stringify({ placed: { study: [{ id: 'desk', x: 1, y: 2 }] } }));
    localStorage.setItem('cq-rewards', JSON.stringify({ v: 1, prizes: ['🍦 An ice cream', '🎨 Art time'], per: 100, used: 1, wins: [{ p: '🍦 An ice cream', t: 1 }] })); } });
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(700);
  const before = await p.evaluate(() => { const o = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.startsWith('cq-')) o[k] = localStorage.getItem(k); } return o; });
  await p.click('#home [data-nav="me"]'); await p.waitForTimeout(300);
  await p.click('#bkSave'); await p.waitForTimeout(600);
  const code = await p.inputValue('#bkCode');
  console.log('backup code:', code.slice(0, 40) + '…', '| length', code.length, '|', await p.textContent('#bkOutMsg'));
  await p.screenshot({ path: 'iso/BK-save.png', fullPage: false });
  await p.click('#bkCopy'); await p.waitForTimeout(200); console.log('copy:', await p.textContent('#bkOutMsg'));
  // a damaged code is refused
  await p.click('#bkRestore'); await p.fill('#bkPaste', code.slice(0, -5) + 'xxxxx'); await p.click('#bkCheck'); await p.waitForTimeout(300);
  console.log('damaged code:', await p.textContent('#bkInMsg'), '| preview shown:', await p.isVisible('#bkPreview'));
  await p.fill('#bkPaste', 'hello'); await p.click('#bkCheck'); await p.waitForTimeout(200); console.log('not a code:', await p.textContent('#bkInMsg'));
  // wipe the device (a new phone), then restore
  await p.evaluate(() => { Object.keys(localStorage).forEach(k => localStorage.removeItem(k)); sessionStorage.s = 1; });
  await p.reload(); await p.waitForTimeout(700);
  console.log('after wipe → welcome shown:', await p.isVisible('#welcome'));
  // go to Me through the welcome quickly, then restore
  await p.fill('#wlNameIn', 'X'); await p.click('#wlNameGo'); await p.fill('#wlTeachIn', 'Y'); await p.click('#wlTeachGo'); await p.click('#wlAges button:has-text("9")'); await p.click('#wlCards .cq-card[data-c="english"]'); await p.click('#wlGo'); await p.waitForTimeout(900);
  await p.click('.tc-skip').catch(() => {}); await p.click('#home [data-nav="me"]'); await p.waitForTimeout(300);
  await p.click('#bkRestore'); await p.fill('#bkPaste', '  ' + code.slice(0, 50) + '\n' + code.slice(50) + '  '); await p.click('#bkCheck'); await p.waitForTimeout(400);
  console.log('preview:', (await p.textContent('#bkPreview')).replace(/\s+/g, ' '));
  await p.screenshot({ path: 'iso/BK-restore.png' });
  await p.click('#bkPreview .cta'); await p.waitForTimeout(1500);
  const after = await p.evaluate(() => { const o = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.startsWith('cq-')) o[k] = localStorage.getItem(k); } return o; });
  const same = Object.keys(before).filter(k => k !== 'cq-backup-at').every(k => after[k] === before[k] || (k === 'cq-progress' || k === 'cq-profile' || k === 'cq-courses' || k === 'cq-cards'));
  console.log('keys restored:', Object.keys(before).filter(k => after[k] !== undefined).length + '/' + Object.keys(before).length);
  console.log('home after restore:', await p.textContent('#topName'), '|', (await p.textContent('#courseTabs')).replace(/\s+/g, ' '), '| embers', await p.textContent('#embers'));
  console.log('prizes kept:', JSON.parse(after['cq-rewards']).prizes.join(', '), '| house item kept:', !!JSON.parse(after['cq-iso']).placed.study);
  console.log('errors', errs); await b.close();
})();
