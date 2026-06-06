import urllib.request
import json

# ============================================================
# PASTE YOUR TOKEN BETWEEN THE QUOTES BELOW
TOKEN = "YOUR_GITHUB_TOKEN_HERE"
# ============================================================

REPO_OWNER = "ereshadul"
REPO_NAME = "365FOS"

def get_issues():
    all_issues = []
    page = 1
    
    while True:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues?state=all&per_page=100&page={page}"
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

print("Fetching issues...\n")
issues = get_issues()

print(f"Total issues found: {len(issues)}\n")
print("Last 10 issues created:")
print("-" * 60)
for issue in issues[:10]:
    labels = [l['name'] for l in issue['labels']]
    print(f"#{issue['number']} [{', '.join(labels)}] {issue['title']}")

print("-" * 60)
print("\nAll issue titles by label:")
from collections import defaultdict
by_label = defaultdict(list)
for issue in issues:
    label = issue['labels'][0]['name'] if issue['labels'] else 'No label'
    by_label[label].append(issue['title'])

for label in sorted(by_label.keys()):
    print(f"\n{label} ({len(by_label[label])} issues):")
    for title in by_label[label]:
        print(f"  - {title}")

input("\nPress Enter to close...")
