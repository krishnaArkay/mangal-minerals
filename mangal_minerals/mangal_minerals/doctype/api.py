import frappe
from frappe.utils import now_datetime, add_days,nowdate,getdate, today, now, get_first_day, nowdate, getdate
from datetime import datetime
from mangal_minerals.mangal_minerals.enums.enums import JumboBagEntryPurpose

@frappe.whitelist()
def get_sales_data():
    # Today's date
    today_date = getdate(today())  # Convert today's date to datetime object
    
    # Yesterday's date
    yesterday_date = getdate(add_days(today_date, -1))  # Convert yesterday's date to datetime object
    
    # First day of the current month
    first_day_of_month = getdate(get_first_day(nowdate()))  # Convert first day of the month to datetime object

    # Fetch Sales Orders Items for today
    today_sales = frappe.db.get_all('Sales Order Item', 
        filters={'transaction_date': ['>=', today_date]}, 
        fields=['item_name', 'qty', 'amount', 'transaction_date'])

    # Fetch Sales Orders Items for yesterday
    yesterday_sales = frappe.db.get_all('Sales Order Item', 
        filters={'transaction_date': ['>=', yesterday_date], 'transaction_date': ['<', today_date]},
        fields=['item_name', 'qty', 'amount', 'transaction_date'])

    # Fetch Sales Orders Items for the current month
    monthly_sales = frappe.db.get_all('Sales Order Item',
        filters={'transaction_date': ['>=', first_day_of_month]}, 
        fields=['item_name', 'qty', 'amount', 'transaction_date'])

    # Initialize dictionaries to hold aggregated data
    today_summary = {}
    yesterday_summary = {}
    monthly_summary = {}

    # Function to aggregate sales data
    def aggregate_sales_data(sales, summary, date_range):
        for sale in sales:
            item_name = sale['item_name']
            amount = sale['amount']
            transaction_date = getdate(sale['transaction_date'])  # Convert transaction_date from string to datetime

            if item_name not in summary:
                summary[item_name] = {
                    'item_name': item_name,
                    'today_amount': 0,
                    'yesterday_amount': 0,
                    'monthly_amount': 0
                }
            
            # Determine which period the sale falls into
            if date_range == 'today' and transaction_date >= today_date:
                summary[item_name]['today_amount'] += amount
            elif date_range == 'yesterday' and yesterday_date <= transaction_date < today_date:
                summary[item_name]['yesterday_amount'] += amount
            elif date_range == 'monthly' and transaction_date >= first_day_of_month:
                summary[item_name]['monthly_amount'] += amount

    # Aggregate data
    aggregate_sales_data(today_sales, today_summary, 'today')
    aggregate_sales_data(yesterday_sales, yesterday_summary, 'yesterday')
    aggregate_sales_data(monthly_sales, monthly_summary, 'monthly')

    # Summarize the totals
    today_total_qty = sum(item['today_amount'] for item in today_summary.values())
    yesterday_total_qty = sum(item['yesterday_amount'] for item in yesterday_summary.values())
    monthly_total_qty = sum(item['monthly_amount'] for item in monthly_summary.values())

    today_total_amount = today_total_qty
    yesterday_total_amount = yesterday_total_qty
    monthly_total_amount = monthly_total_qty

    return {
        'today_sales': list(today_summary.values()),
        'yesterday_sales': list(yesterday_summary.values()),
        'monthly_sales': list(monthly_summary.values()),
        'today_total_qty': today_total_qty,
        'yesterday_total_qty': yesterday_total_qty,
        'monthly_total_qty': monthly_total_qty,
        'today_total_amount': today_total_amount,
        'yesterday_total_amount': yesterday_total_amount,
        'monthly_total_amount': monthly_total_amount
    }
