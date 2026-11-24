# Path of Exile Trade (official)

Site: https://www.pathofexile.com/trade/

pob-mcp talks to the **official Trade API** (`trade.pathofexile.com`). Every search result should include a clickable trade URL when the tool returns one.

Requires `POE_TRADE_ENABLED=true` in [`.cursor/mcp.json`](../../mcp.json).

## League names

Always call `get_leagues` when unsure. Default: **`Covens`**.

| Player league | Trade API name |
|---------------|----------------|
| SC challenge | `Covens` |
| HC challenge | `Hardcore Covens` |
| Permanent | `Standard` / `Hardcore` |

Never guess — trade league strings differ from poe.ninja slugs.

## Tool reference

| Tool | When to use |
|------|-------------|
| `get_leagues` | First call before any trade search; resolve exact league string |
| `search_stats` | Find `stat_id` values for mod filters (`life`, `fire resistance`, etc.) |
| `search_trade_items` | General item search — name, base, price, links, rarity, mod filters |
| `get_item_price` | Quick unique or named-item price check |
| `find_weighted_trade_items` | BIS for loaded build slot — PoB stat weights (**needs `POE_SESSION_ID`**) |
| `find_resistance_gear` | Cap resists on a budget across slots |
| `find_item_upgrades` | What to look for (no API) — spec from build gaps, then `search_trade_items` |
| `search_cluster_jewels` | Cluster jewels by size, enchant, notables |
| `compare_trade_items` | Side-by-side listings from a prior search (`item_ids` + `search_id`) |
| `generate_shopping_list` | Prioritized upgrade list for a build file within budget |

### `search_trade_items` defaults

- `league`: `Covens`
- `limit`: 5 (max 10 — keep low for token use)
- `price_currency`: `chaos` (or `divine`, `exalted`)
- `online_status`: `available` — use `securable` for instant-buy from online sellers

### Mod filters

1. `search_stats` with query (e.g. `maximum life`)
2. Pass `mods: [{ stat_id, min, max }]` to `search_trade_items`

## Query mechanics

The examples below were measured in Allflame (3.29). They explain query semantics, not current
Covens availability: recheck mod tiers, stat IDs and listing counts before recommending a purchase.

### `Adds # to #` filters match the **average**, not the low or high roll

A quiver rolling `Adds 6 to 131 Lightning Damage` matches `min: 68` but not `min: 70`, because its
average is 68.5. The top tier (`Electrocuting`, 5–11 to 124–140) has a maximum average of 75.5 —
and `min: 76` returns exactly zero items league-wide, which is how this was confirmed.

**Consequence:** filter on `(low + high) / 2`, not either endpoint alone.

### Know the mod ceiling for the base type before you filter

Each base type caps at a different tier. Gloves top out around **19 average** flat lightning, so a
`min: 28` glove search returns nothing — not because the market is empty, but because the item is
impossible. Rings reach ~37, quivers ~75.

To inspect available rolls, search with **one** stat filter, no value, and sort by that stat
using the current trade syntax (`stat.<id>`, descending). Read the fetched modifier magnitudes
and verify the current tier in a data source. Price sorting does not establish a mod ceiling.

### `explicit.` also matches crafted mods; `crafted.` does not match rolled ones

For quiver attack speed: `explicit.stat_681332047` returns 1905 items, `crafted.stat_681332047`
returns 7. The explicit form is the superset — a bench-crafted 12% attack speed still matches it.

**Use `explicit.` by default.** Reach for `crafted.` only to *require* that the mod is crafted.

### Bow-attack mods are a separate stat family

Abyss jewels roll both, and they are not interchangeable:

| Mod text | Stat ID |
|----------|---------|
| `Adds # to # Lightning Damage to Attacks` | `explicit.stat_1754445556` |
| `# to # Added Lightning Damage with Bow Attacks` | `explicit.stat_1040269876` |

Note the wording flip — "Adds … to Attacks" versus "… Added … with Bow Attacks". Searching the
wrong one silently misses the whole category. Same pattern for fire (`3120164895`), cold
(`215124030`), physical (`1760576992`), chaos (`3478075311`).

### Gem and item names need the exact trade base type

`"type": "Invert the Rules"` returns `400 Unknown item base type`; the real base is
`Invert the Rules Support`. Resolve names against `https://www.pathofexile.com/api/trade/data/items`
before searching, the same way stat IDs come from `.../data/stats` (17,629 entries).

### A zero result tells you nothing about *which* filter failed

The API gives no diagnostics. When a search returns `total=0`, drop filters one at a time rather
than guessing. Combining `type` with a `category` filter is **not** the problem — both forms return
identical counts; over-constraining on life or resistances almost always is.

### Zero listings can be the answer

