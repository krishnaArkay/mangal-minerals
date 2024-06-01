# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import create_stock_transfer_entry, cancel_stock_entry



class StoreManagement(Document):
	def on_submit(self):
		if self.entry_type == "Stock In":
			stock_entry_type = "Material Receipt" 
			items = []
			for row in self.items:
				item = {
					"item_code": row.item,
					"qty": row.quantity,
					"t_warehouse": self.warehouse
				}
				items.append(item)
			stock_entry_name = create_stock_transfer_entry(items, stock_entry_type)
			self.voucher_number = stock_entry_name
			self.save()
			frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")
		else:
			purposes = {}
			for row in self.items:
				if row.purpose not in purposes:
					# Filter items with the same purpose
					items_with_purpose = [r for r in self.items if r.purpose == row.purpose]
					# Create a stock entry for items with the same purpose
					stock_entry_type = row.purpose
					stock_entry_items = [{
						"item_code": item.item,
						"qty": item.quantity,
						"s_warehouse": self.warehouse,  # Assuming "Stores" is the source warehouse
						# "t_warehouse": self.warehouse
					} for item in items_with_purpose]
					stock_entry_name = create_stock_transfer_entry(stock_entry_items, stock_entry_type)
					purposes[row.purpose] = stock_entry_name  # Track the created stock entry
					frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully for purpose {row.purpose}.")
