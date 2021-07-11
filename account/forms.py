from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from django.utils.translation import gettext as _


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Passwrod"), widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label=_("Repeat password"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Password don't match."))
        return cd["password2"]

    def clean_email(self):
        cd = self.cleaned_data
        try:
            User.objects.get(email=cd["email"])
        except User.DoesNotExist:
            return cd["email"]
        raise forms.ValidationError(_("Email must be unique."))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
