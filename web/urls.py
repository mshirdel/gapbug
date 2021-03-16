from django.views.generic import TemplateView
from django.urls import path
from . import views


app_name = 'web'

urlpatterns = [
    path('', views.index, name="home"),
]
