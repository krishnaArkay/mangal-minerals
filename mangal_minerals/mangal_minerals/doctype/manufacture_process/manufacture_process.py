# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import create_stock_entry_manufacture, cancel_stock_entry
# from mangal_minerals.mangal_minerals.doctype.api import cancel_stock_entry


class ManufactureProcess(Document):
	
	def on_submit(self):
		stock_entry_type = "Manufacture"
		target_warehouse = self.warehouse
		
		# Fetch items from Material Input and Material Output child tables
		input_items = [(row.item, row.quantity) for row in self.material_input]
		output_items = [(row.item, row.quantity,row.is_finished_good) for row in self.material_output]
		
		# Create stock entry
		stock_entry_name = create_stock_entry_manufacture(input_items, output_items, target_warehouse, stock_entry_type)
		self.voucher_number = stock_entry_name
		self.save()
		frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")

	def on_cancel(self):
		stock_entry_name = self.voucher_number
		if stock_entry_name:
			cancel_stock_entry(stock_entry_name)
			frappe.msgprint(f"Stock Entry {stock_entry_name} canceled successfully.")








