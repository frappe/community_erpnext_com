import frappe
from frappe.frappeclient import FrappeClient

def migrate():
	print "connecting..."
	frappe.flags.mute_emails = True
	remote = FrappeClient("https://frappe.io", "Administrator", frappe.conf.frappe_admin_password, verify=False)
	remote.migrate_doctype("Frappe Partner")
	remote.migrate_doctype("Frappe Publisher")
	remote.migrate_doctype("Frappe Job")
	remote.migrate_doctype("Frappe Job Bid")
	frappe.flags.mute_emails = False

	frappe.db.sql("update `tabFrappe Job` set route='jobs'")
	frappe.db.sql("update `tabFrappe Partner` set route='service-providers'")
