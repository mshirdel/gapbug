from django.urls import path
from . import views


app_name = "user_profile"

urlpatterns = [
    path('activate/<uidb64>/<token>/',
         views.EmailVerify.as_view(), name="activate"),
    path('<int:id>/<str:username>/', views.profile, name="profile"),
    path('<int:user_id>/<str:user_name>/edit', views.ProfileEdit.as_view(),
         name='edit'),
]
