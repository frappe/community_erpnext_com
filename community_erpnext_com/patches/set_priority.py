import frappe

def execute():
	frappe.reload_doctype("Frappe Partner")
	for d in frappe.get_all("Frappe Partner"):
		frappe.get_doc("Frappe Partner", d.name).save()
