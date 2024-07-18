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
                        ["name", "in", ["Material Inward", "Returned"]]
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
                        ["name", "in", ["Material Inward", "Returned"]]
                    ]
                };
            });
        }
        frm.clear_table("items"); 
        frm.refresh_fields("items");
        setPurposeFilter(frm);
        
	},
    person_responsible(frm){
        frm.doc.items.forEach((item) => {
            item.person_name = frm.doc.person_responsible
        })
    },
    before_save: function(frm) {
        if (frm.doc.entry_type === "Stock Out") {
            
            // Check if any item in the grid is "Diesel"
            let dieselExists = false;
            frm.doc.items.forEach((item) => {
                if (item.item === "Diesel") {
                    if(!item.vehicle){
                        frappe.throw("Please add a vehicle number for item <b>Diesel</b> at <b>Row " + item.idx+"</b>")
                    }                 
                }
                if(!item.purpose){
                    frappe.throw("Please add a <b>Purpose</b> for item at <b>Row " + item.idx+"</b>")
                }
            });
        }
    }
});

frappe.ui.form.on('Store Management Items', {
	refresh(frm) {
		// Add any refresh logic here if needed
	},
    items_add: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (frm.doc.entry_type === "Stock In") {
            if(!frm.doc.entry_for){
                frm.clear_table("items"); 
                frm.refresh_fields("items");
                // frm.get_field('entry_for').$wrapper.find('input').focus();
                frappe.throw('<span style="color: red;">Please first select an Entry For.</span>')
            }
            console.log("stock in")
            row.purpose = frm.doc.entry_for;
        }
        if(frm.doc.person_responsible){
            row.person_name = frm.doc.person_responsible
        }

        setPurposeQuery(frm);
    },
    item: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn]
        setPurposeQuery(frm);
        if(frm.doc.entry_type === "Stock Out"){
            frappe.db.get_value('Item', row.item, 'custom_stock_out_purpose', (r) => {
                if (r && r.custom_stock_out_purpose) {
                    frappe.model.set_value(cdt, cdn, 'purpose', r.custom_stock_out_purpose);
                }
                frm.fields_dict['items'].grid.grid_rows_by_docname[cdn].toggle_reqd('purpose', true);
            });

        }
        else{
            frm.fields_dict['items'].grid.grid_rows_by_docname[cdn].toggle_reqd('purpose', false);
        }
        frappe.db.get_list('Stock Ledger Entry', {
            filters: {
                item_code: row.item,
                warehouse: frm.doc.warehouse
            },
            fields: ['qty_after_transaction'],
            order_by: 'modified desc',
            limit: 1
        }).then(r => {
            if (r.length > 0) {
                let current_stock = r[0].qty_after_transaction;
                console.log('current_stock', current_stock);
                row.current_stock = current_stock
            } else {
                row.current_stock = 0
                console.log('No stock ledger entries found');
            }
        });
    },
    quantity: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn]
        if(frm.doc.entry_type === "Stock Out"){
            if (row.current_stock <= row.quantity){
                frappe.throw(`Not enough stock: Only ${row.current_stock} available for ${row.item}.`);
            }
        }
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