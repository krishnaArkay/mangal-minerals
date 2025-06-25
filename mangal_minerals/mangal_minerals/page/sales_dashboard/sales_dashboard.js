
// =================================================================================================================
// ================================================= Round Chart ====================================================
// =================================================================================================================
frappe.pages['sales-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Sales Dashboard',
        single_column: true
    });

    // Applying custom styles with modern and sleek design
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            /* General Layout */
            .page-wrapper {
                background: #f8f9fa;
                font-family: 'Roboto', sans-serif;
                color: #333;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 30px;
                min-height: 100vh;
            }

            /* Filter Section */
            .filters {
                background: #ffffff;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
                padding: 25px;
                margin-bottom: 40px;
                width: 100%;
                max-width: 1100px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: box-shadow 0.3s ease;
            }

            .filters input, .filters button {
                padding: 14px 22px;
                border-radius: 10px;
                border: 1px solid #ddd;
                font-size: 16px;
                font-weight: 500;
                transition: transform 0.3s ease, background-color 0.3s ease;
            }

            .filters input {
                background-color: #f1f3f5;
                width: 230px;
            }

            .filters button {
                background-color: #ff6f61;
                color: white;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }

            .filters button:hover {
                background-color: #ff4f3f;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
                transform: translateY(-4px);
            }

            /* Sales Order Cards */
            .card-container {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
                justify-content: center;
                max-width: 1200px;
                margin-top: 60px;
                padding: 20px;
            }

            .card {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                width: 250px;
                text-align: center;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            .card:hover {
                transform: translateY(-6px);
                box-shadow: 0 16px 50px rgba(0, 0, 0, 0.2);
            }

            .card h4 {
                font-size: 20px;
                color: #444;
                font-weight: 600;
                margin-bottom: 15px;
            }

            .card p {
                font-size: 32px;
                color: #ff6f61;
                font-weight: bold;
                margin-top: 10px;
            }

            /* Sales Order Modern Table */
/* Clean and Modern Sales Order Table */
.sales-order-table {
    width: 100%;
    margin-top: 50px;
    border-collapse: collapse;
    font-family: 'Arial', sans-serif;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.sales-order-table th, .sales-order-table td {
    padding: 12px 18px;
    text-align: left;
    font-size: 14px;
    color: #444;
    border-bottom: 1px solid #f1f1f1;
    transition: background-color 0.3s ease;
}

.sales-order-table th {
    background-color: #f7f7f7 !important;
    color: #333 !important;
    font-weight: 600 !important;
}

.sales-order-table tr {
    transition: background-color 0.3s ease;
}

.sales-order-table tr:hover {
    background-color: #f4f4f4;
}

.sales-order-table td:first-child {
    font-weight: 600;
    color: #007bff;
}

.sales-order-table td {
    color: #555;
}

.sales-order-table td .view-link {
    color: #007bff;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: color 0.3s ease;
}

.sales-order-table td .view-link:hover {
    color: #0056b3;
    text-decoration: underline;
}

.sales-order-table .status {
    font-weight: 600;
    text-transform: capitalize;
    padding: 6px 12px;
    border-radius: 4px;
    text-align: center;
}

.sales-order-table .status.open {
    background-color: #f39c12;
    color: #fff;
}

.sales-order-table .status.closed {
    background-color: #27ae60;
    color: #fff;
}

.sales-order-table .status.on-hold {
    background-color: #95a5a6;
    color: #fff;
}



            /* Chart Section */
            .chart-container {
				margin-top: 70px;
				padding: 30px;
				background-color: #ffffff;
				border-radius: 15px;
				box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
				display: flex;
				justify-content: center;  /* Centers the chart horizontally */
				align-items: center;  /* Centers the chart vertically */
				margin-left: auto;  /* Centers the container within the parent */
				margin-right: auto;
            }

            .chart-container canvas {
                width: 100%;
                height: 550px !important;
                border-radius: 12px;
                border: 1px solid #ddd;
				
            }

            /* No Data Message */
            .no-data-message {
                font-size: 18px;
                color: #e74c3c;
                font-weight: bold;
                margin-top: 50px;
                display: none;
                text-align: center;
            }
        `)
        .appendTo('head');

    // Filters and Dashboard Content
    var filters_div = $('<div class="filters"></div>').appendTo(page.main);
    var start_date_input = $('<input type="date" class="start-date" />').appendTo(filters_div);
    var end_date_input = $('<input type="date" class="end-date" />').appendTo(filters_div);
    var filter_button = $('<button>Apply Filters</button>').appendTo(filters_div);

    var card_container = $('<div class="card-container"></div>').appendTo(page.main);
    var chart_container = $('<div class="chart-container"></div>').appendTo(page.main);
    var sales_order_list_container = $('<div class="sales-order-list"></div>').appendTo(page.main);
    var no_data_message = $('<div class="no-data-message">No data found for the selected period.</div>').appendTo(page.main);

    // Create the chart canvas element
    $('<canvas id="salesOrderChart"></canvas>').appendTo(chart_container);

    // Fetch Sales Order Data
    function fetch_sales_orders_data(start_date = '', end_date = '') {
        var filters = {};
        if (start_date && end_date) {
            filters['transaction_date'] = ['between', [start_date, end_date]];
        }

        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Sales Order',
                filters: filters,
                fields: ['name', 'status', 'customer', 'transaction_date', 'total'],
            },
            callback: function(response) {
                var status_count = {};

                response.message.forEach(function(order) {
                    if (!status_count[order.status]) {
                        status_count[order.status] = 0;
                    }
                    status_count[order.status]++;
                });

                update_sales_order_cards(status_count);
                update_sales_order_chart(status_count);
                update_sales_order_list(response.message);

                if (response.message.length === 0) {
                    no_data_message.show();
                } else {
                    no_data_message.hide();
                }
            }
        });
    }

    // Update Sales Order Cards
    function update_sales_order_cards(status_count) {
        card_container.empty();

        for (var status in status_count) {
            var card = $('<div class="card"></div>').appendTo(card_container);
            $('<h4></h4>').text(status).appendTo(card);
            $('<p></p>').text(status_count[status]).appendTo(card);
        }
    }

    // Create Chart
    function update_sales_order_chart(status_count) {
        if (typeof Chart === 'undefined') {
            var script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            script.onload = function() {
                create_chart(status_count);
            };
            document.head.appendChild(script);
        } else {
            create_chart(status_count);
        }
    }

    function create_chart(status_count) {
        if (window.salesOrderChart && window.salesOrderChart.destroy) {
            window.salesOrderChart.destroy();
        }

        var ctx = document.getElementById('salesOrderChart').getContext('2d');
        window.salesOrderChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(status_count),
                datasets: [{
                    label: 'Sales Orders by Status',
                    data: Object.values(status_count),
                    backgroundColor: ['#FF6347', '#FFD700', '#32CD32', '#1E90FF', '#9370DB'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                },
            }
        });
    }

   
function update_sales_order_list(orders) {
    sales_order_list_container.empty();

    // Create table element
    var table = $('<table class="sales-order-table"></table>').appendTo(sales_order_list_container);

    // Add table header
    var header_row = $('<tr></tr>').appendTo(table);
    $('<th></th>').text('Order #').appendTo(header_row);
    $('<th></th>').text('Customer').appendTo(header_row);
    $('<th></th>').text('Date').appendTo(header_row);
    $('<th></th>').text('Total').appendTo(header_row);
    $('<th></th>').text('Status').appendTo(header_row); // Status column
    $('<th></th>').text('Details').appendTo(header_row);

    // Add table rows with dynamic order data
    orders.forEach(function(order) {
        var row = $('<tr></tr>').appendTo(table);

        // Order number with emphasis
        $('<td></td>').text(order.name).appendTo(row);

        // Customer and other details
        $('<td></td>').text(order.customer).appendTo(row);
        $('<td></td>').text(order.transaction_date).appendTo(row);
        $('<td></td>').text(order.total).appendTo(row);

        // Status Column with class
        var status_class = '';
        if (order.status === 'Open') {
            status_class = 'open';
        } else if (order.status === 'Closed') {
            status_class = 'closed';
        } else if (order.status === 'On Hold') {
            status_class = 'on-hold';
        }
        $('<td class="status ' + status_class + '"></td>').text(order.status).appendTo(row);

        // View link for details
        var details_link = $('<a class="view-link">View Details</a>').appendTo($('<td></td>').appendTo(row));
        // details_link.find('.view-details').on('click', function() {
        //     frappe.set_route('Form', 'Sales Order', order.name);
        // });
        // On click for "View Details"
        details_link.on('click', function() {
            frappe.set_route('Form', 'Sales Order', order.name);
            console.log('Viewing details for Order:', order.name);
        });
    });
}





    // Apply Filters
    filter_button.on('click', function() {
        fetch_sales_orders_data(start_date_input.val(), end_date_input.val());
    });

    // Initial Load
    fetch_sales_orders_data();
}

// =================================================================================================================
// ================================================= DARK THEME ====================================================
// =================================================================================================================
// frappe.pages['sales-dashboard'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Sales Dashboard',
//         single_column: true
//     });

//     // Apply totally different style
//     $('<style>')
//         .prop('type', 'text/css')
//         .html(`
//             /* Global Page Layout */
//             .page-wrapper {
//                 background-color: #2e3b4e;
//                 color: #fff;
//                 font-family: 'Helvetica Neue', Arial, sans-serif;
//                 padding: 20px;
//                 display: flex;
//                 flex-direction: column;
//                 align-items: center;
//                 justify-content: flex-start;
//                 min-height: 100vh;
//             }

//             /* Filters Section */
//             .filters {
//                 display: flex;
//                 justify-content: center;
//                 align-items: center;
//                 background: #3a4d69;
//                 border-radius: 12px;
//                 padding: 20px;
//                 margin-bottom: 30px;
//                 width: 100%;
//                 max-width: 1400px;
//             }

//             .filters input,
//             .filters button {
//                 padding: 12px 20px;
//                 font-size: 14px;
//                 border-radius: 8px;
//                 border: none;
//                 margin: 0 15px;
//                 outline: none;
//                 width: 200px;
//                 color: #fff;
//                 background-color: #4b6177;
//                 transition: all 0.2s ease;
//             }

//             .filters input::placeholder {
//                 color: #ccc;
//             }

//             .filters button {
//                 background: #1f8ee9;
//                 color: white;
//                 cursor: pointer;
//                 font-weight: bold;
//             }

//             .filters button:hover {
//                 background: #226fb1;
//             }

//             /* Dashboard Cards */
//             .card-container {
//                 display: flex;
//                 justify-content: center;
//                 gap: 30px;
//                 width: 100%;
//                 max-width: 1300px;
//                 flex-wrap: wrap;
//                 margin-top: 50px;
//             }

//             .card {
//                 background: #374f6b;
//                 border-radius: 15px;
//                 padding: 25px;
//                 text-align: center;
//                 width: 200px;
//                 height: 180px;
//                 display: flex;
//                 flex-direction: column;
//                 justify-content: center;
//                 box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.2);
//                 cursor: pointer;
//                 transition: transform 0.3s ease, box-shadow 0.3s ease;
//             }

//             .card:hover {
//                 transform: translateY(-8px);
//                 box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.4);
//             }

//             .card h4 {
//                 font-size: 20px;
//                 font-weight: 600;
//                 color: #f1f1f1;
//                 margin-bottom: 10px;
//             }

//             .card p {
//                 font-size: 24px;
//                 color: #62d6e8;
//                 font-weight: bold;
//             }

//             /* Sales Order List */
//             .sales-order-list {
//                 margin-top: 40px;
//                 width: 100%;
//                 max-width: 1300px;
//             }

//             .sales-order-item {
//                 background: #3b4f6b;
//                 padding: 20px;
//                 border-radius: 12px;
//                 margin-bottom: 20px;
//                 display: flex;
//                 justify-content: space-between;
//                 align-items: center;
//                 box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
//             }

//             .sales-order-item h5 {
//                 font-size: 18px;
//                 font-weight: 600;
//                 color: #fff;
//             }

//             .sales-order-item p {
//                 font-size: 14px;
//                 color: #b0b0b0;
//             }

//             .sales-order-item .details-link {
//                 font-size: 14px;
//                 font-weight: 600;
//                 color: #1e90ff;
//                 cursor: pointer;
//                 text-align: right;
//                 transition: color 0.3s;
//             }

//             .sales-order-item .details-link:hover {
//                 color: #87cefa;
//             }

//             /* Chart Section */
//             .chart-container {
//                 width: 100%;
//                 max-width: 1200px;
//                 margin-top: 40px;
//                 padding: 30px;
//                 background: #2e3b4e;
//                 border-radius: 10px;
//                 box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
//             }

//             /* No Data Message */
//             .no-data-message {
//                 font-size: 18px;
//                 color: #ff6f61;
//                 font-weight: bold;
//                 display: none;
//                 text-align: center;
//                 margin-top: 40px;
//             }
//         `)
//         .appendTo('head');

//     // Filters Section
//     var filters_div = $('<div class="filters"></div>').appendTo(page.main);
//     var start_date_input = $('<input type="date" class="start-date" />').appendTo(filters_div);
//     var end_date_input = $('<input type="date" class="end-date" />').appendTo(filters_div);
//     var filter_button = $('<button>Apply Filters</button>').appendTo(filters_div);

//     var card_container = $('<div class="card-container"></div>').appendTo(page.main);
//     var chart_container = $('<div class="chart-container"></div>').appendTo(page.main);
//     var sales_order_list_container = $('<div class="sales-order-list"></div>').appendTo(page.main);
//     var no_data_message = $('<div class="no-data-message">No data found for the selected period.</div>').appendTo(page.main);

//     // Create the chart canvas element
//     $('<canvas id="salesOrderChart"></canvas>').appendTo(chart_container);

//     // Fetch Sales Order Data
//     function fetch_sales_orders_data(start_date = '', end_date = '') {
//         var filters = {};
//         if (start_date && end_date) {
//             filters['transaction_date'] = ['between', [start_date, end_date]];
//         }

//         frappe.call({
//             method: 'frappe.client.get_list',
//             args: {
//                 doctype: 'Sales Order',
//                 filters: filters,
//                 fields: ['name', 'status', 'customer', 'transaction_date', 'total'],
//             },
//             callback: function(response) {
//                 var status_count = {};

//                 response.message.forEach(function(order) {
//                     if (!status_count[order.status]) {
//                         status_count[order.status] = 0;
//                     }
//                     status_count[order.status]++;
//                 });

//                 update_sales_order_cards(status_count);
//                 update_sales_order_chart(status_count);
//                 update_sales_order_list(response.message);

//                 if (response.message.length === 0) {
//                     no_data_message.show();
//                 } else {
//                     no_data_message.hide();
//                 }
//             }
//         });
//     }

//     // Update Sales Order Cards
//     function update_sales_order_cards(status_count) {
//         card_container.empty();

//         for (var status in status_count) {
//             var card = $('<div class="card"></div>').appendTo(card_container);
//             $('<h4></h4>').text(status).appendTo(card);
//             $('<p></p>').text(status_count[status]).appendTo(card);
//         }
//     }

//     // Create Chart
//     function update_sales_order_chart(status_count) {
//         if (typeof Chart === 'undefined') {
//             var script = document.createElement('script');
//             script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
//             script.onload = function() {
//                 create_chart(status_count);
//             };
//             document.head.appendChild(script);
//         } else {
//             create_chart(status_count);
//         }
//     }

//     function create_chart(status_count) {
//         if (window.salesOrderChart && window.salesOrderChart.destroy) {
//             window.salesOrderChart.destroy();
//         }

//         var ctx = document.getElementById('salesOrderChart').getContext('2d');
//         window.salesOrderChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: Object.keys(status_count),
//                 datasets: [{
//                     label: 'Sales Orders by Status',
//                     data: Object.values(status_count),
//                     backgroundColor: ['#FF6347', '#FFD700', '#32CD32', '#1E90FF', '#9370DB'],
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     }

//     // Update Sales Order List
//     function update_sales_order_list(orders) {
//         sales_order_list_container.empty();

//         orders.forEach(function(order) {
//             var order_item = $('<div class="sales-order-item"></div>').appendTo(sales_order_list_container);
//             $('<h5></h5>').text(order.name).appendTo(order_item);
//             $('<p></p>').text('Customer: ' + order.customer).appendTo(order_item);
//             $('<p></p>').text('Status: ' + order.status).appendTo(order_item);
//             $('<p></p>').text('Total: ' + order.total).appendTo(order_item);
//             $('<p></p>').text('Date: ' + order.transaction_date).appendTo(order_item);
//             $('<div class="details-link">View Details</div>').appendTo(order_item).on('click', function() {
//                 frappe.set_route('Form', 'Sales Order', order.name);
//             });
//         });
//     }

//     // Trigger Fetch on Filter Apply
//     filter_button.on('click', function() {
//         var start_date = start_date_input.val();
//         var end_date = end_date_input.val();
//         fetch_sales_orders_data(start_date, end_date);
//     });

//     // Initial Data Load
//     fetch_sales_orders_data();
// };

// =================================================================================================================
// =================================================================================================================
// =================================================================================================================

// frappe.pages['sales-dashboard'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Sales Dashboard',
//         single_column: true
//     });

//     // Apply custom style for an impressive design
//     $('<style>')
//         .prop('type', 'text/css')
//         .html(`
//             /* High-end page background */
//             .page-wrapper {
//                 background-color: #f8f8f8;
//                 font-family: 'Roboto', sans-serif;
//                 color: #333;
//                 padding: 40px;
//                 display: flex;
//                 flex-direction: column;
//                 align-items: center;
//                 justify-content: flex-start;
//             }

//             /* Filters Container */
//             .filters {
//                 display: flex;
//                 justify-content: flex-start;
//                 align-items: center;
//                 width: 100%;
//                 max-width: 1100px;
//                 margin-bottom: 40px;
//                 background: #fff;
//                 border-radius: 10px;
//                 padding: 20px;
//                 box-shadow: 0 12px 24px rgba(0, 0, 0, 0.05);
//             }

//             .filters input,
//             .filters button {
//                 padding: 12px 20px;
//                 font-size: 16px;
//                 font-weight: 500;
//                 border-radius: 8px;
//                 border: 1px solid #ddd;
//                 transition: all 0.3s ease;
//             }

//             .filters input {
//                 width: 25%;
//                 margin-right: 20px;
//                 background: #f0f4f8;
//             }

//             .filters button {
//                 background-color: #0066cc;
//                 color: white;
//                 font-weight: bold;
//                 cursor: pointer;
//                 transition: background-color 0.3s ease, box-shadow 0.3s ease;
//             }

//             .filters button:hover {
//                 background-color: #005bb5;
//                 box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
//             }

//             /* Card Container for stats */
//             .card-container {
//                 display: flex;
//                 justify-content: center;
//                 gap: 30px;
//                 width: 100%;
//                 max-width: 1100px;
//                 margin-top: 50px;
//                 flex-wrap: wrap;
//             }

//             .card {
//                 background-color: #fff;
//                 padding: 30px;
//                 border-radius: 20px;
//                 box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
//                 width: 250px;
//                 text-align: center;
//                 transition: transform 0.3s ease, box-shadow 0.3s ease;
//                 height: 200px;
//                 display: flex;
//                 flex-direction: column;
//                 justify-content: space-between;
//             }

//             .card:hover {
//                 transform: translateY(-8px);
//                 box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
//             }

//             .card h4 {
//                 font-size: 22px;
//                 color: #222;
//                 font-weight: 600;
//                 margin-bottom: 12px;
//             }

//             .card p {
//                 font-size: 36px;
//                 color: #0066cc;
//                 font-weight: bold;
//             }

//             /* Chart Section Styling */
//             .chart-container {
//                 width: 100%;
//                 max-width: 950px;
//                 margin: 60px auto;
//             }

//             .chart-container canvas {
//                 width: 100%;
//                 height: 400px;
//                 border-radius: 12px;
//                 border: 1px solid #ddd;
//             }

//             /* Sales Order List */
//             .sales-order-list {
//                 display: flex;
//                 flex-direction: column;
//                 gap: 20px;
//                 margin-top: 60px;
//                 width: 100%;
//                 max-width: 1100px;
//             }

//             .sales-order-item {
//                 background-color: #fff;
//                 padding: 25px;
//                 border-radius: 20px;
//                 box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
//                 transition: transform 0.3s ease, box-shadow 0.3s ease;
//             }

//             .sales-order-item:hover {
//                 transform: translateY(-6px);
//                 box-shadow: 0 16px 50px rgba(0, 0, 0, 0.1);
//             }

//             .sales-order-item h5 {
//                 font-size: 18px;
//                 color: #333;
//                 font-weight: 600;
//                 margin-bottom: 10px;
//             }

//             .sales-order-item p {
//                 font-size: 14px;
//                 color: #777;
//             }

//             .sales-order-item .details-link {
//                 font-size: 14px;
//                 font-weight: 600;
//                 color: #0066cc;
//                 cursor: pointer;
//                 text-align: right;
//                 margin-top: 15px;
//             }

//             .sales-order-item .details-link:hover {
//                 color: #005bb5;
//             }

//             /* No Data Message */
//             .no-data-message {
//                 font-size: 18px;
//                 color: #e74c3c;
//                 font-weight: bold;
//                 margin-top: 50px;
//                 display: none;
//                 text-align: center;
//             }
//         `)
//         .appendTo('head');

//     // Filters and Dashboard Content
//     var filters_div = $('<div class="filters"></div>').appendTo(page.main);
//     var start_date_input = $('<input type="date" class="start-date" />').appendTo(filters_div);
//     var end_date_input = $('<input type="date" class="end-date" />').appendTo(filters_div);
//     var filter_button = $('<button>Apply Filters</button>').appendTo(filters_div);

//     var card_container = $('<div class="card-container"></div>').appendTo(page.main);
//     var chart_container = $('<div class="chart-container"></div>').appendTo(page.main);
//     var sales_order_list_container = $('<div class="sales-order-list"></div>').appendTo(page.main);
//     var no_data_message = $('<div class="no-data-message">No data found for the selected period.</div>').appendTo(page.main);

//     // Create the chart canvas element
//     $('<canvas id="salesOrderChart"></canvas>').appendTo(chart_container);

//     // Fetch Sales Order Data
//     function fetch_sales_orders_data(start_date = '', end_date = '') {
//         var filters = {};
//         if (start_date && end_date) {
//             filters['transaction_date'] = ['between', [start_date, end_date]];
//         }

//         frappe.call({
//             method: 'frappe.client.get_list',
//             args: {
//                 doctype: 'Sales Order',
//                 filters: filters,
//                 fields: ['name', 'status', 'customer', 'transaction_date', 'total'],
//             },
//             callback: function(response) {
//                 var status_count = {};

//                 response.message.forEach(function(order) {
//                     if (!status_count[order.status]) {
//                         status_count[order.status] = 0;
//                     }
//                     status_count[order.status]++;
//                 });

//                 update_sales_order_cards(status_count);
//                 update_sales_order_chart(status_count);
//                 update_sales_order_list(response.message);

//                 if (response.message.length === 0) {
//                     no_data_message.show();
//                 } else {
//                     no_data_message.hide();
//                 }
//             }
//         });
//     }

//     // Update Sales Order Cards
//     function update_sales_order_cards(status_count) {
//         card_container.empty();

//         for (var status in status_count) {
//             var card = $('<div class="card"></div>').appendTo(card_container);
//             $('<h4></h4>').text(status).appendTo(card);
//             $('<p></p>').text(status_count[status]).appendTo(card);
//         }
//     }

//     // Create Chart
//     function update_sales_order_chart(status_count) {
//         if (typeof Chart === 'undefined') {
//             var script = document.createElement('script');
//             script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
//             script.onload = function() {
//                 create_chart(status_count);
//             };
//             document.head.appendChild(script);
//         } else {
//             create_chart(status_count);
//         }
//     }

//     function create_chart(status_count) {
//         if (window.salesOrderChart && window.salesOrderChart.destroy) {
//             window.salesOrderChart.destroy();
//         }

//         var ctx = document.getElementById('salesOrderChart').getContext('2d');
//         window.salesOrderChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: Object.keys(status_count),
//                 datasets: [{
//                     label: 'Sales Orders by Status',
//                     data: Object.values(status_count),
//                     backgroundColor: ['#FF6347', '#FFD700', '#32CD32', '#1E90FF', '#9370DB'],
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     }

