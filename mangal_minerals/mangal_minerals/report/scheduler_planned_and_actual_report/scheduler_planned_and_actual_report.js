// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.query_reports["Scheduler Planned and Actual Report"] = {
	"filters": [
		{
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Select",
            "options": "\nToday\nWeekly\nMonthly\nQuarterly\nYearly",
            "default": "Monthly",
            "reqd": 0
        }, 
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "reqd": 0,
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "reqd": 0
        },
		{
            "fieldname": "open_order",
            "label": __("Open Order"),
            "fieldtype": "Link",
            "options": "Blanket Order",
			"get_query": function() {
					return {
						"filters": [
							["Blanket Order", "docstatus", "=", 1]
						]
					};
				},
            "reqd": 0
        },
	]
};
