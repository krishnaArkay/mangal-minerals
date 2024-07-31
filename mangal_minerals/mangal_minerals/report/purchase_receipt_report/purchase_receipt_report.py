# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_days, today, getdate
from datetime import datetime, timedelta

def get_first_and_last_day_of_month(date):
    # Convert date to datetime object
    date = getdate(date)
    # Get the first day of the month
    first_day = date.replace(day=1)
    # Get the last day of the month
    next_month = first_day + timedelta(days=32)  # Move to the next month
    last_day = next_month.replace(day=1) - timedelta(days=1)
    return first_day, last_day

def execute(filters=None):
    columns = [
        {"fieldname": "party_name", "label": "<b>Party Name</b>", "fieldtype": "Data", "width": 250},
        {"fieldname": "item_name", "label": "<b>Item</b>", "fieldtype": "Data", "width": 150},
        {"fieldname": "qty", "label": "<b>Quantity</b>", "fieldtype": "Float", "width": 100},
        {"fieldname": "royalty", "label": "<b>Royalty</b>", "fieldtype": "Data", "width": 100},
    ]
    period = filters.get("period", "Daily")
    
    if period == "Daily":
        date_condition = "pr.posting_date = %s"
        date_value = add_days(today(), -1)
    elif period == "Monthly":
        first_day, last_day = get_first_and_last_day_of_month(today())
        date_condition = "pr.posting_date BETWEEN %s AND %s"
        date_value = (first_day, last_day)
    
    query = f"""
        SELECT 
            pr.supplier AS party_name, 
            pri.item_name AS item_name, 
            SUM(pri.qty) AS qty,
            COALESCE(NULLIF(pr.custom_royalty_type, ''), ' ') AS royalty
        FROM 
            `tabPurchase Receipt` pr
        JOIN 
            `tabPurchase Receipt Item` pri ON pr.name = pri.parent
        WHERE 
            pr.docstatus = 0 AND {date_condition}
        GROUP BY 
            pr.supplier, pri.item_name, royalty
        ORDER BY 
            pr.supplier, royalty, pri.item_name
    """

    data = frappe.db.sql(query, date_value, as_dict=1)

    return columns, data
