"""Offline checks: uv run tests/check_trade_search.py."""
from __future__ import annotations

import contextlib
from concurrent.futures import ThreadPoolExecutor
from email.message import Message
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
from threading import Barrier
from typing import Any
import urllib.error
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('trade_search', ROOT / 'scripts/trade_search.py')
assert spec and spec.loader
trade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trade)


class Response(io.BytesIO):
    def __init__(self, payload: dict[str, Any]) -> None:
        super().__init__(json.dumps(payload).encode())
        self.headers = Message()


def limited(seconds: str) -> urllib.error.HTTPError:
    headers = Message()
    headers['Retry-After'] = seconds
    return urllib.error.HTTPError('https://example.test', 429, 'limited', headers, io.BytesIO())


with tempfile.TemporaryDirectory() as directory, patch.object(trade, 'RATE_DB', Path(directory) / 'rates.sqlite3'):
    trade.pace('search')
    with sqlite3.connect(trade.RATE_DB) as connection:
        due = connection.execute('SELECT next_at FROM limits WHERE bucket = ?', ('search',)).fetchone()[0]
    # A separate invocation reads the same cooldown instead of sending another request.
    with patch.object(trade.time, 'time', side_effect=[due - 5, due]), patch.object(trade.time, 'sleep') as sleep:
        trade.pace('search')
    sleep.assert_called_once_with(5)
    headers = Message()
    headers['X-Rate-Limit-Rules'] = 'ip, account'
    headers['X-Rate-Limit-Ip'] = '5:10:60,30:300:1800'
    headers['X-Rate-Limit-Ip-State'] = '1:10:0,29:300:0'
    headers['X-Rate-Limit-Account'] = '10:10:60'
    headers['X-Rate-Limit-Account-State'] = '1:10:0'
    assert trade.cooldown(headers) == 301
    headers['Retry-After'] = '1800'
    assert trade.cooldown(headers) == 1800
    trade.defer('search', 1800)
    with patch.object(trade.time, 'sleep') as sleep:
        try:
            trade.pace('search')
        except RuntimeError as exc:
            assert 'cooldown' in str(exc).lower()
        else:
            raise AssertionError('A long cooldown must stop instead of blocking')
    sleep.assert_not_called()

with patch.object(trade, 'pace'), patch.object(trade, 'defer') as defer, patch.object(
    trade.urllib.request, 'urlopen', side_effect=[limited('2'), Response({'result': []})]
) as request:
    assert trade.request_json('https://example.test', 'search') == {'result': []}
    assert request.call_count == 2
    assert defer.call_args_list[0].args == ('search', 2)

with patch.object(trade, 'pace'), patch.object(trade, 'defer'), patch.object(
    trade.urllib.request, 'urlopen', side_effect=limited('2')
) as request:
    try:
        trade.request_json('https://example.test', 'fetch')
    except urllib.error.HTTPError:
        pass
    else:
        raise AssertionError('Repeated 429 responses must stop')
    assert request.call_count == 3

with tempfile.TemporaryDirectory() as directory, patch.object(trade, 'RATE_DB', Path(directory) / 'concurrent.sqlite3'):
    barrier = Barrier(2)

    def reserve() -> bool:
        barrier.wait(timeout=5)
        try:
            trade.pace('search')
            return True
        except RuntimeError:
            return False

    with patch.object(trade, 'MAX_WAIT', 0), ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(reserve) for _ in range(2)]
        assert sorted(future.result() for future in futures) == [False, True]

bad_request = urllib.error.HTTPError('https://example.test', 400, 'bad query', Message(), io.BytesIO())
with patch.object(trade, 'pace'), patch.object(trade.urllib.request, 'urlopen', side_effect=bad_request) as request:
    try:
        trade.request_json('https://example.test', 'search')
    except urllib.error.HTTPError as exc:
        assert exc.code == 400
    else:
        raise AssertionError('Invalid queries must fail without retrying')
    assert request.call_count == 1

entry = {
    'item': {'name': 'Example', 'typeLine': 'Mercenary Warrant', 'ilvl': 83,
             'explicitMods': [{'description': 'Example modifier'}], 'mutatedMods': ['Mutated modifier'],
             'mercenarySkills': [{'name': 'Main skill', 'supports': [{'name': 'Return', 'tier': 3}]}]},
    'listing': {'account': {'name': 'Example#1234'}, 'indexed': '2026-11-24T12:00:00Z',
                'price': {'amount': 2, 'currency': 'divine'}},
}
query = {'query': {'status': {'option': 'online'}}, 'sort': {'price': 'asc'}}
with tempfile.TemporaryDirectory() as directory:
    saved = Path(directory) / 'evidence.json'
    output = io.StringIO()
    with patch.object(trade, 'request_json', side_effect=[{'result': ['a', 'b'], 'total': 2, 'id': 'query-id'}, {'result': [None, entry]}]) as request, contextlib.redirect_stdout(output):
        assert trade.main([json.dumps(query), 'Hardcore Covens', '--save', str(saved)]) == 0
    assert request.call_args_list[0].args[0].endswith('/search/Hardcore%20Covens')
    assert request.call_args_list[0].args[2] == query  # Do not force instant buyout.
    evidence = json.loads(saved.read_text())
    assert evidence['league'] == 'Hardcore Covens'
    assert evidence['query'] == query and evidence['items'] == [None, entry]
    assert evidence['fetched_at']
    assert 'Main skill' in output.getvalue() and 'Return' in output.getvalue()
    assert 'Example modifier' in output.getvalue() and 'Mutated modifier' in output.getvalue()
    with patch.object(trade, 'request_json') as request, contextlib.redirect_stderr(io.StringIO()):
        assert trade.main([json.dumps(query), '--save', str(saved)]) == 1
    request.assert_not_called()
    assert json.loads(saved.read_text()) == evidence

with patch.object(trade, 'request_json', return_value={'result': [], 'total': 0, 'id': 'empty'}) as request, patch.object(sys, 'stdin', io.StringIO(json.dumps(query))), contextlib.redirect_stdout(io.StringIO()):
    assert trade.main(['-']) == 0
    assert request.call_count == 1
    assert request.call_args.args[0].endswith('/search/Covens')

with patch.object(trade, 'request_json') as request, contextlib.redirect_stderr(io.StringIO()):
    assert trade.main(['[]']) == 1
request.assert_not_called()

print('All trade checks passed (offline).')
