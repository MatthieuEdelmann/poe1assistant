# POE1 Expert — source reference

## Current league (default)

| Field | Value |
|-------|-------|
| Challenge league | Covens of Umbra |
| Short / API name | `Covens` |
| Patch | 3.30.0 |
| HC | `Hardcore Covens` |
| Launch | 2026-11-13 |

League mechanics and build meta: [covens.md](covens.md).

Example poe.ninja currency URL:

```
https://poe.ninja/poe1/api/economy/stash/current/currency/overview?league=Covens&type=Currency
```

## pob-mcp

- Repo: https://github.com/ianderse/pob-mcp
- Path of Building checkout: https://github.com/PathOfBuildingCommunity/PathOfBuilding

### Key env vars

| Variable | Purpose |
|----------|---------|
| `POB_DIRECTORY` | Folder with `.xml` build files |
| `POB_LUA_ENABLED` | `true` for live PoB calculations |
| `POB_PATH` | Path to `PathOfBuilding/src` (contains `HeadlessWrapper.lua`) |
| `POB_CMD` | LuaJIT binary (default `luajit`) |
| `POE_TRADE_ENABLED` | `true` for trade API tools |
| `POE_SESSION_ID` | POESESSID cookie for weighted BIS search |

### Tool categories (discover the live list through the current client)

- **XML**: `list_builds`, `analyze_build`, `compare_builds`, tree diff/path tools
- **Lua core**: `lua_start`, `lua_load_build`, `lua_get_stats`, `lua_set_tree`, `validate_build`
- **Items/skills**: `add_item`, `setup_skill_with_gems`, `get_skill_setup`, flask toggles
- **Optimization**: `analyze_defenses`, `suggest_optimal_nodes`, `find_best_anointment`, `check_boss_readiness`
- **Economy**: `get_currency_rates`, `find_arbitrage`, `calculate_trading_profit`
- **Trade** ([trade.md](trade.md), `POE_TRADE_ENABLED=true`): `get_leagues`, `search_stats`, `search_trade_items`, `get_item_price`, `find_weighted_trade_items`, `find_resistance_gear`, `find_item_upgrades`, `search_cluster_jewels`, `compare_trade_items`, `generate_shopping_list`

---

## pathofexile.com/trade

Official site: https://www.pathofexile.com/trade/

pob-mcp uses the Trade API (`trade.pathofexile.com`). Default league: **`Covens`**.

| Tool | Purpose |
|------|---------|
| `get_leagues` | Resolve exact league string before searching |
| `search_stats` | Look up mod `stat_id` for filters |
| `search_trade_items` | Search listings (name, base, price, links, mods) |
| `get_item_price` | Quick price on a named item |
| `find_weighted_trade_items` | PoB-weighted BIS (needs `POE_SESSION_ID` + loaded build) |
| `find_resistance_gear` | Budget resist upgrades across slots |
| `find_item_upgrades` | Shopping spec from build (no API) |
| `search_cluster_jewels` | Clusters by size / enchant / notables |
| `compare_trade_items` | Compare prior search results |
| `generate_shopping_list` | Budget-prioritized upgrade list |

### Resolved stat IDs

Previously verified during Allflame (3.29); recheck with `search_stats` before use in Covens. Full list: `https://www.pathofexile.com/api/trade/data/stats`.
Query semantics and pitfalls: [trade.md](trade.md).

