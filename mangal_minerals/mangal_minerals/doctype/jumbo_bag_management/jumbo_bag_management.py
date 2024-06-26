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

        if self.entry_purpose == JumboBagEntryPurpose.DELIVERED.value or self.entry_purpose == JumboBagEntryPurpose.DAMAGE.value or self.entry_purpose == JumboBagEntryPurpose.FILLED.value:
            entry_purpose=JumboBagEntryPurpose.DELIVERED.value
        else:
            entry_purpose = None
        if entry_purpose:
            if self.entry_purpose == JumboBagEntryPurpose.DELIVERED.value and self.reference_number: 
                warehouse = self.warehouse
            else:
                warehouse = JumboBagWarehouse.INWARD.value
            mangal_bag_item = frappe.get_value("Item", {"custom_mangals_bag": 1}, "name")
            mangal_warehouse = JumboBagWarehouse.INWARD.value
            if any(item.mangals_bag == 0 for item in self.items):
                deduct_stock(self.name, warehouse, mangal_bag_item,entry_purpose,mangal_warehouse)

        
        # jumbo_bag_type = self.entry_purpose
        # warehouse = self.warehouse
        # for row in self.items:
        #     item_code = row.item
        #     qty = row.quantity
        #     frappe.msgprint(f"avyu: {qty}")
        # item = frappe.get_doc("Item", item_code)
        # stock_detail = None

        # for detail in item.custom_stock:
        #     if detail.warehouse == warehouse:
        #         stock_detail = detail
        #         break

        # if not stock_detail:
        #     stock_detail = item.append('custom_stock', {})
        #     stock_detail.warehouse = warehouse

        # # Ensure initial values are set
        # if stock_detail.total_quantity is None:
        #     stock_detail.total_quantity = 0
        # if stock_detail.filled_qty is None:
        #     stock_detail.filled_qty = 0
        # if stock_detail.damage_qty is None:
        #     stock_detail.damage_qty = 0
        # if stock_detail.delivered_qty is None:
        #     stock_detail.delivered_qty = 0

        # if jumbo_bag_type == "Inward":
        #     stock_detail.total_quantity += qty
        # elif jumbo_bag_type == "Filled":
        #     stock_detail.filled_qty += qty
        #     stock_detail.total_quantity -= qty
        # elif jumbo_bag_type == "Damage":
        #     stock_detail.damage_qty += qty
        #     stock_detail.total_quantity -= qty
        # elif jumbo_bag_type == "Delivered":
        #     stock_detail.delivered_qty += qty
        #     stock_detail.total_quantity -= qty

        # item.save()
        # frappe.db.commit()

    
    def on_cancel(self):
            stock_entry_name = self.voucher_number
            if stock_entry_name:
                cancel_stock_entry(stock_entry_name)