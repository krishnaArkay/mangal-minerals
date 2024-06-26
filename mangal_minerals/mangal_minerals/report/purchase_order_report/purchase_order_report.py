# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta

def execute(filters=None):
    columns = [
    {"label": "<b>Name</b>", "fieldname": "name", "fieldtype": "Link", "options": "Purchase Order", "width": 190},
    {"label": "<b>Supplier</b>", "fieldname": "supplier", "fieldtype": "Link", "options": "Supplier", "width": 230},
    {"label": "<b>Date</b>", "fieldname": "transaction_date", "fieldtype": "Date", "width": 130},
    {"label": "<b>Royalty Type</b>", "fieldname": "custom_royalty_type", "fieldtype": "Data", "width": 130},
    {"label": "<b>Transporter Type</b>", "fieldname": "custom_transporter_type", "fieldtype": "Data", "width": 180},
    # {"label": "<b>Item name</b>", "fieldname": "item", "fieldtype": "Data", "width": 150},
    # {"label": "<b>Quantity</b>", "fieldname": "qty", "fieldtype": "float", "width": 80},
    {"label": "<b>Total</b>", "fieldname": "rounded_total", "fieldtype": "Currency", "width": 130},
    
]

    data = get_data(filters)
    return columns, data

def get_data(filters):
    conditions = {"docstatus": 1}

    if filters.get("period"):
        start_date, end_date = calculate_date_range(filters["period"])
        conditions["transaction_date"] = ["between", [start_date, end_date]]
    elif filters.get("from_date") and filters.get("to_date"):
        conditions["transaction_date"] = ["between", [filters.get("from_date"), filters.get("to_date")]]
    elif filters.get("from_date"):
        conditions["transaction_date"] = [">=", filters.get("from_date")]
    elif filters.get("to_date"):
        conditions["transaction_date"] = ["<=", filters.get("to_date")]
        
    # if filters.get("name"):
    #     conditions["name"] = filters["name"]

    if filters.get("supplier"):
        conditions["supplier"] = filters["supplier"]

    if filters.get("custom_royalty_type"):
        conditions["custom_royalty_type"] = filters["custom_royalty_type"]

    if filters.get("custom_transporter_type"):
        conditions["custom_transporter_type"] = filters["custom_transporter_type"]

        
    data = []
    po_list = frappe.get_list(
        "Purchase Order",
        fields=["name", "supplier", "transaction_date", "rounded_total", "custom_royalty_type", "custom_transporter_type"],
        filters=conditions
    )
    for po in po_list:
    #     po_doc = frappe.get_doc("Purchase Order", po.name)
    #     for item in po_doc.items:
        data.append({
            "name": po.name,
            "supplier": po.supplier,
            "transaction_date": po.transaction_date,
            "custom_royalty_type": po.custom_royalty_type,
            "custom_transporter_type": po.custom_transporter_type,
            # "item": item.item_code,  # Adjust based on your actual field name for item code/name
            # "qty": item.qty,
            "rounded_total": po.rounded_total,
        })
    return data


def calculate_date_range(period):
    today = datetime.today()
    if period == "Weekly":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period == "Monthly":
        start_date = today.replace(day=1)
        end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    elif period == "Quarterly":
        current_quarter = (today.month - 1) // 3 + 1
        start_date = datetime(today.year, 3 * current_quarter - 2, 1)
        end_date = (start_date + timedelta(days=92)).replace(day=1) - timedelta(days=1)
    elif period == "Yearly":
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)
    else:
        start_date = end_date = today  # default to today if period is unknown

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
