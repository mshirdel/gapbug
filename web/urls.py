from django.views.generic import TemplateView
from django.urls import path


app_name = 'web'

urlpatterns = [
    path('', TemplateView.as_view(template_name="web/index.html"),
         name="home"),
]
