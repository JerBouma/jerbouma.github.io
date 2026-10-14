"""Draws the JB mark: the favicon, the home-screen icon and the logo in the masthead.

One drawing for all of them: a dark round badge with a thin ring in the homepage
headline's gradient (#38bdf8 -> #818cf8 -> #c084fc) and "JB" in Inter ExtraBold, the
site's typeface, as outlines in that same gradient. The letters are paths, not text,
so the mark looks the same in every browser and at every size.

    python assets/python/gen_favicon.py

Writes assets/images/default/favicon.svg, _includes/brand-mark.svg (the masthead
copy, with its own gradient ids) and assets/images/default/apple-touch-icon.svg.
The PNG sizes are rendered from favicon.svg with a headless browser (see the
visual-check skill): favicon.png (64px) and apple-touch-icon.png (180px).
"""

import io
import re
import urllib.request
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent.parent
GRADIENT = [("0%", "#38bdf8"), ("60%", "#818cf8"), ("100%", "#c084fc")]

CAP_HEIGHT = 42.0  # letter height in a 100-unit badge; large, so it still reads at 16px
GAP = 3.6  # space between the J and the B, in badge units
RING = 6.5  # ring width; about one solid pixel at 16px
OPTICAL_LIFT = 0.6  # round letters look low when centred exactly


def inter_extrabold() -> TTFont:
    css = urllib.request.urlopen(urllib.request.Request(
        "https://fonts.googleapis.com/css2?family=Inter:wght@800",
        headers={"User-Agent": "Mozilla/5.0"})).read().decode()  # a plain agent gets a TTF
    url = re.search(r"url\((https://[^)]+\.ttf)\)", css).group(1)
    return TTFont(io.BytesIO(urllib.request.urlopen(url).read()))


def glyph_paths(font: TTFont) -> str:
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = CAP_HEIGHT / font["OS/2"].sCapHeight

    # bounds of each letter at that scale, to place them by their ink, not their advance
    def bounds(ch):
        pen = BoundsPen(glyphs)
        glyphs[cmap[ord(ch)]].draw(pen)
        x0, y0, x1, y1 = pen.bounds
        return x0 * scale, x1 * scale

    (j0, j1), (b0, b1) = bounds("J"), bounds("B")
    width = (j1 - j0) + GAP + (b1 - b0)
    left = 50 - width / 2
    baseline = 50 + CAP_HEIGHT / 2 - OPTICAL_LIFT

    parts = []
    for ch, x in (("J", left - j0), ("B", left + (j1 - j0) + GAP - b0)):
        pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        glyphs[cmap[ord(ch)]].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        parts.append(pen.getCommands())
    return " ".join(parts)


def stops() -> str:
    return "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in GRADIENT)


def badge(paths: str, prefix: str, size_attrs: str = "", full_bleed: bool = False) -> str:
    """The badge in a 100x100 box; full_bleed fills the square for home-screen icons."""
    r = 50 - RING / 2 - 0.5
    background = (f'<rect width="100" height="100" fill="url(#{prefix}bg)"/>' if full_bleed
                  else f'<circle cx="50" cy="50" r="{r:.2f}" fill="url(#{prefix}bg)"/>')
    mark = (f'<g transform="translate(50 50) scale(0.8) translate(-50 -50)">' if full_bleed else "<g>")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"{size_attrs}>
  <defs>
    <radialGradient id="{prefix}bg" cx="50%" cy="38%" r="65%">
      <stop offset="0%" stop-color="#16213a"/><stop offset="100%" stop-color="#0b1120"/>
    </radialGradient>
    <linearGradient id="{prefix}ink" gradientUnits="userSpaceOnUse" x1="22" y1="26" x2="80" y2="76">{stops()}</linearGradient>
    <linearGradient id="{prefix}ring" gradientUnits="userSpaceOnUse" x1="6" y1="16" x2="94" y2="84">{stops()}</linearGradient>
  </defs>
  {background}
  {mark}<circle cx="50" cy="50" r="{r:.2f}" fill="none" stroke="url(#{prefix}ring)" stroke-width="{RING}"/>
  <path d="{paths}" fill="url(#{prefix}ink)"/></g>
</svg>
'''


def main() -> None:
    paths = glyph_paths(inter_extrabold())
    (ROOT / "assets/images/default/favicon.svg").write_text(badge(paths, ""))
    # rendered to apple-touch-icon.png (180px) and then not needed on the site
    (ROOT / "assets/images/default/apple-touch-icon.svg").write_text(badge(paths, "", full_bleed=True))
    (ROOT / "_includes/brand-mark.svg").write_text(
        badge(paths, "jbm-", ' width="38" height="38" class="site-title__mark" aria-hidden="true" focusable="false"'))
    print("written: favicon.svg, apple-touch-icon.svg, _includes/brand-mark.svg")


if __name__ == "__main__":
    main()
