# Copyright (c) 2015, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def expire_jobs():
	for job in frappe.db.sql_list("""select name from `tabFrappe Job`
		where datediff(curdate(), creation) > 60 and status='Open'"""):
		job = frappe.get_doc("Frappe Job", job)
		job.status = "Expired"
		job.save(ignore_permissions=True)
