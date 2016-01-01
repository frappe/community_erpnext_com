"""
Configuration for docs

Add properties

1. `source_link`
2. `docs_base_url`
3. `context`
"""

source_link = "https://github.com/frappe/community_erpnext_com"
docs_base_url = "https://frappe.github.io/community_erpnext_com"
headline = "Connects service seekers and providers"
sub_heading = "ERPNext Community Portal allows users to post jobs, find service providers and post jobs"

def get_context(context):
	context.title = "ERPNext Community Portal"