#------------------------------------------------------------------------------------------------------------------#
@frappe.whitelist()
def get_purchase_order_data():
    # Today's date
    today_date = getdate(today())  # Convert today's date to datetime object
    
    # Yesterday's date
    yesterday_date = getdate(add_days(today_date, -1))  # Convert yesterday's date to datetime object
    
    # First day of the current month
    first_day_of_month = getdate(get_first_day(nowdate()))  # Convert first day of the month to datetime object

    # Fetch Purchase Order Items for today
    today_orders = frappe.db.get_all('Purchase Order Item',
        filters={'transaction_date': ['>=', today_date]},
        fields=['item_name', 'qty', 'amount', 'transaction_date'])

    # Fetch Purchase Order Items for yesterday
    yesterday_orders = frappe.db.get_all('Purchase Order Item',
        filters={'transaction_date': ['>=', yesterday_date], 'transaction_date': ['<', today_date]},
        fields=['item_name', 'qty', 'amount', 'transaction_date'])

    # Fetch Purchase Order Items for the current month
    monthly_orders = frappe.db.get_all('Purchase Order Item',
        filters={'transaction_date': ['>=', first_day_of_month]},
        fields=['item_name', 'qty', 'amount', 'transaction_date'])

    # Initialize dictionaries to hold aggregated data
    today_summary = {}
    yesterday_summary = {}
    monthly_summary = {}

    # Function to aggregate purchase order data
    def aggregate_purchase_data(orders, summary, date_range):
        for order in orders:
            item_name = order['item_name']
            amount = order['amount']
            transaction_date = getdate(order['transaction_date'])  # Convert transaction_date from string to datetime

            if item_name not in summary:
                summary[item_name] = {
                    'item_name': item_name,
                    'today_amount': 0,
                    'yesterday_amount': 0,
                    'monthly_amount': 0
                }
            
            # Determine which period the order falls into
            if date_range == 'today' and transaction_date >= today_date:
                summary[item_name]['today_amount'] += amount
            elif date_range == 'yesterday' and yesterday_date <= transaction_date < today_date:
                summary[item_name]['yesterday_amount'] += amount
            elif date_range == 'monthly' and transaction_date >= first_day_of_month:
                summary[item_name]['monthly_amount'] += amount

    # Aggregate data
    aggregate_purchase_data(today_orders, today_summary, 'today')
    aggregate_purchase_data(yesterday_orders, yesterday_summary, 'yesterday')
    aggregate_purchase_data(monthly_orders, monthly_summary, 'monthly')

    # Summarize the totals
    today_total_qty = sum(item['today_amount'] for item in today_summary.values())
    yesterday_total_qty = sum(item['yesterday_amount'] for item in yesterday_summary.values())
    monthly_total_qty = sum(item['monthly_amount'] for item in monthly_summary.values())

    today_total_amount = today_total_qty
    yesterday_total_amount = yesterday_total_qty
    monthly_total_amount = monthly_total_qty

    return {
        'today_orders': list(today_summary.values()),
        'yesterday_orders': list(yesterday_summary.values()),
        'monthly_orders': list(monthly_summary.values()),
        'today_total_qty': today_total_qty,
        'yesterday_total_qty': yesterday_total_qty,
        'monthly_total_qty': monthly_total_qty,
        'today_total_amount': today_total_amount,
        'yesterday_total_amount': yesterday_total_amount,
        'monthly_total_amount': monthly_total_amount
    }

