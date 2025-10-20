#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
bash "$DIR/seed_repos.sh"
bash "$DIR/lockdown_actions.sh"
bash "$DIR/enable_security.sh"
bash "$DIR/protect_branches.sh"
echo ">> Completed."
