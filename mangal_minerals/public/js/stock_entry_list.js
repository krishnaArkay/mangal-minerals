frappe.listview_settings['Stock Entry'] = {
    onload: function(listview) {
        if (!frappe.user.has_role('System Manager')) {
            console.log("avyu onload")
            frappe.set_route('mangal-minerals');
        }
    },
    refresh: function(listview) {
        if (!frappe.user.has_role('System Manager')) {
            console.log("avyu refresh")
            frappe.set_route('mangal-minerals');
        }
    }
}