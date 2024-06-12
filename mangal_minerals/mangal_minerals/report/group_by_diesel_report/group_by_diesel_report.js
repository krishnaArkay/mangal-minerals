// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.query_reports["Group by Diesel Report"] = {
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
            "fieldname": "vehicle",
            "label": __("Vehicle"),
            "fieldtype": "Link",
            "options":"Mangal Vehicle",
            "reqd": 0
        },
        {
            "fieldname": "vehicle_type",
            "label": __("Vehicle Type"),
            "fieldtype": "Link",
            "options":"Vehicle Type",
            "reqd": 0
        },
	]
	
};
