"""Hash-bind manually inspected protection candidates; never updates production faces.json."""
import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parents[3];Q=Path(__file__).resolve().parent
assets={a['id']:a for a in json.loads((B/'art/book1-v07/progress.json').read_text())['assets']};faces=json.loads((B/'revisions/book1-v08/faces.json').read_text())
specs={
'B01V07-P36-01':dict(head_rects=[[41,43,11,16]],hand_prop_rects=[[45,59,10,32]],quiet_source_rects=[[54,3,37,20]],finding='Current wide night scene: Yitzhak head is lower-center, not the old face box at x51.5 y25.9 w19.6 h13. Old faces.json is stale for this replacement.'),
'B01V07-P38-03':dict(head_rects=[[10,17,20,34],[30,12,13,26],[42,19,10,22],[50,21,13,24],[61,18,13,25],[72,20,20,30]],hand_prop_rects=[[16,56,72,25]],quiet_source_rects=[],finding='Six complete heads and two male speakers are present in full source. Narrow cover crop clips both male speakers. Reserve lettering in renderer space with contain; do not make daughters into speakers.'),
'B01V07-P38-04':dict(head_rects=[[20,11,24,40]],hand_prop_rects=[[29,44,17,26]],quiet_source_rects=[[61,3,22,20]],finding='Chava is the focus. Henich speech comes from off-panel right/edge. Set explicit offPanel=true; skip nearest-face matching; proposed mouth [1.02,.38] in normalized final panel space, mirrored to[-.02,.38] in English. Suggested bubble zone [60,3,36,19] percent of final panel, pending text metrics.'),
'B01V07-P21-01':dict(head_rects=[[37,10,18,30]],hand_prop_rects=[[34,61,12,13],[71,25,9,10],[38,52,62,45]],quiet_source_rects=[],finding='Essential head + two hands + open crate span most of source height. Present short strip cannot preserve them at legible size by object-position alone. Increase slot height or use contain as temporary diagnostic.'),
'B01V07-P28-04':dict(head_rects=[[60,3,17,25],[10,39,20,31]],hand_prop_rects=[[43,17,9,21],[83,70,10,7],[50,66,24,21]],quiet_source_rects=[],finding='Speaker head at top of original source is cut by cover crop. Even fy=0/zoom1 intersects slanted mask; contain .92 is safer. Keep collecting box and raised hand.'),
'B01V07-P26-04':dict(head_rects=[],hand_prop_rects=[[0,4,34,43],[67,0,33,36],[17,19,66,51]],quiet_source_rects=[],finding='Current source is hands choosing fabric swatches, no face. Existing faces.json entry at x54.7 y19.2 w11.6 h23.5 belongs to superseded source.'),
'B01V07-P27-01':dict(head_rects=[],hand_prop_rects=[[40,7,35,24],[9,24,86,70]],quiet_source_rects=[],finding='Current source is a hand carrying sample case; no head in the depicted detail. Existing faces.json entry at x50.9 y29.4 w15.8 h12.7 belongs to superseded source.')}
out=[]
for pid,sp in specs.items():
 a=assets[pid];p=B/a['file'];p=p if p.exists() else B/a['web_file']
 out.append(dict(id=pid,sourceSHA=a['sha256'],reviewed_input=str(p.relative_to(B)),reviewed_input_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),existing_unbound_faces=faces.get(pid),coordinates='percent x,y,w,h of full source; manually estimated conservative candidate regions, not detector output',**sp))
(Q/'manual-protection-candidates.json').write_text(json.dumps(dict(created_utc=datetime.now(timezone.utc).isoformat(),note='Source review only, not final lettering clearance. Empty head_rects describes visible current detail, not a claim that automated absence proves safety. No production face map was modified.',panels=out),indent=2))
print(len(out),'source-bound manual protection records')
