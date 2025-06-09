from django.contrib.admin import AdminSite
from .views import signout


class OrgAdminSite(AdminSite):
    # site_header = "Your Site Administration"
    # site_title = "Your Site Admin"
    # index_title = "Welcome to Your Site Administration"

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path("logout/", signout, name="org_admin_logout"),
        ]
        return custom_urls + urls


# Create custom admin site instance
org_admin_site = OrgAdminSite(name="org_admin")
