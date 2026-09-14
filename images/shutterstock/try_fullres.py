#!/usr/bin/env python3
"""Attempt full-res licensing via Shutterstock API for top-selected images."""
import base64, json, os, sys, urllib.request, urllib.parse, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, ".env")) as f:
    for line in f:
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

CID = os.environ["SHUTTERSTOCK_CLIENT_ID"]
SEC = os.environ["SHUTTERSTOCK_CLIENT_SECRET"]
BASE = "https://api.shutterstock.com/v2"

CANDIDATES = ["1866104704", "1879621333", "1616446483", "390544690",
              "1866104743", "1586691571", "1586690878", "742464493", "1863922717"]

basic = base64.b64encode(f"{CID}:{SEC}".encode()).decode()
req = urllib.request.Request(
    BASE + "/oauth/access_token",
    data=urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CID,
        "client_secret": SEC,
    }).encode(),
    headers={"Authorization": "Basic " + basic,
             "Content-Type": "application/x-www-form-urlencoded",
             "Accept": "application/json"},
    method="POST")
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        token = json.loads(r.read())["access_token"]
    print("AUTH OK")
except urllib.error.HTTPError as e:
    print(f"AUTH FAILED HTTP {e.code}: {e.read().decode()[:200]}")
    sys.exit(1)

ok_any = False
for img_id in CANDIDATES:
    body = json.dumps({"images": [{"image_id": img_id}]}).encode()
    req = urllib.request.Request(
        BASE + "/images/licenses",
        data=body,
        headers={"Authorization": "Bearer " + token,
                 "Content-Type": "application/json",
                 "Accept": "application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        print(f"{img_id}: LICENSED -> {json.dumps(data)[:150]}")
        ok_any = True
    except urllib.error.HTTPError as e:
        print(f"{img_id}: FAILED HTTP {e.code} {e.read().decode()[:150]}")

print("FULLRES_OK" if ok_any else "FULLRES_UNAVAILABLE -> using highest-res previews")