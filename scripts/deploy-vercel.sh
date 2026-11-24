#!/usr/bin/env bash
# Deploys site/ to Vercel production through the REST API. Needs only curl and
# sha1sum, so no Vercel CLI or npm install.
#
#   VERCEL_TOKEN=...  scripts/deploy-vercel.sh
#
# Optional: VERCEL_TEAM_ID (deploy into a team), VERCEL_PROJECT (default
# silkroad-exchange, which gives https://silkroad-exchange.vercel.app if free).
set -euo pipefail
: "${VERCEL_TOKEN:?Set VERCEL_TOKEN to a Vercel access token}"
PROJECT="${VERCEL_PROJECT:-silkroad-exchange}"
API=https://api.vercel.com
TEAM=""
if [ -n "${VERCEL_TEAM_ID:-}" ]; then TEAM="?teamId=${VERCEL_TEAM_ID}"; fi
auth=(-H "Authorization: Bearer ${VERCEL_TOKEN}")

# Paths keep their site/ prefix: the Vercel project's Root Directory is "site",
# the same setting a Git-connected deploy uses.
cd "$(dirname "$0")/.."
files="["
count=0
# Upload every file once; Vercel skips ones it already has (same SHA-1).
while IFS= read -r -d '' path; do
  rel="${path#./}"
  sha=$(sha1sum "$path" | cut -d' ' -f1)
  size=$(stat -c%s "$path")
  curl -fsS -X POST "${API}/v2/files${TEAM}" "${auth[@]}" \
    -H "x-vercel-digest: ${sha}" -H "Content-Type: application/octet-stream" \
    --data-binary @"$path" > /dev/null
  files+="{\"file\":\"${rel}\",\"sha\":\"${sha}\",\"size\":${size}},"
  count=$((count + 1))
done < <(find site -type f ! -name README.md -print0)
files="${files%,}]"
echo "Uploaded ${count} files"

# Static site: no framework, no build, serve site/ as is.
body=$(printf '{"name":"%s","target":"production","files":%s,"projectSettings":{"framework":null,"buildCommand":null,"installCommand":null,"outputDirectory":null}}' "$PROJECT" "$files")
curl -fsS -X POST "${API}/v13/deployments${TEAM}" "${auth[@]}" \
  -H "Content-Type: application/json" -d "$body" \
  | python3 -c 'import json, sys; d = json.load(sys.stdin); print("Deployment:", "https://" + d["url"], d.get("readyState", "")); print("Production aliases:", ", ".join("https://" + a for a in d.get("alias", [])) or "assigned when the build is ready")'
