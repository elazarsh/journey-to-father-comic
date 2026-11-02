"""Register selected native imagegen output without modifying original pixels."""
import datetime, hashlib, json, shutil, sys
from pathlib import Path
from PIL import Image
B = Path(__file__).resolve().parents[2]
D = B / 'art/book1-v08-corrections'
for task in json.loads(Path(sys.argv[1]).read_text()):
    folder = 'characters' if task['kind'] == 'character-reference' else 'panels' if task.get('target') else 'extras'
    dest = D / folder / (task['id']+'.png')
    dest.parent.mkdir(parents=True, exist_ok=True)
    source = Path(task['source'])
    refs = [{'file':str(Path(p).relative_to(B)) if Path(p).is_relative_to(B) else p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in task.get('refs',[])]
    shutil.copyfile(source, dest)
    assert source.read_bytes() == dest.read_bytes()
    with Image.open(dest) as im:
        im.load(); size = list(im.size); mode = im.mode
        web = dest.with_suffix('.webp'); im.save(web, 'WEBP', quality=88, method=5)
    receipt = {**{k:v for k,v in task.items() if k not in ['source','refs']},'file':str(dest.relative_to(B)),'web_file':str(web.relative_to(B)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'web_sha256':hashlib.sha256(web.read_bytes()).hexdigest(),'actual_size':size,'mode':mode,'original_generation_path':str(source),'generation_tool':'image_gen.imagegen','references':refs,'status':'generated-candidate-for-Claude-integration','family_approved':False,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    out=D/'receipts'/(task['id']+'.json');out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(task['id'],receipt['file'])