An empty result set can be a finding, not a failure. In the historical Allflame session, no
`Invert the Rules Support` was listed, so the advice was "level it yourself". Query Covens afresh;
do not carry that availability claim into the new league.

## Direct API fallback

`search_trade_items` in pob-mcp crashes on some listings (notably certain bows). When it does, use
[`scripts/trade_search.py`](../../../scripts/trade_search.py), which posts raw queries to the
official endpoints and prints prices, item properties, special modifiers and mercenary support
attachments. It preserves your query's status and sort order; choose these explicitly:

```bash
uv run scripts/trade_search.py '<query json>' Covens
uv run scripts/trade_search.py '<query json>' 'Hardcore Covens' --save /tmp/poe-step-1.json
uv run scripts/trade_search.py - Covens < query.json
```

`--save` records the query, league, UTC timestamp, search URL, total and raw fetched listings;
it refuses to overwrite an existing file. The script fetches at most ten results and skips
unavailable entries when displaying them. Save different comparison steps to different files.

Run `uv run tests/check_trade_search.py` for the offline checks.

## Additional pricing filters

- Resolve current IDs and filter options with `search_stats` and official trade metadata
  (`/api/trade/data/stats`, `/items`, `/filters`, `/static`) instead of expanding a hard-coded ID list.
- Use pseudo filters for relevant combined totals; use `fractured` filters when the actual
  fracture matters. An ordinary explicit match does not prove that a modifier is fractured.
- Some item types require an object with `option` and `discriminator`, rather than a plain
  string. Preserve the representation returned by item metadata.
- A `count` stat group expresses alternatives; an `and` group requires the combination.
  Simplify queries rejected as too complex instead of assuming that no listings exist.
- Do not interpret capped totals as an exact population. Fetch returned entries before
  interpreting prices, attachment-dependent modifiers or properties absent from filters.
- Keep valuation methodology in [pricing.md](pricing.md), including how to handle weak samples
  and the difference between asking prices and completed sales.

## Workflows

### Price a unique

```
get_leagues → get_item_price (item_name, league: Covens)
```

For an actual valuation rather than a quick generic quote, follow [unique pricing](pricing/uniques.md).

### Find gear for a build gap

```
lua_load_build → find_item_upgrades (slot, priority) → search_trade_items
```

Or for resistance problems:

```
validate_build → find_resistance_gear (league: Covens, fire/cold/lightning_resist_needed, max_price_per_item)
```

### BIS weighted search (authenticated)

```
lua_start → lua_load_build → find_weighted_trade_items (league: Covens, slot: "Body Armour")
```

Requires `POE_SESSION_ID` in MCP env (see README).

### Full upgrade shop run

```
lua_load_build → generate_shopping_list (build_name, league: Covens, budget, budget_tier)
→ search_trade_items per slot
```

## Trade URLs

pob-mcp returns links in this form:

```
https://www.pathofexile.com/trade/search/{league}/{searchId}
https://www.pathofexile.com/trade/search/{league}/{searchId}#{itemId}
```

**Always paste these** when recommending a listing so the user can buy in-game.

Manual search UI (same backend): https://www.pathofexile.com/trade/search/Covens

## POE_SESSION_ID setup

Weighted BIS (`find_weighted_trade_items`) requires your session cookie:

1. Log in at https://www.pathofexile.com/trade/
2. DevTools → Application → Cookies → `POESESSID`
3. Add to `.cursor/mcp.json`:

```json
"POE_SESSION_ID": "<value>"
```

4. Reload MCP. Never commit this value.

## Rate limits

- The MCP config's `POE_RATE_LIMIT_PER_SECOND` and `POE_CACHE_TTL` are client settings, not
  guarantees of server allowance. Read the returned quota and state headers; limits can change.
- The fallback script shares request slots across its invocations in
  `$XDG_CACHE_HOME/poe1assistant/trade-limits.sqlite3` (default `~/.cache`). Search slots are
  at least 12 seconds apart; fetch slots at least one second apart. It also defers calls when
  returned quota states approach a limit or impose a penalty.
- HTTP 429 retries honor `Retry-After` and stop after three attempts per request. A cooldown
  exceeding the 60-second automatic wait budget stops with a retry delay, which remains saved
  for later invocations. Do not loop around that failure to evade the cooldown.
- This state coordinates this helper only; MCP calls and other machines can share the server's
  quota without sharing its local state. Avoid simultaneous pricing sweeps through other clients.

Header semantics: [official rate-limit documentation](https://www.pathofexile.com/developer/docs#ratelimits).

## poe.ninja vs trade

| Need | Use |
|------|-----|
| Bulk currency, div card averages, economy trends | poe.ninja |
| Live buyable listings, rare mod combos, exact upgrade | trade API |
| Build-weighted BIS | `find_weighted_trade_items` |

Quote **listing prices** from trade; use poe.ninja only as a sanity check.
