# Hand-built map of the siblings' new homes (real coordinates), 1536x1024, painted-parchment look.
import math
W,H=1536,1024
lon0,lon1,lat0,lat1=18.35,22.45,49.6,53.1
def P(lat,lon):
    x=(lon-lon0)/(lon1-lon0)*W
    y=(lat1-lat)/(lat1-lat0)*H
    return x,y
home=('יונדזיוב','Jędrzejów',50.645,20.303)
dest=[('קילץ','Kielce',50.866,20.628,'שרהלה','Sarale'),
      ('ורשה','Warsaw',52.230,21.012,'שמעון','Shimon'),
      ('מיעכוב','Miechów',50.357,20.028,'לייבל','Leibel'),
      ('לודז׳','Łódź',51.759,19.456,'איטשע','Itche')]
vistula=[(49.97,19.6),(50.05,19.95),(50.08,20.4),(50.2,20.95),(50.35,21.4),(50.68,21.75),(51.0,21.85),(51.35,21.8),(51.6,21.55),(51.9,21.3),(52.1,21.15),(52.25,21.05),(52.45,20.75),(52.55,20.5)]
pilica=[(50.45,19.65),(50.8,19.85),(51.1,20.05),(51.45,20.5),(51.65,21.0),(51.85,21.3)]
def path(pts): return 'M'+' L'.join('%.1f,%.1f'%P(a,b) for a,b in pts)
hx,hy=P(home[2],home[3])
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
'''<defs><radialGradient id="pg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#f3e3bf"/><stop offset=".7" stop-color="#e2c690"/><stop offset="1" stop-color="#b98d52"/></radialGradient>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .25  0 0 0 0 .12  0 0 0 .18 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7a2e16"/></marker></defs>''',
f'<rect width="{W}" height="{H}" fill="url(#pg)"/><rect width="{W}" height="{H}" filter="url(#rough)" fill="#000"/>',
f'<path d="{path(vistula)}" fill="none" stroke="#5f8aa0" stroke-width="7" stroke-linecap="round" opacity=".75"/>',
f'<path d="{path(pilica)}" fill="none" stroke="#5f8aa0" stroke-width="4" stroke-linecap="round" opacity=".6"/>']
vx,vy=P(51.15,21.95); svg.append(f'<text x="{vx}" y="{vy}" font-family="Frank Ruhl Libre,serif" font-size="30" fill="#4f7486" font-style="italic" text-anchor="middle" transform="rotate(-80 {vx} {vy})">ויסלה · Vistula</text>')
for name,en,lat,lon,kid,kid_en in dest:
    x,y=P(lat,lon); dx,dy=x-hx,y-hy; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L
    sx,sy=hx+ux*34,hy+uy*34; ex,ey=x-ux*30,y-uy*30
    cx,cy=(sx+ex)/2-uy*L*.12,(sy+ey)/2+ux*L*.12
    svg.append(f'<path d="M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}" fill="none" stroke="#7a2e16" stroke-width="5" stroke-dasharray="14 10" marker-end="url(#ar)" opacity=".85"/>')
    svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#7a2e16" stroke="#fbf1da" stroke-width="5"/>')
    off={'קילץ':(185,-24),'ורשה':(-60,-72),'מיעכוב':(-30,62),'לודז׳':(0,-72)}[name]
    lx=x+off[0]; y=y+off[1]+6; anchor='middle'
    svg.append(f'<text x="{lx:.1f}" y="{y-6:.1f}" font-family="Frank Ruhl Libre,serif" font-weight="900" font-size="46" fill="#3a2414" text-anchor="{anchor}" stroke="#f3e3bf" stroke-width="6" paint-order="stroke">{name}: {kid}</text>')
    svg.append(f'<text x="{lx:.1f}" y="{y+34:.1f}" font-family="Heebo,sans-serif" font-size="26" fill="#5a3a20" text-anchor="{anchor}" stroke="#f3e3bf" stroke-width="5" paint-order="stroke">{en}: {kid_en}</text>')
svg.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="26" fill="#c9861f" stroke="#3a2414" stroke-width="5"/><path d="M{hx-14:.1f},{hy+6:.1f} L{hx:.1f},{hy-12:.1f} L{hx+14:.1f},{hy+6:.1f} L{hx+14:.1f},{hy+14:.1f} L{hx-14:.1f},{hy+14:.1f}Z" fill="#3a2414"/>')
svg.append(f'<text x="{hx+300:.1f}" y="{hy+30:.1f}" font-family="Frank Ruhl Libre,serif" font-weight="900" font-size="46" fill="#3a2414" text-anchor="middle" stroke="#f3e3bf" stroke-width="6" paint-order="stroke">יונדזיוב, הבית: חוה ורייזל</text>')
svg.append(f'<text x="{hx+300:.1f}" y="{hy+66:.1f}" font-family="Heebo,sans-serif" font-size="26" fill="#5a3a20" text-anchor="middle" stroke="#f3e3bf" stroke-width="5" paint-order="stroke">Jędrzejów, home: Chava and Reizel</text>')
# compass
cx,cy=W-190,260
svg.append(f'<g opacity=".8"><circle cx="{cx}" cy="{cy}" r="58" fill="none" stroke="#3a2414" stroke-width="3"/><path d="M{cx},{cy-70} L{cx+14},{cy} L{cx},{cy+70} L{cx-14},{cy}Z" fill="#3a2414"/><text x="{cx}" y="{cy-80}" font-family="Heebo" font-size="30" font-weight="700" text-anchor="middle" fill="#3a2414">צ · N</text></g>')
svg.append(f'<text x="170" y="{H-150}" font-family="Frank Ruhl Libre,serif" font-size="40" font-weight="700" fill="#3a2414" text-anchor="start" opacity=".75">פולין · Poland</text>')
svg.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" fill="none" stroke="#5a3a20" stroke-width="6" opacity=".6"/></svg>')
open('map.svg','w',encoding='utf-8').write('\n'.join(svg))
html='<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@700;900&family=Heebo:wght@400;700&display=swap" rel="stylesheet"><style>body{margin:0}</style>'+'\n'.join(svg)
open('map.html','w',encoding='utf-8').write(html)
