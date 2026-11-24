#!/usr/bin/env python3
"""Resolve a PoE character name to its `Name#1234` account name via the public ladder.

Only finds characters ranked in the league's top 15,000. If this misses, ask the
user for their account name directly — it cannot be derived from a character name.

Usage: find_account.py <character-name> [league]
       find_account.py --self-check
"""
from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

BASE = "https://www.pathofexile.com/api/ladders"
UA = "poe1-expert-agent/1.0 (contact: local user; low volume)"
PAGE = 200


def encode_account(account: str) -> str:
    """URL-encode an account name so the `#` discriminator survives as %23."""
    return urllib.parse.quote(account, safe="")


def fetch_page(league: str, offset: int) -> dict[str, Any]:
    url = f"{BASE}?id={urllib.parse.quote(league)}&limit={PAGE}&offset={offset}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload: dict[str, Any] = json.load(resp)
    return payload


def find(character: str, league: str) -> tuple[str, int] | None:
    """Return (account_name, rank) for `character`, or None if not on the ladder."""
    target = character.casefold()
    offset = 0
    total = PAGE
    while offset < total:
        try:
            page = fetch_page(league, offset)
        except urllib.error.HTTPError as exc:
            print(f"HTTP {exc.code} at offset {offset}: {exc.read().decode()[:200]}", file=sys.stderr)
            return None
        total = int(page.get("total", 0) or 0)
        entries = page.get("entries")
        if not isinstance(entries, list) or not entries:
            return None
        for entry in entries:
            if str(entry["character"]["name"]).casefold() == target:
                return str(entry["account"]["name"]), int(entry["rank"])
        offset += PAGE
        print(f"  ...scanned {min(offset, total)}/{total}", file=sys.stderr)
        time.sleep(0.3)  # ladder API is rate limited
    return None


def self_check() -> None:
    assert encode_account("Poteitik#3151") == "Poteitik%233151"
    assert encode_account("plain") == "plain"
    print("self-check ok")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-check":
        self_check()
        return 0
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    character = sys.argv[1]
    league = sys.argv[2] if len(sys.argv) > 2 else "Covens"
    hit = find(character, league)
    if hit is None:
        print(
            f"'{character}' is not on the {league} ladder. Ask the user for their "
            f"account name (shown as Name#1234 in the in-game social panel).",
            file=sys.stderr,
        )
        return 1
    account, rank = hit
    print(f"character : {character}")
    print(f"account   : {account}")
    print(f"encoded   : {encode_account(account)}")
    print(f"rank      : {rank}")
    print(
        f"\ngear: https://www.pathofexile.com/character-window/get-items"
        f"?accountName={encode_account(account)}&character={urllib.parse.quote(character)}&realm=pc"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