#------------------------------------------------------------------------------------------------------------------#
@frappe.whitelist()
def get_top_sales_data():
    # Today's date
    today_date = getdate(today())
    
    # Yesterday's date
    yesterday_date = getdate(add_days(today_date, -1))
    
    # First day of the current month
    first_day_of_month = getdate(get_first_day(nowdate()))

    # Fetch Sales Orders Items for today
    today_sales = frappe.db.get_all('Sales Order',
        filters={'transaction_date': ['>=', today_date]},
        fields=['customer', 'total', 'transaction_date'])

    # Fetch Sales Orders Items for yesterday
    yesterday_sales = frappe.db.get_all('Sales Order',
        filters={'transaction_date': ['>=', yesterday_date], 'transaction_date': ['<', today_date]},
        fields=['customer', 'total', 'transaction_date'])

    # Fetch Sales Orders Items for the current month
    monthly_sales = frappe.db.get_all('Sales Order',
        filters={'transaction_date': ['>=', first_day_of_month]},
        fields=['customer', 'total', 'transaction_date'])

    # Initialize dictionaries to hold aggregated data
    today_summary = {}
    yesterday_summary = {}
    monthly_summary = {}

    # Function to aggregate sales data by customer
    def aggregate_sales_data(sales, summary, date_range):
        for sale in sales:
            customer = sale['customer']
            total = sale['total']
            transaction_date = getdate(sale['transaction_date'])

            if customer not in summary:
                summary[customer] = {
                    'customer': customer,
                    'today_total': 0,
                    'yesterday_total': 0,
                    'monthly_total': 0
                }
            
            if date_range == 'today' and transaction_date >= today_date:
                summary[customer]['today_total'] += total
            elif date_range == 'yesterday' and yesterday_date <= transaction_date < today_date:
                summary[customer]['yesterday_total'] += total
            elif date_range == 'monthly' and transaction_date >= first_day_of_month:
                summary[customer]['monthly_total'] += total

    # Aggregate data
    aggregate_sales_data(today_sales, today_summary, 'today')
    aggregate_sales_data(yesterday_sales, yesterday_summary, 'yesterday')
    aggregate_sales_data(monthly_sales, monthly_summary, 'monthly')

    # Combine all summaries into a single result
    all_customers = set(today_summary.keys()) | set(yesterday_summary.keys()) | set(monthly_summary.keys())
    combined_summary = {}

    for customer in all_customers:
        combined_summary[customer] = {
            'customer': customer,
            'today_total': today_summary.get(customer, {}).get('today_total', 0),
            'yesterday_total': yesterday_summary.get(customer, {}).get('yesterday_total', 0),
            'monthly_total': monthly_summary.get(customer, {}).get('monthly_total', 0)
        }

    # Sort by monthly_total and take the top 5 customers
    top_customers = sorted(combined_summary.values(), key=lambda x: x['monthly_total'], reverse=True)[:5]

    # Summarize the totals
    today_total_total = sum(item['today_total'] for item in top_customers)
    yesterday_total_total = sum(item['yesterday_total'] for item in top_customers)
    monthly_total_total = sum(item['monthly_total'] for item in top_customers)

    return {
        'top_sales_by_customer': top_customers,
        'today_total_total': today_total_total,
        'yesterday_total_total': yesterday_total_total,
        'monthly_total_total': monthly_total_total
    }


#------------------------------------------------------------------------------------------------------------------#
# def send_daily_report():
    # """
    # Sends the daily purchase receipt report via email.
    # """
    # data = get_daily_purchase_report()
    
    # if not data:
    #     frappe.msgprint("No purchase receipts found for the previous day.")
    #     return
    
    # total_qty = sum(row['qty'] for row in data)
    # report_content = f"""
    # <div style="font-family: Arial, sans-serif;">
    #     <h2 style="text-align: left;">Daily Purchase Receipt Report</h2>
    #     <table style="width: 100%; border-collapse: collapse;">
    #         <thead>
    #             <tr>
    #                 <th style="border: 1px solid #f0f0f0; padding: 8px; text-align: left;">#</th>
    #                 <th style="border: 1px solid #f0f0f0; padding: 8px; text-align: left;">Party Name</th>
    #                 <th style="border: 1px solid #f0f0f0; padding: 8px; text-align: left;">Item</th>
    #                 <th style="border: 1px solid #f0f0f0; padding: 8px; text-align: left;">Quantity</th>
    #                 <th style="border: 1px solid #f0f0f0; padding: 8px; text-align: left;">Royalty</th>
    #             </tr>
    #         </thead>
    #         <tbody>
    # """
    
    # for idx, row in enumerate(data, 1):
    #     report_content += f"""
    #         <tr>
    #             <td style="border: 1px solid #f0f0f0; padding: 8px;">{idx}</td>
    #             <td style="border: 1px solid #f0f0f0; padding: 8px;">{row['party_name']}</td>
    #             <td style="border: 1px solid #f0f0f0; padding: 8px;">{row['item_name']}</td>
    #             <td style="border: 1px solid #f0f0f0; padding: 8px;">{row['qty']}</td>
    #             <td style="border: 1px solid #f0f0f0; padding: 8px;">{row['royalty']}</td>
    #         </tr>
    #     """
    
    # report_content += f"""
    #     <tr>
    #         <td style="border: 1px solid #f0f0f0; padding: 8px;" colspan="3"><b>Total</b></td>
    #         <td style="border: 1px solid #f0f0f0; padding: 8px;" colspan="2">{total_qty}</td>
    #     </tr>
    #     </tbody>
    #     </table>
    #     <p style="font-size: 12px; color: #687178;">This report was generated on {now()}.</p>
    # </div>
    # """
    
    # frappe.sendmail(
    #     recipients=["krishna@arkayapps.com"],  # Update with actual email
    #     subject="Daily Purchase Receipt Report",
    #     message=report_content,
    #     sender="krishna@arkayapps.com",
    #     # is_html=True
    # )
    
    # frappe.msgprint("Email sent successfully")
