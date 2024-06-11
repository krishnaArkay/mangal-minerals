# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "date", "label": "<b>" + _("Date") + "</b>", "fieldtype": "Date", "width": 130},
        {"fieldname": "entry_purpose", "label": "<b>" + _("Entry Purpose") + "</b>", "fieldtype": "Data", "width": 150},
        {"fieldname": "warehouse", "label": "<b>" + _("Warehouse") + "</b>", "fieldtype": "Link", "options": "Warehouse", "width": 300},
        {"fieldname": "item", "label": "<b>" + _("Jumbo Bag Name") + "</b>", "fieldtype": "Link", "options":"Item", "width": 250},
        {"fieldname": "quantity", "label": "<b>" + _("Quantity") + "</b>", "fieldtype": "Data", "width": 100}
    ]

def get_data(filters):
    data = []
    total_quantity = 0
    total_qty= 0
    total = "Total"

    # Define color codes for each entry purpose
    color_codes = {
        "Delivered": "#FFA500",
        "Inward": "green",
        "Filled": "blue",
        "Damage": "red"
    }
    default_filters = {"docstatus":1}

    if filters.get("date") and filters.get("to_date"):
        default_filters["date"] = ["between", [filters["date"], filters["to_date"]]]
    elif filters.get("date"):
        default_filters["date"] = [">=", filters["date"]]
    elif filters.get("to_date"):
        default_filters["date"] = ["<=", filters["to_date"]]

    if filters.get("entry_purpose"):
        default_filters["entry_purpose"] = filters["entry_purpose"]

    if filters.get("warehouse"):
        default_filters["warehouse"] = filters["warehouse"]

    if filters.get("item"):
        default_filters["item"] = filters["item"]

    records = frappe.get_list(
        "Jumbo Bag Management",
        filters=default_filters,  # Filter to fetch only documents with docstatus = 1
        fields=["name", "date", "entry_purpose", "warehouse"],
    )

    # Process the fetched records
    for record in records:
        ji = frappe.get_doc("Jumbo Bag Management",record.name)
        color = color_codes.get(record.entry_purpose, "")
        font_weight = "bold"
        

        for item in ji.items:
             # Get color based on entry purpose
            if filters.get("item"):
                if item.item != filters.get("item"):
                    break

          # Set font-weight to bold

            # Format text with HTML color and font-weight tags
            entry_purpose_text = f'<span style="color: {color}; font-weight: {font_weight};">{record.entry_purpose}</span>'
            quantity_text = f'<span style="color: {color}; font-weight: {font_weight};">{item.quantity}</span>'
        
            data.append({
                "date": record.date,
                "entry_purpose": entry_purpose_text,
                "warehouse": record.warehouse,
                "item": item.item,
                "quantity": quantity_text,
            })
            qty= int(item.quantity)
            total_quantity += qty
    if total_quantity != 0:
        total = f'<span style=" font-weight: {font_weight};">Total</span>'
        total_qty = f'<span style=" font-weight: {font_weight};">{total_quantity}</span>'

    data.append({
            "date": "",
            "entry_purpose": total,
            "warehouse": "",
            "item": "",
            "quantity": total_qty,
        })

    return data
