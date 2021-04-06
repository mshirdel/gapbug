from datetime import datetime
from django.shortcuts import redirect
from django.views import View
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib import messages
from .tokens import email_verification_token


class EmailVerify(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            user_id = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and \
                email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            user.profile.is_email_verified = True
            user.profile.email_verify_date = datetime.now()
            user.profile.save()
            messages.add_message(request, messages.INFO,
                                 _('Yout email address verified successfuly.'))
        else:
            messages.add_message(request, messages.WARNING,
                                 _('Error in email verification.'))
        return redirect('web:home')
