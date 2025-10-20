#!/usr/bin/env bash
set -euo pipefail
ORG="comics-lab"
REPOS="comicbook-core mylar3-sanity comicmeta-comicvine comicmeta-metron comicmeta-gcd cbz-doctor comic-file-organizer comics-suite"
for R in $REPOS; do
echo ">> Locking Actions on ${ORG}/${R}"
# Repo-level policy
gh api -X PUT -H "Accept: application/vnd.github+json" /repos/$ORG/$R/actions/permissions -f enabled=true -f allowed_actions=selected
# Default token perms
gh api -X PUT -H "Accept: application/vnd.github+json" /repos/$ORG/$R/actions/permissions/workflow -f default_workflow_permissions=read -f can_approve_pull_request_reviews=false
done
