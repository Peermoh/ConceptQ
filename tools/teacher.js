// The robot teacher's name is the learner's choice (cq-profile.teacher, 'Nibb' by default).
// Every bit of text that says Nibb (labels, captions, buttons, aria-labels) shows the chosen name instead.
// CQSetTeacher(name) changes it live; text already showing an earlier chosen name is updated too.
(function () {
  var name = 'Nibb', old = ['Nibb'], RX = null, ATTRS = ['aria-label', 'title', 'placeholder', 'alt'], observer = null;
  function clean(t) { return String(t || '').replace(/[\u0000-\u001f<>&"\\]/g, '').trim().slice(0, 14); }
  try { var p = JSON.parse(localStorage.getItem('cq-profile') || 'null'); if (p && clean(p.teacher)) name = clean(p.teacher); } catch (e) {}
  function esc(t) { return t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function build() { var olds = old.filter(function (o) { return o !== name; }); RX = olds.length ? new RegExp('\\b(' + olds.map(esc).join('|') + ')\\b', 'g') : null; }
  function has(v) { if (!RX || !v) return false; RX.lastIndex = 0; return RX.test(v); }
  function fixText(n) { if (has(n.nodeValue)) { RX.lastIndex = 0; n.nodeValue = n.nodeValue.replace(RX, name); } }
  function fixEl(el) { ATTRS.forEach(function (a) { var v = el.getAttribute && el.getAttribute(a); if (has(v)) { RX.lastIndex = 0; el.setAttribute(a, v.replace(RX, name)); } }); }
  function fix(root) {
    if (!root || !RX) return;
    if (root.nodeType === 3) { fixText(root); return; }
    if (root.nodeType !== 1) return;
    if (/^(SCRIPT|STYLE)$/.test(root.tagName)) return;
    fixEl(root);
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), t;
    while ((t = w.nextNode())) { var pt = t.parentNode; if (pt && /^(SCRIPT|STYLE)$/.test(pt.tagName)) continue; fixText(t); }
    root.querySelectorAll('[aria-label],[title],[placeholder],[alt]').forEach(fixEl);
  }
  function apply() {
    build(); if (!RX || !document.body) return;
    if (has(document.title)) { RX.lastIndex = 0; document.title = document.title.replace(RX, name); }
    fix(document.body);
    if (!observer) {
      observer = new MutationObserver(function (ms) { ms.forEach(function (m) {
        if (m.type === 'characterData') fixText(m.target); else if (m.type === 'attributes') fixEl(m.target); else m.addedNodes.forEach(fix);
      }); });
      observer.observe(document.body, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ATTRS });
    }
  }
  window.CQ_TEACHER = name;
  window.CQSetTeacher = function (n) { n = clean(n) || 'Nibb'; if (old.indexOf(name) < 0) old.push(name); name = n; window.CQ_TEACHER = n; apply(); };
  if (document.body) apply(); else document.addEventListener('DOMContentLoaded', apply);
})();
