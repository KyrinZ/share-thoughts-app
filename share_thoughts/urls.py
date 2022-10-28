from django.urls import path
from . import views

urlpatterns = [
    # Page Url
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('about/', views.about, name='about'),
    path('s/', views.landing_page, name='landing_page'),
    path('home2/', views.home2, name='home2'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('abou2t/', views.about2, name='about2'),

    # Function Url(filter, liking post, liking comment)
    path('like-post/<int:post_id>/',
         views.liking_post, name='like_post'),
    path('like-comment/<int:comment_id>/',
         views.liking_comment, name='like_comment'),
    path('filter/<str:filter_key>/', views.filtering, name='filter'),

    # Json Url
    path('post-json/page<int:pg>/',
         views.post_json_format, name='post_json_format'),
    path('like-post-json/<int:post_id>/',
         views.like_post_json, name='like_post_json'),
    path('like-comment-json/<int:comment_id>/',
         views.like_comment_json, name='like_comment_json'),
]
