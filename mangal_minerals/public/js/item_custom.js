frappe.ui.form.on('Item', {
	refresh(frm) {
        console.log("Avyu")
        $('div[data-doctype="Stock Entry"]').hide()
        }
    })