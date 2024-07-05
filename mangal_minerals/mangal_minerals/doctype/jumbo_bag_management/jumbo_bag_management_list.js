frappe.listview_settings['Jumbo Bag Management'] = {
    formatters: {
        entry_purpose(val) {
            if (val == "Inward") {
                return "<span class='indicator-pill green'>" + __(val) + "</span>";
            }else if(val == "Filled") {
                return "<span class='indicator-pill blue'>" + __(val) + "</span>";
            }
            else if(val == "Damage") {
                return "<span class='indicator-pill orange'>" + __(val) + "</span>";
            }
            else {
                return "<span class='indicator-pill yellow'>" + __(val) + "</span>";
            }
        }
    }
};

