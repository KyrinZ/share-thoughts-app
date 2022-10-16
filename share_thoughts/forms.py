from django import forms
from .models import *
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text_field']
        widgets = {
            'text_field': forms.Textarea(attrs={'placeholder': 'Share thoughts', 'rows': 10})
        }

    def clean(self):
        if not self.cleaned_data.get('text_field') and not self.cleaned_data.get('image_field'):
            raise forms.ValidationError(
                "You cant keep both field empty"
            )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text_field']
        widgets = {
            'text_field': forms.Textarea(attrs={'placeholder': 'Comments', 'rows': 1})
        }

    def clean(self):
        if not self.cleaned_data.get('text_field') and not self.cleaned_data.get('image_field'):
            raise forms.ValidationError(
                "You cant keep both field empty"
            )
