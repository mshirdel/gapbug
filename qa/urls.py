from django.urls import path
from . import views


app_name = "qa"

urlpatterns = [
    path('', views.QuestionList.as_view(), name="index"),
    path('ask', views.Ask.as_view(), name='question'),
    path('show/<int:id>/<str:slug>', views.show, name='show'),
    path('<int:id>/answer/submit', views.AnswerQuestion.as_view(),
         name='submit_answer'),
    path('<int:question_id>/up', views.QuestionVoteUp.as_view(),
         name="question_vote_up"),
    path('<int:question_id>/down', views.QuestionVoteDown.as_view(),
         name="question_vote_down"),
    path('<int:question_id>/edit', views.EditQuestion.as_view(),
         name="question_edit"),
    path('<int:question_id>/edit/answer/<int:answer_id>',
         views.EditAnswer.as_view(), name='answer_edit'),
    path('<int:question_id>/<int:answer_id>/up',
         views.AnswerVoteUp.as_view(), name='answer_voteup'),
]
