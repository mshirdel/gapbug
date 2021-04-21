from qa.privilages import Privilages
from django.test import TestCase
from django.contrib.auth.models import User
from user_profile.models import Profile


class PrivilagesTest(TestCase):
    def setUp(self):
        u = User.objects.create_user(
            'john', 'lennon@google.com', 'thepassword')
        Profile.objects.create(user=u)

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
