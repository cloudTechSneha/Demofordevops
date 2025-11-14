#!/usr/bin/env python3
import os, json, requests, sys

event_path = os.environ.get("GITHUB_EVENT_PATH")
repo = os.environ.get("GITHUB_REPOSITORY")
token = os.environ.get("GITHUB_TOKEN")

if not event_path or not os.path.exists(event_path):
    print("GITHUB_EVENT_PATH not set or file missing; exiting.")
    sys.exit(0)

with open(event_path) as f:
    event = json.load(f)

# For workflow_run events, the payload includes 'workflow_run' with 'conclusion' and 'pull_requests'
workflow_run = event.get("workflow_run", {})
conclusion = workflow_run.get("conclusion")  # "success" or "failure"
pull_requests = workflow_run.get("pull_requests", [])

headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}

def post_comment(pr_number, body):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    r = requests.post(url, headers=headers, json={"body": body})
    print("POST", url, "->", r.status_code)
    return r

def list_review_threads(pr_number):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/threads"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("Failed to list threads for PR", pr_number, r.status_code, r.text)
        return []
    return r.json()

def resolve_thread(pr_number, thread_id):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/threads/{thread_id}"
    r = requests.patch(url, headers=headers, json={"resolved": True})
    print("PATCH", url, "->", r.status_code)
    return r

if not pull_requests:
    print("No pull requests associated with this workflow run; exiting.")
    sys.exit(0)

for pr in pull_requests:
    pr_number = pr.get("number")
    if not pr_number:
        continue
    if conclusion == "success":
        # resolve threads
        threads = list_review_threads(pr_number)
        resolved = 0
        for t in threads:
            tid = t.get("id")
            if tid and not t.get("resolved", False):
                resp = resolve_thread(pr_number, tid)
                if resp.status_code == 200:
                    resolved += 1
        post_comment(pr_number, f"✅ All tests in workflow_run concluded SUCCESS. Marked {resolved} thread(s) resolved.")
    else:
        post_comment(pr_number, "❌ Tests failed in the workflow. Please address failures — conversations have been (re)opened.")