#------------------------------------------------------------------------------------------------------------------#
def transaction_date(doc, method):
    # Ensure that the parent document has a transaction_date
    if doc.transaction_date:
        # Iterate through the child table items
        for item in doc.items:
            # Set the transaction_date in the child table
            item.transaction_date = doc.transaction_date
#------------------------------------------------------------------------------------------------------------------#

def create_stock_transfer_entry(items,stock_entry_type):
    doc = frappe.get_doc({
        "doctype": "Stock Entry",
        "stock_entry_type": stock_entry_type,
        "items": items
    })
    doc.save(ignore_permissions=True)
    doc.submit()
    return doc.name

#------------------------------------------------------------------------------------------------------------------#
# Manufacture Process
def create_stock_entry_manufacture(input_items, output_items,jb_items, target_warehouse, stock_entry_type,j_b_flag, per_kg_jb):
    items = []
    jb_qty = 0
    if j_b_flag:
        for item, qty in jb_items:
            jb_qty += qty
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
        if j_b_flag:
            if is_finished_good == 1:
                qty_kg = qty * 1000
                jb_number_qty = qty_kg / per_kg_jb
                total_bag = jb_qty * per_kg_jb
                rem_qty = qty_kg - total_bag

                total_bag_mt = total_bag / 1000
                rem_qty_mt  = rem_qty / 1000

                items.append({
                    "item_code": item,
                    "qty": rem_qty_mt,
                    "t_warehouse": target_warehouse,
                    "is_finished_item": is_finished_good  
                })
            else:
                items.append({
                    "item_code": item,
                    "qty": qty,
                    "t_warehouse": target_warehouse,
                    "is_finished_item": is_finished_good  
                })
        else:
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
    stock_entry.save(ignore_permissions=True)
    stock_entry.submit()
    
    return stock_entry.name
#------------------------------------------------------------------------------------------------------------------#


#------------------------------------------------------------------------------------------------------------------#
# Cancel Stock Entry
def cancel_stock_entry(voucher_number):

    # frappe.db.sql(f"UPDATE `tabStock Entry` SET docstatus = 2 WHERE name = '{voucher_number}'")
    # frappe.db.commit()
    # original_user = frappe.session.user  # Save the original user
    # try:
    #     # Temporarily set user as Administrator to bypass permissions
    #     frappe.set_user('Administrator')
    stock_entry = frappe.get_doc("Stock Entry", voucher_number)
    if stock_entry and stock_entry.docstatus == 1:  # Check if the stock entry is submitted
        stock_entry.cancel()    
    # except Exception as e:
    #     frappe.log_error(f"Error cancelling Stock Entry {voucher_number}: {str(e)}")
    # finally:
    #     frappe.set_user(original_user)
