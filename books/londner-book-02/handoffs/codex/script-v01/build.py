from pathlib import Path
import copy,json,re,html,hashlib
from script_data import PAGES,c
from series_data import SEQUENCES,TURNS,OPEN_QUESTIONS
from family_data import FAMILY
V=Path(__file__).resolve().parent
source={p['id']:p for p in json.loads((V/'research/source-pages.json').read_text())}
pages=copy.deepcopy(PAGES);registry=[];quotes=[];allpanels=[]
POLY={'soft':[[0,0],[100,0],[100,100],[0,100]],'slant-bottom':[[0,0],[100,0],[100,93],[0,100]],'slant-top':[[0,7],[100,0],[100,100],[0,100]],'oval':None}
def frame(x,y,w,h,shape):return dict(x=x,y=y,w=w,h=h,shape=shape,polygon=POLY[shape])
def layout(n,num):
 if n==4:return 'action-sequence',[frame(52,4,44,42,'soft'),frame(4,4,44,42,'slant-bottom'),frame(4,50,92,39,'slant-bottom'),frame(4,93,92,43,'soft')]
 if num in [1,7,12,16,21,25,32,39,41,48,50,57,59,60,61,64]:
  return 'panorama-details',[frame(4,4,92,72,'slant-bottom'),frame(52,80,44,56,'soft'),frame(4,80,44,56,'oval' if num==25 else 'slant-top')]
 if num in [13,27]:return 'quiet-presence',[frame(52,4,44,52,'soft'),frame(4,4,44,52,'soft'),frame(4,60,92,76,'soft')]
 if num in [3,8,22,28,33,36,42,43,47,49,51,53,55,58,63]:
  return 'question-and-reaction',[frame(52,4,44,59,'slant-bottom'),frame(4,4,44,59,'slant-top'),frame(4,67,92,69,'soft')]
 return 'intimate-flow',[frame(4,4,92,58,'soft'),frame(52,66,44,70,'soft'),frame(4,66,44,70,'oval' if num==4 else 'slant-top')]
for p in pages:
 p['sequence']=next(s['id'] for s in SEQUENCES if s['first']<=p['number']<=s['last'])
 explicit={t['source'] for _,t in p['beats'] if t and t.get('source')}
 p['sources']=list(dict.fromkeys(p['sources']+sorted(explicit)))
 assert all(sid in source for sid in p['sources'])
 p['layout'],frames=layout(len(p['beats']),p['number']);p['panels']=[]
 for i,(action,t) in enumerate(p.pop('beats')):
  pid=f"B02V01-P{p['number']:02}-{i+1:02}";texts=[]
  if t:
   t.update(id=pid+'-T1',sources=p['sources'],review_required=t['kind']!='quote')
   t['source']=t['source'] or p['sources'][0]
   assert t['source'] in p['sources']
   assert t['he'] and t['en']
   assert not re.search('[—–]',t['he'])
   assert len(t['he'].split())<=18,(p['number'],t['he'])
   if t['presentation'] in ['speech','thought']:assert len(t['he'].split())<=12,(p['number'],t['he'])
   if t['kind']=='quote':
    needle=' '.join(t['he'].strip(' .!?,:;').split());hay=' '.join(source[t['source']]['text'].split())
    assert needle in hay,(pid,needle)
    quotes.append(t)
   else:registry.append(dict(page=p['number'],**t))
   texts=[t]
  panel=dict(id=pid,reading_order=i+1,action=action,texts=texts,geometry=frames[i],art_status='not generated',source_ids=p['sources'],historical_status='Source-based event; exact gestures, framing and supporting faces are proposed staging.')
  p['panels'].append(panel);allpanels.append(panel)
 p['word_count_he']=sum(len(t['he'].split()) for q in p['panels'] for t in q['texts'])
 assert p['word_count_he']<=50,(p['number'],p['word_count_he'])
 # All frames fit and are separate; these are planned shapes, not a finished image crop approval.
 for i,g in enumerate(frames):
  assert g['x']>=0 and g['y']>=0 and g['x']+g['w']<=100 and g['y']+g['h']<=140
  for h in frames[:i]:assert max(0,min(g['x']+g['w'],h['x']+h['w'])-max(g['x'],h['x']))*max(0,min(g['y']+g['h'],h['y']+h['h'])-max(g['y'],h['y']))==0
assert [p['number'] for p in pages]==list(range(1,65))
assert len({q['id'] for q in allpanels})==len(allpanels)
assert sum(q['geometry']['shape']=='oval' for q in allpanels)<=2
for group in FAMILY['household_counts']:
 assert sum(group.get('member_counts',{}).get(member,1) for member in group['members'])==group['count']
