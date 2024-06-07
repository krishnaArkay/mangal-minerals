frappe.ui.form.on('Purchase Receipt', {
    refresh: function(frm) {
        // Add custom button
        frm.add_custom_button(__('Create Manufacture Process'), function() {
            createManufactureProcess(frm);
        });
    }
});

function createManufactureProcess(frm) {
    // Open new Manufacture Process document
    frappe.new_doc("Manufacture Process", {}, doc => {
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