// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.query_reports["Store Management Report"] = {
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
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options":"Item",
			"get_query": function() {
				return {
					"filters": [
						["Item", "item_group", "in", ["Store Item", "Consumable"]]
					]
				};
			},
            "reqd": 0
        },
		{
            "fieldname": "purpose",
            "label": __("Purpose"),
            "fieldtype": "Link",
            "options":"Stock Entry Type",
			"get_query": function() {
				return {
					"filters": [
						["Stock Entry Type", "name", "in", ["Material Consumption", "Issued for Usage","Return", "Material Inward", "Material Outward"]]
					]
				};
			},
            "reqd": 0
        },
	]
};
