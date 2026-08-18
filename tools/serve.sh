#!/usr/bin/env bash
# Local preview at http://localhost:1313 .
# Renders to .hugo-preview/, never to docs/ — a dev build carries
# "Disallow: /" in robots.txt and localhost URLs, and must never be committed.
set -euo pipefail
cd "$(dirname "$0")/.."
exec hugo server --destination .hugo-preview --baseURL "http://localhost:1313/" --disableFastRender "$@"
