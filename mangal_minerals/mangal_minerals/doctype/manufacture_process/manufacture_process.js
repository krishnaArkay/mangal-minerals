// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.ui.form.on("Manufacture Process", {
	refresh: function(frm) {
        if (frm.is_new()) {
            frm.doc.voucher_number = "";
            frm.doc.jumbo_bag = "";
            frm.doc.remarks = ""
        }
       if(frm.doc.docstatus === 1){
            // Add a custom button for the Stock Ledger report
            frm.add_custom_button(__('Stock Ledger'), function() {
                frappe.set_route('query-report', 'Stock Ledger', {
                    voucher_no: frm.doc.voucher_number,
                    from_date: frm.doc.date,
                    to_date: frm.doc.date,
                });
            });
            // Add a custom button for Stock Transfer
            frm.add_custom_button(__('Stock Transfer'), function() {
                create_stock_transfer(frm);
            }, __('Create'));
            // frm.add_custom_button(__('Delivery Note'), function() {
            //     create_delivery_note(frm)
            // }, __('Create'));
        }
    },
    before_save: function(frm) {
        let total_percentage = 0;
    
        frm.doc.material_output.forEach(function(row) {
            total_percentage += row.percentage;
            // if (row.percentage === 0) {
            //     // Remove row from Material Output table
            //     frm.doc.material_output = frm.doc.material_output.filter(item => item.name !== row.name);
            // }
        });
    
        if (total_percentage !== 100) {
            frappe.throw("The total percentage must be 100%.");
        }
    }
});
frappe.ui.form.on('Material Input', {
    material_input_add: function(frm,cdt,cdn){
        clear_table(frm)
    },
    material_input_remove: function(frm,cdt,cdn){
        clear_table(frm);
    },
    item: function(frm,cdt,cdn){
        clear_table(frm)
    },
    quantity: function(frm,cdt,cdn){
        clear_table(frm)
    }
})

frappe.ui.form.on('Material Output', {
    percentage: function(frm, cdt, cdn) {
        var total_input_qty = 0;

        // Calculate the total input quantity
        frm.doc.material_input.forEach(function(row) {
            total_input_qty += row.quantity;
        });
        var total_percentage = 0;
        // Loop through all material output rows
        frm.doc.material_output.forEach(function(row) {
            total_percentage += row.percentage || 0;
            // Calculate the output quantity based on the percentage
            var output_qty = total_input_qty * (row.percentage / 100);
            frappe.model.set_value(cdt, row.name, 'quantity', output_qty);
        });

        if (total_percentage > 100) {
            frappe.throw("Total percentage cannot exceed 100%. Please adjust.");
            // frappe.model.set_value(cdt, cdn, 'percentage', 0);
            return;
        }
    }
});
function clear_table(frm){
    if (frm.doc.material_output && frm.doc.material_output.length > 0) {
        cur_frm.clear_table("material_output"); 
        cur_frm.refresh_fields();
        console.log("Table Material Output cleared");
    }
}

function create_stock_transfer(frm) {
    // Create a new Stock Transfer document
    frappe.new_doc("Stock Transfer", {}, doc => {
        doc.default_from_warehouse = frm.doc.warehouse;
        doc.defualt_to_warehouse = '';
        doc.reference_no = frm.doc.name;
        // Set other fields as needed
        frappe.model.clear_table(doc, "items");

        frm.doc.material_output.forEach(mo_item => {
            let st_item = frappe.model.add_child(doc, "items");
            st_item.item = mo_item.item;
            st_item.quantity = mo_item.quantity;
            st_item.from_warehouse = frm.doc.warehouse;

            // Set other fields as needed
        });
    });
}
function create_delivery_note(frm) {
    // Create a new Delivery Note document
    frappe.new_doc("Delivery Note", {}, doc => {
        doc.set_warehouse = frm.doc.warehouse;
        frappe.model.clear_table(doc, "items");

        const add_item = (item) => {
            let dn_item = frappe.model.add_child(doc, "items");
            dn_item.item_code = item.item;
            dn_item.qty = item.quantity;
            frappe.db.get_value("Item", item.item, ["item_name", "item_group", "stock_uom"], (r) => {
                if (r) {
                    dn_item.item_name = r.item_name;
                    dn_item.item_group = r.item_group;
                    dn_item.uom = r.stock_uom;
                }
            });
        };

        frm.doc.material_output.forEach(add_item);

        if (frm.doc.jumbo_bag_items && frm.doc.jumbo_bag_items.length > 0) {
            frm.doc.jumbo_bag_items.forEach(add_item);
        }
    });
}
