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
    period = filters.get("period", "Daily")
    
    if period == "Daily":
        # Get yesterday's date
        date_condition = "jb.date = %s"
        date_value = add_days(today(), -1)
    elif period == "Monthly":
        # Get the first and last day of the current month
        first_day, last_day = get_first_and_last_day_of_month(today())
        date_condition = "jb.date BETWEEN %s AND %s"
        date_value = (first_day, last_day)

    columns = [
        {"fieldname": "jumbo_bag_name", "label": "<b>Jumbo Bag Name</b>", "fieldtype": "Data", "width": 250},
        {"fieldname": "quantity", "label": "<b>Quantity</b>", "fieldtype": "Float", "width": 100},
        {"fieldname": "warehouse", "label": "<b>Warehouse</b>", "fieldtype": "Data", "width": 150},
    ]


    # Corrected SQL query with date condition
    query = f"""
        SELECT 
            jbi.item AS jumbo_bag_name,
            SUM(jbi.quantity) AS quantity,
            jb.warehouse AS warehouse
        FROM 
            `tabJumbo Bag Items` jbi
        JOIN 
            `tabManufacture Process` jb ON jbi.parent = jb.name
        WHERE 
        	jb.docstatus = 1 AND {date_condition}
        GROUP BY 
            jbi.item, jb.warehouse
        ORDER BY 
            jbi.item, jb.warehouse
    """

    data = frappe.db.sql(query, date_value, as_dict=1)

    return columns, data
