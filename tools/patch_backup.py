# Me → "Save my progress": a backup code (copy / share), a backup file, and "Restore progress" with a preview.
# Everything the app keeps (every localStorage key starting with cq-) goes in, compressed, with a check so a
# damaged code is refused instead of breaking anything.
import re, subprocess, tempfile
SRC = '/tmp/claude-0/-home-user/04fb4c8a-c3c6-5b70-a037-a38267535510/scratchpad/lantern/lantern-quest.html'
s = open(SRC).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

rep("""        <section class="panel" aria-labelledby="myCoursesH">""",
"""        <section class="panel" aria-labelledby="backupH">
          <h2 class="sub-h" id="backupH">Save my progress</h2>
          <p class="muted small" id="backupHint">Your progress is kept on this device only. Save a backup so you never lose it, for example if the browser is cleared or you get a new phone.</p>
          <div class="gate-row"><button class="chip-btn" id="bkSave" type="button">💾 Save a backup</button><button class="chip-btn ghost" id="bkRestore" type="button">↩️ Restore progress</button></div>
          <div class="bk-box" id="bkOut" hidden>
            <span class="pe-lbl">Your backup code: keep it somewhere safe (WhatsApp to yourself, notes, email)</span>
            <textarea id="bkCode" rows="4" readonly spellcheck="false"></textarea>
            <div class="gate-row"><button class="chip-btn" id="bkCopy" type="button">📋 Copy code</button><button class="chip-btn" id="bkShare" type="button" hidden>📤 Share</button><button class="chip-btn ghost" id="bkFile" type="button">⬇️ Download file</button></div>
            <span class="gate-msg" id="bkOutMsg" aria-live="polite"></span>
          </div>
          <div class="bk-box" id="bkIn" hidden>
            <span class="pe-lbl">Paste your backup code, or choose a backup file</span>
            <textarea id="bkPaste" rows="4" spellcheck="false" placeholder="CQ1…"></textarea>
            <div class="gate-row"><label class="chip-btn ghost bk-filebtn">📁 Choose file<input type="file" id="bkPick" accept=".txt,.conceptq,text/plain" hidden></label><button class="chip-btn" id="bkCheck" type="button">Check backup</button></div>
            <div class="bk-preview" id="bkPreview" hidden></div>
            <span class="gate-msg" id="bkInMsg" aria-live="polite"></span>
          </div>
        </section>
        <section class="panel" aria-labelledby="myCoursesH">""")
rep(".pe-lbl {", """.bk-box { display: flex; flex-direction: column; gap: 8px; margin-top: 10px; }
.bk-box textarea { width: 100%; box-sizing: border-box; padding: 10px; border-radius: 12px; border: 1.5px solid var(--line); background: rgba(0,0,0,.25); color: inherit; font: 12px/1.4 'JetBrains Mono', monospace; word-break: break-all; resize: vertical; }
.bk-filebtn { cursor: pointer; display: inline-flex; align-items: center; }
.bk-preview { padding: 12px; border-radius: 14px; background: rgba(124,245,200,.1); border: 1.5px solid var(--mint, #7CF5C8); display: flex; flex-direction: column; gap: 8px; }
.bk-preview b { font-size: 16px; } .bk-preview ul { margin: 0; padding-left: 18px; font-weight: 700; font-size: 14px; }
.pe-lbl {""")

