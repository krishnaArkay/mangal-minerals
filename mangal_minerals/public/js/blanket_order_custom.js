frappe.ui.form.on('Blanket Order', {
    refresh: function(frm) {
        // frm.get_docfield("items").grid.allow_bulk_edit = 0;
        console.log("calll")
        // Add custom button
        $('div[data-doctype="Purchase Order"]').hide();
        $('div[data-doctype="Quotation"]').hide();
        setTimeout(() => {
            cur_frm.remove_custom_button('Quotation', 'Create');
        }, 200);
    },
    before_save(frm){
        validate_order(frm)
        total_qty(frm)
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
function total_qty(frm){
    let total_qty = 0;
        $.each(frm.doc.items || [], function(i, d) {
            total_qty += d.qty;
        });
        frm.set_value('custom_total_qty', total_qty);
}

function validate_order(frm) {
    if (frm.doc.items && frm.doc.items.length > 1) {
        frappe.throw("A Open Order can only contain one item. Please remove the extra items and try again.");
    }
}