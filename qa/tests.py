from qa.privilages import Privilages
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Question, Answer
from .reputations import Reputation


class PrivilagesTest(TestCase):
    def setUp(self):
        u = User.objects.create_user("john", "lennon@google.com", "thepassword")

        Question.objects.create(
            user=u, title="question1 title", body_md="<p>question1 body</p>"
        )

    def test_user_defualt_reputation(self):
        u = User.objects.get(username="john")
        self.assertEqual(u.profile.privilages(), ["create_post"])

    def test_privilage_check_default_privilage(self):
        u = User.objects.get(username="john")
        p = Privilages(u)
        self.assertTrue(p.check_privilage("create_post"))

    def test_privilage_check_privilage(self):
        u = User.objects.get(username="john")
        u.profile.reputation = 50
        u.save()
        self.assertEqual(len(u.profile.privilages()), 4)
        self.assertEqual(
            u.profile.privilages(),
            ["create_post", "vote_up", "flag_posts", "comment_everywhere"],
        )
        self.assertNotIn("vote_down", u.profile.privilages())
        self.assertNotIn("trusted_user", u.profile.privilages())
        p = Privilages(u)
        self.assertTrue(p.check_privilage("create_post"))
        self.assertTrue(p.check_privilage("vote_up"))
        self.assertTrue(p.check_privilage("flag_posts"))
        self.assertTrue(p.check_privilage("comment_everywhere"))
        self.assertFalse(p.check_privilage("vote_down"))
        self.assertFalse(p.check_privilage("trusted_user"))


class QuestionsTest(TestCase):
    def setUp(self) -> None:
        u = User.objects.create_user("john", "lennon@google.com", "thepassword")

        u15 = User.objects.create_user("user_15", "user15@gmail.com", "thepassword")
        u15.profile.reputation = 15
        u15.profile.save()

        u150 = User.objects.create_user("user_150", "user150@gmail.com", "thepassword")
        u150.profile.reputation = 150
        u150.profile.save()

        Question.objects.create(
            user=u, title="question1 title", body_md="<p>question1 body</p>"
        )

    def test_question_show_view(self):
        c = Client()
        q = Question.objects.get(title="question1 title")
        response = c.get(f"/questions/show/{q.id}/{q.slug}")
        self.assertEqual(response.status_code, 200)

    def test_question_voteup_fail(self):
        c = Client()
        q = Question.objects.get(title="question1 title")
        u = User.objects.get(username="john")
        self.assertTrue(c.login(username=u.username, password="thepassword"))
        response = c.post(f"/questions/{q.id}/up")
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 403)

    def test_question_voteup_success(self):
        c = Client()
        q = Question.objects.get(title="question1 title")
        question_owner_reputation = q.user.profile.reputation
        u15 = User.objects.get(username="user_15")
        self.assertTrue(c.login(username=u15.username, password="thepassword"))
        response = c.post(f"/questions/{q.id}/up")
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 200)
        q = Question.objects.get(title="question1 title")
        self.assertEqual(q.vote, 1)
        self.assertEqual(
            question_owner_reputation + Reputation.QUESTION_VOTE_UP.value,
            q.user.profile.reputation,
        )

    def test_question_votedown_fail(self):
        c = Client()
        q = Question.objects.get(title="question1 title")
        u = User.objects.get(username="john")
        response = c.post(f"/questions/{q.id}/down")
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(c.login(username=u.username, password="thepassword"))
        response = c.post(f"/questions/{q.id}/down")
        self.assertEqual(response.status_code, 403)

    def test_question_votedown_success(self):
        c = Client()
        q = Question.objects.get(title="question1 title")
        question_owner_reputation = q.user.profile.reputation
        before_vote = q.vote
        u150 = User.objects.get(username="user_150")
        response = c.post(f"/questions/{q.id}/down")
        self.assertNotEqual(response.status_code, 404)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(c.login(username=u150.username, password="thepassword"))
        response = c.post(f"/questions/{q.id}/down")
        self.assertEqual(response.status_code, 200)
        q = Question.objects.get(title="question1 title")
        self.assertEqual(q.vote, before_vote - 1)
        self.assertEqual(
            question_owner_reputation + Reputation.QUESTION_VOTE_DOWN.value,
            q.user.profile.reputation,
        )


class AnswersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("john", "lennon@google.com", "thepassword")

        self.u15 = User.objects.create_user(
            "user_15", "user15@gmail.com", "thepassword"
        )
        self.u15.profile.reputation = 15
        self.u15.profile.save()

        self.u150 = User.objects.create_user(
            "user_150", "user150@gmail.com", "thepassword"
        )
        self.u150.profile.reputation = 150
        self.u150.profile.save()

        self.question = Question.objects.create(
            user=self.user, title="question1 title", body_md="<p>question1 body</p>"
        )

        self.ans1 = Answer.objects.create(
            user=self.user, question=self.question, body_html="answer1"
        )

        self.ans2 = Answer.objects.create(
            user=self.user, question=self.question, body_html="answer2"
        )

    def test_answer_voteup_fail_user_not_authenticated(self):
        c = Client()
        ans = self.question.answer_set.first()
        resp = c.post(f"/questions/{self.question.id}/{ans.id}/up")
        self.assertEqual(resp.status_code, 302)

    def test_answer_voteup_fail_user_not_authorized(self):
        c = Client()
        ans = self.question.answer_set.first()
        self.assertTrue(c.login(username=self.user.username, password="thepassword"))
        resp = c.post(f"/questions/{self.question.id}/{ans.id}/up")
        self.assertEqual(resp.status_code, 403)

    def test_answer_voteup(self):
        c = Client()
        answer_owner_rep_before = self.ans1.user.profile.reputation
        self.assertEqual(answer_owner_rep_before, 1)
        self.assertTrue(c.login(username=self.u15, password="thepassword"))
        resp = c.post(f"/questions/{self.ans1.question.id}/{self.ans1.id}/up")
        self.assertEqual(resp.status_code, 200)
        answer_after_vote = Answer.objects.get(pk=self.ans1.id)
        answer_owner_rep_after = answer_after_vote.user.profile.reputation
        self.assertNotEqual(answer_after_vote.vote, self.ans1.vote)
        self.assertEqual(answer_after_vote.vote, self.ans1.vote + 1)
        self.assertNotEqual(answer_owner_rep_before, answer_owner_rep_after)
        self.assertEqual(
            answer_owner_rep_after,
            answer_owner_rep_before + Reputation.ANSWER_VOTE_UP.value,
        )

    def test_answer_votedown_fail_user_not_authenticated(self):
        c = Client()
        answer = self.question.answer_set.first()
        resp = c.post(f"/questions/{self.question.id}/{answer.id}/down")
        self.assertNotEqual(resp.status_code, 404)
        self.assertEqual(resp.status_code, 302)

    def test_answer_votedown_fail_user_not_authorized(self):
        c = Client()
        ans = self.question.answer_set.first()
        self.assertTrue(c.login(username=self.user.username, password="thepassword"))
        resp = c.post(f"/questions/{self.question.id}/{ans.id}/down")
        self.assertEqual(resp.status_code, 403)

    def test_answer_votedown(self):
        c = Client()
        answer_owner_rep_before = self.ans2.user.profile.reputation
        self.assertEqual(answer_owner_rep_before, 1)
        self.assertTrue(c.login(username=self.u150, password="thepassword"))
        resp = c.post(f"/questions/{self.question.id}/{self.ans2.id}/down")
        self.assertEqual(resp.status_code, 200)
        answer_after_vote = Answer.objects.get(pk=self.ans2.id)
        answer_owner_rep_after = answer_after_vote.user.profile.reputation
        self.assertNotEqual(answer_after_vote.vote, self.ans2.vote)
        self.assertEqual(answer_after_vote.vote, self.ans2.vote - 1)
        self.assertNotEqual(answer_owner_rep_before, answer_owner_rep_after)
        self.assertEqual(
            answer_owner_rep_after,
            answer_owner_rep_before + Reputation.ANSWER_VOTE_DOWN.value,
        )


class QuestionPageTest(TestCase):
    fixtures = ["fixture.json"]

    def setUp(self):
        self.client = Client()

    def test_user_can_not_answer_a_question_two_times(self):
        self.assertTrue(self.client.login(username="user15", password="thepassword"))
        resp = self.client.get("/questions/show/1/question-1")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context["show_answer_form"])

    def test_user_can_answer_a_question(self):
        self.assertTrue(self.client.login(username="user1", password="thepassword"))
        resp = self.client.get("/questions/show/1/question-1")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["show_answer_form"])
