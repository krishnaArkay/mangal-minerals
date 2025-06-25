# Copyright (c) 2025, Arkay Apps and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt
from frappe.model.document import Document
from mangal_minerals.mangal_minerals.doctype.api import cancel_stock_reconciliation, create_stock_reconcilliation_entry, create_stock_transfer_entry, cancel_stock_entry,deduct_stock

class TalpatriManagement(Document):
    def on_submit(self):
        if self.entry_purpose in ["Inward", "Damaged", "Delivered"]:
            create_transfer_entry(self)
        elif self.entry_purpose == "Stock Reconciliation":
            process_stock_reconciliation(self)

    def on_cancel(self):
            stock_entry_name = self.voucher_number
            if self.entry_purpose != "Stock Reconciliation":
                cancel_stock_entry(stock_entry_name)
            else:
                cancel_stock_reconciliation(stock_entry_name)
                
def process_stock_reconciliation(self):
    items = [
        {
            "item_code": row.item,
            "qty": flt(row.quantity),
            "warehouse": self.warehouse,
            "valuation_rate": 100
        }
        for row in self.items
    ]

    stock_reco_name = create_stock_reconcilliation_entry(
        items, "Stock Reconciliation", self.date, self.time, self.company
    )
    self.voucher_number = stock_reco_name
    frappe.db.set_value(self.doctype, self.name, "voucher_number", stock_reco_name)

def create_transfer_entry(self):
    entry_type_map = {
        "Inward": {
            "stock_entry_type": "Material Receipt",
            "direction": "t_warehouse"
        },
        "Damaged": {
            "stock_entry_type": "Talpatri Bag Damage",
            "direction": "s_warehouse"
        },
        "Delivered": {
            "stock_entry_type": "Talpatri Bag Delivered",
            "direction": "s_warehouse"
        }
    }

    config = entry_type_map[self.entry_purpose]
    items = []

    for row in self.items:
        item = {
            "item_code": row.item,
            "qty": flt(row.quantity)
        }
        item[config["direction"]] = self.warehouse
        items.append(item)

    stock_entry_name = create_stock_transfer_entry(items, config["stock_entry_type"], self.date)
    self.voucher_number = stock_entry_name
    frappe.db.set_value(self.doctype, self.name, "voucher_number", stock_entry_name)
