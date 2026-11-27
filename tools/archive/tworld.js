const { chromium, devices } = require('playwright');
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const [c, v, build, dev] of [['maths', 12, 11, 'iPhone 13'], ['english', 13, 12, 'iPhone 13'], ['maths', 7, 6, null], ['english', 4, -1, null]]) {
    const ctx = await b.newContext(dev ? { ...devices[dev], deviceScaleFactor: 1 } : { viewport: { width: 1366, height: 768 } });
    await ctx.addInitScript(() => localStorage.setItem('cq-scene', JSON.stringify({ world: 'canyon', weather: 'rain', time: 'sunset' })));
    const p = await ctx.newPage(); p.on('pageerror', e => errs.push(c + ': ' + e.message));
    await p.goto('file://' + process.cwd() + '/lantern/world.html?course=' + c + '&v=' + v + (build >= 0 ? '&build=' + build : '')); await p.waitForTimeout(2200);
    await p.screenshot({ path: 'iso/W-' + c + v + (dev ? '' : '-desk') + '.png' });
    console.log(c, v, await p.textContent('#count'), '| toast:', await p.textContent('#toast'), '| items', await p.$$eval('.item', e => e.length), 'plots', await p.$$eval('.plot', e => e.length));
    await ctx.close();
  }
  console.log('errors', errs); await b.close();
})();
