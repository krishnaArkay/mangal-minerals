# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
    
    # Define columns
    columns = [
    {"label": "<b>Vehicle</b>", "fieldname": "vehicle", "fieldtype": "Data", "width": 150},
    {"label": "<b>Vehicle Type</b>", "fieldname": "vehicle_type", "fieldtype": "Data", "width": 150},
    {"label": "<b>Total Quantity</b>", "fieldname": "total_quantity", "fieldtype": "Float", "width": 150},
    {"label": "<b>Total Trip</b>", "fieldname": "total_trip_cycles", "fieldtype": "Int", "width": 120},
]

    data = []
    filters = get_filters(filters)

    # Get list of Stock Transfer documents
    stock_transfer = frappe.get_list(
        "Stock Transfer",
        filters=filters,
        fields=["name", "date"]
    )
    
    vehicle_data = {}

    for stock in stock_transfer:
        entry = frappe.get_doc("Stock Transfer", stock.name)
        
        for item in entry.items:
            qty = item.quantity or 0.0
            trip = item.trip_cycle or 0.0
            
            if item.vehicle not in vehicle_data:
                vehicle_data[item.vehicle] = {
                        "vehicle_type": item.vehicle_type,
                        "vehicle": item.vehicle,
                        "total_quantity": 0,
                        "total_trip_cycles": 0
                    }

            vehicle_data[item.vehicle]["total_quantity"] += qty
            vehicle_data[item.vehicle]["total_trip_cycles"] += trip
    for vehicle, vehicle_info in vehicle_data.items():
        data.append(vehicle_info)

    return columns, data

def get_filters(filters):
    stock_filters = {"docstatus": 1}
    
    if filters.get("period"):
        start_date, end_date = calculate_date_range(filters["period"])
        stock_filters["date"] = ["between", [start_date, end_date]]
    elif filters.get("from_date") and filters.get("to_date"):
        stock_filters["date"] = ["between", [filters["from_date"], filters["to_date"]]]
    elif filters.get("date"):
        stock_filters["date"] = [">=", filters["from_date"]]
    elif filters.get("to_date"):
        stock_filters["date"] = ["<=", filters["to_date"]]

    if filters.get("vehicle"):
        stock_filters["vehicle"] = filters["vehicle"]

    if filters.get("vehicle_type"):
        stock_filters["vehicle_type"] = filters["vehicle_type"]

    return stock_filters

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