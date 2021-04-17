from django.shortcuts import get_object_or_404, render
from django.views import View
from django.urls import reverse
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Question, Answer


class QuestionList(ListView):
    queryset = Question.objects.all()
    context_object_name = 'questions'
    paginate_by = 50
    template_name = 'qa/index.html'


class Ask(View):
    def get(self, request):
        return render(request, 'qa/ask_question.html')

    def post(self, request):
        question = Question.objects.create(user=self.request.user,
                                           title=request.POST['title'],
                                           body_md=request.POST['body_md'])
        messages.add_message(request, messages.INFO,
                             _('Your question saved.'))
        return HttpResponseRedirect(reverse("qa:show",
                                            kwargs={
                                                "id": question.pk,
                                                "slug": question.slug
                                            }))


def show(request, id, slug):
    question = get_object_or_404(Question, pk=id, slug=slug)
    return render(request, 'qa/question.html', {'question': question})


class AnswerQuestion(View):
    def post(self, request, id):
        q = get_object_or_404(Question, id=id)
        if request.POST['body_md']:
            Answer.objects.create(user=request.user,
                                  question=q,
                                  body_md=request.POST['body_md'])
            messages.add_message(request, messages.INFO,
                                 _('Your answer saved'))
        else:
            messages.add_message(request, messages.WARNING,
                                 _('Please enter your answer'))
        return HttpResponseRedirect(reverse("qa:show",
                                            kwargs={
                                                "id": q.pk,
                                                "slug": q.slug
                                            }))
