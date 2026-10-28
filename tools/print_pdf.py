"""Bind the sheets made by tools/print_pdf.js into A4 PDFs: a print master and a light copy for sharing.
Usage: python tools/print_pdf.py [he|en]"""
import sys, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
lang = sys.argv[1] if len(sys.argv) > 1 else 'he'
name = 'hagibor-sheli' if lang == 'he' else 'my-hero'
sheets = sorted((ROOT / 'print' / f'sheets-{lang}').glob('*.jpg'))
A4 = (2480, 3508)
for label, dpi, q in (('print', 300, 88), ('screen', 150, 80)):
    size = (A4[0] * dpi // 300, A4[1] * dpi // 300)
    pages = [Image.open(f).convert('RGB').resize(size, Image.LANCZOS) for f in sheets]
    out = ROOT / 'print' / f'{name}-A4-{label}.pdf'
    pages[0].save(out, save_all=True, append_images=pages[1:], resolution=dpi, quality=q)
    print(out.name, len(pages), 'pages', round(out.stat().st_size / 1e6, 1), 'MB')
