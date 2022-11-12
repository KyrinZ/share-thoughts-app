from django.urls import path
from . import views

urlpatterns = [
    # Page Url
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.login, name="login"),
    path("registration/", views.registration, name="registration"),
    path("about/", views.about, name="about"),
]
