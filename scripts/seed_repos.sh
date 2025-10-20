#!/usr/bin/env bash
set -euo pipefail
ORG="comics-lab"
REPOS="comicbook-core mylar3-sanity comicmeta-comicvine comicmeta-metron comicmeta-gcd cbz-doctor comic-file-organizer comics-suite"
for R in $REPOS; do
echo ">> Creating repo ${ORG}/${R}"
gh repo create "$ORG/$R" --private --confirm || true
done