//     // Update Sales Order List
//     function update_sales_order_list(orders) {
//         sales_order_list_container.empty();

//         orders.forEach(function(order) {
//             var order_item = $('<div class="sales-order-item"></div>').appendTo(sales_order_list_container);
//             $('<h5></h5>').text(order.name).appendTo(order_item);
//             $('<p></p>').text('Customer: ' + order.customer).appendTo(order_item);
//             $('<p></p>').text('Status: ' + order.status).appendTo(order_item);
//             $('<p></p>').text('Total: ' + order.total).appendTo(order_item);
//             $('<p></p>').text('Date: ' + order.transaction_date).appendTo(order_item);
//             $('<div class="details-link">View Details</div>').appendTo(order_item).on('click', function() {
//                 frappe.set_route('Form', 'Sales Order', order.name);
//             });
//         });
//     }

//     // Trigger Fetch on Filter Apply
//     filter_button.on('click', function() {
//         var start_date = start_date_input.val();
//         var end_date = end_date_input.val();
//         fetch_sales_orders_data(start_date, end_date);
//     });

//     // Initial Data Load
//     fetch_sales_orders_data();
// };





// frappe.pages['sales-dashboard'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Sales Dashboard',
//         single_column: true
//     });

//     // Add custom CSS for a polished and modern look
//     $('<style>')
//         .prop('type', 'text/css')
//         .html(`
//             /* Global Styles */
//             body {
//                 background-color: #f4f7fc;
//                 font-family: 'Arial', sans-serif;
//                 color: #4d4d4d;
//                 margin: 0;
//                 padding: 0;
//             }

