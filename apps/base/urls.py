from django.conf import settings
from django.urls import path

from .admin_site import org_admin_site
from .views import HomeRedirectView, PermanentHomeRedirectView, SignUp, signin, signout

# app_name = "base"

# Choose redirect type based on DEBUG setting
RedirectView = HomeRedirectView if settings.DEBUG else PermanentHomeRedirectView

urlpatterns = [
    path("admin/", org_admin_site.urls, name="org-admin"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("", RedirectView.as_view(), name="home_redirect"),
]
