# Copyright (c) 2024, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import create_stock_entry_manufacture, cancel_stock_entry

class ManufactureProcess(Document):
    
    def on_submit(self):
        stock_entry_type = "Manufacture"
        date = self.date
        target_warehouse = self.warehouse
        jb_qty = 0
        jb_kg = 0
        jb_mt = 0
        per_kg_jb = self.per_jumbo_bag_kg

        if self.jumbo_bag_items:
            j_b_flag = True
        else:
            j_b_flag = False
        # Fetch items from Material Input and Material Output child tables
        input_items = [(row.item, row.quantity) for row in self.material_input]
        output_items = [(row.item, row.quantity,row.is_finished_good) for row in self.material_output]
        jb_items = [(row.item, row.quantity) for row in self.jumbo_bag_items]
        # Create stock entry
        stock_entry_name = create_stock_entry_manufacture(date, input_items, output_items, jb_items, target_warehouse, stock_entry_type, j_b_flag, per_kg_jb)
        self.voucher_number = stock_entry_name
        self.save()
        # frappe.msgprint(f"Stock Entry {stock_entry_name} created successfully.")

        # for row in self.material_output:
        # if hasattr(row, 'is_finished_good') and row.is_finished_good:
        #     qty_kg = row.quantity * 1000

        # Create Jumbo Bag Management entry if jumbo bag items exist
        if self.jumbo_bag_items:
            bag_items = [(row.item, row.quantity) for row in self.jumbo_bag_items]
            items = []
            for row in self.jumbo_bag_items:
                jb_kg = row.quantity * per_kg_jb  # Calculate kg for each bag
                jb_mt = jb_kg / 1000
                row.qty_mt = jb_mt
                frappe.msgprint(f"jb_mt: {jb_mt}")
                items.append({
                    "item": row.item,
                    "quantity": row.quantity,
                    "qty_mt": jb_mt
                })
            # for item, qty in bag_items:
                # jb_kg = qty * per_kg_jb  # Calculate kg for each bag
                # jb_mt = jb_kg / 1000
                # frappe.msgprint(f"jb_mt{jb_mt}")
                # items = [{
                #     "item": item,
                #     "quantity": qty,
                #     "qty_mt": jb_mt
                # } for item, qty in bag_items]
            
            doc = frappe.get_doc({
                "doctype": "Jumbo Bag Management",
                "entry_purpose": "Filled",
                "warehouse": self.warehouse,
                "date": self.date,
                "reference_doctype":"Manufacture Process",
                "reference_number": self.name,
                "remarks": f"This Bag was filled during the manufacturing process - {self.name}",
                "items": items
            })
            doc.save()
            doc.submit()
            self.jumbo_bag = doc.name
            self.save()
    
    def on_cancel(self):
        stock_entry_name = self.voucher_number
        if stock_entry_name:
            cancel_stock_entry(stock_entry_name)
            # frappe.msgprint(f"Stock Entry {stock_entry_name} canceled successfully.")








