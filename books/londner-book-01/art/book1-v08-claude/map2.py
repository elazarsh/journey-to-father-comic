# Siblings map on a real satellite base (Sentinel-2 cloudless 2016 by EOX, CC BY 4.0). Real town coordinates.
import math, base64, sys
OUT=sys.argv[1]
from PIL import Image, ImageEnhance
x0,y0,w,h,Z=[float(v) for v in open(OUT+'_geo.txt').read().split()]
from PIL import Image as _I
W,H=_I.open(OUT+'.jpg').size
TALL=H>W; N=2**int(Z)*256
def P(lat,lon):
    r=math.radians(lat); X=(lon+180)/360*N; Y=(1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*N
    return (X-x0)/w*W,(Y-y0)/h*H
im=Image.open(OUT+'.jpg'); im=ImageEnhance.Brightness(im).enhance(1.35); im=ImageEnhance.Contrast(im).enhance(1.08); im=ImageEnhance.Color(im).enhance(0.9)
warm=Image.new('RGB',im.size,(255,214,150)); im=Image.blend(im,warm,0.12); im.save(OUT+'_warm.jpg',quality=92)
b64=base64.b64encode(open(OUT+'_warm.jpg','rb').read()).decode()
home=('יונדזיוב','Jędrzejów',50.645,20.303)
TALL=TALL
dest=[('קילץ','Kielce',50.866,20.628,'שרהלה','Sarale',(130 if TALL else 170,-18)),
      ('ורשה','Warsaw',52.230,21.012,'שמעון','Shimon',(-150,58) if TALL else (170,10)),
      ('מיעכוב','Miechów',50.357,20.028,'לייבל','Leibel',(-60,58)),
      ('לודז׳','Łódź',51.759,19.456,'איטשע','Itche',(0,-72))]
hx,hy=P(home[2],home[3])
T='font-family="Frank Ruhl Libre,serif" font-weight="900" fill="#fff6e2" stroke="#2a1a0c" stroke-width="8" paint-order="stroke" text-anchor="middle"'
E='font-family="Heebo,sans-serif" font-weight="700" fill="#fff6e2" stroke="#2a1a0c" stroke-width="6" paint-order="stroke" text-anchor="middle"'
s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
 '<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#ffcf5a"/></marker>',
 '<radialGradient id="vg" cx="50%" cy="50%" r="72%"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1a0f05" stop-opacity=".55"/></radialGradient></defs>',
 f'<image href="data:image/jpeg;base64,{b64}" width="{W}" height="{H}"/>',f'<rect width="{W}" height="{H}" fill="url(#vg)"/>']
for name,en,lat,lon,kid,kid_en,off in dest:
    x,y=P(lat,lon); dx,dy=x-hx,y-hy; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L
    sx,sy=hx+ux*36,hy+uy*36; ex,ey=x-ux*28,y-uy*28; cx,cy=(sx+ex)/2-uy*L*.12,(sy+ey)/2+ux*L*.12
    d=f'M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}'
    s.append(f'<path d="{d}" fill="none" stroke="#2a1a0c" stroke-width="11" opacity=".55"/><path d="{d}" fill="none" stroke="#ffcf5a" stroke-width="6" stroke-dasharray="16 10" marker-end="url(#ar)"/>')
    s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#c0392b" stroke="#fff6e2" stroke-width="5"/>')
    lx,ly=x+off[0],y+off[1]
    s.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="48" {T}>{name}: {kid}</text>')
s.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="28" fill="#e0a84f" stroke="#2a1a0c" stroke-width="5"/><path d="M{hx-15:.1f},{hy+6:.1f} L{hx:.1f},{hy-13:.1f} L{hx+15:.1f},{hy+6:.1f} L{hx+15:.1f},{hy+15:.1f} L{hx-15:.1f},{hy+15:.1f}Z" fill="#2a1a0c"/>')
s.append(f'<text x="{hx+(0 if TALL else 275):.1f}" y="{hy+(84 if TALL else 44):.1f}" font-size="48" {T}>יונדזיוב, הבית: חוה ורייזל</text>')
cx,cy=W-150,170
s.append(f'<g><circle cx="{cx}" cy="{cy}" r="56" fill="#000" fill-opacity=".25" stroke="#fff6e2" stroke-width="3"/><path d="M{cx},{cy-66} L{cx+13},{cy} L{cx},{cy+66} L{cx-13},{cy}Z" fill="#fff6e2"/><text x="{cx}" y="{cy-78}" font-size="30" {E}>צפון</text></g>')
s.append(f'<text x="330" y="{H-170}" font-size="44" {T}>פולין</text>')
s.append(f'<text x="{W-40}" y="{H-24}" font-family="Heebo" font-size="16" fill="#fff6e2" opacity=".8" text-anchor="end">צילום לוויין: EOX, Sentinel-2 2016 (CC BY 4.0)</text></svg>')
open(OUT+'.html','w',encoding='utf-8').write('<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@900&family=Heebo:wght@400;700&display=swap" rel="stylesheet"><style>body{margin:0}</style>'+'\n'.join(s))
