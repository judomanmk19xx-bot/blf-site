#!/usr/bin/env python3
"""Shutterstock search round 4: tight keywords per Thầy's direction.
Strategy: product studio shots ('white background'), ethnicity filter for
Asian workers, exclude_keywords to kill cooked/retail noise."""
import json, os, urllib.request, urllib.parse, base64

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
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    return json.loads(urllib.request.urlopen(req).read())

ASIA = ["southeast_asian", "east_asian"]

# Each entry: q=query, eth=ethnicity filter (optional), ex=exclude_keywords
QUERIES = {
    "prod_eggplant": [
        {"q": "eggplant white background"},
        {"q": "fresh eggplants basket harvest"},
    ],
    "prod_sweetpotato": [
        {"q": "sweet potato white background"},
        {"q": "sweet potatoes harvest basket farm"},
    ],
    "prod_okra": [
        {"q": "okra white background"},
        {"q": "fresh okra pods market"},
    ],
    "prod_bellpepper": [
        {"q": "bell peppers white background"},
        {"q": "red yellow bell peppers crate harvest"},
    ],
    "prod_zucchini": [
        {"q": "zucchini white background"},
        {"q": "fresh zucchini crate harvest farm"},
    ],
    "prod_frozen_mix": [
        {"q": "frozen vegetables mix bowl"},
        {"q": "frozen vegetables package factory"},
    ],
    "processing_asia": [
        {"q": "vegetable processing factory workers hairnet gloves", "eth": ASIA, "ex": ["tomato"]},
        {"q": "food factory workers asia conveyor vegetables", "ex": ["solar", "aquaponic"]},
        {"q": "vegetable sorting factory conveyor belt workers"},
    ],
    "qc_lab_asia": [
        {"q": "food quality control laboratory technician asia", "eth": ASIA},
        {"q": "asian scientist food laboratory white coat gloves"},
    ],
    "cold_storage": [
        {"q": "frozen food warehouse pallets worker jacket", "ex": ["supermarket", "grocery"]},
        {"q": "cold storage warehouse industrial pallets frozen", "ex": ["supermarket", "retail"]},
    ],
    "tea_vietnam": [
        {"q": "vietnam tea plantation farmer harvesting"},
        {"q": "tea plantation hills vietnam workers"},
        {"q": "green tea processing factory asia"},
    ],
    "port_vietnam": [
        {"q": "vietnam container port aerial"},
        {"q": "ho chi minh city port container ship"},
    ],
    "factory_exterior": [
        {"q": "food factory building exterior asia"},
        {"q": "factory building vietnam industrial exterior"},
    ],
}

out_dir = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/shutterstock/previews_v4"
os.makedirs(out_dir, exist_ok=True)

all_results = {}
seen_global = set()
for cat, qlist in QUERIES.items():
    all_results[cat] = []
    for spec in qlist:
        if len(all_results[cat]) >= 8:
            break
        params = {"query": spec["q"], "per_page": 10, "image_type": "photo"}
        if spec.get("eth"):
            params["ethnicity"] = spec["eth"]
        if spec.get("ex"):
            params["exclude_keywords"] = ",".join(spec["ex"])
        try:
            r = api_get("/v2/images/search", params)
        except Exception as e:
            # retry without ethnicity if param rejected
            params.pop("ethnicity", None)
            try:
                r = api_get("/v2/images/search", params)
            except Exception as e2:
                print(f"  ❌ search '{spec['q']}': {e2}")
                continue
        for item in r.get("data", []):
            iid = str(item["id"])
            if iid in seen_global:
                continue
            seen_global.add(iid)
            desc = item.get("description", "")[:100]
            preview = item.get("assets", {}).get("preview", {}).get("url", "")
            if not preview:
                continue
            fname = f"{out_dir}/{cat}_{iid}.jpg"
            try:
                urllib.request.urlretrieve(preview, fname)
                size = os.path.getsize(fname)
                all_results[cat].append({
                    "id": iid, "file": fname, "query": spec["q"],
                    "size_kb": round(size/1024, 1), "desc": desc
                })
                print(f"  ✅ {cat}/{iid}: {desc[:60]}")
            except Exception as e:
                print(f"  ❌ dl {iid}: {e}")
            if len(all_results[cat]) >= 8:
                break
    print(f"{cat}: {len(all_results[cat])} images")

manifest = f"{out_dir}/manifest_v4.json"
with open(manifest, "w") as f:
    json.dump(all_results, f, indent=2)
total = sum(len(v) for v in all_results.values())
print(f"\nTOTAL: {total} previews → {out_dir}")
print(f"Manifest: {manifest}")
