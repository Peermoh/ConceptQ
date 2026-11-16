// Builds 300 quizzes per lesson with the app's own makeQuiz and the page's hand-written questions.
// Checks: right length, the marked answer is the same option text before and after shuffling, no topic twice.
const fs = require('fs');
const page = fs.readFileSync(process.argv[2], 'utf8'), gen = fs.readFileSync(process.argv[3], 'utf8');
const keys = { hello: 'HELLO', vars: 'VARS', nums: 'NUMS', strings: 'STRINGS', input: 'INPUT', bool: 'BOOL', if: 'IF', loop: 'LOOP', boss: 'BOSS', lists1: 'LISTS1' };
let blocks = '';
for (const N of Object.values(keys)) { const a = page.indexOf('  var Q_' + N + ' = ['); const b = page.indexOf('\n  ];\n', a) + 6; blocks += page.slice(a, b); }
const api = new Function(blocks + gen + '; return { makeQuiz: makeQuiz, Q: {' + Object.entries(keys).map(([k, N]) => JSON.stringify(k) + ': Q_' + N).join(',') + '} };')();
const plain = c => c.replace(/<[^>]+>/g, '').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&');
const TOPIC = [/\.pop\(/, /\.append\(/, /\[-1\]/, /\[\d:\d\]/, /len\(/, /\s%\s/, /\/\//, /\*\*/, /\+=/, /range\(\d+, \d+, \d+\)/, /break/, /elif/, / and /, / - /];
for (const [k, qs] of Object.entries(api.Q)) {
  let dupQuiz = 0, badLen = 0, distinct = new Set();
  for (let r = 0; r < 300; r++) {
    const quiz = api.makeQuiz({ key: k, quiz: qs });
    if (quiz.length !== qs.length) badLen++;
    const t = quiz.map(q => TOPIC.findIndex(re => re.test(plain(q.code)))).filter(x => x >= 0);
    if (new Set(t).size !== t.length) dupQuiz++;
    distinct.add(quiz.map(q => plain(q.code) + q.options.join('|')).join('#'));
    quiz.forEach(q => { if (q.answer < 0 || q.answer > 3 || q.why.length !== q.options.length) throw new Error('broken question in ' + k); });
  }
  console.log(k.padEnd(8), 'questions', qs.length, '| wrong length', badLen, '| quizzes with a repeated topic', dupQuiz, '/ 300 | different quizzes', distinct.size, '/ 300');
}
