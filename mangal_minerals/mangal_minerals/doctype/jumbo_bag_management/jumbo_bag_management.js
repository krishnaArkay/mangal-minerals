// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.ui.form.on("Jumbo Bag Management", {
	refresh(frm) {
        if (frm.is_new()) {
            frm.doc.voucher_number = ""
            frm.doc.reference_doctype = ""
            frm.doc.reference_number= ""
            frm.doc.jumbo_bag_reference = ""
            frm.doc.remarks = ""
            if(frm.doc.entry_purpose === "Damage"){
                frm.set_value("warehouse","Rejected Warehouse - MGSS")
                frm.set_df_property("warehouse","read_only",1)
            }else if(frm.doc.entry_purpose === "Inward"){
                frm.set_value("warehouse","Empty Jumbo Bag - MGSS")
                frm.set_df_property("warehouse","read_only",1)
            }else{
                frm.set_value("warehouse","")
                frm.set_df_property("warehouse","read_only",0)
            }
        }
        if(frm.doc.docstatus === 1 && frm.doc.voucher_number){
            // Add a custom button for the Stock Ledger report
            frm.add_custom_button(__('Stock Ledger'), function() {
                // Open Stock Ledger report with the specified filters
                frappe.set_route('query-report', 'Stock Ledger', {
                    voucher_no: frm.doc.voucher_number,
                    from_date: frm.doc.date,
                    to_date: frm.doc.date,
                });
            });
        }
	},
    entry_purpose(frm){
        if(frm.doc.entry_purpose === "Damage"){
            frm.set_value("warehouse","Rejected Warehouse - MGSS")
            frm.set_df_property("warehouse","read_only",1)
        }else if(frm.doc.entry_purpose === "Inward"){
            frm.set_value("warehouse","Empty Jumbo Bag - MGSS")
            frm.set_df_property("warehouse","read_only",1)
        }else{
            frm.set_value("warehouse","")
            frm.set_df_property("warehouse","read_only",0)
        } 
    }
});
