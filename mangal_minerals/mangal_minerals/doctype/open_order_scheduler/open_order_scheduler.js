// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.ui.form.on("Open Order Scheduler", {
	refresh(frm) {
       
	},
    open_order(frm){
        if (frm.doc.open_order) {
            frappe.call({
                method: 'mangal_minerals.mangal_minerals.doctype.api.get_items_from_blanket_order',
                args: {
                    blanket_order: frm.doc.open_order
                },
                callback: function(r) {
                    if (r.message) {
                        var item_codes = r.message;
                        frm.set_query('item', function() {
                            return {
                                filters: [
                                    ['Item', 'item_code', 'in', item_codes]
                                ]
                            };
                        });
                    }
                }
            });
        }
    }
});

frappe.ui.form.on('Open Order Scheduler Item', {
	// refresh(frm) {
	// 	// your code here
	// }
    planned_truck(frm,cdt,cdn){
        row = locals[cdt][cdn]
        console.log("table",row.planned_truck )
        row.planned_mt = row.planned_truck*frm.doc.per_truck_mt
        refresh_field('planned_mt', row.name, row.parentfield);
    },
    delivered_mt(frm,cdt,cdn){
        console.log("delive mt changed")
    }

})
