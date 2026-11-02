"""Generate comparison proofs for suggested crop-only treatments. Does not edit production."""
from pathlib import Path
import json,sys,math,hashlib
from PIL import Image,ImageDraw,ImageFont
B=Path(__file__).resolve().parents[3];Q=Path(__file__).resolve().parent
M=json.loads((Q/'crop-proof-metadata.json').read_text());byid={r['id']:r for r in M['panels']};assets={a['id']:a for a in json.loads((B/'art/book1-v07/progress.json').read_text())['assets']}
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
ids=['B01V07-P01-02','B01V07-P05-01','B01V07-P08-01','B01V07-P21-01','B01V07-P28-04','B01V07-P38-02','B01V07-P38-03']
records=[]
for pid in ids:
 a=assets[pid];p=B/a['file'];p=p if p.exists() else B/a['web_file'];im=Image.open(p).convert('RGB');m=byid[pid];asp=m['desktop_box_aspect'];W=600;H=max(50,min(700,round(W/asp)));H=round(W/asp) if W/asp<700 else 700
 # Use native aspect but cap long side for tall panels.
 if W/asp>=700:H=700;W=round(H*asp)
 px,py=m['current_object_position'];s=max(W/im.width,H/im.height);z=1.03;ox=((W-im.width*s)*px/100-W/2)*z+W/2;oy=((H-im.height*s)*py/100-H/2)*z+H/2
 cur=im.transform((W,H),Image.Transform.AFFINE,(1/(s*z),0,-ox/(s*z),0,1/(s*z),-oy/(s*z)),Image.Resampling.BICUBIC)
 prop=Image.new('RGB',(W,H),'#221b16');fit=min(W/im.width,H/im.height)*.92;tmp=im.resize((max(1,round(im.width*fit)),max(1,round(im.height*fit))),Image.Resampling.LANCZOS);prop.paste(tmp,((W-tmp.width)//2,(H-tmp.height)//2))
 # Show a fy=0 cover candidate for wide sermon; keep contain as safe fallback.
 if pid=='B01V07-P05-01':
  s=max(W/im.width,H/im.height);ox=(W-im.width*s)*.5;oy=H-im.height*s;prop=im.transform((W,H),Image.Transform.AFFINE,(1/s,0,-ox/s,0,1/s,-oy/s),Image.Resampling.BICUBIC);candidate={'fit':'cover','fx':.5,'fy':1.0,'zoom':1.0}
 else:candidate={'fit':'contain','fx':.5,'fy':.5,'zoom':.92,'note':'8% renderer inset keeps source content clear of diagonal mask corners; stage fills unused area. Prefer reallocate panel height/width when image would become too small.'}
 # polygon mask in local screen coordinates
 sh=m['shape'];poly=sh.get('poly')
 if poly:
  pts=[(100-x,y) for x,y in poly];xs=[p[0] for p in pts];ys=[p[1] for p in pts];x0,y0=min(xs),min(ys);bw,bh=max(xs)-x0,max(ys)-y0
  mask=Image.new('L',(W,H),0);ImageDraw.Draw(mask).polygon([((x-x0)/bw*W,(y-y0)/bh*H) for x,y in pts],fill=255)
  for img in [cur,prop]:img.paste(Image.new('RGB',(W,H),'#eee7da'),(0,0),Image.eval(mask,lambda v:255-v))
 sheet=Image.new('RGB',(max(2*W+30,700),H+85),'#eee7da');d=ImageDraw.Draw(sheet);d.text((10,5),pid+' | crop candidates, no lettering',font=F,fill='black');d.text((10,30),'Current source in v08 mask',font=F,fill='black');d.text((W+20,30),'Candidate (renderer only)',font=F,fill='black');sheet.paste(cur,(10,65));sheet.paste(prop,(W+20,65));sheet.save(Q/f'{pid}-crop-options.png')
 records.append(dict(id=pid,sourceSHA=a['sha256'],proof_input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),candidate=candidate,implemented=False,review_status='static candidate only; needs actual polygon/lettering/phone validation'))
(Q/'crop-override-candidates.json').write_text(json.dumps(records,indent=2))
print(len(records),'comparison proofs')
