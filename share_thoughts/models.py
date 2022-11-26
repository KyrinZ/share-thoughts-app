from django.db import models
from django.contrib.auth.models import User
import os.path


def user_directory_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    return f"upload_profile/Profile__{instance.user.id}{extension}"


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(default="Nickname", max_length=100)
    show_nickname = models.BooleanField(default=False, blank=True)
    image = models.ImageField(
        default="upload_profile/default.jpg", upload_to=user_directory_path
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} profile"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s post on {self.created_at}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s comment for post no.{self.post.id} on {self.post.created_at}"


class LikePost(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="like_post_set"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="like_post_set"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")


class LikeComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="like_comment_set"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="like_comment_set"
    )
    post = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="like_comment_post_set"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment", "post")
