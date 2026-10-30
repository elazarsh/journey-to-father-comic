from pathlib import Path
import json,math,html,base64,hashlib
V=Path(__file__).resolve().parent;B=V.parents[1]
book=json.loads((V/'book1-script.json').read_text());family=json.loads((V/'family-continuity.json').read_text())
OUT=V/'production';OUT.mkdir(exist_ok=True)
ART=B/'art/book1-v07';ART.mkdir(exist_ok=True)
STYLE='Dramatic pastoral literary graphic novel, painterly watercolor and gouache with selective fine ink contours, cinematic chiaroscuro, natural expressive faces, rich but restrained colors, tactile period materials, gentle atmospheric depth. Strong silhouettes and meaningful visual storytelling. Warmth and dignity in ordinary life, quiet beauty without idealizing hardship. Never cartoonishly enlarged eyes, generic cute faces, photorealistic skin or glossy 3D rendering.'
CHARACTERS={
 'approved_on':'2026-10-30','approval':'Family approved the first-book plot and the previously created Yitzhak child, youth and adult identities; targeted opening and comic lettering refinements authorized.',
 'child_master':'art/chars/yitzhak-child-v02.png','adult_elder_master':'art/chars/yitzhak-three-ages-v01.png',
 'elder_scene_reference':'art/drafts/p01-1.png','youth_continuity_photo':'ref/S08-img013.jpg',
 'identity_rules':'Keep narrow oval face, natural brown eyes, pronounced ears, bridge of nose and restrained mouth. Preserve identity across age changes. The older rejected child attempt is not the current child master. The middle image of the three-age sheet is adult, not a verified teenage sheet.',
 'youth_asset_status':'User approved youth likeness in conversation. No separately named illustrated teenage sheet was located in current art/chars. Use approved facial continuity and the existing youth photograph when constructing that stage; do not label the middle adult portrait a teenager.',
 'supporting_family':'Counts and relative ages follow family-continuity.json. Approval of Yitzhak does not identify the faces of other relatives.'}
(V/'character-approvals.json').write_text(json.dumps(CHARACTERS,ensure_ascii=False,indent=2))
# Canvas is 100 x 140; gutters and story order stay legible in RTL.
# Geometric variety is assigned by narrative purpose rather than a random mask on every panel.
def box(x,y,w,h,shape='soft',z=0):return dict(x=x,y=y,w=w,h=h,shape=shape,z=z)
def arrangement(n,p):
 if n==3:
  if p in [2,19,25,26,32,47,48]:return 'panorama-detail',[box(4,4,92,70,'slant-bottom'),box(52,78,44,58,'soft'),box(4,78,44,58,'oval' if p in [25,47] else 'slant-top')]
  return 'intimate',[box(4,4,92,76,'soft'),box(52,84,44,52,'soft'),box(4,84,44,52,'oval')]
 if n==5:return 'five-actions',[box(52,4,44,38),box(4,4,44,38),box(4,46,92,38,'slant-bottom'),box(52,88,44,48),box(4,88,44,48)]
 if p in [3,4,10,14,20,24,28,29,31,39,42,44,45,46]:
  return 'cinematic-bands',[box(4,4,92,43,'slant-bottom'),box(52,51,44,38,'soft'),box(4,51,44,38,'oval' if p in [4,10,20,42] else 'slant-top'),box(4,93,92,43,'slant-top')]
 if p in [11,21,33,35,36,40,43]:
  return 'tension-diagonal',[box(53,4,43,57,'slant-bottom'),box(4,4,45,57,'slant-top'),box(53,65,43,71,'slant-top'),box(4,65,45,71,'slant-bottom')]
 if p==12:return 'family-reveal',[box(52,4,44,35),box(4,4,44,35,'oval'),box(4,43,92,38,'slant-bottom'),box(4,85,92,51,'soft')]
 return 'quiet-flow',[box(52,4,44,45,'soft'),box(4,4,44,45,'soft'),box(4,53,92,40,'slant-bottom'),box(4,97,92,39,'soft')]
POLY={
 'soft':[[0,0],[100,0],[100,100],[0,100]],
 'slant-top':[[0,6],[100,0],[100,100],[0,100]],
 'slant-bottom':[[0,0],[100,0],[100,94],[0,100]],
 'oval':None}
