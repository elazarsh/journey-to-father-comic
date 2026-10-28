import fitz, json, math, io, html
from PIL import Image
from pathlib import Path

src=Path(__file__).resolve().parent.parent; dest=src/'proof'; m=json.loads((src/'manifest.json').read_text(encoding='utf-8'))
font=str(dest/'fonts'/'DejaVuSans.ttf')
css=f'''@font-face {{font-family: NotoHebrew;src:url({font});}} * {{font-family:NotoHebrew;}} body {{ margin:0; direction:rtl; text-align:right; font-size:14px; color:#211b19; line-height:1.18; }}'''
arch=fitz.Archive(str(dest/'fonts'))
# Archive paths are relative to archive root.
css=css.replace(font,'DejaVuSans.ttf')
doc=fitz.open(); W,H=720,1040; gap=15; margin=24; header=50
for p in m['pages']:
 panels=[a for a in p['panels'] if a['kind']!='layer']; rows=math.ceil(len(panels)/2)
 page=doc.new_page(width=W,height=H); page.draw_rect(page.rect,color=None,fill=(.97,.96,.94))
 head=f'<p dir="rtl" style="font-size:20px;font-weight:bold;margin:0">המסע אל אבא — עמוד {p["page"]} | טיוטת איורים</p>'
 page.insert_htmlbox(fitz.Rect(margin,12,W-margin,45),head,css=css,archive=arch)
 cellw=(W-2*margin-gap)/2; cellh=(H-header-margin-(rows-1)*gap)/rows
 for i,a in enumerate(panels):
  col=1-(i%2); row=i//2; x=margin+col*(cellw+gap); y=header+row*(cellh+gap)
  contexts=[v.get('hebrew','').strip() for v in a.get('lettering_context',[]) if v.get('hebrew','').strip()]
  # Explicit label preserves each caption's wording while keeping it separate from artwork.
  text='<br>'.join(html.escape(t) for t in contexts)
  th=55 if text else 8
  im=Image.open(src/'art'/a['file']).convert('RGB');im.thumbnail((1100,900));buf=io.BytesIO();im.save(buf,format='JPEG',quality=81,optimize=True)
  available=cellh-th; actual_w=min(cellw, available*im.width/im.height); actual_h=actual_w*im.height/im.width
  r=fitz.Rect(x+(cellw-actual_w)/2,y,x+(cellw+actual_w)/2,y+actual_h);page.draw_rect(r,color=(.7,.66,.62),fill=(1,1,1),width=.5);page.insert_image(r,stream=buf.getvalue(),keep_proportion=True)
  if text: page.insert_htmlbox(fitz.Rect(x,y+actual_h+3,x+cellw,y+actual_h+th),f'<div dir="rtl">{text}</div>',css=css,archive=arch)
path=dest/'comic-storyboard-preview.pdf';doc.save(path,garbage=4,deflate=True);doc.close()
d=fitz.open(path);pix=d[0].get_pixmap(matrix=fitz.Matrix(1,1));pix.save(str(dest/'page-01.png'));print('pages',len(d),'size',path.stat().st_size)
