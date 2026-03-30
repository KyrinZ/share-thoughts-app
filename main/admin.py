from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Post, PostMedia, Comment, Like, CommentLike, Follow


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = 'follower'
    extra = 0


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline, FollowInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 0


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at')
    inlines = [PostMediaInline, LikeInline, CommentInline]


class CommentLikeInline(admin.TabularInline):
    model = CommentLike
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'created_at')
    inlines = [CommentLikeInline]


