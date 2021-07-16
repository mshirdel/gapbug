# gapbug
QA site with Python/Django

Gapbug is a Question and Answers Django project like stackoverflow created for personal learning web application development with python. 

The mechanisms used here are almost similar to Stockflow, which makes the focus more on the question and the answer, rather than on forums, a place to discuss issues. 

We will be happy to report any problems with the code or any idea to make this project better.

Tech Stack:
* Programming language: [Python](https://www.python.org/)
* Backend Web framework: [Django](https://www.djangoproject.com/)
* UI framework: [Bootstrap](https://getbootstrap.com/)
* Database: [Postgresql](https://www.postgresql.org/)
* Deoploy platform: [Liara](https://liara.ir/) - [More info for deployment](https://docs.liara.ir/app-deploy/django/getting-started)


# Install locally
```bash
python -m venv env
source env/bin/activate
git clone https://github.com/mshirdel/gapbug.git
cd gapbug
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

For local development setting use this config as gapbug/settings/development.py

```python
SECRET_KEY = '[your-secret-key]'

ALLOWED_HOSTS = []

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gapbug',
        'USER': '[your-database-user]',
        'PASSWORD': '[your-database-password]',
        'HOST': '',
        'PORT': '5432',
    }
}

INSTALLED_APPS.append('rosetta')
INSTALLED_APPS.append('django_extensions')
INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_INFO = 'email_name@example.com'
DEFAULT_FROM_EMAIL = 'email_name@example.com'
```

Migrate database and run project:
```
python manage.py migrate
python manage.py runserver
```

# Todo features:
- [ ] Add comment to questions and answers (Work in progress with @MojixCoder)
- [ ] Help center
- [ ] Add more test
- [ ] Search users in user section
- [ ] Show online status of users (django-channels)
- [ ] Flag questions as spam
- [ ] Add SEO features
- [ ] Add social links to user profile
- [ ] Add contact us
