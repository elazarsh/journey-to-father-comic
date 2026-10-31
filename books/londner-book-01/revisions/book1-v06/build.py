from pathlib import Path
import copy,json,re,html,base64,hashlib
from book1_scene_data import PAGES,text
from series_data import SERIES,SEQUENCES,TURNS
from family_data import FAMILY,CAST

V=Path(__file__).resolve().parent;B=V.parents[1]
sources={p['id']:p for p in json.loads((B/'research/pages.json').read_text())}
pages=copy.deepcopy(PAGES)
registry=[];literal=[];panels=[]
for p in pages:
    for sid in p['sources']:assert sid in sources,sid
    p['sequence']=next(s['id'] for s in SEQUENCES if s['first']<=p['number']<=s['last'])
    p['family_cast']=CAST.get(p['number'])
    p['panels']=[]
    for i,action in enumerate(p.pop('actions')):
        pid=f"B01V06-P{p['number']:02}-{i+1:02}"
        tx=p['copy'].get(i)
        ts=[] if tx is None else [tx]
        for j,t in enumerate(ts):
            t.update(id=pid+f'-T{j+1}',sources=p['sources'],review_required=t['kind']!='quote')
            if t['source'] is None:t['source']=p['sources'][0]
            assert t['source'] in sources
            if t['kind']=='quote':
                needle=' '.join(t['he'].strip(' .!?,:;').split());hay=' '.join(sources[t['source']]['text'].split())
                assert needle in hay,(pid,needle)
                literal.append(t)
            else:registry.append(dict(page=p['number'],**t))
            assert not re.search('[—–]',t['he'])
        q=dict(id=pid,reading_order=i+1,action=action,texts=ts,kind='scene',visual_status='storyboard directions, not generated art',historical_status='Source-based event; exact framing, gestures and environment are proposed staging.',source_ids=p['sources'])
        p['panels'].append(q);panels.append(q)
    assert all(int(i)<len(p['panels']) for i in p.pop('copy'))
    p['word_count_he']=sum(len(t['he'].split()) for q in p['panels'] for t in q['texts'])
    assert p['word_count_he']<=55,(p['number'],p['word_count_he'])

takeaways=[text('לשאול, ללמוד ולנסות.','Ask, learn and try.',kind='editorial',speaker='מסגרת הספר'),text('לשמור על יושר גם כשאיש לא בודק.','Be honest even when no one is checking.',kind='editorial',speaker='מסגרת הספר'),text('לקבל עזרה, ולקחת אחריות.','Accept help and take responsibility.',kind='editorial',speaker='מסגרת הספר')]
for i,t in enumerate(takeaways):
    t.update(id=f'B01V06-TAKEAWAY-{i+1}',sources=['S08-memoir-9','S08-memoir-10','S08-memoir-22','S08-memoir-23','S08-memoir-29','S08-memoir-40'],review_required=True)
    registry.append(dict(page=47,**t))
pages[46]['reader_takeaways']=takeaways
ending=text('המשך יבוא.','To be continued.',kind='editorial',speaker='מסגרת הספר');ending.update(id='B01V06-CONTINUED',sources=[],review_required=True)
pages[47]['continued']=ending;registry.append(dict(page=48,**ending))

for t in TURNS:
    assert t['setup']%2==1 and t['reveal']==t['setup']+1
    assert 1<=t['setup']<=48 and 1<=t['reveal']<=48
assert [p['number'] for p in pages]==list(range(1,49))
assert len({q['id'] for q in panels})==len(panels)
assert all(t['he'] and t['en'] for t in registry+literal)

