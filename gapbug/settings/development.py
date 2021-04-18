from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
SECRET_KEY = 'o8t2%j=a6h^nq7y#n0r0t#(qetfb(=e-mz3y+q3!-8^uvxat(v'

ALLOWED_HOSTS = ['localhost', '192.168.1.37']

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gapbug',
        'USER': 'meysam',
        'PASSWORD': 'pg123',
        'HOST': '',
        'PORT': '5432',
    }
}

INSTALLED_APPS.append('rosetta')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
