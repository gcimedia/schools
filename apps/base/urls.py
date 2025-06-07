from django.urls import path

from .views import SignUp, home, signin, signout

app_name = "base"

urlpatterns = [
    # auth
    path("signup", SignUp.as_view(), name="signup"),
    path("signin", signin, name="signin"),
    path("signout", signout, name="signout"),
    # hero
    path("", home, name="home"),
    # blog
]
