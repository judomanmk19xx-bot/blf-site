#!/usr/bin/env python3
"""Shutterstock search round 2: Vietnam/Asia-focused images for BLF website."""
import json, os, sys, urllib.request, urllib.parse, base64

ENV = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/shutterstock/.env"
creds = {}
with open(ENV) as f:
    for line in f:
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            creds[k.strip()] = v.strip()

cid, csec = creds["SHUTTERSTOCK_CLIENT_ID"], creds["SHUTTERSTOCK_CLIENT_SECRET"]
basic = base64.b64encode(f"{cid}:{csec}".encode()).decode()

def get_token():
    data = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": cid, "client_secret": csec
    }).encode()
    req = urllib.request.Request(
        "https://api.shutterstock.com/v2/oauth/access_token",
        data=data,
        headers={"Authorization": f"Basic {basic}",
                 "Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(urllib.request.urlopen(req).read())["access_token"]

token = get_token()
print(f"Token OK: {token[:15]}...")

def api_get(path, params=None):
    url = f"https://api.shutterstock.com{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    return json.loads(urllib.request.urlopen(req).read())

# Vietnam/Asia-focused queries per category (verified counts 2026-08-22)
QUERIES = {
    "shrimp_processing": [
        "shrimp processing",
        "seafood processing workers gloves",
        "shrimp factory workers",
    ],
    "vegetable_processing": [
        "asian food factory",
        "food factory workers asia conveyor",
        "vegetable factory workers hairnet asia",
    ],
    "qc_lab_asia": [
        "asian scientist laboratory food",
        "food quality control laboratory asia",
        "asian laboratory technician microscope",
    ],
    "tea_production": [
        "vietnam tea plantation",
        "tea plantation workers asia harvesting",
        "green tea processing factory",
    ],
    "port_logistics": [
        "ho chi minh city port containers",
        "vietnam port container ship",
        "container port aerial cranes",
    ],
    "cold_storage_asia": [
        "cold storage warehouse frozen",
        "frozen food warehouse workers",
        "industrial cold storage pallets",
    ],
}

out_dir = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/shutterstock/previews_v2"
os.makedirs(out_dir, exist_ok=True)

all_results = {}
for cat, queries in QUERIES.items():
    all_results[cat] = []
    seen_ids = set()
    for q in queries:
        if len(all_results[cat]) >= 6:
            break
        try:
            r = api_get("/v2/images/search", {
                "query": q, "per_page": 10,
                "image_type": "photo",  # photos only, no illustrations/AI
            })
            for item in r.get("data", []):
                iid = str(item["id"])
                if iid in seen_ids:
                    continue
                seen_ids.add(iid)
                desc = item.get("description", "")[:100]
                preview = item.get("assets", {}).get("preview", {}).get("url", "")
                if not preview:
                    continue
                fname = f"{out_dir}/{cat}_{iid}.jpg"
                try:
                    urllib.request.urlretrieve(preview, fname)
                    size = os.path.getsize(fname)
                    all_results[cat].append({
                        "id": iid, "file": fname, "query": q,
                        "size_kb": round(size/1024, 1), "desc": desc
                    })
                    print(f"  ✅ {cat}/{iid}: {desc[:60]}")
                except Exception as e:
                    print(f"  ❌ dl {iid}: {e}")
                if len(all_results[cat]) >= 6:
                    break
        except Exception as e:
            print(f"  ❌ search '{q}': {e}")
    print(f"{cat}: {len(all_results[cat])} images")

manifest = f"{out_dir}/manifest_v2.json"
with open(manifest, "w") as f:
    json.dump(all_results, f, indent=2)
total = sum(len(v) for v in all_results.values())
print(f"\nTOTAL: {total} previews → {out_dir}")
print(f"Manifest: {manifest}")
