# clearlabwebsite

Public pages for the **CLEAR Lab**, served by GitHub Pages from `main`.

- **Live:** https://eisenlohrmoul.github.io/clearlabwebsite/
- **Public URL:** https://www.clearlabresearch.com

## Layout

```
/           the landing page: what the lab studies, three research cards,
            the roster, and the upcoming PINES trial
/pines/     the PINES study site: a hub plus four audience pages
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

The wall signage is **not part of this site**. It lives on the `lab-signage`
branch, deliberately off `main`, because Pages serves everything on `main` from
the root — anything committed here is live on the public web.

    git checkout lab-signage    # signs/posters-11x17.html, signs/README.md

`tools/build_index.py` belonged to that workflow and moved with it.

## Notes

- `.nojekyll` — keep; required for Pages to serve the files verbatim.
- Fonts: Hanken Grotesk and Schibsted Grotesk, via Google Fonts.
- The Notion wiki "The CLEAR Lab" is separate and unaffected by this repo.
