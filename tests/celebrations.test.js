// Celebrations: the recorded cheer starts with the banner, and every firework burst drawn gets a bang at the same moment.
const { check, finish, open } = require('./lib');
(async () => {
  const { b, p, errs } = await open({ autoplay: true, init: () => {
    window.__ev = [];
    const st = AudioBufferSourceNode.prototype.start;
    AudioBufferSourceNode.prototype.start = function (...a) { if (this.buffer && this.buffer.duration > 0.5) window.__ev.push({ dur: this.buffer.duration, t: performance.now() }); return st.apply(this, a); };
  } });
  await p.fill('#wlNameIn', 'Mia'); await p.click('#wlNameGo'); await p.waitForTimeout(1500); // the first tap turns sound on and loads the clips
  for (const big of [false, true]) {
    const r = await p.evaluate(async big => {
      window.__ev = []; window.__booms = []; const ob = window.CQBoom;
      window.CQBoom = function () { window.__booms.push(performance.now()); ob(); };
      const t0 = performance.now(); window.CQCelebrate('Congratulations!', 'test', big);
      await new Promise(r => setTimeout(r, big ? 4500 : 3200)); window.CQBoom = ob;
      return { t0, ev: window.__ev, booms: window.__booms };
    }, big);
    const cheer = r.ev.find(c => c.dur > 4), bangs = r.ev.filter(c => c.dur < 2);
    const gap = Math.max(0, ...r.booms.map(bt => Math.min(...bangs.map(c => Math.abs(c.t - bt)), 1e9)));
    const name = big ? 'big celebration' : 'small celebration';
    check(cheer && cheer.t - r.t0 < 300, `${name}: the cheer starts with the banner (+${cheer ? Math.round(cheer.t - r.t0) : '-'} ms)`);
    check(r.booms.length > 0 && bangs.length > 0 && gap < 80, `${name}: ${r.booms.length} bursts, ${bangs.length} bangs, worst gap ${Math.round(gap)} ms`);
  }
  check(!errs.length, 'no page errors ' + errs.join(' | '));
  await b.close(); finish();
})();
