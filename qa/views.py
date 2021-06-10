from django.utils import timezone
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator

from .models import (
    Question,
    Answer,
    QuestionVote,
    AnswerVote,
    QuestionHitCount)
from user_profile.models import ReputationHistory
from .reputations import Reputation
from .mixins import PrivilageRequiredMixin
from common.utils import get_finger_print
from .forms import QuestionForm


class QuestionList(ListView):
    queryset = Question.objects.all().prefetch_related('user', 'answer_set')
    context_object_name = 'questions'
    paginate_by = 10
    template_name = 'qa/index.html'


@method_decorator(login_required, name='dispatch')
class Ask(PrivilageRequiredMixin, View):
    privilage_required = 'create_post'

    def get(self, request):
        return render(request, 'qa/ask_question.html')

    def post(self, request):
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(
                user=self.request.user,
                title=form.cleaned_data['title'],
                body_html=form.cleaned_data['body_html'])
            messages.add_message(request, messages.INFO,
                                 _('Your question saved.'))
            return redirect(question)
        else:
            return render(request, 'qa/ask_question.html',
                          {
                              'form': form
                          })


@method_decorator(login_required, name='dispatch')
class EditQuestion(View):

    def get(self, request, question_id):
        q = get_object_or_404(Question, pk=question_id)
        return render(request, 'qa/edit_question.html',
                      {'question': q})

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            if request.POST['title']:
                question.title = request.POST['title']
            if request.POST['body_html']:
                question.body_html = request.POST['body_html']
            question.content_modified_date = timezone.now()
            question.save()
            messages.add_message(request, messages.INFO,
                                 _('Question updated'))
        except Exception as ex:
            # TODO log exception
            messages.add_message(request, messages.WARNING,
                                 _('Some error in updating question'))
        return redirect(question)


def show(request, id, slug):
    question = get_object_or_404(Question, pk=id, slug=slug)
    QuestionHitCount.objects.create(
        question=question,
        fingerprint=get_finger_print(request))
    user_answered_befor = False
    if request.user.is_authenticated:
        if question.answer_set.filter(user=request.user):
            user_answered_befor = True
    return render(request, 'qa/question.html',
                  {
                      'question': question,
                      'show_answer_form': not user_answered_befor
                  })


@method_decorator(login_required, name='dispatch')
class AnswerQuestion(View):
    def post(self, request, id):
        question = get_object_or_404(Question, id=id)
        if request.POST['body_html']:
            Answer.objects.create(user=request.user,
                                  question=question,
                                  body_html=request.POST['body_html'])
            messages.add_message(request, messages.INFO,
                                 _('Your answer saved'))
        else:
            messages.add_message(request, messages.WARNING,
                                 _('Please enter your answer'))
        return redirect(question)


@method_decorator(login_required, name='dispatch')
class QuestionVoteUp(PrivilageRequiredMixin, View):
    privilage_required = 'vote_up'

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            qv = QuestionVote.objects.create(
                user=request.user,
                question=question,
                rate=1)
            if qv:
                ReputationHistory.objects.create(
                    user=question.user,
                    cause=Reputation.QUESTION_VOTE_UP.name,
                    reputation=Reputation.QUESTION_VOTE_UP.value
                )
            return JsonResponse({
                'status': 'ok',
                'vote': Question.objects.get(pk=question_id).vote
            })
        except Exception as ex:
            return JsonResponse({
                'status': 'error'
            })


@method_decorator(login_required, name='dispatch')
class QuestionVoteDown(PrivilageRequiredMixin, View):
    privilage_required = 'vote_down'

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            qv = QuestionVote.objects.create(
                user=request.user,
                question=question,
                rate=-1)
            if qv:
                ReputationHistory.objects.create(
                    user=question.user,
                    cause=Reputation.QUESTION_VOTE_DOWN.name,
                    reputation=Reputation.QUESTION_VOTE_DOWN.value
                )
            return JsonResponse({
                'status': 'ok',
                'vote': Question.objects.get(pk=question_id).vote
            })
        except Exception as ex:
            return JsonResponse(
                {
                    'status': 'error'
                })


