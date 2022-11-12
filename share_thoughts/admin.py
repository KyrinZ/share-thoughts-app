from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Profile, Post, Comment, LikePost, LikeComment


class ProfileAdminInline(admin.StackedInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    fieldsets = [
        (None, {"fields": ["username"]}),
    ]

    inlines = [ProfileAdminInline]


class LikePostAdminInline(admin.TabularInline):
    model = LikePost
    extra = 0


class CommentAdminInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {"fields": ["user", "content", "created_at", "updated_at"]},
        ),
    ]
    readonly_fields = ("created_at", "updated_at")
    inlines = [CommentAdminInline, LikePostAdminInline]
    list_display = ("user", "created_at")


class LikeCommentAdminInline(admin.TabularInline):
    model = LikeComment
    extra = 0
    fk_name = "comment"


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {"fields": ["user", "post", "content", "created_at", "updated_at"]},
        ),
    ]
    readonly_fields = ("created_at", "updated_at")
    inlines = [LikeCommentAdminInline]
    list_display = ("user", "post", "created_at")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
