# Skill gems

Apply the [shared pricing method](../pricing.md).

- Resolve the exact skill or support name. Supports generally include `Support` in their
  trade type; transfigured and Vaal versions must not be merged with the normal skill.
- Match level, quality and corruption state in the poe.ninja `SkillGem` rows. Read explicit
  fields as well as the variant label; a bare name is insufficient.
- For levels or qualities between tracked variants, query the actual item on trade.
  Nearby tracked variants provide context, not an automatic interpolation or lower bound.
- Verify current gem-level, quality, corruption and transfiguration filters against trade
  metadata. Fetch listings to confirm that the returned gems match the intended version.
- A high aggregate value from one listing is an outlier candidate, not a recommendation.
  State when exact matches are unavailable or the market has too few independent sellers.

Check current patch notes before claiming corruption limits, vendor recipes or whether
leveling/quality investment is profitable. Do not reuse a prior league's empty search as
proof that a gem cannot be bought now.
