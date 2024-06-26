# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data
def get_columns():
    return [
        {"fieldname": "open_order", "label": "<b>" + _("Open Order") + "</b>", "fieldtype": "Link", "options": "Blanket Order", "width": 190},
        {"fieldname": "customer", "label": "<b>" + _("Customer Name") + "</b>", "fieldtype": "Link", "options": "Customer", "width": 250},
        {"fieldname": "date", "label": "<b>" + _("Planned Date") + "</b>", "fieldtype": "Date", "width": 150},
        {"fieldname": "p_truck", "label": "<b>" + _("Planned Truck") + "</b>", "fieldtype": "Data", "width": 120},
        {"fieldname": "a_truck", "label": "<b>" + _("Actual Truck") + "</b>", "fieldtype": "Data", "width": 120},
        {"fieldname": "p_qty", "label": "<b>" + _("Planned MT") + "</b>", "fieldtype": "Float", "width": 140},
        {"fieldname": "a_qty", "label": "<b>" + _("Delivered MT") + "</b>", "fieldtype": "Float", "width": 130},
        {"fieldname": "difference", "label": "<b>" + _("Difference") + "</b>", "fieldtype": "Float", "width": 120},
        {"fieldname": "remaining_mt", "label": "<b>" + _("Remaining MT") + "</b>", "fieldtype": "Float", "width": 130},
        {"fieldname": "id", "label": "<b>" + _("Scheduler Link") + "</b>", "fieldtype": "Link", "options": "Open Order Scheduler", "width": 190},
    ]
def get_data(filters):
    data = []
    scheduler_filters = {"docstatus": 1}
    if filters.get('customer'):
        scheduler_filters["customer"] = filters["customer"]
    if filters.get('open_order'):
        scheduler_filters["open_order"] = filters["open_order"]
    
    schedule_orders = frappe.get_list(
        "Open Order Scheduler",
        fields=["name", "open_order", "customer", "date"],
        filters=scheduler_filters,
        order_by="modified desc"
    )

    for order in schedule_orders:
        order_doc = frappe.get_doc("Open Order Scheduler", order.name)
        for item in order_doc.items:
            item_date = getdate(item.date)
            include_item = True
            if filters.get("period"):
                start_date, end_date = calculate_date_range(filters["period"])
                s_date = getdate(start_date)
                e_date = getdate(end_date)
                if not (s_date <= item_date <= e_date):
                    include_item = False
                    # continue

            elif filters.get('from_date'):
                from_date = getdate(filters.get('from_date'))
                if item_date < from_date:
                    include_item = False
                    # continue
            
            elif filters.get('to_date'):
                to_date = getdate(filters.get('to_date'))
                if item_date > to_date:
                    include_item = False
                    # continue
            
            elif filters.get('from_date') and filters.get('to_date'):
                if not (from_date <= item_date <= to_date):
                    include_item = False
                    # continue
            if include_item:
                data.append({
                    "open_order": order_doc.open_order,
                    "customer": order_doc.customer,
                    "date": item.date,
                    "p_truck":item.planned_truck,
                    "a_truck": item.actual_truck,
                    "p_qty": item.planned_mt,
                    "a_qty": item.delivered_mt,
                    "difference": item.difference,
                    "remaining_mt": (item.planned_mt-item.delivered_mt),
                    "id":order_doc.name
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


