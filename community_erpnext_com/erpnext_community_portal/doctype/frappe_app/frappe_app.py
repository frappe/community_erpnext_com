# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
import requests
import json
from frappe.utils import flt

class FrappeApp(WebsiteGenerator):
	website = frappe._dict(
		template = "templates/generators/app.html",
		page_title_field = "app_name",
		no_cache=1
	)
	
	def make_route(self):
		return 'app/' + self.scrub(self.name)
	
	def get_context(self, context):
		repo = '/'.join(self.repository_url.split('/')[-2::])
		res = requests.get("https://api.github.com/repos/{0}".format(repo))
		res = res.json()
		
		context.stargazers_count = res.get("stargazers_count", 0)
		context.repo_size = flt(flt(res.get("size", 0))/1000)
		context.open_issues = res.get("open_issues_count", 0)
		