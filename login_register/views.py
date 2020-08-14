from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib import messages

from .forms import *
from main.models import *


# Regsiter view
def user_register(request):
    form = RegisterForm()

    # Logged-in user is denied to access register page and redirected to home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))

    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():

                username = form.cleaned_data.get('username')
                password = make_password(form.cleaned_data.get('password'))
                user = User.objects.create_user(
                    username=username, password=password)

                login(request, user)

                messages.success(request, 'You are registered and logged in')
                return HttpResponseRedirect(reverse('main:home'))

        return render(request, 'login_register/register.html', {
            'form': form
        })


# Login view
def user_login(request):
    form = LoginForm()

    # Logged-in user is denied to access register page and redirected to home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main:home'))
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

                # User is authentcated and logged-in
                user = authenticate(
                    request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You are logged in')
                    return HttpResponseRedirect(reverse('main:home'))

        return render(request, 'login_register/login.html', {
            'form': form
        })


# Logout view
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_register:login'))
