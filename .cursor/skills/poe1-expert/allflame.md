# Curse of the Allflame (3.29)

Current challenge league. Launched **24 July 2026** with patch **3.29.0**.

Official overview: https://www.pathofexile.com/allflame  
Patch notes: https://www.pathofexile.com/forum/view-thread/3985332

## League names (use exact strings)

| Context | Name |
|---------|------|
| poe.ninja economy API | `Allflame` |
| Trade / pob-mcp | `Allflame` (confirm with `get_leagues` if trade fails) |
| Hardcore | `Hardcore Allflame` |
| Player-facing shorthand | Curse of the Allflame, Allflame |

Default to **`Allflame`** for prices, trade, and economy unless the user specifies HC/SSF.

## Core league loop

1. **Lost Charts** drop from map monsters.
2. Board **The Sovereign** (Valerie's ship) and chart seafloor areas.
3. Explore the seafloor — Allflame lanterns protect from pressure; loot gold, chests, threats.
4. Combine charts into a **Voyage** — revisit charts for amplified rewards.
5. **Allflame Crafting** (belowdecks) — feed an item; pick one ghostly outcome.
6. **Ducats** — league currency from the seafloor; used for Allflame crafting twists.

## Build-relevant 3.29 changes

Assume PoB and pob-mcp are on **3.29** data. When advising builds, weight these meta shifts:

### Ascendancy / class

- **Reliquarian** (Scion Bloodline) — notables shuffled for Allflame; verify current tree in PoB.
- **Luminary** — mercenary-based play; Valdo "less damage per equipped item" mod applies to merc + their minions.
- Two new **Bloodline Classes** (one league-exclusive).
- **Scion** playable from account creation (no Act 3 unlock).

### Mechanics reworks

- **Mercenaries of Trarthus** — core league; Trarthan Scarabs on the atlas.
- **Abyss** — higher-tier abyssal jewel rolls buffed.
- **Legion** — timeless emblem modifiers reworked (XP, reward progress, revived-monster scaling).
- **Talisman** — enchantments replace implicits; Bestiary/Beast crafting focus; old bases unobtainable.
- **Ultimatum** — sole source of Catalysts (removed from Heist/Expedition/Ritual).

### Crafting / gear

- **Socket colours** — new bench crafts: 2/3/4 non-white sockets (5/20/75 chromatics).
- **Vorici Betrayal** — rank 1 reforges socket *count*; rank 2 reforges non-white *colours*.
- Crafting bench: reroll 3 random rare mods (3c), reroll 1 random rare mod (8c).
- **Pearlescent Amulet** — new base with all-element res implicit.

### Self-cast / spells (meta-relevant)

- New keystones near Witch: **Bitter Frost**, **Roiling Tempest**, **Voracious Flame** (element-lock keystones).
- Tree: "reduced cost" → **Cost Efficiency** conversion.
- New Exceptional gems: Pact of Beidat/Ghorr/K'tash/Lycia; Coursing Currents, Crystalfall supports.
- New skills: Mana-Infused Staff; transfigured Holy/Reap variants.

### Betrayal / economy notes

- Syndicate leaders no longer drop Allflame Embers; Mastermind drops **Allflame Ember of Kulemak** only.
- Catalyst economy shifted to Ultimatum — factor into farming advice.

## PoB / pob-mcp

- pob-mcp targets **3.29** — use `get_leagues` for trade, never hard-code an old league.
- For boss DPS in this league, confirm pinnacle targets (new endgame content in 3.29) via poewiki or patch notes before setting `set_enemy_stats`.

## Wiki pages (when poewiki is reachable)

- `Curse_of_the_Allflame`
- `Allflame_Crafting`
- `Ducat`
- `Lost_Chart`
- `Reliquarian`
- `Luminary`
- `Mercenaries_of_Tarthus`
