from django.urls import path
from . import views
from qa.views import UserAnswerList, UserQuestionList


app_name = "user_profile"

urlpatterns = [
    path('activate/<uidb64>/<token>/',
         views.EmailVerify.as_view(), name="activate"),
    path('<int:id>/<str:username>/', views.profile, name="profile"),
    path('<int:user_id>/<str:user_name>/edit', views.ProfileEdit.as_view(),
         name='edit'),
    path('avatar/upload/', views.ProfileImageUplade.as_view(),
         name="avatar_upload"),
    path('<int:user_id>/<str:user_name>/questions',
         UserQuestionList.as_view(), name='user_questions_list'),
    path('<int:user_id>/<str:user_name>/answers',
         UserAnswerList.as_view(), name='user_answers_list'),
]
