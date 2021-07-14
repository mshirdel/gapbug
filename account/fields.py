from django.contrib.auth.forms import UsernameField
from django.contrib.auth.validators import ASCIIUsernameValidator


class ASCIIUsernameField(UsernameField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(ASCIIUsernameValidator())
