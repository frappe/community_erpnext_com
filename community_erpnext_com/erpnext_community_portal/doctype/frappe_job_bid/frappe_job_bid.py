# Copyright (c) 2015, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.website.website_generator import WebsiteGenerator
from frappe.website.utils import get_comment_list

class FrappeJobBid(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/bid.html",
		page_title = "Bid",
		no_cache = 1,
	)
	def onload(self):
		self.frappe_job_title = frappe.db.get_value("Frappe Job", self.frappe_job, "job_title")
		self.frappe_job_title = frappe.db.get_value("Frappe Job", self.frappe_job, "job_title")

	def before_insert(self):
		if frappe.db.get_value("Frappe Job Bid",
			{"frappe_partner": self.frappe_partner, "frappe_job": self.frappe_job}):
			frappe.msgprint("You have already bid for this job")
			raise frappe.ValidationError

		if frappe.db.get_value("Frappe Job", self.frappe_job, "owner")==frappe.session.user:
			frappe.msgprint("You can't bid for your own job!")
			raise frappe.ValidationError

		self.frappe_job_title = frappe.db.get_value("Frappe Job", self.frappe_job,
			"job_title")
		self.frappe_partner_title = frappe.db.get_value("Frappe Partner", self.frappe_partner,
			"partner_name")

	def after_insert(self):
		frappe.sendmail(recipients=[self.owner], subject="New Bid for your Job {0}".format(self.name),
			message=new_bid_template.format(**self.as_dict()), bulk=True)

	def get_context(self, context):
		context.job = frappe.get_doc("Frappe Job", self.frappe_job)
		context.partner = frappe.get_doc("Frappe Partner", self.frappe_partner)
		context.comment_list = get_comment_list(self.doctype, self.name)

	def get_parents(self, context):
		return [{"title":"Community", "name": "community"},
			{"title":"Jobs", "name": "community/jobs"},
			{"title": context.job.job_title, "name": context.job.get_route() }]


	def on_trash(self):
		if self.status == "Accepted":
			frappe.throw(_("Accepted bid cannot be deleted"))


@frappe.whitelist()
def accept(bid):
	bid = frappe.get_doc("Frappe Job Bid", bid)
	job = frappe.get_doc("Frappe Job", bid.frappe_job)
	if job.owner != frappe.session.user:
		frappe.throw(_("Not Allowed"), frappe.PermissionError)
	if job.status != "Open":
		frappe.throw(_("Bid not Open"))
	bid.status = "Accepted"
	bid.save(ignore_permissions=True)
	bid.clear_cache()

	job.status = "Assigned"
	job.frappe_partner = bid.frappe_partner
	job.save(ignore_permissions=True)
	job.clear_cache()

@frappe.whitelist()
def delete(bid):
	bid = frappe.get_doc("Frappe Job Bid", bid)
	if bid.owner != frappe.session.user:
		frappe.throw(_("Not Allowed"), frappe.PermissionError)

	frappe.delete_doc("Frappe Job Bid", bid.name, ignore_permissions=True)

	job = frappe.get_doc("Frappe Job", bid.frappe_job)
	job.clear_cache()

new_bid_template = """
<h3>Notification from Frappe.io Community Portal</h3>
<p>{frappe_partner} has bid for your job {frappe_job}</p>
<p><a href="https://frappe.io/community/jobs/{frappe_job}">
	Click here to manage bids</a></p>
"""
