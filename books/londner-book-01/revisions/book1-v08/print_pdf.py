"""Bind the A4 sheets from print_pdf.js into a print PDF (300dpi) and a light screen PDF (150dpi).
    python3 revisions/book1-v08/print_pdf.py OUT_DIR"""
import glob
import os
import sys

from PIL import Image

out = sys.argv[1]
files = sorted(glob.glob(os.path.join(out, 'sheet-*.jpg')))
A4 = (2480, 3508)
for name, dpi, q in (('londner-book1-A4-print.pdf', 300, 88), ('londner-book1-A4-screen.pdf', 150, 70)):
    size = (A4[0] * dpi // 300, A4[1] * dpi // 300)
    pages = []
    for f in files:
        im = Image.open(f).convert('RGB')
        pages.append(im.resize(size, Image.LANCZOS))
    path = os.path.join(out, name)
    pages[0].save(path, save_all=True, append_images=pages[1:], resolution=dpi, quality=q)
    print(name, len(pages), 'pages', round(os.path.getsize(path) / 1e6, 1), 'MB')
