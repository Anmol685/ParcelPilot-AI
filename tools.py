import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader

EXCEL_PATH = "data/excel/ParcelPilot_Assessment_Data.xlsx"
PDF_FOLDER = "data/pdfs"

# ==========================
# PDF SEARCH
# ==========================
def search_documents(query):
    if not os.path.exists(PDF_FOLDER):
        return "PDF folder not found."

    query = query.lower()
    best_doc = ""
    best_text = ""
    best_score = 0

    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(PDF_FOLDER, file))
            pages = loader.load()

            for page in pages:
                text = page.page_content
                score = sum(1 for word in query.split() if word in text.lower())

                if score > best_score:
                    best_score = score
                    best_doc = file
                    best_text = text[:700]

    if best_score == 0:
        return "No matching policy found."

    return f"""## 📄 Relevant Policy

**Document:** {best_doc}

### Relevant Excerpt

{best_text}
"""


# ==========================
# EXCEL INFO
# ==========================
def get_excel_info():
    if not os.path.exists(EXCEL_PATH):
        return "Excel file not found."

    xl = pd.ExcelFile(EXCEL_PATH)

    return "Workbook Loaded!\n\nSheets:\n" + "\n".join(xl.sheet_names)


# ==========================
# ORDER LOOKUP
# ==========================
def get_order(order_id):
    xl = pd.ExcelFile(EXCEL_PATH)

    orders = pd.read_excel(xl, "orders")
    accounts = pd.read_excel(xl, "accounts")

    orders.columns = orders.columns.str.strip()
    accounts.columns = accounts.columns.str.strip()

    row = orders[orders["order_id"] == order_id.upper().strip()]

    if row.empty:
        return "Order not found."

    row = row.iloc[0]

    acc = accounts[accounts["account_id"] == row["account_id"]]

    account_name = "Unknown"

    if not acc.empty:
        account_name = acc.iloc[0]["account_name"]

    return f"""## 📦 Order Details

**Order ID:** {row['order_id']}

**Account:** {account_name}

**Carrier:** {row['carrier']}

**Status:** {row['status']}

**Booked At:** {row['booked_at']}

**Pickup Window:** {row['pickup_window_start']} → {row['pickup_window_end']}

**Shipment Fee:** ₹{row['shipment_fee_inr']}
"""


# ==========================
# TICKET LOOKUP
# ==========================
def get_ticket(ticket_id):
    xl = pd.ExcelFile(EXCEL_PATH)

    tickets = pd.read_excel(xl, "tickets")
    accounts = pd.read_excel(xl, "accounts")

    tickets.columns = tickets.columns.str.strip()
    accounts.columns = accounts.columns.str.strip()

    row = tickets[tickets["ticket_id"] == ticket_id.upper().strip()]

    if row.empty:
        return "Ticket not found."

    row = row.iloc[0]

    acc = accounts[accounts["account_id"] == row["account_id"]]

    account_name = "Unknown"

    if not acc.empty:
        account_name = acc.iloc[0]["account_name"]

    return f"""## 🎫 Ticket Details

**Ticket ID:** {row['ticket_id']}

**Account:** {account_name}

**Status:** {row['status']}

**Subject:** {row['subject']}

**Description:** {row['description']}

**Channel:** {row['channel']}

**Assigned To:** {row['assigned_to']}
"""


# ==========================
# AI REPLY
# ==========================
def ai_reply(query):
    q = query.lower()

    if "shipment creation" in q or "500" in q:
        return """## 🤖 AI Resolution

**Issue:** HTTP 500 while creating shipments.

**Priority:** P1 (Critical)

### Recommended Action

- Escalate to Backend Engineering
- Check shipment API logs
- Existing shipments remain accessible
"""

    if "cancellation" in q:
        return """## 🤖 Cancellation Guidance

Orders cancelled within **30 minutes** incur **no fee**.

After 30 minutes, the default cancellation fee is **₹250**, unless the customer agreement waives it.
"""

    if "service credit" in q:
        return """## 🤖 Service Credit

Service credits depend on the Support Policy and customer agreement.
"""

    return "I couldn't find an exact answer. Try ORD-1001, TKT-501, or a policy keyword."


# ==========================
# ESCALATION TOOL
# ==========================
def create_escalation(ticket_id):
    return f"""## 🚨 Escalation Prepared

**Ticket:** {ticket_id}

**Priority:** P1

**Assigned Team:** Backend Engineering

Type **CONFIRM** to create this escalation.
"""