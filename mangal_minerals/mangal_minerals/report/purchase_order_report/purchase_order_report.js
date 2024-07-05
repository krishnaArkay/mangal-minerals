// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.query_reports["Purchase Order Report"] = {
	"filters": [
        {
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Select",
            "options": "\nToday\nWeekly\nMonthly\nQuarterly\nYearly",
            "width": "100px",
            "default": "Weekly"
        },
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "width": "80px"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            // "default": frappe.datetime.get_today(),
            "width": "80px"
        },
        // {
        //     "fieldname": "name",
        //     "label": __("Name"),
        //     "fieldtype": "Link",
        //     "options": "Purchase Order",
        //     "width": "150px"
        // },
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier",
            "width": "150px"
        },
        {
            "fieldname": "custom_royalty_type",
            "label": __("Royalty Type"),
            "fieldtype": "Select",
            "options": "\nWith Royalty\nWithout Royalty\nExtra charge for Royalty",
            "width": "120px"
        },
        {
            "fieldname": "custom_transporter_type",
            "label": __("Transporter Type"),
            "fieldtype": "Select",
            "options": "\nThird-party Transporter\nSame Party Transporter\nIn-house Transport",
            "width": "120px"
        },
        // {
        //     "fieldname": "item",
        //     "label": __("Item"),
        //     "fieldtype": "Link",
        //     "options": "Item",
        //     "width": "150px"
        // },
        
	]
};
