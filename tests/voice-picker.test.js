const { BASE, check, finish } = require('./lib');
// Feeds realistic device voice lists to the app's pickVoice() and checks the pick is male and matches the narrator.
const { chromium } = require('playwright');
const V = (name, lang, local = true) => ({ name, lang, localService: local, voiceURI: name });
const LISTS = {
  iphone: [V('Samantha', 'en-US'), V('Karen', 'en-AU'), V('Daniel', 'en-GB'), V('Rishi', 'en-IN'), V('Moira', 'en-IE'), V('Veena', 'en-IN'), V('Arthur', 'en-GB')],
  windowsEdge: [V('Microsoft Zira - English (United States)', 'en-US'), V('Microsoft David - English (United States)', 'en-US'), V('Microsoft Ryan Online (Natural) - English (United Kingdom)', 'en-GB', false), V('Microsoft Prabhat Online (Natural) - English (India)', 'en-IN', false), V('Microsoft Neerja Online (Natural) - English (India)', 'en-IN', false)],
  chromeDesktop: [V('Google US English', 'en-US', false), V('Google UK English Female', 'en-GB', false), V('Google UK English Male', 'en-GB', false), V('Google हिन्दी', 'hi-IN', false)],
  androidChrome: [V('English United States', 'en-US'), V('English United Kingdom', 'en-GB'), V('English India', 'en-IN')],
};
const EXPECT = { // [prabhat, ryan]
  iphone: ['Rishi', 'Daniel|Arthur'], windowsEdge: ['Prabhat', 'Ryan'], chromeDesktop: ['UK English Male', 'UK English Male'], androidChrome: ['English India', 'English United Kingdom'],
};
(async () => {
  const b = await chromium.launch(); const p = await (await b.newContext()).newPage();
  await p.route('**/index.html', async r => { const res = await r.fetch(); let t = await res.text();
    t = t.replace('function voiceLang() {', 'window.__pick = function (n) { profile.narrator = n; voiceMemo.key = ""; var v = pickVoice(); return v && v.name; };\n  function voiceLang() {');
    await r.fulfill({ response: res, body: t }); });
  await p.addInitScript(() => { window.__voices = []; Object.defineProperty(window, 'speechSynthesis', { value: { getVoices: () => window.__voices, speak() {}, cancel() {} } }); window.SpeechSynthesisUtterance = function () {}; });
  await p.goto(BASE + '/index.html'); await p.waitForTimeout(800);
  let fails = 0;
  for (const [dev, list] of Object.entries(LISTS)) {
    await p.evaluate(l => { window.__voices = l; }, list);
    for (const [i, n] of ['prabhat', 'ryan'].entries()) {
      const got = await p.evaluate(n => window.__pick(n), n), ok = new RegExp(EXPECT[dev][i]).test(got || '');
      check(ok, `${dev}: narrator ${n} uses ${got}`);
    }
  }
  await b.close(); finish();
})();
