from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.forms import ValidationError

from share_thoughts.models import *

from .forms import *


# Profile View
@login_required(login_url='login_register:login')
def profile(request):

    posts = Post.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)

    # Forms
    profile_form = ProfileForm()
    change_password_form = ChangePassword()

    return render(request, 'profile_app/profile.html', {
        'profile': profile,
        'profile_form': profile_form,
        'change_password_form': change_password_form,
        'posts': posts
    })


# Profile settings view
@login_required(login_url='login_register:login')
def profile_settings(request):

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():

            profile_obj = Profile.objects.get(user=request.user)
            profile_form.update_profile(profile_obj)
            messages.success(request, 'profile status updated')
        else:
            return render(request, 'profile_app/error_form.html', {
                'profile_form': profile_form
            })
    return HttpResponseRedirect(reverse('profile_app:profile'))


# Changing password view
@login_required(login_url='login_register:login')
def change_password(request):

    if request.method == 'POST':
        change_password_form = ChangePassword(request.POST)

        if change_password_form.is_valid():
            user = User.objects.get(username=request.user)
            old_password = change_password_form.cleaned_data.get(
                'old_password')
            new_password = change_password_form.cleaned_data.get(
                'new_password')
            confirmation = change_password_form.cleaned_data.get(
                'confirmation')

            if check_password(old_password, user.password):
                password = make_password(new_password)
                user.password = password
                user.save()

                login(request, user)
                messages.success(request, 'Password updated')

            else:
                messages.error(request, "Your Old password didn't match")
        else:
            return render(request, 'profile_app/error_form.html', {
                'change_password_form': change_password_form
            })
    return HttpResponseRedirect(reverse('profile_app:profile'))


# Delete Post view
@ login_required(login_url='login_register:login')
def delete_post(request, post_id):
    Post.objects.filter(id=post_id).delete()
    messages.success(request, 'Post deleted')
    return HttpResponseRedirect(reverse('profile_app:profile'))
