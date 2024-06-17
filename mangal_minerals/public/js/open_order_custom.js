frappe.ui.form.on('Blanket Order', {
	refresh(frm) {
		// your code here
	},
    before_save(frm){
        if (frm.doc.items && frm.doc.items.length > 1) {
            frappe.throw("You can only one Item in Open Order")
        }
    }
})
frappe.ui.form.on('Blanket Order Item', {
	items_add:function(frm,cdt,cdn) {
        if (frm.doc.items && frm.doc.items.length > 1) {
            frappe.throw("You can only add one item in the Open Order.");
        }
		// your code here
	}
})