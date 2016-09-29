import frappe

def execute():
	frappe.reload_doc("erpnext_community_portal", "doctype", "frappe_job_bid")

	for bid in frappe.get_all("Frappe Job Bid"):
		frappe.db.set_value("Frappe Job Bid", bid.name, "route", "bid/{0}".format(bid.name), 
			update_modified=False)
