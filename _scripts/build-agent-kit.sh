#!/usr/bin/env bash
# Zips agent-kit/ (including its hidden folders) into the built site, so the
# Financial Modelling guide can offer it as a download. Run after jekyll build.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p _site/assets/files
rm -f _site/assets/files/financial-modelling-agent-kit.zip
(cd agent-kit && zip -qrX ../_site/assets/files/financial-modelling-agent-kit.zip . -x '*.DS_Store')
echo "Agent kit written to _site/assets/files/financial-modelling-agent-kit.zip"