//             /* Page Container */
//             .sales-dashboard-container {
//                 padding: 30px;
//                 max-width: 1200px;
//                 margin: 0 auto;
//                 background-color: white;
//                 border-radius: 8px;
//                 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
//             }

//             /* Header */
//             .page-header {
//                 text-align: center;
//                 margin-bottom: 40px;
//             }

//             .page-header h1 {
//                 font-size: 28px;
//                 font-weight: 700;
//                 color: #333;
//                 margin: 0;
//             }

//             .page-header p {
//                 font-size: 18px;
//                 color: #777;
//             }

//             /* Filter Section */
//             .filters {
//                 display: flex;
//                 justify-content: space-between;
//                 gap: 20px;
//                 margin-bottom: 30px;
//             }

//             .filters input, .filters button {
//                 padding: 12px 20px;
//                 font-size: 14px;
//                 border-radius: 8px;
//                 border: 1px solid #ddd;
//                 transition: all 0.3s ease;
//             }

//             .filters input:focus, .filters button:focus {
//                 outline: none;
//                 border-color: #0056b3;
//                 box-shadow: 0 0 5px rgba(0, 86, 179, 0.3);
//             }

//             .filters button {
//                 background-color: #007bff;
//                 color: white;
//                 font-weight: 600;
//                 cursor: pointer;
//             }

