"""Turn the finished media-archive page into the website's /media/ page.

The archive is drawn in its own folder (media-mentions/build_media_page.py writes
media_mentions.html). That file is a page body without the outer wrapper a website
page needs, so this adds the wrapper and the site's menu bar, and saves it here as
media/index.html. Nothing in the archive's content is changed.

Run after the archive is redrawn:
    python3 media/build_from_archive.py            (from the clearlabwebsite folder)
    python3 media/build_from_archive.py <path to media_mentions.html>
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = HERE.parents[1] / "media-mentions" / "media_mentions.html"
OUT = HERE / "index.html"

# The site's menu bar, styled with the archive's own colour names so it follows
# the archive's light and dark modes. Not sticky: the archive's filter bar is.
NAV_STYLE = """
.site-nav { background: var(--paper); border-bottom: 1px solid var(--line); }
.site-nav .in { max-width: 1040px; margin: 0 auto; padding: 9px 20px; display: flex; align-items: center;
  gap: 4px; overflow-x: auto; scrollbar-width: none; }
.site-nav .in::-webkit-scrollbar { display: none; }
.site-nav a { font: 600 13.5px/1 var(--font-body); color: var(--ink-soft); text-decoration: none;
  padding: 7px 11px; border-radius: 7px; white-space: nowrap; }
.site-nav a:hover { background: var(--wash); color: var(--ink); }
.site-nav a[aria-current="page"] { color: var(--ink); background: var(--wash); }
.site-nav a.cta { margin-left: auto; color: var(--red); }
@media (max-width: 560px) { .site-nav a { font-size: 12.5px; padding: 7px 9px; } }
"""

NAV = """<nav class="site-nav" aria-label="CLEAR Lab website"><div class="in">
  <a href="../">CLEAR Lab home</a>
  <a href="../#people">Meet the lab</a>
  <a href="../pines/">PINES trial</a>
  <a href="./" aria-current="page">In the media</a>
  <a class="cta" href="mailto:temo@uchicago.edu">Contact</a>
</div></nav>
"""


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    page = src.read_text()
    split = page.find('\n<div class="wrap">')
    if not page.startswith("<title>") or split < 0:
        sys.exit(f"{src} does not look like the archive page (expected it to start with <title> "
                 f"and contain <div class=\"wrap\">); nothing written.")
    head, body = page[:split], page[split:]
    head = head.replace("<title>Eisenlohr-Moul in the Media</title>",
                        "<title>In the Media | CLEAR Lab</title>", 1)
    head = head.replace("</style>", NAV_STYLE + "</style>", 1)
    OUT.write_text(
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<meta name=\"description\" content=\"News, radio, podcasts, talks and books featuring "
        "Dr. Tory Eisenlohr-Moul and the CLEAR Lab's research.\">\n"
        "<link rel=\"icon\" href=\"../assets/pines-badge.svg\">\n"
        f"{head}\n</head>\n<body>\n{NAV}{body}\n</body>\n</html>\n")
    print(f"wrote {OUT.relative_to(HERE.parent)} from {src}")


if __name__ == "__main__":
    main()