endcopy=' '.join(t['he'] for p in pages[62:] for q in p['panels'] for t in q['texts'])
assert 'גנבו לנו את שני הסוסים' in endcopy
assert all(word not in endcopy for word in ['קנדה','אסתר','קניתי זוג סוסים'])
for t in TURNS:assert t['setup']%2 and t['reveal']==t['setup']+1
TAKEAWAYS=[c('אפשר ללמוד גם ממי שצעיר מאיתנו.','We can learn from people younger than ourselves.',basis='editorial_takeaway'),c('לבקש עזרה, ולהציע כשאפשר.','Ask for help, and offer it when you can.',basis='editorial_takeaway'),c('לבנות צעד אחר צעד.','Build one step at a time.',basis='editorial_takeaway')]
for i,t in enumerate(TAKEAWAYS):
 t.update(id=f'B02V01-TAKEAWAY-{i+1}',sources=['S08-memoir-74','S08-memoir-106','S08-memoir-108'],review_required=True)
 registry.append(dict(page=62,**t))
pages[61]['reader_takeaways']=TAKEAWAYS
ending=c('המשך יבוא בספר השלישי.','To be continued in the third book.',basis='series_boundary',speaker='מסגרת הספר');ending.update(id='B02V01-CONTINUED',sources=[],review_required=True);pages[63]['continued']=ending;registry.append(dict(page=64,**ending))
book=dict(version='0.2-reviewed-script',book_number=2,title_he='מקום משלנו',title_en='A Place of Our Own',status='Complete source-grounded review script, not yet family-approved; no illustrations generated for book 2',audience='Children 10+, teenagers and adults; family descendants',story_pages=64,physical_pages_provisional=68,pages=pages,sequences=SEQUENCES,page_turns=TURNS,scope='Arrival in 1925, household and livelihood, family losses and new children, help for other families and Reuven, the attempt to help Hershel, wartime work, 1943 dismissal and move toward farming, children teaching the parents, gradual farm building, theft of the horses. Stop before any Canadian help or Esther rescue process.',reader_opening_policy='Start immediately with the arrival that book 1 withheld. No plot synopsis or future loss spoilers in the opening.',print_assumption='Story page 1 is provisionally a single left page in an RTL book; spreads 2/3, 4/5 etc. Check actual front-matter imposition before final illustration and printing.',wording_policy='All new Hebrew and English copy is registered. Adapted speech draws on reported exchanges; thought bubbles only adapt reported uncertainty or intentions. Staging is proposed, not newly discovered evidence.',open_questions=OPEN_QUESTIONS,visual_style='Dramatic pastoral literary graphic novel, painterly watercolor/gouache with selected fine ink, cinematic light and natural expressive faces. Consistent with family-approved Yitzhak identities.',art_policy='One scene per image, no baked-in lettering, bubbles or borders. Reserve low-detail space away from faces and mouth for live lettering. Art contracts and actual face-crop checks are not claimed in this script-only draft.')
(V/'book2-script.json').write_text(json.dumps(book,ensure_ascii=False,indent=2))
(V/'new-wording-registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
(V/'family-continuity.json').write_text(json.dumps(FAMILY,ensure_ascii=False,indent=2))
used={sid for p in pages for sid in p['sources']};used.update(s for r in FAMILY['nuclear_family']+FAMILY['other_households'] for s in r['sources'])
assert all(s in source for s in used)
(V/'source-excerpts.json').write_text(json.dumps([source[s] for s in sorted(used)],ensure_ascii=False,indent=2))
report=dict(story_pages=64,physical_pages_provisional=68,panels=len(allpanels),text_blocks=sum(len(q['texts']) for q in allpanels)+len(TAKEAWAYS)+1,words_he=sum(p['word_count_he'] for p in pages)+sum(len(t['he'].split()) for t in TAKEAWAYS)+len(ending['he'].split()),max_page_words_he=max(p['word_count_he'] for p in pages),max_text_block_words_he=max(len(t['he'].split()) for t in registry+quotes),silent_action_panels=sum(not q['texts'] for q in allpanels),literal_quotes_verified=len(quotes),adapted_speech_bubbles=sum(t['kind']=='adapted_speech' for t in registry),documented_thought_bubbles=sum(t['kind']=='adapted_thought' for t in registry),scene_sequences=len(SEQUENCES),farm_sequence_pages=23,designed_real_page_turn_pairs=len(TURNS),layout_families=len({p['layout'] for p in pages}),checks=dict(all_64_pages_have_need_change_emotion=True,all_sources_resolve=True,quotes_match_primary=True,all_text_bilingual=True,all_new_text_registered=True,no_long_dashes_in_hebrew=True,all_block_word_counts_under_19=True,all_page_word_counts_under_51=True,unique_panel_ids=True,geometry_in_canvas_and_no_frame_overlaps=True,exact_horse_theft_boundary_without_solution=True,speech_and_thought_under_13_words=True,oval_insets_at_most_two=True,household_counts_consistent=True),not_claimed=['No illustrations generated for book 2.','No browser visual QA, image masking, face-crop or final typography approval.','No child comprehension trial or guarantee against anxiety.','No final family approval of book 2 or unresolved chronology.'])
(V/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
md=['# מקום משלנו · ספר 2 · תסריט מלא לעיון','64 עמודי סיפור. זהו תסריט והוראות איור, לא ספר מאויר גמור. ספר 1 נשאר ללא שינוי.','הכותרות, שאלות המתח והסברי התפקיד נועדו לעריכה, לא להקדמה לילדים.']
reading=['# מקום משלנו · כיתוב הקריאה ברצף','כיתוב בלבד. פעולות שקטות ותוכן חזותי אינם מופיעים בקובץ זה.']
for p in pages:
 md += [f"## עמוד {p['number']}: {p['title']}",f"הצורך: {p['scene_need']}",f"השינוי: {p['change']}",f"הרגש: {p['emotion']}",f"אל ההמשך: {p['turn_hook']}",f"מה לא ממציאים: {p['withhold']}"]
 reading += [f"## עמוד {p['number']}"]
 for q in p['panels']:
  md += [f"### {q['id']}",q['action']]
  if not q['texts']:md+=['ללא כיתוב.']
  for t in q['texts']:
   md += [f"{t['speaker']} · {t['kind']}: {t['he']}",t['en']]
   reading += [t['he']]
 if p.get('reader_takeaways'):
  md += ['מחשבות לקורא, בנפרד מקולו של יצחק:']+[t['he'] for t in p['reader_takeaways']];reading += [t['he'] for t in p['reader_takeaways']]
 if p.get('continued'):md += [p['continued']['he']];reading += [p['continued']['he']]
 md += ['מקורות: '+', '.join(p['sources'])]
(V/'script-he.md').write_text('\n\n'.join(md));(V/'reading-text-he.md').write_text('\n\n'.join(reading))
wording=['# נוסח חדש לעיון המשפחה','כל הכיתוב כאן מעובד. הציטוטים המילוליים שבתסריט נבדקו מול המקור. דיבור ומחשבה אינם תמליל אלא עיבוד של שיחה, כוונה או אי־ידיעה מתועדת. מסגרת המספר ומסקנות הסיפור הן ניסוח ספרותי רשום.']
for t in registry:wording += [f"## {t['id']} · עמוד {t['page']}",t['he'],t['en'],f"סוג: {t['kind']}; עיגון: {t['basis']}",'מקורות: '+', '.join(t['sources'])]
(V/'new-wording-review.md').write_text('\n\n'.join(wording))
family=['# מפת המשפחה והגילים','לא כל הדמויות גרים יחד בכל תקופה. אין לצייר ילדים שטרם נולדו או ילדים שנפטרו בתוך אירועים מאוחרים.']
for r in FAMILY['nuclear_family']:family += ['## '+r['name'],r['role'],r.get('birth',''),r.get('death',''),r['visual'],'מקורות: '+', '.join(r['sources'])]
family+=['## משקי בית אחרים']
for r in FAMILY['other_households']:family += ['### '+r['name'],r['rule'],'מקורות: '+', '.join(r['sources'])]
family+=['## ספירת דמויות לפי תקופה']
for r in FAMILY['household_counts']:family += ['### '+r['period'],str(r['count'])+' דמויות. '+r['note']]
family+=['## הנחיות נוכחות וגיל']+['- '+x for x in FAMILY['casting_rules']]
(V/'family-continuity.md').write_text('\n\n'.join(family))
payload=json.dumps(dict(book=book,report=report,family=FAMILY),ensure_ascii=False).replace('</','<\\/')
tpl=(V/'template.html').read_text()
for name,mode in [('index.html','overview'),('book2-reader.html','reader')]: (V/name).write_text(tpl.replace('__MODE__',mode).replace('__DATA__',payload))
print(json.dumps(report,ensure_ascii=False,indent=2))
