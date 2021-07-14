from datetime import datetime
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView
from django.conf import settings
from .tokens import email_verification_token
from .forms import ProfileForm, ProfileAvatarForm
from account.forms import UserForm


class EmailVerify(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            user_id = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            user.profile.is_email_verified = True
            user.profile.email_verify_date = datetime.now()
            user.profile.save()
            messages.add_message(
                request, messages.INFO, _("Yout email address verified successfuly.")
            )
        else:
            messages.add_message(
                request, messages.WARNING, _("Error in email verification.")
            )
        return redirect("web:home")


def profile(request, id, username):
    user = get_object_or_404(User, pk=id, username=username)
    questions = user.questions.all()[:10]
    answers = user.answers.all()[:10]
    return render(
        request,
        "user_profile/profile.html",
        {"user": user, "questions": questions, "answers": answers},
    )


@method_decorator(login_required, name="dispatch")
class ProfileEdit(View):
    def get(self, request, user_id, user_name):
        user = get_object_or_404(User, pk=user_id, username=user_name)
        if request.user != user:
            raise PermissionDenied
        profile_form = ProfileForm(instance=user.profile)
        user_form = UserForm(instance=user)
        return render(
            request,
            "user_profile/profile_edit.html",
            {"profile_form": profile_form, "user_form": user_form, "user": user},
        )

    def post(self, request, user_id, user_name):
        user = get_object_or_404(User, pk=user_id)
        if request.user != user:
            raise PermissionDenied
        profile_form = ProfileForm(request.POST, instance=user.profile)
        user_form = UserForm(request.POST, instance=user)
        forms_has_error = False
        if user_form.is_valid():
            user_form.save()
            messages.add_message(
                request, messages.INFO, _("Your account info updatd successfully")
            )
        else:
            for error in user_form.errors:
                messages.add_message(request, messages.WARNING, error)
            forms_has_error = True

        if profile_form.is_valid():
            profile_form.save()
            messages.add_message(
                request, messages.INFO, _("Your profile updatd successfully")
            )
        else:
            for error in profile_form.errors:
                messages.add_message(request, messages.WARNING, error)
            forms_has_error = True

        if forms_has_error:
            return render(
                request,
                "user_profile/profile_edit.html",
                {"profile_form": profile_form, "user_form": user_form, "user": user},
            )
        else:
            return HttpResponseRedirect(
                reverse(
                    "user_profile:profile",
                    kwargs={"id": user_id, "username": user_name},
                )
            )


@method_decorator(login_required, name="dispatch")
class ProfileImageUplade(View):
    """
    Handle ajax requests for uploading profile image.
    """

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = ProfileAvatarForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    "user_profile:edit",
                    kwargs={"user_id": user.id, "user_name": user.username},
                )
            )
        else:
            return JsonResponse({"status": form.errors})


class UsersList(ListView):
    """
    Show list of all users that have profile. Admin user don't have profile!
    """

    queryset = User.objects.filter(profile__isnull=False).order_by(
        "-profile__reputation"
    )
    context_object_name = "users"
    paginate_by = settings.LARGE_PAGE_SIZE
    template_name = "user_profile/users_list.html"
