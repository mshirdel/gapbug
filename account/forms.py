from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from .fields import ASCIIUsernameField


class UserRegistrationForm(forms.ModelForm):
    # email = forms.EmailField(
    #     label=_("Email"),
    #     required=True,
    #     widget=forms.EmailInput(attrs={"class": "form-control"}),
    # )
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
        field_classes = {"username": ASCIIUsernameField}

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError(_("Password don't match."))
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError(_("Email field is mandatory."))
        if User.objects.filter(email__iexact=email).exists():
            self.add_error("email", _("Email must be unique."))
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username).exists():
            self.add_error("username", _("A user with this username already exists."))
        return username


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
