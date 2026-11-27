// Runs every test in this folder against a local copy of the app.  Usage: node tests/run.js [name-filter]
// Needs: npm i -D playwright (or a global playwright with Chromium), and python3 for the Python-course check.
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..', 'prototype');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.mp3': 'audio/mpeg', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
  const data = fs.readFileSync(f), range = req.headers.range && /bytes=(\d*)-(\d*)/.exec(req.headers.range);
  const head = { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream', 'Accept-Ranges': 'bytes' };
  if (range) { // audio seeking needs range requests
    const s = range[1] ? +range[1] : 0, e = range[2] ? +range[2] : data.length - 1;
    res.writeHead(206, { ...head, 'Content-Range': `bytes ${s}-${e}/${data.length}`, 'Content-Length': e - s + 1 }); return res.end(data.slice(s, e + 1));
  }
  res.writeHead(200, { ...head, 'Content-Length': data.length }); res.end(data);
});
server.listen(0, () => {
  const BASE = 'http://localhost:' + server.address().port, only = process.argv[2] || '';
  const tests = fs.readdirSync(__dirname).filter(f => f.endsWith('.test.js') && f.includes(only)).sort();
  const results = [];
  (async () => {
    for (const t of tests) {
      console.log('\n# ' + t);
      const t0 = Date.now(), r = await new Promise(done => {
        const c = require('child_process').spawn(process.execPath, [path.join(__dirname, t)], { env: { ...process.env, BASE }, stdio: 'inherit' });
        c.on('exit', code => done(code));
      });
      results.push([t, r === 0, ((Date.now() - t0) / 1000).toFixed(0) + 's']);
    }
    console.log('\n' + results.map(([t, ok, s]) => (ok ? 'PASS ' : 'FAIL ') + t + ' (' + s + ')').join('\n'));
    server.close(); process.exit(results.every(r => r[1]) ? 0 : 1);
  })();
});