| Mod | Stat ID |
|-----|---------|
| Adds # to # Lightning Damage to Attacks | `explicit.stat_1754445556` |
| Adds # to # Fire Damage to Attacks | `explicit.stat_1573130764` |
| Adds # to # Cold Damage to Attacks | `explicit.stat_4067062424` |
| # to # Added Lightning Damage with Bow Attacks | `explicit.stat_1040269876` |
| # to # Added Fire Damage with Bow Attacks | `explicit.stat_3120164895` |
| # to # Added Cold Damage with Bow Attacks | `explicit.stat_215124030` |
| +# to maximum Life | `explicit.stat_3299347043` |
| +#% to Lightning Resistance | `explicit.stat_1671376347` |
| +#% chance to Suppress Spell Damage | `explicit.stat_3680664274` |
| #% increased Attack Speed | `explicit.stat_681332047` |
| #% increased Attack Speed (Local) | `explicit.stat_210067635` |
| #% increased Elemental Damage with Attack Skills | `explicit.stat_387439868` |
| +#% to Critical Strike Multiplier with Bows | `explicit.stat_1712221299` |
| #% increased Critical Strike Chance with Bows | `explicit.stat_2091591880` |
| +#% to Global Critical Strike Multiplier | `explicit.stat_3556824919` |
| #% increased Damage with Bow Skills | `explicit.stat_1241625305` |
| Bow Attacks fire # additional Arrows | `explicit.stat_3885405204` |
| +#% total to Lightning Resistance (pseudo) | `pseudo.pseudo_total_lightning_resistance` |

Search result URLs:

```
https://www.pathofexile.com/trade/search/{league}/{searchId}
https://www.pathofexile.com/trade/search/{league}/{searchId}#{itemId}
```

Manual UI entry point: https://www.pathofexile.com/trade/search/Covens

Full workflows: [trade.md](trade.md).

---

## poewiki.net

| Use case | URL pattern |
|----------|-------------|
| Item | `https://www.poewiki.net/wiki/{Item_Name}` |
| Skill gem | `https://www.poewiki.net/wiki/{Gem_Name}` |
| Ascendancy | `https://www.poewiki.net/wiki/{Ascendancy_Name}` |
| Mechanic | `https://www.poewiki.net/wiki/{Mechanic_Name}` |
| League | `https://www.poewiki.net/wiki/{League_Name}` |

Search: `https://www.poewiki.net/index.php?search={query}`

Naming: spaces → underscores; keep apostrophes and punctuation as on the wiki.

---

## poe.ninja (PoE 1)

Site: https://poe.ninja/poe1/

After the 2025 merge, PoE1 economy APIs use the `/poe1/api/economy/` prefix.

### Currency (stash rates — most common for item pricing)

```
https://poe.ninja/poe1/api/economy/stash/current/currency/overview?league={LEAGUE}&type=Currency
https://poe.ninja/poe1/api/economy/stash/current/currency/overview?league={LEAGUE}&type=Fragment
```

### Currency exchange

```
https://poe.ninja/poe1/api/economy/exchange/current/overview?league={LEAGUE}&type=Currency
```

### Items

```
https://poe.ninja/poe1/api/economy/stash/current/item/overview?league={LEAGUE}&type={TYPE}
```

Common `type` values: `UniqueWeapon`, `UniqueArmour`, `UniqueAccessory`, `UniqueJewel`, `UniqueFlask`, `SkillGem`, `ClusterJewel`, `Map`, `UniqueMap`, `DivinationCard`, `Essence`, `Fossil`, `Oil`, `BaseType`, `HelmetEnchant`.

Scarabs were removed in 3.30. For Threads, inspect the current poe.ninja categories or use official trade; do not assume the old `Scarab` category or invent a replacement API type.

### Response fields

- Currency lines: `chaosEquivalent`, `pay` / `receive` currency ids
- Item lines: `name`, `chaosValue`, `divineValue`, `detailsId`, `links`

### Legacy endpoints (may 404)

Older tools used `https://poe.ninja/api/data/currencyoverview?...` — prefer `/poe1/api/economy/...` if those fail.

### pob-mcp shortcut

`get_currency_rates`, `find_arbitrage`, and `calculate_trading_profit` wrap poe.ninja. Pass league **`Covens`** unless the user is on HC/Standard.

---

## Class / ascendancy IDs (lua_set_tree)

Classes: 0=Scion, 1=Marauder, 2=Ranger, 3=Witch, 4=Duelist, 5=Templar, 6=Shadow

Witch ascendancies: 1=Occultist, 2=Elementalist, 3=Necromancer