#------------------------------------------------------------------------------------------------------------------#

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
                    "remarks": f"{item_code} has a negative value, causing the stock of {mangal_bag_item} to be affected. Reference: Jumbo Bag {jumbo_bag_name}.",
                    "items": [{
                        "item": mangal_bag_item,
                        "quantity": -stock,  # Deduct the negative stock from the Mangal Bag item
                    }]
                })

                jumbo_bag_entry.save(ignore_permissions=True)
                jumbo_bag_entry.submit()
                
                frappe.msgprint(f"Stock was updated from {mangal_bag_item} due to negative stock of {item_code}.")
#------------------------------------------------------------------------------------------------------------------#
def item_validation(doc,method):
    # send_daily_report()
    if doc.item_group == "Services":
        doc.is_stock_item = 0
    if doc.item_group == "Jumbo Bag":
        if not doc.allow_negative_stock:
            doc.allow_negative_stock = 1
            
        if doc.custom_mangals_bag:
            if doc.name != "Mangal Bag":
                item_exists = frappe.db.exists({
                'doctype': 'Item',
                'item_group': 'Jumbo Bag',
                'custom_mangals_bag': 1
                })
            
                if item_exists:
                    # Logic if the item exists
                    frappe.throw("An item with 'Mangal's Bag' already exists.")
    else:
        doc.custom_mangals_bag = 0
#------------------------------------------------------------------------------------------------------------------#

#delivery note
def dn_before_save(doc,method):
    for item in doc.items:
        if item.item_group == "Jumbo Bag":
            frappe.db.set_value("Item", item.item_code, "allow_negative_stock", 0)
def dn_after_save(doc,method):
    for item in doc.items:
        if item.item_group == "Jumbo Bag":
            frappe.db.set_value("Item", item.item_code, "allow_negative_stock", 1)
def delivery_note_on_submit(doc, method):
    entry_purpose = JumboBagEntryPurpose.DELIVERED.value
    reference_doctype = "Delivery Note"
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
    update_delivered_qty(doc, method)
    frappe.db.set_value("Item", item.item_code, "allow_negative_stock", 1)
#------------------------------------------------------------------------------------------------------------------#

#Purchase reciept Submit
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

#------------------------------------------------------------------------------------------------------------------#

#Purchase reciept Cancel

#------------------------------------------------------------------------------------------------------------------#

 # Create a new Jumbo Bag document  
def create_jumbo_bag_document(reference_doctype,reference_number,entry_purpose, jumbo_bag_items, jumbo_bag_warehouse):    
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
    jumbo_bag_doc.save(ignore_permissions=True)
    jumbo_bag_doc.submit()
#------------------------------------------------------------------------------------------------------------------#
    
