# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import create_stock_transfer_entry, cancel_stock_entry,deduct_stock


class JumboBagManagement(Document):
	def on_submit(self):
		stock_entry_type = ""
		items = []

		if self.entry_purpose == "Inward":
			entry_purpose="Inward"
			warehouse = self.warehouse  
			mangal_bag_item = frappe.get_value("Item", {"custom_mangals_bag": 1}, "name")
			frappe.msgprint(mangal_bag_item)
			if any(item.mangals_bag == 0 for item in self.items):
				deduct_stock(self.name, warehouse, mangal_bag_item,entry_purpose)

		if self.entry_purpose == "Inward" and not self.reference_number:
			stock_entry_type = "Material Receipt"
			for row in self.items:
				item = {
					"item_code": row.item,
					"qty": row.quantity,
					"t_warehouse": self.warehouse
				}
				items.append(item)
		elif self.entry_purpose in ["Damage", "Delivered"] and not self.reference_number:
			if self.entry_purpose == "Damage":
				stock_entry_type = "Jumbo Bag Damage"
			elif self.entry_purpose == "Delivered":
				stock_entry_type = "Jumbo Bag Delivered"
				

			for row in self.items:
				item = {
					"item_code": row.item,
					"qty": row.quantity,
					"s_warehouse": self.warehouse
				}
				items.append(item)
		else:
			# Pass if the entry purpose is not "Inward", "Damage", or "Delivered"
			pass

		if items:
			stock_entry_name = create_stock_transfer_entry(items, stock_entry_type)
			self.voucher_number = stock_entry_name
			self.save()
			frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")

			if self.entry_purpose == "Delivered":
				entry_purpose="Delivered"

			warehouse = self.warehouse  
			mangal_bag_item = frappe.get_value("Item", {"custom_mangals_bag": 1}, "name")
			mangal_warehouse = frappe.db.sql("""
							SELECT warehouse 
							FROM `tabBin` 
							WHERE item_code = %s AND actual_qty > 0 
							LIMIT 1
						""", mangal_bag_item, as_dict=True)

			if mangal_warehouse:
				mangal_warehouse = mangal_warehouse[0]["warehouse"]
				frappe.msgprint(mangal_warehouse)
			if any(item.mangals_bag == 0 for item in self.items):
				deduct_stock(self.name, warehouse, mangal_bag_item,entry_purpose,mangal_warehouse)

	
	def on_cancel(self):
		if self.voucher_number:
			cancel_stock_entry(self.voucher_number)