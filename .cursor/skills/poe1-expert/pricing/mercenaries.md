# Mercenary Warrants

Apply the [shared pricing method](../pricing.md). These items require inspection beyond
ordinary stat filters: a support appearing somewhere on a warrant is not enough.

1. Resolve the warrant's current build type and discriminator through trade item metadata.
   Distinguish normal and Infamous variants. Retain the mercenary's level and all skills.
2. Establish the build's base market, then add meaningful skill combinations, variant and
   relevant support tiers. Query the complete combination before drawing a conclusion.
3. Resolve skill/support stat IDs from the current `mercenary` stat category. Do not infer
   IDs or tier hashes from old notes. Check whether a filter expresses attachment to a skill;
   if it only requires a support anywhere on the warrant, the query is deliberately broader.
4. Inspect `mercenarySkills[].supports` in every fetched comparable. Verify each valuable
   support's name, tier and parent skill. Exclude or label listings whose support placement
   does not match, even if their search filters are otherwise identical.
5. If the first fetched results have the wrong attachments, refine the query or inspect
   another bounded sample using supported filters. Do not silently treat ten listings as
   the whole market, or keep searching indefinitely to manufacture a precise price.

The fallback script prints supports under their parent skill and can save the raw listings.
For a scarce combination, report the number of genuinely matching listings and distinct
sellers. An empty exact sample does not prove either a high premium or a negligible value.

Historical observations suggest testing support placement and skill synergy together;
they do not establish a permanent premium for Return, Second Wind, Greater Fork or Infamous.
