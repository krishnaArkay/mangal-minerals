// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.ui.form.on("Stock Transfer", {
	refresh(frm) {
        if(frm.doc.docstatus === 1){
            // Add a custom button for the Stock Ledger report
            frm.add_custom_button(__('Stock Ledger'), function() {
                // Open Stock Ledger report with the specified filters
                frappe.set_route('query-report', 'Stock Ledger', {
                    voucher_no: frm.doc.voucher_number,
                    from_date: frm.doc.date,
                    to_date: frm.doc.date,
                });
            });
        }
	},
    default_from_warehouse(frm){
        frm.doc.items.forEach(function(item) {
            item.from_warehouse = frm.doc.default_from_warehouse;
        });

        frm.refresh_field('items');
    },
    default_to_warehouse(frm){
        frm.doc.items.forEach(function(item) {
            item.to_warehouse = frm.doc.default_to_warehouse;
        });

        frm.refresh_field('items');
    },
});

frappe.ui.form.on('Stock Transfer Item', {
	refresh(frm) {
		// your code here
	},
    items_add: function(frm,cdt,cdn) {
        let row = locals[cdt][cdn];
        row.from_warehouse = frm.doc.default_from_warehouse;
        row.to_warehouse = frm.doc.default_to_warehouse;

        frm.refresh_field('items');
        
    }
})