#!/usr/bin/env python3
import os, json, requests, sys

event_path = os.environ.get("GITHUB_EVENT_PATH")
repo = os.environ.get("GITHUB_REPOSITORY")
token = os.environ.get("GITHUB_TOKEN")
summary_path = "build-artifacts/test-summary.txt"

if not repo or not token:
    print("GITHUB_REPOSITORY or GITHUB_TOKEN not set; cannot post results.")
    sys.exit(0)

if event_path and os.path.exists(event_path):
    with open(event_path) as f:
        event = json.load(f)
    pr_number = event.get("number") or (event.get("pull_request") or {}).get("number")
    if not pr_number:
        # Some events embed pull_request differently
        pr = event.get("pull_request")
        if pr:
            pr_number = pr.get("number")
else:
    pr_number = None

with open(summary_path, 'r') as f:
    summary = f.read()

comment = f"""🧪 **Maven Test Summary**

```
{summary}
```
"""

headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

if pr_number:
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    resp = requests.post(url, headers=headers, json={"body": comment})
    if resp.status_code >= 300:
        print("Failed to post PR comment:", resp.status_code, resp.text)
        sys.exit(1)
    print("Posted test summary to PR", pr_number)
else:
    print("No PR number found in event; skipping comment.")
