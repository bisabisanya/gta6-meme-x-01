// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: a GTA 6 meme (meme.png, made by this
// agent with make_meme.py) posted from a public X account with make.fun
// and the entrant's play code in its text. This program does the one
// thing the gate needs: it copies POST.json from the repository root to
// /output/POST.json, where the house reads the post's address and builds
// the dossier the judge sees. Nothing this program writes is judged.
//
// Deterministic: a byte-for-byte copy, no network, no clock, no files
// outside the repository. Run it twice, get the same bytes twice.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and
// MAKEFUN_OUTPUT_DIR stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const src = join(BOT_DIR, 'POST.json');
const dst = join(OUTPUT_DIR, 'POST.json');

mkdirSync(OUTPUT_DIR, { recursive: true });

// Read the whole file first so a missing or malformed POST.json fails
// here, loudly, instead of writing a partial copy. Only the shape is
// checked (an object with a string url); the house validates the address
// itself when it reads the post from X, so this program never has to
// know what a good post address looks like.
const data = readFileSync(src);
const post = JSON.parse(data.toString('utf8')) as unknown;
if (typeof post !== 'object' || post === null || typeof (post as { url?: unknown }).url !== 'string') {
  console.error(`POST.json at ${src} must be a JSON object with a string "url" field`);
  process.exit(1);
}

writeFileSync(dst, data);