//             .filters button:hover {
//                 background-color: #0056b3;
//             }

//             /* Cards Section */
//             .card-container {
//                 display: flex;
//                 gap: 30px;
//                 flex-wrap: wrap;
//                 justify-content: space-between;
//                 margin-bottom: 40px;
//             }

//             .card {
//                 background-color: #fff;
//                 padding: 25px;
//                 border-radius: 12px;
//                 box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
//                 flex: 1 1 300px;
//                 text-align: center;
//                 transition: all 0.3s ease;
//             }

//             .card:hover {
//                 box-shadow: 0 12px 25px rgba(0, 0, 0, 0.1);
//                 transform: translateY(-5px);
//             }

//             .card h4 {
//                 font-size: 22px;
//                 color: #333;
//                 margin-bottom: 10px;
//             }

//             .card p {
//                 font-size: 16px;
//                 color: #777;
//             }

//             .card .status-count {
//                 font-size: 30px;
//                 color: #007bff;
//                 font-weight: 700;
//                 margin-top: 10px;
//             }

//             /* Chart Section */
//             .chart-container {
//                 margin-bottom: 40px;
//             }

//             .chart-container canvas {
//                 border-radius: 12px;
//                 box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
//             }

//             /* No Data Message */
//             .no-data-message {
//                 font-size: 20px;
//                 color: #ff6347;
//                 text-align: center;
//                 display: none;
//                 font-weight: bold;
//             }

