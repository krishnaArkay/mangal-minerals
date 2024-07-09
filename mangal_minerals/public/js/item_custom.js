frappe.ui.form.on('Item', {
	refresh(frm) {
        console.log("AVyu")
        $('div[data-doctype="Stock Entry"]').hide()
        }
    })