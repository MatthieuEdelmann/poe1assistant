# Item pricing

Use this workflow when the player pastes an item copied in-game or asks what to sell it for.
Read only the relevant category sheet. For query construction, use [trade.md](trade.md);
for endpoints and response fields, use [reference.md](reference.md).

| Item | Sheet |
|------|-------|
| Rare or magic equipment, ordinary and abyss jewels, flasks | [Rares](pricing/rares.md) |
| Unique equipment, unique jewels, relics and tinctures | [Uniques](pricing/uniques.md) |
| Active, support, Vaal and transfigured gems | [Gems](pricing/gems.md) |
| Normal, influenced, fractured or synthesised crafting bases | [Bases](pricing/bases.md) |
| Cluster jewel bases and finished clusters | [Clusters](pricing/clusters.md) |
| Stackable currency, fragments and consumables | [Bulk](pricing/bulk.md) |
| Maps, invitations, logbooks, contracts and other league items | [Maps and league items](pricing/maps.md) |
| Mercenary Warrants | [Mercenaries](pricing/mercenaries.md) |

## Shared method

1. Read the copied item's class, rarity, name, base, item level, rolls, sockets/links,
   quality and special states. Ask for missing details that could change the comparison.
   Confirm the player's league using the shared skill's league guidance.
2. For supported categories, inspect the matching poe.ninja variant and its sample size.
   Fewer than ten listings is a caution signal, not a hard validity threshold. Rares need
   live comparables; a generic base price does not value the finished item.
3. Build a comparison ladder: base/category and rarity first, then one distinguishing
   property at a time. Record the filters, listing count and low asking prices at each step.
   Finish with all relevant properties together: combinations can matter when individual
   modifiers do not. Only run steps that resolve a real pricing uncertainty.
4. Fetch the cheapest 6–10 results where available; inspect at least 2–3 usable comparables,
   seller diversity, listing age, rolls and unsupported properties. Separate inferior items
   from equal-or-better ones. State when the sample is smaller or dominated by one seller.
5. If the full combination has no comparable listings, its price remains unknown.
   A broader search is context, not a proven minimum or evidence of a premium. Do not infer
   a sale price from one expensive listing or from rarity alone.
6. Report an asking-price range and a suggested listing price with confidence and a trade
   link. Distinguish asking prices from completed sales. Explain likely liquidity only when
   the data supports it; never promise a sale time. Convert chaos/divine using a current rate.

Use `securable` for instant-buy comparisons and other statuses for the corresponding market;
label the choice and keep it consistent across steps. Do not mix markets to manufacture a floor.
For low-value items, keep the answer short and consider bulk selling or keeping the item.

The helper's `--save` option preserves the raw query and listings with league and timestamp.
Use distinct filenames per step. Historical anecdotes inspired these methods but are not current
price evidence. Do not automatically rewrite category rules after each valuation; retain reusable
lessons only when requested, with their date, league and evidence, separate from enduring mechanics.
