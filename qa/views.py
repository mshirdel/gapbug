from django.shortcuts import render
from .models import Question


def index(request):
    questions = Question.objects.all()[:10]
    return render(request, 'qa/index.html',
                  {
                      'questions': questions
                  })
