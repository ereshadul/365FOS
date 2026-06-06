import urllib.request
import json
import time

# ============================================================
# PASTE YOUR TOKEN BETWEEN THE QUOTES BELOW
TOKEN = "YOUR_GITHUB_TOKEN_HERE"
# ============================================================

REPO_OWNER = "ereshadul"
REPO_NAME = "365FOS"

# Correct order of phases
PHASE_ORDER = [
    "0: Setup",
    "1: Excel",
    "2: D365 CRM",
    "3: Outlook",
    "4: Power Automate",
    "5: Power BI",
    "6: AI Reporting",
    "7: Final"
]

# Correct order of issues within each phase
ISSUE_ORDER = [
    # 0: Setup
    "Sign up for Microsoft 365 Business Premium Trial",
    "Sign up for Dynamics 365 Sales Trial",
    "Set up Power Automate access",
    "Download and install Power BI Desktop",
    "Enable Microsoft Copilot in M365 Admin Center",
    "Verify all tools are connected under one tenant",

    # 1: Excel
    "Create raw Excel file Ron_Sales_Data_Raw.xlsx",
    "Add merged cells title and wrong-row headers",
    "Enter 20 rows of intentionally dirty data",
    "Leave Budget column empty for 5 rows and add messy Notes column",
    "Fix the mess — remove merged cells and fix headers",
    "Remove duplicate rows and empty rows",
    "Fix dates, convert text amounts to numbers, replace TBD",
    "Standardize Status and Industry values",
    "Fill blank Rep Names and Budget cells",
    "Delete Notes column and save clean file",
    "Add formula columns: Quarter, % to Budget, Won Flag, Deal Size, Days to Close",
    "Build Pivot Table 1 — Revenue by Rep by Quarter",
    "Build Pivot Table 2 — Win Rate by Industry",
    "Build Pivot Table 3 — Budget vs Actual",
    "Build Pivot Table 4 — Deal Size Mix by Industry",
    "Build Pivot Table 5 — Average Days to Close",
    "Apply pro Excel tricks: Flash Fill, XLOOKUP, Conditional Formatting, Data Validation",
    "Practice COUNTIFS and SUMIFS formulas",

    # 2: D365 CRM
    "Log in to D365 and configure organization settings",
    "Create 5 customer accounts",
    "Create 10 contacts (2 per company)",
    "Create 7 custom fields on Opportunity form",
    "Add custom fields to Opportunity form and publish",
    "Create 10 opportunities with realistic magnet data",
    "Mark Surgical Tools and Guidance Systems as At Risk",
    "Create 3 sales rep user accounts",
    "Configure security permissions for reps and Ron",
    "Log activity history on every opportunity",
    "Create Personal View — Ron's At Risk Deals",
    "Create System View — This Week's Follow-ups",
    "Create Email Template for rep follow-ups",
    "Set up Duplicate Detection Rules",
    "Create D365 Dashboard with pipeline tiles",
    "Set up Business Process Flow on Opportunity",

    # 3: Outlook
    "Configure server-side sync between Outlook and D365",
    "Test email sync between Outlook and D365",
    "Connect alias emails for fake sales reps",

    # 4: Power Automate
    "Build Flow 1 — Stale Deal Alert",
    "Build Flow 2 — Stage Change Notification",
    "Build Flow 3 — New Lead Auto Assignment",
    "Build Flow 4 — Closed Won Celebration",
    "Build Flow 5 — Weekly Pipeline Summary",
    "Build Flow 6 — Overdue Task Reminder",
    "Add error handling to all flows",
    "Use variables and Apply to Each for dynamic content",

    # 5: Power BI
    "Connect Power BI to clean Excel file",
    "Connect Power BI to D365 Sales",
    "Clean data in Power Query",
    "Merge Excel and D365 tables in Power Query",
    "Create relationships between tables in Model view",
    "Create DAX measures: Total Pipeline, Total Won, Win Rate, % to Budget",
    "Create DAX measures: Avg Deal Size, Deals at Risk, YTD Revenue",
    "Build Page 1 — Executive Summary",
    "Build Page 2 — Sales Rep Performance",
    "Build Page 3 — Pipeline Health",
    "Build Page 4 — Product Analytics",
    "Build Page 5 — Budget vs Actual",

    # 6: AI Reporting
    "Enrich Excel data with Customer Comments, Loss Reason, Next Action columns",
    "Build Report A — Microsoft Copilot in Power BI",
    "Build Report B — Claude AI analysis",
    "Compare Copilot vs Claude and build summary table",

    # 7: Final
    "Replace Excel source with live D365 data in Power BI",
    "Publish dashboard and set scheduled refresh",
    "Test end-to-end: stage change triggers flow and updates dashboard",
    "Scenario 1 — Give Ron today's pipeline in under 2 minutes",
    "Scenario 2 — Onboard a new sales rep in under 15 minutes",
    "Scenario 3 — Export Q3 forecast for Finance in under 3 minutes",
    "Scenario 4 — Investigate and resolve a stale deal",
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

def update_issue_title(issue_number, new_title):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}"
    data = json.dumps({"title": new_title}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PATCH")
    req.add_header("Authorization", f"token {TOKEN}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"✅ Updated: {new_title}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ Failed: {new_title} — {e.code}")
        return False

print("Fetching all open issues...\n")
all_issues = get_all_issues()

# Build a lookup dictionary by title
issue_lookup = {}
for issue in all_issues:
    # Strip any existing serial number if present
    title = issue['title']
    if title[:4].startswith('[') and title[3] == ']':
        title = title[5:].strip()
    issue_lookup[title.strip()] = issue

print(f"Found {len(all_issues)} open issues\n")
print("Adding serial numbers...\n")

not_found = []
for i, title in enumerate(ISSUE_ORDER):
    serial = f"[{str(i+1).zfill(2)}]"
    new_title = f"{serial} {title}"

    if title in issue_lookup:
        issue = issue_lookup[title]
        update_issue_title(issue['number'], new_title)
        time.sleep(0.8)
    else:
        print(f"⚠️  Not found: {title}")
        not_found.append(title)

print(f"\n🎉 Done! All issues numbered.")
if not_found:
    print(f"\n⚠️  These {len(not_found)} issues were not found:")
    for t in not_found:
        print(f"  - {t}")

input("\nPress Enter to close...")
