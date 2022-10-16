from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import *


class ProfileAdminInline(admin.TabularInline):
    model = Profile


class UserAdmin(BaseUserAdmin):
    fieldsets = [
        ('User Info',               {'fields': ['username', 'password']}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    ]
    inlines = [ProfileAdminInline]


class LikeForPostAdminInline(admin.TabularInline):
    model = LikeForPost
    extra = 0


class CommentAdminInline(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',               {'fields': ['user']}),
        ('Post Area', {'fields': [
            'text_field']}),
        ('Date Posted', {'fields': ['date_posted']})
    ]
    inlines = [CommentAdminInline, LikeForPostAdminInline]
    list_display = ('user', 'date_posted')


class LikeForCommentAdminInline(admin.TabularInline):
    model = LikeForComment
    extra = 0


class CommentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User',               {'fields': ['user', 'post']}),
        ('Post Area', {'fields': [
            'text_field']}),
        ('Date commented', {'fields': ['date_commented']})
    ]
    inlines = [LikeForCommentAdminInline]
    list_display = ('user', 'post', 'date_commented')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
