from django.conf import settings
from django.urls import path

from .admin_site import admin_site
from .views import (
    SignUpView,
    landing,
    signin,
    signout,
)

admin_url = settings.ADMIN_URL.strip("/") + "/"

urlpatterns = [
    path(admin_url, admin_site.urls, name="org-admin"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("", landing, name="landing"),
]
