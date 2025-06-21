# # Copyright (c) 2024, Arkay Apps and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.utils import add_days, today, getdate
# from datetime import datetime, timedelta

# def get_first_and_last_day_of_month(date):
#     # Convert date to datetime object
#     date = getdate(date)
#     # Get the first day of the month
#     first_day = date.replace(day=1)
#     # Get the last day of the month
#     next_month = first_day + timedelta(days=32)  # Move to the next month
#     last_day = next_month.replace(day=1) - timedelta(days=1)
#     return first_day, last_day

# def execute(filters=None):
#     columns = [
#         {"fieldname": "party_name", "label": "<b>Party Name</b>", "fieldtype": "Data", "width": 250},
#         {"fieldname": "item_name", "label": "<b>Item</b>", "fieldtype": "Data", "width": 150},
#         {"fieldname": "qty", "label": "<b>Quantity</b>", "fieldtype": "Float", "width": 100},
#         {"fieldname": "royalty", "label": "<b>Royalty</b>", "fieldtype": "Data", "width": 100},
#     ]
#     period = filters.get("period", "Daily")
    
#     if period == "Daily":
#         date_condition = "pr.posting_date = %s"
#         date_value = add_days(today(), -1)
#     elif period == "Monthly":
#         first_day, last_day = get_first_and_last_day_of_month(today())
#         date_condition = "pr.posting_date BETWEEN %s AND %s"
#         date_value = (first_day, last_day)
    
#     query = f"""
#         SELECT 
#             pr.supplier AS party_name, 
#             pri.item_name AS item_name, 
#             SUM(pri.qty) AS qty,
#             COALESCE(NULLIF(pr.custom_royalty_type, ''), ' ') AS royalty
#         FROM 
#             `tabPurchase Receipt` pr
#         JOIN 
#             `tabPurchase Receipt Item` pri ON pr.name = pri.parent
#         WHERE 
#             pr.docstatus = 1 AND {date_condition}
#         GROUP BY 
#             pr.supplier, pri.item_name, royalty
#         ORDER BY 
#             pr.supplier, royalty, pri.item_name
#     """

#     data = frappe.db.sql(query, date_value, as_dict=1)

#     return columns, data



#  ________ Here forth changes done on 19th June,25. Changes done for Royalty Qty

# # Copyright (c) 2024, Arkay Apps and contributors
# # For license information, please see license.txt

import frappe
from frappe.utils import add_days, today, getdate
from datetime import datetime, timedelta

# def get_first_and_last_day_of_month(date):
#     # Convert date to datetime object
#     date = getdate(date)
#     # Get the first day of the month
#     first_day = date.replace(day=1)
#     # Get the last day of the month
#     next_month = first_day + timedelta(days=32)  # Move to the next month
#     last_day = next_month.replace(day=1) - timedelta(days=1)
#     return first_day, last_day

# def execute(filters=None):
#     columns = [
#         {"fieldname": "party_name", "label": "<b>Party Name</b>", "fieldtype": "Data", "width": 250},
#         {"fieldname": "item_name", "label": "<b>Item</b>", "fieldtype": "Data", "width": 150},
#         {"fieldname": "qty", "label": "<b>Quantity</b>", "fieldtype": "Float", "width": 100},
#         {"fieldname": "royalty", "label": "<b>Royalty</b>", "fieldtype": "Data", "width": 100},
#     ]
#     period = filters.get("period", "Daily")
    
#     if period == "Daily":
#         date_condition = "pr.posting_date = %s"
#         date_value = add_days(today(), -1)
#     elif period == "Monthly":
#         first_day, last_day = get_first_and_last_day_of_month(today())
#         date_condition = "pr.posting_date BETWEEN %s AND %s"
#         date_value = (first_day, last_day)
    
#     query = f"""
#         SELECT 
#             pr.supplier AS party_name, 
#             pri.item_name AS item_name, 
#             SUM(pri.qty) AS qty,
#             COALESCE(NULLIF(pr.custom_royalty_type, ''), ' ') AS royalty
#         FROM 
#             `tabPurchase Receipt` pr
#         JOIN 
#             `tabPurchase Receipt Item` pri ON pr.name = pri.parent
#         WHERE 
#             pr.docstatus = 1 AND {date_condition}
#         GROUP BY 
#             pr.supplier, pri.item_name, royalty
#         ORDER BY 
#             pr.supplier, royalty, pri.item_name
#     """

#     data = frappe.db.sql(query, date_value, as_dict=1)

#     return columns, data

def get_first_and_last_day_of_month(date):
    date = getdate(date)
    first_day = date.replace(day=1)
    next_month = (first_day + timedelta(days=32)).replace(day=1)
    last_day = next_month - timedelta(days=1)
    return first_day, last_day

def execute(filters=None):
    from frappe.utils import today, add_days
    from datetime import timedelta

    columns = [
        {"fieldname": "party_name", "label": "<b>Party Name</b>", "fieldtype": "Data", "width": 250},
        {"fieldname": "item_name", "label": "<b>Item</b>", "fieldtype": "Data", "width": 150},
        {"fieldname": "qty", "label": "<b>Quantity</b>", "fieldtype": "Float", "width": 100},        
        {"fieldname": "royalty_qty", "label": "<b>Royalty Quantity</b>", "fieldtype": "Float", "width": 150},
        {"fieldname": "royalty", "label": "<b>Royalty</b>", "fieldtype": "Data", "width": 100},
    ]

    conditions = ["pr.docstatus = 1"]
    values = []

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")
    period = filters.get("period")
    supplier = filters.get("supplier")

    # Case 1: If from_date and to_date exist, use them directly
    if from_date and to_date:
        conditions.append("pr.posting_date BETWEEN %s AND %s")
        values += [getdate(from_date), getdate(to_date)]

    # Case 2: Only from_date
    elif from_date:
        conditions.append("pr.posting_date >= %s")
        values.append(getdate(from_date))

    # Case 3: Only to_date
    elif to_date:
        conditions.append("pr.posting_date <= %s")
        values.append(getdate(to_date))

    # Case 4: No dates given, but period is selected
    elif period == "Daily":
        filters["from_date"] = filters["to_date"] = add_days(today(), -1)
        conditions.append("pr.posting_date = %s")
        values.append(getdate(filters["from_date"]))

    elif period == "Monthly":
        from_date, to_date = get_first_and_last_day_of_month(today())
        conditions.append("pr.posting_date BETWEEN %s AND %s")
        values += [from_date, to_date]


    if supplier:
        conditions.append("pr.supplier = %s")
        values.append(supplier)

    # else: No date filters at all (fetch all data with docstatus = 1)

    where_clause = " AND ".join(conditions)

    query = f"""
        SELECT 
            pr.supplier AS party_name, 
            pri.item_name AS item_name, 
            SUM(pri.qty) AS qty,
            Sum(pri.custom_royalty_qty) AS royalty_qty,
            COALESCE(NULLIF(pr.custom_royalty_type, ''), ' ') AS royalty
        FROM 
            `tabPurchase Receipt` pr
        JOIN 
            `tabPurchase Receipt Item` pri ON pr.name = pri.parent
        WHERE 
            {where_clause}
        GROUP BY 
            pr.supplier, pri.item_name, royalty
        ORDER BY 
            pr.supplier, royalty, pri.item_name
    """

    data = frappe.db.sql(query, values, as_dict=1)

    return columns, data
