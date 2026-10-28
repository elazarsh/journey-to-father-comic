#!/usr/bin/env python3
"""Turn a flat pure-green (#00FF00) background into transparency.
Usage: python chromakey.py art/raw/p01-n1.png art/p01-n1.png
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

def key(src, dst, lo=35.0, hi=110.0, margin=6):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    greenness = g - np.maximum(r, b)                      # how much greener than red/blue
    alpha = np.clip(1.0 - (greenness - lo) / (hi - lo), 0.0, 1.0)
    # remove green spill on edge pixels
    g2 = np.minimum(g, np.maximum(r, b) + 6.0)
    out = np.stack([r, np.where(greenness > 0, g2, g), b], axis=-1)
    alpha_img = Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    rgba = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).convert("RGBA")
    rgba.putalpha(alpha_img)
    bbox = alpha_img.point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        l, t, rr, bb = bbox
        rgba = rgba.crop((max(0, l - margin), max(0, t - margin), min(rgba.width, rr + margin), min(rgba.height, bb + margin)))
    rgba.save(dst)
    return rgba.size

if __name__ == "__main__":
    print(key(sys.argv[1], sys.argv[2]))
