frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
        // Add custom button
        setTimeout(() => {
            // cur_frm.remove_custom_button('Purchase Return', 'Create');
            cur_frm.remove_custom_button('Payment Request', 'Create');
            cur_frm.remove_custom_button('Payment', 'Create');
            cur_frm.remove_custom_button('Purchase Invoice', 'Create');
            cur_frm.remove_custom_button('Product Bundle', 'Get Items From');
            cur_frm.remove_custom_button('Material Request', 'Get Items From');
            cur_frm.remove_custom_button('Supplier Quotation', 'Get Items From');
            cur_frm.remove_custom_button('Link to Material Request', 'Tools');
            console.log("Call")
        }, 100);
    },
})