from django.urls import path

from .admin_site import portal_site
from .views import SignUpView, contact, signin, signout

urlpatterns = [
    path("portal/", portal_site.urls, name="portal"),
    path("mail/contact/", contact, name="contact"),
    path("auth/signup/", SignUpView.as_view(), name="signup"),
    path("auth/signin/", signin, name="signin"),
    path("auth/signout/", signout, name="signout"),
]