//             /* Sales Orders List Section */
//             .sales-order-list-container {
//                 background-color: #fff;
//                 padding: 25px;
//                 border-radius: 12px;
//                 box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
//             }

//             .sales-order-list-container h3 {
//                 text-align: center;
//                 font-size: 22px;
//                 color: #333;
//                 margin-bottom: 25px;
//             }

//             .sales-order-card {
//                 display: flex;
//                 justify-content: space-between;
//                 background-color: #f9f9f9;
//                 padding: 15px;
//                 margin-bottom: 15px;
//                 border-radius: 8px;
//                 box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
//                 transition: all 0.3s ease;
//             }

//             .sales-order-card:hover {
//                 box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
//                 transform: translateY(-5px);
//             }

//             .sales-order-card .details {
//                 display: flex;
//                 align-items: center;
//                 justify-content: space-between;
//                 width: 100%;
//             }

//             .sales-order-card .details div {
//                 flex: 1;
//                 font-size: 14px;
//                 color: #666;
//             }

//             .sales-order-card .view-details {
//                 font-size: 14px;
//                 color: #007bff;
//                 cursor: pointer;
//                 text-decoration: underline;
//                 transition: color 0.3s ease;
//             }

//             .sales-order-card .view-details:hover {
//                 color: #0056b3;
//             }

