# clearlabwebsite

Public homepage for the **CLEAR Lab** — a designed one-page site ("CLEAR Lab
Signs": a "Welcome" sheet and a "Meet the Lab" sheet).

- **Live site:** https://eisenlohrmoul.github.io/clearlabwebsite/
- **Public URL:** https://www.clearlabresearch.com

## How it's served (the domain chain)

```
www.clearlabresearch.com
  -> bit.ly/clearlabresearch            (Bitly short link "The CLEAR Lab")
  -> https://eisenlohrmoul.github.io/clearlabwebsite/   (GitHub Pages, this repo)
```

GitHub Pages serves this repo's `main` branch from the root. `.nojekyll` tells
Pages to serve the files verbatim (no Jekyll processing).

To move the public URL somewhere else later, edit the destination of the Bitly
link `bit.ly/clearlabresearch` — nothing about the domain lives in this repo.

## Files

- `index.html` — the page (single file, ~50 KB).
- `assets/` — logo, the `menstrualcycleR` badge, `pines-badge.svg`, and 15
  headshots (`ph-*.webp`). Every file here is referenced by `index.html`.
- `.nojekyll` — keep; required for Pages to serve as-is.
- `tools/build_index.py` — regenerates `index.html` from a fresh design export.

## Updating the design

The page is designed in Claude's design tool, not hand-edited here. To publish a
new version:

1. In Claude, open the "CLEAR Lab Signs" design, then **save the page from the
   browser** to `~/Desktop/CLEAR Lab Signs.htm` (this also writes a
   `CLEAR Lab Signs_files/` folder of images next to it).
2. Regenerate the page:
   ```
   python3 tools/build_index.py
   ```
   (Defaults to `~/Desktop/CLEAR Lab Signs.htm` -> `index.html`. The script
   strips the ~3.4 MB of browser-extension junk and swaps in real Google Fonts
   links. It fails loudly if the output still contains junk.)
3. Copy any new/changed images from `CLEAR Lab Signs_files/` into `assets/`
   (keep the exact filenames).
4. `git add -A && git commit && git push` — Pages redeploys automatically in ~1 min.

## Notes

- The design is a **fixed-width print layout** (two letter-size sheets). It is
  intentionally **not** mobile-responsive — that's by design, not a bug.
- Fonts: Inter, DM Mono, Hanken Grotesk, Schibsted Grotesk (all Google Fonts,
  loaded via `<link>` in the `<head>`).
- The Notion wiki "The CLEAR Lab" is separate and unaffected by this repo.
