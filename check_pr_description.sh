#!/bin/bash
set -euo pipefail
if [[ -z "${GITHUB_EVENT_PATH:-}" ]]; then
  echo "GITHUB_EVENT_PATH not set; cannot validate PR description."
  exit 0
fi
if ! command -v jq >/dev/null 2>&1; then
  echo "jq is required but not installed."
  exit 1
fi

PR_BODY=$(jq -r '.pull_request.body // ""' "$GITHUB_EVENT_PATH")
if [[ ! "$PR_BODY" =~ JIRA-[0-9]+ ]]; then
  echo "❌ PR description must contain a JIRA ID (e.g., JIRA-123)"
  exit 1
fi
echo "✅ JIRA ID found in PR description."
