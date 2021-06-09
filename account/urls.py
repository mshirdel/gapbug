from django.urls import path, include

from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('sign-in/', views.LoginView.as_view(), name='signin'),
    path('register/', views.register, name="register"),
]
