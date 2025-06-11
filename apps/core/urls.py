from django.conf import settings
from django.urls import path

from .admin_site import portal_site
from .views import (
    SignUpView,
    signin,
    signout,
)

portal_url = settings.PORTAL_URL.strip("/") + "/"

urlpatterns = [
    path(portal_url, portal_site.urls, name="portal"),
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path("auth/signin/", signin, name="signin"),
    path("auth/signout/", signout, name="signout"),
]
