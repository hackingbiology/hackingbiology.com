#!/usr/bin/env bash
# usage: ./wp.sh <path-after-/rest/v1.1/> [curl args...]
TOK=$(python -c "import json,io;print(json.load(io.open(r'C:\Users\admin\.hackingbiology\token.json',encoding='utf-8'))['access_token'])")
P="$1"; shift
curl -s --max-time 40 -H "Authorization: Bearer $TOK" "https://public-api.wordpress.com/rest/v1.1/$P" "$@"