@method_decorator(login_required, name='dispatch')
class EditAnswer(View):

    def get(self, request, question_id, answer_id):
        q = get_object_or_404(Question, pk=question_id)
        ans = get_object_or_404(Answer, pk=answer_id)
        return render(request, 'qa/edit_answer.html',
                      {'answer': ans, 'question': q})

    def post(self, request, question_id, answer_id):
        question = get_object_or_404(Question, pk=question_id)
        ans = get_object_or_404(Answer, pk=answer_id)
        try:
            if request.POST['body_html']:
                ans.body_html = request.POST['body_html']
                ans.save()
                messages.add_message(request, messages.INFO,
                                     _('Answer updated'))
        except Exception as ex:
            # TODO log ex
            messages.add_message(request, messages.WARNING,
                                 _('Some error in edditing answer.'))
        return redirect(question)


@method_decorator(login_required, name='dispatch')
class AnswerVoteUp(PrivilageRequiredMixin, View):
    privilage_required = 'vote_up'

    def post(self, request, question_id, answer_id):
        question = get_object_or_404(Question, pk=question_id)

        try:
            answer = question.answer_set.get(id=answer_id)
            av = AnswerVote.objects.create(
                user=request.user,
                answer=answer,
                rate=1)
            if av:
                ReputationHistory.objects.create(
                    user=answer.user,
                    cause=Reputation.ANSWER_VOTE_UP.name,
                    reputation=Reputation.ANSWER_VOTE_UP.value
                )
            return JsonResponse({
                'status': 'ok',
                'vote': Answer.objects.get(pk=answer_id).vote
            })
        except Exception as ex:
            return JsonResponse({
                'status': 'error'
            })


@method_decorator(login_required, name='dispatch')
class AnswerVoteDown(PrivilageRequiredMixin, View):
    privilage_required = 'vote_down'

    def post(self, request, question_id, answer_id):
        question = get_object_or_404(Question, pk=question_id)

        try:
            answer = question.answer_set.get(id=answer_id)
            av = AnswerVote.objects.create(
                user=request.user,
                answer=answer,
                rate=-1)
            if av:
                ReputationHistory.objects.create(
                    user=answer.user,
                    cause=Reputation.ANSWER_VOTE_DOWN.name,
                    reputation=Reputation.ANSWER_VOTE_DOWN.value
                )
            return JsonResponse({
                'status': 'ok',
                'vote': Answer.objects.get(pk=answer_id).vote
            })
        except Exception as ex:
            return JsonResponse({
                'status': 'error'
            })


@method_decorator(login_required, name='dispatch')
class AcceptAnswer(View):
    def post(self, request, question_id, answer_id):
        answer = get_object_or_404(Answer, pk=answer_id)
        question = get_object_or_404(Question, pk=question_id)
        if answer.question.id != question_id:
            return JsonResponse({
                'status': 'error',
                # TODO: log this error
            })
        if not question.accepted:
            answer.accepted = True
            answer.accepted_date = timezone.now()
            answer.save()
            question.accepted = True
            question.save()
            ReputationHistory.objects.create(
                user=answer.user,
                cause=Reputation.ANSWER_MARKED_ACCEPTED.name,
                reputation=Reputation.ANSWER_MARKED_ACCEPTED.value
            )
            ReputationHistory.objects.create(
                user=request.user,
                cause=Reputation.ANSWER_MARKED_ACCEPTED_ACCEPTOR.name,
                reputation=Reputation.ANSWER_MARKED_ACCEPTED_ACCEPTOR.value
            )
            return JsonResponse({
                'status': 'ok'
            })
        else:
            return JsonResponse({
                'status': 'not required'
            })


class UserQuestionList(ListView):
    context_object_name = 'questions'
    paginate_by = 10
    template_name = 'qa/questions_list.html'

    def get_queryset(self):
        user = get_object_or_404(User,
                                 pk=self.kwargs['user_id'],
                                 username=self.kwargs['user_name'])
        return Question.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_name"] = _('User questions list')
        user = get_object_or_404(User, pk=self.kwargs['user_id'],
                                 username=self.kwargs['user_name'])
        context["user_question_count"] = user.questions.count()
        return context


class UserAnswerList(ListView):
    context_object_name = 'answers'
    paginate_by = 10
    template_name = 'qa/answers_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['user_id'],
                                 username=self.kwargs['user_name'])
        return Answer.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_name"] = _('User answers list')
        user = get_object_or_404(User, pk=self.kwargs['user_id'],
                                 username=self.kwargs['user_name'])
        context["user_answer_count"] = user.answers.count()
        return context
