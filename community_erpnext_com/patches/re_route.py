from frappe.patches.v7_0.re_route import update_routes

def execute():
	update_routes(['Frappe Job', 'Frappe Partner', 'Frappe Job Bid'])