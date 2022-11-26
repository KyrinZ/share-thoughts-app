from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import os
from .models import Profile, Post, Comment


def home_view(request):
    context = {}
    context["posts"] = Post.objects.all().order_by("-created_at")
    return render(request, "home.html", context)


def create_post_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":

        content = request.POST.get("post", "")
        if content is not "":
            Post(user=request.user, content=content).save()
            messages.success(request, "Post added!!")
    return redirect("home")


def create_comment_view(request, post_id):
    context = {}
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":

        content = request.POST.get("comment", "")
        if content is not "":
            post = Post.objects.get(id=post_id)
            if post is not None:
                Comment(user=request.user, post=post, content=content).save()
                messages.success(request, "Comment added!!")
    return redirect("home")


def profile_view(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        image = request.FILES.get("image", None)
        nickname = request.POST.get("nickname", "")
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")
        user = request.user
        profile = Profile.objects.get(user=user)

        is_profile_updated = False
        if image is not None:
            try:
                os.remove(profile.image.path)
            except:
                pass
            profile.image = image
            profile.save()
            is_profile_updated = True

        if nickname is not "" and nickname != profile.nickname:
            profile.nickname = nickname
            profile.save()
            is_profile_updated = True

        if password is not "":
            if password != confirmation:
                messages.error(request, "Password did not match.")
            else:
                user.set_password(password)
                user.save()
                messages.success(request, "Password changed!")
                return redirect("login")

        if is_profile_updated:
            messages.success(request, "Profile updated!")

        return redirect("profile")
    else:
        return render(request, "profile.html", context)


def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Username or password is invalid.")
            return redirect("login")
        login(request, user)
        messages.success(request, "Logged in successfully!")
        return redirect("home")
    else:
        return render(request, "login.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out.")
    return redirect("home")


def registration_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        confirmation = request.POST.get("confirmation", "")

        if not username or not password or not confirmation:
            messages.error(request, "Fields are empty.")
            return redirect("registration")

        if password != confirmation:
            messages.error(request, "Password did not match.")
            return redirect("registration")

        user_found = User.objects.filter(username=username).first()
        if user_found:
            messages.error(request, "Username already exist.")
            return redirect("registration")

        user = User.objects.create_user(username=username, password=password)
        user.save()
        Profile(user=user, nickname=user.username).save()
        login(request, user)
        messages.success(request, "Registered successfully!")
        return redirect("home")

    return render(request, "registration.html", context)


def about_view(request):
    context = {}
    return render(request, "about.html", context)
