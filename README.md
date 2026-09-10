# clearlabwebsite

Public pages for the **CLEAR Lab**, served by GitHub Pages from `main`.

- **Live:** https://eisenlohrmoul.github.io/clearlabwebsite/
- **Public URL:** https://www.clearlabresearch.com

## Layout

```
/           holding page — "the website is being rebuilt", links out to PINES
            and the lab wiki
/pines/     the PINES study site: a hub plus four audience pages
/signs/     the printable "CLEAR Lab Signs" sheets (was at the root until
            Sept 2026)
/assets/    logos, headshots, the PINES badge
```

## How the domain resolves

```
www.clearlabresearch.com
  -> bit.ly/clearlabresearch            (Bitly short link "The CLEAR Lab")
  -> https://eisenlohrmoul.github.io/clearlabwebsite/
```

Nothing about the domain lives in this repo. To move the public URL, edit the
Bitly destination. DNS is on Squarespace and does not need touching.

## The PINES pages

See `pines/COPY.md` for the plain-text source of every page, the hormone
naming convention, and the reason the participant page is a deliberate dead
end (recruitment framing). Unfilled items are HTML comments — search the
files for `TO FILL IN`.

## The signs page

A fixed-width print layout (two letter-size sheets), intentionally not
responsive. It is designed in Claude's design tool, not hand-edited. To
publish a new version:

1. Save the "CLEAR Lab Signs" design from the browser to
   `~/Desktop/CLEAR Lab Signs.htm`.
2. `python3 tools/build_index.py` — writes `signs/index.html`, strips the
   browser-extension junk, and swaps in real Google Fonts links.
3. Copy new images from `CLEAR Lab Signs_files/` into `assets/`.
4. Commit and push; Pages redeploys in about a minute.

Note that `build_index.py` still writes to the repo root by default. Point it
at `signs/index.html`, and remember that the page references assets as
`../assets/` now that it is one level down.

## Notes

- `.nojekyll` — keep; required for Pages to serve the files verbatim.
- Fonts: Hanken Grotesk and Schibsted Grotesk, via Google Fonts.
- The Notion wiki "The CLEAR Lab" is separate and unaffected by this repo.