//             /* Responsive Adjustments */
//             @media (max-width: 768px) {
//                 .filters {
//                     flex-direction: column;
//                 }

//                 .card-container {
//                     flex-direction: column;
//                 }
//             }
//         `)
//         .appendTo('head');

//     // Page Wrapper
//     var container = $('<div class="sales-dashboard-container"></div>').appendTo(page.main);

//     // Header
//     var header = $('<div class="page-header"></div>').appendTo(container);
//     $('<h1>Sales Dashboard</h1>').appendTo(header);
//     $('<p>Monitor and manage your sales data efficiently</p>').appendTo(header);

//     // Filters Section
//     var filters_div = $('<div class="filters"></div>').appendTo(container);
//     var start_date_input = $('<input type="date" class="start-date" />').appendTo(filters_div);
//     var end_date_input = $('<input type="date" class="end-date" />').appendTo(filters_div);
//     var filter_button = $('<button>Apply Filters</button>').appendTo(filters_div);

//     // Cards Section
//     var card_container = $('<div class="card-container"></div>').appendTo(container);

//     // Chart Section
//     var chart_container = $('<div class="chart-container"></div>').appendTo(container);
//     var sales_order_chart_div = $('<canvas id="salesOrderChart" width="400" height="200"></canvas>').appendTo(chart_container);

//     // No Data Message
//     var no_data_message = $('<div class="no-data-message">No data found for the selected period.</div>').appendTo(container);

//     // Sales Order List Section
//     var sales_order_list_container = $('<div class="sales-order-list-container"></div>').appendTo(container);
//     var list_header = $('<h3>Sales Orders List</h3>').appendTo(sales_order_list_container);

//     // Function to fetch sales order data
//     function fetch_sales_orders_data(start_date = '', end_date = '') {
//         var filters = {};
//         if (start_date && end_date) {
//             filters['transaction_date'] = ['between', [start_date, end_date]];
//         }

//         frappe.call({
//             method: 'frappe.client.get_list',
//             args: {
//                 doctype: 'Sales Order',
//                 filters: filters,
//                 fields: ['name', 'status', 'customer', 'transaction_date', 'total'],
//             },
//             callback: function(response) {
//                 var status_count = {};

//                 response.message.forEach(function(order) {
//                     if (!status_count[order.status]) {
//                         status_count[order.status] = 0;
//                     }
//                     status_count[order.status]++;
//                 });

//                 // Update cards with status counts
//                 update_sales_order_cards(status_count);

//                 // Update chart
//                 update_sales_order_chart(status_count);

//                 // Update sales order list
//                 update_sales_order_list(response.message);

//                 // Show/hide no data message
//                 if (response.message.length === 0) {
//                     no_data_message.show();
//                 } else {
//                     no_data_message.hide();
//                 }
//             }
//         });
//     }

//     // Update cards with status counts
//     function update_sales_order_cards(status_count) {
//         card_container.empty();
//         for (var status in status_count) {
//             var card = $('<div class="card"></div>').appendTo(card_container);
//             $('<h4>' + status + '</h4>').appendTo(card);
//             $('<p>Total Orders</p>').appendTo(card);
//             $('<p class="status-count"></p>').text(status_count[status]).appendTo(card);
//         }
//     }

//     // Update chart
//     function update_sales_order_chart(status_count) {
//         if (typeof Chart === 'undefined') {
//             var script = document.createElement('script');
//             script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
//             script.onload = function() {
//                 create_chart(status_count);
//             };
//             document.head.appendChild(script);
//         } else {
//             create_chart(status_count);
//         }
//     }

