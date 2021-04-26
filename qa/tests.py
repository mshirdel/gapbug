from qa.privilages import Privilages
from django.test import TestCase, Client
from django.contrib.auth.models import User
from user_profile.models import Profile
from .models import Question


class PrivilagesTest(TestCase):
    def setUp(self):
        u = User.objects.create_user(
            'john', 'lennon@google.com', 'thepassword')
        Profile.objects.create(user=u)

        q = Question.objects.create(user=u,
                                    title='question1 title',
                                    body_md='<p>question1 body</p>')

    def test_user_defualt_reputation(self):
        u = User.objects.get(username='john')
        self.assertEqual(u.profile.privilages(), ['create_post'])

    def test_privilage_check_default_privilage(self):
        u = User.objects.get(username='john')
        p = Privilages(u)
        self.assertTrue(p.check_privilage('create_post'))

    def test_privilage_check_privilage(self):
        u = User.objects.get(username='john')
        u.profile.reputation = 50
        u.save()
        self.assertEqual(len(u.profile.privilages()), 4)
        self.assertEqual(u.profile.privilages(),
                         ['create_post', 'vote_up',
                         'flag_posts', 'comment_everywhere'])
        self.assertNotIn('vote_down', u.profile.privilages())
        self.assertNotIn('trusted_user', u.profile.privilages())
        p = Privilages(u)
        self.assertTrue(p.check_privilage('create_post'))
        self.assertTrue(p.check_privilage('vote_up'))
        self.assertTrue(p.check_privilage('flag_posts'))
        self.assertTrue(p.check_privilage('comment_everywhere'))
        self.assertFalse(p.check_privilage('vote_down'))
        self.assertFalse(p.check_privilage('trusted_user'))


class QuestionsTest(TestCase):
    def setUp(self) -> None:
        u = User.objects.create_user(
            'john', 'lennon@google.com', 'thepassword')
        Profile.objects.create(user=u)

        u15 = User.objects.create_user(
            'user_15', 'user15@gmail.com', 'thepassword')
        Profile.objects.create(user=u15, reputation=15)

        u150 = User.objects.create_user(
            'user_150', 'user150@gmail.com', 'thepassword')
        Profile.objects.create(user=u150, reputation=150)

        q = Question.objects.create(user=u,
                                    title='question1 title',
                                    body_md='<p>question1 body</p>')

    def test_question_show_view(self):
        c = Client()
        q = Question.objects.get(title='question1 title')
        response = c.get(f'/questions/show/{q.id}/{q.slug}')
        self.assertEqual(response.status_code, 200)

    def test_question_voteup_fail(self):
        c = Client()
        q = Question.objects.get(title='question1 title')
        u = User.objects.get(username='john')
        self.assertTrue(c.login(username=u.username, password='thepassword'))
        response = c.post(f'/questions/{q.id}/up')
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 403)

    def test_question_voteup_success(self):
        c = Client()
        q = Question.objects.get(title='question1 title')
        u15 = User.objects.get(username='user_15')
        self.assertTrue(c.login(username=u15.username, password='thepassword'))
        response = c.post(f'/questions/{q.id}/up')
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 200)
        q = Question.objects.get(title='question1 title')
        self.assertEqual(q.vote, 1)

    def test_question_votedown_fail(self):
        c = Client()
        q = Question.objects.get(title='question1 title')
        u = User.objects.get(username='john')
        response = c.post(f'/questions/{q.id}/down')
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(c.login(username=u.username, password='thepassword'))
        response = c.post(f'/questions/{q.id}/down')
        self.assertEqual(response.status_code, 403)

    def test_question_votedown_success(self):
        c = Client()
        q = Question.objects.get(title='question1 title')
        before_vote = q.vote
        u150 = User.objects.get(username='user_150')
        response = c.post(f'/questions/{q.id}/down')
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            c.login(username=u150.username, password='thepassword'))
        response = c.post(f'/questions/{q.id}/down')
        self.assertEqual(response.status_code, 200)
        q = Question.objects.get(title='question1 title')
        self.assertEqual(q.vote, before_vote-1)
