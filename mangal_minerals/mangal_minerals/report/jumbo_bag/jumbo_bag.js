// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.query_reports["Jumbo Bag"] = {
	"filters": [
		{
            "fieldname": "date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 0
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 0,
        },
        {
            "fieldname": "entry_purpose",
            "label": __("Entry Purpose"),
            "fieldtype": "Select",
            "options": ["","Delivered", "Inward", "Filled", "Damage"],
            "reqd": 0
        },
        {
            "fieldname": "warehouse",
            "label": __("Warehouse"),
            "fieldtype": "Link",
            "options": "Warehouse",
            "get_query": function() {
                return {
                    "filters": [
                        ["Warehouse", "is_group", "!=", 1]
                    ]
                };
            },
            "reqd": 0
        },
        {
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item",
            "get_query": function() {
                return {
                    "filters": [
                        ["Item", "item_group", "=", "Jumbo Bag"]
                    ]
                };
            },
            "reqd": 0
        }
    ]
};

