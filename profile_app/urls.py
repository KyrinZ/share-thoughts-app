from django.urls import path
from . import views

app_name = 'profile_app'
urlpatterns = [
    path('profile/', views.profile, name='profile'),

    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
]
