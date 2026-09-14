#!/usr/bin/env python3
"""Download BLF stock photos from Pexels using compressed URLs."""
import json
import os
import urllib.request

BASE = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/stock_crawl"
os.makedirs(BASE, exist_ok=True)

# Curated best images from search results (compressed URLs that work without auth)
TARGETS = {
    "processing_line_asian": "https://images.pexels.com/photos/6711687/pexels-photo-6711687.jpeg?auto=compress&cs=tinysrgb&w=1280",
    "factory_worker_ppe": "https://images.pexels.com/photos/6711689/pexels-photo-6711689.jpeg?auto=compress&cs=tinysrgb&w=1280",
    "cold_storage_frozen": "https://images.pexels.com/photos/36201561/pexels-photo-36201561.jpeg?auto=compress&cs=tinysrgb&w=1280",
    "qc_lab_testing": "https://images.pexels.com/photos/11589239/pexels-photo-11589239.jpeg?auto=compress&cs=tinysrgb&w=1280",
    "matcha_tea_japanese": "https://images.pexels.com/photos/8951771/pexels-photo-8951771.jpeg?auto=compress&cs=tinysrgb&w=1280",
    "frozen_vegetables": "https://images.pexels.com/photos/24394699/pexels-photo-24394699.jpeg?auto=compress&cs=tinysrgb&w=1280",
    "food_processing_line": "https://images.pexels.com/photos/2889193/pexels-photo-2889193.jpeg?auto=compress&cs=tinysrgb&w=1280",
    "warehouse_logistics": "https://images.pexels.com/photos/5953713/pexels-photo-5953713.jpeg?auto=compress&cs=tinysrgb&w=1280",
}

results = []
for name, url in TARGETS.items():
    out_path = os.path.join(BASE, f"{name}.jpg")
    try:
        urllib.request.urlretrieve(url, out_path)
        size_kb = os.path.getsize(out_path) // 1024
        results.append(f"OK: {name}.jpg ({size_kb}KB)")
    except Exception as e:
        results.append(f"FAIL: {name} - {e}")

for r in results:
    print(r)

</parameter>