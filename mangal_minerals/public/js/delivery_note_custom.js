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