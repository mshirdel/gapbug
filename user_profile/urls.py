from django.urls import path
from . import views


app_name = "user_profile"

urlpatterns = [
    path('activate/<uidb64>/<token>/',
         views.EmailVerify.as_view(), name="activate"),
]
