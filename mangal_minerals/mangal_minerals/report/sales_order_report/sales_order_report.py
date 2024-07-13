# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _
from frappe.utils import getdate, add_days, add_months, add_years
from datetime import timedelta
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()  # Define the columns
    data = get_data(filters)  # Get data based on filters
    return columns, data

def get_columns():
    return [
        {"fieldname": "ID", "label": _("ID"), "fieldtype": "Link", "options": "Sales Order", "width": 150},
        {"fieldname": "customer", "label": _("Customer"), "fieldtype": "Link", "options": "Customer", "width": 200},
        {"fieldname": "date", "label": _("Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "item_name", "label": _("Item Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "qty", "label": _("Quantity"), "fieldtype": "Float", "width": 100},
        {"fieldname": "amount", "label": _("Amount"), "fieldtype": "Currency", "width": 140},
        {"fieldname": "delivery_date", "label": _("Delivery Date"), "fieldtype": "Date", "width": 100},
        {"fieldname": "delivery_status", "label": _("Delivery Status"), "fieldtype": "Data", "width": 130},
        {"fieldname": "delivered", "label": _("% Delivered"), "fieldtype": "Percent", "width": 100}
    ]


@frappe.whitelist()
def get_data(filters):
    data = []
    default_filters = {"docstatus": ["!=", 2]}

    if filters.get("customer_name"):
        default_filters["customer_name"] = filters["customer_name"]

    period = filters.get("period")
    today = getdate()

    if period == "Today":
        default_filters["transaction_date"] = ["=", today]
    elif period == "Yesterday":
        default_filters["transaction_date"] = ["=", today - timedelta(days=1)]
    elif period == "Tomorrow":
        default_filters["transaction_date"] = ["=", today + timedelta(days=1)]
    elif period == "Week":
        default_filters["transaction_date"] = [">=", today - timedelta(days=7)]
    elif period == "Month":
        default_filters["transaction_date"] = [">=", today - timedelta(days=30)]
    elif period == "Quarterly":
        default_filters["transaction_date"] = [">=", today - timedelta(days=90)]
    elif period == "Half-yearly":
        default_filters["transaction_date"] = [">=", today - timedelta(days=180)]
    elif period == "Yearly":
        default_filters["transaction_date"] = [">=", today - timedelta(days=365)]

    sales_orders = frappe.get_list("Sales Order", filters=default_filters, fields=["name", "transaction_date"],order_by="transaction_date desc")

    for salese_order in sales_orders:
        so = frappe.get_doc("Sales Order", salese_order.name)

        for item in so.items:
            item_name = item.item_name
            qty = item.qty
            amount = item.amount
            data.append({
                "ID": so.name,
                "customer": so.customer_name,
                "date": so.transaction_date,
                "delivery_date": so.delivery_date,
                "delivery_status": so.delivery_status,
                "item_name": item_name,
                "qty": qty,
                "amount": amount,
                "delivered": so.per_delivered
            })
        
    return data