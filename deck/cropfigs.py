"""Tight-crop every figure to its ink, keeping a fixed margin, so slide layout is exact."""
from PIL import Image, ImageChops
import glob, os
for p in sorted(glob.glob("figures/*.png")):
    im = Image.open(p).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        m = 12
        b = (max(0, bbox[0]-m), max(0, bbox[1]-m),
             min(im.width, bbox[2]+m), min(im.height, bbox[3]+m))
        im.crop(b).save(p)
        print(f"{os.path.basename(p):20s} {im.size} -> {Image.open(p).size}")
