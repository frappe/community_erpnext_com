
from __future__ import unicode_literals
import frappe
import frappe.website.render

no_cache = 1

def get_context(context):
	frappe_partner = frappe.get_meta("Frappe Partner")

	countries = frappe_partner.get_field("country").options.split("\n")
	if frappe.session.get("session_country") and frappe.session.get("session_country") in countries:
		frappe.form_dict.country = frappe.session.get("session_country")

	context.all_partners = None
	context.partners = []

	if frappe.form_dict.country:
		title = "ERPNext Service Providers in {0}".format(frappe.form_dict.country)
		context.partners = frappe.db.sql("""select * from `tabFrappe Partner`
			where show_in_website=1 and country=%s order by priority desc,
			name asc limit 50""", frappe.form_dict.country, as_dict=True)

	else:
		title = "ERPNext Service Providers"
		context.all_partners = frappe.db.sql("""select
			name, partner_name, route, country, partner_category
			from `tabFrappe Partner`
			where show_in_website = 1
			order by priority desc, name asc""", as_dict=1)

	# if frappe.form_dict.service:
	# 	condition += " and ifnull({0}, 0)=1".format(frappe.scrub(frappe.form_dict.service))


	context.update({
		"title": title,
		"countries": frappe.db.sql_list("""select distinct country from `tabFrappe Partner`
			where show_in_website = 1
			order by country"""),
		"country_list": countries,
		"services": ["Customization", "App Development", "ERP Implementation", "Integration"]
	});
