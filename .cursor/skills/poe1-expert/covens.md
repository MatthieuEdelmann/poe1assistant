# Covens of Umbra (3.30)

Current challenge league, launched **13 November 2026**. Last checked **24 November 2026**.

## League identifiers

| Context | Name |
|---------|------|
| Trade / pob-mcp / poe.ninja economy API | `Covens` |
| Hardcore | `Hardcore Covens` |
| SSF ladder | `SSF Covens` |
| Hardcore SSF ladder | `HC SSF Covens` |
| poe.ninja site slug | `covens` |

Identifiers and launch date were checked against the [official league API](https://api.pathofexile.com/leagues?type=main&compact=1), [trade league list](https://www.pathofexile.com/api/trade/data/leagues) and [poe.ninja](https://poe.ninja/poe1/economy/covens/currency).
Use `get_leagues` before trade searches. SSF has no trade market; do not turn an SSF character lookup into a shopping recommendation.

## League loop and endgame

- Disrupt covenite rituals, then choose **Fates** to increase the area boss's difficulty and rewards.
- Defeat empowered bosses for **Viscera** to place on your **Wickerman**, granting character power.
- **Threads replace Scarabs**. Spending Threads at the Map Device enables associated mechanics and can add random effects; Shaped Regions provide free Threads.
- **Memory Threads** are now **Memory Traces**; distinguish these from the new map-device Threads.
- Item generation and the Atlas changed. Recheck farming assumptions, map availability and crafting recipes before reusing a 3.29 strategy.

Source: [official 3.30.0 patch notes](https://www.pathofexile.com/forum/view-thread/4013680). Expansion page: [Covens of Umbra](https://www.pathofexile.com/covens).

## Post-launch changes

**3.30.0d (19 November)** adjusted currency rarity scaling, added Foulborn currencies to core drops, and introduced Originator's and Primordial Exalted Orbs. Covens outcomes guaranteeing a single Divine Orb or Orb of Annulment now need two matching copies instead of three. Thread rewards and several endgame encounters also changed. Use these updated rules when assessing farming or crafting.

Source: [3.30.0d patch notes](https://www.pathofexile.com/forum/view-thread/4017726).

The latest entry checked was [3.30.0d Hotfix 3 (22 November)](https://www.pathofexile.com/forum/view-thread/4019056), a Windows 7 launch fix. Recheck the [patch-note index](https://www.pathofexile.com/forum/view-forum/patch-notes) for subsequent changes; do not treat announced changes as shipped until patch notes confirm them.

## Build calculations and economy

- Verify installed PoB and pob-mcp data compatibility with **3.30**; live league discovery only validates the market identifier.
- Reimport the player's current character and confirm tree, gems, items and Wickerman effects are represented before reporting DPS or defenses. State any unsupported effects explicitly.
- Bundled `builds/labcummer.*` and README measurements belong to Allflame. Do not relabel them as Covens benchmarks.
- Query current Covens prices and listings. Old price ratios, mod ceilings and empty searches are historical observations, not current market facts.
- Keep [allflame.md](allflame.md) for historical questions only; it does not establish which old league mechanics remain available in 3.30.
