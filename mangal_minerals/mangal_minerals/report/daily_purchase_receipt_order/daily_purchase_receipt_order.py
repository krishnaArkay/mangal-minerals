# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data
# my_custom_app/reports/daily_purchase_receipt_report/daily_purchase_receipt_report.py
import frappe
from frappe.utils import add_days, today

def execute(filters=None):
    columns = [
        {"fieldname": "party_name", "label": "Party Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "item_name", "label": "Item", "fieldtype": "Data", "width": 150},
        {"fieldname": "qty", "label": "Quantity", "fieldtype": "Float", "width": 100},
        {"fieldname": "royalty", "label": "Royalty", "fieldtype": "Data", "width": 100},
    ]
    
    data = frappe.db.sql("""
		SELECT 
			pr.supplier AS party_name, 
			pri.item_name AS item_name, 
			SUM(pri.qty) AS qty,
			COALESCE(NULLIF(pr.custom_royalty_type, ''), ' ') AS royalty
		FROM 
			`tabPurchase Receipt` pr
		JOIN 
			`tabPurchase Receipt Item` pri ON pr.name = pri.parent
		WHERE 
			pr.docstatus = 0 AND pr.posting_date = %s
		GROUP BY 
			pr.supplier, pri.item_name, royalty
		ORDER BY 
			pr.supplier, royalty, pri.item_name
	""", (add_days(today(), -1)), as_dict=1)


    
    return columns, data
