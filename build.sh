#!/bin/sh
# Rebuild the site after editing anything in src/ (needs Python 3).
set -e
cd "$(dirname "$0")"
python3 src/build.py
python3 src/mksw.py
echo "Built index.html and sw.js"
