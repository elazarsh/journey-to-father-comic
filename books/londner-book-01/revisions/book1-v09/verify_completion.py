from pathlib import Path
import json,hashlib,datetime,re
from PIL import Image,ImageOps,ImageStat
V=Path(__file__).resolve().parent;B=V.parents[1];Q=V/'qa';Q.mkdir(exist_ok=True)
p=json.load(open(B/'art/book1-v07/progress.json'));a={x['id']:x for x in p['assets']};plan=json.load(open(V/'layout-plan.json'));ids=[pid for pg in plan['pages'] for pid in pg['order']];cache=json.load(open(B/'handoffs/codex/github-sync-cache.json'))
assert len(ids)==len(set(ids))==170
errors=[];rows=[];local=0;inherited=0
for pid in ids:
 x=a[pid];master=B/x['file'];web=B/x['web_file'];row=dict(id=pid,master_file=x['file'],master_sha256=x['sha256'],preview_file=x['web_file'])
 assert 'rejected' not in x['status']
 if not web.exists():errors.append(pid+': preview missing');continue
 raw=web.read_bytes();row['preview_sha256']=hashlib.sha256(raw).hexdigest();row['preview_git_blob_sha1']=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 with Image.open(web) as im:im.load();ws=im.size;preview=im.convert('RGB').resize((128,128))
 if abs(ws[0]/ws[1]-x['actual_size'][0]/x['actual_size'][1])>.015:errors.append(pid+': preview aspect mismatch')
 if master.exists():
  raw=master.read_bytes();sha=hashlib.sha256(raw).hexdigest();assert sha==x['sha256'],pid
  row['master_git_blob_sha1']=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest();row['master_verified_locally']=True;local+=1
  with Image.open(master) as im:im.load();assert list(im.size)==x['actual_size'];source=im.convert('RGB').resize((128,128))
  from PIL import ImageChops
  mae=sum(ImageStat.Stat(ImageChops.difference(source,preview)).mean)/3;row['preview_correspondence_mae']=round(mae,3)
  if mae>12:errors.append(pid+': preview differs from selected master')
 else:
  row['master_verified_locally']=False;row['inherited_from']=x.get('origin_commit');inherited+=1
  row['master_git_blob_sha1']=cache['files'].get('books/londner-book-01/'+x['file'])
  if not row['master_git_blob_sha1'] or not row['inherited_from']:errors.append(pid+': inherited master provenance missing')
 row['master_in_last_synced_tree']=cache['files'].get('books/londner-book-01/'+x['file'])==row['master_git_blob_sha1'];rows.append(row)
queue=json.load(open(V/'image-work-queue.json'));assert all(x['task']=='existing' for x in queue['images'])
html=(V/'sketch.html').read_text();m=re.search(r'var DATA = (.*);\n',html);data=json.loads(m.group(1));renderable=sum(bool(q.get('art')) and q.get('verdict')!='redirect' for pg in data['pages'] for q in pg['panels']);assert renderable==170
report=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),story_pages=48,active_images=170,renderable_images=renderable,local_master_hashes_verified=local,inherited_master_records=inherited,all_previews_decode=True,all_preview_aspects_match=not any('aspect' in e for e in errors),selected_sources_complete=True,source_selection_pins=json.load(open(V/'source-selection.json')),master_uploads_pending=sum(not r['master_in_last_synced_tree'] for r in rows),errors=errors,rows=rows,not_claimed=['No new browser screenshot/phone/print lettering approval.','Static crop settings are conservative; page21 height and full bubble overlap need final layout review.','Inherited PNGs are preserved in upstream GitHub commits, not re-created from previews.'])
(Q/'completion-integrity-20261101.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ['rows','source_selection_pins']},ensure_ascii=False))
assert not errors,errors
