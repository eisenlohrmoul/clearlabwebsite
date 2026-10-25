"""Turn the finished media-archive page into the website's /media/ page.

The archive is drawn in its own folder (media-mentions/build_media_page.py writes
media_mentions.html). That file is a page body without the outer wrapper a website
page needs, so this adds the wrapper and the site's menu bar, and saves it here as
media/index.html. Nothing in the archive's content is changed.

It also lifts the preview pictures out of the page. The archive page carries all
83 of them inside the HTML itself, which is how a Claude artifact has to do it, and
that alone is 2.2 MB of the 2.4 MB page: a phone downloads every picture before it
sees a word, and the "only load this when it scrolls into view" note already on 82
of them can never do anything, because an embedded picture arrives with the page
whether or not anyone scrolls to it. Here each one is written out as its own file
in media/thumbs/ and the page points at it, so the page itself is about 220 KB and
the pictures arrive as the reader reaches them. Each picture's real size is written
into the page too, so the text does not jump around while they load.

Run after the archive is redrawn:
    python3 media/build_from_archive.py            (from the clearlabwebsite folder)
    python3 media/build_from_archive.py <path to media_mentions.html>
"""
import base64
import hashlib
import io as _io
import re
import sys
from pathlib import Path

from PIL import Image

THUMBS = "thumbs"
EXT = {"jpeg": "jpg", "jpg": "jpg", "png": "png", "gif": "gif",
       "webp": "webp", "svg+xml": "svg"}


def externalize_images(page, outdir):
    """Write each embedded picture to its own file and point the page at it.

    Returns (page, number written, bytes moved out of the page).
    """
    outdir.mkdir(parents=True, exist_ok=True)
    written, moved, keep = {}, 0, set()

    def one_tag(m):
        nonlocal moved
        tag = m.group(0)
        d = re.search(r'src="data:image/([a-z+]+);base64,([A-Za-z0-9+/=]+)"', tag)
        if not d:
            return tag
        fmt, b64 = d.group(1), d.group(2)
        try:
            raw = base64.b64decode(b64 + "=" * (-len(b64) % 4))
        except Exception:
            return tag                       # leave anything we cannot decode alone
        name = f"{hashlib.sha1(raw).hexdigest()[:12]}.{EXT.get(fmt, 'img')}"
        keep.add(name)
        if name not in written:
            (outdir / name).write_bytes(raw)
            written[name] = True
        moved += len(b64)
        tag = tag.replace(d.group(0), f'src="{THUMBS}/{name}"')
        if "width=" not in tag and fmt != "svg+xml":
            try:
                w, h = Image.open(_io.BytesIO(raw)).size
                tag = tag[:-1].rstrip() + f' width="{w}" height="{h}">'
            except Exception:
                pass
        # Do not add "load this only when it scrolls into view" to a picture the
        # archive left without it -- that is the banner at the very top, which
        # should start downloading immediately, and 82 of the 83 already say it.
        if "decoding=" not in tag:
            tag = tag[:-1].rstrip() + ' decoding="async">'
        return tag

    page = re.sub(r"<img[^>]*>", one_tag, page)
    for stale in outdir.glob("*"):           # the folder is generated; prune what left
        if stale.is_file() and stale.name not in keep:
            stale.unlink()
    return page, len(written), moved

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
    body, n_img, moved = externalize_images(body, OUT.parent / THUMBS)
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
    size = OUT.stat().st_size
    print(f"wrote {OUT.relative_to(HERE.parent)} from {src}")
    print(f"  page {round(size/1024)} KB; {n_img} pictures moved out into "
          f"{THUMBS}/ ({round(moved/1024)} KB of embedded text removed)")


if __name__ == "__main__":
    main()
