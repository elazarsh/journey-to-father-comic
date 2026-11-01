#!/usr/bin/env python3
"""Register a native image generation as a candidate; never overwrite old art."""
import datetime, hashlib, json, shutil, sys
from pathlib import Path
from PIL import Image
B=Path(__file__).resolve().parents[2]
D=B/'art/book1-v08-corrections'
target, source, note = sys.argv[1:4]
ident=target+'-family-proof-v01'
dest=D/'panels'/(ident+'.png')
if dest.exists(): raise SystemExit(f'Already exists: {dest}')
shutil.copyfile(source,dest)
with Image.open(dest) as im:
    im.load(); size=list(im.size); mode=im.mode
    web=dest.with_suffix('.webp'); im.save(web,'WEBP',quality=88,method=5)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=D/'receipts'/(ident+'.json')
entry={'target':target,'file':str(dest.relative_to(B)),'web_file':str(web.relative_to(B)),'sha256':sha(dest),'web_sha256':sha(web),'actual_size':size,'mode':mode,'generation_tool':'image_gen.imagegen','status':'candidate-for-Claude-integration','family_approved':False,'requires_new_face_and_crop_review':True,'qa_notes':note,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
receipt.write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
entry['receipt']=str(receipt.relative_to(B))
mp=D/'replacement-map.json'; m=json.loads(mp.read_text(encoding='utf-8'))
if any(x.get('target')==target for x in m['replacements']):
    for x in m['replacements']:
        if x.get('target')==target:
            m.setdefault('previous_replacement_entries',[]).append(x.copy())
            x.clear();x.update(entry);break
else:m['replacements'].append(entry)
m['replacement_count']=len(m['replacements'])
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(target,entry['file'],entry['sha256'])
