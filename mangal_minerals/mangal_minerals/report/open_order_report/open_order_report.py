# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "open_order", "label": "<b>" + _("Open Order") + "</b>", "fieldtype": "Link", "options": "Blanket Order", "width": 200},
        {"fieldname": "customer", "label": "<b>" + _("Customer Name") + "</b>", "fieldtype": "Link", "options": "Customer", "width": 250},
        {"fieldname": "item_code", "label": "<b>" + _("Item") + "</b>", "fieldtype": "Link", "options": "Item", "width": 150},
        {"fieldname": "quantity", "label": "<b>" + _("Quantity") + "</b>", "fieldtype": "Data", "width": 100},
        {"fieldname": "from_date", "label": "<b>" + _("Order From Date") + "</b>", "fieldtype": "Date", "width": 140},
        {"fieldname": "to_date", "label": "<b>" + _("Order To Date") + "</b>", "fieldtype": "Date", "width": 130},
        {"fieldname": "delivered_mt", "label": "<b>" + _("Delivered MT") + "</b>", "fieldtype": "Float", "width": 120},
        {"fieldname": "remaining_mt", "label": "<b>" + _("Remaining MT") + "</b>", "fieldtype": "Float", "width": 130},
    ]

def get_data(filters):
    data = []

    blanket_order_filters = {"docstatus": 1}

    if filters.get('customer'):
        blanket_order_filters["customer_name"] = filters["customer"]
    if filters.get("period"):
        start_date, end_date = calculate_date_range(filters["period"])
        blanket_order_filters["from_date"] = ["between", [start_date, end_date]]
    elif filters.get('from_date') and filters.get('to_date'):
        blanket_order_filters["from_date"] = ["between", [filters["from_date"], filters["to_date"]]]

    blanket_orders = frappe.get_list(
        "Blanket Order",
        fields=["name", "customer_name", "from_date", "to_date"],
        filters=blanket_order_filters,
        order_by="from_date ASC"
    )

    for blanket_order in blanket_orders:
        blanket = frappe.get_doc("Blanket Order", blanket_order.name)
        for row in blanket.items:
            item_code = row.item_code
            quantity = row.qty

            if filters.get("item") and item_code != filters["item"]:
                continue  # Skip this item if it does not match the filter

            open_orders = frappe.get_list(
                "Open Order Scheduler",
                fields=["name", "date", "total_delivered_mt", "total_remaining_mt"],
                filters={"docstatus": 1, "open_order": blanket_order.name},
                order_by="date ASC"
            )

            total_delivered_mt = sum(order['total_delivered_mt'] for order in open_orders)
            total_remaining_mt = sum(order['total_remaining_mt'] for order in open_orders)

            data.append({
                "open_order": blanket.name,
                "customer": blanket.customer_name,
                "item_code": item_code,
                "quantity": quantity,
                "from_date": blanket.from_date,
                "to_date": blanket.to_date,
                "delivered_mt": total_delivered_mt,
                "remaining_mt": total_remaining_mt,
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

