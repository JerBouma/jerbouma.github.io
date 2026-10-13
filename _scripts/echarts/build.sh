#!/bin/bash
# Builds assets/js/lib/echarts-5.5.1-site.min.js from _scripts/echarts/entry.js.
# Needs echarts@5.5.1 and esbuild in a node_modules folder, by default the one in
# $WEBSITE_TOOLS/ebuild (npm install echarts@5.5.1 esbuild@0.24.0 there).
set -e
cd "$(dirname "$0")/../.."
T=${WEBSITE_TOOLS:-/root/.cache/website-tools}/ebuild
NODE_PATH=$T/node_modules "$T/node_modules/.bin/esbuild" _scripts/echarts/entry.js \
  --bundle --minify --format=iife --target=es2017 --legal-comments=none \
  --outfile=assets/js/lib/echarts-5.5.1-site.min.js
ls -la assets/js/lib/echarts-5.5.1-site.min.js
