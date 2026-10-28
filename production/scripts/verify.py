#!/usr/bin/env python3
"""Check that every file in manifest.json exists and has the right shape.
Usage: python verify.py manifest.json art
"""
import json, os, sys
from PIL import Image

manifest = json.load(open(sys.argv[1], encoding="utf-8"))
art = sys.argv[2] if len(sys.argv) > 2 else "art"
missing, bad, ok = [], [], 0
for page in manifest["pages"]:
    for it in page["panels"]:
        name = it["file"]
        cands = [os.path.join(art, name)] if name.endswith(".png") else [os.path.join(art, name + e) for e in (".png", ".webp", ".jpg")]
        path = next((c for c in cands if os.path.exists(c)), None)
        if not path:
            missing.append(name); continue
        im = Image.open(path)
        want_w, want_h = [int(v) for v in it["generate_size"].split("x")]
        if it["kind"] == "layer":
            if im.mode != "RGBA":
                bad.append((name, "layer must be RGBA with transparency")); continue
            alpha = im.getchannel("A").getextrema()
            if alpha[0] > 5:
                bad.append((name, "layer has no transparent pixels")); continue
        else:
            ratio = im.width / im.height
            if abs(ratio - want_w / want_h) > 0.03:
                bad.append((name, f"aspect {ratio:.2f}, expected {want_w/want_h:.2f}")); continue
        ok += 1
print(f"ok: {ok}")
print(f"missing ({len(missing)}):", ", ".join(missing) or "none")
for n, why in bad:
    print("problem:", n, "-", why)
