frappe.ui.form.on('Delivery Note', {
    refresh: function(frm) {
        console.log("hello")
        setTimeout(() => {
            cur_frm.remove_custom_button('Packing Slip', 'Create');
            cur_frm.remove_custom_button('Quality Inspection(s)', 'Create');
            cur_frm.remove_custom_button('Shipment', 'Create');
            cur_frm.remove_custom_button('Sales Return', 'Create');
            cur_frm.remove_custom_button('Delivery Trip', 'Create');
            cur_frm.remove_custom_button('Sales Invoice', 'Create');
            cur_frm.remove_custom_button('Installation Note', 'Create');
            cur_frm.remove_custom_button('Accounting Ledger', 'Preview');
            cur_frm.remove_custom_button('Accounting Ledger', 'View');
        }, 100);

    }
});

frappe.ui.form.on('Delivery Note Item', {
	refresh(frm) {
		// your code here
	},
    custom_average_mt(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        
        if (row.custom_average_mt){
            row.custom_total_mt = row.qty * row.custom_average_mt
            frm.refresh_field('items');
        }
    }
})