/* Print edition: renders site/index.html (built by tools/build_site.py) sheet by sheet at print resolution.
   Opened with ?print the viewer lays every page out for a whole A4 sheet (panels cover the full page area);
   a softened copy of the page's main picture sits under the thin outer margin, so no sheet has an empty area. Sheets are saved as JPEG; tools/print_pdf.py binds them into the PDF.
   Usage: node tools/print_pdf.js [he|en] [dpi]   (needs Playwright with Chromium) */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
const lang = process.argv[2] || 'he';
const dpi = +(process.argv[3] || 300);
const outDir = path.join(__dirname, '..', 'print', 'sheets-' + lang);
const MM = 96 / 25.4;
const QR = 'data:image/png;base64,' + fs.readFileSync(path.join(__dirname, '..', 'print', 'qr-site.png')).toString('base64');
const BACK = {
  he: { kicker: 'סיפורי סבא עמנואל · ספר 1', title: 'הגיבור שלי',
    blurb: ['מרץ 1946. אירופה עוד מעלה עשן אחרי המלחמה, וילד בן שמונה וחצי יוצא עם אמו ואחיו הגדול למסע ארוך: רכבת דרך צרפת, אונייה ענקית, והים הפתוח.',
      'בסוף הדרך מחכה לו אבא שמעולם לא ראה, והגיבור שדמיין בכל לילה.',
      'בדרך הוא ימצא חבר ויאבד אותו, יצחק מול סערה, יפגוש גנבים בנאפולי, ויגלה סוד שמסתתר מתחת למיטה.',
      'סיפור אמיתי, כפי שסבא עמנואל סיפר אותו לנכדיו בבית הכנסת. סיפור על מה שבאמת הופך אדם לגדול.'],
    for: 'לכל המשפחה: לילדים, להורים ולסבים', online: 'לקריאה באתר, עם אנימציות ותנועה:' },
  en: { kicker: 'GRANDPA EMMANUEL’S STORIES · BOOK 1', title: 'My Hero',
    blurb: ['March 1946. Europe is still smoking after the war, and an eight-and-a-half-year-old boy sets out with his mother and big brother on a long journey: a train across France, a giant ship, and the open sea.',
      'At the end of the road waits a father he has never seen, and the hero he has imagined every night.',
      'On the way he will find a friend and lose him, laugh at a storm, meet thieves in Naples, and discover a secret hiding under the bed.',
      'A true story, as Grandpa Emmanuel told it to his grandchildren in the synagogue. A story about what really makes a person big.'],
    for: 'For the whole family: children, parents and grandparents', online: 'Read it online, with animation:' }
};
const CSS = `
html.printing, html.printing body { background: #0d0907 !important; overflow: visible !important; }
html.printing { --rim: #1b1410; }
html.printing #atmos, html.printing .topbar, html.printing .hud, html.printing .rail, html.printing #loader, html.printing #studio, html.printing .cue, html.printing #startBtn, html.printing #restart, html.printing .cv-letter { display: none !important; }
html.printing .sheet { width: 210mm !important; height: 297mm !important; min-height: 0 !important; margin: 0 !important; padding: 0 !important; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
html.printing .sheet::before { content: ""; position: absolute; inset: -8mm; z-index: 0; background: var(--bg) center / cover no-repeat; filter: blur(14px) brightness(.5) saturate(.95); }
html.printing .cover.cine::before { display: block !important; animation: none !important; transform: none !important; }
html.printing .sheet::after { content: ""; position: absolute; inset: 0; z-index: 0; background: radial-gradient(ellipse at 50% 50%, transparent 40%, rgba(0, 0, 0, .45) 100%); pointer-events: none; }
html.printing .page { counter-increment: pg; }
html.printing .cover.sheet { display: block; }
html.printing .cover.sheet::before { display: none !important; }
html.printing .cover .cv-art { opacity: 1 !important; transform: none !important; transition: none !important; inset: 0 !important; filter: saturate(.95) brightness(.72) !important; }
html.printing .cover .cv-sun { top: 25% !important; opacity: .5 !important; transition: none !important; }
html.printing .cover .cv-rays { top: 25% !important; opacity: .45 !important; transition: none !important; }
html.printing .cover .cover-inner { position: absolute; top: 22mm; left: 14mm; right: 14mm; max-width: none; transition: none !important; }
html.printing .cover .cover-inner::before { inset: -8% -6% !important; }
html.printing .cover .title { font-size: 34mm !important; }
html.printing .cover .title .ch { transition: none !important; animation: none !important; opacity: 1 !important; transform: none !important; filter: drop-shadow(0 0 18px rgba(255, 190, 100, .55)) drop-shadow(0 4px 0 rgba(60, 30, 10, .9)) !important; }
html.printing .cover .kicker, html.printing .cover .subtitle, html.printing .cover .rule, html.printing .cover .cv-tagline, html.printing .cover .cv-by { transition: none !important; opacity: 1 !important; transform: none !important; }
html.printing .cover .kicker { font-size: 11pt; letter-spacing: .25em; }
html.printing .cover .subtitle { font-size: 17pt; }
html.printing .cover .cv-tagline { font-size: 14pt; }
html.printing .cover > .cv-by { position: absolute; left: 0; right: 0; bottom: 18mm; z-index: 4; text-align: center; font-size: 12pt; margin: 0; }
html.printing .cover::after { content: ""; position: absolute; inset: 8mm; z-index: 3; border: 1px solid rgba(224, 168, 79, .6); background: none; pointer-events: none; }
html.printing .interlude.sheet { display: block; }
html.printing .interlude.sheet::before, html.printing .interlude.sheet::after { display: none !important; }
html.printing .il-stage { position: relative !important; height: 297mm !important; }
html.printing .il-img { opacity: 0 !important; transform: none !important; }
html.printing .il-img:nth-of-type(2) { opacity: 1 !important; filter: grayscale(.85) sepia(.15) brightness(.55) !important; }
html.printing .il-lines { display: flex; flex-direction: column; justify-content: center; gap: 9mm; padding: 0 22mm; }
html.printing .il-lines p { grid-area: auto; opacity: 1 !important; transform: none !important; filter: none !important; transition: none !important; font-size: 17pt; max-width: none; margin: 0 auto; }
html.printing .backcover { position: relative; overflow: hidden; color: #f3e8d2; }
html.printing .backcover.sheet::before { filter: blur(3px) brightness(.38) saturate(.9); }
html.printing .bc-in { position: relative; z-index: 2; width: 150mm; display: grid; gap: 7mm; justify-items: center; text-align: center; }
html.printing .bc-kicker { margin: 0; font: 700 10pt var(--font-ui); letter-spacing: .25em; color: #f8dca0; }
html.printing .bc-in h2 { margin: 0; font: 900 30pt var(--font-display); color: #f6d08a; text-shadow: 0 0 14px rgba(255, 190, 100, .5); }
html.printing .bc-blurb { margin: 0; display: grid; gap: 4mm; font: 500 13pt/1.6 var(--font-display); text-wrap: pretty; }
html.printing .bc-blurb p { margin: 0; }
html.printing .bc-for { margin: 0; font: 700 11pt var(--font-ui); letter-spacing: .08em; color: #f8dca0; }
html.printing .bc-qr { display: flex; align-items: center; gap: 6mm; margin-top: 4mm; padding: 4mm 6mm; background: rgba(10, 7, 4, .6); border: 1px solid rgba(224, 168, 79, .5); border-radius: 3mm; font: 500 10pt/1.5 var(--font-ui); text-align: start; }
html.printing .bc-qr img { width: 26mm; height: 26mm; border-radius: 1.5mm; }
html.printing .bc-qr b { display: block; direction: ltr; font-weight: 700; color: #f6d08a; }
html.printing .page .canvas { width: var(--pw) !important; flex: none; container-type: inline-size; z-index: 1; }
html.printing .page .pnum { position: absolute; z-index: 2; bottom: 6mm; left: 50%; transform: translateX(-50%); font: 600 11pt 'Frank Ruhl Libre', serif; color: #f3e3c2; text-shadow: 0 1px 4px #000; }
html.printing .cover.cine, html.printing .outro { background: none !important; }
html.printing .cover-inner, html.printing .outro-inner { opacity: 1 !important; transform: none !important; z-index: 2; }
html.printing .cover .cv-rays, html.printing .cover .cv-sun, html.printing .cover .cv-fig, html.printing .cover .cv-ground { z-index: 1; }
html.printing .cover .cv-rays { opacity: .55 !important; animation: none !important; }
html.printing .outro .outro-text { color: #fbeed0; text-shadow: 0 2px 12px #000; }
html.printing .outro .rule { background: #e0a84f; }
html.printing .pw { transform: none !important; }
html.printing .frame { opacity: 1 !important; transform: none !important; animation: none !important; }
html.printing .txt { opacity: 1 !important; transform: rotate(var(--rot, 0deg)) !important; transition: none !important; }
html.printing .art { animation: none !important; -webkit-mask-image: none !important; mask-image: none !important; clip-path: none !important; }
html.printing .art img { animation: none !important; opacity: 1 !important; transform: scaleX(var(--flip, 1)) scale(calc(1.05 * var(--zm, 1))) !important; }
html.printing .fl, html.printing .rays { display: none !important; }
`;
(async () => {
  fs.rmSync(outDir, { recursive: true, force: true }); fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: Math.round(210 * MM), height: Math.round(297 * MM) }, deviceScaleFactor: dpi / 96 });
  await p.goto('file://' + path.join(__dirname, '..', 'site', 'index.html') + '?print');
  await p.evaluate(() => document.fonts.ready);
  if (lang !== 'he') await p.evaluate(l => document.querySelector('[data-lang="' + l + '"]').click(), lang);
  await p.addStyleTag({ content: CSS });
  await p.evaluate(([MM, BACK, QR]) => {
    const root = document.documentElement;
    root.classList.add('printing'); root.classList.remove('loading');
    document.getElementById('loader').classList.add('done');
    const cover = document.getElementById('cover'), outro = document.getElementById('outro');
    cover.classList.add('go', 'sheet'); outro.classList.add('sheet');
    outro.style.setProperty('--bg', 'url("art/p22-a.webp")');
    cover.appendChild(cover.querySelector('.cv-by'));
    document.getElementById('interlude').classList.add('sheet');
    const bk = document.createElement('section'); bk.className = 'backcover sheet'; bk.style.setProperty('--bg', 'url("art/p16-a.webp")');
    const T = BACK, inner = document.createElement('div'); inner.className = 'bc-in';
    inner.innerHTML = '<p class="bc-kicker"></p><h2></h2><div class="bc-blurb"></div><p class="bc-for"></p><div class="bc-qr"><img alt=""><span><span class="o"></span><b>elazarsh.github.io/hagibor-hanamuch</b></span></div>';
    inner.querySelector('.bc-kicker').textContent = T.kicker; inner.querySelector('h2').textContent = T.title;
    T.blurb.forEach(t => { const q = document.createElement('p'); q.textContent = t; inner.querySelector('.bc-blurb').appendChild(q); });
    inner.querySelector('.bc-for').textContent = T.for; inner.querySelector('.o').textContent = T.online; inner.querySelector('img').src = QR;
    bk.appendChild(inner); outro.after(bk);
    document.querySelectorAll('.pw').forEach(pw => pw.classList.add('in'));
    document.querySelectorAll('.art img').forEach(i => { i.loading = 'eager'; i.style.setProperty('--py', '0px'); });
    document.querySelectorAll('.page').forEach((sec, n) => {
      sec.classList.add('sheet');
      sec.style.setProperty('--pw', (200 * MM) + 'px');
      let best = null, area = 0;
      sec.querySelectorAll('.pw').forEach(pw => { const im = pw.querySelector('.art img'); const a = pw.offsetWidth * pw.offsetHeight; if (im && a > area) { area = a; best = im; } });
      if (best) sec.style.setProperty('--bg', 'url("' + best.getAttribute('src') + '")');
      const num = document.createElement('span'); num.className = 'pnum'; num.textContent = String(n + 1); sec.appendChild(num);
    });
    window.dispatchEvent(new Event('resize'));
  }, [MM, BACK[lang] || BACK.he, QR]);
  await p.waitForFunction(() => [...document.querySelectorAll('.art img')].every(i => i.complete && i.naturalWidth), null, { timeout: 120000 });
  await p.waitForTimeout(1500);
  const sheets = await p.$$('.sheet');
  let k = 0;
  for (const s of sheets) {
    await s.scrollIntoViewIfNeeded();
    await p.waitForTimeout(150);
    await s.screenshot({ path: path.join(outDir, String(++k).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  }
  console.log('sheets', k, outDir);
  await b.close();
})();
