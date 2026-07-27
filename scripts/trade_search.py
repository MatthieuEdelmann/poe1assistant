#!/usr/bin/env python3
"""Query the official PoE trade API directly.

pob-mcp's search_trade_items crashes on some bow listings, so this is the fallback.
Usage: trade_search.py '<query json>' [league]
"""
import json
import sys
import time
import urllib.error
import urllib.request

LEAGUE = sys.argv[2] if len(sys.argv) > 2 else "Allflame"
BASE = "https://www.pathofexile.com/api/trade"
UA = "poe1-expert-agent/1.0 (contact: local user; low volume)"


def post(url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"User-Agent": UA, "Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


query = json.loads(sys.argv[1])
try:
    res = post(f"{BASE}/search/{LEAGUE}", query)
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:500]}")
    sys.exit(1)

ids = res["result"][:10]
print(f"total={res['total']}  search=https://www.pathofexile.com/trade/search/{LEAGUE}/{res['id']}")
if not ids:
    sys.exit(0)

time.sleep(1)
data = get(f"{BASE}/fetch/{','.join(ids)}?query={res['id']}")
for entry in data["result"]:
    if not entry:
        continue
    item = entry["item"]
    listing = entry["listing"]
    price = listing.get("price") or {}
    amount = price.get("amount", "?")
    currency = price.get("currency", "?")
    print(f"\n--- {item.get('name', '')} {item.get('typeLine', '')} | {amount} {currency} "
          f"| ilvl {item.get('ilvl')} | {listing['account']['name']}")
    for line in item.get("implicitMods", []):
        print(f"    (implicit) {line}")
    for line in item.get("fracturedMods", []):
        print(f"    (fractured) {line}")
    for line in item.get("explicitMods", []):
        print(f"    {line}")
    for line in item.get("craftedMods", []):
        print(f"    (crafted) {line}")
