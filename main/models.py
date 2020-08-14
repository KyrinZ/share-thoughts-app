from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count

from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(default='Nickname', max_length=100)
    show_nickname = models.BooleanField(default=False, blank=True)
    profile_pic = models.ImageField(default='default.jpg')

    def __str__(self):
        return f"{self.user} Profile"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_field = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s post on {self.date_posted}"

    # Method to filter posts based on key passed
    @classmethod
    def filtering_posts(cls, key):
        if key == 'oldest':
            post = cls.objects.order_by(
                'date_posted')
        elif key == 'popularity':
            post = cls.objects.annotate(
                num_likes=Count('likeforpost')).order_by('-num_likes')
        else:
            post = cls.objects.order_by(
                '-date_posted')
        return post


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text_field = models.TextField(blank=True, null=True)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}'s comment for post no.{self.post.id} on {self.post.date_posted}"


class LikeForPost(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(blank=True, default=True)


class LikeForComment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    liked = models.BooleanField(blank=True, default=True)
