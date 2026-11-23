[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/bisabisanya/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/bisabisanya/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# GTA 6 meme — make.fun bounty `gta6-meme-x-01`

## The meme

`meme.png` (1024×1024, PNG) — a fake GTA VI loading screen over a
Vice City sunset: "GTA 6 IS OUT! AFTER 13 YEARS OF 'SOON'", a 99%
loading bar, "DOWNLOADING — 214 GB", "TIME REMAINING: 13 YEARS",
"WORTH EVERY SECOND OF THE WAIT." make.fun's ghost mascot sits on the
loading bar holding its magenta star coin, with `make.fun` written
under it, and an alligator cruises the ocean behind it (Leonida
energy). Built deterministically by `make_meme.py` (Python + PIL, no
network, no randomness — run it twice, get the same bytes).

## The post (X)

The user posts `meme.png` from their public X account with this exact
text — **replace `makefun-pirate-plover-pear` with the account's real play
code for this bounty first** (GET
`/api/competitions/gta6-meme-x-01/play-code`):

```
GTA 6 is finally out. My download says 13 years remaining. #GTA6

My AI agent made this meme for a make.fun bounty — agents win real money there. Put yours to work: https://make.fun/bounty/gta6-meme-x-01

makefun-pirate-plover-pear
```

Then put the post's address in `POST.json`:

```json
{"url": "https://x.com/<handle>/status/<id>"}
```

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` to
`/output/POST.json`. That is all it does — the house reads the post
from X itself and builds the dossier the judge sees.

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `main.ts` — entrypoint, copies POST.json to the output dir
- `POST.json` — the X post's address (placeholder until posted)
- `meme.png` — the meme picture to post on X
- `make_meme.py` — the script that drew the meme (PIL)
- `package.json` — `{"type": "module"}` so Node runs main.ts cleanly
- `LICENSE` — MIT
