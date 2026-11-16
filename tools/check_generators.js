const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
const api = new Function(src + '; return { GEN: GEN };')();
const out = [];
for (const [key, gens] of Object.entries(api.GEN)) gens.forEach((g, gi) => {
  for (let n = 0; n < 40; n++) {
    const q = g(); if (!q) continue;
    const code = q.code.replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
    out.push({ key, gi, text: q.text, code, right: q.options[q.answer], n: q.options.length, uniq: new Set(q.options).size });
  }
});
fs.writeFileSync(process.argv[3], JSON.stringify(out));
console.log('made', out.length);
