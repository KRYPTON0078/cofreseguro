#!/usr/bin/env bash
# Run this ONCE after creating an empty public repo:
#   https://github.com/new  → name: cofreseguro  (no README / no .gitignore)
set -euo pipefail
cd "$(dirname "$0")/.."
OWNER="${GITHUB_OWNER:-KRYPTON0078}"
REPO="${GITHUB_REPO:-cofreseguro}"
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Set GITHUB_TOKEN to a classic PAT with 'repo' scope, then re-run."
  exit 1
fi
# Create if missing
STATUS=$(curl -s -o /tmp/cs_repo.json -w "%{http_code}" \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/${OWNER}/${REPO}")
if [[ "$STATUS" == "404" ]]; then
  curl -s -X POST -H "Authorization: token ${GITHUB_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/user/repos \
    -d "{\"name\":\"${REPO}\",\"description\":\"CofreSeguro — mobile-money fraud shield (EN/PT)\",\"private\":false,\"auto_init\":false}"
  echo
fi
git remote remove origin 2>/dev/null || true
git remote add origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${OWNER}/${REPO}.git"
git push -u origin main
echo "Published: https://github.com/${OWNER}/${REPO}"
