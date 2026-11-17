// Course switch end to end: node tcourse.js <maths|english> <lessonIndex> [desktop]
// Switches course on the Learn tab, plays the lesson, answers the quiz (hearing its sounds),
// watches the build in Number Town / the Story Library, opens the new build's card, then checks
// Python's progress and house are untouched and that switching back works.
const { chromium, devices } = require('playwright');
const course = process.argv[2], idx = +process.argv[3], desk = process.argv[4] === 'desktop';
(async () => {
  const b = await chromium.launch({ args: ['--autoplay-policy=no-user-gesture-required'] }); const errs = [], bad = [];
  const ctx = await b.newContext(desk ? { viewport: { width: 1366, height: 800 }, deviceScaleFactor: 1 } : { ...devices['iPhone 13'], deviceScaleFactor: 1 });
  await ctx.addInitScript((a) => { if (!sessionStorage.getItem('s')) { sessionStorage.setItem('s', 1);
    localStorage.setItem('cq-progress', JSON.stringify({ v: 2, current: 12, embers: 0, streak: 1, day: '' })); localStorage.setItem('cq-house-seen', '12');
    localStorage.setItem('cq-courses', JSON.stringify({ course: 'py', maths: a[0] === 'maths' ? a[1] : 0, english: a[0] === 'english' ? a[1] : 0 })); } }, [course, idx]);
  const p = await ctx.newPage(); p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push('console: ' + m.text()); }); p.on('response', r => { if (r.status() >= 400) bad.push(r.url()); });
  await p.goto('http://localhost:8765/index.html'); await p.waitForTimeout(800);
  console.log('tabs:', (await p.textContent('#courseTabs')).replace(/\s+/g, ' '), '| python card:', await p.textContent('#cardTitle'));
  await p.click('#courseTabs button:nth-child(' + (course === 'maths' ? 2 : 3) + ')'); await p.waitForTimeout(500);
  console.log('card:', await p.textContent('#cardEyebrow'), '|', await p.textContent('#cardTitle'), '|', await p.textContent('#ctaText'), '| path:', await p.textContent('#pathTitle'), await p.textContent('#pathCount'), '| topics', await p.$$eval('#topics .topic', e => e.length), '| tile:', await p.textContent('#pyLevel'), '| nav:', (await p.textContent('#home [data-navbar]')).replace(/\s+/g, ' '));
  await p.screenshot({ path: 'iso/C-' + course + idx + '-home.png' });
  await p.click('#startBtn'); await p.waitForTimeout(600);
  console.log('lesson:', await p.textContent('#learnTag'), '|', await p.textContent('#learnTitle'), '| steps', await p.$$eval('#steps button', e => e.length));
  await p.click('#playBtn'); await p.waitForTimeout(4500);
  console.log('caption:', (await p.textContent('#caption')).slice(0, 80), '| audio:', await p.evaluate(() => { var a = window.__aud && window.__aud(); return a ? 'step ' + a.step + ' mode ' + a.mode + ' t=' + a.t.toFixed(1) + ' paused=' + a.paused + ' url=' + (a.voice[0] && a.voice[0].url) : 'none'; }));
  await p.screenshot({ path: 'iso/C-' + course + idx + '-lesson.png' });
  await p.click('#toQuiz'); await p.waitForTimeout(400);
  const nq = +((await p.textContent('#qTag')).match(/of (\d+)/)[1]);
  for (let q = 0; q < nq; q++) {
    const info = await p.evaluate(() => ({ t: document.getElementById('qText').textContent, pic: document.getElementById('qPic').hidden ? '' : document.getElementById('qPic').textContent, code: !document.getElementById('qCode').hidden, hear: document.getElementById('qHear').hidden ? '' : document.getElementById('qHear').textContent, opts: [...document.querySelectorAll('#qOptions .opt .val')].map(e => e.textContent) }));
    if (q === 0 || info.hear.indexOf('again') >= 0) { await p.waitForTimeout(1200); }
    const ph = await p.evaluate(() => { var a = [...document.querySelectorAll('audio')]; return 'n/a'; });
    console.log(' Q' + (q + 1) + ':', info.t, '[' + info.pic + ']', info.opts.join(' | '), info.code ? 'CODE-BOX-SHOWN' : '', info.hear);
    if (q === 0) await p.screenshot({ path: 'iso/C-' + course + idx + '-quiz.png' });
    for (let k = 0; k < info.opts.length; k++) { await p.click('#opt-' + q + '-' + k); await p.waitForTimeout(90); if (await p.$('.sheet.is-right')) break; await p.evaluate((qq) => window.__undo(qq), q); await p.waitForTimeout(50); }
    await p.click('#sheetBtn'); await p.waitForTimeout(160);
  }
  console.log('done:', await p.textContent('#doneTitle'), '|', await p.textContent('#doneText'), '| earned:', (await p.textContent('#doneEarned')).replace(/\s+/g, ' '), '| cards +' + await p.textContent('#dCards'));
  await p.screenshot({ path: 'iso/C-' + course + idx + '-done.png' });
  await p.click('#doneHouse'); await p.waitForTimeout(2600);
  const fr = p.frames().find(f => /world\.html/.test(f.url()));
  console.log('world:', fr ? fr.url().split('/').pop() : 'NO WORLD FRAME', '|', fr && await fr.textContent('#count'), '|', fr && await fr.textContent('#toast'));
  await p.screenshot({ path: 'iso/C-' + course + idx + '-world.png' });
  if (fr) { await fr.click('.item[data-i="' + idx + '"] .hit', { force: true }); await p.waitForTimeout(600); console.log('card:', await fr.textContent('#shT'), '|', await fr.textContent('#shV'), '|', await fr.textContent('#shP')); await p.screenshot({ path: 'iso/C-' + course + idx + '-card.png' }); }
  const saved = await p.evaluate(() => [localStorage.getItem('cq-progress'), localStorage.getItem('cq-courses')]);
  console.log('saved:', saved.join(' || '));
  // back to Python: its card, path and house are as they were
  await p.click('#house [data-nav="home"]').catch(() => p.click('[data-nav="home"]'));
  await p.waitForTimeout(400); await p.click('#courseTabs button:nth-child(1)'); await p.waitForTimeout(500);
  console.log('python again:', await p.textContent('#cardEyebrow'), '|', await p.textContent('#cardTitle'), '| tabs:', (await p.textContent('#courseTabs')).replace(/\s+/g, ' '));
  await p.click('[data-nav="house"]'); await p.waitForTimeout(1500);
  console.log('house frame:', p.frames().map(f => f.url().split('/').pop()).filter(u => /house|world/.test(u)).join(','));
  await p.reload(); await p.waitForTimeout(800);
  console.log('after reload:', (await p.textContent('#courseTabs')).replace(/\s+/g, ' '), '|', await p.textContent('#cardTitle'));
  await p.click('[data-nav="cards"]'); await p.waitForTimeout(400); console.log('cards:', await p.textContent('#cardsSummary'));
  console.log('errors', errs, 'bad', bad);
  await b.close();
})();
