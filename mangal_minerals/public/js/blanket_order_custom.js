frappe.ui.form.on('Blanket Order', {
    refresh: function(frm) {
        console.log("calll")
        // Add custom button
        $('div[data-doctype="Purchase Order"]').hide();
        $('div[data-doctype="Quotation"]').hide();
        setTimeout(() => {
            cur_frm.remove_custom_button('Quotation', 'Create');
        }, 100);
    },
    before_save(frm){
        validate_order(frm)
    }
})
frappe.ui.form.on('Blanket Order Item', {
	refresh(frm) {
		// your code here
	},
    items_add(frm,cdt,cdn){
        validate_order(frm)
    }
})
function validate_order(frm) {
    if (frm.doc.items && frm.doc.items.length > 1) {
        frappe.throw("A Open Order can only contain one item. Please remove the extra items and try again.");
    }
}