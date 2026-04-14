import ssl, urllib.request, re, io
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ctx = ssl._create_unverified_context()

# Fetch Google Fonts CSS with Chrome UA to get all subset @font-face blocks
req = urllib.request.Request(
    "https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap",
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
)
with urllib.request.urlopen(req, context=ctx) as r:
    css = r.read().decode()

# Find the woff2 that contains basic Latin (J=U+004A, B=U+0042)
all_urls = re.findall(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", css)
font_bytes = None
for url in all_urls:
    r2 = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(r2, context=ctx) as r:
        fb = r.read()
    tc = TTFont(io.BytesIO(fb)).getBestCmap()
    if ord("J") in tc and ord("B") in tc:
        font_bytes = fb
        print("Found Latin subset:", url)
        break

if not font_bytes:
    raise RuntimeError("Could not find Latin subset containing J and B")

font = TTFont(io.BytesIO(font_bytes))
cmap = font.getBestCmap()
hmtx = font["hmtx"]
units_per_em = font["head"].unitsPerEm
glyph_set = font.getGlyphSet()
ascender = font["OS/2"].sTypoAscender
descender = font["OS/2"].sTypoDescender

SVG_SIZE = 100
PADDING = 8  # px each side

# Measure total advance
total_advance = sum(hmtx.metrics[cmap[ord(ch)]][0] for ch in "JB")

# Scale to fit within padded area
available = SVG_SIZE - 2 * PADDING
S = available / total_advance

total_width = total_advance * S
glyph_height = (ascender - descender) * S

x_offset = (SVG_SIZE - total_width) / 2
y_top = (SVG_SIZE - glyph_height) / 2 + ascender * S

# Render each glyph as SVG path
x_cursor = 0
path_parts = []
for ch in "JB":
    gid = cmap[ord(ch)]
    advance, _ = hmtx.metrics[gid]
    pen = SVGPathPen(glyph_set)
    t_pen = TransformPen(pen, (S, 0, 0, -S, x_offset + x_cursor * S, y_top))
    glyph_set[gid].draw(t_pen)
    path_parts.append(pen.getCommands())
    x_cursor += advance

combined = " ".join(path_parts)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_SIZE} {SVG_SIZE}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="45%" stop-color="#0c2346"/>
      <stop offset="100%" stop-color="#1a1040"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="40%" r="55%">
      <stop offset="0%" stop-color="#1e3a6e" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="text" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="55%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#c084fc"/>
    </linearGradient>
  </defs>
  <rect width="{SVG_SIZE}" height="{SVG_SIZE}" rx="14" fill="url(#bg)"/>
  <rect width="{SVG_SIZE}" height="{SVG_SIZE}" rx="14" fill="url(#glow)"/>
  <path d="{combined}" fill="url(#text)"/>
</svg>"""

out = "assets/images/default/favicon.svg"
with open(out, "w") as f:
    f.write(svg)

print(f"Written {len(svg)} bytes to {out}")
print(f"UPM={units_per_em}, S={S:.4f}, total_width={total_width:.1f}, y_top={y_top:.1f}")
print(f"Total width: {total_width:.1f}, x_offset: {x_offset:.1f}, y_top: {y_top:.1f}")
