import pandas as pd
import os

EXCEL_PATH = os.path.join(
    "data",
    "excel",
    "ParcelPilot_Assessment_Data.xlsx"
)

# Load workbook
xls = pd.ExcelFile(EXCEL_PATH)

orders = pd.read_excel(xls, sheet_name="orders")
accounts = pd.read_excel(xls, sheet_name="accounts")
tickets = pd.read_excel(xls, sheet_name="tickets")

# Clean column names
orders.columns = orders.columns.str.strip()
accounts.columns = accounts.columns.str.strip()
tickets.columns = tickets.columns.str.strip()


def format_result(df, value, title):
    value = str(value).strip().upper()

    # Search in every column
    for col in df.columns:
        result = df[
            df[col].astype(str).str.strip().str.upper() == value
        ]

        if not result.empty:
            row = result.iloc[0]

            text = f"## {title}\n\n"

            for c in row.index:
                v = row[c]
                if pd.isna(v):
                    v = "N/A"

                text += f"**{c}** : {v}\n\n"

            return text

    return f"❌ {title} not found."


def get_order(order_id):
    return format_result(
        orders,
        order_id,
        f"Order Details ({order_id})"
    )


def get_account(account_id):
    return format_result(
        accounts,
        account_id,
        f"Account Details ({account_id})"
    )


def get_ticket(ticket_id):
    return format_result(
        tickets,
        ticket_id,
        f"Ticket Details ({ticket_id})"
    )