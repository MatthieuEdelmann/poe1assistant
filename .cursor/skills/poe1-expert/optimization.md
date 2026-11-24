# Character optimization with comparable builds

Use this workflow for character audits, progression advice and build optimization. Compare
the player's build with compatible characters on [poe.ninja Builds](https://poe.ninja/poe1/builds),
then validate promising changes in the player's own PoB. This is a build-analysis workflow;
item valuation remains in [pricing.md](pricing.md).

## Establish the player's build

Load the current build using [character.md](character.md) and the shared skill's PoB workflow.
Record the baseline, intended content, level, available passive points and any stated budget.
Identify:

- The actual main damage skill, including its exact transfigured/Vaal variant and delivery
  mode: self-cast, triggered, totem, trap, mine or minion. A utility gem appearing in the
  character's links does not make it the main skill. Record separate clear/boss setups if used.
- The ascendancy, damage-scaling mechanism and defensive model, including dependencies such
  as conversion, critical strikes, ailments, resource stacking or special keystones.
- The build-enabling uniques. For each, explain the mechanic that would stop working without
  it. Popularity alone does not make an item mandatory. Separate equipped requirements from
  a missing enabling item needed for the player's intended archetype.

Check mechanic-sensitive variants, mutated modifiers, jewel effects and relevant roll thresholds;
the same unique name can hide a different functional setup. If a dependency is unclear, verify
it from the build and current mechanics before choosing the comparison group.

## Find compatible peers on poe.ninja

1. Select the player's league and mode, with a relevant current snapshot or comparable
   progression snapshot. Record the actual selection; do not silently use Standard, another
   patch or a different league mode when the requested group is sparse.
2. Filter by the exact **main skill** and inspect its links/mode on each candidate profile.
   Match the player's ascendancy by default. A different ascendancy or delivery mode belongs
   in a separately labelled alternative-archetype discussion, not the direct comparison.
3. Require **all build-enabling uniques together**, checking their functional variants on
   the profiles. Do not require every incidental unique the player wears. Conversely, exclude
   peers whose setup depends on additional enabling gear or mechanics the player lacks, or
   explicitly describe the full transition needed before their changes become applicable.
4. Inspect a small representative sample, normally 3–5 profiles when available. Prefer
   attainable progression and similar constraints; include an aspirational example separately
   if useful. Do not select only the highest displayed DPS or treat expensive gear as required.
5. Keep the filtered search URL, each inspected character URL, snapshot/retrieval date and
   matching rationale. Report how many compatible profiles were actually inspected. Site-wide
   popularity or a small sample is not proof that a choice is optimal.

Use the site's visible filters, public character pages and offered PoB export/import controls.
Its [API documentation](https://poe.ninja/docs/api) identifies builds/profile endpoints as internal
and unavailable for third-party use; do not implement a scraper against those endpoints. If the
site cannot be read with available browsing tools, say so and request a public profile link or
PoB export when needed. Do not invent peers or claim a completed comparison from search snippets.

If no exact peers exist, show which constraints failed. Broaden level or optional equipment
first. Retain the main skill and enabling uniques for direct peers; label any relaxation of
those requirements as a different archetype rather than silently mixing the results.

## Compare and test changes

Compare actual differences in skill links and gem levels/quality, passive paths and masteries,
ascendancy choices, jewels/clusters, anoints, auras/reservation, gear modifiers, flasks and
relevant league-specific or companion effects. Look for missing interactions and attainable
improvements, not a wholesale copy of another character's equipment.

- Separate extra character levels/passive points and investment from better allocation.
  Check resistances, attributes, resource sustain, reservation, accuracy and defensive losses.
- Keep imported peer builds separate from the player's saved baseline. Website DPS/EHP values
  are discovery signals, not directly comparable upgrade measurements.
- Test one transferable change at a time in a copy of the player's PoB. Test coupled changes
  together only when the mechanic requires them, and disclose the dependency bundle.
- Use the same enemy, encounter and calculation version for before/after measurements.
  Keep charges, buffs, flasks, ailments, minion counts and conditional effects justified by
  what each configuration can actually sustain; do not copy unsupported peer assumptions.
- Report measured damage/defense changes and trade-offs. When PoB lacks an effect or cannot
  run, distinguish qualitative observations from unverified hypotheses; do not invent gains.

## Deliver the recommendation

Show the player's build identity and mandatory-unique rationale, then a compact comparison:
peer link, why it matches, relevant difference, applicability and measured result when available.
Finish with prioritized changes, dependencies and rejected suggestions with a concrete reason.
Keep direct peer observations, local PoB measurements and speculative alternatives distinguishable.
Use trade/pricing workflows only if an accepted improvement needs a purchase or cost estimate.
