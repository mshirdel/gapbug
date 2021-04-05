import uuid
from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    email_verify_date = models.DateTimeField(blank=True, null=True)
