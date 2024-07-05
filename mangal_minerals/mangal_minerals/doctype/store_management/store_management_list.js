frappe.listview_settings['Store Management'] = {
    formatters: {
        entry_type(val) {
            if (val == "Stock In") {
                return "<span class='indicator-pill green'>" + __(val) + "</span>";
            }else{
                return "<span class='indicator-pill red'>" + __(val) + "</span>";
            }
        }
    },
    // refresh: function(listview) {
    //     console.log("List view data:", listview.data); // Log listview data for debugging
        
    //     listview.data.forEach(function(item) {
           
    //         var $rows = $(`.list-row [data-name="${item.name}"]`).closest('.list-row');
            
    //         $rows.each(function() {
    //             if (item.entry_type === "Stock In") {
    //                 $(this).css("background-color", "#C8E6C9");
    //             } else if (item.entry_type === "Stock Out") {
    //                 $(this).css("background-color", "#FFCDD2");
    //             } 
    //         });
    //     });
        
    // }
};




