from django.contrib.auth.models import User
from django.test import TestCase, Client

from account.forms import UserRegistrationForm


class RegisterFormTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        url = '/auth/register/'
        data = {'email': 'testclient@example.com', 'password': 'password', 'password2': 'password', 'username': 'test'}

        self.client.post(url, data=data, format='json')
        self.user = User.objects.get(email="testclient@example.com")

    def test_invalid_email(self):
        data = {'email': 'not valid', 'password': 'password', 'password2': 'password', 'username': 'zahra'}
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email'].errors, ['یک ایمیل آدرس معتبر وارد کنید.'])

    def test_invalid_password(self):
        data = {'email': 'test@gmail.com', 'password': 'password', 'password2': 'passwordk', 'username': 'zahra'}
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password2'].errors, ['رمزهای عبور مطابقت ندارند'])

    def test_duplicate_email(self):
        data = {'email': 'testclient@example.com', 'password': 'password', 'password2': 'password',
                'username': 'zahra'}
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email'].errors, ['از ایمیل تکراری استفاده شده است'])

    def test_duplicate_username(self):
        data = {'email': 'test@example.com', 'password': 'password', 'password2': 'password',
                'username': 'test'}
        form = UserRegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['username'].errors, ['A user with this username already exists.'])

    def test_success(self):
        # The success case.
        data = {'email': 'testSuccess@example.com', 'password': 'password', 'password2': 'password',
                'username': 'testSuccess'}
        form = UserRegistrationForm(data)
        self.assertTrue(form.is_valid())
        form.save(commit=False)
        u = form.save()
        self.assertEqual(repr(u), '<User: testSuccess>')
