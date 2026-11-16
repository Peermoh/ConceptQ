// Reads the quiz code straight from the app page (local file, written by us) and
//   1. writes 40 samples from every question generator to a JSON file, for Python to run
//   2. builds 300 quizzes per lesson and checks their length, answers and topics.
// Usage: node check.js <page.html> <samples-out.json>
const fs = require('fs');
const page = fs.readFileSync(process.argv[2], 'utf8');
const code = page.slice(page.indexOf('  function ri('), page.indexOf('  function startQuiz'));
const names = [...page.matchAll(/  var Q_([A-Z0-9]+) = \[/g)].map(m => m[1]);
let blocks = '';
for (const N of names) { const a = page.indexOf('  var Q_' + N + ' = ['); blocks += page.slice(a, page.indexOf('\n  ];\n', a) + 6); }
// LESSON_DATA ties each quiz to its key
const keyOf = {}; for (const m of page.matchAll(/board: BOARD_([A-Z0-9]+), quiz: Q_[A-Z0-9]+, key: '([^']+)'/g)) keyOf[m[1]] = m[2];
const api = (new Function(blocks + code + '; return { GEN: GEN, makeQuiz: makeQuiz, Q: {' + names.map(N => 'Q_' + N + ': Q_' + N).join(',') + '} };'))();
const plain = c => c.replace(/<[^>]+>/g, '').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&');
const out = [];
for (const [key, gens] of Object.entries(api.GEN)) gens.forEach((g, gi) => {
  for (let n = 0; n < 40; n++) { const q = g(); if (q) out.push({ key, gi, text: q.text, code: plain(q.code), right: q.options[q.answer], uniq: new Set(q.options).size }); }
});
fs.writeFileSync(process.argv[3], JSON.stringify(out));
const TOPIC = [/\.pop\(/, /\.append\(/, /\[-1\]/, /\[\d:\d\]/, /len\(/, /\s%\s/, /\/\//, /\*\*/, /\+=/, /range\(\d+, \d+, \d+\)/, /break/, /elif/, / and /, / - /, /sqrt\(/, /ceil\(|floor\(/, /\.get\(/, /\.split\(/, /\.join\(/, /\.replace\(/, /\.count\(/, /\.sort\(|sorted\(/, /\[::/];
let problems = 0;
for (const N of names) {
  const k = keyOf[N]; if (!k) continue;
  const qs = api.Q['Q_' + N]; let dup = 0, distinct = new Set();
  for (let r = 0; r < 300; r++) {
    const quiz = api.makeQuiz({ key: k, quiz: qs });
    if (quiz.length !== qs.length) problems++;
    quiz.forEach(q => { if (q.answer < 0 || q.answer >= q.options.length || q.why.length !== q.options.length || new Set(q.options).size !== q.options.length) problems++; });
    const t = quiz.map(q => TOPIC.findIndex(re => re.test(plain(q.code)))).filter(x => x >= 0);
    if (new Set(t).size !== t.length) dup++;
    distinct.add(quiz.map(q => plain(q.code) + q.options.join('|')).join('#'));
  }
  console.log(k.padEnd(9), 'questions', String(qs.length).padStart(2), '| generators', (api.GEN[k] || []).length, '| repeated topic', dup, '/300 | different', distinct.size, '/300');
}
console.log('generator samples', out.length, '| broken quizzes', problems);
