# My Account

<!-- jinja -->

{% if frappe.user == "Guest" %}
<div class="alert alert-info">
	Please <a href="/login?redirect-to=/community/manage" class="btn btn-small btn-primary">Login</a> to manage your account.
</div>
{% else %}
<div class="alert alert-info">
	You are logged in as {{ frappe.full_name }}
</div>
<ul class="list-group">
	<li class="list-group-item">
		<i class="icon-fixed-width icon-legal"></i>
		<a href="/community/jobs?jobs=my-bids">My Bids</a>
	</li>
	<li class="list-group-item">
		<i class="icon-fixed-width icon-user"></i>
		<a href="/community/jobs?jobs=my-jobs">Jobs by me</a>
	</li>
	<li class="list-group-item">
		<i class="icon-fixed-width icon-edit"></i>
		<a href="/become-a-partner">Edit Service Provider Listing</a>
	</li>
	<li class="list-group-item">
		<i class="icon-fixed-width icon-edit"></i>
		<a href="/post-jobs">Edit Jobs</a>
	</li>
	<li class="list-group-item">
		<i class="icon-fixed-width icon-edit"></i>
		<a href="/list-your-app">Edit Apps</a>
	</li>
</ul>
{% endif %}

