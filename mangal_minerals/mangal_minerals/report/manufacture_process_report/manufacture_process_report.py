# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta

# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"fieldname": "date", "label": _("<b>Date</b>"), "fieldtype": "Data", "width": 120},
        {"fieldname": "process_name", "label": _("<b>Process Name</b>"), "fieldtype": "Data", "width": 200},
        {"fieldname": "warehouse", "label": _("<b>Warehouse</b>"), "fieldtype": "Data", "width": 230},
        {"fieldname": "material_input_item", "label": _("<b>MI Item</b>"), "fieldtype": "Data", "width": 150},
        {"fieldname": "material_input_qty", "label": _("<b>MI Qty</b>"), "fieldtype": "Data", "width": 100},
        {"fieldname": "material_output_item", "label": _("<b>MO Item</b>"), "fieldtype": "Data", "width": 150},
        {"fieldname": "material_output_qty", "label": _("<b>MO Qty</b>"), "fieldtype": "Data", "width": 100},
        {"fieldname": "loose_mt", "label": _("<b>Loose MT</b>"), "fieldtype": "Data", "width": 100},
        {"fieldname": "filled_mt", "label": _("<b>Filled MT</b>"), "fieldtype": "Data", "width": 100},
        {"fieldname": "jumbo_bag_item", "label": _("<b>JB Item</b>"), "fieldtype": "Data", "width": 150},
        {"fieldname": "jumbo_bag_qty", "label": _("<b>JB Qty</b>"), "fieldtype": "Data", "width": 100},
        # {"fieldname": "id", "label": _("<b>id</b>"), "fieldtype": "Link", "options":"Manufacture Process", "width": 100}
        
    ]
def get_data(filters):
    data = []
    filter_conditions = get_filters(filters)
    manufacture_processes = frappe.get_all("Manufacture Process", filters=filter_conditions, fields=["name", "date", "process_name", "warehouse"],order_by="modified desc")

    for process in manufacture_processes:
        entry = frappe.get_doc("Manufacture Process", process.name)
        material_inputs = entry.material_input or [{}]
        material_outputs = entry.material_output or [{}]
        jumbo_bags = entry.jumbo_bag_items or [{}]

        max_length = max(len(material_inputs), len(material_outputs), len(jumbo_bags))
        for i in range(max_length):
            material_input = material_inputs[i] if i < len(material_inputs) else {}
            material_output = material_outputs[i] if i < len(material_outputs) else {}
            jumbo_bag = jumbo_bags[i] if i < len(jumbo_bags) else {}
            data.append({
                "date": entry.date.strftime("%d-%m-%Y") if i == 0 else f'<span style="color:white">{entry.date.strftime("%d-%m-%Y")}</span>',
                "process_name": entry.process_name if i == 0 else f'<span style="color:white">{entry.process_name}</span>',
                "warehouse": entry.warehouse if i == 0 else f'<span style="color:white">{entry.warehouse}</span>',
                "material_input_item": f'<span style="color:#fb6107;font-weight:bold">{material_input.get("item", "")}</span>',
                "material_input_qty": f'<span style="color:#fb6107;font-weight:bold">{material_input.get("quantity", "")}</span>',
                "material_output_item":f'<span style="color:#007200;font-weight:bold">{material_output.get("item", "")}</span>' ,
                "material_output_qty": f'<span style="color:#007200;font-weight:bold">{material_output.get("quantity", 0):.2f}</span>' ,
                "filled_mt": f'<span style="color:#E76F51;font-weight:bold">{jumbo_bag.get("qty_mt", "")}</span>',
                "loose_mt": f'<span style="color:#E76F51;font-weight:bold">{material_output.get("quantity", 0) - jumbo_bag.get("qty_mt", 0):.2f}</span>',
                "jumbo_bag_item": f'<span style="color:#124076;font-weight:bold">{jumbo_bag.get("item", "")}</span>',
                "jumbo_bag_qty":f'<span style="color:#124076;font-weight:bold">{jumbo_bag.get("quantity", "")}</span>',
                # "id": entry.name if i == 0 else f'<span style="color:white">{entry.name}</span>'
            })


    return data
def get_filters(filters):
    filter_conditions = {"docstatus":1}

    if filters.get("warehouse"):
        filter_conditions["warehouse"] = filters.get("warehouse")
    
    if filters.get("process"):
        filter_conditions["process_name"] = filters.get("process")
        
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