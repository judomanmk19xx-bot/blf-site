#!/usr/bin/env python3
"""Download best preview (1500px) for final Asia/Vietnam-focused selection."""
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
data = urllib.parse.urlencode({"grant_type": "client_credentials",
                               "client_id": cid, "client_secret": csec}).encode()
req = urllib.request.Request("https://api.shutterstock.com/v2/oauth/access_token",
    data=data, headers={"Authorization": f"Basic {basic}",
                        "Content-Type": "application/x-www-form-urlencoded"})
token = json.loads(urllib.request.urlopen(req).read())["access_token"]
print("Token OK")

# Final selection: (semantic_name, shutterstock_id, rating, role)
SELECTION = [
    ("tea_plantation_vn",   "1048255066", 9, "About bento / hero — VN tea picker nón lá"),
    ("processing_line_iqf", "1932297077", 9, "Processing — frozen veg line, gloved inspection"),
    ("processing_intake",   "1932297074", 8, "Processing — raw intake, gowned worker"),
    ("qc_lab_asia",         "1009353163", 9, "Quality — Asian QC team hairnet+mask+gloves"),
    ("worker_qc_male",      "1859248447", 9, "OEM/QC — Asian male worker hairnet+mask"),
    ("worker_qc_female",    "1941853804", 9, "OEM/QC — Asian female inspecting bottles"),
    ("cold_storage_rack",   "158685212",  9, "Cold chain — pallet rack warehouse"),
    ("freezer_forklift",    "1548693137", 8, "Cold chain — forklift at freezer door"),
    ("port_aerial",         "1561887058", 9, "Logistics — full port aerial cranes"),
    ("port_containers",     "1553620877", 9, "Logistics — top-down containers teal sea"),
    ("tea_farm_walk",       "1286581306", 8, "Sourcing — worker walking tea rows"),
    ("tea_picker_highland", "1888614103", 7, "Sourcing — highland hand-pick basket"),
]

out_dir = "/Users/tringuyen/.buzz/OUTBOX/BLF_PROFILE/images/shutterstock/best_preview"
os.makedirs(out_dir, exist_ok=True)

manifest = []
for name, iid, rating, role in SELECTION:
    req = urllib.request.Request(f"https://api.shutterstock.com/v2/images/{iid}",
        headers={"Authorization": f"Bearer {token}"})
    info = json.loads(urllib.request.urlopen(req).read())
    assets = info.get("assets", {})
    # prefer preview_1500 (largest comp), fallback preview_1000, preview
    url = ""
    used = ""
    for key in ("preview_1500", "preview_1000", "preview"):
        u = assets.get(key, {}).get("url", "")
        if u:
            url, used = u, key
            break
    if not url:
        print(f"  ❌ {name}/{iid}: no preview URL")
        continue
    fname = f"{out_dir}/{name}.jpg"
    urllib.request.urlretrieve(url, fname)
    size = os.path.getsize(fname)
    w = assets.get(used, {}).get("width", "?")
    h = assets.get(used, {}).get("height", "?")
    manifest.append({"name": name, "id": iid, "rating": rating, "role": role,
                     "file": fname, "asset": used, "dims": f"{w}x{h}",
                     "size_kb": round(size/1024, 1)})
    print(f"  ✅ {name}: {w}x{h} {round(size/1024)}KB ({used})")

with open(f"{out_dir}/selection.json", "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\nDownloaded {len(manifest)}/{len(SELECTION)} → {out_dir}")
