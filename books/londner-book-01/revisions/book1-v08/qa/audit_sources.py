"""Read-only source/receipt audit. Writes only QA evidence in this directory."""
import hashlib,json,sys
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
from PIL import Image
B=Path(__file__).resolve().parents[3]; Q=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((B/'revisions/book1-v08/layout-plan.json').read_text()); progress=json.loads((B/'art/book1-v07/progress.json').read_text()); faces=json.loads((B/'revisions/book1-v08/faces.json').read_text())
active={pid:pg['page'] for pg in plan['pages'] for pid in pg['order']}
rows=[]
for a in progress['assets']:
 pid=a['id']; src=B/a['file'];web=B/a['web_file'];receipt=B/a.get('receipt',f'art/book1-v07/receipts/{pid}.json')
 r=json.loads(receipt.read_text()) if receipt.exists() else {}; issues=[]
 local=src.exists(); h=sha(src) if local else None;wh=sha(web) if web.exists() else None
 if local and h!=a.get('sha256'):issues.append('master_vs_progress_hash')
 if local and r.get('sha256') and h!=r['sha256']:issues.append('master_vs_receipt_hash')
 if r.get('sha256') and a.get('sha256')!=r['sha256']:issues.append('progress_vs_receipt_hash')
 if local:
  im=Image.open(src); size=list(im.size); im.verify()
  if size!=a.get('actual_size'):issues.append('master_size_vs_progress')
 else:size=None
 if not web.exists():issues.append('web_missing')
 else:
  im=Image.open(web); wsize=list(im.size);im.verify()
  if size and abs(wsize[0]/wsize[1]-size[0]/size[1])>.003:issues.append('preview_aspect_vs_master')
 review=r.get('v08_source_review',{}); review=review if isinstance(review,dict) else {}
 if review.get('source_web_sha256') and wh!=review['source_web_sha256']:issues.append('web_changed_since_v08_source_review')
 if bool(a.get('master_available_locally',local))!=local:issues.append('master_local_flag_mismatch')
 rows.append(dict(id=pid,page=active.get(pid),active=pid in active,local_master=local,master_sha256=h,recorded_master_sha256=a.get('sha256'),web_file=a['web_file'],web_sha256=wh,source_size=size or a.get('actual_size'),status=a['status'],receipt_exists=receipt.exists(),receipt_sha256=r.get('sha256'),source_review_bound_to_current_preview=bool(review.get('source_web_sha256')) and wh==review.get('source_web_sha256'),face_boxes_unbound=faces.get(pid),face_provenance='UNBOUND: faces.json contains no sourceSHA/model/time; coordinates are candidates, not confirmed protection',issues=issues))
missing=[dict(id=pid,page=pg) for pid,pg in active.items() if pid not in {a['id'] for a in progress['assets']}]
out=dict(created_utc=datetime.now(timezone.utc).isoformat(),scope='Source and receipt integrity only; no browser, mask, lettering, identity or face-detection approval',active_panel_count=len(active),pages=len(plan['pages']),assets=len(rows),active_assets=sum(r['active'] for r in rows),active_local_masters=sum(r['active'] and r['local_master'] for r in rows),active_remote_masters_with_local_preview=sum(r['active'] and not r['local_master'] and bool(r['web_sha256']) for r in rows),missing=missing,issue_counts=dict(Counter(i for r in rows for i in r['issues'])),rows=rows)
(Q/'source-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='rows'},ensure_ascii=False,indent=2))