rep("  document.getElementById('meAge').addEventListener('change',", r"""  // ================= backup and restore =================
  // A backup is every cq-* key, as JSON, compressed (deflate) when the browser can, in base64url, with a short
  // checksum: "CQ1." + data + "." + check. Restoring replaces this device's progress, after a preview and a yes.
  function bkKeys() { var out = {}; for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k && k.indexOf('cq-') === 0) out[k] = localStorage.getItem(k); } return out; }
  function b64url(bytes) { var s2 = ''; for (var i = 0; i < bytes.length; i += 8192) s2 += String.fromCharCode.apply(null, bytes.subarray(i, i + 8192)); return btoa(s2).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); }
  function unb64url(t) { t = t.replace(/-/g, '+').replace(/_/g, '/'); while (t.length % 4) t += '='; var bin = atob(t), out = new Uint8Array(bin.length); for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i); return out; }
  function check(t) { var h = 5381; for (var i = 0; i < t.length; i++) h = ((h * 33) ^ t.charCodeAt(i)) >>> 0; return h.toString(36); }
  async function squeeze(bytes, how) {
    if (!window.CompressionStream) return null;
    var cs = how === 'in' ? new CompressionStream('deflate-raw') : new DecompressionStream('deflate-raw');
    var out = await new Response(new Blob([bytes]).stream().pipeThrough(cs)).arrayBuffer(); return new Uint8Array(out);
  }
  async function makeBackup() {
    saveProgress(); saveProfile();
    var payload = JSON.stringify({ app: 'conceptq', v: 1, at: Date.now(), keys: bkKeys() }), raw = new TextEncoder().encode(payload), z = await squeeze(raw, 'in').catch(function () { return null; });
    var body = (z ? 'z' : 'r') + b64url(z || raw);
    return 'CQ1.' + body + '.' + check(body);
  }
  async function readBackup(code) {
    code = String(code || '').replace(/\s+/g, '');
    var m = /^CQ1\.([zr][A-Za-z0-9_-]+)\.([a-z0-9]+)$/.exec(code); if (!m) throw new Error('This does not look like a ConceptQ backup code.');
    if (check(m[1]) !== m[2]) throw new Error('This code is incomplete or has a typo. Copy the whole code again.');
    var bytes = unb64url(m[1].slice(1));
    if (m[1][0] === 'z') { bytes = await squeeze(bytes, 'out'); if (!bytes) throw new Error('This browser cannot open this backup. Try another browser.'); }
    var data = JSON.parse(new TextDecoder().decode(bytes));
    if (!data || data.app !== 'conceptq' || typeof data.keys !== 'object') throw new Error('This backup is not from ConceptQ.');
    Object.keys(data.keys).forEach(function (k) { if (k.indexOf('cq-') !== 0 || typeof data.keys[k] !== 'string') throw new Error('This backup has something unexpected in it.'); });
    return data;
  }
  function bkSummary(data) { // what the backup holds, in words, for the preview
    var K = data.keys, J = function (k) { try { return JSON.parse(K[k] || 'null'); } catch (e) { return null; } };
    var pf = J('cq-profile') || {}, pr = J('cq-progress') || {}, cs = J('cq-courses') || {}, cards = J('cq-cards') || {};
    var lines = [];
    if (pr.current) lines.push('Python: ' + pr.current + ' of 46 lessons');
    if (cs.maths) lines.push('Maths: ' + cs.maths + ' of ' + courseTotal('maths') + ' lessons');
    if (cs.english) lines.push('English: ' + cs.english + ' of ' + courseTotal('english') + ' lessons');
    if (!lines.length) lines.push('No lessons finished yet');
    lines.push((pr.embers || 0) + ' embers' + (pr.streak ? ' · ' + pr.streak + '-day streak' : ''));
    var nc = Object.keys(cards.state || cards || {}).length; if (nc) lines.push(nc + ' flashcards');
    return { who: (pf.name || 'A learner') + (pf.age ? ', age ' + pf.age : '') + (pf.teacher ? ' · teacher ' + pf.teacher : ''), lines: lines, when: new Date(data.at).toLocaleString() };
  }
  var bkData = null;
  document.getElementById('bkSave').addEventListener('click', async function () {
    var out = document.getElementById('bkOut'), ta = document.getElementById('bkCode'), msg = document.getElementById('bkOutMsg');
    document.getElementById('bkIn').hidden = true; out.hidden = false; ta.value = 'Making your backup…'; msg.textContent = '';
    try { ta.value = await makeBackup(); msg.textContent = 'Backup ready: ' + ta.value.length + ' characters. Saved ' + new Date().toLocaleString() + '.'; try { localStorage.setItem('cq-backup-at', String(Date.now())); } catch (e) {} }
    catch (e) { ta.value = ''; msg.textContent = 'Sorry, the backup could not be made here.'; }
    document.getElementById('bkShare').hidden = !navigator.share;
  });
  document.getElementById('bkCopy').addEventListener('click', function () {
    var ta = document.getElementById('bkCode'), msg = document.getElementById('bkOutMsg');
    function fallback() { ta.focus(); ta.select(); try { document.execCommand('copy'); msg.textContent = 'Copied! Paste it somewhere safe.'; } catch (e) { msg.textContent = 'Select the code above and copy it.'; } }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(ta.value).then(function () { msg.textContent = 'Copied! Paste it somewhere safe.'; }, fallback); else fallback();
  });
  document.getElementById('bkShare').addEventListener('click', function () {
    var code = document.getElementById('bkCode').value;
    navigator.share({ title: 'ConceptQ backup', text: 'My ConceptQ progress backup for ' + profile.name + ' (paste it in Me → Restore progress):\n' + code }).catch(function () {});
  });
  document.getElementById('bkFile').addEventListener('click', function () {
    var code = document.getElementById('bkCode').value, msg = document.getElementById('bkOutMsg');
    try {
      var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([code], { type: 'text/plain' }));
      a.download = 'conceptq-' + profile.name.replace(/[^A-Za-z0-9]+/g, '') + '-' + new Date().toISOString().slice(0, 10) + '.conceptq.txt';
      document.body.appendChild(a); a.click(); a.remove(); msg.textContent = 'File saved to your downloads.';
    } catch (e) { msg.textContent = 'This browser cannot save files here: use Copy code instead.'; }
  });
  document.getElementById('bkRestore').addEventListener('click', function () {
    document.getElementById('bkOut').hidden = true; var box = document.getElementById('bkIn'); box.hidden = !box.hidden;
    document.getElementById('bkPreview').hidden = true; document.getElementById('bkInMsg').textContent = ''; bkData = null;
  });
  document.getElementById('bkPick').addEventListener('change', function (e) {
    var f = e.target.files && e.target.files[0]; if (!f) return;
    f.text().then(function (t) { document.getElementById('bkPaste').value = t.trim(); document.getElementById('bkCheck').click(); });
  });
  document.getElementById('bkCheck').addEventListener('click', async function () {
    var msg = document.getElementById('bkInMsg'), pv = document.getElementById('bkPreview'); pv.hidden = true; msg.textContent = '';
    try {
      bkData = await readBackup(document.getElementById('bkPaste').value);
      var sm = bkSummary(bkData);
      pv.innerHTML = ''; var b = document.createElement('b'); b.textContent = sm.who; pv.appendChild(b);
      var ul = document.createElement('ul'); sm.lines.forEach(function (l) { var li = document.createElement('li'); li.textContent = l; ul.appendChild(li); }); pv.appendChild(ul);
      var w = document.createElement('span'); w.className = 'muted small'; w.textContent = 'Saved ' + sm.when + '. Restoring replaces the progress on this device.'; pv.appendChild(w);
      var go = document.createElement('button'); go.type = 'button'; go.className = 'cta mint'; go.textContent = 'Restore this progress'; pv.appendChild(go);
      go.addEventListener('click', function () {
        // replace: remove this device's cq-* keys, write the backup's, then start again
        Object.keys(bkKeys()).forEach(function (k) { localStorage.removeItem(k); });
        Object.keys(bkData.keys).forEach(function (k) { localStorage.setItem(k, bkData.keys[k]); });
        msg.textContent = 'Restored! Opening your progress…'; setTimeout(function () { location.reload(); }, 600);
      });
      pv.hidden = false;
    } catch (e) { msg.textContent = e.message || 'This backup could not be read.'; }
  });
  document.getElementById('meAge').addEventListener('change',""")

open(SRC, 'w').write(s)
code = re.search(r'<script>(.*?)</script>', s, re.S).group(1)
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as t: t.write(code)
r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[:800]
print('patched')
