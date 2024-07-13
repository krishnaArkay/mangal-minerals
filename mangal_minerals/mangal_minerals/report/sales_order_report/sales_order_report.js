// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

// frappe.query_reports["Sales Order Report"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Sales Order Report"] = {
    "filters": [
        {
            "fieldname": "customer_name",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "default": ""
        },
        {
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Select",
            "options": "\nToday\nYesterday\nTomorrow\nWeek\nMonth\nQuarterly\nHalf-yearly\nYearly",
            "default": "Today"
        }
    ],
};
