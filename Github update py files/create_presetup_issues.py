import urllib.request
import json
import time

# ============================================================
# PASTE YOUR TOKEN BETWEEN THE QUOTES BELOW
TOKEN = "YOUR_GITHUB_TOKEN_HERE"
# ============================================================

REPO_OWNER = "ereshadul"
REPO_NAME = "365FOS"

issues = [
    {
        "title": "[00a] Set up cPanel email hosting and fix DNS records in Cloudflare",
        "label": "0: Setup",
        "body": "Set up cPanel email hosting for cacacumo.com and fix DNS records in Cloudflare.\n\nCompleted steps:\n- Fixed MX record → server210-3.web-hosting.com\n- Fixed SPF record → v=spf1 +ip4:198.54.115.150 +include:spf.web-hosting.com ~all\n- Updated DKIM key in Cloudflare with correct cPanel key\n- Added DMARC record → v=DMARC1; p=none;\n- Tested send and receive — working ✅\n\nStatus: COMPLETED",
        "close": True
    },
    {
        "title": "[00b] Create email accounts in cPanel",
        "label": "0: Setup",
        "body": "Create the following email accounts in cPanel → Email Accounts:\n\n| Email | Purpose |\n|---|---|\n| admin@cacacumo.com | M365 admin account |\n| ron@cacacumo.com | Ron (the manager) |\n| sarah@cacacumo.com | Fake sales rep |\n| mike@cacacumo.com | Fake sales rep |\n| lisa@cacacumo.com | Fake sales rep |\n\nSteps:\n1. Go to cPanel → Email Accounts → Create\n2. Create each email one by one\n3. Use a strong password for each\n4. Test each account via webmail.cacacumo.com",
        "close": False
    }
]

def create_issue(title, label, body):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    data = json.dumps({
        "title": title,
        "body": body,
        "labels": [label]
    }).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ Created: {title}")
            return result['number']
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: {title} — {e.code}")
        return None

def close_issue(issue_number, title):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    data = json.dumps({"state": "closed"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PATCH")
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"🔒 Closed: {title}")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to close: {title} — {e.code}")

print("Creating pre-setup issues...\n")

for issue in issues:
    number = create_issue(issue["title"], issue["label"], issue["body"])
    if number and issue["close"]:
        time.sleep(1)
        close_issue(number, issue["title"])
    time.sleep(1)

print("\n🎉 Done!")
print("\nSummary:")
print("  [00a] - Created and CLOSED (already completed)")
print("  [00b] - Created and OPEN (to do next session)")

input("\nPress Enter to close...")