def update_delivered_qty(doc, method):
    delivery_note_item_qty = doc.items[0].qty
    blanket_order_name = frappe.db.get_value("Sales Order Item",
                                             filters={"parent": doc.items[0].against_sales_order},
                                             fieldname="blanket_order")
    
    if blanket_order_name:
        open_order_schedulers = frappe.get_list("Open Order Scheduler", {"open_order": blanket_order_name, "docstatus":1})

        for scheduler in open_order_schedulers:
            total_qty = frappe.db.get_value("Open Order Scheduler", scheduler.name, "total_quantity")
            per_truck_mt = frappe.db.get_value("Open Order Scheduler", scheduler.name, "per_truck_mt")
            parent_doc = frappe.get_doc("Open Order Scheduler", scheduler.name)
            if method == "on_submit":
                delivery_date_exists = frappe.db.exists("Open Order Scheduler Item", {
                    "parent": scheduler.name,
                    "date": doc.posting_date
                })
                if delivery_date_exists:
                    
                # Update delivered quantity, remaining_mt and reference number in open order scheduler items for submitted delivery note
                    frappe.db.sql("""
                        UPDATE `tabOpen Order Scheduler Item`
                        SET delivered_mt = delivered_mt + %(qty)s,
                            reference_number = CONCAT_WS(', ', reference_number, %(ref_num)s)
                        WHERE parent = %(parent)s AND date = %(delivery_date)s
                    """, {
                        'qty': delivery_note_item_qty,
                        'ref_num': doc.name,
                        'parent': scheduler.name,
                        'delivery_date': doc.posting_date
                    })
                else:
                    # new_child_row = frappe.new_doc("Open Order Scheduler Item")
                    new_child_row = frappe.get_doc("Blanket Order",scheduler.name)
                    new_child_row.parent = parent_doc.name  # Parent document name
                    new_child_row.parenttype = parent_doc.doctype  # Parent document type
                    new_child_row.parentfield = "items"  # Child table field name in parent document
                    new_child_row.date = doc.posting_date
                    new_child_row.delivered_mt = delivery_note_item_qty
                    new_child_row.reference_number = doc.name
                    new_child_row.planned_mt = 0
                    new_child_row.planned_truck = 0

                    new_child_row.insert(ignore_permissions=True)
                    parent_doc.append("items", new_child_row)

                    # Save the parent document
                    parent_doc.save()
                    
                    # frappe.db.commit()

                frappe.db.sql("""
                    UPDATE `tabOpen Order Scheduler Item`
                    SET remaining_mt = %(total_qty)s - (
                                    SELECT COALESCE(SUM(delivered_mt), 0)
                                    FROM `tabOpen Order Scheduler Item`
                                    WHERE parent = %(parent)s
                                ),
                        difference = planned_mt - (delivered_mt),
                        actual_truck = delivered_mt/%(per_truck_mt)s
                    WHERE parent = %(parent)s AND date = %(delivery_date)s
                """, {
                    'qty': delivery_note_item_qty,
                    'total_qty': total_qty,
                    'parent': scheduler.name,
                    'delivery_date':doc.posting_date,
                    'per_truck_mt': per_truck_mt,
                })
            

            elif method == "on_cancel":
                # Update delivered quantity and reference number in open order scheduler for cancelled delivery note
                frappe.db.sql("""
                    UPDATE `tabOpen Order Scheduler Item`
                    SET delivered_mt = delivered_mt - %(qty)s, 
                        difference = planned_mt - delivered_mt, 
                        actual_truck = delivered_mt/%(per_truck_mt)s, 
                        reference_number = REPLACE(reference_number, %(ref_num)s, ''), 
                        remaining_mt = remaining_mt + %(qty)s
                    WHERE reference_number LIKE CONCAT('%%', %(ref_num)s, '%%')
                """, {
                    'qty': delivery_note_item_qty,
                    'ref_num': doc.name,
                    'per_truck_mt': per_truck_mt
                })

            # Update total delivered and remaining quantities in the parent scheduler
            frappe.db.sql("""
                UPDATE `tabOpen Order Scheduler`
                SET total_delivered_mt = (
                    SELECT COALESCE(SUM(delivered_mt), 0) 
                    FROM `tabOpen Order Scheduler Item`
                    WHERE parent = %(parent)s
                ),
                total_remaining_mt = %(total_qty)s - total_delivered_mt,
                delivered = (total_delivered_mt/total_quantity)*100,
                remaining = (total_remaining_mt/total_quantity)*100,
                status = CASE
                    WHEN total_quantity <= total_delivered_mt THEN 'Completed'
                    WHEN total_delivered_mt > 0 AND total_quantity > total_delivered_mt THEN 'Partially Completed'
                    ELSE status
                END
                WHERE name = %(parent)s
            """, {
                'parent': scheduler.name,
                'total_qty': total_qty
            })
            frappe.db.commit() 
            
