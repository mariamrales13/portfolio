#!/usr/bin/env python3
"""
Adds width/height attributes to the freelance gallery images (class "fl-img")
so the page doesn't jump around while images load.

Usage (run from your project folder, the one that contains index.html and images/):
    pip install pillow
    python3 add-image-sizes.py            # edits index.html in place (makes index.html.bak first)
    python3 add-image-sizes.py --dry-run  # only prints what it would do

Safe to run more than once: images that already have width/height are skipped.
CSS already sets height:auto on .fl-img, so the images stay fully responsive.
"""
import re, sys, shutil
from pathlib import Path
from urllib.parse import unquote
from PIL import Image

dry = "--dry-run" in sys.argv
root = Path(__file__).resolve().parent
page = root / "index.html"
html = page.read_text(encoding="utf-8")

done = skipped = missing = 0

def fix(m):
    global done, skipped, missing
    tag = m.group(0)
    if 'class="fl-img' not in tag or re.search(r'\swidth=', tag):
        skipped += 1
        return tag
    src = re.search(r'\ssrc="([^"]+)"', tag)
    if not src:
        skipped += 1
        return tag
    file = root / unquote(src.group(1))
    if not file.exists():
        print(f"  missing file: {file.relative_to(root)}")
        missing += 1
        return tag
    with Image.open(file) as im:
        w, h = im.size
    done += 1
    print(f"  {file.relative_to(root)}  ->  {w}x{h}")
    return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)

new = re.sub(r"<img\b[^>]*>", fix, html)
print(f"\nupdated {done}, skipped {skipped}, missing {missing}")
if not dry and done:
    shutil.copy(page, root / "index.html.bak")
    page.write_text(new, encoding="utf-8")
    print("index.html updated (backup: index.html.bak)")
