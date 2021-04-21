import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from user_profile.tokens import email_verification_token
from common.models import TimeStampModel
from qa.privilages import Privilages


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    email_verify_date = models.DateTimeField(blank=True, null=True)
    reputation = models.IntegerField(default=1)

    def send_verification_email(self, request):
        current_site = get_current_site(request)
        subject = _("Please verify your email")
        message = render_to_string('user_profile/verify_email.html', {
            'user': self.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': email_verification_token.make_token(self.user)
        })
        send_mail(subject,
                  message,
                  settings.EMAIL_INFO,
                  [self.user.email],
                  fail_silently=False)

    def privilages(self):
        return Privilages(self.user).get_user_privilages()

    def has_privilage(self, privilage):
        return privilage in self.privilages()


# class ReputationHistory(TimeStampModel):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)
#     cause = models.TextChoices('A', 'B')
