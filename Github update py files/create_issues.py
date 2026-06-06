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
    # Phase 0: Setup
    {"title": "Sign up for Microsoft 365 Business Premium Trial", "label": "0: Setup", "body": "Go to microsoft.com/microsoft-365/business and click 'Try free for one month'.\nUse Cacacumo email as the admin account.\n\nGives you: Outlook, Excel, Teams, SharePoint, Copilot features.\nTrial lasts 30 days — start this only when ready to work."},
    {"title": "Sign up for Dynamics 365 Sales Trial", "label": "0: Setup", "body": "Go to dynamics.microsoft.com/sales and click 'Try for free'.\nUse the same Cacacumo email to stay under one tenant.\n\nGives you: full CRM with admin rights.\nTrial lasts 30 days."},
    {"title": "Set up Power Automate access", "label": "0: Setup", "body": "No separate signup needed.\nGo to make.powerautomate.com and log in with Cacacumo email.\nUses your M365 license automatically."},
    {"title": "Download and install Power BI Desktop", "label": "0: Setup", "body": "Download free from powerbi.microsoft.com/downloads.\nNo account needed for desktop version.\nSign in with Cacacumo account when publishing dashboards later."},
    {"title": "Enable Microsoft Copilot in M365 Admin Center", "label": "0: Setup", "body": "Go to M365 admin center and turn on Copilot features.\nVerify Copilot icon appears inside Excel, Word, and Power BI before starting AI Reporting Phase."},
    {"title": "Verify all tools are connected under one tenant", "label": "0: Setup", "body": "Open each tool one by one and confirm login works with Cacacumo email.\nFix any connection issues before starting tasks.\nAll tools must share the same account."},

    # Phase 1: Excel
    {"title": "Create raw Excel file Ron_Sales_Data_Raw.xlsx", "label": "1: Excel", "body": "Open blank Excel and save as 'Ron_Sales_Data_Raw.xlsx'.\nThis is the 'before' snapshot — keep it untouched.\nCleaned version will be saved separately later."},
    {"title": "Add merged cells title and wrong-row headers", "label": "1: Excel", "body": "Merge cells A1 and B1, type 'Sales Data'.\nPut column headers in Row 3 (not Row 1):\nDate, Rep Name, Industry, Product, Amount, Budget, Status, Close Date."},
    {"title": "Enter 20 rows of intentionally dirty data", "label": "1: Excel", "body": "Fill 20 rows with fake sales data including these problems:\n- 3 completely empty rows\n- 2 duplicate rows\n- 5 dates as text in different formats\n- 4 amounts as text with dollar signs\n- 2 blank Rep Name cells\n- Status typed 3 different ways\n- 'TBD' in one Amount cell\n- Industry spelled 3 different ways"},
    {"title": "Leave Budget column empty for 5 rows and add messy Notes column", "label": "1: Excel", "body": "Leave Budget blank for 5 rows.\nInsert a 'Notes' column between Industry and Product with merged cells inside it."},
    {"title": "Fix the mess — remove merged cells and fix headers", "label": "1: Excel", "body": "Select entire sheet → Home → Merge & Center → Unmerge Cells.\nMove headers from Row 3 to Row 1.\nDelete all empty rows above headers."},
    {"title": "Remove duplicate rows and empty rows", "label": "1: Excel", "body": "Delete empty rows: Find & Select → Go To Special → Blanks → Delete Row.\nRemove duplicates: Data → Remove Duplicates."},
    {"title": "Fix dates, convert text amounts to numbers, replace TBD", "label": "1: Excel", "body": "Fix dates: Data → Text to Columns → Date (MDY).\nRemove $ and , from Amount column using Find & Replace.\nReplace 'TBD' with 0 using Find & Replace."},
    {"title": "Standardize Status and Industry values", "label": "1: Excel", "body": "Status: convert all variations to exactly: Closed Won, Closed Lost, Open.\nIndustry: convert all variations to exactly: Automotive, Industrial, Medical, Aerospace, Electronics."},
    {"title": "Fill blank Rep Names and Budget cells", "label": "1: Excel", "body": "Rep Name blanks: F5 → Special → Blanks → type 'Unassigned' → Ctrl+Enter.\nBudget blanks: same trick, fill with 0."},
    {"title": "Delete Notes column and save clean file", "label": "1: Excel", "body": "Right-click Notes column → Delete.\nSave as 'Ron_Sales_Data_Clean.xlsx'.\nNow you have two files: raw mess and clean version."},
    {"title": "Add formula columns: Quarter, % to Budget, Won Flag, Deal Size, Days to Close", "label": "1: Excel", "body": "Quarter: =CHOOSE(ROUNDUP(MONTH(A2)/3,0),\"Q1\",\"Q2\",\"Q3\",\"Q4\")\n% to Budget: =IF(F2=0,0,E2/F2)\nWon Flag: =IF(G2=\"Closed Won\",1,0)\nDeal Size: =IF(E2>=75000,\"Large\",IF(E2>=40000,\"Medium\",\"Small\"))\nDays to Close: =NETWORKDAYS(A2,H2)"},
    {"title": "Build Pivot Table 1 — Revenue by Rep by Quarter", "label": "1: Excel", "body": "New sheet 'Rev by Rep'.\nRows: Rep Name. Columns: Quarter. Values: Sum of Amount.\nMost-requested sales report format."},
    {"title": "Build Pivot Table 2 — Win Rate by Industry", "label": "1: Excel", "body": "New sheet 'Win Rate'.\nRows: Industry. Values: Sum of Won Flag, Count of Status.\nAdd calculated field: Win Rate = Won Flag / Status. Format as percentage."},
    {"title": "Build Pivot Table 3 — Budget vs Actual", "label": "1: Excel", "body": "New sheet 'Budget vs Actual'.\nRows: Rep Name. Values: Sum of Amount and Budget.\nAdd calculated field: Variance = Amount - Budget.\nConditional formatting: green positive, red negative."},
    {"title": "Build Pivot Table 4 — Deal Size Mix by Industry", "label": "1: Excel", "body": "New sheet 'Deal Size Mix'.\nRows: Deal Size Category. Columns: Industry. Values: Count of deals."},
    {"title": "Build Pivot Table 5 — Average Days to Close", "label": "1: Excel", "body": "New sheet 'Avg Days to Close'.\nRows: Rep Name. Values: Average of Days to Close."},
    {"title": "Apply pro Excel tricks: Flash Fill, XLOOKUP, Conditional Formatting, Data Validation", "label": "1: Excel", "body": "Flash Fill: Ctrl+E to split full names into first/last.\nXLOOKUP: pull rep territory from reference table.\nConditional Formatting: red fill for % to Budget below 70%.\nData Validation: dropdown for Status column.\nFreeze top row: View → Freeze Panes."},
    {"title": "Practice COUNTIFS and SUMIFS formulas", "label": "1: Excel", "body": "COUNTIFS: =COUNTIFS(B:B,\"Sarah Chen\",G:G,\"Open\")\nSUMIFS: =SUMIFS(E:E,B:B,\"Sarah Chen\",C:C,\"Automotive\")\nThese two functions handle 80% of real-world Excel reporting needs."},

    # Phase 2: D365 CRM
    {"title": "Log in to D365 and configure organization settings", "label": "2: D365 CRM", "body": "Set organization name to 'RonTech Magnets'.\nSet fiscal year to January-December.\nSet base currency to USD.\nSet timezone to Central Time (Oklahoma City)."},
    {"title": "Create 5 customer accounts", "label": "2: D365 CRM", "body": "Create these accounts in Sales → Accounts → New:\n- Tesla — Automotive — Austin TX\n- Siemens — Industrial — Chicago IL\n- Medtronic — Medical — Minneapolis MN\n- Lockheed Martin — Aerospace — Fort Worth TX\n- Samsung — Electronics — San Jose CA"},
    {"title": "Create 10 contacts (2 per company)", "label": "2: D365 CRM", "body": "Tesla: James Carter (Procurement Manager), Amy Lin (Engineering Lead)\nSiemens: Robert Klein (Operations Director), Nina Shah (Buyer)\nMedtronic: David Park (Supply Chain Manager), Laura White (R&D Lead)\nLockheed: Brian Scott (VP Procurement), Michelle Reed (Systems Engineer)\nSamsung: Kevin Yoon (Component Buyer), Priya Nair (Product Manager)"},
    {"title": "Create 7 custom fields on Opportunity form", "label": "2: D365 CRM", "body": "Settings → Customizations → Customize the System → Opportunity → Fields:\n- Magnet Grade (Single Line Text)\n- Shape (Option Set: Disc, Ring, Block, Arc)\n- Coating (Option Set: Nickel, Zinc, Epoxy, Uncoated)\n- Polarity Marking (Two Options: Yes/No)\n- Packaging Type (Option Set: Bulk, Custom Box, Retail)\n- At Risk (Two Options: Yes/No)\n- Deal Size Category (Option Set: Small, Medium, Large)"},
    {"title": "Add custom fields to Opportunity form and publish", "label": "2: D365 CRM", "body": "Open Opportunity main form.\nDrag each new field onto the form.\nSave and click Publish All Customizations.\nVerify all fields are visible on the form."},
    {"title": "Create 10 opportunities with realistic magnet data", "label": "2: D365 CRM", "body": "EV Motor Magnets — Tesla — Sarah Chen — Negotiation — $85,000 — N52, Arc, Nickel\nIndustrial Sensors — Siemens — Mike Patel — Proposal — $42,000 — N42, Ring, Zinc\nMRI Components — Medtronic — Lisa Torres — Qualified — $67,000 — N35, Disc, Epoxy\nGuidance Systems — Lockheed — Mike Patel — Prospecting — $120,000 — N48, Block, Uncoated\nSpeaker Magnets — Samsung — Sarah Chen — Closed Won — $28,000 — N38, Disc, Nickel\nMotor Assembly — Tesla — Sarah Chen — Proposal — $55,000 — N50, Arc, Nickel\nPump Magnets — Siemens — Mike Patel — Qualified — $33,000 — N42, Ring, Zinc\nSurgical Tools — Medtronic — Lisa Torres — Negotiation — $78,000 — N45, Disc, Epoxy\nRadar Parts — Lockheed — Mike Patel — Closed Lost — $95,000 — N52, Block, Uncoated\nDisplay Magnets — Samsung — Sarah Chen — Prospecting — $18,000 — N35, Ring, Nickel"},
    {"title": "Mark Surgical Tools and Guidance Systems as At Risk", "label": "2: D365 CRM", "body": "Open both opportunities and set At Risk = Yes.\nAdd note: 'Customer delayed decision, budget review in progress'."},
    {"title": "Create 3 sales rep user accounts", "label": "2: D365 CRM", "body": "Settings → Security → Users → New. Assign Salesperson security role.\n- Sarah Chen — Territory: Automotive + Electronics\n- Mike Patel — Territory: Aerospace + Industrial\n- Lisa Torres — Territory: Medical\nAssign opportunities to correct reps based on industry."},
    {"title": "Configure security permissions for reps and Ron", "label": "2: D365 CRM", "body": "Reps: security role read scope = User (own records only).\nRon: security role read scope = Organization (sees everything)."},
    {"title": "Log activity history on every opportunity", "label": "2: D365 CRM", "body": "For each of the 10 opportunities log:\n- 2 emails\n- 1 phone call note\n- 1 follow-up task with due date\nVerify every opportunity has at least 3 activity records in timeline."},
    {"title": "Create Personal View — Ron's At Risk Deals", "label": "2: D365 CRM", "body": "Filter: At Risk = Yes AND Stage = Negotiation.\nSave as personal view 'Ron's At Risk Deals'."},
    {"title": "Create System View — This Week's Follow-ups", "label": "2: D365 CRM", "body": "Settings → Customizations → System Views → New.\nFilter: Tasks Due Date in next 7 days.\nSave as 'This Week's Follow-ups'."},
    {"title": "Create Email Template for rep follow-ups", "label": "2: D365 CRM", "body": "Settings → Templates → Email Templates → New.\nBuild follow-up template using Opportunity Name and Magnet Grade fields.\nReps insert with one click — saves 5 minutes per email."},
    {"title": "Set up Duplicate Detection Rules", "label": "2: D365 CRM", "body": "Settings → Data Management → Duplicate Detection Rules.\nCreate rule that flags accounts with the same name.\nPrevents duplicate Tesla, Siemens etc. records."},
    {"title": "Create D365 Dashboard with pipeline tiles", "label": "2: D365 CRM", "body": "Dashboards → New. Add these tiles:\n- Open opportunities count\n- Pipeline by stage chart\n- Overdue tasks list\n- Top 5 deals by amount"},
    {"title": "Set up Business Process Flow on Opportunity", "label": "2: D365 CRM", "body": "Settings → Processes → New → Business Process Flow.\nStages: Prospecting → Qualified → Proposal → Negotiation → Closed.\nForces reps to follow the correct sales process."},

    # Phase 3: Outlook
    {"title": "Configure server-side sync between Outlook and D365", "label": "3: Outlook", "body": "Settings → Email Configuration → Email Server Profiles.\nSet up connection to Cacacumo Outlook server.\nApprove mailbox and click 'Test & Enable Mailbox'.\nWait for green checkmark."},
    {"title": "Test email sync between Outlook and D365", "label": "3: Outlook", "body": "Send a real email from Outlook to a D365 contact.\nOpen D365 → contact record → verify email appears in timeline.\nIf yes, sync is working correctly."},
    {"title": "Connect alias emails for fake sales reps", "label": "3: Outlook", "body": "Create alias addresses: sarah@cacacumo.com, mike@cacacumo.com, lisa@cacacumo.com.\nConfigure each in D365 mailboxes.\nVerify activity timeline on each contact shows synced emails."},

    # Phase 4: Power Automate
    {"title": "Build Flow 1 — Stale Deal Alert", "label": "4: Power Automate", "body": "Scheduled flow, runs daily at 8am.\nList D365 opportunities modified more than 5 days ago.\nSend Ron one consolidated email with all stale deals in a table.\nSubject: 'Stale Deal Alert — [count] deals need attention'."},
    {"title": "Build Flow 2 — Stage Change Notification", "label": "4: Power Automate", "body": "Trigger: When D365 Opportunity record is updated.\nCondition: Stage changes to Negotiation.\nAction: Send Ron immediate email with deal name, company, rep, and amount."},
    {"title": "Build Flow 3 — New Lead Auto Assignment", "label": "4: Power Automate", "body": "Trigger: When new Lead is created in D365.\nSwitch on Industry field:\n- Automotive/Electronics → Sarah Chen\n- Aerospace/Industrial → Mike Patel\n- Medical → Lisa Torres\nElse: email Ron to assign manually.\nSend assigned rep a welcome email with lead details."},
    {"title": "Build Flow 4 — Closed Won Celebration", "label": "4: Power Automate", "body": "Trigger: Opportunity status changes to Closed Won.\nAction 1: Post message in Teams channel 'Sales Wins'.\nAction 2: Send rep a congratulations email.\nUse parallel branches so both actions run simultaneously."},
    {"title": "Build Flow 5 — Weekly Pipeline Summary", "label": "4: Power Automate", "body": "Scheduled flow, every Monday at 8am.\nList all open opportunities from D365.\nBuild HTML email with pipeline grouped by stage with totals.\nSend to Ron. Subject: 'Weekly Pipeline Summary — [Date]'."},
    {"title": "Build Flow 6 — Overdue Task Reminder", "label": "4: Power Automate", "body": "Scheduled flow, daily at 9am.\nList all tasks past due date.\nSend assigned rep a reminder email.\nIf task is more than 3 days overdue, CC Ron."},
    {"title": "Add error handling to all flows", "label": "4: Power Automate", "body": "In each flow, after main action add 'Configure run after' set to 'has failed'.\nAdd action to send yourself an email with error details.\nBookmark run history page and check daily."},
    {"title": "Use variables and Apply to Each for dynamic content", "label": "4: Power Automate", "body": "Flow 5: Use Initialize Variable and Append to Variable inside Apply to Each loop.\nBuild email text dynamically from data instead of hardcoding.\nFlow 1: collect all stale deals into one HTML table before sending."},

    # Phase 5: Power BI
    {"title": "Connect Power BI to clean Excel file", "label": "5: Power BI", "body": "Home → Get Data → Excel → Ron_Sales_Data_Clean.xlsx.\nClick Transform Data to enter Power Query.\nInspect data before loading."},
    {"title": "Connect Power BI to D365 Sales", "label": "5: Power BI", "body": "Home → Get Data → Online Services → Dynamics 365.\nEnter D365 environment URL.\nSelect Opportunities, Accounts, and Contacts tables.\nClick Transform Data."},
    {"title": "Clean data in Power Query", "label": "5: Power BI", "body": "Rename columns: replace spaces with underscores.\nSet correct data types: Amount/Budget = Currency, Dates = Date, text fields = Text.\nAdd custom Deal Size column.\nRemove null rows.\nClose and Apply."},
    {"title": "Merge Excel and D365 tables in Power Query", "label": "5: Power BI", "body": "Home → Merge Queries → As New.\nMerge Excel table with D365 Opportunities on Rep_Name.\nExpand only needed columns: Stage, At_Risk, Magnet_Grade."},
    {"title": "Create relationships between tables in Model view", "label": "5: Power BI", "body": "Click Model view (third icon on left).\nDrag Rep Name from Excel table onto Rep Name in D365 Opportunities.\nVerify cardinality is set to many-to-one."},
    {"title": "Create DAX measures: Total Pipeline, Total Won, Win Rate, % to Budget", "label": "5: Power BI", "body": "Total Pipeline = SUM(Opportunities[Amount])\nTotal Won = CALCULATE(SUM(Opportunities[Amount]), Opportunities[Status]=\"Closed Won\")\nWin Rate = DIVIDE([Total Won], [Total Pipeline], 0)\n% to Budget = DIVIDE(SUM(Opportunities[Amount]), SUM(Opportunities[Budget]), 0)"},
    {"title": "Create DAX measures: Avg Deal Size, Deals at Risk, YTD Revenue", "label": "5: Power BI", "body": "Avg Deal Size = AVERAGE(Opportunities[Amount])\nDeals at Risk = COUNTROWS(FILTER(Opportunities, Opportunities[At_Risk]=\"Yes\"))\nYTD Revenue = TOTALYTD(SUM(Opportunities[Amount]), Dates[Date])"},
    {"title": "Build Page 1 — Executive Summary", "label": "5: Power BI", "body": "3 card visuals: Total Pipeline, Total Won YTD, % to Budget.\nGauge: % to Budget with target at 100%.\nTable: top 3 deals closing this month.\nDonut chart: Won vs Lost."},
    {"title": "Build Page 2 — Sales Rep Performance", "label": "5: Power BI", "body": "Bar chart: Revenue by Rep.\nBar chart: Win Rate by Rep.\nBar chart: Avg Deal Size by Rep.\nTable: Activity Count per rep (last 30 days).\nClustered bar: Rep vs Budget comparison."},
    {"title": "Build Page 3 — Pipeline Health", "label": "5: Power BI", "body": "Funnel chart: Deals by Stage.\nBar chart: Pipeline Value by Stage.\nTable: At Risk deals with red conditional formatting.\nBar chart: Average days in each stage.\nPie chart: Pipeline by Industry."},
    {"title": "Build Page 4 — Product Analytics", "label": "5: Power BI", "body": "Bar chart: Revenue by Magnet Grade.\nBar chart: Revenue by Coating Type.\nMatrix: Most popular Shape by Industry.\nDonut: Packaging Type distribution."},
    {"title": "Build Page 5 — Budget vs Actual", "label": "5: Power BI", "body": "Line chart: Monthly bookings vs budget.\nGauge: Quarter to date vs target.\nLine chart: Forecast to year end (use Analytics → Forecast).\nTable: Underperforming reps flagged red (below 70%), yellow (70-90%), green (above 90%)."},

    # Phase 6: AI Reporting
    {"title": "Enrich Excel data with Customer Comments, Loss Reason, Next Action columns", "label": "6: AI Reporting", "body": "Add to Ron_Sales_Data_Clean.xlsx:\n- Customer Comments: 1-2 sentences of fake feedback per row\n- Loss Reason: for Closed Lost deals (Lost on price, Competitor won, etc.)\n- Next Action: for open deals (Send revised quote, Schedule technical call, etc.)\nSave as 'Ron_Sales_Data_Enriched.xlsx'."},
    {"title": "Build Report A — Microsoft Copilot in Power BI", "label": "6: AI Reporting", "body": "Enable Copilot: File → Options → Preview Features → Copilot.\nLoad enriched Excel into new Power BI file.\nPrompt Copilot: 'Create a report page summarizing sales performance, win rates, and reasons for lost deals'.\nRefine with follow-up prompts.\nSave as 'Report_A_Copilot_Generated.pbix'."},
    {"title": "Build Report B — Claude AI analysis", "label": "6: AI Reporting", "body": "Export enriched Excel as CSV: 'sales_data_for_claude.csv'.\nUpload to claude.ai.\nAsk Claude to: analyze win rates, identify top 3 loss reasons, flag underperforming reps.\nAsk for a board-ready 1-page narrative.\nAsk Claude to suggest 5 Power BI visuals with exact specs.\nSave output as 'Report_B_Claude_Generated.docx'."},
    {"title": "Compare Copilot vs Claude and build summary table", "label": "6: AI Reporting", "body": "Create comparison table: Tool, Strength, Weakness, Best Use Case.\nCopilot: faster for visuals inside Power BI.\nClaude: stronger for narrative analysis and explanation.\nPractice presenting both to Ron out loud."},

    # Phase 7: Final
    {"title": "Replace Excel source with live D365 data in Power BI", "label": "7: Final", "body": "Open main dashboard PBIX.\nIn Power Query, change source from Excel file to D365 Opportunities table.\nMap columns correctly.\nDashboard now pulls live data instead of static Excel file."},
    {"title": "Publish dashboard and set scheduled refresh", "label": "7: Final", "body": "Publish to Power BI Service (powerbi.com).\nDataset → Settings → Scheduled Refresh → set to 7am daily.\nShare with Ron (Viewer role).\nReps should not have access."},
    {"title": "Test end-to-end: stage change triggers flow and updates dashboard", "label": "7: Final", "body": "In D365, move one opportunity from Qualified to Negotiation.\nVerify Power Automate Flow 2 emails Ron within seconds.\nVerify Power BI reflects the change after next refresh.\nEnd-to-end test passed."},
    {"title": "Scenario 1 — Give Ron today's pipeline in under 2 minutes", "label": "7: Final", "body": "Open Power BI → Pipeline Health page → screenshot.\nWalk through: total open deals, value by stage, deals at risk.\nPractice doing this in under 2 minutes."},
    {"title": "Scenario 2 — Onboard a new sales rep in under 15 minutes", "label": "7: Final", "body": "Create new user in D365 (5 min).\nAssign territory and permissions (3 min).\nConnect Outlook (2 min).\nUpdate Flow 3 to include new rep (2 min).\nRep is ready in under 15 minutes."},
    {"title": "Scenario 3 — Export Q3 forecast for Finance in under 3 minutes", "label": "7: Final", "body": "Power BI Budget vs Actual page → filter to Q3 → Export → Excel.\nEmail to Finance.\nWithout your dashboard this would take Finance 2 days manually."},
    {"title": "Scenario 4 — Investigate and resolve a stale deal", "label": "7: Final", "body": "Show Ron the Power Automate stale deal email.\nOpen D365 → opportunity record → show the activity gap.\nUpdate opportunity with new contact attempt.\nVerify tomorrow's stale alert no longer includes it.\nDemonstrates the full automation loop in action."},
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
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ Failed: {title} — {e.code}: {error_body}")
        return False

print(f"Creating {len(issues)} issues in {REPO_OWNER}/{REPO_NAME}...\n")

for i, issue in enumerate(issues):
    create_issue(issue["title"], issue["label"], issue["body"])
    time.sleep(1)  # Avoid hitting GitHub rate limits

print(f"\n🎉 Done! All issues processed.")
