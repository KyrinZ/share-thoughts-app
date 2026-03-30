from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/<str:username>/", views.profile, name="profile_detail"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("notifications/", views.notifications, name="notifications"),
    path("messages/", views.messages, name="messages"),
    path("profile/<str:username>/followers/", views.followers, name="followers"),
    path("profile/<str:username>/following/", views.following, name="following"),
    
    # JSON API ENDPOINTS
    path("api/follow/<int:user_id>/", views.api_toggle_follow, name="api_toggle_follow"),
    path("api/conversations/", views.api_conversations, name="api_conversations"),
    path("api/messages/<int:convo_id>/", views.api_messages, name="api_messages"),
    path("api/start-convo/<int:user_id>/", views.api_start_conversation, name="api_start_conversation"),
    path("api/posts/", views.api_posts, name="api_posts"),
    path("api/posts/<int:post_id>/", views.api_post_detail, name="api_post_detail"),
    path("api/posts/<int:post_id>/like/", views.api_like_post, name="api_like_post"),
    path("api/posts/<int:post_id>/comments/", views.api_comments, name="api_comments"),
    path("api/comments/<int:comment_id>/", views.api_comment_detail, name="api_comment_detail"),
    path("api/comments/<int:comment_id>/like/", views.api_like_comment, name="api_like_comment"),
    path("api/trending/", views.api_trending, name="api_trending"),
    path("api/suggestions/", views.api_suggestions, name="api_suggestions"),
]