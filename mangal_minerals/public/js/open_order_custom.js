frappe.ui.form.on('Blanket Order', {
	refresh(frm){
        console.log("Refreshhhh")
        setTimeout(() => {
            console.log("avyu")
            $("[data-doctype='Purchase Order']").parent().hide();
        }, 10);
	},
    before_save(frm){
        if (frm.doc.items && frm.doc.items.length > 1) {
            frappe.throw("You can only one Item in Open Order")
        }
    },
    customer(frm){
        console.log("Customer changed")
    }
})
frappe.ui.form.on('Blanket Order Item', {
	items_add:function(frm,cdt,cdn) {
        console.log("Item add")
        if (frm.doc.items && frm.doc.items.length > 1) {
            frappe.throw("You can only add one item in the Open Order.");
        }
		// your code here
	}
})