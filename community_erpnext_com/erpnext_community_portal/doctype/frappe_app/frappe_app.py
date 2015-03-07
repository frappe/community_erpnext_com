# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

from frappe.website.website_generator import WebsiteGenerator

class FrappeApp(WebsiteGenerator):
	website = frappe._dict(
		condition_field = "published",
		template = "templates/generators/frappe_app.html",
		page_title_field = "application_name",
	)

	def before_insert(self):
		# show on default - good faith
		self.show_in_website = 1
		self.parent_website_route = "apps"

	def get_parents(self, context):
		return [
			{"title": "Community", "name": "community"},
			{"title": "Apps", "name": "community/apps"}
		]

