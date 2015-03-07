# Copyright (c) 2015, Frappe Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FrappeJobApplicant(Document):
	def after_insert(self):
		frappe.sendmail("info@erpnext.com",
			subject=  "New Job Applicant",
			message = "Please find attached",
			attachments = [{
				"fname": self.name + ".pdf",
				"fcontent": frappe.get_print_format(self.doctype, self.name, as_pdf=True)
			}])