//     // Create the chart
//     function create_chart(status_count) {
//         if (window.salesOrderChart && window.salesOrderChart.destroy) {
//             window.salesOrderChart.destroy();
//         }

//         var ctx = document.getElementById('salesOrderChart').getContext('2d');
//         window.salesOrderChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: Object.keys(status_count),
//                 datasets: [{
//                     label: 'Sales Orders by Status',
//                     data: Object.values(status_count),
//                     backgroundColor: generate_colors(Object.keys(status_count).length),
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     }

//     // Generate color palette for chart
//     function generate_colors(count) {
//         const colors = [];
//         const colorPalette = ['#FF6347', '#FFD700', '#32CD32', '#1E90FF', '#9370DB', '#FF4500', '#DA70D6'];
//         for (let i = 0; i < count; i++) {
//             colors.push(colorPalette[i % colorPalette.length]);
//         }
//         return colors;
//     }

//     // Update sales order list with cards
//     function update_sales_order_list(orders) {
//         sales_order_list_container.empty(); // Clear existing list

//         orders.forEach(function(order) {
//             var order_card = $('<div class="sales-order-card"></div>').appendTo(sales_order_list_container);
//             var details_div = $('<div class="details"></div>').appendTo(order_card);
//             $('<div>' + order.name + '</div>').appendTo(details_div);
//             $('<div>' + order.customer + '</div>').appendTo(details_div);
//             $('<div>' + order.transaction_date + '</div>').appendTo(details_div);
//             $('<div>' + order.total + '</div>').appendTo(details_div);
//             var view_details_link = $('<span class="view-details">View Details</span>').appendTo(details_div);

//             view_details_link.on('click', function() {
//                 frappe.set_route('Form', 'Sales Order', order.name);
//             });
//         });
//     }

//     // Initial data fetch
//     fetch_sales_orders_data();

//     // Apply filters
//     filter_button.on('click', function() {
//         var start_date = start_date_input.val();
//         var end_date = end_date_input.val();
//         fetch_sales_orders_data(start_date, end_date);
//     });
// };



//  =======================================================================================================================
//  =======================================================================================================================
//  =======================================================================================================================


// frappe.pages['sales-dashboard'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Sales Dashboard',
//         single_column: true
//     });

//     // Add custom CSS for a more impressive design
//     $('<style>')
//         .prop('type', 'text/css')
//         .html(`
//             .filters {
//                 margin-top: 20px;
//                 display: flex;
//                 gap: 15px;
//                 justify-content: flex-start;
//                 margin-bottom: 40px;
//             }

//             .filters input, .filters button {
//                 padding: 12px 18px;
//                 font-size: 15px;
//                 border-radius: 5px;
//                 border: 1px solid #ccc;
//                 box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
//             }

//             .filters button {
//                 background-color: #007bff;
//                 color: white;
//                 font-weight: 600;
//                 cursor: pointer;
//                 transition: background-color 0.3s ease;
//             }

//             .filters button:hover {
//                 background-color: #0056b3;
//             }

//             .filters input {
//                 width: 180px;
//                 border-color: #007bff;
//             }

//             .card-container {
//                 display: flex;
//                 gap: 20px;
//                 margin-top: 20px;
//                 flex-wrap: wrap;
//                 justify-content: space-between;
//                 transition: transform 0.3s ease;
//             }

//             .card {
//                 background-color: #fff;
//                 padding: 25px;
//                 border-radius: 10px;
//                 box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
//                 flex: 1 1 240px; 
//                 text-align: center;
//                 transition: transform 0.3s ease, box-shadow 0.3s ease;
//             }

//             .card:hover {
//                 transform: translateY(-10px);
//                 box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.15);
//             }

//             .card h4 {
//                 margin-bottom: 12px;
//                 font-size: 18px;
//                 font-weight: 600;
//                 color: #333;
//             }

//             .card p {
//                 font-size: 16px;
//                 color: #555;
//             }

//             .card .status-count {
//                 font-size: 22px;
//                 font-weight: bold;
//                 color: #007bff;
//             }

//             .chart-container {
//                 margin: 30px 0;
//                 padding: 20px;
//                 background-color: #fff;
//                 border-radius: 8px;
//                 box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
//             }

//             .no-data-message {
//                 font-size: 20px;
//                 color: #ff6347;
//                 text-align: center;
//                 display: none;
//                 font-weight: bold;
//             }

//             .sales-order-table {
//                 width: 100%;
//                 border-collapse: collapse;
//                 margin-top: 40px;
//                 background-color: #fff;
//                 border-radius: 8px;
//                 box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
//             }

//             .sales-order-table th, .sales-order-table td {
//                 padding: 14px 20px;
//                 text-align: left;
//                 border: 1px solid #ddd;
//             }

//             .sales-order-table th {
//                 background-color: #f1f1f1;
//                 color: #333;
//             }

//             .sales-order-table td {
//                 background-color: #fff;
//                 color: #555;
//             }

//             .sales-order-table tr:nth-child(even) {
//                 background-color: #f9f9f9;
//             }

//             .sales-order-table td .view-details {
//                 color: #007bff;
//                 cursor: pointer;
//                 font-weight: 600;
//                 text-decoration: none;
//                 transition: color 0.3s ease;
//             }

//             .sales-order-table td .view-details:hover {
//                 color: #0056b3;
//             }

//             /* Responsive adjustments */
//             @media (max-width: 768px) {
//                 .filters {
//                     flex-direction: column;
//                     align-items: stretch;
//                 }

//                 .card-container {
//                     flex-direction: column;
//                     align-items: stretch;
//                 }

