#!/usr/bin/env python3
"""Shutterstock API v2 integration for BLF website stock images.

Auth flow (per Shutterstock docs):
  1. POST /v2/oauth/access_token
     - Header: Authorization: Basic base64(client_id:client_secret)
     - Body:   grant_type=client_credentials
  2. Use returned Bearer token for all /v2 endpoints.

Endpoints:
  - Search:   GET  /v2/images/search?query=...&per_page=5
  - Subs:     GET  /v2/user/subscriptions  (to find subscription_id)
  - License:  POST /v2/images/licenses  body {"images":[{"image_id","subscription_id"}]}

Credentials are read from .env in this directory (never hardcoded/printed).
Search is free; licensing/downloading requires an active paid subscription.
"""
import base64
import datetime
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- load .env ----
env_path = os.path.join(HERE, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

CLIENT_ID = os.environ.get("SHUTTERSTOCK_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SHUTTERSTOCK_CLIENT_SECRET", "")
SUBSCRIPTION_ID = os.environ.get("SHUTTERSTOCK_SUBSCRIPTION_ID", "")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: set SHUTTERSTOCK_CLIENT_ID / SHUTTERSTOCK_CLIENT_SECRET in .env")
    sys.exit(1)

BASE = "https://api.shutterstock.com/v2"
OUT_DIR = HERE
RESULTS_PATH = os.path.join(OUT_DIR, "results.json")

SEARCHES = {
    "processing_line": (
        "frozen vegetables factory processing line "
        "workers PPE stainless steel asia"
    ),
    "qc_lab": (
        "food quality control laboratory testing "
        "HACCP scientist white coat"
    ),
    "cold_storage": (
        "cold storage warehouse frozen food "
        "pallets frost temperature"
    ),
    "matcha_tea": (
        "matcha tea ceremony japanese "
        "traditional bamboo whisk"
    ),
    "hero_factory": (
        "food processing factory exterior "
        "asia modern building"
    ),
}


def mask(s):
    return s[:4] + "***" if s else "(empty)"


def http_error_body(exc):
    try:
        return exc.read().decode()[:300]
    except Exception:
        return ""


def get_access_token():
    """OAuth2 client_credentials flow with Basic auth header."""
    basic = base64.b64encode(
        "{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode()
    ).decode()
    req = urllib.request.Request(
        BASE + "/oauth/access_token",
        data=urllib.parse.urlencode(
            {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
            }
        ).encode(),
        headers={
            "Authorization": "Basic " + basic,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def api_get(path, token):
    req = urllib.request.Request(
        BASE + path,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def search_images(token, query, per_page=5):
    q = urllib.parse.quote(query)
    path = (
        "/images/search?query={}&per_page={}"
        "&image_type=photo&orientation=horizontal"
    ).format(q, per_page)
    return api_get(path, token)


def get_subscriptions(token):
    return api_get("/user/subscriptions", token)


def license_image(token, image_id, subscription_id):
    """POST /v2/images/licenses -> returns download url for full-res image."""
    body = json.dumps(
        {
            "images": [
                {
                    "image_id": str(image_id),
                    "subscription_id": subscription_id,
                }
            ]
        }
    ).encode()
    req = urllib.request.Request(
        BASE + "/images/licenses",
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def main():
    print("Auth: client_id={} secret={}".format(
        mask(CLIENT_ID), mask(CLIENT_SECRET)))
    try:
        tok = get_access_token()
    except urllib.error.HTTPError as e:
        print("AUTH FAILED: HTTP {} {}".format(e.code, http_error_body(e)))
        sys.exit(2)
    token = tok.get("access_token", "")
    if not token:
        print("AUTH FAILED: no access_token in response")
        sys.exit(2)
    print("AUTH OK (token acquired, not printed)")

    results = {
        "generated_at": datetime.datetime.now().isoformat(),
        "auth": "oauth2_client_credentials",
        "categories": {},
        "summary": {},
    }

    # try to discover subscription id (needed for licensing/downloads)
    subs_info = None
    try:
        subs_info = get_subscriptions(token)
    except urllib.error.HTTPError as e:
        subs_info = {"error": "HTTP {} {}".format(e.code, http_error_body(e))}
    except Exception as e:
        subs_info = {"error": str(e)}
    results["subscriptions"] = subs_info

    lines = []
    ok = 0
    for cat, query in SEARCHES.items():
        entry = {"query": query}
        try:
            data = search_images(token, query)
            photos = data.get("data", [])
            entry["total_found"] = data.get("total_count", 0)
            entry["results"] = [
                {
                    "id": ph.get("id"),
                    "description": ph.get("description", "")[:120],
                    "preview_url": ph.get("assets", {})
                    .get("preview", {})
                    .get("url", ""),
                    "thumb_url": ph.get("assets", {})
                    .get("small_thumb", {})
                    .get("url", ""),
                }
                for ph in photos
            ]
            lines.append("{}: {} results (total_available={})".format(
                cat, len(photos), entry["total_found"]))
            ok += 1
        except urllib.error.HTTPError as e:
            entry["error"] = "HTTP {} {}".format(e.code, http_error_body(e))
            lines.append("{}: ERROR {}".format(cat, entry["error"]))
        except Exception as e:
            entry["error"] = str(e)
            lines.append("{}: ERROR {}".format(cat, e))
        results["categories"][cat] = entry

    results["summary"] = {
        "categories_ok": ok,
        "categories_total": len(SEARCHES),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n".join(lines))
    print("Saved: {}".format(RESULTS_PATH))
    print("NOTE: previews watermarked; full download needs POST /v2/images/licenses with subscription_id.")


if __name__ == "__main__":
    main()
