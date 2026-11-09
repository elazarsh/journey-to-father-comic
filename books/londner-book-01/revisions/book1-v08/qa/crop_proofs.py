"""Static QA artifacts using generated sources only. No lettering and no browser claim."""
import sys,json,hashlib,io
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[3]; V=B/'revisions/book1-v08';Q=V/'qa';sys.path.insert(0,str(V));import geometry
plan=json.loads((V/'layout-plan.json').read_text());assets={a['id']:a for a in json.loads((B/'art/book1-v07/progress.json').read_text())['assets']};faces=json.loads((V/'faces.json').read_text())
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
FB=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20)
meta=[]
source_cache={}
source_hashes={}
def bbox(poly):
 x,y,w,h=geometry.bbox(poly);return x,y,w,h
def params(pid):
 fc=[f for f in faces.get(pid,[]) if f[2]>=2.5]
 if fc:return sum(f[0]+f[2]/2 for f in fc)/len(fc),max(0,min(100,sum(f[1]+f[3]/2 for f in fc)/len(fc)-6))
 return 50,32
def art(pid):
 if pid in source_cache:return source_cache[pid].copy()
 a=assets.get(pid)
 if not a:return None
 p=B/a['file'];p=p if p.exists() else B/a['web_file']
 if not p.exists():return None
 data=p.read_bytes();im=Image.open(io.BytesIO(data)).convert('RGB');source_cache[pid]=im;source_hashes[pid]=dict(path=str(p.relative_to(B)),sha256=hashlib.sha256(data).hexdigest());return im.copy()
def render_crop(pid,w,h,fx=None,fy=None,zoom=1.03):
 im=art(pid)
 if im is None:return Image.new('RGB',(w,h),'#3e382f')
 iw,ih=im.size;s=max(w/iw,h/ih);dw,dh=iw*s,ih*s
 px,py=params(pid);px=px if fx is None else fx;py=py if fy is None else fy
 # Browser object-fit cover at object-position, followed by CSS transform scale around center.
 ox=((w-dw)*px/100-w/2)*zoom+w/2;oy=((h-dh)*py/100-h/2)*zoom+h/2
 return im.transform((w,h),Image.Transform.AFFINE,(1/(s*zoom),0,-ox/(s*zoom),0,1/(s*zoom),-oy/(s*zoom)),Image.Resampling.BICUBIC)
for pg in plan['pages']:
 order=pg['order'];hero=order.index(pg['hero']) if pg.get('hero') in order else None;inset=order.index(pg['inset']) if pg.get('inset') in order else None;morph=[(order.index(a),order.index(b)) for a,b in pg.get('morph',[]) if a in order and b in order];roomy=[i for i,pid in enumerate(order) if any(t.get('type') in ['speech','thought','whisper','shout'] for t in pg['texts'].get(pid,[]))]
 shapes=geometry.page_shapes(pg['recipe'],len(order),hero,morph,inset,roomy)
 page=Image.new('RGB',(700,1045),'#19120d');d=ImageDraw.Draw(page);d.text((12,6),f'PAGE {pg["page"]:02}  |  static crop proof, no live lettering',font=F,fill='white');scale=6.7
 for i in sorted(range(len(order)),key=lambda i: 2 if shapes[i].get('circle') else 1 if shapes[i].get('fade') else 0):
  pid=order[i]
  sh=shapes[i];poly=sh.get('poly');circle=sh.get('circle')
  if circle:x,y,w,h=circle;x=100-x-w;pts=None
  else:
   pts=[(100-x,y) for x,y in poly];x,y,w,h=bbox(pts)
  W,H=round(w*scale),round(h*scale*1.037);crop=render_crop(pid,W,H);mask=Image.new('L',(W,H),0);md=ImageDraw.Draw(mask)
  if circle:md.ellipse((0,0,W-1,H-1),fill=255)
  else:md.polygon([((xx-x)*scale,(yy-y)*scale*1.037) for xx,yy in pts],fill=255)
  page.paste(crop,(round(x*scale+15),round(y*scale*1.037+40)),mask)
  d.text((round(x*scale+20),round(y*scale*1.037+43)),pid.replace('B01V07-',''),font=F,fill='#fff69e',stroke_width=2,stroke_fill='#000')
  a=assets.get(pid);meta.append(dict(id=pid,page=pg['page'],sourceSHA=a.get('sha256') if a else None,has_source=bool(a),preview_used=bool(a and not (B/a['file']).exists()),proof_input=source_hashes.get(pid),shape=sh,current_object_position=params(pid),desktop_box_aspect=w/(h*1.037),phone_box_aspect=max(.72,min(1.45,w/h)),face_coordinates_unbound=faces.get(pid)))
 page.save(Q/f'page-{pg["page"]:02}-static.png')
# 12 sources per sheet, true source aspect preserved; crop proof sits immediately below each.
active=[(pg['page'],pid) for pg in plan['pages'] for pid in pg['order'] if pid in assets]
for n in range(0,len(active),12):
 chunk=active[n:n+12];sheet=Image.new('RGB',(1440,1290),'#ede6d8');d=ImageDraw.Draw(sheet)
 for j,(pn,pid) in enumerate(chunk):
  xx=(j%4)*360;yy=(j//4)*430;im=art(pid);im.thumbnail((350,290));sheet.paste(im,(xx+(360-im.width)//2,yy+30))
  d.text((xx+8,yy+5),f'{pn:02} {pid}',font=F,fill='black')
  inf=next(m for m in meta if m['id']==pid);asp=inf['desktop_box_aspect'];W,H=(330,max(20,round(330/asp))) if asp>3 else (max(20,round(90*asp)),90)
  cr=render_crop(pid,W,H);cr.thumbnail((340,95));sheet.paste(cr,(xx+(360-cr.width)//2,yy+325));d.text((xx+6,yy+410),'desktop crop; letters omitted',font=F,fill='black')
 sheet.save(Q/f'sources-{n//12+1:02}.jpg',quality=90)
(Q/'crop-proof-metadata.json').write_text(json.dumps(dict(note='Faithful static reproduction of CSS object-fit/object-position +1.03 transform and v08 polygon bounding boxes. Desktop 1.037 page-height CSS factor included. No fade gradients, shadows, lettering, browser metrics or pass. Current faces.json centroids applied but provenance unbound. Source pixels remain untouched.',panels=meta),indent=2))
print(len(active),'source thumbnails; 48 static page crop proofs')
