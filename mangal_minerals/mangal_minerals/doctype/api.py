import frappe
from mangal_minerals.mangal_minerals.enums.enums import JumboBagEntryPurpose

def create_stock_transfer_entry(items,stock_entry_type):
    doc = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": stock_entry_type,
        "items": items
    })
    doc.save()
    doc.submit()
    return doc.name

def create_stock_entry_manufacture(input_items, output_items, target_warehouse, stock_entry_type):
    items = []
    
    # Add items from Material Input with s_warehouse set
    for item, qty in input_items:
        items.append({
            "item_code": item,
            "qty": qty,
            "s_warehouse": target_warehouse,
            "is_finished_item":0
        })
    
    # Add items from Material Output with t_warehouse set
    for item, qty, is_finished_good in output_items:
        items.append({
            "item_code": item,
            "qty": qty,
            "t_warehouse": target_warehouse,
            "is_finished_item": is_finished_good  
        })
    
    # Create stock entry document
    stock_entry = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": stock_entry_type,
        "items": items
    })
    
    # Save and submit stock entry
    stock_entry.save()
    stock_entry.submit()
    
    return stock_entry.name

def cancel_stock_entry(voucher_number):
    stock_entry = frappe.get_doc("Stock Entry", voucher_number)
    if stock_entry.docstatus == 1:  # Check if the stock entry is submitted
        stock_entry.cancel()

# Jumbo Bag Stock Effect
@frappe.whitelist(allow_guest=True)
def deduct_stock(jumbo_bag_name, warehouse, mangal_bag_item,entry_purpose,mangal_warehouse):
    jumbo_bag = frappe.get_doc("Jumbo Bag Management", jumbo_bag_name)

    for item in jumbo_bag.items:
        if item.mangals_bag == 0:
            item_code = item.item
            stock = frappe.get_value("Bin", {"item_code": item_code, "warehouse": warehouse}, "actual_qty") or 0
            if stock < 0:
                # Create Jumbo Bag document
                jumbo_bag_entry = frappe.get_doc({
                    "doctype": "Jumbo Bag Management",
                    "entry_purpose":entry_purpose,
                    "warehouse": mangal_warehouse,
                    "jumbo_bag_reference": jumbo_bag_name,
                    "remarks": f"{item_code} - this item has negative value that's why Mangal Minerals {mangal_bag_item} bag Stock Effect. Reference of Jumbo Bag {jumbo_bag_name}",
                    "items": [{
                        "item": mangal_bag_item,
                        "quantity": -stock,  # Deduct the negative stock from the Mangal Bag item
                    }]
                })

                jumbo_bag_entry.save()
                jumbo_bag_entry.submit()
                
                frappe.msgprint(f"Stock updated to {mangal_bag_item} due to negative stock of {item_code}.")

def item_validation(doc,method):
    if doc.item_group == "Jumbo Bag":
        doc.allow_negative_stock = 1
        
        if doc.custom_mangals_bag:
            item_exists = frappe.db.exists({
            'doctype': 'Item',
            'item_group': 'Jumbo Bag',
            'custom_mangals_bag': 1
            })
        
            if item_exists:
                # Logic if the item exists
                frappe.throw("An item with 'Mangal's Bag' already exists.")

#delivery note
def delivery_note_on_submit(doc, method):
    entry_purpose = JumboBagEntryPurpose.DELIVERED.value
    reference_doctype = "Delivery Note"
    reference_number = doc
    jumbo_bag_items = []  
    jumbo_bag_warehouse = None  
    for item in doc.items:
        if item.item_group == "Jumbo Bag":
            if jumbo_bag_warehouse is None:  
                jumbo_bag_warehouse = item.warehouse
            jumbo_bag_items.append({
                "item_code": item.item_code,
                "qty": item.qty
            })
    if jumbo_bag_items:
        create_jumbo_bag_document(reference_doctype, reference_number, entry_purpose, jumbo_bag_items,jumbo_bag_warehouse)
    
#Purchase reciept
def purchase_receipt_on_submit(doc, method):
    entry_purpose = JumboBagEntryPurpose.INWARD.value
    reference_doctype = "Purchase Receipt"
    reference_number = doc.name
    jumbo_bag_items = []  
    jumbo_bag_warehouse = None  
    for item in doc.items:
        if item.item_group == "Jumbo Bag":
            if jumbo_bag_warehouse is None:  
                jumbo_bag_warehouse = item.warehouse
            jumbo_bag_items.append({
                "item_code": item.item_code,
                "qty": item.qty
            })
    if jumbo_bag_items:
        create_jumbo_bag_document(reference_doctype, reference_number, entry_purpose, jumbo_bag_items,jumbo_bag_warehouse)
            

def create_jumbo_bag_document(reference_doctype,reference_number,entry_purpose, jumbo_bag_items, jumbo_bag_warehouse):    # Create a new Jumbo Bag document
    jumbo_bag_doc = frappe.new_doc("Jumbo Bag Management")
    # Set any relevant fields for the Jumbo Bag document
    jumbo_bag_doc.reference_doctype = reference_doctype
    jumbo_bag_doc.entry_purpose = entry_purpose
    jumbo_bag_doc.reference_number = reference_number
    jumbo_bag_doc.warehouse = jumbo_bag_warehouse
    jumbo_bag_doc.remarks = f"Created From {reference_doctype} - {reference_number}"
    for item in jumbo_bag_items:
        jumbo_bag_doc.append("items", {
            "item": item["item_code"],
            "quantity": item["qty"],
        })
    # Save and submit the Jumbo Bag document
    jumbo_bag_doc.insert()
    jumbo_bag_doc.submit()