from pathlib import Path
import hashlib, json, re, subprocess, tempfile
from PIL import Image

B = Path(__file__).resolve().parents[1]
book = json.loads((B / 'production/book.json').read_text())
manifest = json.loads((B / 'production/manifest.json').read_text())
assets = manifest['images']
original = json.loads((B / 'research/script-v01.json').read_text())
assert len(book['pages']) == 32
assert len(assets) == 89
assert len({a['id'] for a in assets}) == 89
texts = [t for p in book['pages'] for q in p['panels'] for t in q['texts']]
before = [t for p in original['pages'] for q in p['panels'] for t in q['texts']]
assert [(t['he'], t['en']) for t in texts] == [(t['he'], t['en']) for t in before]
assert len(texts) == 112
assert sum(t['status'] == 'quote' for t in texts) == 14
assert [t['he'] for t in book['opening']] == ['מי היה סבא, לפני שהיה סבא?', 'המחברת שלו פותחת לנו דלת.']
assert len(book['backcover']) == 2
generated = []
for a in assets:
    g = a['geometry']
    assert 0 <= g['x'] < g['x'] + g['w'] <= 100.001
    assert 0 <= g['y'] < g['y'] + g['h'] <= 140.001
    for x, y in g['polygon']:
        assert 0 <= x <= 100 and 0 <= y <= 100
    for key in ['caption_zone', 'protected_target_zone']:
        x, y, w, h = g[key]
        assert 0 <= x < x+w <= 100.001 and 0 <= y < y+h <= 100.001
    if a['status'].startswith('generated'):
        src = B / a['file']
        assert src.exists() and (B / a['web_file']).exists()
        assert hashlib.sha256(src.read_bytes()).hexdigest() == a['sha256']
        with Image.open(src) as im:
            assert list(im.size) == a['actual_size']
        generated.append(a['id'])
    assert not a['file'].startswith('art/rejected/')
for rel in ['production/structure.html', 'viewer/index.html']:
    html = (B / rel).read_text()
    assert not re.search(r'__(BOOK|ASSET|FILES|CHAR|DEFAULT)_', html)
    assert '.picture{position:absolute;inset:0}' in html
    js = re.search(r'<script>([\s\S]*?)</script>', html).group(1)
    with tempfile.NamedTemporaryFile(suffix='.js', mode='w') as f:
        f.write(js)
        f.flush()
        subprocess.run(['node', '--check', f.name], check=True, capture_output=True)
    filemap = json.loads(re.search(r'const files=(.*?);\n', js).group(1))
    for target in filemap.values():
        assert ((B / rel).parent / target).resolve().exists(), target
report = dict(story_pages=32, panels=89, image_panels=sum(a['kind']=='panel' for a in assets),
              graphic_panels=sum(a['kind']=='graphic' for a in assets), text_blocks=112,
              unchanged_story_text=True, preserved_quotes=14, new_opening_and_backcover_lines=4,
              generated_current_batch=generated, javascript_syntax='passed',
              geometry_bounds='passed', local_asset_links='passed',
              browser_visual_qa='not run: Chromium blocked by environment setsockopt restriction',
              github_upload='See production/github-receipt.json for verified remote upload status')
(B / 'production/qa-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps(report, ensure_ascii=False, indent=2))
