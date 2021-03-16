from django.urls import path, include

from . import views

app_name = 'auth'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
]
