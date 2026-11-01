"""Build a private, portable visual inventory, independent of the comic/PDF renderer."""
from pathlib import Path
import base64
import csv
import hashlib
import html
import io
import json
import zipfile
from PIL import Image

B = Path(__file__).resolve().parents[2]
V = B / 'revisions/book1-v08'
OUT = V / 'qa'
OUT.mkdir(exist_ok=True)
DELIVERY = Path('/workspace/londner-family-research/deliverables/book1-v08')
DELIVERY.mkdir(parents=True, exist_ok=True)
plan = json.loads((V / 'layout-plan.json').read_text())
assets = {x['id']: x for x in json.loads((B / 'art/book1-v07/progress.json').read_text())['assets']}
checks = {x['id']: x for x in json.loads((OUT / 'completion-integrity-20261101.json').read_text())['rows']}
fixes = {'B01V07-' + x for x in ['P05-03','P05-04','P06-02','P06-03','P07-01','P07-02']}
base = 'https://github.com/elazarsh/journey-to-father-comic/blob/claude/londner-script-review/books/londner-book-01/'

def thumb(path):
    with Image.open(path) as im:
        im = im.convert('RGB')
        im.thumbnail((620, 460))
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=68, method=5)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()

rows = []
parts = ['<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>ספר 1 · מפתח כל האיורים</title>',
         '<style>body{font:18px system-ui;background:#f3eee5;color:#2a251e;margin:24px auto;max-width:1400px;padding:0 18px}header{position:sticky;top:0;background:#f3eee5ee;padding:10px;z-index:1}h1{font-size:28px}section{margin:35px 0;break-inside:avoid}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}figure{margin:0;background:white;padding:12px;box-shadow:0 2px 6px #0002}img{width:100%;height:250px;object-fit:contain}figcaption{font-size:15px}code{direction:ltr;unicode-bidi:isolate;display:inline-block}a{color:#165d76}.fix{border:3px solid #628a59}.cover img{height:500px}nav a{display:inline-block;margin:5px}p{max-width:1000px;line-height:1.6}</style>',
         '<header><h1>ספר 1: מפתח חזותי של כל האיורים</h1><b>48 עמודי סיפור · 170 איורים נבחרים · עטיפה ייעודית נוספת</b></header>',
         '<p>זהו גיליון הפקה עם ספוילרים, המציג כל קובץ בנפרד ללא מסכות או בועות. הוא אינו PDF מעודכן או אישור עימוד. קישורי המקור מפנים לענף העבודה המשותף בגיטהאב. שש התמונות שתוקנו מסומנות במסגרת ירוקה. העטיפה החדשה ממתינה לעיון המשפחה.</p>',
         '<nav>' + ' '.join(f'<a href="#page-{p["page"]}">{p["page"]}</a>' for p in plan['pages']) + '</nav>',
         '<section class="cover"><h2>איור עטיפה ייעודי</h2><figure><img src="' + thumb(B/'art/book1-v08-cover/cover-v01.webp') + '"><figcaption><a href="'+base+'art/book1-v08-cover/cover-v01.png">מקור העטיפה</a> · ללא טקסט צרוב · ללא הגדלה בחיתוך A4</figcaption></figure></section>']
for pg in plan['pages']:
    parts.append(f'<section id="page-{pg["page"]}"><h2>עמוד {pg["page"]} · {len(pg["order"])} איורים</h2><div class="grid">')
    for slot, pid in enumerate(pg['order'], 1):
        a = assets[pid]
        web = B/a['web_file']
        with Image.open(web) as im:
            im.load()
        c = checks[pid]
        assert a['sha256'] == c['master_sha256']
        assert hashlib.sha256(web.read_bytes()).hexdigest() == c['preview_sha256']
        row = dict(page=pg['page'], slot=slot, id=pid, master_file=a['file'], preview_file=a['web_file'], source_sha256=a['sha256'], master_git_blob_sha1=c['master_git_blob_sha1'], fixed_review=pid in fixes, source_url=base+a['file'])
        rows.append(row)
        label = ' · תוקן לפי הסקירה' if pid in fixes else ''
        parts.append('<figure class="'+('fix' if pid in fixes else '')+'"><a href="'+row['source_url']+'"><img loading="lazy" src="'+thumb(web)+'" alt="'+pid+'"></a><figcaption><code>'+pid+'</code>'+label+'<br><a href="'+row['source_url']+'">קובץ המקור</a></figcaption></figure>')
    parts.append('</div></section>')
parts.append('</html>')
assert len(rows) == len({r['id'] for r in rows}) == len({r['source_sha256'] for r in rows}) == 170
assert sum(r['fixed_review'] for r in rows) == 6
doc = '\n'.join(parts)
(OUT/'art-inventory.html').write_text(doc)
(DELIVERY/'book1-art-inventory.html').write_text(doc)
(OUT/'art-inventory.json').write_text(json.dumps(dict(branch='claude/londner-script-review',story_pages=48,story_images=170,cover_additional=True,rows=rows),ensure_ascii=False,indent=2))
csvpath = OUT/'art-inventory.csv'
with csvpath.open('w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
with zipfile.ZipFile(DELIVERY/'book1-art-review.zip','w',zipfile.ZIP_DEFLATED) as z:
    z.writestr('index.html',doc)
    z.write(csvpath, 'art-inventory.csv')
    z.write(OUT/'art-inventory.json','art-inventory.json')
print(json.dumps(dict(story_images=len(rows),review_fixes=sum(r['fixed_review'] for r in rows),portable_html_bytes=len(doc.encode()),review_zip_bytes=(DELIVERY/'book1-art-review.zip').stat().st_size)))
