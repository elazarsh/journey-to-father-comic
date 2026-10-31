"""Technical layout proofs only: original masters unchanged; no retouching or new art."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,math
V=Path(__file__).resolve().parent;B=V.parents[1];Q=V/'qa';Q.mkdir(exist_ok=True)
book=json.loads((V/'book1-script.json').read_text());scale=12
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(fontpath,23);small=ImageFont.truetype(fontpath,15)
def lines(s,w):
 out=[];row=''
 for word in s.split():
  t=(row+' '+word).strip()
  if row and font.getlength(t,direction='rtl')>w:out.append(row);row=word
  else:row=t
 if row:out.append(row)
 return out
made=[]
for p in book['pages']:
 present=[(B/'art/book1-v07'/f"{q['id']}.png").exists() for q in p['panels']]
 if not all(present):continue
 canvas=Image.new('RGB',(100*scale,140*scale),'#fffaf0');draw=ImageDraw.Draw(canvas)
 for q in p['panels']:
  g=q['geometry'];x,y,w,h=[round(g[k]*scale) for k in ['x','y','w','h']]
  path=B/'art/book1-v07'/f"{q['id']}.png"
  with Image.open(path) as src:im=ImageOps.contain(src.convert('RGB'),(w,h))
  tile=Image.new('RGB',(w,h),'#e9e3d7');tile.paste(im,((w-im.width)//2,(h-im.height)//2))
  mask=Image.new('L',(w,h));md=ImageDraw.Draw(mask)
  if g['shape']=='oval':md.ellipse((0,0,w-1,h-1),fill=255)
  else:md.polygon([(round(a*w/100),round(b*h/100)) for a,b in g['polygon']],fill=255)
  canvas.paste(tile,(x,y),mask)
  zone=q.get('lettering',{}).get('zone',[4,5,66,25]);ty=y+round(h*zone[1]/100);bx=x+round(w*zone[0]/100);bw=round(w*zone[2]/100)
  for t in q['texts']:
   ls=lines(t['he'],bw-28);kind=t.get('presentation','caption');bh=len(ls)*31+18
   if kind in ['speech','thought']:
    draw.rounded_rectangle((bx,ty,bx+bw,ty+bh),radius=min(bh//3,25),fill='#fffef4',outline='#315448',width=2);color='#173c32'
    if kind=='speech':draw.polygon([(bx+bw*.74,ty+bh-1),(bx+bw*.8,ty+bh-1),(bx+bw*.81,ty+bh+15)],fill='#fffef4')
    else:
     for k,r in enumerate([5,4,2]):cx=bx+bw*.8+k*8;cy=ty+bh+9+k*8;draw.ellipse((cx-r,cy-r,cx+r,cy+r),fill='#fffef4',outline='#315448')
   else:draw.rounded_rectangle((bx,ty,bx+bw,ty+bh),radius=4,fill='#244b3e');color='#fffdf1'
   for j,line in enumerate(ls):draw.text((bx+bw-14,ty+8+j*31),line,font=font,fill=color,direction='rtl',anchor='ra')
   ty+=bh+13
  draw.text((x+4,y+3),q['id'],font=small,fill='#29553f')
 draw.text((20,1658),'Layout proof: contained sources, final crop and bubble-mouth anchoring pending.',font=small,fill='#516750')
 out=Q/f"page-{p['number']:02}-layout-proof.jpg";canvas.save(out,quality=91);made.append(p['number'])
(Q/'layout-proof-status.json').write_text(json.dumps(dict(pages=made,renderer='Pillow technical composition, not browser QA',master_pixels_unchanged=True,fit='contain'),indent=2))
print(json.dumps(dict(complete_source_pages=made)))
