from django import forms
from django.forms import fields, widgets
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "title",
            "about_me",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "about_me": forms.HiddenInput(attrs={"id": "aboutMeEditor"}),
        }


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("avatar",)
