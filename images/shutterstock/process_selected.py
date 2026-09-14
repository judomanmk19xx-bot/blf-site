#!/usr/bin/env python3
"""Upscale selected previews 2x with sips (Lanczos) and copy to website assets."""
import os, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
PREV = os.path.join(HERE, "previews")
OUT = os.path.join(os.path.dirname(HERE), "shutterstock_web")  # images/shutterstock_web
os.makedirs(OUT, exist_ok=True)

# (source_file, target_name, rating, category)
SELECTED = [
    ("hero_factory_1866104743.jpg",   "hero_factory.jpg",      9, "hero_factory"),
    ("hero_factory_742464493.jpg",    "factory_workers.jpg",   7, "hero_factory"),
    ("processing_line_1866104704.jpg","processing_line.jpg",   9, "processing_line"),
    ("processing_line_1586691571.jpg","processing_worker.jpg", 8, "processing_line"),
    ("qc_lab_1879621333.jpg",         "qc_lab.jpg",           10, "qc_lab"),
    ("qc_lab_1586690878.jpg",         "qc_inspection.jpg",     9, "qc_lab"),
    ("cold_storage_1616446483.jpg",   "cold_storage.jpg",      9, "cold_storage"),
    ("matcha_tea_390544690.jpg",      "matcha.jpg",           10, "matcha_tea"),
    ("matcha_tea_1863922717.jpg",     "matcha_whisk.jpg",      9, "matcha_tea"),
]

def dims(p):
    out = subprocess.check_output(["sips", "-g", "pixelWidth", "-g", "pixelHeight", p]).decode()
    w = int([l for l in out.splitlines() if "pixelWidth" in l][0].split()[-1])
    h = int([l for l in out.splitlines() if "pixelHeight" in l][0].split()[-1])
    return w, h

print(f"ImageMagick available: {shutil.which('magick') or shutil.which('convert') or 'NO (using sips)'}")
results = []
for src, tgt, rating, cat in SELECTED:
    sp = os.path.join(PREV, src)
    tp = os.path.join(OUT, tgt)
    shutil.copy(sp, tp)
    w, h = dims(tp)
    # 2x upscale via sips Lanczos resampling
    subprocess.check_call(["sips", "--resampleWidth", str(w * 2),
                           "--resampleHeight", str(h * 2), tp],
                          stdout=subprocess.DEVNULL)
    w2, h2 = dims(tp)
    kb = os.path.getsize(tp) // 1024
    results.append((tgt, cat, rating, f"{w}x{h}", f"{w2}x{h2}", kb))
    print(f"OK {tgt:24s} {cat:16s} rating={rating:2d}  {w}x{h} -> {w2}x{h2}  {kb}KB")

print(f"\n{len(results)} images processed -> {OUT}")