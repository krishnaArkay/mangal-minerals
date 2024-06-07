// Copyright (c) 2024, Arkay Apps and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Open Order Scheduler", {
// 	refresh(frm) {
       
// 	}
// });

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
