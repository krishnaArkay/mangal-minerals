# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import create_stock_transfer_entry, cancel_stock_entry

class StoreManagement(Document):
    
    def on_submit(self):
        date = self.date
        bundle_name = ""
        if self.entry_type == "Stock In":
            if self.has_batch_no and self.item and self.batch_count:
            # Create Serial and Batch Bundle
                bundle = frappe.new_doc("Serial and Batch Bundle")
                bundle.voucher_type = "Stock Entry"
                bundle.item_code = self.item
                bundle.warehouse = self.warehouse
                bundle.type_of_transaction = "Inward"
                bundle.has_batch_no = 1
                for row in self.batch_details:
                    if row.batch and row.qty:
                        bundle.append("entries", {
                            "batch_no": row.batch,
                            "qty": row.qty
                        })
                bundle.save()
                bundle_name = bundle.name
            # self.serial_and_batch_bundle = bundle.name  # Optional: Add a link field in Store Management to reference this bundle
            
            stock_entry_type = "Material Receipt" 
            items = []
            
            for row in self.items:
                item = {
                    "item_code": row.item,
                    "qty": row.quantity,
                    "t_warehouse": self.warehouse,
                    "serial_and_batch_bundle": bundle_name
                }
                items.append(item)
            
            stock_entry_name = create_stock_transfer_entry(items,stock_entry_type, date)
            self.voucher_number = stock_entry_name
            self.save()
            # frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")
        else:
            purposes = {}
            if self.has_batch_no and self.item and self.batch_count:
            # Create Serial and Batch Bundle
                bundle = frappe.new_doc("Serial and Batch Bundle")
                bundle.voucher_type = "Stock Entry"
                bundle.item_code = self.item
                bundle.warehouse = self.warehouse
                bundle.type_of_transaction = "Outward"
                bundle.has_batch_no = 1
                for row in self.batch_details:
                    if row.batch and row.qty:
                        bundle.append("entries", {
                            "batch_no": row.batch,
                            "qty": row.qty
                        })
                bundle.save()
                bundle_name = bundle.name
            for row in self.items:
                if row.purpose not in purposes:
                    # Filter items with the same purpose
                    items_with_purpose = [r for r in self.items if r.purpose == row.purpose]
                    # Create a stock entry for items with the same purpose
                    stock_entry_type = row.purpose
                    stock_entry_items = [{
                        "item_code": item.item,
                        "qty": item.quantity,
                        "serial_and_batch_bundle": bundle_name,
                        "s_warehouse": self.warehouse,  # Assuming "Stores" is the source warehouse
                    } for item in items_with_purpose]
                    stock_entry_name = create_stock_transfer_entry(stock_entry_items, stock_entry_type, date)
                    purposes[row.purpose] = stock_entry_name  # Track the created stock entry
                    # frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully for purpose {row.purpose}.")
            for row in self.items:
                row.voucher_number = purposes.get(row.purpose, '')
            self.save()

        # date = self.date
        # if self.entry_type == "Stock In":
        # 	stock_entry_type = "Material Receipt" 
        # 	items = []
            
        # 	for row in self.items:
        # 		item = {
        # 			"item_code": row.item,
        # 			"qty": row.quantity,
        # 			"t_warehouse": self.warehouse
        # 		}
        # 		items.append(item)
        # 	stock_entry_name = create_stock_transfer_entry(items,stock_entry_type, date)
        # 	self.voucher_number = stock_entry_name
        # 	self.save()
        # 	# frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")
        # else:
        # 	purposes = {}
        # 	for row in self.items:
        # 		if row.purpose not in purposes:
        # 			# Filter items with the same purpose
        # 			items_with_purpose = [r for r in self.items if r.purpose == row.purpose]
        # 			# Create a stock entry for items with the same purpose
        # 			stock_entry_type = row.purpose
        # 			stock_entry_items = [{
        # 				"item_code": item.item,
        # 				"qty": item.quantity,
        # 				"s_warehouse": self.warehouse,  # Assuming "Stores" is the source warehouse
        # 			} for item in items_with_purpose]
        # 			stock_entry_name = create_stock_transfer_entry(stock_entry_items, stock_entry_type, date)
        # 			purposes[row.purpose] = stock_entry_name  # Track the created stock entry
        # 			# frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully for purpose {row.purpose}.")

        # 	for row in self.items:
        # 		row.voucher_number = purposes.get(row.purpose, '')

        # 	self.save()				
    
    def on_cancel(self):
        if self.entry_type == "Stock In":
            cancel_stock_entry(self.voucher_number)
        else:
            for row in self.items:
                if row.voucher_number:
                    cancel_stock_entry(row.voucher_number)