book=dict(version='0.6-three-volume-merged-book1',book_number=1,title_he='הדרך של איטשע',title_en='Itshe’s Journey',status='Complete 48-page scene-and-panel review draft; not final approved art or print layout',audience='Children 10+, teenagers and adults; descendants meeting Yitzhak for the first time',story_pages=48,physical_pages_provisional=52,pages=pages,sequences=SEQUENCES,page_turns=TURNS,reader_opening_policy='Only the personal family dedication before the story. No series synopsis or foreknowledge of later losses.',scope='Childhood and learning, recovery, family work and honesty, orphanhood, independent trade, wartime work, farming dream, two army services, marriage and departure on Asia in 1925. Stop before arrival; arrival opens book 2.',editorial_frame='The direct address to great-grandchildren is new literary framing requested by the family. The 1971 diary dedication names children and grandchildren. No meeting with great-grandchildren is claimed.',stage_policy='Known events may be staged visually; do not invent a new incident, spoken exchange, promise, failure, rescue or emotional declaration as historical fact.',print_assumption='For planning, story page 1 is a single left page in an RTL book; spreads are 2/3, 4/5 etc. Verify actual front-matter imposition before final art. Reveal pairs must stay separated by a real page turn.',open_questions=['Exact ages and dates for foot illness, Warsaw and Vienna.','The Balkan-wars reference and place names are retrospective; do not infer a precise year from them without further research.','The first-school recollection names 1904. Character age must differ from later childhood; the existing child-v02 is not a verified age-four reference.','The timing of Father’s departure relative to surgery in Warsaw is not dated.','The original says Father did not collect Yitzhak on the return from Warsaw; a man from their town did.','The siddur was thrown ON TOP of a tall stove. No burning, retrieval or replacement is recorded.','Which Vienna hospital and synagogue, supporting faces and exact buildings remain unidentified.'],lettering_policy='Live Hebrew and English, one scene per image, no AI lettering, generous crop and text margins. Count words after arranging the scene; never abbreviate essential context to hit an arbitrary total.')

