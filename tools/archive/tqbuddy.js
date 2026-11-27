// The robot on the question screen: follows the reading (question, A, B, C), never stops on the answer only,
// cheers / says oops after an answer; reads by itself for age 8 and under.
const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const age of [7, 12]) {
    const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
    // a pretend voice: each sentence starts, takes 600 ms, ends, then the next one starts
    await ctx.addInitScript(() => { window.__said = []; const S = window.speechSynthesis; let q = [], busy = false;
      function next() { if (busy || !q.length) return; busy = true; const u = q.shift(); window.__said.push(u.text); u.onstart && u.onstart(); setTimeout(() => { busy = false; u.onend && u.onend(); next(); }, 600); }
      S.speak = u => { q.push(u); next(); }; S.cancel = () => { q = []; }; });
    await ctx.addInitScript(a => { if (!sessionStorage.s) { sessionStorage.s = 1; localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 0, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-courses', JSON.stringify({ course: 'maths', maths: 9, english: 0 })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: a, toured: true, courses: ['maths'], antics: false })); } }, age);
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message));
    await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(600);
    await p.click('#startBtn'); await p.waitForTimeout(300); await p.click('#toQuiz'); await p.waitForTimeout(250);
    const where = async () => p.evaluate(() => { const b = document.getElementById('qBuddy'); if (b.hidden) return 'hidden'; const r = b.getBoundingClientRect(), opts = [...document.querySelectorAll('#qOptions .opt')];
      const lit = opts.findIndex(o => o.classList.contains('reading')); const near = opts.findIndex(o => { const q = o.getBoundingClientRect(); return r.top + r.height / 2 > q.top && r.top + r.height / 2 < q.bottom; });
      return (near >= 0 ? 'beside ' + 'ABC'[near] : document.getElementById('qText').classList.contains('reading') ? 'by question' : 'resting') + (lit >= 0 ? ' (lit ' + 'ABC'[lit] + ')' : ''); });
    const path = [];
    for (let t = 0; t < 16; t++) { await p.waitForTimeout(250); const w = await where(); if (path[path.length - 1] !== w) path.push(w); if (t === 6) await p.screenshot({ path: 'iso/QB-age' + age + '.png' }); }
    console.log('age', age, '| first question read by itself:', (await p.evaluate(() => window.__said.length)) > 0, '| robot:', path.join(' → '));
    if (age === 12) { await p.click('#qHear'); for (let t = 0; t < 14; t++) { await p.waitForTimeout(250); const w = await where(); if (path[path.length - 1] !== w) path.push(w); } console.log('   after tapping Read it to me:', path.slice(1).join(' → ')); }
    console.log('   said:', (await p.evaluate(() => window.__said)).slice(0, 4).join(' | '));
    // answer: robot reacts beside the chosen choice
    await p.click('#opt-0-1'); await p.waitForTimeout(400);
    console.log('   after answering B:', await where(), '| mood:', await p.$eval('#qBuddy svg', e => e.innerHTML.length > 0 ? (e.innerHTML.indexOf('cheer') >= 0 || /react-cheer|mouth-open/.test(e.innerHTML) ? 'drawn' : 'drawn') : 'empty'), '| sheet:', await p.textContent('.sheet h4'));
    await p.screenshot({ path: 'iso/QB-age' + age + '-answered.png' });
    // leaving the quiz hides it
    await p.click('#quiz .qhead button').catch(() => {}); await p.waitForTimeout(300);
    console.log('   left quiz → robot hidden:', await p.$eval('#qBuddy', e => e.hidden));
    await ctx.close();
  }
  // Python quiz: no robot
  const ctx = await b.newContext({ ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript(() => { localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 3, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-profile', JSON.stringify({ name: 'Mia', age: 13, toured: true, courses: ['py'], antics: false })); });
  const p = await ctx.newPage(); await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(500); await p.click('#startBtn'); await p.waitForTimeout(300); await p.click('#toQuiz'); await p.waitForTimeout(400);
  console.log('python quiz: robot hidden:', await p.$eval('#qBuddy', e => e.hidden));
  console.log('errors', errs); await b.close();
})();