manifest=[];geos=[];textrows=[]
for p in book['pages']:
 layout,boxes=arrangement(len(p['panels']),p['number']);p['production_layout']=layout
 for q,g in zip(p['panels'],boxes):
  g['polygon']=POLY[g['shape']];g['reading_order']=q['reading_order'];q['geometry']=g
  q['lettering']=dict(zone=[5,6,66,25],type=q['texts'][0].get('presentation','caption') if q['texts'] else 'none',tail_toward=[72,48],tail_status='provisional; re-anchor near actual speaker mouth after image inspection',language_policy='Live Hebrew RTL and English LTR; no lettering baked into images. On phone, text may flow below art for legibility.')
  age='elder about 71' if p['number'] in [1,47] else 'child about four' if p['number'] in [2,3,4,5,6,7] else 'later childhood, exact age uncertain' if p['number']<=24 else 'young teenager about 13–14' if p['number']<=29 else 'teenager about 16–17' if p['number']<=34 else 'young adult, early twenties' if p['number']<=43 else 'young adult about 25 in 1925'
  palette='warm amber and soft blue domestic light' if p['number']<=12 else 'muted blue-green with humane warm light' if p['number']<=19 else 'ochre and restrained blue-grey' if p['number']<=31 else 'pastoral olive, sunlit earth and deep sky' if p['number'] in [32,33] else 'dusk blue, warm skin, restrained contrast' if p['number'] in [35,36,37] else 'soft amber domestic and work colors' if p['number']<=44 else 'deep maritime blue with hopeful warm light'
  if p['number']==4:palette='warm amber oil-lamp light with deep indigo shadows'
  target_ratio=g['w']/(g['h']*1.4)
  size=[1536,1024] if target_ratio>=1 else [1024,1536]
  filename=f"art/book1-v07/{q['id']}.png"
  refs=['art/chars/yitzhak-child-v02.png'] if p['number']<=34 else ['art/chars/yitzhak-three-ages-v01.png']
  if p['number'] in [1,47]:refs=['art/chars/yitzhak-three-ages-v01.png','art/drafts/p01-1.png']
  if 25<=p['number']<=43:refs+=['ref/S08-img013.jpg']
  casting=p.get('family_cast');rule=casting['rule'] if casting else 'Only the figures required by this action. Do not populate the scene with extra identifiable siblings.'
  prompt=f"{STYLE}\nONE scene, ONE image; no panel borders, collage, speech balloons, thought clouds, readable lettering, logos or watermarks.\nAction: {q['action']}\nAge continuity for Yitzhak: {age}.\nFamily constraint: {rule}\nPalette: {palette}.\nCompose for a {target_ratio:.2f}:1 visible panel, source requested {size[0]}x{size[1]}. Keep all essential faces, hands and props within central 60% width and central 56% height, with at least 15% overscan. Reserve subdued low-detail wall/sky in upper-left for live lettering. Use foreground, gaze and light to convey the action instead of explaining it with invented objects.\nSource-based historical event, proposed staging. No new promises, rescues, battles, relatives, modern flags or invented dated evidence. Leather shop sells supplies and is not a cobbler workshop."
  r=dict(id=q['id'],page=p['number'],file=filename,kind='panel',status='planned',generate_size=size,palette=palette,age_band=age,geometry=g,lettering=q['lettering'],protected_source_zone=[20,24,60,56],quiet_source_zone=[4,4,48,18],crop=dict(fx=.5,fy=.5,zoom=1,fit='cover',mirror=False),zoom_checks=[1,1.05,1.15],reference_paths=refs,family_contract=casting,source_ids=p['sources'],prompt=prompt)
  manifest.append(r);geos.append(dict(id=q['id'],page=p['number'],**g));textrows.extend(dict(panel=q['id'],page=p['number'],**t) for t in q['texts'])
 # Link a per-page production note with both copy and composition contract.
 notes=[f"# עמוד {p['number']}: {p['title']}",f"פריסה: {layout}; סדר קריאה לפי reading_order מימין לשמאל."]
 for q in p['panels']:notes += [f"## {q['id']}",q['action'],json.dumps(q['geometry'],ensure_ascii=False),'כיתוב חי: '+' / '.join(t['he'] for t in q['texts'])]
 (OUT/f"page-{p['number']:02}.md").write_text('\n\n'.join(notes))
