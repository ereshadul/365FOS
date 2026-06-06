import urllib.request
import json
import time

# ============================================================
# PASTE YOUR TOKEN BETWEEN THE QUOTES BELOW
TOKEN = "YOUR_GITHUB_TOKEN_HERE"
# ============================================================

REPO_OWNER = "ereshadul"
REPO_NAME = "365FOS"

# These are the duplicate titles to clean up in Phase 0
DUPLICATES_TO_DELETE = [
    "Set up Power Automate",
    "Sign up for Microsoft 365 Business Premium Trial",
    "Sign up for Dynamics 365 Sales Trial",
    "Download and install Power BI Desktop",
    "Enable Microsoft Copilot in M365 Admin Center",
    "Verify all tools are connected under one tenant",
]

def get_all_issues():
    all_issues = []
    page = 1
    while True:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues?state=open&per_page=100&page={page}"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"token {TOKEN}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        with urllib.request.urlopen(req) as response:
            issues = json.loads(response.read().decode())
            if not issues:
                break
            all_issues.extend(issues)
            page += 1
    return all_issues

def close_issue(issue_number, title):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    data = json.dumps({"state": "closed"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PATCH")
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ Closed #{issue_number}: {title}")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed #{issue_number}: {title} — {e.code}")

print("Fetching all issues...\n")
all_issues = get_all_issues()

# Find duplicates — for each duplicate title, keep the HIGHER number (newer), close the LOWER number (older)
print("Finding duplicates...\n")
for dup_title in DUPLICATES_TO_DELETE:
    matches = [i for i in all_issues if i['title'].strip() == dup_title.strip()]
    if len(matches) >= 2:
        # Sort by issue number, keep highest, close the rest
        matches.sort(key=lambda x: x['number'])
        to_close = matches[:-1]  # all except the last (highest number)
        keep = matches[-1]
        print(f"Keeping  #{keep['number']}: {keep['title']}")
        for issue in to_close:
            close_issue(issue['number'], issue['title'])
        time.sleep(1)
    elif len(matches) == 1:
        print(f"ℹ️  Only one found (no duplicate): {dup_title}")
    else:
        print(f"⚠️  Not found: {dup_title}")

print("\n🎉 Done! Duplicates have been closed.")
print("Note: GitHub doesn't allow deleting issues via API, so they are closed instead.")
print("Closed issues won't appear in your open issues list.")

input("\nPress Enter to close...")
