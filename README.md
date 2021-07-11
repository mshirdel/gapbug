# gapbug
QA site with Python/Django

<p dir="rtl">
    اینجا مکانیست برای پرسش و پاسخ درباره برنامه‌نویسی مشابه سایت
    استک‌اورفلو. مکانیزم‌های بکار رفته در اینجا تقریبا شبیه به
    استک‌اورفلو است که باعث می‌شود تمرکز بیشتر بر پرسش و رسیدن به جواب
    آن باشد نه مانند فروم‌ها مکانی برای گفتگو در مورد مسایل. امکاناتی
    برای بهتر شدن در آینده نزدیک اضافه می‌شود که هم در استک‌اورفلو وجود
    دارد یا با توجه به نیاز امکاناتی جدید نسبت به استک‌اورفلو. کد این
    سایت به صورت منبع‌باز بوده و در <a href="https://github.com/mshirdel/gapbug">گیت‌هاب</a> قرار دارد. به تمام مشارکت
    کنندگان خوش‌آمد گفته می‌شود. هدف اولیه از ایجاد چنین سیستمی آشنایی
    من با توسعه وب در دنیای منبع‌باز با استفاده از زبان برنامه‌نویسی
    پایتون و فریم‌ورک وب جنگو بود.
</p>

<div dir="rtl">
    <p>
        تکنولوژی‌های بکار رفته:
        <ul>
        <li>زبان برنامه‌نویسی:‌ <a href="https://www.python.org/">پایتون</a></li>
        <li>فریم‌ورک وب: <a href="https://www.djangoproject.com/">جنگو</a></li>
        <li>فریم‌ورک رابط‌کاربری: <a href="https://getbootstrap.com/">بوت‌استرپ</a></li>
        <li>پایگاه‌داده: <a href="https://www.postgresql.org/">پست‌گرس</a></li>
        <li>پلتفرم دیپلوی: <a href="https://liara.ir/">لیارا</a></li>
        </ul>
    </p>
</div>

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