from django.urls import path
from . import views

urlpatterns = [
    # Page Url
    path("", views.home_view, name="home"),
    path("profile/", views.profile_view, name="profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registration/", views.registration_view, name="registration"),
    path("about/", views.about_view, name="about"),
]
