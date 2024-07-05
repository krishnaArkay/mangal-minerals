app_name = "mangal_minerals"
app_title = "Mangal Minerals"
app_publisher = "Arkay Apps"
app_description = "Customized Soultions For Mangal Minerals"
app_email = "krishna@arkayapps.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mangal_minerals/css/mangal_minerals.css"
# app_include_js = "/assets/mangal_minerals/js/mangal_minerals.js"

# include js, css files in header of web template
# web_include_css = "/assets/mangal_minerals/css/mangal_minerals.css"
# web_include_js = "/assets/mangal_minerals/js/mangal_minerals.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mangal_minerals/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Purchase Receipt" : "public/js/purchase_receipt_custom.js",
              "Customer" : "public/js/customer_custom.js",
              "Supplier" : "public/js/supplier_custom.js",
            #   "Blanket Order":"public/js/open_order_custom.js",
              "Delivery Note":"public/js/delivery_note_custom.js",
              "Purchase Order":"public/js/purchase_order_custom.js",
              "Sales Order":"public/js/sales_order_custom.js",
              "Blanket Order":"public/js/blanket_order_custom.js"
			  }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "mangal_minerals/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {f
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "mangal_minerals.utils.jinja_methods",
# 	"filters": "mangal_minerals.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "mangal_minerals.install.before_install"
# after_install = "mangal_minerals.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mangal_minerals.uninstall.before_uninstall"
# after_uninstall = "mangal_minerals.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "mangal_minerals.utils.before_app_install"
# after_app_install = "mangal_minerals.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "mangal_minerals.utils.before_app_uninstall"
# after_app_uninstall = "mangal_minerals.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mangal_minerals.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Item": {
        "before_save": "mangal_minerals.mangal_minerals.doctype.api.item_validation",
        # "on_submit": "mangal_minerals.mangal_minerals.doctype.api.on_sales_order_submit",
		# "on_update": "method",
		# "on_cancel": "method",
		"on_trash": "mangal_minerals.mangal_minerals.doctype.api.before_delete",
        "before_rename": "mangal_minerals.mangal_minerals.doctype.api.before_rename"
	},
    "Delivery Note": {
        "before_submit": "mangal_minerals.mangal_minerals.doctype.api.dn_before_save",
         "on_submit": "mangal_minerals.mangal_minerals.doctype.api.delivery_note_on_submit",
		# "on_update": "method",
		 "on_cancel": "mangal_minerals.mangal_minerals.doctype.api.update_delivered_qty",
		# "on_trash": "method"
	},
    "Purchase Receipt":{
        "before_submit": "mangal_minerals.mangal_minerals.doctype.api.purchase_receipt_on_submit",
        
	},
    # "Open Order Scheduler":{
    #     "on_update":"mangal_minerals.mangal_minerals.doctype.api.submit_sche"
	# }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "1 0 * * *": [
            "mangal_minerals.mangal_minerals.doctype.api.update_OPS_truck"
        ]
    }
# 	"all": [
# 		"mangal_minerals.tasks.all"
# 	],
	# "daily": [
	# 	"mangal_minerals.tasks.update_OPS_truck"
	# ],
# 	"hourly": [
# 		"mangal_minerals.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mangal_minerals.tasks.weekly"
# 	],
# 	"monthly": [
# 		"mangal_minerals.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "mangal_minerals.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mangal_minerals.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mangal_minerals.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["mangal_minerals.utils.before_request"]
# after_request = ["mangal_minerals.utils.after_request"]

# Job Events
# ----------
# before_job = ["mangal_minerals.utils.before_job"]
# after_job = ["mangal_minerals.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"mangal_minerals.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


