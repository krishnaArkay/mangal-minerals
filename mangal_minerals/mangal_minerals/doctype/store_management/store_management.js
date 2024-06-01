// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.ui.form.on("Store Management", {
	refresh(frm) {
        if (frm.is_new()) {
            frm.doc.voucher_number = ""
        }
        if (frm.doc.entry_type === "Stock In") {
            frm.set_query("entry_for", function() {
                return {
                    filters: [
                        ["name", "in", ["Material Inward", "Return"]]
                    ]
                };
            });
        }
        setPurposeFilter(frm);
	},
    entry_type(frm) {
        if (frm.doc.entry_type === "Stock Out") {
            frm.doc.entry_for = ""
        }else{
            frm.set_query("entry_for", function() {
                return {
                    filters: [
                        ["name", "in", ["Material Inward", "Return"]]
                    ]
                };
            });
        }
        setPurposeFilter(frm);
	},

});

frappe.ui.form.on('Store Management Items', {
	refresh(frm) {
		// Add any refresh logic here if needed
	},
    items_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (frm.doc.entry_type === "Stock In") {
            console.log("stock in")
            row.purpose = frm.doc.entry_for;
        }

        setPurposeQuery(frm);
    },
    item: function(frm, cdt, cdn) {
        setPurposeQuery(frm);
    }
});

function setPurposeFilter(frm) {
    let entryType = frm.doc.entry_type;
    frm.fields_dict['items'].grid.get_field('purpose').get_query = function(doc, cdt, cdn) {
        return {
            filters: [
                // Example: If entry_type is 'Stock In'
                entryType === 'Stock In' ? ['name', 'in', ['Material Inward', 'Return']] : 
                // Otherwise (if entry_type is 'Stock Out')
                ['name', 'in', ['Material Outward', 'Issued for Usage', 'Material Consumption']]
            ]
        };
    };
}

function setPurposeQuery(frm) {
    let entryType = frm.doc.entry_type;

    frm.set_query('purpose', 'items', function(doc, cdt, cdn) {
        return {
            filters: [
                // Example: If entry_type is 'Stock In'
                entryType === 'Stock In' ? ['name', 'in', ['Material Inward', 'Return']] : 
                // Otherwise (if entry_type is 'Stock Out')
                ['name', 'in', ['Material Outward', 'Issued for Usage', 'Material Consumption']]
            ]
        };
    });

    frm.refresh_field("items");
}