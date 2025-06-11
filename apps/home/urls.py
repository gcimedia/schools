from django.conf import settings
from django.urls import path

from .admin_site import portal_site
from .views import (
    SignUpView,
    landing,
    signin,
    signout,
)

urlpatterns = [
    path(settings.PORTAL_URL.strip("/") + "/", portal_site.urls, name="portal"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("", landing, name="landing"),
]
