from django.urls import path
from accounts import views as accounts_views

urlpatterns = [
    path("login/", accounts_views.login_redirect, name="login"),
    path("logout/", accounts_views.logout_view, name="logout"),
    path("profile/", accounts_views.user_profile, name="user_profile"),
]