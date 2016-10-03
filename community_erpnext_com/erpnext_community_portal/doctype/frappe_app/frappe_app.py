# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
import requests
from frappe.utils import flt

class FrappeApp(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/app.html",
		page_title_field = "app_name",
		no_cache=1
	)
	
	def on_update(self):
		self.set_repo_details()

	def set_repo_details(self):
		if not self.repository_url:
			return

		repo = '/'.join(self.repository_url.split('/')[-2::])
		
		try:
			res = requests.get("https://api.github.com/repos/{0}".format(repo))
			res = res.json()
		except:
			res = {}
		
		self.db_set("stargazers_count", res.get("stargazers_count", 0))
		self.db_set("repo_size", flt(flt(res.get("size", 0))/1000))
		self.db_set("open_issue_count", res.get("open_issues", 0))
	
	def make_route(self):
		return 'app/' + self.scrub(self.name)
	
	def get_context(self, context):
		context.stargazers_count = self.stargazers_count or 0
		context.repo_size = self.repo_size or 0
		context.open_issues = self.open_issue_count or 0

def set_repo_details():
	for app in frappe.get_all("Frappe App", filters={"repository_url": ['!=', '']}):
		doc = frappe.get_doc("Frappe App", app.name)
		doc.set_repo_details()