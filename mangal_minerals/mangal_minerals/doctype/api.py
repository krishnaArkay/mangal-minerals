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
    add_delivered_qty(doc, method)
    
    
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
    

# Open Order
def add_delivered_qty(doc, method):
        delivery_date = doc.posting_date
        delivery_note_item_qty = doc.items[0].qty

        # Get the blanket order linked to the delivery note
        blanket_order_name = frappe.db.get_value("Sales Order Item",
                                                  filters={"parent": doc.items[0].against_sales_order},
                                                  fieldname="blanket_order")

        if blanket_order_name:
             open_order_schedulers = frappe.get_list("Open Order Scheduler", {"open_order": blanket_order_name})

             for scheduler in open_order_schedulers:
                total_qty = frappe.db.get_value("Open Order Scheduler", scheduler.name, "total_quantity")
                per_truck_mt = frappe.db.get_value("Open Order Scheduler", scheduler.name, "per_truck_mt")
                
                # Update delivered quantity, remaining_mt and reference number in open order scheduler items
                frappe.db.sql("""
                    UPDATE `tabOpen Order Scheduler Item`
                    SET delivered_mt = delivered_mt + %(qty)s,
                        reference_number = CONCAT_WS(', ', reference_number, %(ref_num)s)
                    WHERE parent = %(parent)s AND date = %(delivery_date)s
                """, {
                    'qty': delivery_note_item_qty,
                    'ref_num': doc.name,
                    'parent': scheduler.name,
                    'delivery_date': delivery_date
                })
                frappe.db.sql("""
                    UPDATE `tabOpen Order Scheduler Item`
                    SET remaining_mt = %(total_qty)s - (
                            SELECT COALESCE(SUM(delivered_mt), 0)
                            FROM `tabOpen Order Scheduler Item`
                        ),
                        difference = planned_mt - (delivered_mt),
                        actual_truck = delivered_mt/%(per_truck_mt)s
                    WHERE parent = %(parent)s AND date = %(delivery_date)s
                """, {
                    'qty': delivery_note_item_qty,
                    'total_qty': total_qty,
                    'parent': scheduler.name,
                    'delivery_date': delivery_date,
                    'per_truck_mt': per_truck_mt,
                })

             frappe.db.sql("""
                UPDATE `tabOpen Order Scheduler`
                SET total_delivered_mt = (
                    SELECT COALESCE(SUM(delivered_mt), 0) 
                    FROM `tabOpen Order Scheduler Item`
                    WHERE parent = %(parent)s
                ),
                total_remaining_mt =%(total_qty)s- total_delivered_mt
            """, {
                'parent': scheduler.name,
                'total_qty':total_qty
            })


def deduct_delivered_qty(doc, method):
    delivery_note_item_qty = doc.items[0].qty
    blanket_order_name = frappe.db.get_value("Sales Order Item",
                                                  filters={"parent": doc.items[0].against_sales_order},
                                                  fieldname="blanket_order")

    if blanket_order_name:
             open_order_schedulers = frappe.get_list("Open Order Scheduler", {"open_order": blanket_order_name})
            
             for scheduler in open_order_schedulers:
                 total_qty = frappe.db.get_value("Open Order Scheduler", scheduler.name, "total_quantity")
                 per_truck_mt = frappe.db.get_value("Open Order Scheduler", scheduler.name, "per_truck_mt")
                    # Update delivered quantity and reference number in open order scheduler for cancelled delivery note
                 frappe.db.sql("""
                        UPDATE `tabOpen Order Scheduler Item`
                        SET delivered_mt = delivered_mt - %(qty)s, 
                              difference = planned_mt - delivered_mt, 
                              actual_truck = delivered_mt/%(per_truck_mt)s, 
                              reference_number = REPLACE(reference_number, %(ref_num)s, ''), 
                              remaining_mt = remaining_mt +%(qty)s
                        WHERE reference_number LIKE CONCAT('%%', %(ref_num)s, '%%')
                        # WHERE reference_number = %(ref_num)s
                    """, {
                        'qty': delivery_note_item_qty,
                        'ref_num': doc.name,
                        'per_truck_mt':per_truck_mt,

                    })   

                 frappe.db.sql("""
                            UPDATE `tabOpen Order Scheduler`
                            SET total_delivered_mt = (
                                SELECT COALESCE(SUM(delivered_mt), 0) 
                                FROM `tabOpen Order Scheduler Item`
                                WHERE parent = %(parent)s
                            ),
                              total_remaining_mt =%(total_qty)s- total_delivered_mt
                        """, {
                            'parent': scheduler.name,
                            'total_qty':total_qty
                        })
       