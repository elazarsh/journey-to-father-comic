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
const CSS = `
html.printing, html.printing body { background: #0d0907 !important; overflow: visible !important; }
html.printing { --rim: #1b1410; }
html.printing #atmos, html.printing .topbar, html.printing .hud, html.printing .rail, html.printing #loader, html.printing #studio, html.printing .cue, html.printing #startBtn, html.printing #restart, html.printing .cv-letter { display: none !important; }
html.printing .sheet { width: 210mm !important; height: 297mm !important; min-height: 0 !important; margin: 0 !important; padding: 0 !important; position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; }
html.printing .sheet::before { content: ""; position: absolute; inset: -8mm; z-index: 0; background: var(--bg) center / cover no-repeat; filter: blur(14px) brightness(.5) saturate(.95); }
html.printing .cover.cine::before { display: block !important; animation: none !important; transform: none !important; }
html.printing .sheet::after { content: ""; position: absolute; inset: 0; z-index: 0; background: radial-gradient(ellipse at 50% 50%, transparent 40%, rgba(0, 0, 0, .45) 100%); pointer-events: none; }
html.printing .page { counter-increment: pg; }
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
  await p.evaluate((MM) => {
    const root = document.documentElement;
    root.classList.add('printing'); root.classList.remove('loading');
    document.getElementById('loader').classList.add('done');
    const cover = document.getElementById('cover'), outro = document.getElementById('outro');
    cover.classList.add('go', 'sheet'); outro.classList.add('sheet');
    cover.style.setProperty('--bg', 'url("art/p16-a.webp")'); outro.style.setProperty('--bg', 'url("art/p22-a.webp")');
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
  }, MM);
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
