"""Merge inherited Claude assets and new local sources without redrawing or losing originals."""
from pathlib import Path
import json,hashlib,datetime
from PIL import Image
V=Path(__file__).resolve().parent;B=V.parents[1];A=B/'art/book1-v07'
plan=json.load(open(V/'layout-plan.json'));active={i for p in plan['pages'] for i in p['order']}
assets={a['id']:dict(a) for a in json.load(open(A/'remote-inherited-assets-v08.json'))}
pins=json.load(open(V/'source-selection.json')) if (V/'source-selection.json').exists() else {}
for rp in sorted((A/'receipts').glob('*.json')):
 try:r=json.load(open(rp))
 except (OSError,ValueError):continue
 pid=r.get('id');rel=r.get('file')
 if not pid:continue
 if pid in pins and r.get('sha256',r.get('accepted_sha256'))!=pins[pid]['sha256']:continue
 acceptance_sha=r.get('accepted_sha256',r.get('source_sha256',r.get('sha256')))
 accepted_v08=(r.get('layout_version')=='0.8' or r.get('claude_v08_review_complete'))
 if pid in assets and accepted_v08 and acceptance_sha==assets[pid].get('sha256'):
  assets[pid]['reviewed_layout_version']='0.8';assets[pid]['claude_v08_review_complete']=True
 if not rel:continue
 src=B/rel
 if not src.exists():continue
 raw=src.read_bytes();sha=hashlib.sha256(raw).hexdigest()
 if sha!=r.get('sha256'):continue
 if 'rejected' in r.get('status',''):continue
 web=A/'web'/f'{pid}.webp';tag=web.with_suffix('.source-sha256.txt');web.parent.mkdir(exist_ok=True)
 if not web.exists() or not tag.exists() or tag.read_text()!=sha:
  with Image.open(src) as im:im.save(web,'WEBP',quality=90,method=5)
  tag.write_text(sha)
 with Image.open(src) as im:size=list(im.size)
 prior=assets.get(pid,{})
 a=dict(id=pid,file=rel,web_file=str(web.relative_to(B)),actual_size=size,sha256=sha,status=r.get('status','generated-source-reviewed'),receipt=str(rp.relative_to(B)),master_available_locally=True)
 if prior.get('sha256')==sha:
  for k in ['claude_v08_review','origin_commit']:a[k]=prior.get(k)
 if r.get('layout_version')=='0.8' or r.get('claude_v08_review_complete'):
  a['reviewed_layout_version']='0.8';a['claude_v08_review_complete']=True
 if r.get('fixed_by_review'):a['fixed_by_review']=r['fixed_by_review']
 if prior.get('sha256')==sha and prior.get('status')=='source-present-needs-claude-fix' and not a.get('fixed_by_review'):a['status']=prior['status']
 assets[pid]=a
for pid,a in assets.items():a['in_active_layout']=pid in active
made=sum(pid in assets for pid in active);fixes=[i for i,a in assets.items() if i in active and a['status']=='source-present-needs-claude-fix']
progress=dict(version='0.8',assets=list(assets.values()),generated=made,generated_active=made,source_images_archived_or_inactive=sum(i not in active for i in assets),planned=len(active),remaining=len(active)-made,fixes_pending=fixes,status='Sources present are distinct from final crop/balloon approval. Full inherited PNG masters are preserved at Claude commit; previews use verified local WebP copies.',last_refreshed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(A/'progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2))
queue=json.load(open(V/'image-work-queue.json'));script=json.load(open(B/'revisions/book1-v07/book1-script.json'));old={q['id']:q for p in script['pages'] for q in p['panels']}
for q in queue['images']:
 a=assets.get(q['id']);q['existing']=a
 if not q.get('shows'):q['shows']=old.get(q['id'],{}).get('action','')
 fixed=bool(a and (a.get('fixed_by_review') or a.get('claude_v08_review_complete')))
 passed=bool(a and a.get('claude_v08_review',{} ) and a['claude_v08_review'].get('verdict')=='pass')
 q['task']='fix' if q.get('review_fix') and not fixed else 'generate' if a is None else 'review_redirect' if q.get('purpose',{}).get('verdict')=='redirect' and not (fixed or passed) else 'review_existing' if a is not None and not (fixed or passed) else 'existing'
(V/'image-work-queue.json').write_text(json.dumps(queue,ensure_ascii=False,indent=2))
statep=B/'handoffs/codex/state.json';state=json.load(open(statep));state.update(active_revision='revisions/book1-v08',active_layout='revisions/book1-v08/layout-plan.json',active_manifest='revisions/book1-v08/image-work-queue.json',generated_images=made,remaining_images=len(active)-made,panels_planned=len(active),source_parent='4b7f81fb6a1c052602e2c8e13460e7171eb6b0c2',status='Continuing Claude v08 instructions; preserve fidelity edits and removed panel list.')
statep.write_text(json.dumps(state,ensure_ascii=False,indent=2))
print(json.dumps(dict(active_images=len(active),sources_present=made,missing=len(active)-made,fixes_pending=len(fixes),redirect_reviews=sum(q['task']=='review_redirect' for q in queue['images']),existing_reviews=sum(q['task']=='review_existing' for q in queue['images']))))
