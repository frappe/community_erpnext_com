import frappe

def get_context(context):
	filters = frappe._dict({"published":1})

	if "application_category" in frappe.form_dict:
		filters.application_category = frappe.form_dict.application_category
	if "application_name" in frappe.form_dict:
		filters.application_name = ("like", "%{0}%".format(frappe.form_dict.application_name))

	context.apps = frappe.get_all("Frappe App", filters=filters,
		fields=["application_name", "introduction", "headline", "publisher", "route",
			"icon"], limit_page_length=50)
	context.categories = frappe.get_meta("Frappe App").get_field("application_category").options.split("\n")
