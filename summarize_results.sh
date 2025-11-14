#!/bin/bash
set -euo pipefail
mkdir -p build-artifacts
# Try to summarize surefire reports; fallback gracefully
if ls target/surefire-reports/*.txt >/dev/null 2>&1; then
  echo "Collecting test summaries..."
  grep -h "Tests run:" target/surefire-reports/*.txt || true
  # create a short summary file
  printf "Maven test summary\n-------------------\n" > build-artifacts/test-summary.txt
  grep -h "Tests run:" target/surefire-reports/*.txt >> build-artifacts/test-summary.txt || true
else
  echo "No surefire text reports found; creating empty summary."
  printf "No test report found.\n" > build-artifacts/test-summary.txt
fi
