from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import Profile


class UserCreationTest(TestCase):
    def setUp(self):
        u = User.objects.create(
            username="john", email="john@gmail.com", password="thepassword"
        )
        Profile.objects.create(user=u)

    def test_profile_reputation(self):
        u = User.objects.get(username="john")
        self.assertEqual(u.profile.reputation, 1)