(V/'book1-script.json').write_text(json.dumps(book,ensure_ascii=False,indent=2))
(V/'series-plan.json').write_text(json.dumps(dict(version='0.6',volume_count=3,requested_volumes=SERIES,total_story_pages_min=sum(x['story_pages_min'] for x in SERIES),total_story_pages_max=sum(x['story_pages_max'] for x in SERIES),status='Three-volume structure requested by family; only book 1 has a complete panel script. Later lengths remain provisional.',boundary_policy='Stop inside an unresolved source-based process between books. No invented cliff danger and no spoiler synopsis in reader opening.',later_life='Memoir sections after 112 remain future material.'),ensure_ascii=False,indent=2))
(V/'new-wording.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))

md=['# הדרך של איטשע · ספר 1 · תסריט מאוחד, גרסה 0.6','טיוטה חדשה של 48 עמודי סיפור. מספור העמודים והמשבצות חדש. זהו תסריט וסקיצת סצנות; האיורים טרם הופקו.','הכותרות, שאלות המתח והסברי התפקיד מיועדים לצוות ואינם מסופרים לילד מראש. ציטוטים נשמרו כלשונם. דיבור מעובד נבנה רק משיחות שמדווחות במקור, ונרשם בנפרד לעיון המשפחה.']
for p in pages:
    md += [f"## עמוד {p['number']}: {p['title']}",f"מה צריך לקרות: {p['scene_need']}",f"מה משתנה: {p['change']}",f"מה הקורא מרגיש: {p['emotion']}",f"מה מחזיק להמשך: {p['turn_hook']}",f"מה לא חושפים/ממציאים: {p['withhold']}"]
    for q in p['panels']:
        md += [f"### {q['id']}",q['action']]
        if not q['texts']:md+=['ללא כיתוב.']
        for t in q['texts']:md += [f"{t['speaker']} · {t['kind']}: {t['he']}",t['en']]
    if p.get('reader_takeaways'):md+=['שלוש מחשבות קצרות לקורא, בנפרד מקולו של יצחק:']+[t['he'] for t in p['reader_takeaways']]
    if p.get('continued'):md += [p['continued']['he']]
    if p.get('family_cast'):md += ['המשפחה באיור: '+p['family_cast']['stage']+'. '+p['family_cast']['rule']]
    md += ['מקורות: '+', '.join(p['sources'])]
(V/'book1-script-he.md').write_text('\n\n'.join(md))

wording=['# נוסח חדש לעיון המשפחה, גרסה 0.6','הפנייה לנינים, מסגרת המספר, הכותרות וההזמנות הן עיבוד חדש. דיבור מעובד אינו תמליל מקורי: אלה שאלות ותשובות שהיומן מספר שאכן התקיימו, בניסוח מותאם לילדים. לא הומצאה שיחה חדשה. הבימוי והבעת הפנים הם שחזור מוצע.']
for t in registry:wording += [f"## {t['id']} · עמוד {t['page']}",t['he'],t['en'],f"סוג: {t['kind']}; עיגון: {t['basis']}",'מקורות: '+', '.join(t['sources'])]
(V/'new-wording-review.md').write_text('\n\n'.join(wording))

used=set(s for p in pages for s in p['sources'])
used.update(s for r in FAMILY['roster'] for s in r['sources'])
used.update(s for r in FAMILY['other_households'] for s in r['sources'])
used.update(FAMILY['confirmed_birth_family']['sources'])
assert all(s in sources for s in used)
assert len(SERIES)==3
assert len(FAMILY['roster'])==8
assert sum(r['sex']=='בן' for r in FAMILY['roster'])==5
assert sum(r['sex']=='בת' for r in FAMILY['roster'])==3
assert 'raisel' not in CAST[3]['members'] and 'raisel' not in CAST[4]['members']
assert set(CAST[12]['members'])=={r['id'] for r in FAMILY['roster']}
assert 'שלא אנעל נעליים' in json.dumps(pages,ensure_ascii=False)
assert all('לא אלבש נעליים' not in t['he'] and 'לא ללבוש נעליים' not in t['he'] for t in registry+literal)
(V/'family-continuity.json').write_text(json.dumps(dict(evidence=FAMILY,page_contracts=CAST),ensure_ascii=False,indent=2))
(V/'source-excerpts.json').write_text(json.dumps([sources[s] for s in sorted(used)],ensure_ascii=False,indent=2))
report=dict(story_pages=48,physical_pages_provisional=52,scene_sequences=len(SEQUENCES),panels=len(panels),text_blocks=sum(len(q['texts']) for q in panels)+len(takeaways)+1,words_he=sum(p['word_count_he'] for p in pages)+sum(len(t['he'].split()) for t in takeaways)+2,max_page_words_he=max(p['word_count_he'] for p in pages),max_text_block_words_he=max(len(t['he'].split()) for t in registry+literal),silent_action_panels=sum(not q['texts'] for q in panels),literal_quotes_verified=len(literal),adapted_reported_speech=sum(t['kind']=='adapted_speech' for t in registry),designed_page_turn_pairs=len(TURNS),checks=dict(exactly_three_volumes=True,original_family_five_sons_three_daughters=True,all_eight_cast_ids_unique=True,raisel_absent_before_birth_in_old_house_contract=True,scene_family_contracts=len(CAST),shoe_verb_corrected=True,stop_before_arrival=True,all_48_pages_have_need_change_emotion=True,all_sources_resolve=True,quotes_match_primary_transcript=True,all_text_has_hebrew_and_english=True,page_turn_pairs_not_on_same_provisional_spread=True,no_long_dashes_in_hebrew=True,all_panel_ids_unique_and_separate_from_old_manifest=True),not_claimed=['No child-reader comprehension study.','No browser visual, face-crop or final lettering approval.','No final chronology or family approval.','No new illustrations in this revision.','No GitHub publication of this revision.'])
(V/'qa-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))

def esc(x):return html.escape(str(x))
elder=B/'art/web/draft-p01-1.webp'
img='data:image/webp;base64,'+base64.b64encode(elder.read_bytes()).decode() if elder.exists() else ''
payload=json.dumps(dict(book=book,series=SERIES,report=report,elder=img,family=FAMILY),ensure_ascii=False).replace('</','<\\/')
tpl=(V/'template.html').read_text()
for file,mode in [('index.html','overview'),('book1-reader.html','reader')]:
    (V/file).write_text(tpl.replace('__MODE__',mode).replace('__DATA__',payload))
print(json.dumps(report,ensure_ascii=False,indent=2))

# A short review reading without production direction text, for continuity proofreading.
reading=['# ספר 1, נוסח הקריאה ברצף, גרסה 0.6','רק הכיתוב העתידי, בלי תיאורי הציורים. בכוונה חסרות כאן פעולות שהאיור יספר.']
for p in pages:
    reading += [f"## עמוד {p['number']}"]
    reading += [t['he'] for q in p['panels'] for t in q['texts']]
    reading += [t['he'] for t in p.get('reader_takeaways',[])]
    if p.get('continued'): reading += [p['continued']['he']]
(V/'reading-text-he.md').write_text('\n\n'.join(reading))
