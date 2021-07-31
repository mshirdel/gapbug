from django.test import TestCase
from django.contrib.auth.models import User


class ProfileTest(TestCase):
    def test_creating_profile(self):
        user = User.objects.create(
            username="username1", email="username@gmail.com", password="password1"
        )
        self.assertEqual(user.profile.reputation, 1)
