#!/usr/bin/env python3
"""Download BLF stock photos from Pexels API."""
import json
import os
import urllib.parse
import urllib.request

KEY = "cs9nqVLS16pDC4ewzb2cdaHmJCahpvnWDkVLwfeJ3jIXdMBrVtauoTv7"
BASE = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/pexels"

SEARCHES = {
    "frozen_vegetables_processing": "frozen vegetables factory processing line",
    "matcha_tea_japanese": "matcha tea ceremony japanese traditional",
    "food_quality_lab": "food quality control laboratory testing",
    "cold_storage_logistics": "cold storage warehouse logistics frozen",
    "business_meeting_asian": "business meeting asian professional",
    "bamboo_basket_vegetables": "bamboo basket fresh vegetables asian market",
    "factory_workers_ppe": "factory workers protective equipment food processing",
    "certifications_food_safety": "food safety certification HACCP ISO badge",
}

os.makedirs(BASE, exist_ok=True)

results = []
for prefix, query in SEARCHES.items():
    search_url = "https://api.pexels.com/v1/search?query={}&per_page=5&orientation=landscape".format(
        urllib.parse.quote(query)
    )
    req = urllib.request.Request(search_url, headers={"Authorization": KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        results.append("{}: SEARCH_ERROR {}".format(prefix, e))
        continue

    photos = data.get("photos", [])
    if not photos:
        results.append("{}: NO_RESULTS".format(prefix))
        continue

    best = max(photos, key=lambda p: p["width"] * p["height"])
    img_url = best["src"]["original"]
    out_path = os.path.join(BASE, "{}_{}.jpg".format(prefix, best["id"]))

    try:
        urllib.request.urlretrieve(img_url, out_path)
        size_kb = os.path.getsize(out_path) // 1024
        results.append("{}: OK {} ({}KB, {}x{}, photographer={})".format(
            prefix, out_path, size_kb, best["width"], best["height"], best["photographer"]
        ))
    except Exception as e:
        results.append("{}: DOWNLOAD_ERROR {}".format(prefix, e))

for r in results:
    print(r)

</parameter>