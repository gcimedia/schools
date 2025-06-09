from django.contrib.admin import AdminSite

from .views import signin, signout


class OrgAdminSite(AdminSite):
    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path("login/", signin, name="org_admin_login"),
            path("logout/", signout, name="org_admin_logout"),
        ]
        return custom_urls + urls


# Create custom admin site instance
org_admin_site = OrgAdminSite(name="org_admin")
