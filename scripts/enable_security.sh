#!/usr/bin/env bash
set -euo pipefail
ORG="comics-lab"
REPOS="comicbook-core mylar3-sanity comicmeta-comicvine comicmeta-metron comicmeta-gcd cbz-doctor comic-file-organizer comics-suite"
for R in $REPOS; do
echo ">> Enabling security on ${ORG}/${R}"
# Secret scanning
gh api -X PUT -H "Accept: application/vnd.github+json" /repos/$ORG/$R/secret-scanning/settings -f state=enabled -f push_protection_enabled=true || true
# CodeQL default setup
gh api -X PUT -H "Accept: application/vnd.github+json" /repos/$ORG/$R/code-scanning/default-setup -f state=configured -f language=python || true
done
