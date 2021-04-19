from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('account.urls')),
    path('', include('web.urls', namespace='web')),
    path('questions/', include('qa.urls', namespace='qa')),
    path('profile/', include('user_profile.urls', namespace='user_profile')),
    path('__debug__/', include(debug_toolbar.urls)),
]

if settings.DEBUG:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),
    ]
