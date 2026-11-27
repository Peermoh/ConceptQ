// Runs every Maths/English quiz generator many times: no throws, distinct options, right answer first.
const fs = require('fs');
const s = fs.readFileSync(process.argv[2] || 'lantern/lantern-quest.html', 'utf8');
const grab = (a, b) => { const i = s.indexOf(a); return s.slice(i, s.indexOf(b, i)); };
let src = ['function ri(', 'function pickOne(', 'function shuffled('].map(h => { const i = s.indexOf(h); return s.slice(i, s.indexOf('\n', i)); }).join('\n');
src += '\n' + grab('  function hlCode(code)', '  var WORDS = [');
src += '\nvar GEN = {}, Q_STEPS = {}, GEN_STEPS = {}, CARDS = [];\n';
src += grab('  // ==== COURSE PACKS', '  // ==== END COURSE PACKS');
src += '\n;module.exports = { GEN, COURSE_PACKS, GEN_STEPS, Q_STEPS, CARDS, setL: function (l) { QLEVEL = l; } };';
fs.writeFileSync('/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/iso/_g2.js', src);
const M = require('/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/iso/_g2.js');
let bad = 0, total = 0, samples = [];
for (const c of ['maths', 'english']) {
  const P = M.COURSE_PACKS[c];
  Object.values(P.data).forEach(ld => {
    const gs = M.GEN[ld.key] || []; if (!gs.length) { console.log('NO GEN', ld.key); bad++; }
    if ((M.GEN_STEPS[ld.key] || []).length !== gs.length) { console.log('GEN_STEPS count', ld.key); bad++; }
    gs.forEach((g, gi) => {
      let nulls = 0;
      for (let t = 0; t < 600; t++) {
        M.setL(t % 3); let q; try { q = g(); } catch (e) { console.log('THROW', ld.key, gi, e.message); bad++; break; }
        if (!q) { nulls++; continue; } total++;
        if (new Set(q.options).size !== q.options.length) { console.log('DUP', ld.key, q.options); bad++; }
        if (q.options.length < 2 || q.why.length !== q.options.length || q.why.some(w => !w)) { console.log('SHAPE', ld.key, q); bad++; }
        if (q.options.some(o => /undefined|NaN|null/.test(o)) || /undefined|NaN/.test(q.text + q.why.join(' ') + (q.pic || ''))) { console.log('UNDEF', ld.key, q.text, q.options); bad++; }
        if (q.snd && q.snd.some(x => typeof x !== 'string')) { console.log('SND', ld.key); bad++; }
        if (t < 2) samples.push(ld.key + ': ' + q.text + ' [' + (q.pic || '') + '] ' + q.options.map((o, i) => (i === 0 ? '*' : '') + o).join(' | ') + (q.snd ? '  🔊' + q.snd.join(',') : ''));
      }
      if (nulls > 400) { console.log('MOSTLY NULL', ld.key, gi, nulls); bad++; }
    });
  });
}
console.log(samples.join('\n'));
console.log('generated', total, 'problems', bad);
