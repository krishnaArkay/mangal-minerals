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
        {
            "fieldname": "date",
            "label": _("<b>Date</b>"),
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "purpose",
            "label": _("<b>Purpose</b>"),
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "item_name",
            "label": _("<b>Item Name</b>"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "in_qty",
            "label": _("<b>In Quantity</b>"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "out_qty",
            "label": _("<b>Out Quantity</b>"),
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "fieldname": "balance",
            "label": _("<b>Balance</b>"),
            "fieldtype": "Float",
            "width": 130,
        },
        {
            "fieldname": "used_in",
            "label": _("<b>Used In</b>"),
            "fieldtype": "Data",
            "width": 150,
            "align": "left",
        },
        {
            "fieldname": "item_remarks",
            "label": _("<b>Item Remarks</b>"),
            "fieldtype": "Data",
            "width": 250,
            "align": "left",
        },
        {
            "fieldname": "remarks",
            "label": _("<b>Remarks</b>"),
            "fieldtype": "Data",
            "width": 250,
            "align": "left",
        },
        {
            "fieldname": "per_responsible",
            "label": _("<b>Responsible</b>"),
            "fieldtype": "Data",
            "width": 150,
            "align": "left",
        },
        {
            "fieldname": "id",
            "label": _("<b>Link</b>"),
            "fieldtype": "Link",
            "options": "Store Management",
            "width": 200,
        },
    ]


def get_data(filters):
    data = []
    total_quantity_in = 0
    total_qty_in = 0
    total_quantity_out = 0
    total_qty_out = 0
    total = "Total"
    total_blance = 0
    filter_conditions = get_filters(filters)
    store_management_entries = frappe.get_list(
        "Store Management",
        filters=filter_conditions,
        fields=["name", "date", "entry_type"],
        order_by="date desc",
    )

    for entry in store_management_entries:
        store_management_doc = frappe.get_doc("Store Management", entry.name)
        for item in store_management_doc.items:
            if filters.get("item") and filters.get("item") != item.item:
                continue
            if filters.get("purpose") and filters.get("purpose") != item.purpose:
                continue
            if filters.get("used_in") and filters.get("used_in") != item.used_in:
                continue

            in_qty = item.quantity if entry.entry_type == "Stock In" else 0.0
            out_qty = item.quantity if entry.entry_type == "Stock Out" else 0.0
            if store_management_doc.voucher_number:
                actual_qty = frappe.get_value(
                    "Stock Ledger Entry",
                    filters={
                        "voucher_no": store_management_doc.voucher_number,
                        "item_code": item.item,
                        "warehouse": store_management_doc.warehouse,
                    },
                    fieldname="qty_after_transaction",
                )
            else:
                actual_qty = frappe.get_value(
                    "Stock Ledger Entry",
                    filters={
                        "voucher_no": item.voucher_number,
                        "item_code": item.item,
                        "warehouse": store_management_doc.warehouse,
                    },
                    fieldname="qty_after_transaction",
                )
            # Apply green color if quantity is greater than 0
            in_qty_str = (
                f'<span style="color: #007200;font-weight:bold">{in_qty}</span>'
                if in_qty > 0
                else in_qty
            )
            out_qty_str = (
                f'<span style="color: #fb6107;font-weight:bold">{out_qty}</span>'
                if out_qty > 0
                else out_qty
            )
            purpose = (
                f'<span style="color: #007200;font-weight:bold">{item.purpose}</span>'
                if in_qty > 0
                else f'<span style="color: #fb6107;font-weight:bold">{item.purpose}</span>'
            )

            data.append(
                {
                    "date": store_management_doc.date,
                    "item_name": item.item,
                    "purpose": item.purpose,
                    "in_qty": in_qty_str,
                    "out_qty": out_qty_str,
                    "balance": actual_qty,
                    "per_responsible": item.person_name,
                    "used_in": item.used_in,
                    "item_remarks": item.remarks,
                    "remarks": store_management_doc.remarks,
                    "id": store_management_doc.name,
                }
            )

            qty_in = int(in_qty)
            qty_out = int(out_qty)

            total_quantity_in += qty_in
            total_quantity_out += qty_out
            # total_blance += actual_qty

    if total_quantity_in != 0:
        total = f'<span style=" font-weight: bold;">Total</span>'
        total_qty_in = f'<span style=" font-weight: bold;">{total_quantity_in}</span>'
    if total_quantity_out != 0:
        total = f'<span style=" font-weight: bold;">Total</span>'
        total_qty_out = f'<span style=" font-weight:bold;">{total_quantity_out}</span>'

    data.append(
        {
            "date": "",
            "item_name": total,
            "purpose": "",
            "in_qty": total_qty_in,
            "out_qty": total_qty_out,
            "balance": "",
            "per_responsible": "",
            "item_remarks": "",
            "remarks": "",
            "used_in": "",
            "id": "",
        }
    )

    return data


def get_filters(filters):
    filter_conditions = {"docstatus": 1}

    if filters.get("period"):
        start_date, end_date = calculate_date_range(filters["period"])
        filter_conditions["date"] = ["between", [start_date, end_date]]
    if filters.get("from_date") and filters.get("to_date"):
        filter_conditions["date"] = [
            "between",
            [filters.get("from_date"), filters.get("to_date")],
        ]
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

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
