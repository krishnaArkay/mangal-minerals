# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "date", "label": _("<b>Date</b>"), "fieldtype": "Date", "width": 120},
        {"fieldname": "item_name", "label": _("<b>Item Name</b>"), "fieldtype": "Data", "width": 150},
        {"fieldname": "qty", "label": _("<b>Quantity</b>"), "fieldtype": "Data", "width": 90},
        {"fieldname": "from_warehouse", "label": _("<b>From Warehouse</b>"), "fieldtype": "Data", "width": 180},
        {"fieldname": "to_warehouse", "label": _("<b>To Warehouse</b>"), "fieldtype": "Data", "width": 180},
        {"fieldname": "vehicle_type", "label": _("<b>Type</b>"), "fieldtype": "Data", "width": 100},
        {"fieldname": "vehicle", "label": _("<b>Vehicle</b>"), "fieldtype": "Data", "width": 150},
        {"fieldname": "trip", "label": _("<b>Trip</b>"), "fieldtype": "Data", "width": 70},
        {"fieldname": "transporter_name", "label": _("<b>Transporter Name</b>"), "fieldtype": "Data", "width": 150, "align":"Left"},
        {"fieldname": "remarks", "label": _("<b>Remarks</b>"), "fieldtype": "Data", "width": 200, "align":"Left"},
        {"fieldname": "id", "label": _("<b>Link</b>"), "fieldtype": "Link", "options":"Stock Transfer", "width": 100}
        
    ]

def get_data(filters):
    data = []
    filter_conditions = get_filters(filters)
    stock_transfer = frappe.get_list("Stock Transfer", filters=filter_conditions, fields=["name", "date"],order_by="date desc")
    
    for stock in stock_transfer:
        entry = frappe.get_doc("Stock Transfer", stock.name)
        for row in entry.items:
            if filters.get("item") and filters.get("item") != row.item:
                continue
            if filters.get("vehicle") and filters.get("vehicle") != row.vehicle:
                continue
            if filters.get("vehicle_type") and filters.get("vehicle_type") != row.vehicle_type:
                continue
            data.append({
                "date": entry.date,
                "item_name": row.item,
                "qty": row.quantity,
                "from_warehouse": row.from_warehouse,
                "to_warehouse": row.to_warehouse,
                "vehicle_type":row.vehicle_type,
                "vehicle": row.vehicle,
                "trip": row.trip_cycle,
                "transporter_name":row.transporter_name,
                "remarks": entry.remarks,
                "id": entry.name
            })
    return data

def get_filters(filters):
    filter_conditions = {"docstatus":1}

    # if filters.get("vehicle"):
    #     filter_conditions["vehicle"] = filters.get("vehicle")
    
    # if filters.get("item"):
    #     filter_conditions["item"] = filters.get("item")
        
    if filters.get("period"):
        start_date, end_date = calculate_date_range(filters["period"])
        filter_conditions["date"] = ["between", [start_date, end_date]]
    elif filters.get("from_date") and filters.get("to_date"):
        filter_conditions["date"] = ["between", [filters.get("from_date"), filters.get("to_date")]]
    elif filters.get("from_date"):
        filter_conditions["date"] = [">=", filters.get("from_date")]
    elif filters.get("to_date"):
        filter_conditions["date"] = ["<=", filters.get("to_date")]

    return filter_conditions

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