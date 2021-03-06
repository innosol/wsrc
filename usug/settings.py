"""
Django settings for usug project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#AUTH_USER_MODEL = 'app.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h_+usjl)sna0yp6ydg$ekuip_$w3cp*ss4*pq1i!(pmm#6q+l)'

# SECURITY WARNING: don't run with debug turned on in production!
#404 & 500 page calling
#DEBUG = False
DEBUG= True

#ALLOWED_HOSTS = ['localhost', '103.17.108.185']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'applications.app',
    'applications.admin1',
    'applications.tza',
    'applications.uta',
    'applications.hzm',
    'applications.director',
    'applications.engineering',
    'applications.accountants',
    'django_cron',
    'django_filters',
    'captcha',
    'smart_selects',
    'simple_history',
    'notifications',
    'django_messages',
)

USE_DJANGO_JQUERY = False
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

CRON_CLASSES = [
    'usug.Cron.TailanEhleh',
    'usug.Cron.TailanDuusah',
    'usug.Cron.UAtailanIlgeeh',
    'usug.Cron.TailanUusgeh'

]

ROOT_URLCONF = 'usug.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Templates'),
            os.path.join(BASE_DIR, 'Templates/django_messages'),
            os.path.join(BASE_DIR, 'applications/engineering/Templates'),
            os.path.join(BASE_DIR, 'applications/admin1/Templates'),
            os.path.join(BASE_DIR, 'applications/accountants/Templates'),
            os.path.join(BASE_DIR, 'applications/director/Templates'),
            os.path.join(BASE_DIR, 'applications/tza/Templates'),
            os.path.join(BASE_DIR, 'applications/engineering/Templates'),
            os.path.join(BASE_DIR, 'applications/uta/Templates'),
            os.path.join(BASE_DIR, 'applications/hzm/Templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_messages.context_processors.inbox',
            ],
        },
    },
]

WSGI_APPLICATION = 'usug.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

import db

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': db.NAME,
       'USER': db.USER,
       'PASSWORD': db.PASSWORD,
       'HOST': 'localhost',
        'PORT': '',

    }
}
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ulaanbaatar'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")

STATICFILES_DIRS = (
    ( 'assets', os.path.join(BASE_DIR, 'static') ),
    )


STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wsrcmon@gmail.com'
EMAIL_HOST_PASSWORD = 'duheufocpsahrbhi'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/engineering/baiguul/'

NOTIFICATIONS_USE_JSONFIELD=True
