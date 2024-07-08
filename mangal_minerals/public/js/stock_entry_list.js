frappe.listview_settings['Stock Entry'] = {
    onload: function(listview) {
        if(!frappe.user.has_role('System Manager')){
            frappe.set_route('mangal-minerals');
        }
    }
}