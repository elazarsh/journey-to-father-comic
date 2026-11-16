# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, '.')
import recs_part1, recs_part2, recs_part3
from recs_part1 import R, SECTIONS, SRC, COST
data = dict(recs=R, sections=[dict(id=a,title=b,sub=c) for a,b,c in SECTIONS], src=SRC, cost=COST)
J = json.dumps(data, ensure_ascii=False)
html = r'''<title>המלצות לספר איטשע 0.9</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700&family=Heebo:wght@400;500;700&display=swap">
<style>
/* One reading column; each recommendation is a card with a big approve box. */
:root{--bg:#f7f4ee;--fg:#231d17;--muted:#6a5f52;--accent:#2f5d7c;--line:#ddd3c3;--card:#fffdf8;--cell:#ece6da;--ok:#2d7a4f;--no:#a4412f;--warn:#9a6a12;color-scheme:light}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#14181c;--fg:#e9e4da;--muted:#a79f92;--accent:#8ab8d8;--line:#2d343b;--card:#1b2126;--cell:#222a30;--ok:#6fcf97;--no:#f08a76;--warn:#e0b45a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#14181c;--fg:#e9e4da;--muted:#a79f92;--accent:#8ab8d8;--line:#2d343b;--card:#1b2126;--cell:#222a30;--ok:#6fcf97;--no:#f08a76;--warn:#e0b45a;color-scheme:dark}
body{background:var(--bg);color:var(--fg);font-family:Heebo,Arial,sans-serif;font-size:16px;line-height:1.7;margin:0}
.wrap{max-width:820px;margin:0 auto;padding-block:20px 80px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2{font-family:"Frank Ruhl Libre",serif;line-height:1.3;text-wrap:balance}
h1{font-size:1.8rem;color:var(--accent);margin:.2rem 0 .4rem} h2{font-size:1.35rem;margin:2.2rem 0 .2rem;padding-top:1rem;border-top:1px solid var(--line)}
.lead{color:var(--muted);margin:.2rem 0 1rem}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding:.6rem 0;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:.5rem .8rem;align-items:center}
.count{font-weight:700} .count b{color:var(--ok)} .count i{font-style:normal;color:var(--no)}
.chips{display:flex;flex-wrap:wrap;gap:.35rem}
button{font:500 .85rem Heebo,sans-serif;color:var(--fg);background:var(--cell);border:1px solid var(--line);border-radius:999px;padding:.3rem .8rem;cursor:pointer}
button[aria-pressed=true]{background:var(--accent);color:var(--bg);border-color:var(--accent)}
button:focus-visible,input:focus-visible,textarea:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.status{font-size:.8rem;color:var(--muted)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:.8rem 1rem;margin:.7rem 0;display:grid;grid-template-columns:auto 1fr;gap:.2rem .8rem}
.card.off{opacity:.62;border-style:dashed}
.card .ck{grid-row:1 / span 3;padding-top:.15rem}
.ck input{width:1.7rem;height:1.7rem;accent-color:var(--ok);cursor:pointer}
.card h3{margin:0;font:700 1.02rem Heebo,sans-serif;line-height:1.45}
.tags{display:flex;flex-wrap:wrap;gap:.3rem;margin:.15rem 0}
.tag{font-size:.75rem;border:1px solid var(--line);border-radius:999px;padding:0 .6rem;background:var(--cell);color:var(--muted);white-space:nowrap}
.tag.pg{color:var(--fg)} .tag.fam{color:var(--warn);border-color:var(--warn)} .tag.keep{color:var(--no);border-color:var(--no)}
.detail{margin:.1rem 0;font-size:.95rem}
.note{margin:.3rem 0 0;font-size:.85rem;color:var(--muted);border-inline-start:3px solid var(--line);padding-inline-start:.6rem}
details{margin-top:.3rem} summary{cursor:pointer;font-size:.8rem;color:var(--accent)}
textarea{width:100%;box-sizing:border-box;font:inherit;font-size:.9rem;background:var(--bg);color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:.4rem;min-height:3.2rem;margin-top:.3rem}
.sum{margin-top:2rem;padding:1rem;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.sum pre{white-space:pre-wrap;font:inherit;font-size:.9rem;max-height:14rem;overflow:auto;margin:.5rem 0}
@media (max-width:520px){.card{grid-template-columns:1fr}.card .ck{grid-row:auto}}
</style>
<div class="wrap" dir="rtl" lang="he">
<h1>המלצות לספר איטשע 0.9</h1>
<p class="lead">כל ההמלצות של הסוכנים במקום אחד. <strong>כולן מסומנות כמאושרות כברירת מחדל.</strong> הורד את הסימון מכל מה שלא תרצה, ואחר כך נעבור יחד ונחליט איך מתקנים. לכל המלצה: מי הציע, באילו עמודים, מה העלות, והאם צריך אישור משפחה. ההחלטות נשמרות כאן ואני יכול לקרוא אותן.</p>
<div class="bar"><span class="count" id="count"></span><span class="status" id="status"></span>
<div class="chips" id="secs"></div>
<div class="chips"><button id="bAll">אשר הכול</button><button id="bNone">בטל הכול</button><button id="bOff" aria-pressed="false">רק מה שלא אושר</button><button id="bFam" aria-pressed="false">רק מה שדורש משפחה</button></div></div>
<div id="list"></div>
<div class="sum"><strong>סיכום ההחלטות</strong> <button id="bCopy">העתק</button><pre id="sum"></pre></div>
</div>
<script>
const D = __DATA__;
const state = {}; // id -> {approved, note}
D.recs.forEach(r => state[r.id] = {approved: true, note: ''});
let db = null, only = 'all', filtOff = false, filtFam = false, saveTimer = {};
const $ = s => document.querySelector(s);
const el = (t, c, p) => { const e = document.createElement(t); if (c) e.className = c; if (p) p.appendChild(e); return e; };
function setStatus(t){ $('#status').textContent = t; }
function counts(){ const n = D.recs.length, a = D.recs.filter(r => state[r.id].approved).length; $('#count').innerHTML = '<b>' + a + ' מאושרות</b> · <i>' + (n - a) + ' לא מאושרות</i> · ' + n + ' בסך הכול'; }
function summary(){ const off = D.recs.filter(r => !state[r.id].approved), notes = D.recs.filter(r => state[r.id].note);
  let t = 'מאושרות: ' + (D.recs.length - off.length) + ' מתוך ' + D.recs.length + '\n';
  if (off.length) t += '\nלא מאושרות:\n' + off.map(r => '- ' + r.id + ' (עמ\' ' + r.pages + '): ' + r.title + (state[r.id].note ? ' | הערה: ' + state[r.id].note : '')).join('\n');
  const on = notes.filter(r => state[r.id].approved); if (on.length) t += '\n\nמאושרות עם הערה:\n' + on.map(r => '- ' + r.id + ': ' + state[r.id].note).join('\n');
  $('#sum').textContent = t; }
function save(id){ try { localStorage.setItem('v09-' + id, JSON.stringify(state[id])); } catch (e) {}
  if (!db) return; clearTimeout(saveTimer[id]);
  saveTimer[id] = setTimeout(() => { db.collection('decisions').doc(id).set({approved: state[id].approved, note: state[id].note, title: D.recs.find(r => r.id === id).title, updated: new Date().toISOString()}).then(() => setStatus('נשמר'), e => setStatus('שמירה בענן נכשלה: ' + (e && e.code || ''))); }, 350); }
function draw(){
  const list = $('#list'); list.innerHTML = '';
  D.sections.forEach(s => {
    if (only !== 'all' && only !== s.id) return;
    const recs = D.recs.filter(r => r.sec === s.id && (!filtOff || !state[r.id].approved) && (!filtFam || r.family));
    if (!recs.length) return;
    const h = el('h2', '', list); h.textContent = s.title; const p = el('p', 'lead', list); p.textContent = s.sub;
    recs.forEach(r => {
      const c = el('div', 'card' + (state[r.id].approved ? '' : ' off'), list);
      const ck = el('label', 'ck', c); const cb = el('input', '', ck); cb.type = 'checkbox'; cb.id = 'cb-' + r.id; cb.checked = state[r.id].approved; cb.setAttribute('aria-label', 'אישור: ' + r.title);
      cb.onchange = () => { state[r.id].approved = cb.checked; c.classList.toggle('off', !cb.checked); counts(); summary(); save(r.id); if (filtOff) draw(); };
      const h3 = el('h3', '', c); h3.textContent = r.title;
      const tg = el('div', 'tags', c);
      el('span', 'tag pg', tg).textContent = 'עמ\' ' + r.pages;
      r.src.forEach(k => { el('span', 'tag', tg).textContent = D.src[k]; });
      el('span', 'tag', tg).textContent = 'עלות: ' + D.cost[r.cost];
      if (r.family) el('span', 'tag fam', tg).textContent = 'דורש אישור משפחה';
      if (r.keep) el('span', 'tag keep', tg).textContent = 'המנהל ממליץ לדחות או להשאיר';
      const body = el('div', '', c);
      el('p', 'detail', body).textContent = r.detail;
      if (r.note) el('p', 'note', body).textContent = 'בדיקת המנהל: ' + r.note;
      const dt = el('details', '', body); if (state[r.id].note) dt.open = true; el('summary', '', dt).textContent = 'הערה שלי';
      const ta = el('textarea', '', dt); ta.id = 'ta-' + r.id; ta.value = state[r.id].note; ta.placeholder = 'למשל: לקצר, לשאול את דוד, לא לגעת';
      ta.oninput = () => { state[r.id].note = ta.value; summary(); save(r.id); };
    });
  });
  counts(); summary();
}
function chips(){ const box = $('#secs'); box.innerHTML = '';
  [['all', 'הכול']].concat(D.sections.map(s => [s.id, s.title])).forEach(([id, t]) => { const b = el('button', '', box); b.textContent = t; b.setAttribute('aria-pressed', only === id); b.onclick = () => { only = id; chips(); draw(); }; }); }
$('#bAll').onclick = () => { D.recs.forEach(r => { state[r.id].approved = true; save(r.id); }); draw(); };
$('#bNone').onclick = () => { D.recs.forEach(r => { state[r.id].approved = false; save(r.id); }); draw(); };
$('#bOff').onclick = e => { filtOff = !filtOff; e.currentTarget.setAttribute('aria-pressed', filtOff); draw(); };
$('#bFam').onclick = e => { filtFam = !filtFam; e.currentTarget.setAttribute('aria-pressed', filtFam); draw(); };
$('#bCopy').onclick = () => { const t = $('#sum').textContent; (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(() => setStatus('הועתק'), () => { const r = document.createRange(); r.selectNodeContents($('#sum')); const s = getSelection(); s.removeAllRanges(); s.addRange(r); setStatus('סומן: העתק ידנית'); }); };
// per-viewer fallback, then the shared store
D.recs.forEach(r => { try { const v = JSON.parse(localStorage.getItem('v09-' + r.id) || 'null'); if (v) state[r.id] = v; } catch (e) {} });
chips(); draw();
(async () => {
  try { db = (window.claude && window.claude.use) ? await window.claude.use('db') : null; } catch (e) { db = null; }
  if (!db) { setStatus('שמירה בדפדפן בלבד'); return; }
  let t = setTimeout(() => setStatus('הענן לא ענה, שמירה בדפדפן'), 10000);
  db.collection('decisions').onSnapshot(snap => { clearTimeout(t); snap.docs.forEach(d => { const v = d.data(); if (state[d.id] && v) state[d.id] = {approved: v.approved !== false, note: v.note || ''}; }); setStatus('מחובר, ההחלטות נשמרות'); const a = document.activeElement; if (!(a && a.tagName === 'TEXTAREA')) draw(); }, e => { clearTimeout(t); setStatus('אין חיבור לענן: ' + (e && e.code || '')); });
})();
</script>'''.replace('__DATA__', J)
open('/tmp/claude-0/-home-user-journey-to-father-comic/fc7d47f4-bcfe-5699-9aba-3fff59060772/scratchpad/recs.html', 'w', encoding='utf8').write(html)
print(len(html))
