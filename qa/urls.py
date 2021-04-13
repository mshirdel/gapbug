from django.urls import path
from . import views


app_name = "qa"

urlpatterns = [
    path('', views.QuestionList.as_view(), name="index"),
    path('ask', views.Ask.as_view(), name='question'),
    path('show/<int:id>/<str:slug>', views.show, name='show')
]
