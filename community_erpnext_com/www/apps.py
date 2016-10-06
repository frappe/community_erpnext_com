import frappe

no_cache = 1

def get_context(context):
	filters = frappe._dict()

	if "category" in frappe.form_dict:
		filters.category = frappe.form_dict.category
	if "app_name" in frappe.form_dict:
		filters.app_name = ("like", "%{0}%".format(frappe.form_dict.app_name))

	context.apps = frappe.get_all("Frappe App", filters=filters,
		fields=["app_name", "title", "description", "repository_url", "badge", "route", "category"], limit_page_length=50)

	context.categories = frappe.get_meta("Frappe App").get_field("category").options.split("\n")
