frappe.listview_settings['Store Entry'] = {
    refresh: function(listview) {
        // if(!frappe.user.has_role('System Manager')){
            frappe.msgprint("Rooot")
            frappe.set_route('mangal-minerals');
        // }
    }
}