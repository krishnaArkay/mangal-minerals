frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        // Add custom button
        setTimeout(() => {
            // cur_frm.remove_custom_button('Purchase Return', 'Create');
            cur_frm.remove_custom_button('Payment Request', 'Create');
            cur_frm.remove_custom_button('Payment', 'Create');
            cur_frm.remove_custom_button('Sales Invoice', 'Create');
            cur_frm.remove_custom_button('Quotation', 'Get Items From');
            cur_frm.remove_custom_button('Pick List', 'Create');
            // cur_frm.remove_custom_button('Delivery Note', 'Create');
            cur_frm.remove_custom_button('Work Order', 'Create');
            cur_frm.remove_custom_button('Material Request', 'Create');
            cur_frm.remove_custom_button('Request for Raw Materials', 'Create');
            cur_frm.remove_custom_button('Project', 'Create');
            console.log("Call")
        }, 100);
    },
})