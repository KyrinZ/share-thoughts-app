from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    # Page Url
    path('', views.landing_page, name='main'),
    path('home/', views.home, name='home'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('about/', views.about, name='about'),

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
