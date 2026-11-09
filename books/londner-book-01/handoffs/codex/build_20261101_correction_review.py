"""A portable before/after sheet and explicit handoff map; does not alter the book."""
from pathlib import Path
import base64, hashlib, html, io, json, shutil
from PIL import Image
B = Path(__file__).resolve().parents[2]
D = B/'art/book1-v08-corrections'
OUT = Path('/workspace/londner-family-research/deliverables/book1-v08')
OUT.mkdir(parents=True, exist_ok=True)
assets = {a['id']:a for a in json.loads((B/'art/book1-v07/progress.json').read_text())['assets']}
receipts = [json.loads(p.read_text()) for p in sorted((D/'receipts').glob('*.json'))]

def embed(p, size=(800,650)):
    with Image.open(p) as im:
        im.load(); im.thumbnail(size)
        buf=io.BytesIO(); im.save(buf,'WEBP',quality=76,method=5)
    return 'data:image/webp;base64,'+base64.b64encode(buf.getvalue()).decode()

for r in receipts:
    p=B/r['file']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
    with Image.open(p) as im:
        im.load(); assert list(im.size)==r['actual_size']
    with Image.open(B/r['web_file']) as im: im.load()
replacements=[]
for r in receipts:
    if not r.get('target'):continue
    old=assets[r['target']]
    replacements.append(dict(target=r['target'],file=r['file'],web_file=r['web_file'],sha256=r['sha256'],actual_size=r['actual_size'],age_band=r.get('age_band'),previous_file=r.get('previous_source_file',old['file']),previous_sha256=r.get('previous_source_sha256',old['sha256']),receipt='art/book1-v08-corrections/receipts/'+r['id']+'.json',requires_new_face_and_crop_review=True))
memory=next(r for r in receipts if r['id']=='children-memory-v01')
with Image.open(B/memory['file']) as im:
    assert im.mode=='RGBA',im.mode
    alpha=im.getchannel('A');assert alpha.getextrema()[0]==0
    alpha_info=dict(mode=im.mode,alpha_range=list(alpha.getextrema()),suggested_live_opacity=0.55)