#------------------------------------------------------------------------------------------------------------------#
# Schedular at 01:01 AM
@frappe.whitelist()
def update_OPS_truck():
    frappe.logger().info("update_OPS_truck called")
    diff_truck = None
    extra = None
    extra_mt = None
    yesterday = getdate(add_days(nowdate(), -1))
    frappe.logger().info(f"Calculated yesterday's date: {yesterday}")
    print(f"yesterday {yesterday}")

    parent_docs = frappe.get_all('Open Order Scheduler', fields=['name'], filters={'docstatus': 1})
    frappe.logger().info(f"Fetched {len(parent_docs)} parent documents")

    for doc in parent_docs:
        parent_doc = frappe.get_doc('Open Order Scheduler', doc.name)
        per_truck_mt = parent_doc.per_truck_mt
        frappe.logger().info(f"Processing document: {doc.name} with per_truck_mt: {per_truck_mt}")

        for item in parent_doc.items:
            frappe.logger().info(f"Checking item with date: {item.date}")
            print(f"item {item.date}")
            if str(item.date) == str(yesterday):
                frappe.logger().info(f"Item date matches yesterday: {yesterday}")
                print(f"date")
                if item.actual_truck:
                    if item.delivered_mt:
                        extra_mt = item.delivered_mt/parent_doc.per_truck_mt
                        if item.actual_truck > extra_mt:
                            extra_mt =  item.actual_truck -extra_mt
                        else:
                            extra_mt = None
                    else:
                        extra_mt = item.actual_truck
                    diff_truck = extra_mt
                    print(f"Delivery: {item.delivered_mt}, Extra: {extra_mt}")
                    frappe.logger().info(f"Calculated extra_mt: {extra_mt}, actual_truck: {item.actual_truck}, delivered_mt: {item.delivered_mt}")
                    # frappe.msgprint(f"Extra: {extra}")
                if item.planned_truck > item.actual_truck:
                    diff_truck = item.planned_truck - item.actual_truck
                    frappe.logger().info(f"Calculated diff_truck: {diff_truck}, planned_truck: {item.planned_truck}, actual_truck: {item.actual_truck}")

        if diff_truck is not None:
            found_future_item = False
            frappe.logger().info(f"diff_truck is not None, looking for future items")

            for item in parent_doc.items:
                frappe.logger().info(f"Checking future item with date: {item.date}")
                print(f"item.date: {item.date}, yesterday: {yesterday}")
                if item.date > yesterday:
                    item.planned_truck += diff_truck
                    item.planned_mt = item.planned_truck * per_truck_mt
                    parent_doc.save(ignore_permissions=True)
                    print(f"Updated item {item.idx} on {item.date} with new planned_truck: {item.planned_truck}")
                    frappe.logger().info(f"Updated item {item.idx} on {item.date} with new planned_truck: {item.planned_truck}, planned_mt: {item.planned_mt}")
                    found_future_item = True
                    break
                
            if not found_future_item:
                new_item = parent_doc.append("items", {})
                new_item.date = nowdate()
                new_item.planned_truck = 0
                new_item.planned_mt = 0
                new_item.actual_truck = diff_truck
                new_item.actual_mt = new_item.planned_truck * per_truck_mt
                new_item.delivered_mt = 0
                parent_doc.save(ignore_permissions=True)
                frappe.logger().info(f"Added new item for today with actual_truck: {diff_truck}, actual_mt: {new_item.actual_mt}")
                print("Added new item for today")
    frappe.logger().info("update_OPS_truck completed")
# ---------------------------------------------------------------------------------------------------------------#

@frappe.whitelist()
def get_items_from_blanket_order(blanket_order):
    items = frappe.get_all('Blanket Order Item', filters={'parent': blanket_order}, fields=['item_code'])
    return [item['item_code'] for item in items]
#------------------------------------------------------------------------------------------------------------------#

def before_delete(doc,method):
    if doc.item_code == "Diesel":
        frappe.throw("You cannot delete this item.")
#------------------------------------------------------------------------------------------------------------------#

def before_rename(doc, method,old_name, new_name, merge=False):
    if old_name == "Diesel":
        frappe.throw("You cannot rename this item.")
#------------------------------------------------------------------------------------------------------------------#
    