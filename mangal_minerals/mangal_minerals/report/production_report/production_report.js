// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.query_reports["Production Report"] = {
	"filters": [
		{
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Select",
            "options": [
                "Daily",
                "Monthly"
            ],
            "default": "Daily",
        }
	]
};
