"""Generate panel images with the OpenAI image API (GPT image), for the v0.8 plan.
Reads a JSON list [{id, size, refs, prompt}], writes art/book1-v07/<id>.png (or <id>.v2.png when Codex art
already exists for that id, keeping the original), and a receipt in art/book1-v07/receipts/. Then run
refresh_art.py so progress.json and the web copies update. The key comes from OPENAI_API_KEY (never stored).
    python3 revisions/book1-v08/generate_images.py PROMPTS.json [--only ID,ID] [--workers 4] [--quality high]"""
import base64
import concurrent.futures as cf
import datetime
import hashlib
import json
import sys
from pathlib import Path

from openai import OpenAI

V = Path(__file__).resolve().parent
B = V.parents[1]
A = B / 'art/book1-v07'
MODEL = 'gpt-image-2'
args = sys.argv[1:]
items = json.loads(Path(args[0]).read_text(encoding='utf-8'))
only = set(args[args.index('--only') + 1].split(',')) if '--only' in args else None
workers = int(args[args.index('--workers') + 1]) if '--workers' in args else 4
quality = args[args.index('--quality') + 1] if '--quality' in args else 'high'
force = '--force' in args
client = OpenAI()


def one(it):
    pid = it['id']
    existing = (A / 'receipts' / f'{pid}.json').exists()
    stem = f'{pid}.v2' if existing else pid
    out = A / f'{stem}.png'
    if out.exists() and not force:
        return pid, 'skip (exists)'
    refs = [Path(r) for r in it.get('refs', []) if Path(r).exists()][:3]
    for attempt in range(3):
        try:
            if refs:
                files = [open(r, 'rb') for r in refs]
                try:
                    res = client.images.edit(model=MODEL, image=files, prompt=it['prompt'], size=it['size'], quality=quality)
                finally:
                    for f in files:
                        f.close()
            else:
                res = client.images.generate(model=MODEL, prompt=it['prompt'], size=it['size'], quality=quality)
            break
        except Exception as e:  # rate limits or transient errors: retry, then report
            err = str(e)
            if attempt == 2:
                return pid, 'error: ' + err[:300]
    raw = base64.b64decode(res.data[0].b64_json)
    out.write_bytes(raw)
    receipt = dict(id=pid, file=str(out.relative_to(B)), status='generated-claude-awaiting-review',
                   prompt=it['prompt'], tool=f'openai {MODEL} ({"edit" if refs else "generate"}, {quality})',
                   referenced_files=[str(r.relative_to(B)) if B in r.parents else str(r) for r in refs],
                   sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw),
                   created_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
    (A / 'receipts' / f'{stem}.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    return pid, 'ok ' + out.name


todo = [it for it in items if not only or it['id'] in only]
with cf.ThreadPoolExecutor(workers) as ex:
    for pid, status in ex.map(one, todo):
        print(pid, status, flush=True)