(OUT/'manifest.json').write_text(json.dumps(dict(version='0.7',status='Ready to start the authorized opening image batch; layout and lettering are production drafts',style=STYLE,images=manifest),ensure_ascii=False,indent=2))
(OUT/'geometry.json').write_text(json.dumps(dict(canvas=dict(width=100,height=140),panels=geos),ensure_ascii=False,indent=2))
(OUT/'text.json').write_text(json.dumps(textrows,ensure_ascii=False,indent=2))
(V/'book1-script.json').write_text(json.dumps(book,ensure_ascii=False,indent=2))
progresspath=ART/'progress.json'
if not progresspath.exists():progresspath.write_text(json.dumps(dict(version='0.7',requested_batch=['B01V07-P03-01','B01V07-P04-02','B01V07-P01-01'],assets=[],status='Awaiting verified GitHub pre-art handoff'),ensure_ascii=False,indent=2))
if not (ART/'generation-receipts.json').exists():(ART/'generation-receipts.json').write_text('[]')
# Refresh the live HTML after geometry attachment. Existing master pixels remain unchanged.
report=json.loads((V/'qa-report.json').read_text());report['production_contracts']=dict(panels=len(manifest),layout_families=len(set(p['production_layout'] for p in book['pages'])),shapes=sorted(POLY),all_have_crop_and_quiet_zone=True,actual_image_crop_review='pending generation')
(V/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
elder=B/'art/web/draft-p01-1.webp';img='data:image/webp;base64,'+base64.b64encode(elder.read_bytes()).decode()
payload=json.dumps(dict(book=book,series=json.loads((V/'series-plan.json').read_text())['requested_volumes'],report=report,elder=img,family=family['evidence']),ensure_ascii=False).replace('</','<\\/')
tpl=(V/'template.html').read_text()
for name,mode in [('index.html','overview'),('book1-reader.html','reader')]: (V/name).write_text(tpl.replace('__MODE__',mode).replace('__DATA__',payload))
# All-page geometry reference for the next tool, with truthful placeholders, no generated art implied.
svgpages=[]
for p in book['pages']:
 shapes=[]
 for q in p['panels']:
  g=q['geometry'];x,y,w,h=g['x'],g['y'],g['w'],g['h']
  if g['shape']=='oval':el=f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}"/>'
  else:el='<polygon points="'+' '.join(f'{x+a*w/100},{y+b*h/100}' for a,b in g['polygon'])+'"/>'
  shapes += [el,f'<text x="{x+w/2}" y="{y+h/2}" text-anchor="middle">{q["reading_order"]}</text>']
 svgpages.append(f'<article><h2>עמוד {p["number"]}: {html.escape(p["title"])}</h2><svg viewBox="0 0 100 140">'+''.join(shapes)+'</svg><p>'+html.escape(p['production_layout'])+'</p></article>')
(OUT/'layout-map.html').write_text('<!doctype html><html lang="he" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>48 עמודים, מפת פריסה</title><style>body{background:#eee8dc;color:#173c34;font:17px Arial;padding:20px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}article{background:#fffaf0;padding:18px;border-radius:10px}svg{width:100%;max-height:440px}polygon,ellipse{fill:#dfdfc7;stroke:#527566;stroke-width:.5}text{fill:#315849;font-size:6px}h2{font-size:18px}</style><h1>מפת פריסות, ספר 1</h1><p>מספרי המשבצות מציינים סדר קריאה. אלו חלונות איור מתוכננים, לא עמודי איורים גמורים. האיורים המקוריים יישמרו ללא מסגרות וכיתוב.</p><main>'+''.join(svgpages)+'</main></html>')
print(json.dumps(dict(pages=48,panels=len(manifest),layouts=len(set(p['production_layout'] for p in book['pages'])),speech=sum(t.get('presentation')=='speech' or t['kind']=='adapted_speech' for t in textrows),thought=sum(t.get('presentation')=='thought' for t in textrows)),ensure_ascii=False))
