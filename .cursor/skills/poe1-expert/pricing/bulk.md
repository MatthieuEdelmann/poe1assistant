# Stackable items and bulk exchange

Apply the [shared pricing method](../pricing.md), using unit prices and quantities rather
than equipment modifiers. This includes currency, fragments, divination cards, essences,
fossils, oils, tattoos, omens, Threads and other supported consumables.

- Use the poe.ninja exchange endpoint in [reference.md](../reference.md) for the relevant
  category only. Inspect the response's currency basis and item-ID mapping before treating
  a numeric value as chaos. Volume indicates activity, not guaranteed liquidity for your lot.
- Match the exact item, then report the unit price and stack total. Check minimum lot sizes,
  seller stock and bulk premiums/discounts instead of blindly multiplying a single-item quote.
- Resolve bulk identifiers with `https://www.pathofexile.com/api/trade/data/static`.
  An empty ordinary item search does not establish that an exchange-traded item is unavailable.
- Cross-check unusual aggregates against executable offers with the correct exchange
  direction and quantities. Neither the first exchange offer nor an aggregate is inherently
  authoritative; explain discrepancies instead of always discarding one source.
- Fetch the current divine/chaos rate in the same league when converting values. If the rate
  is absent or ambiguous, report the original currency rather than dividing by a missing value.

`Thread` is a candidate exchange category from the supplied 3.30 notes; verify current
availability before use. Empty categories and ended leagues require explicit handling, not
an automatic switch to Standard. Use historical exports only for historical questions.
