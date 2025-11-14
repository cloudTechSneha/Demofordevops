#!/bin/bash
set -euo pipefail
if [[ -z "${GITHUB_EVENT_PATH:-}" ]]; then
  echo "GITHUB_EVENT_PATH not set; cannot validate labels."
  exit 0
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required but not installed."
  exit 1
fi

LABELS=$(jq -r '.pull_request.labels // [] | map(.name) | join(",")' "$GITHUB_EVENT_PATH")
if [[ -z "$LABELS" ]]; then
  echo "❌ At least one label required on the PR."
  exit 1
fi
echo "✅ Labels present: $LABELS"
