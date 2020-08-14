from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Profile Form


class ProfileForm(forms.Form):
    profile_pic = forms.ImageField(required=False)
    nickname = forms.CharField(
        required=False, max_length=100, widget=forms.TextInput(attrs={'id': 'nickname'}))
    show_nickname = forms.BooleanField(required=False)

    def clean(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        nickname = self.cleaned_data.get('nickname')
        show_nickname = self.cleaned_data.get('show_nickname')
        if not nickname and not show_nickname and not profile_pic:
            raise forms.ValidationError(
                "Please dont leave the fields blank"
            )

    # Method for updating profile model
    def update_profile(self, profile_obj):
        profile_pic = self.cleaned_data.get('profile_pic')
        nickname = self.cleaned_data.get('nickname')
        show_nickname = self.cleaned_data.get('show_nickname')

        if profile_pic:
            profile_obj.profile_pic = profile_pic
        if nickname:
            profile_obj.nickname = nickname
        profile_obj.show_nickname = show_nickname
        profile_obj.save()


# Password Form
class ChangePassword(forms.Form):
    old_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput())
    new_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput())
    confirmation = forms.CharField(
        max_length=100, widget=forms.PasswordInput())

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirmation = self.cleaned_data.get('confirmation')
        if not old_password and not new_password and not confirmation:
            raise forms.ValidationError(
                "Please dont leave the fields blank"
            )
        if new_password != confirmation:
            raise forms.ValidationError(
                "Your New Password and Confirmation should be same"
            )
