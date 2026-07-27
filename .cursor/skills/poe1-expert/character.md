# Getting a character's build from their PoE account

Every character lookup needs the **account name**, not the character name. Get it before anything else — without it, `poe.ninja` and Path of Building both return 404 and you end up guessing.

## Account name format

Since 2023 account names carry a discriminator: `Name#1234` (e.g. `Poteitik#3151`).

- The `#` **must** be URL-encoded as `%23` in every API call.
- The character name is *not* the account name. `labcummer` is a character; its owner is a separate `Name#1234`.

## How to resolve the account name

Try these in order and stop at the first that works.

### 1. Ask the user (preferred)

Ask once, then reuse it for the whole conversation. Tell them where to find it:

> In game, open the social panel — your name is shown as `Name#1234`. It's also the last part of your profile URL at `pathofexile.com/account/view-profile/...`.

Do not guess the discriminator. There is no way to derive it from the character name.

### 2. Search the league ladder

Works only if the character is ranked (top 15,000 by experience in the league) and the account is public. The ladder maps character name to account name:

```
https://www.pathofexile.com/api/ladders?id={LEAGUE}&limit=200&offset={N}
```

- No authentication required.
- `limit` caps at 200; page with `offset` up to `total` (15,000 in Allflame).
- Each entry has `character.name` and `account.name`.

Use `scripts/find_account.py <character-name>` in this repo to page through it.

### 3. Read it off a trade listing

If the user linked an item they are selling, the trade API's `listing.account.name` is already in `Name#1234` form. Narrow, but free when it applies.

## Pulling the build once you have the account

All three endpoints are **public and unauthenticated** for accounts with a public profile. Add `realm=pc` (or `xbox` / `sony`).

| Endpoint | Returns |
|----------|---------|
| `https://www.pathofexile.com/character-window/get-characters?accountName={ACCT}&realm=pc` | Every character: name, class, league, level |
| `https://www.pathofexile.com/character-window/get-items?accountName={ACCT}&character={CHAR}&realm=pc` | Full equipped gear, sockets, mods, jewels |
| `https://www.pathofexile.com/character-window/get-passive-skills?accountName={ACCT}&character={CHAR}&realm=pc` | Allocated tree hashes, mastery choices, jewel data |

Example (note the encoded `#`):

```bash
curl -s 'https://www.pathofexile.com/character-window/get-characters?accountName=Poteitik%233151&realm=pc'
```

If these return `403` or an empty character list, the profile is **private**. Ask the user to either make it public (Privacy Settings on the site) or supply `POE_SESSION_ID`.

## Getting it into Path of Building

`pob-mcp` has no character-import tool — do not look for one. Two working routes:

1. **Ask the user to import and export.** In Path of Building: `Import/Export Build` → `Import from site` → paste the account name → pick the character → then `Share` → copy the build code. This is the most reliable route and it costs the user about thirty seconds.
2. **Reconstruct from the API.** Fetch gear and passives from the endpoints above and build the PoB XML yourself. Slower and easy to get wrong on tree nodes; only worth it when the user cannot use the game client.

Save the resulting build to `builds/{character}.xml` so `lua_load_build` can find it — `POB_DIRECTORY` points at this repo's `builds/` folder.

## Do not

- Do not attempt to search poe.ninja by character name alone. Its build endpoint requires `account` **and** `name`; without the account it returns a 400 validation error.
- Do not paste long base64 PoB codes through the model. They get corrupted. Have the user save the code to a file, or write it to `builds/` directly.
