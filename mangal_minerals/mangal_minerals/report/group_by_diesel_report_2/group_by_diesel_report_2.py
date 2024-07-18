import frappe
from frappe import _
from datetime import datetime, timedelta

def execute(filters=None):
    # Define the columns of the report
    columns = [
        {"fieldname": "date", "label": "<b>" + _("Date") + "</b>", "fieldtype": "Date", "width": 120},
        {"fieldname": "vehicle_type", "label": "<b>" + _("Vehicle Type") + "</b>", "fieldtype": "Data", "width": 150},
        {"fieldname": "vehicle", "label": "<b>" + _("Vehicle") + "</b>", "fieldtype": "Data", "width": 150},
        {"fieldname": "qty", "label": "<b>" + _("Liter") + "</b>", "fieldtype": "Float", "width": 100},
        {"fieldname": "reading", "label": "<b>" + _("HRS/KM") + "</b>", "fieldtype": "Float", "width": 100},
        {"fieldname": "diff", "label": "<b>" + _("Difference") + "</b>", "fieldtype": "Float", "width": 100},
        {"fieldname": "avg", "label": "<b>" + _("Average") + "</b>", "fieldtype": "Float", "width": 100},
        {"fieldname": "remarks", "label": "<b>" + _("Remarks") + "</b>", "fieldtype": "Data", "width": 350}
    ]

    data = []
    entry_purpose_text = ""
    previous_reading = None  # To keep track of the previous row's reading

    filters = get_filters(filters)

    stock_outs = frappe.get_all("Store Management", filters=filters, fields=["name", "date", "entry_type", "remarks"], order_by="date asc")

    for stock_out in stock_outs:
        entry = frappe.get_doc("Store Management", stock_out.name)

        for item in entry.items:
            if item.item == "Diesel":
                qty = item.quantity or 0.0
                reading = item.reading or 0.0
                

                entry_purpose_text = f'<span style="color: #f02d3a;font-weight:bold">{entry.remarks or ""}</span>'
                
                difference = (reading - previous_reading) if previous_reading is not None else 0.0
                previous_reading = reading
                avg = qty / difference if difference != 0 else 0.0
                data.append({
                    "date": entry.date,
                    "vehicle_type": item.vehicle_type,
                    "vehicle": item.vehicle,
                    "qty": qty,
                    "reading": reading,
                    "diff": difference,
                    "avg": avg,
                    "remarks": entry_purpose_text
                })

    return columns, data

def get_filters(filters):
    stock_filters = {"entry_type": "stock out", "docstatus": 1}
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
