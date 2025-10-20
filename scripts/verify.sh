#!/usr/bin/env bash
set -euo pipefail
ORG="comics-lab"
REPOS="comicbook-core mylar3-sanity comicmeta-comicvine comicmeta-metron comicmeta-gcd cbz-doctor comic-file-organizer comics-suite"
OUT="verification-summary.jsonl"
: > "$OUT"
for R in $REPOS; do
  echo -n '{"repo":"'$R'"' >> "$OUT"
  if gh api /repos/$ORG/$R/branches/main/protection -H "Accept: application/vnd.github+json" >/dev/null 2>&1; then echo -n ', "branch_protection":"ok"' >> "$OUT"; else echo -n ', "branch_protection":"missing"' >> "$OUT"; fi
  if gh api /repos/$ORG/$R/actions/permissions -H "Accept: application/vnd.github+json" >/dev/null 2>&1; then echo -n ', "actions_policy":"ok"' >> "$OUT"; else echo -n ', "actions_policy":"missing"' >> "$OUT"; fi
  if gh api /repos/$ORG/$R/secret-scanning/settings -H "Accept: application/vnd.github+json" >/dev/null 2>&1; then echo -n ', "secret_scanning":"ok"' >> "$OUT"; else echo -n ', "secret_scanning":"missing"' >> "$OUT"; fi
  if gh api /repos/$ORG/$R/code-scanning/default-setup -H "Accept: application/vnd.github+json" >/dev/null 2>&1; then echo -n ', "codeql_default":"ok"' >> "$OUT"; else echo -n ', "codeql_default":"missing"' >> "$OUT"; fi
  echo '}' >> "$OUT"
done
echo "Summary written to $OUT"
