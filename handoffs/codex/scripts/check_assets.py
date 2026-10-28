#!/usr/bin/env python3
"""Inventory contract checks. No claim of visual or crop correctness."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
panels = [p for page in manifest['pages'] for p in page['panels']]
missing = [p['file'] for p in panels if not (root / 'art' / p['file']).is_file()]
print(f"Pages: {len(manifest['pages'])}; expected images: {len(panels)}; missing: {len(missing)}")
for name in missing:
    print('MISSING', name)
try:
    from PIL import Image
except ImportError:
    print('Pillow unavailable: dimensions and alpha were not checked.')
else:
    mismatch = []
    layers_without_alpha = []
    for p in panels:
        path = root / 'art' / p['file']
        if not path.is_file():
            continue
        with Image.open(path) as im:
            expected = tuple(map(int, p['generate_size'].split('x')))
            if im.size != expected:
                mismatch.append((p['file'], im.size, expected))
            if p['kind'] == 'layer' and ('A' not in im.getbands() or im.getchannel('A').getextrema()[0] == 255):
                layers_without_alpha.append(p['file'])
    print(f'Dimension mismatches: {len(mismatch)}')
    for item in mismatch:
        print('SIZE', *item)
    print(f'Layers without transparency: {len(layers_without_alpha)}')
    for name in layers_without_alpha:
        print('ALPHA', name)
raise SystemExit(1 if missing else 0)
