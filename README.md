# POE1 Expert Agent

Cursor agent skill for **Path of Exile 1** — tuned for the **Curse of the Allflame** challenge league (patch **3.29**, economy league `Allflame`).

Sources:

- [pob-mcp](https://github.com/ianderse/pob-mcp) — Path of Building MCP server (3.29 data)
- [pathofexile.com/trade](https://www.pathofexile.com/trade/) — official trade search (via pob-mcp)
- [poewiki.net](https://www.poewiki.net/) — game mechanics and items
- [poe.ninja](https://poe.ninja/poe1/) — live economy data (`league=Allflame`)

Invoke in chat with `/poe1-expert` or ask any PoE1 question (the skill auto-applies from context).

## Usage example 1: "what is my next 50 div upgrade?"

A real session against the `labcummer` build in [`builds/`](builds) — a level 92 Deadeye running
Lightning Arrow with Trinity.

> **Prompt:** what is the next 50div upgrade for my character labcummer with pob, show me the DPS improvement

The agent loads the build into a headless Path of Building, measures boss DPS, then tests one change
at a time against live trade listings. Nothing is estimated from memory — every number below came out
of the PoB engine.

### The answer

Baseline was **1,078,463** boss DPS. The recommended buys reach **1,685,311**, a **+56% gain for
about 10 divine**:

| # | Action | Cost | DPS after | Cumulative |
|---|--------|------|-----------|------------|
| 1 | Level `Invert the Rules` from 3 → 20 | 0 div | 1.30M | +20.4% |
| 2 | `Trinity` and `Increased Critical Damage` to 20, quality 20 on all supports | a few chaos | 1.36M | +26.5% |
| 3 | `Woe Nails` quiver | 10 div | 1.64M | +52.2% |
| 4 | `Ancient Prism` searching eye jewel | 1 chaos | 1.69M | +56.3% |

The headline finding is that the biggest single lever was **not an item**. One under-levelled support
gem was worth **+16.2%** on its own, and a trade search returned zero listings for it league-wide —
so the correct advice was "level it yourself", not "buy something".

### Why the quiver, and which one

Six quivers benchmarked in PoB on the gem-fixed build:

| Quiver | Boss DPS | vs equipped |
|--------|----------|-------------|
| `Vortex Spear` (equipped) | 1.35M | — |
| `Beast Brand` | 1.42M | +5.2% |
| `Dusk Skewer` | 1.51M | +11.2% |
| `Empyrean Shot` | 1.55M | +14.7% |
| `Maelstrom Spear` | 1.56M | +15.3% |
| `Woe Nails` | 1.64M | **+21.2%** |

A 2 div `Entropy Skewer` with *more* attack speed and +36% bow crit multiplier scored 5% **lower**
than the 10 div Woe Nails — Woe Nails carries flat fire damage, which balances Trinity's resonance
better than raw crit does. That is the kind of result you only get by calculating rather than
eyeballing mods.

### What it refused to buy

Roughly 40 divine was left deliberately unspent:

| Candidate | Measured | Verdict |
|-----------|----------|---------|
| Damage rings | +4.5% DPS | Lightning resistance 71% → 34%, EHP −19.5%. Rejected. |
| Helmet with −9% enemy lightning res | −0.6% DPS | Worse than the equipped `The Gull`. |
| 35 div abyss jewel | +1.4% | Barely ahead of the 1 chaos option. |
| Gloves | not buyable | Zero listings with the needed mod combination. |
| Bow | none exist | Nothing above 50 div beats the equipped fractured Spine Bow. |

The blocker was resistances, not currency: the equipped two-stone ring was holding the whole
resistance profile together, so every damage ring on the market cost a fifth of the character's
effective HP. Fixing resistances first unlocks those slots.

## Usage example 2: "which unique body armours are worth 6-linking?"

An economy question rather than a build question — no character involved.

> **Prompt:** look for unique body armour and 6link equivalent, give me list of the highest price delta

The agent pulled every unique body armour poe.ninja tracks in Allflame, paired each armour's
unlinked line with its 6-link line, and ranked by the gap. It then swept all 92 socketable unique
chests against the live trade API as a cross-check.

### The finding: there is barely a list

The 6-link premium is close to a **constant**, not a property of the armour. Unlinked unique chests
have a median value of **2 chaos** and range from 1c to 862c, but their 6-linked versions collapse
onto a narrow band centred on **323 chaos**. Queen of the Forest, Blunderbore, Briskwrap and The
Ivory Tower are unrelated items worth 1 chaos each, and all four sell 6-linked for 323–369c. You are
pricing six linked sockets, not the unique.

That reframes the ranking into a decision. Linking one yourself costs about **495 chaos** (1500 Orbs
of Fusing at 0.33c; ~363c on a 20% quality base). Of the 51 uniques with enough listings to trust,
only two clear it:

| Unique | Unlinked | 6-link | Delta | Listings (unlinked / 6L) | Verdict |
|--------|----------|--------|-------|--------------------------|---------|
| `Replica Hyrri's Ire` | 9c | 646c | **+637c** | 146 / 5 | Link it yourself |
| `The Fourth Vow` | 5c | 615c | **+610c** | 187 / 11 | Link it yourself |
| `Replica Farrul's Fur` | 862c | 1337c | +475c | 32 / 5 | Only on a 20q base |
| `The Brass Dome` | 5c | 466c | +461c | 372 / 6 | Only on a 20q base |
| `Replica Covenant` | 83c | 539c | +455c | 39 / 11 | Only on a 20q base |
| `Cloak of Defiance` | 3c | 401c | +398c | 283 / 26 | Buy the 6-link |
| `Carcass Jack` | 2c | 388c | +386c | 1629 / 50 | Buy the 6-link |

Everything below the top two is cheaper to buy already-linked than to fuse. The big *multiples* are
the same trap: `Queen of the Forest` is a 369x return that nets 368 chaos, which still loses to a
495c link attempt.

The ceiling on the whole market is **`Tabula Rasa` at 5 chaos** across 899 listings. A guaranteed
6-link with six white sockets for 5c is what every other unique's link premium competes against.
`Skin of the Loyal` (690c) is the only inherently-6L chest that holds real value.

### Why poe.ninja and not live listings

The live 6-link market is too sparse to rank: of 92 socketable uniques swept on the trade API,
**82 had no online 6-link listing at all**, and most of the rest had one or two. `Carcass Jack` makes
the case — a single live listing at 5000c against a poe.ninja value of 388c drawn from 50 listings.
Ranking on live listings would have put one overpriced item at the top.

The same caution applies inside the poe.ninja data. The largest raw delta in the set,
`Greed's Embrace` at +1012c, rests on two listings, and a live search found one at 150c. Anything
under five listings a side is an anecdote, so the agent reports those separately instead of ranking
them.

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
