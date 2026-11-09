"""Unlettered static phone crop contact sheets; no browser or typography assertion."""
import json,hashlib,io
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[3];Q=Path(__file__).resolve().parent
meta=json.loads((Q/'crop-proof-metadata.json').read_text())['panels'];assets={a['id']:a for a in json.loads((B/'art/book1-v07/progress.json').read_text())['assets']};rows=[]
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
active=[m for m in meta if m['has_source']]
for base in range(0,len(active),12):
 sheet=Image.new('RGB',(1440,1560),'#eee7da');d=ImageDraw.Draw(sheet)
 for j,m in enumerate(active[base:base+12]):
  pid=m['id'];a=assets[pid];p=B/a['file'];p=p if p.exists() else B/a['web_file'];data=p.read_bytes();im=Image.open(io.BytesIO(data)).convert('RGB');asp=m['phone_box_aspect'];W=340;H=round(W/asp);px,py=m['current_object_position'];z=1.03;s=max(W/im.width,H/im.height);ox=((W-im.width*s)*px/100-W/2)*z+W/2;oy=((H-im.height*s)*py/100-H/2)*z+H/2
  out=im.transform((W,H),Image.Transform.AFFINE,(1/(s*z),0,-ox/(s*z),0,1/(s*z),-oy/(s*z)),Image.Resampling.BICUBIC);mask=Image.new('L',(W,H),0);md=ImageDraw.Draw(mask);sh=m['shape']
  if sh.get('circle'):md.ellipse((0,0,W,H),fill=255)
  else:
   pts=[(100-x,y) for x,y in sh['poly']];x0=min(x for x,y in pts);y0=min(y for x,y in pts);bw=max(x for x,y in pts)-x0;bh=max(y for x,y in pts)-y0;md.polygon([((x-x0)/bw*W,(y-y0)/bh*H) for x,y in pts],fill=255)
  xx=(j%4)*360+10;yy=(j//4)*520+30;sheet.paste(out,(xx,yy),mask);d.text((xx,yy-25),pid,font=F,fill='black');rows.append(dict(id=pid,input=str(p.relative_to(B)),inputSHA256=hashlib.sha256(data).hexdigest(),phone_aspect=asp,object_position=[px,py]))
 sheet.save(Q/f'phone-crops-{base//12+1:02}.jpg',quality=89)
(Q/'phone-proof-metadata.json').write_text(json.dumps(dict(note='Static mask/image transformation at phone aspect clamp .72–1.45. Live text height, collisions, fonts, tails and actual 390px layout are not tested. Sources unchanged.',panels=rows),indent=2));print(len(rows),'phone crop proofs')
