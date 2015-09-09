
from __future__ import unicode_literals
import frappe
import frappe.website.render

def get_context(context):
	frappe_partner = frappe.get_meta("Frappe Partner")

	countries = frappe_partner.get_field("country").options.split("\n")
	if frappe.session.get("session_country") and frappe.session.get("session_country") in countries:
		frappe.form_dict.country = frappe.session.get("session_country")

	condition, values = "", []
	if frappe.form_dict.country:
		condition += " and country=%s"
		values.append(frappe.form_dict.country)
		title = "ERPNext Service Provders in {0}".format(frappe.form_dict.country)
	else:
		condition += " and partner_category != 'Unverified'"
		title = "ERPNext Service Provders"

	# if frappe.form_dict.service:
	# 	condition += " and ifnull({0}, 0)=1".format(frappe.scrub(frappe.form_dict.service))


	context.update({
		"title": title,
		"countries": frappe.db.sql_list("""select distinct country from `tabFrappe Partner`
			where show_in_website = 1
			order by country"""),
		"partners": frappe.db.sql("""select * from `tabFrappe Partner`
			where show_in_website=1 {0} order by priority desc,
			name asc limit 50""".format(condition),
			values, as_dict=True),
		"country_list": countries,
		"services": ["Customization", "App Development", "ERP Implementation", "Integration"]
	});
