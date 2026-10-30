from pathlib import Path
import json,hashlib,base64,datetime,shutil
from PIL import Image
V=Path(__file__).resolve().parent;B=V.parents[1];A=B/'art/book1-v07'
book=json.loads((V/'book1-script.json').read_text());manifest=json.loads((V/'production/manifest.json').read_text())
receipts={};images={};assets=[];needs=[]
for p in sorted((A/'receipts').glob('*.json')):
 try:r=json.loads(p.read_text())
 except (ValueError,OSError):continue
 pid=r.get('id',p.stem);master=B/r.get('file',f'art/book1-v07/{pid}.png')
 if not master.exists():continue
 raw=master.read_bytes();sha=hashlib.sha256(raw).hexdigest()
 if r.get('sha256')!=sha:continue
 # Normalize a web copy only; leave all source pixels untouched.
 web=A/'web'/f'{pid}.webp';web.parent.mkdir(exist_ok=True)
 normalized=A/'web'/f'{pid}.source-sha256.txt'
 if not web.exists() or not normalized.exists() or normalized.read_text()!=sha:
  with Image.open(master) as im:im.save(web,'WEBP',quality=90,method=5)
  normalized.write_text(sha)
 with Image.open(master) as im:size=list(im.size)
 rel=str(web.relative_to(B));status=r.get('status','generated-source-reviewed')
 assets.append(dict(id=pid,file=str(master.relative_to(B)),web_file=rel,actual_size=size,sha256=sha,status=status,receipt=str(p.relative_to(B))))
 receipts[pid]=r
 # Preview uses contained masters until masks/lettering get actual visual approval.
 images[pid]=dict(src='../../'+rel,fit='contain',status=status)
 if 'needed' in status or 'adjust' in status:needs.append(pid)
for p in book['pages']:
 for q in p['panels']:
  if q['id'] in images:q['art']=images[q['id']];q['visual_status']=images[q['id']]['status']
for m in manifest['images']:
 a=next((a for a in assets if a['id']==m['id']),None)
 if a:m.update({k:a[k] for k in ['status','actual_size','sha256','web_file','receipt']})
(V/'book1-script.json').write_text(json.dumps(book,ensure_ascii=False,indent=2))
(V/'production/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
progress=dict(version='0.7',assets=assets,generated=len(assets),planned=len(manifest['images']),remaining=len(manifest['images'])-len(assets),crop_adjustment_flags=needs,status='Source images in production. Fit contain previews; final crop and bubble overlap review pending.',last_refreshed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(A/'progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2));(A/'generation-receipts.json').write_text(json.dumps(list(receipts.values()),ensure_ascii=False,indent=2))
report=json.loads((V/'qa-report.json').read_text());report['generated_assets']=len(assets);report['not_claimed']=[s for s in report['not_claimed'] if not s.startswith('No new illustrations') and not s.startswith('No GitHub publication')];report['not_claimed']+=['Source artwork is not final face-crop, balloon-overlap or browser visual approval.'];report['not_claimed']=list(dict.fromkeys(report['not_claimed']));(V/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
elder=B/'art/web/draft-p01-1.webp';img='data:image/webp;base64,'+base64.b64encode(elder.read_bytes()).decode()
payload=json.dumps(dict(book=book,series=json.loads((V/'series-plan.json').read_text())['requested_volumes'],report=report,elder=img,family=json.loads((V/'family-continuity.json').read_text())['evidence'],images=images),ensure_ascii=False).replace('</','<\\/')
tpl=(V/'template.html').read_text()
for name,mode in [('index.html','overview'),('book1-reader.html','reader')]: (V/name).write_text(tpl.replace('__MODE__',mode).replace('__DATA__',payload))
statepath=B/'handoffs/codex/state.json';state=json.loads(statepath.read_text());state.update(status='Parallel image generation and book-2 script writing in progress',generated_images=len(assets),remaining_images=progress['remaining'],art_progress='art/book1-v07/progress.json');statepath.write_text(json.dumps(state,ensure_ascii=False,indent=2))
print(json.dumps(dict(generated=len(assets),remaining=progress['remaining'],crop_flags=needs)))
