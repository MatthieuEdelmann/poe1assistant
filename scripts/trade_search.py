#!/usr/bin/env python3
"""Query official trade listings: trade_search.py '<query json>' [league] [--save FILE].

Use - instead of JSON to read stdin. Offline checks: uv run tests/check_trade_search.py.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from email.message import Message
import json
import os
from pathlib import Path
import sqlite3
import sys
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

BASE = 'https://www.pathofexile.com/api/trade'
UA = 'poe1-expert-agent/1.0 (contact: local user; low volume)'
RATE_DB = Path(os.environ.get('XDG_CACHE_HOME', Path.home() / '.cache')) / 'poe1assistant' / 'trade-limits.sqlite3'
MAX_WAIT = 60.0


def pace(bucket: str) -> None:
    """Serialize request slots across invocations sharing the same cache directory."""
    RATE_DB.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + MAX_WAIT
    while True:
        with sqlite3.connect(RATE_DB, timeout=5) as db:
            db.execute('CREATE TABLE IF NOT EXISTS limits (bucket TEXT PRIMARY KEY, next_at REAL)')
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT next_at FROM limits WHERE bucket = ?', (bucket,)).fetchone()
            now = time.time()
            wait = max(0.0, row[0] - now) if row else 0.0
            if not wait:
                gap = 12.0 if bucket == 'search' else 1.0
                db.execute('INSERT OR REPLACE INTO limits VALUES (?, ?)', (bucket, now + gap))
                return
        if wait > deadline - time.monotonic():
            raise RuntimeError(f'Trade cooldown: retry in {wait:.0f}s; automatic waiting is limited to {MAX_WAIT:.0f}s.')
        print(f'Waiting {wait:.1f}s for the {bucket} quota.', file=sys.stderr)
        time.sleep(wait)


def defer(bucket: str, seconds: float) -> None:
    if seconds <= 0:
        return
    with sqlite3.connect(RATE_DB, timeout=5) as db:
        db.execute('UPDATE limits SET next_at = MAX(next_at, ?) WHERE bucket = ?', (time.time() + seconds, bucket))


def cooldown(headers: Message) -> float:
    delay = float(headers.get('Retry-After', '0'))
    for rule in headers.get('X-Rate-Limit-Rules', 'ip').split(','):
        prefix = f'X-Rate-Limit-{rule.strip()}'
        limits = headers.get(prefix, '')
        states = headers.get(f'{prefix}-State', '')
        if not limits or not states:
            continue
        for limit, state in zip(limits.split(','), states.split(',')):
            maximum, window, _ = map(int, limit.split(':'))
            count, _, penalty = map(int, state.split(':'))
            delay = max(delay, penalty, window + 1 if count >= maximum - 1 else 0)
    return delay


def request_json(url: str, bucket: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'User-Agent': UA, 'Content-Type': 'application/json', 'Accept': 'application/json'},
    )
    for attempt in range(3):
        pace(bucket)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                defer(bucket, cooldown(response.headers))
                result: Any = json.load(response)
                if not isinstance(result, dict):
                    raise ValueError('Expected a JSON object from the trade API.')
                if result.get('error'):
                    raise ValueError(f'Trade API error: {result["error"]}')
                return result
        except urllib.error.HTTPError as exc:
            if exc.code != 429:
                raise
            defer(bucket, max(cooldown(exc.headers), 1 if exc.headers.get('Retry-After') else 60))
            if attempt == 2:
                raise
    raise RuntimeError('Trade retry budget exhausted.')


def describe(entry: dict[str, Any]) -> str:
    item = entry['item']
    listing = entry['listing']
    price = listing.get('price') or {}
    lines = [f"\n--- {item.get('name', '')} {item.get('typeLine', '')} | "
             f"{price.get('amount', '?')} {price.get('currency', '?')} | ilvl {item.get('ilvl')}"]
    lines.append(f"    seller: {listing.get('account', {}).get('name', '?')} | listed: {listing.get('indexed', '?')}")
    for key in ('properties', 'sockets', 'influences'):
        if item.get(key):
            lines.append(f'    {key}: {json.dumps(item[key], ensure_ascii=False)}')
    flags = [key for key in ('corrupted', 'mirrored', 'fractured', 'synthesised', 'split', 'duplicated') if item.get(key)]
    if flags:
        lines.append(f"    flags: {', '.join(flags)}")
    for key in ('enchantMods', 'implicitMods', 'fracturedMods', 'explicitMods', 'craftedMods', 'mutatedMods'):
        for mod in item.get(key) or []:
            text = mod.get('description', mod.get('text', str(mod))) if isinstance(mod, dict) else mod
            lines.append(f'    {key}: {text}')
    for skill in item.get('mercenarySkills') or []:
        supports = ', '.join(f"{support['name']} T{support['tier']}" for support in skill.get('supports') or [])
        lines.append(f"    skill: {skill['name']} [{supports}]")
    return '\n'.join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', help='Full trade query JSON, or - for stdin')
    parser.add_argument('league', nargs='?', default='Covens')
    parser.add_argument('--save', type=Path, help='Save raw evidence to a new JSON file')
    args = parser.parse_args(argv)
    try:
        if args.save and args.save.exists():
            raise ValueError(f'Refusing to overwrite {args.save}. Choose a new evidence filename.')
        query = json.loads(sys.stdin.read() if args.query == '-' else args.query)
        if not isinstance(query, dict) or not isinstance(query.get('query'), dict):
            raise ValueError('Provide a trade query object containing a query object.')
        league = urllib.parse.quote(args.league, safe='')
        result = request_json(f'{BASE}/search/{league}', 'search', query)
        search_id = result['id']
        ids = result['result'][:10]
        link = f'https://www.pathofexile.com/trade/search/{league}/{search_id}'
        print(f"total={result['total']}  search={link}")
        items = request_json(f"{BASE}/fetch/{','.join(ids)}?{urllib.parse.urlencode({'query': search_id})}", 'fetch')['result'] if ids else []
        if args.save:
            with args.save.open('x') as output:
                json.dump({'league': args.league, 'fetched_at': datetime.now(timezone.utc).isoformat(),
                           'query': query, 'total': result['total'], 'search_url': link, 'items': items}, output, indent=2)
        for entry in items:
            if entry is not None:
                print(describe(entry))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, sqlite3.Error) as exc:
        print(f'Trade search failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
