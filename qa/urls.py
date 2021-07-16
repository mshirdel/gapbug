from django.urls import path, include
from rest_framework import routers
from . import views, apis


router = routers.DefaultRouter()

# Comment, CommentVote ViewSet
#TODO Add CommentVoteViewSet
router.register('comment', apis.CommentViewSet, basename="comment")


app_name = "qa"

urlpatterns = [
    path("", views.QuestionList.as_view(), name="index"),
    path("ask", views.Ask.as_view(), name="question"),
    path("show/<int:id>/<str:slug>", views.show, name="show"),
    path(
        "<int:id>/answer/submit", views.AnswerQuestion.as_view(), name="submit_answer"
    ),
    path(
        "<int:question_id>/up", views.QuestionVoteUp.as_view(), name="question_vote_up"
    ),
    path(
        "<int:question_id>/down",
        views.QuestionVoteDown.as_view(),
        name="question_vote_down",
    ),
    path("<int:question_id>/edit", views.EditQuestion.as_view(), name="question_edit"),
    path("<int:pk>/delete/", views.DeleteQuestion.as_view(), name="question_delete"),
    path(
        "<int:question_id>/answer/<int:pk>/delete/",
        views.DeleteAnswer.as_view(),
        name="answer_delete",
    ),
    path(
        "<int:question_id>/edit/answer/<int:answer_id>",
        views.EditAnswer.as_view(),
        name="answer_edit",
    ),
    path(
        "<int:question_id>/<int:answer_id>/up",
        views.AnswerVoteUp.as_view(),
        name="answer_voteup",
    ),
    path(
        "<int:question_id>/<int:answer_id>/down",
        views.AnswerVoteDown.as_view(),
        name="answer_voteup",
    ),
    path(
        "<int:question_id>/<int:answer_id>/accept",
        views.AcceptAnswer.as_view(),
        name="accept_answer",
    ),
    path("search/", views.Search.as_view(), name="search"),
    path("tags/", views.TagList.as_view(), name="tags_list"),
    path("tags/<str:tag>/", views.QuestionByTag.as_view(), name="by_tag"),
    path("tagslist/", views.QuestionTagList.as_view(), name="all_tags"),
    
    # Router Urls
    path("api/", include(router.urls)),
]
