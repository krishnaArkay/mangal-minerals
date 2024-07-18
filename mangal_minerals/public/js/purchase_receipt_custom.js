frappe.ui.form.on('Purchase Receipt', {
    refresh: function(frm) {
        // Add custom button
        setTimeout(() => {
            cur_frm.remove_custom_button('Purchase Return', 'Create');
            cur_frm.remove_custom_button('Make Stock Entry', 'Create');
            cur_frm.remove_custom_button('Quality Inspection(s)', 'Create');
            cur_frm.remove_custom_button('Retention Stock Entry', 'Create');
            cur_frm.remove_custom_button('Purchase Invoice', 'Create');
            cur_frm.remove_custom_button('Purchase Invoice', 'Get Items From');
            cur_frm.remove_custom_button('Asset Movement', 'View');
            cur_frm.remove_custom_button('Asset', 'View');
            cur_frm.remove_custom_button('Accounting Ledger', 'Preview');
            cur_frm.remove_custom_button('Accounting Ledger', 'View');
            console.log("Call")
        }, 100);
        if(frm.doc.docstatus === 1){
            frm.add_custom_button(__('Create Manufacture Process'), function() {
                createManufactureProcess(frm);
            });
        }
    },
    before_save: function(frm) {
        frm.doc.items.forEach(function(item) {
            if (item.item_group === "Jumbo Bag") {
                item.warehouse = "Empty Jumbo Bag - MGSS";
            }
        });
    }
});

function createManufactureProcess(frm) {
    // Open new Manufacture Process document
    frappe.new_doc("Manufacture Process", {}, doc => {
        doc.warehouse = frm.doc.set_warehouse
        // Add items from Purchase Receipt to Manufacture Process
        frappe.model.clear_table(doc, "material_input");

        frm.doc.items.forEach(item => {
            if (item.item_group !== "Jumbo Bag") {
                let mi_item = frappe.model.add_child(doc, "material_input");
                mi_item.item = item.item_code;
                mi_item.quantity = item.qty;
            }
        });
    });
}