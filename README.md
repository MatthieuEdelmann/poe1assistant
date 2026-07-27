# POE1 Expert Agent

Cursor agent skill for **Path of Exile 1** — tuned for the **Curse of the Allflame** challenge league (patch **3.29**, economy league `Allflame`).

Sources:

- [pob-mcp](https://github.com/ianderse/pob-mcp) — Path of Building MCP server (3.29 data)
- [pathofexile.com/trade](https://www.pathofexile.com/trade/) — official trade search (via pob-mcp)
- [poewiki.net](https://www.poewiki.net/) — game mechanics and items
- [poe.ninja](https://poe.ninja/poe1/) — live economy data (`league=Allflame`)

Invoke in chat with `/poe1-expert` or ask any PoE1 question (the skill auto-applies from context).

## One-time setup

### 1. Install system deps

```bash
# LuaJIT (required for live PoB calculations)
sudo apt-get install luajit   # Debian/Ubuntu
# or: brew install luajit     # macOS
```

### 2. Clone Path of Building

```bash
git clone https://github.com/PathOfBuildingCommunity/PathOfBuilding.git ~/Projects/PathOfBuilding
```

### 3. Install pob-mcp

```bash
./scripts/setup-pob-mcp.sh
```

Or manually:

```bash
git clone https://github.com/ianderse/pob-mcp.git vendor/pob-mcp
cd vendor/pob-mcp && npm install && npm run build
```

### 4. Configure paths

Edit [`.cursor/mcp.json`](.cursor/mcp.json):

| Variable | Set to |
|----------|--------|
| `POB_DIRECTORY` | Your PoB `Builds` folder |
| `POB_PATH` | `PathOfBuilding/src` (must contain `HeadlessWrapper.lua`) |
| `POB_CMD` | Full path to `luajit` if not on `PATH` |
| `POE_TRADE_ENABLED` | `true` (enabled by default) — official trade API |
| `POE_SESSION_ID` | Your `POESESSID` cookie for weighted BIS search (optional) |

Trade is **enabled** in the default config. For build-weighted BIS (`find_weighted_trade_items`):

1. Log in at https://www.pathofexile.com/trade/
2. Copy the `POESESSID` cookie from browser devtools
3. Add to `.cursor/mcp.json`:

```json
"POE_SESSION_ID": "<your POESESSID>"
```

4. Reload MCP. Do not commit this value.

### 5. Enable MCP in Cursor

Open this folder in Cursor. The project-level `.cursor/mcp.json` registers the `pob` server. Restart Cursor or reload MCP if tools do not appear.

Verify: ask the agent to `get_leagues` or `get_item_price` for a unique in `Allflame`.

## Skill location

- [`.cursor/skills/poe1-expert/SKILL.md`](.cursor/skills/poe1-expert/SKILL.md) — agent instructions
- [`.cursor/skills/poe1-expert/allflame.md`](.cursor/skills/poe1-expert/allflame.md) — 3.29 / Allflame league reference
- [`.cursor/skills/poe1-expert/trade.md`](.cursor/skills/poe1-expert/trade.md) — official trade workflows
- [`.cursor/skills/poe1-expert/character.md`](.cursor/skills/poe1-expert/character.md) — resolving an account name and pulling a character's gear/tree

## Looking up your own character

The agent needs your **account name** (`Name#1234`), not your character name. Give it once and it will reuse it.

If your character is ranked in the league, it can also resolve the account itself:

```bash
python3 scripts/find_account.py <character-name> [league]
```

## Smoke test (optional)

```bash
cd vendor/pob-mcp
POB_PATH=~/Projects/PathOfBuilding/src npm run test:smoke
```
