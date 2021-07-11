from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext as _

from .forms import UserRegistrationForm, LoginForm
from user_profile.models import Profile


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.is_active = False
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            profile.send_verification_email(request)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        form = UserRegistrationForm()
    return render(request, "account/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        next_url = ""
        if request.GET.get("next"):
            next_url = request.GET.get("next")
        return render(
            request,
            "registration/login.html",
            {
                "next": next_url,
            },
        )

    def post(self, request):
        form = LoginForm(request.POST)
        errors = []
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user:
                if user.profile.is_email_verified:
                    login(request, user)
                    if request.POST["next"]:
                        return HttpResponseRedirect(request.POST["next"])
                    else:
                        return HttpResponseRedirect(reverse("qa:index"))
                else:
                    errors.append(
                        _(
                            "Your email is not verified.\
                         we sent a verification email to you."
                        )
                    )
                    login(request, user)
                    user.profile.send_verification_email(request)
                    logout(request)
                    return render(
                        request,
                        "registration/login.html",
                        {"next": request.POST["next"], "errors": errors},
                    )
            else:
                errors.append(
                    _(
                        "Your username and password didn't match.\
                                    Please try again."
                    )
                )
                return render(
                    request,
                    "registration/login.html",
                    {"next": request.POST["next"], "errors": errors},
                )
        else:
            return render(
                request,
                "registration/login.html",
                {
                    "next": request.POST["next"],
                    "errors": form.errors,
                },
            )
