# Satellite base (Sentinel-2 cloudless 2016, EOX, CC BY 4.0) for the siblings map, web-mercator, 1536x1024.
import math, io, urllib.request, sys
from PIL import Image
Z=9; T=256; N=2**Z*T
def mx(lon): return (lon+180)/360*N
def my(lat):
    r=math.radians(lat); return (1-math.log(math.tan(r)+1/math.cos(r))/math.pi)/2*N
lon0,lon1=17.1,23.5
cx_lat=51.25
x0,x1=mx(lon0),mx(lon1); w=x1-x0; h=w/1.5
yc=my(cx_lat); y0,y1=yc-h/2,yc+h/2
tiles={}
mos=Image.new('RGB',(int(x1//T-x0//T+1)*T,int(y1//T-y0//T+1)*T))
for tx in range(int(x0//T),int(x1//T)+1):
    for ty in range(int(y0//T),int(y1//T)+1):
        url=f'https://tiles.maps.eox.at/wmts/1.0.0/s2cloudless_3857/default/g/{Z}/{ty}/{tx}.jpg'
        data=urllib.request.urlopen(url,timeout=30).read()
        mos.paste(Image.open(io.BytesIO(data)).convert('RGB'),((tx-int(x0//T))*T,(ty-int(y0//T))*T))
ox,oy=int(x0//T)*T,int(y0//T)*T
crop=mos.crop((int(x0-ox),int(y0-oy),int(x1-ox),int(y1-oy))).resize((1536,1024),Image.LANCZOS)
crop.save('sat.jpg',quality=92)
open('sat_geo.txt','w').write(f'{x0} {y0} {w} {h} {Z}')
print(crop.size)
