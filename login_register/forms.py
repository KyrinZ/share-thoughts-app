from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not username and not password:
            raise forms.ValidationError(
                "Please dont leave the fields blank"
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(
                "Username doesnot exists, please make sure you typed in right username"
            )
        if not check_password(password, user.password):
            raise forms.ValidationError(
                "Password didn't match"
            )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    confirmation = forms.CharField(
        max_length=100, widget=forms.PasswordInput())

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirmation = self.cleaned_data.get('confirmation')

        if not username and not password and not confirmation:
            raise forms.ValidationError(
                "Please dont leave the fields blank"
            )
        if password != confirmation:
            raise forms.ValidationError(
                "Password didnt match, make sure the password fields are identical"
            )
        try:
            if User.objects.get(username=username):
                raise forms.ValidationError(
                    "Username exists, please choose another username"
                )
        except User.DoesNotExist:
            return
