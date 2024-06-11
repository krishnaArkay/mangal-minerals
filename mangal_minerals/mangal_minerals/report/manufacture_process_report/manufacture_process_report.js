// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.query_reports["Manufacture Process Report"] = {
	"filters": [
		{
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Select",
            "options": "\nWeekly\nMonthly\nQuarterly\nYearly",
            "default": "Monthly",
            "reqd": 0
        },        
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.get_today(),
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.get_today(),
            "reqd": 0
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options":"Warehouse",
            "reqd": 0
        },
        {
            "fieldname": "process",
            "label": __("Process"),
            "fieldtype": "Link",
            "options":"Process Type",
            "reqd": 0
        },
	]
};
