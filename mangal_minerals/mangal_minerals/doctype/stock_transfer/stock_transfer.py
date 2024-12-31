# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import create_stock_transfer_entry, cancel_stock_entry


class StockTransfer(Document):
	def on_submit(self):
		stock_entry_type = "Material Transfer"
		items = []
		date = self.date
		for row in self.items:
			item = {
				"item_code": row.item,
				"qty": row.quantity,
				"s_warehouse": row.from_warehouse,
				"t_warehouse": row.to_warehouse
			}
			items.append(item)
		stock_entry_name = create_stock_transfer_entry(items,stock_entry_type, date)
		self.voucher_number = stock_entry_name
		self.save()
		# frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")
	
	def on_cancel(self):
		stock_entry_name = self.voucher_number
		if stock_entry_name:
			# if frappe.db.exists("Stock Entry", stock_entry_name):
			cancel_stock_entry(stock_entry_name)
			