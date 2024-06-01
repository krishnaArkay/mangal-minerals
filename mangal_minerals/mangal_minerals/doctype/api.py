import frappe
# def create_stock_entry(items):
#     # Create a new Stock Entry document
#     stock_entry = frappe.get_doc({
#         "doctype": "Stock Entry",
#         "stock_entry_type": stock_entry_type,
#         "items": [{
#             "item_code": item_code,
#             "qty": qty,
#             "t_warehouse": target_warehouse
#         }]
#     })

    # Insert the document into the database
    # stock_entry.save()
    # # Submit the document to make it a valid entry
    # stock_entry.submit()
    
    # return stock_entry.name

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
    # Initialize stock entry items list
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
            "is_finished_item": is_finished_good  # Directly using row.is_finished_good
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

def cancel_stock_entry(stock_entry_name):
    stock_entry = frappe.get_doc("Stock Entry", stock_entry_name)
    if stock_entry.docstatus == 1:  # Check if the stock entry is submitted
        stock_entry.cancel()