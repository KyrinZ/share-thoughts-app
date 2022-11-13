from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile


def home_view(request):
    context = {}
    return render(request, "home.html", context)


def profile_view(request):
    context = {}
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
