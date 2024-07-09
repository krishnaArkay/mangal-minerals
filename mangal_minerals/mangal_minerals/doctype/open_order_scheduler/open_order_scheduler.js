// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

frappe.ui.form.on("Open Order Scheduler", {
	refresh(frm) {
        if (frappe.user.has_role('System Manager')) {
            // User has the System Manager role
            frm.set_df_property('items', 'allow_on_submit', 1)
            console.log('User has the System Manager role');
        } else {
            frm.set_df_property('items', 'allow_on_submit', 0)
            // User does not have the System Manager role
            console.log('User does not have the System Manager role');
        }
        // calculate_percentage(frm)
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

function calculate_percentage(frm) {
    if(frm.doc.docstatus !== 2){
        if (frm.doc.total_quantity > 0) {
            frm.set_value('delivered', (frm.doc.total_delivered_mt / frm.doc.total_quantity) * 100);
            frm.save('Update');
        } else {
            frm.set_value('delivered', 0);
            frm.doc.save("Update")
        }
    }
}
