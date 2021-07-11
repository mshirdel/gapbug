from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name = "web"

urlpatterns = [
    path("", views.index, name="home"),
    path("about", TemplateView.as_view(template_name="web/about.html"), name="about"),
    path("help", TemplateView.as_view(template_name="web/help.html"), name="help"),
    path("trix/upload/", views.TrixUploadFile.as_view()),
]
