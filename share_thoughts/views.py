from django.shortcuts import render


def home(request):
    context = {}
    return render(request, "home.html", context)


def profile(request):
    context = {}
    return render(request, "profile.html", context)


def login(request):
    context = {}
    return render(request, "login.html", context)


def registration(request):
    context = {}
    return render(request, "registration.html", context)


def about(request):
    context = {}
    return render(request, "about.html", context)
