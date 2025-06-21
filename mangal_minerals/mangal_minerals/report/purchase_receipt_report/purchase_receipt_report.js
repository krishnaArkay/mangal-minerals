// // Copyright (c) 2024, Arkay Apps and contributors
// // For license information, please see license.txt
// frappe.query_reports["Purchase Receipt Report"] = {
//  "filters": [
//         {
//             "fieldname": "period",
//             "label": __("Period"),
//             "fieldtype": "Select",
//             "options": [
//                 "Daily",
//                 "Monthly"
//             ],
//             "default": "Daily",
//         },
//         {
//             "fieldname": "from_date",
//             "label": __("From Date"),
//             "fieldtype": "Date",
//         },
//         {
//             "fieldname": "to_date",
//             "label": __("To Date"),
//             "fieldtype": "Date",
//         },
//     ]
// };
frappe.query_reports["Purchase Receipt Report"] = {
    "filters": [
        {
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Select",
            "options": ["","Daily", "Monthly"],
            "default": "Daily",
            "on_change": function (query_report) {
                const period = frappe.query_report.get_filter_value("period");
                const today = frappe.datetime.get_today();
                if (period === "Daily") {
                    query_report.set_filter_value("from_date", today);
                    query_report.set_filter_value("to_date", today);
                } else if (period === "Monthly") {
                    const start = frappe.datetime.month_start(today);
                    const end = frappe.datetime.month_end(today);
                    query_report.set_filter_value("from_date", start);
                    query_report.set_filter_value("to_date", end);
                }
            }
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "supplier",
            "label": __("Supplier"),
            "fieldtype": "Link",
            "options": "Supplier"
        }
    ]
};