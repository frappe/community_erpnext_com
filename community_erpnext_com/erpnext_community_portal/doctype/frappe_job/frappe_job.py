# Copyright (c) 2015, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.user import get_fullname_and_avatar
from frappe.website.utils import get_comment_list
from frappe.utils import markdown
from frappe import _

class FrappeJob(WebsiteGenerator):
	website = frappe._dict(
		condition_field = "show_in_website",
		template = "templates/generators/job.html",
		page_title_field = "job_title",
		no_cache = 1,
	)

	def validate(self):
		if self.status in ("Open", "Assigned", "Completed"):
			self.show_in_website = 1
		else:
			self.show_in_website = 0

		self.route = 'jobs/' + self.name

		if self.status != "Open":
			self.docstatus = 1
			all_bids = self.get_all_bids()
			if self.status in ("Expired", "Withdrawn"):
				for bid in all_bids:
					bid = frappe.get_doc("Frappe Job Bid", bid.name)
					bid.status = self.status
					bid.save(ignore_permissions=True)

			elif self.status == "Completed":
				bid = frappe.get_doc("Frappe Job Bid", {"frappe_job": self.name, "status":"Accepted"})
				if bid:
					bid.status = "Completed"
					bid.save(ignore_permissions=True)

			elif self.status in "Assigned":
				for bid in all_bids:
					bid = frappe.get_doc("Frappe Job Bid", bid.name)
					if bid.status != "Accepted":
						bid.status = "Lost"
						bid.save(ignore_permissions=True)

		if self.frappe_partner:
			frappe.get_doc("Frappe Partner", self.frappe_partner).clear_cache()

	def before_update_after_submit(self):
		self.validate()

	def get_all_bids(self):
		return frappe.get_all("Frappe Job Bid", filters={"frappe_job": self.name})

	def get_context(self, context):
		user_details = get_fullname_and_avatar(self.owner)
		if user_details.get("name"):
			del user_details['name']

		context.update(user_details)
		context.comment_list = get_comment_list(self.doctype, self.name)
		if frappe.session.user == self.owner:
			context.bids = frappe.get_all("Frappe Job Bid",
				fields=["status, ""name", "frappe_partner", "creation", "frappe_partner_title"],
				filters={"frappe_job": self.name}, order_by="creation asc")

			if self.status == "Assigned":
				context.bid = [b for b in context.bids if b.status=='Accepted'][0].name

		elif frappe.session.user != "Guest":
			context.bid = frappe.db.get_value("Frappe Job Bid",
				{"owner": frappe.session.user, "frappe_job": self.name})

		if self.frappe_partner:
			context.frappe_partner_name, context.frappe_partner_route = \
				frappe.db.get_value("Frappe Partner",
					self.frappe_partner, ["partner_name", "route"])

	def get_parents(self, context):
		return [{"title":"Community", "name": "community"},
			{"title":"Jobs", "name": "community/jobs"}]

	def on_trash(self):
		for bid in self.get_all_bids():
			frappe.delete_doc("Frappe Job Bid", bid.name)

	def after_insert(self):
		all_providers = frappe.get_all("Frappe Partner", fields=["email"], filters={"show_in_website": 1})
		params = self.as_dict()
		params['job_detail'] = markdown(params['job_detail'])
		frappe.sendmail(
			subject = "New Job " + self.job_title,
			sender = "noreply@erpnext.com",
			recipients = [p.email for p in all_providers] + ["info@erpnext.com"],
			content = new_job_template.format(**params),
			delayed = True,
			reference_doctype = self.doctype,
			reference_name = self.name
		)
	
	def get_route(self):
		return frappe.db.get_value("Frappe Job", self.name, "route")

@frappe.whitelist()
def bid(job):
	partner = frappe.db.get_value("Frappe Partner", {"owner": frappe.session.user})
	if not partner:
		frappe.msgprint("Please update your Service Provider details before bidding")
		return

	bid = frappe.new_doc("Frappe Job Bid")
	bid.frappe_job = job
	bid.frappe_partner = partner
	bid.insert(ignore_permissions=True)

	return bid.name


@frappe.whitelist()
def delete(job):
	job = frappe.get_doc("Frappe Job", job)
	if job.owner != frappe.session.user:
		frappe.throw(_("Not Allowed"), frappe.PermissionError)

	frappe.delete_doc("Frappe Job", job.name, ignore_permissions=True)

@frappe.whitelist()
def complete(job, feedback, rating):
	job = frappe.get_doc("Frappe Job", job)
	if job.owner != frappe.session.user:
		frappe.throw(_("Not Allowed"), frappe.PermissionError)

	job.status = "Completed"
	job.feedback = feedback
	job.rating = rating
	job.save(ignore_permissions=True)

	partner = frappe.get_doc("Frappe Partner", job.frappe_partner)
	partner.update_rating_and_feedback()


@frappe.whitelist()
def close(job):
	job = frappe.get_doc("Frappe Job", job)
	if job.owner != frappe.session.user:
		frappe.throw(_("Not Allowed"), frappe.PermissionError)

	job.status = "Withdrawn"
	job.save(ignore_permissions=True)

def weekly_digest():
	new_jobs = frappe.db.sql("""select job_title, route, job_detail, company_name
		from `tabFrappe Job` where datediff(curdate(), creation) < 7""", as_dict=True)

	if not new_jobs:
		return

	recipients = frappe.db.sql_list("""select distinct owner from `tabFrappe Partner`
		where name != 'Administrator'""")

	template = """
<h3>New Jobs Listed on Frappe.io</h3>

<table style="width: 100%" cellspacing="0" border="1px" cellpadding="2px">
	<tbody>
		{% for j in jobs %}
		<tr>
			<td style="width: 50%">
				<a href="https://community.erpnext.com/{{ j.route }}">
					{{ j.job_title }}</a>
				<br><span style="color: #888">{{ j.company_name }}</span>
			</td>
			<td>
				{{ j.job_detail[:300] }}{{ "..." if j.job_detail|length > 300 else "" }}
			</td>
		</tr>
		{% endfor %}
	</tbody>
</table>
"""

	frappe.sendmail(recipients = recipients, subject="New Jobs This Week on Frappe.io",
		message = frappe.render_template(template, {"jobs": new_jobs}))

new_job_template = '''
<h3>{job_title}</h3>
<p>By {company_name}, {country}</p>
<hr>
	<div>
		<a href="https://community.erpnext.com/{route}">
			{job_title}
		</a>
	{job_detail}
	</div>
<hr>
<p>Please do not reply to this mail. This is an automatic notification from the Frappe Job Portal.</p>
'''