//                 .card {
//                     margin-bottom: 15px;
//                 }
//             }
//         `)
//         .appendTo('head');

//     // Divs for chart and data
//     var filters_div = $('<div class="filters"></div>').appendTo(page.main);
//     var start_date_input = $('<input type="date" class="start-date" />').appendTo(filters_div);
//     var end_date_input = $('<input type="date" class="end-date" />').appendTo(filters_div);
//     var filter_button = $('<button>Apply Filters</button>').appendTo(filters_div);

//     var chart_container = $('<div class="chart-container"></div>').appendTo(page.main);
//     var sales_order_chart_div = $('<canvas id="salesOrderChart" width="400" height="200"></canvas>').appendTo(chart_container);

//     var card_container = $('<div class="card-container"></div>').appendTo(page.main);
//     var no_data_message = $('<div class="no-data-message">No data found for the selected period.</div>').appendTo(page.main);

//     var sales_order_table_container = $('<div class="sales-order-table-container"></div>').appendTo(page.main);
//     var sales_order_table = $('<table class="sales-order-table"></table>').appendTo(sales_order_table_container);
//     var table_header = $('<thead><tr><th>Order Name</th><th>Status</th><th>Customer</th><th>Transaction Date</th><th>Total Amount</th><th>Details</th></tr></thead>').appendTo(sales_order_table);
//     var table_body = $('<tbody></tbody>').appendTo(sales_order_table);

//     // Function to fetch sales orders data
//     function fetch_sales_orders_data(start_date = '', end_date = '') {
//         var filters = {};
//         if (start_date && end_date) {
//             filters['transaction_date'] = ['between', [start_date, end_date]];
//         }

//         frappe.call({
//             method: 'frappe.client.get_list',
//             args: {
//                 doctype: 'Sales Order',
//                 filters: filters,
//                 fields: ['name', 'status', 'customer', 'transaction_date', 'total'],
//             },
//             callback: function(response) {
//                 var status_count = {};

//                 response.message.forEach(function(order) {
//                     // Ensure status exists in the count object
//                     if (!status_count[order.status]) {
//                         status_count[order.status] = 0;
//                     }
//                     status_count[order.status]++;
//                 });

//                 // Update cards with status counts
//                 update_sales_order_cards(status_count);

//                 // Update chart
//                 update_sales_order_chart(status_count);

//                 // Update sales order table
//                 update_sales_order_table(response.message);

//                 // Show/hide no data message
//                 if (response.message.length === 0) {
//                     no_data_message.show();
//                 } else {
//                     no_data_message.hide();
//                 }
//             }
//         });
//     }

//     // Update cards with counts for each status dynamically
//     function update_sales_order_cards(status_count) {
//         card_container.empty();  // Clear existing cards

//         // Create a card for each status
//         for (var status in status_count) {
//             var card = $('<div class="card"></div>').appendTo(card_container);
//             $('<h4></h4>').text(status).appendTo(card);
//             $('<p class="status-count"></p>').text(status_count[status]).appendTo(card);
//         }
//     }

//     // Create or update the chart
//     function update_sales_order_chart(status_count) {
//         // Check if Chart.js is loaded, and create it
//         if (typeof Chart === 'undefined') {
//             var script = document.createElement('script');
//             script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
//             script.onload = function() {
//                 create_chart(status_count);
//             };
//             document.head.appendChild(script);
//         } else {
//             create_chart(status_count);
//         }
//     }

//     // Create the chart
//     function create_chart(status_count) {
//         // Destroy existing chart if it exists
//         if (window.salesOrderChart && window.salesOrderChart.destroy) {
//             window.salesOrderChart.destroy();
//         }

//         // Create the new chart
//         var ctx = document.getElementById('salesOrderChart').getContext('2d');
//         window.salesOrderChart = new Chart(ctx, {
//             type: 'bar',
//             data: {
//                 labels: Object.keys(status_count),
//                 datasets: [{
//                     label: 'Sales Orders by Status',
//                     data: Object.values(status_count),
//                     backgroundColor: generate_colors(Object.keys(status_count).length),
//                     borderWidth: 1
//                 }]
//             },
//             options: {
//                 scales: {
//                     y: {
//                         beginAtZero: true
//                     }
//                 }
//             }
//         });
//     }

//     // Function to generate different colors for each status in chart
//     function generate_colors(count) {
//         const colors = [];
//         const colorPalette = ['#FF6347', '#FFD700', '#32CD32', '#1E90FF', '#9370DB', '#FF4500', '#DA70D6'];
//         for (let i = 0; i < count; i++) {
//             colors.push(colorPalette[i % colorPalette.length]);
//         }
//         return colors;
//     }

//     // Update the sales order table with the fetched data
//     function update_sales_order_table(orders) {
//         table_body.empty(); // Clear existing rows

//         orders.forEach(function(order) {
//             var row = $('<tr></tr>').appendTo(table_body);
//             $('<td></td>').text(order.name).appendTo(row);
//             $('<td></td>').text(order.status).appendTo(row);
//             $('<td></td>').text(order.customer).appendTo(row);
//             $('<td></td>').text(order.transaction_date).appendTo(row);
//             $('<td></td>').text(order.total).appendTo(row);
//             var details_link = $('<td><span class="view-details">View</span></td>').appendTo(row);
//             details_link.find('.view-details').on('click', function() {
//                 frappe.set_route('Form', 'Sales Order', order.name);
//             });
//         });
//     }

//     // Trigger fetch on filter click
//     filter_button.on('click', function() {
//         var start_date = start_date_input.val();
//         var end_date = end_date_input.val();
//         fetch_sales_orders_data(start_date, end_date);
//     });

//     // Initial data load
//     fetch_sales_orders_data();
// };
