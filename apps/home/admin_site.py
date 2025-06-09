from django.contrib.admin import AdminSite

from .views import signin, signout


class OrgAdminSite(AdminSite):
    """
    Custom admin site for the organization.

    Overrides default admin login/logout URLs with custom views
    for authentication that may include branding, layout, or behavior
    tailored to the organization.
    """

    def get_urls(self):
        """
        Returns a list of URL patterns for the custom admin site.

        Adds custom login and logout paths (handled by `signin` and `signout` views),
        and appends the default admin site URLs.
        """
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path("login/", signin, name="org_admin_login"),
            path("logout/", signout, name="org_admin_logout"),
        ]
        return custom_urls + urls


# Create custom admin site instance
org_admin_site = OrgAdminSite(name="org_admin")
