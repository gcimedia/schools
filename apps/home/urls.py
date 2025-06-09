from django.urls import path

from .admin_site import org_admin_site
from .views import (
    SignUpView,
    landing,
    signin,
    signout,
)

urlpatterns = [
    path("admin/", org_admin_site.urls, name="org-admin"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("", landing, name="landing"),
]
