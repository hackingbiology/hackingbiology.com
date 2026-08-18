#!/usr/bin/env bash
# Build the site into /docs (where GitHub Pages serves from).
#   ./tools/build.sh                       -> builds for the final domain
#   ./tools/build.sh <base-url>            -> builds for a preview URL
set -euo pipefail
cd "$(dirname "$0")/.."
BASE="${1:-}"
if [ -n "$BASE" ]; then hugo --gc --minify --baseURL "$BASE"; else hugo --gc --minify; fi

# GitHub Pages must not run Jekyll over Hugo's output.
touch docs/.nojekyll

# WordPress served the feed at /feed/. GitHub Pages only serves index.html for a
# directory, so the XML cannot live at /feed/ itself. Keep both: the real feed at
# /feed/index.xml, and a redirect page at /feed/ for anything that hits the old address.
mkdir -p docs/feed
cp docs/index.xml docs/feed/index.xml
FEED_URL="${BASE%/}/index.xml"
[ -z "$BASE" ] && FEED_URL="https://hackingbiology.com/index.xml"
cat > docs/feed/index.html <<HTML
<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>Hacking Biology &middot; RSS</title>
<link rel="alternate" type="application/rss+xml" title="Hacking Biology" href="$FEED_URL">
<meta http-equiv="refresh" content="0; url=$FEED_URL">
<link rel="canonical" href="$FEED_URL"></head>
<body><p>The feed moved to <a href="$FEED_URL">$FEED_URL</a>.</p></body></html>
HTML

echo "built -> docs/  ($(find docs -name 'index.html' | wc -l) pages)"
