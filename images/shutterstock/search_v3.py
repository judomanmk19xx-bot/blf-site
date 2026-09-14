#!/usr/bin/env python3
"""Shutterstock search round 3: BLF real products (Thầy's keywords) + VN/Asia factory scenes.
Fix: sort=relevance (best_match is invalid enum -> 400)."""
import json, os, urllib.request, urllib.parse, base64

BASE = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/shutterstock"
creds = {}
with open(f"{BASE}/.env") as f:
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
        "client_id": cid, "client_secret": csec}).encode()
    req = urllib.request.Request(
        "https://api.shutterstock.com/v2/oauth/access_token", data=data,
        headers={"Authorization": f"Basic {basic}",
                 "Content-Type": "application/x-www-form-urlencoded"})
    return json.loads(urllib.request.urlopen(req).read())["access_token"]

token = get_token()
print(f"Token OK: {token[:12]}...")

def api_get(path, params):
    url = f"https://api.shutterstock.com{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    return json.loads(urllib.request.urlopen(req).read())

# BLF real frozen-vegetable products (Thầy's keywords) + VN/Asia scenes
QUERIES = {
    # --- BLF products (Thầy dictating) ---
    "prod_eggplant": ["japanese eggplant fresh", "asian eggplant vegetable market"],
    "prod_sweetpotato": ["japanese sweet potato", "sweet potato harvest farm"],
    "prod_okra": ["fresh okra vegetable", "okra pods green"],
    "prod_bellpepper": ["red bell pepper fresh", "bell peppers colorful"],
    "prod_zucchini": ["zucchini courgette fresh", "zucchini vegetable"],
    # --- VN/Asia factory scenes ---
    "shrimp_processing": ["shrimp processing factory workers gloves",
                          "seafood processing asia factory workers"],
    "veg_processing_asia": ["vegetable processing factory asian workers hairnet",
                            "food processing factory workers conveyor vegetables asia"],
    "qc_lab_asia": ["asian food quality control laboratory",
                    "food testing laboratory technician asia"],
    "tea_vietnam": ["vietnam tea plantation harvest", "green tea production asia"],
    "port_vietnam": ["container port vietnam", "container ship port aerial cranes"],
    "cold_storage": ["cold storage warehouse frozen food",
                     "industrial freezer warehouse pallets"],
}

out_dir = f"{BASE}/previews_v3"
os.makedirs(out_dir, exist_ok=True)
PER_CAT = 6

all_results = {}
for cat, queries in QUERIES.items():
    all_results[cat] = []
    seen = set()
    for q in queries:
        if len(all_results[cat]) >= PER_CAT:
            break
        try:
            r = api_get("/v2/images/search", {
                "query": q, "per_page": 10, "sort": "relevance",
                "image_type": "photo"})
            print(f"[{cat}] '{q}' -> {r.get('total_count')} total")
            for item in r.get("data", []):
                iid = str(item["id"])
                if iid in seen:
                    continue
                seen.add(iid)
                preview = item.get("assets", {}).get("preview", {}).get("url", "")
                if not preview:
                    continue
                fname = f"{out_dir}/{cat}_{iid}.jpg"
                try:
                    urllib.request.urlretrieve(preview, fname)
                    all_results[cat].append({
                        "id": iid, "file": fname, "query": q,
                        "size_kb": round(os.path.getsize(fname)/1024, 1),
                        "desc": item.get("description", "")[:120]})
                except Exception as e:
                    print(f"  dl fail {iid}: {e}")
                if len(all_results[cat]) >= PER_CAT:
                    break
        except Exception as e:
            print(f"[{cat}] search fail '{q}': {e}")
    print(f"  => {cat}: {len(all_results[cat])} previews")

with open(f"{out_dir}/manifest_v3.json", "w") as f:
    json.dump(all_results, f, indent=2)
total = sum(len(v) for v in all_results.values())
print(f"\nTOTAL: {total} previews -> {out_dir}")
