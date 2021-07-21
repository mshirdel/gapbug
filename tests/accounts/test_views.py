from http import HTTPStatus

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase


class RegisterViewTests(TestCase):
    def setUp(self):
        url = '/auth/register/'
        data = dict(password='password', username='sample', email='sample@gmail.com', password2='password')
        self.client.post(path=url, data=data, format='json')
        self.user = User.objects.get(email='sample@gmail.com')

    def test_invalid_username(self):
        url = '/auth/register/'
        data = dict(password='password', username='invalid۱۱۱', email='zz@gmail.com', password2='password')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertContains(
            response, 'یک نام کاربری معتبر وارد کنید. این مقدار میتواند فقط شامل حروف الفبای انگلیسی، اعداد، و علامات '
                      '@/./+/-/_ باشد.', html=True
        )

    def test_invalid_password(self):
        url = '/auth/register/'
        data = dict(password='password', password2='pass', username='test', email='test@gmail.com')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertContains(
            response, ' رمزهای عبور مطابقت ندارند', html=True
        )

    def test_success(self):
        url = '/auth/register/'
        data = dict(password='password', username='test', email='test@gmail.com', password2='password')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, ' رمزهای عبور مطابقت ندارند', html=True
        )
        self.assertTemplateUsed(response, 'account/register_done.html')
        self.assertContains(
            response, ' حساب کاربری جدید شما با موفقیت ساخته شد. ', html=True
        )

    def test_duplicate_email(self):
        url = '/auth/register/'
        data = dict(password='password', username='test', email='sample@gmail.com', password2='password')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertNotContains(
            response, ' حساب کاربری جدید شما با موفقیت ساخته شد. ', html=True
        )
        self.assertContains(
            response, 'از ایمیل تکراری استفاده شده است', html=True
        )

    def test_duplicate_username(self):
        url = '/auth/register/'
        data = dict(password='password', username='sample', email='test@gmail.com', password2='password')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertNotContains(
            response, ' حساب کاربری جدید شما با موفقیت ساخته شد. ', html=True
        )
        self.assertNotContains(
            response, 'از ایمیل تکراری استفاده شده است', html=True
        )
        self.assertContains(
            response, 'A user with this username already exists.', html=True
        )

    def test_not_confirm_email(self):
        url = '/auth/sign-in/'
        data = dict(password='password', username='sample@gmail.com', next='')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'user_profile/verify_email.html')
        self.assertContains(
            response, ' ایمیل شما تایید نشده است. ایمیل جدیدی برای تایید ارسال شد. ', html=True
        )

    def test_confirm_email(self):
        self.confirm_email()
        url = '/auth/sign-in/'
        data = dict(password='password', username='sample@gmail.com', next='')
        response = self.client.post(path=url, data=data, format='json', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(
            response, ' ایمیل شما تایید نشده است. ایمیل جدیدی برای تایید ارسال شد. ', html=True
        )

    def test_fail_login(self):
        url = '/auth/sign-in/'
        data = dict(password='wrong password', username='sample@gmail.com', next='')
        response = self.client.post(path=url, data=data, format='json', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Your username and password didn't match.                                    "
                                      "Please try again.", html=True)

    def test_successful_login(self):
        url = '/auth/sign-in/'
        data = dict(password='password', username='sample@gmail.com', next='')
        response = self.client.post(path=url, data=data, format='json', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "Your username and password didn't match.                                    "
                                         "Please try again.", html=True)
        self.assertContains(response, 'پرسش‌ها', html=True)

    def confirm_email(self):
        email_lines = mail.outbox[0].body.splitlines()
        activation_link = [email_line for email_line in email_lines if '/activate/' in email_line][0]
        uid, token, _ = activation_link.split('/')[-3:]
        data = {'uid': uid, 'token': token}
        url = '/users/activate/{}/{}/'.format(uid, token)
        self.client.get(url, data, format='json')