reference=D/'references/S08-img053.jpg';reference.parent.mkdir(exist_ok=True)
if not reference.exists(): shutil.copyfile('/workspace/londner-family-research/working/images/S08-img053.jpg',reference)
mapping=dict(status='ready-for-Claude-integration' if len(replacements)==32 else 'in-progress',book=1,story_art_unchanged_until_integration=True,replacement_count=len(replacements),new_character_references=3,extra_assets=2,replacements=replacements,opening_background='art/book1-v08-corrections/extras/opening-dedication-background-v01.png',memory=dict(file=memory['file'],**alpha_info,reference='art/book1-v08-corrections/references/S08-img053.jpg',source_caption='מימין מוטלה, מנחם, סבא יצחק, סבתא חוה וחיה.',viewer_left_to_right=['חיה','מנחם','מוטלה']),integration_notes='handoffs/codex/20261101-family-image-review.md',not_claimed=['Family approval of new likenesses','Final lettering/crop/browser/print approval','A regenerated book PDF'])
(D/'replacement-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
css='body{background:#f4eddf;color:#352d23;font:18px system-ui;max-width:1300px;margin:25px auto;padding:0 18px;line-height:1.6}h1{font-size:30px}h2{margin-top:38px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;direction:ltr}figure{margin:0;background:#fffaf1;padding:12px}figure img{width:100%;height:330px;object-fit:contain}figcaption{direction:rtl}code{display:inline-block;direction:ltr;unicode-bidi:isolate}.extras img{height:500px}.memory{background:#f5e4c7;border-radius:45%;padding:20px;max-width:700px;position:relative}.memory img{opacity:.55;width:100%;display:block}.opening-demo{position:relative;max-width:650px;margin:30px auto}.opening-demo>.scene{width:100%;display:block}.opening-demo .memory{position:absolute;top:2%;left:3%;width:40%;padding:2%;border-radius:45%}.memory:after{content:"";position:absolute;bottom:-15px;right:18%;width:16px;height:16px;border-radius:50%;background:#f5e4c7}.memory:before{content:"";position:absolute;bottom:-30px;right:15%;width:9px;height:9px;border-radius:50%;background:#f5e4c7}a{color:#266174}article{margin:28px 0;padding:15px;background:#eee3d1}small{display:block}@media(max-width:650px){.pair{grid-template-columns:1fr}figure img{height:auto;max-height:500px}}'
parts=['<!doctype html><html dir="rtl" lang="he"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>תיקוני האיורים של ספר 1</title><style>'+css+'</style><h1>ספר 1 · תיקוני גיל, פרופורציות ופתיחה</h1>',f'<p>{len(replacements)} איורים חלופיים · שלושה רפרנסים חדשים לגיל · רקע הקדמה וזיכרון הילדים. זהו גיליון השוואה לעיון, לפני שילוב בספר בידי קלוד.</p>', '<h2>ארבע תחנות בגיל</h2><div class="grid">']
for label,p in [('ילדות מוקדמת, כארבע','art/book1-v08-corrections/characters/yitzhak-age04-v01.png'),('ילדות מאוחרת, הרפרנס המאושר','art/chars/yitzhak-child-v02.png'),('תחילת הנעורים, כ־13–14','art/book1-v08-corrections/characters/yitzhak-age14-v01.png'),('נעורים מאוחרים, סביב 17','art/book1-v08-corrections/characters/yitzhak-age17-v01.png')]:
    parts.append('<figure><img src="'+embed(B/p)+'"><figcaption>'+label+'</figcaption></figure>')
parts+=['</div><p>הדיוקנאות החדשים הם שחזור אמנותי לעיונכם. טווחי הגיל אינם קביעה מחדש של תאריכי הסיפור.</p><h2>רקע מואר לעמוד ההקדמה</h2><div class="extras"><figure><img src="'+embed(D/'extras/opening-dedication-background-v01.png',(900,1350))+'"><figcaption>רקע המיועד לטקסט החי של ההקדמה, ללא טקסט צרוב.</figcaption></figure></div><h2>חיה, מנחם ומוטלה כזיכרון</h2><p>הדגמת שקיפות בתוך בועת מחשבה בגוון קרם. המיקום בתוך עמוד הקומיקס ייקבע בעימוד של קלוד.</p><label>עוצמת הזיכרון: <input id="opacity" type="range" min="35" max="85" value="55"><output id="amount">55%</output></label><div class="memory"><img id="memory" src="'+embed(B/memory['file'],(1000,700))+'"></div><p>משמאל לצופה: חיה, מנחם ומוטלה. הציור מבוסס על התצלום המשפחתי עם הכיתוב המזהה.</p>']
parts.append('<h2>הדגמת הזיכרון מעל סבא הכותב</h2><p>דוגמת שילוב בלבד; הטקסט והמסגרת הסופית יותאמו בידי קלוד.</p><div class="opening-demo"><img class="scene" src="'+embed(B/assets['B01V07-P01-01']['web_file'],(800,1200))+'"><div class="memory"><img src="'+embed(B/memory['file'],(750,600))+'"></div></div>')
for r in sorted(replacements,key=lambda x:x['target']):
    before=assets[r['target']]['web_file']
    parts.append('<article><h2><code>'+html.escape(r['target'])+'</code></h2><div class="pair"><figure><img loading="lazy" src="'+embed(B/before)+'"><figcaption>לפני</figcaption></figure><figure><img loading="lazy" src="'+embed(B/r['web_file'])+'"><figcaption>אחרי</figcaption></figure></div></article>')
parts.append('<script>document.getElementById("opacity").addEventListener("input",function(){document.querySelectorAll(".memory img").forEach(im=>im.style.opacity=this.value/100);document.getElementById("amount").value=this.value+"%";});</script></html>')
doc='\n'.join(parts);(D/'review.html').write_text(doc);(OUT/'book1-corrections-review.html').write_text(doc)
(D/'verification.json').write_text(json.dumps(dict(verified_masters=len(receipts),verified_previews=len(receipts),all_png_hashes_match=True,memory_alpha=alpha_info,scene_replacements=len(replacements),final_layout_qa=False),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(new_assets=len(receipts),scene_replacements=len(replacements),memory_alpha=alpha_info,review_html_bytes=len(doc.encode())),ensure_ascii=False))
