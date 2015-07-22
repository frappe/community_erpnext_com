app_name = "community_erpnext_com"
app_title = "ERPNext Community Portal"
app_publisher = "Frappe Technologies Pvt. Ltd."
app_description = "community.erpnext.com"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@frappe.io"
app_version = "0.0.1"
hide_in_installer = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/community_erpnext_com/css/community_erpnext_com.css"
# app_include_js = "/assets/community_erpnext_com/js/community_erpnext_com.js"

# include js, css files in header of web template
# web_include_css = "/assets/community_erpnext_com/css/community_erpnext_com.css"
# web_include_js = "/assets/community_erpnext_com/js/community_erpnext_com.js"

required_apps = ["frappe_theme"]

website_context = {
	"brand_html": "<img class='navbar-icon' src='/assets/frappe_theme/img/erp-icon.svg' />ERPNext Community",
	"top_bar_items": [
		{"label": "Jobs", "url":"/jobs", "right": 1},
		{"label": "Service Providers", "url":"/service-providers", "right": 1},
		{"label": "Terms", "url":"/terms", "right": 1}
	],
	"favicon": "/assets/frappe_theme/img/favicon.ico"
}

my_account_context = [
	{"label": "My Bids", "url": "/jobs?jobs=my-bids"},
	{"label": "Jobs by me", "url": "/jobs?jobs=my-jobs"},
	{"label": "Edit Service Provider Listing", "url": "/become-a-partner"},
	{"label": "Edit Jobs", "url": "/post-jobs"}
]

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "index"

web_include_css = "/assets/frappe/css/hljs.css"
web_include_js = "/assets/frappe/js/lib/highlight.pack.js"

website_generators = ["Frappe Partner", "Frappe Job", "Frappe Job Bid"]

fixtures = [
	"Contact Us Settings",
	"Frappe Publisher",
	"Web Form"
]

scheduler_events = {
	"daily": ["community_erpnext_com.erpnext_community_portal.doctype.frappe_job.frappe_job.expire_jobs"],
	"weekly": ["community_erpnext_com.erpnext_community_portal.doctype.frappe_job.frappe_job.weekly_digest"]
}

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "community_erpnext_com.install.before_install"
# after_install = "community_erpnext_com.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "community_erpnext_com.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"community_erpnext_com.tasks.all"
# 	],
# 	"daily": [
# 		"community_erpnext_com.tasks.daily"
# 	],
# 	"hourly": [
# 		"community_erpnext_com.tasks.hourly"
# 	],
# 	"weekly": [
# 		"community_erpnext_com.tasks.weekly"
# 	]
# 	"monthly": [
# 		"community_erpnext_com.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "community_erpnext_com.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "community_erpnext_com.event.get_events"
# }
