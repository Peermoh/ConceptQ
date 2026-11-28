// The Maths "Work it out" pad: each lesson offers the tools that fit it, and every tool works on a phone.
const { check, finish, open, onboard } = require('./lib');
(async () => {
  const { b, p, errs } = await open({ hooks: [['  function scratchOpen() {',
    `window.__pad = function (key, text) { useCourse('maths', true); var k = Object.keys(LESSON_DATA).filter(function (i) { return LESSON_DATA[i].key === key; })[0];
       LD = LESSON_DATA[k]; Q = [{ text: text, options: ['1', '2', '3'], why: ['', '', ''], answer: 0 }]; qi = 0; scratchReset(); scratchOpen(); return CQTools.forLesson(key, text); };`]] });
  await onboard(p, 'maths');
  await p.click('#startBtn'); await p.waitForTimeout(700); await p.click('#toQuiz', { force: true }); await p.waitForTimeout(700); // the pad belongs to the quiz screen
  const pad = (key, text) => p.evaluate(([k, t]) => window.__pad(k, t), [key, text]);
  const read = () => p.textContent('#scratchTool .tl-read').catch(() => '');
  const tab = n => p.click(`#scratchTabs button:has-text("${n}")`);
  const fits = async name => check(await p.evaluate(() => { const r = document.querySelector('.scratch-sheet').getBoundingClientRect(); return [...document.querySelectorAll('#scratchTool *')].every(e => { const q = e.getBoundingClientRect(); return !q.width || (q.left >= r.left - 1 && q.right <= r.right + 1); }); }), `${name}: fits the phone screen`);

  let t = await pad('m3_add', 'A shop sold 367 pens on Monday and 258 on Tuesday. How many pens?');
  check(t[0] === 'columns', 'adding lesson opens on the column sum: ' + t.join(', '));
  const cells = await p.$$eval('#scratchTool .tl-cell', c => c.map(x => x.textContent).join(''));
  check(/367/.test(cells) && /258/.test(cells), 'column sum is filled in with the two numbers from the question (' + cells + ')');
  await p.click('#scratchTool .tl-key:has-text("5")');
  check((await p.$$eval('#scratchTool .tl-ans', c => c.map(x => x.textContent).join(''))).includes('5'), 'tapping a number writes it in the answer row');
  await fits('column sum');
  await p.click('#scratchTool .tl-op'); check((await p.textContent('#scratchTool .tl-op')) === '−', 'the sign can be changed');
  await tab('Number line'); const box = await p.locator('#scratchTool svg').boundingBox();
  await p.mouse.click(box.x + box.width * 0.2, box.y + box.height * 0.68); await p.mouse.click(box.x + box.width * 0.6, box.y + box.height * 0.68);
  check(/→ now at/.test(await read()) && (await p.$$('#scratchTool svg path')).length === 1, 'number line: two taps make one hop with its size (' + (await read()) + ')');
  await fits('number line');
  await tab('Column sum'); check((await p.$$eval('#scratchTool .tl-ans', c => c.map(x => x.textContent).join(''))).includes('5'), "switching tools keeps each tool's work");

  t = await pad('m2_share', 'Share 12 laddoos between 3 children. How many each?');
  check(t[0] === 'counters', 'sharing lesson opens on counters');
  check((await p.textContent('#scratchTool .tl-num')) === '3', 'the 3 children from the question become 3 plates');
  await p.click('#scratchTool button:has-text("+10")'); await p.click('#scratchTool button:has-text("+1")'); await p.click('#scratchTool button:has-text("+1")');
  await p.click('#scratchTool button:has-text("Deal out")');
  check(/4 \/ 4 \/ 4 on the plates/.test(await read()), 'deal out shares 12 counters into 3 plates of 4 (' + (await read()) + ')');
  await fits('counters');

  t = await pad('m2_groups', '3 children each hold up one hand. How many fingers?');
  check((await p.textContent('#scratchTool .tl-num')) === '3' && await p.isVisible('#scratchTool button:has-text("+1 in each")') && !(await p.isVisible('#scratchTool button:has-text("Deal out")')),
    'an "each" question: 3 groups (one per child) and a "+1 in each" button');
  for (let i = 0; i < 5; i++) await p.click('#scratchTool button:has-text("+1 in each")');
  check(/3 groups of 5 = 15 in all/.test(await read()), 'tapping "+1 in each" 5 times (one per finger) shows 3 groups of 5 = 15 (' + (await read()) + ')');
  await fits('counters in groups');

  t = await pad('m3_shapes', 'How many sides does a hexagon have?');
  const dot = async (x, y) => { const bb = await p.locator('#scratchTool svg').boundingBox(); await p.mouse.click(bb.x + (25 + x * 50) / 450 * bb.width, bb.y + (25 + y * 50) / 300 * bb.height); };
  await dot(1, 1); await dot(3, 1); await dot(3, 3); await dot(1, 1);
  check(/3 sides drawn/.test(await read()), 'dot grid: tapping dots draws straight sides (' + (await read()) + ')');
  await p.click('#scratchTool button:has-text("Mirror line")');
  check((await p.$$('#scratchTool line[stroke-dasharray="6 5"]')).length === 3, 'mirror line reflects every side');

  t = await pad('m3_fractions', 'What fraction is shaded?');
  await p.click('#scratchTool button[data-n="4"]');
  for (let i = 0; i < 3; i++) await p.click(`#scratchTool svg [data-i="${i}"]`);
  check(/3 of 4 equal parts coloured = 3\/4/.test(await read()), 'fractions: tap parts to colour them (' + (await read()) + ')');

  t = await pad('m2_time', 'What time is it?');
  for (let i = 0; i < 9; i++) await p.click('#scratchTool button:has-text("+5 min")');
  check(/3:45 · quarter to 4/.test((await read()).replace(/\s+/g, ' ')), 'clock: the time and its words follow the hands (' + (await read()) + ')');
  await fits('clock');

  t = await pad('m2_money', 'A pencil costs ₹15 and an eraser ₹8. How much in all?');
  for (const v of ['₹10', '₹5', '₹5', '₹2']) await p.click(`#scratchTool .tl-coins button:text-is("${v}")`);
  check(/₹22/.test(await read()), 'money: coins add up (' + (await read()) + ')');
  await p.click('#scratchTool .tl-tray button >> nth=0'); check(/₹12/.test(await read()), 'tapping a coin on the tray takes it back');
  await fits('money');

  t = await pad('m2_data', 'Which fruit is the most?');
  for (let i = 0; i < 7; i++) await p.click('#scratchTool .tl-trow >> nth=0 >> button:text-is("+")');
  check((await p.$$('#scratchTool .tl-trow >> nth=0 >> .tl-tg.five')).length === 1 && (await p.textContent('#scratchTool .tl-trow >> nth=0 >> .tl-num')) === '7', 'tally: 7 marks show as one crossed group of five and two');

  t = await pad('m2_numbers', 'How many tens are in 47?');
  for (let i = 0; i < 4; i++) await p.click('#scratchTool .tl-pvc >> nth=1 >> button:text-is("+")');
  for (let i = 0; i < 7; i++) await p.click('#scratchTool .tl-pvc >> nth=2 >> button:text-is("+")');
  check(/^47$/.test((await read()).trim()), 'place-value blocks build 47 from 4 tens and 7 ones (' + (await read()) + ')');

  t = await pad('m3_measure', 'How long is the pencil?');
  check(t[0] === 'ruler' && (await p.$$('#scratchTool .tl-facts span')).length >= 4, 'measuring lesson: a ruler with the unit facts');
  await p.click('#scratchClear'); check(/5 cm/.test(await read()), 'Reset puts the tool back to the start');
  await tab('Chalk'); check(await p.isVisible('#scratchCv') && !(await p.isVisible('#scratchTool')), 'the chalkboard is always there');
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
