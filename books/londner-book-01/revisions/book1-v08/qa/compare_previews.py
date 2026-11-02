"""Lossy preview correspondence, read only; no image rewriting."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
B=Path(__file__).resolve().parents[3];Q=Path(__file__).resolve().parent
p=json.loads((B/'art/book1-v07/progress.json').read_text());rows=[]
for a in p['assets']:
 s=B/a['file'];w=B/a['web_file']
 if not s.exists() or not w.exists():continue
 im=Image.open(s).convert('RGB').resize((160,160),Image.Resampling.LANCZOS);web=Image.open(w).convert('RGB').resize((160,160),Image.Resampling.LANCZOS)
 mae=float(np.abs(np.array(im,dtype=float)-np.array(web,dtype=float)).mean())
 rows.append(dict(id=a['id'],rgb_mean_absolute_error_0_255=round(mae,3),potential_stale_preview=mae>10))
(Q/'preview-correspondence.json').write_text(json.dumps(rows,indent=2));print('Compared',len(rows),'local source/preview pairs');print(json.dumps([r for r in rows if r['potential_stale_preview']],indent=2))
