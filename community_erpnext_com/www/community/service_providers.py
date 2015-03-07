
from __future__ import unicode_literals
import frappe
import frappe.website.render

def get_context(context):
	frappe_partner = frappe.get_meta("Frappe Partner")
	condition, values = "", []
	if frappe.form_dict.country:
		condition += " and country=%s"
		values.append(frappe.form_dict.country)

	if frappe.form_dict.service:
		condition += " and ifnull({0}, 0)=1".format(frappe.scrub(frappe.form_dict.service))

	context.update({
		"partners": frappe.db.sql("""select * from `tabFrappe Partner`
			where show_in_website=1 {0} order by priority desc, average_rating desc,
			name asc limit 50""".format(condition),
			values, as_dict=True),
		"country_list": frappe_partner.get_field("country").options.split("\n"),
		"services": ["Customization", "App Development", "ERP Implementation", "Integration"]
	});
