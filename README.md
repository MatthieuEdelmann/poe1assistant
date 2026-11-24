# POE1 Assistant

A shared Path of Exile 1 assistant for **character optimization, build comparisons, item pricing
and trade**, usable from Cursor, Claude Code and ChatGPT/Codex with repository access.

Current defaults: **Covens of Umbra · patch 3.30 · API league `Covens`**.
See the [league reference](.cursor/skills/poe1-expert/covens.md) for sources and the last verification date.

The repository contains agent instructions and command-line helpers. Live calculations require
[Path of Building](https://github.com/PathOfBuildingCommunity/PathOfBuilding) and
[pob-mcp](https://github.com/ianderse/pob-mcp); live comparisons and prices use
[poe.ninja](https://poe.ninja/poe1/), the [official trade site](https://www.pathofexile.com/trade/)
and [PoE Wiki](https://www.poewiki.net/).

## What you can ask

| Task | Example prompt |
|------|----------------|
| Optimize a character | “Audit my build and find the next upgrades within 50 divine. Measure the damage and defense changes in my PoB.” |
| Compare similar builds | “Compare my character with poe.ninja builds using the same main skill and mandatory uniques. Explain which changes transfer to my build.” |
| Price a copied item | “Estimate this item's listing price from current comparables.” Then paste its in-game copied text. |
| Check a mercenary warrant | “Compare this warrant with matching skills and support placements, not just the same mercenary type.” |
| Find gear | “Find upgrades that keep my resistances capped, with direct trade links.” |
| Inspect an account | “Load character `<character>` from account `Name#1234`.” |

Provide your current PoB file or export for calculations. For account lookups, the account name
including its discriminator is needed; a character name alone may only be resolvable through the ladder.

## Character optimization and build comparisons

The assistant audits your current build, then finds compatible characters on
[poe.ninja Builds](https://poe.ninja/poe1/builds). Direct peers match the exact main skill and
its delivery mode, the league/mode, and all uniques required for the build's mechanics.
Optional uniques do not unnecessarily narrow the search. Functional item variants and
missing dependencies are checked before another character's setup is considered transferable.

The comparison covers gems, passive paths, masteries, jewels, gear and defenses. It separates
attainable changes from alternative archetypes or aspirational equipment, then tests promising
changes in your own PoB. Results include source profiles, applicability, measured gains and
trade-offs when calculations are available. Leaderboard DPS is not your expected improvement.

Full workflow: [Character optimization](.cursor/skills/poe1-expert/optimization.md).

## Item pricing

Paste an item copied in-game. The assistant selects the relevant category guide, compares exact
variants and useful modifier combinations, and inspects current listings. It reports asking-price
ranges and uncertainty rather than treating an expensive listing as a completed sale.

| Category | Guide |
|----------|-------|
| Rare/magic equipment, ordinary and abyss jewels, flasks | [Rares](.cursor/skills/poe1-expert/pricing/rares.md) |
| Unique equipment and unique jewels | [Uniques](.cursor/skills/poe1-expert/pricing/uniques.md) |
| Active, support, Vaal and transfigured gems | [Gems](.cursor/skills/poe1-expert/pricing/gems.md) |
| Normal, influenced, fractured and synthesised bases | [Crafting bases](.cursor/skills/poe1-expert/pricing/bases.md) |
| Cluster bases and finished clusters | [Cluster jewels](.cursor/skills/poe1-expert/pricing/clusters.md) |
| Currency, fragments and stackable consumables | [Bulk items](.cursor/skills/poe1-expert/pricing/bulk.md) |
| Maps, invitations, logbooks and other league items | [Maps and league items](.cursor/skills/poe1-expert/pricing/maps.md) |
| Mercenary Warrants and skill/support combinations | [Mercenaries](.cursor/skills/poe1-expert/pricing/mercenaries.md) |

The [shared pricing workflow](.cursor/skills/poe1-expert/pricing.md) contains the common method.
Category guides contain only their specialized considerations. Methods were adapted from the
supplied `/price` notes; historical prices were not imported as current market facts.

## One source of instructions

All PoE rules live in [the canonical skill](.cursor/skills/poe1-expert/SKILL.md) and its linked
references. The `.cursor` directory is retained for existing skill discovery; the content is shared.

| Client | Entry point |
|--------|-------------|
| Cursor | `.cursor/skills/poe1-expert/SKILL.md`; invoke `/poe1-expert` or ask a PoE1 question |
| Claude Code | [CLAUDE.md](CLAUDE.md) imports `AGENTS.md` |
| ChatGPT/Codex with repository access | [AGENTS.md](AGENTS.md) directs the assistant to the canonical skill |

Open this repository as the working project. Edit the canonical files to change behavior;
keep the entry points as redirects without copied rules. See the official documentation for
[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and
[Claude imports](https://code.claude.com/docs/en/memory#import-additional-files).

For chats without repository access, provide the skill and the relevant reference files as
context. A local path alone does not expose its contents, and loading instructions does not
connect the PoB server.

## Setup

### 1. Prepare the environment

Install Git, Node.js with npm, [uv](https://docs.astral.sh/uv/) for the Python helpers, and LuaJIT
for live PoB calculations. For example:

```bash
sudo apt-get install luajit   # Debian/Ubuntu
# macOS: brew install luajit

git clone https://github.com/MatthieuEdelmann/poe1assistant.git
cd poe1assistant
```

### 2. Install Path of Building and pob-mcp

```bash
mkdir -p ~/Projects
git clone https://github.com/PathOfBuildingCommunity/PathOfBuilding.git ~/Projects/PathOfBuilding
./scripts/setup-pob-mcp.sh
```

The setup script clones pob-mcp into `vendor/pob-mcp`, installs its npm dependencies and builds it.
Verify that the installed PoB and pob-mcp data support the current patch before calculating builds.

### 3. Configure the server for your client

[`.cursor/mcp.json`](.cursor/mcp.json) contains the existing `pob` server definition. Its paths
are machine-specific: replace them with your own before use.

| Setting | Value to configure |
|---------|--------------------|
| Server command | `node` |
| Server argument | Absolute path to `vendor/pob-mcp/build/index.js` when the working directory is not this repository |
| `POB_DIRECTORY` | Absolute path to your XML builds folder; use this repository's `builds/` folder if desired |
| `POB_PATH` | Absolute path to `PathOfBuilding/src`, containing `HeadlessWrapper.lua` |
| `POB_CMD` | `luajit`, or its absolute path if unavailable on the client's `PATH` |
| `POB_LUA_ENABLED` | `true` for live calculations |
| `POE_TRADE_ENABLED` | `true` for trade tools |
| `POE_SESSION_ID` | Optional session cookie for weighted trade searches; keep it out of version control |

Cursor uses the project MCP configuration. Claude Code and ChatGPT/Codex need the same server
command and environment registered through their own MCP configuration; they do not automatically
load `.cursor/mcp.json`. Reload the MCP connection after changing configuration.

For weighted BIS searches, supply your `POESESSID` cookie from a logged-in official trade session
through a private client setting or environment. Without it, use ordinary searches and item-upgrade
suggestions. Without a working PoB bridge, the assistant can inspect build data but must identify
calculations it could not perform.

### 4. Verify the connection

Ask the assistant to discover the `pob` tools and call `get_leagues`. Confirm `Covens`, then load
an XML build from `POB_DIRECTORY` and request its stats. League discovery checks market access;
it does not establish that the installed PoB data supports 3.30.

## Command-line helpers

Run commands from the repository root.

### Resolve a ranked character's account

```bash
uv run scripts/find_account.py YourCharacter
uv run scripts/find_account.py YourCharacter 'Hardcore Covens'
```

The default is `Covens`. An explicit league overrides it. If the character is not found on the
ladder, provide the account name directly. Details: [Character lookup](.cursor/skills/poe1-expert/character.md).

### Query trade and save evidence

```bash
uv run scripts/trade_search.py '{"query":{"name":"Tabula Rasa","status":{"option":"securable"}},"sort":{"price":"asc"}}' Covens --save /tmp/poe-tabula.json
uv run scripts/trade_search.py - 'Hardcore Covens' < query.json
```

The helper preserves the requested status and sort, fetches up to ten listings, and displays
special modifiers and mercenary supports under their parent skills. `--save` writes a new JSON
file containing the league, timestamp, query, search URL, total and raw fetched listings.
Use a different filename for each comparison step; existing evidence is never overwritten.

Request spacing is shared between helper invocations through a local SQLite cache. Quota headers
and HTTP 429 responses can defer calls; retries and automatic waiting are bounded. Other MCP
clients do not share this helper's local quota state. Details: [Trade guide](.cursor/skills/poe1-expert/trade.md).

## Validation and updates

Offline checks:

```bash
uv run tests/check_trade_search.py
uv run scripts/find_account.py --self-check
```

Optional PoB integration smoke test after dependency setup:

```bash
(cd vendor/pob-mcp && POB_PATH=~/Projects/PathOfBuilding/src npm run test:smoke)
```

To update clean dependency checkouts:

```bash
git -C ~/Projects/PathOfBuilding pull --ff-only
git -C vendor/pob-mcp pull --ff-only
./scripts/setup-pob-mcp.sh
```

Substitute the actual PoB checkout if different, then reload the MCP connection. The setup script
rebuilds an existing pob-mcp checkout but does not pull its updates. Changing a market league does
not update PoB's tree, gems or item data.

## Reference index

- [Shared skill](.cursor/skills/poe1-expert/SKILL.md)
- [Covens of Umbra / 3.30](.cursor/skills/poe1-expert/covens.md)
- [Character optimization and peer comparisons](.cursor/skills/poe1-expert/optimization.md)
- [Character lookup and import](.cursor/skills/poe1-expert/character.md)
- [Pricing workflow and category routing](.cursor/skills/poe1-expert/pricing.md)
- [Trade tools and query mechanics](.cursor/skills/poe1-expert/trade.md)
- [Source and API reference](.cursor/skills/poe1-expert/reference.md)
- [Historical Allflame / 3.29 reference](.cursor/skills/poe1-expert/allflame.md)

## Historical examples: Allflame 3.29

The records below and [`builds/labcummer.*`](builds) belong to the previous league. They illustrate
past sessions, not current prices, available listings or 3.30 DPS. The original results are retained
for context; rerun the queries and calculations before applying any recommendation today.

<details>
<summary>Show the two historical worked examples</summary>

### Example 1: "what is my next 50 div upgrade?"

A real session against the `labcummer` build in [`builds/`](builds) — a level 92 Deadeye running
Lightning Arrow with Trinity.

> **Prompt:** what is the next 50div upgrade for my character labcummer with pob, show me the DPS improvement

The agent loads the build into a headless Path of Building, measures boss DPS, then tests one change
at a time against live trade listings. Nothing is estimated from memory — every number below came out
of the PoB engine.

#### The answer

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

#### Why the quiver, and which one

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

#### What it refused to buy

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

### Example 2: "which unique body armours are worth 6-linking?"

An economy question rather than a build question — no character involved.

> **Prompt:** look for unique body armour and 6link equivalent, give me list of the highest price delta

The agent pulled every unique body armour poe.ninja tracks in Allflame, paired each armour's
unlinked line with its 6-link line, and ranked by the gap. It then swept all 92 socketable unique
chests against the live trade API as a cross-check.

#### The finding: there is barely a list

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

#### Why poe.ninja and not live listings

The live 6-link market is too sparse to rank: of 92 socketable uniques swept on the trade API,
**82 had no online 6-link listing at all**, and most of the rest had one or two. `Carcass Jack` makes
the case — a single live listing at 5000c against a poe.ninja value of 388c drawn from 50 listings.
Ranking on live listings would have put one overpriced item at the top.

The same caution applies inside the poe.ninja data. The largest raw delta in the set,
`Greed's Embrace` at +1012c, rests on two listings, and a live search found one at 150c. Anything
under five listings a side is an anecdote, so the agent reports those separately instead of ranking
them.

</details>
