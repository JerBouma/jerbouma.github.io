"""
Self-hosted Font Awesome with only the icons the site uses.

Scans the site's sources (and the theme's includes) for `fa-<name>` classes,
keeps those icon rules from Font Awesome's all.css plus every non-icon rule
(sizes, animations, the font families), and subsets the three web fonts to
the matching code points. Writes assets/fonts/fontawesome/{fa.css,*.woff2}.

    python _scripts/fontawesome/build.py <path to @fortawesome/fontawesome-free 6.x>

Needs fonttools and brotli. Rerun it after using an icon the site did not use
before: an icon that is missing here shows as an empty square.
"""
import glob
import os
import re
import subprocess
import sys

FA = sys.argv[1]
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "fonts", "fontawesome")
THEME = subprocess.run(["bundle", "info", "--path", "minimal-mistakes-jekyll"], cwd=ROOT,
                       capture_output=True, text=True).stdout.strip()

sources = []
for pattern in ["_includes/**/*", "_layouts/**/*", "_pages/**/*", "_data/**/*", "assets/js/*.js",
                "_plugins/*.rb", "_sass/**/*.scss", "*.md", "*.html", "*.yml"]:
    sources += glob.glob(os.path.join(ROOT, pattern), recursive=True)
if THEME:
    sources += glob.glob(os.path.join(THEME, "_includes", "**", "*"), recursive=True)
    sources += glob.glob(os.path.join(THEME, "_layouts", "**", "*"), recursive=True)
used = set()
for path in sources:
    if os.path.isfile(path):
        used |= set(re.findall(r"\bfa-([a-z0-9-]+)", open(path, encoding="utf-8", errors="ignore").read()))

css = open(os.path.join(FA, "css", "all.css"), encoding="utf-8").read()
# split into top-level rules (all.css has no nested blocks except @keyframes/@media,
# which carry no icon rules and are kept whole)
rules, depth, start = [], 0, 0
for i, ch in enumerate(css):
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            rules.append(css[start:i + 1].strip())
            start = i + 1
ICON = re.compile(r'^((?:\.fa-[a-z0-9-]+\s*,?\s*)+)\{\s*--fa:\s*"\\([0-9a-f]+)";\s*\}$', re.S)
kept, codepoints, icons = [], set(), set()
for rule in rules:
    m = ICON.match(rule)
    if not m:
        kept.append(rule)
        continue
    names = [n.strip()[4:] for n in m.group(1).split(",") if n.strip()]
    names = [n for n in names if n in used]
    if names:
        kept.append(",\n".join(".fa-" + n for n in names) + ' {\n  --fa: "\\' + m.group(2) + '"; }')
        codepoints.add(int(m.group(2), 16))
        icons |= set(names)

os.makedirs(OUT, exist_ok=True)
out_css = "\n\n".join(kept).replace("../webfonts/", "")
# only woff2: every browser the site supports reads it, the .ttf fallbacks go
out_css = re.sub(r',\s*url\("[^"]+\.ttf"\) format\("truetype"\)', "", out_css)
open(os.path.join(OUT, "fa.css"), "w", encoding="utf-8").write(
    "/* Font Awesome Free 6.7.2 (https://fontawesome.com/license/free), subset by _scripts/fontawesome/build.py */\n" + out_css + "\n")
unicodes = ",".join(f"U+{c:04X}" for c in sorted(codepoints))
for font in ["fa-solid-900", "fa-regular-400", "fa-brands-400", "fa-v4compatibility"]:
    subprocess.run([os.path.join(os.path.dirname(sys.executable), "pyftsubset"),
                    os.path.join(FA, "webfonts", font + ".ttf"), "--unicodes=" + unicodes,
                    "--flavor=woff2", "--output-file=" + os.path.join(OUT, font + ".woff2"),
                    "--layout-features=*", "--no-hinting"], check=True)
print(len(icons), "icons kept")
