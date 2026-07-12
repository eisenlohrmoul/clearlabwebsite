#!/usr/bin/env python3
"""Regenerate index.html from a browser-saved "CLEAR Lab Signs" .htm export.

The site is designed in Claude's design tool and saved from the browser as a
single .htm file. That saved file is ~3.4 MB, of which ~99% is browser-extension
junk (<plasmo-csui> shadow-DOM blocks injected before the real <head>). The real
page is the ~50 KB from the single <head> to </html>. This script extracts that,
repoints image paths to assets/, and swaps in real Google Fonts <link>s.

Usage:
    python3 tools/build_index.py [SRC.htm] [OUT.html]

Defaults:
    SRC = ~/Desktop/CLEAR Lab Signs.htm
    OUT = index.html   (repo root)

After running, also copy any new/changed images from the export's
"CLEAR Lab Signs_files/" folder into assets/ (same filenames). See README.
"""
import os
import re
import sys

DEFAULT_SRC = os.path.expanduser("~/Desktop/CLEAR Lab Signs.htm")
SRC = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
OUT = sys.argv[2] if len(sys.argv) > 2 else "index.html"

s = open(SRC, encoding="utf-8", errors="replace").read()
html_open = re.search(r"<html\b[^>]*>", s).group(0)
page = s[s.index("<head>"): s.index("</html>") + len("</html>")]
c = "<!DOCTYPE html>\n" + html_open + "\n" + page

# repoint local asset folder -> assets/
c = c.replace("./CLEAR Lab Signs_files/", "assets/").replace("./CLEAR%20Lab%20Signs_files/", "assets/")

# replace the saved google-fonts stylesheet link with real font links (design uses these 4 families)
gfonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link href="https://fonts.googleapis.com/css2?'
          'family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900'
          '&family=DM+Mono:wght@500'
          '&family=Hanken+Grotesk:wght@400;500;600;700;800'
          '&family=Schibsted+Grotesk:wght@500;600;700;800;900'
          '&display=swap" rel="stylesheet">')
c = re.sub(r'<link[^>]*href="assets/css2"[^>]*>', gfonts, c)

# drop the one leftover extension highlight div class token
c = re.sub(r'(\sclass="[^"]*?)\bcmVhZGVyLWxpbmU\w*\b([^"]*")', r"\1\2", c).replace(' class=""', '')

open(OUT, "w", encoding="utf-8").write(c)

# sanity checks — fail loudly if the extraction didn't come out clean
imgs = c.count("<img")
plasmo = c.count("plasmo")
old_paths = c.count("CLEAR Lab Signs_files")
asset_refs = c.count('src="assets/')
print(f"wrote {OUT}: {len(c)} bytes, {imgs} <img> tags")
print(f"SANITY: plasmo={plasmo} (want 0) | old-paths={old_paths} (want 0) | "
      f"assets/ img refs={asset_refs}")
if plasmo or old_paths:
    sys.exit("ERROR: extraction still contains junk — check the source file.")
