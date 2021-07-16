from .base import *

SECRET_KEY = 'asdasdasdasds'

ALLOWED_HOSTS = ["*"]

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gapbug', 
        'USER': os.getenv("db_user", "postgres"), 
        'PASSWORD': os.getenv("db_password", "pawndarby"),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
        'TEST': {
            'NAME': 'gapbug_test',
        },
    }
}

INSTALLED_APPS.append('rosetta')
INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_INFO = 'email_name@example.com'
DEFAULT_FROM_EMAIL = 'email_name@example.com'