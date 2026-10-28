"""Build the public website (site/) from viewer/index.html and the web-sized art.

The site holds only what a reader needs: the page and art/*.webp. Nothing from ref/,
production/ or handoffs/ is copied, so the private reference photo never leaves the repo.
Usage: python tools/build_site.py [base_url]
"""
import shutil, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
BASE = (sys.argv[1] if len(sys.argv) > 1 else 'https://elazarsh.github.io/hagibor-hanamuch/').rstrip('/') + '/'

body = (ROOT / 'viewer' / 'index.html').read_text(encoding='utf-8')
head = f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#070403">
<meta name="description" content="הגיבור שלי · המסע אל אבא. סיפור אמיתי בקומיקס מתוך סיפורי סבא עמנואל.">
<meta property="og:title" content="הגיבור שלי · המסע אל אבא">
<meta property="og:description" content="מרץ 1946. ילד בן שמונה וחצי יוצא לפגוש את אבא שמעולם לא ראה. סיפור אמיתי בקומיקס.">
<meta property="og:image" content="{BASE}art/p16-a.webp">
<meta property="og:type" content="website">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23170d06'/%3E%3Ccircle cx='32' cy='40' r='18' fill='%23f2c97a'/%3E%3Cpath d='M28 54h8l1-14h-10z M26 40l-6-10 2-1 7 10z M38 40l6-10-2-1-7 10z' fill='%23170d06'/%3E%3Ccircle cx='32' cy='35' r='3.5' fill='%23170d06'/%3E%3C/svg%3E">
'''
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
title_end = body.index('</title>') + len('</title>')
page = head + body[:title_end] + '\n</head>\n<body>\n' + body[title_end:] + '\n</body>\n</html>\n'
# the style block must be in the head for a clean first paint; it follows the title in the viewer source
page = page.replace('\n</head>\n<body>\n', '\n', 1)
style_end = page.index('</style>') + len('</style>')
page = page[:style_end] + '\n</head>\n<body>' + page[style_end:]

# the public book is for reading only: the layout studio and director mode stay in the private viewer
tools = '<div class="tools">'
assert page.count(tools) == 1
page = page.replace(tools, '<div class="tools" style="display:none" aria-hidden="true">')

if SITE.exists():
    shutil.rmtree(SITE)
(SITE / 'art').mkdir(parents=True)
(SITE / 'index.html').write_text(page, encoding='utf-8')
(SITE / '.nojekyll').write_text('', encoding='utf-8')
n = 0
for f in sorted((ROOT / 'art').glob('*.webp')):
    shutil.copy2(f, SITE / 'art' / f.name); n += 1
print(f'site/ ready: index.html + {n} images')
