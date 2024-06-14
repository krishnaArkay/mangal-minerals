# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import create_stock_transfer_entry, cancel_stock_entry,deduct_stock
from mangal_minerals.mangal_minerals.enums.enums import JumboBagEntryPurpose,JumboBagWarehouse

class JumboBagManagement(Document):
	def on_submit(self):
		stock_entry_type = ""
		items = []

		if self.entry_purpose == JumboBagEntryPurpose.INWARD.value:
			entry_purpose=JumboBagEntryPurpose.INWARD.value
			warehouse = self.warehouse
			mangal_warehouse = self.warehouse
			mangal_bag_item = frappe.get_value("Item", {"custom_mangals_bag": 1}, "name")
			if any(item.mangals_bag == 0 for item in self.items):
				deduct_stock(self.name, warehouse, mangal_bag_item,entry_purpose,mangal_warehouse)

		if self.entry_purpose == JumboBagEntryPurpose.INWARD.value and not self.reference_number:
			stock_entry_type = "Material Receipt"
			for row in self.items:
				item = {
					"item_code": row.item,
					"qty": row.quantity,
					"t_warehouse": self.warehouse
				}
				items.append(item)
		elif self.entry_purpose in [JumboBagEntryPurpose.DAMAGE.value, JumboBagEntryPurpose.DELIVERED.value] and not self.reference_number:
			if self.entry_purpose == JumboBagEntryPurpose.DAMAGE.value:
				stock_entry_type = "Jumbo Bag Damage"
				for row in self.items:
					item = {
						"item_code": row.item,
						"qty": row.quantity,
						"s_warehouse": JumboBagWarehouse.INWARD.value,
						"t_warehouse":self.warehouse
					}
					items.append(item)
			elif self.entry_purpose == JumboBagEntryPurpose.DELIVERED.value:
				stock_entry_type = "Jumbo Bag Delivered"
				for row in self.items:
					item = {
						"item_code": row.item,
						"qty": row.quantity,
						"s_warehouse": self.warehouse
					}
					items.append(item)
		elif self.entry_purpose == JumboBagEntryPurpose.FILLED.value:
			stock_entry_type = "Jumbo Bag Filled"
			for row in self.items:
				item = {
					"item_code": row.item,
					"qty": row.quantity,
					"s_warehouse": JumboBagWarehouse.INWARD.value,
					"t_warehouse":self.warehouse
				}
				items.append(item)
		else:
			pass

		if items:
			stock_entry_name = create_stock_transfer_entry(items, stock_entry_type)
			self.voucher_number = stock_entry_name
			self.save()
			# frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")

		if self.entry_purpose == JumboBagEntryPurpose.DELIVERED.value or self.entry_purpose == JumboBagEntryPurpose.DAMAGE.value or self.entry_purpose == JumboBagEntryPurpose.FILLED.value:
			entry_purpose=JumboBagEntryPurpose.DELIVERED.value
		# elif self.entry_purpose == JumboBagEntryPurpose.DAMAGE.value:
		# 	entry_purpose=JumboBagEntryPurpose.DAMAGE.value
		# elif self.entry_purpose == JumboBagEntryPurpose.FILLED.value:
		# 	entry_purpose=JumboBagEntryPurpose.FILLED.value
		# else:
		# 	pass

			warehouse = self.warehouse  
			mangal_bag_item = frappe.get_value("Item", {"custom_mangals_bag": 1}, "name")
			# mangal_warehouse = frappe.db.sql("""
			# 				SELECT warehouse 
			# 				FROM `tabBin` 
			# 				WHERE item_code = %s AND actual_qty > 0 
			# 				LIMIT 1
			# 			""", mangal_bag_item, as_dict=True)
			mangal_warehouse = JumboBagWarehouse.INWARD.value
			# if mangal_warehouse:
			# 	mangal_warehouse = mangal_warehouse[0]["warehouse"]
			# 	frappe.msgprint(mangal_warehouse)
			if any(item.mangals_bag == 0 for item in self.items):
				deduct_stock(self.name, warehouse, mangal_bag_item,entry_purpose,mangal_warehouse)
	
	def on_cancel(self):
			stock_entry_name = self.voucher_number
			if stock_entry_name:
				cancel_stock_entry(stock_entry_name)