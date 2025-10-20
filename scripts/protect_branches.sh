#!/usr/bin/env bash
set -euo pipefail
ORG="comics-lab"
REPOS="comicbook-core mylar3-sanity comicmeta-comicvine comicmeta-metron comicmeta-gcd cbz-doctor comic-file-organizer comics-suite"
for R in $REPOS; do
echo ">> Protecting ${ORG}/${R} main"
gh api -X PUT -H "Accept: application/vnd.github+json" /repos/$ORG/$R/branches/main/protection -f required_pull_request_reviews[dismiss_stale_reviews]=true -f required_pull_request_reviews[required_approving_review_count]=1 -f required_pull_request_reviews[require_code_owner_reviews]=false -f enforce_admins=true -f required_status_checks[strict]=true -f restrictions=
done
