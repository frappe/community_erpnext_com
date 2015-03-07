
from __future__ import unicode_literals
import frappe
import frappe.website.render

def get_context(context):
	frappe_job = frappe.get_meta("Frappe Job")
	condition, values, my_bids = "", [], []
	if frappe.form_dict.country:
		condition += " and country=%s"
		values.append(frappe.form_dict.country)

	if frappe.form_dict.service:
		condition += " and service=%s"
		values.append(frappe.form_dict.service)

	if frappe.session.user != "Guest":
		my_bids = frappe.db.sql_list("""select frappe_job
			from `tabFrappe Job Bid` where status in ("Open", "Assigned", "Completed")
			and owner = %s""", frappe.session.user)

		if frappe.form_dict.jobs=="my-jobs":
			condition += """ and owner=%s"""
			values.append(frappe.session.user)

	jobs = frappe.db.sql("""select * from `tabFrappe Job`
			where show_in_website=1 {0} order by creation desc limit 50""".format(condition),
			values, as_dict=True)

	if my_bids:
		for j in jobs:
			if j.name in my_bids:
				j.my_bid = 1

	if frappe.form_dict.jobs=="my-bids":
		jobs = filter(lambda d: d.my_bid, jobs)

	context.update({
		"is_jobs": True,
		"jobs": jobs,
		"country_list": frappe_job.get_field("country").options.split("\n"),
		"services": frappe_job.get_field("service").options.split("\n")
	})
