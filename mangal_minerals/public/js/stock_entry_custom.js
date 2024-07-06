frappe.ui.form.on('Stock Entry', {
    refresh: function(frm) {
        if(!frappe.user.has_role('System Manager')){
            frappe.set_route('mangal-minerals');
        }
    }
})