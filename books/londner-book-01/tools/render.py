from pathlib import Path
import json,base64,shutil,hashlib,zipfile
from PIL import Image
B=Path(__file__).resolve().parents[1];R=B
D=B/'exports';D.mkdir(parents=True,exist_ok=True)
book=json.loads((B/'production/book.json').read_text());m=json.loads((B/'production/manifest.json').read_text());assets=m['images']
files={};embedded={}
def webp(src,dest):
 p=B/src;out=B/dest;out.parent.mkdir(parents=True,exist_ok=True)
 with Image.open(p) as im:
  im.convert('RGB').save(out,'WEBP',quality=93,method=6)
 files[src]='../'+dest
 embedded[src]='data:image/webp;base64,'+base64.b64encode(out.read_bytes()).decode()
for a in assets:
 if (B/a['file']).exists():webp(a['file'],a['web_file']);files[a['web_file']]=files[a['file']];embedded[a['web_file']]=embedded[a['file']]
 if a.get('existing_draft'):webp(a['existing_draft'],f'art/web/draft-{a["id"]}.webp')
webp('art/chars/yitzhak-child-v02.png','art/web/child-reference.webp')
tpl=(B/'tools/template.html').read_text()
def make(mode,inline=False):
 d=embedded if inline else files
 out=tpl.replace('__DEFAULT_MODE__',mode).replace('__BOOK_DATA__',json.dumps(book,ensure_ascii=False).replace('</','<\\/')).replace('__ASSET_DATA__',json.dumps(assets,ensure_ascii=False).replace('</','<\\/')).replace('__FILES_DATA__',json.dumps(d,ensure_ascii=False)).replace('__CHAR_DATA__',json.dumps(d['art/chars/yitzhak-child-v02.png']))
 return out
(B/'production/structure.html').write_text(make('plan'))
(B/'viewer/index.html').write_text(make('reader'))
(D/'book-production-map.html').write_text(make('plan',True))
(D/'book-reader-preview.html').write_text(make('reader',True))
progress=[{'id':a['id'],'file':a['file'],'web_file':a['web_file'],'status':a['status'],'actual_size':a.get('actual_size'),'geometry_sha256':a['geometry_sha256'],'sha256':a.get('sha256'),'crop_qa':a['crop_qa']} for a in assets if a['status'].startswith('generated')]
(B/'art/progress.json').write_text(json.dumps(progress,ensure_ascii=False,indent=2))
(B/'handoffs/codex/state.json').write_text(json.dumps({'stage':'layout-led production','book':'Yitzhak Meir Londner, Book 1','layout':'production/structure.html','reader':'viewer/index.html','manifest':'production/manifest.json','generated_current_batch':[x['id'] for x in progress],'current_batch_target':['p02-1','p03-1','p03-2','p03-3','p04-1','p04-2','p04-3'],'status':'production candidates, not final approved art','unresolved':'Historical review and identity details remain marked per panel; do not treat existence of an image as factual/family approval.'},ensure_ascii=False,indent=2))
print(json.dumps({'blueprint':str(D/'book-production-map.html'),'reader_preview':str(D/'book-reader-preview.html'),'produced':[x['id'] for x in progress],'embedded_assets':len(embedded),'html_bytes':(D/'book-production-map.html').stat().st_size},ensure_ascii=False))
