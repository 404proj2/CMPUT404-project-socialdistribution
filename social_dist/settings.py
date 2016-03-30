"""
Django settings for social_dist project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR  = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%rdo8!a#$s7)hg$m)r2ednw5uv%r82=!1f!3$(-x5*pp!mrh#a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
#LOCAL_HOST = "http://127.0.0.1:8000/"
LOCAL_HOST = "https://mighty-cliffs-82717.herokuapp.com/"

# Application definition

INSTALLED_APPS = (
    'authors',
    'friends',
    'posts',
    'stream',
    'settings',
    'comments',
    'nodes',
    'api',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'social_dist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'social_dist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
PROFILE_IMAGES_URL = '/profile_images/'
PROFILE_IMAGES_ROOT = os.path.join(BASE_DIR,'profile_images')
STATIC_PATH = os.path.abspath(os.path.join(BASE_DIR, 'static'))
PROFILE_IMAGES_PATH = os.path.abspath(os.path.join(BASE_DIR, 'profile_images'))
STATICFILES_DIRS = (
    STATIC_PATH,
    PROFILE_IMAGES_PATH
)

MEDIA_URL = 'https://mighty-cliffs-82717.herokuapp.com/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR,'media')
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Default page if not logged in.
LOGIN_URL= '/login'

# Telling Django about the profile object
AUTH_PROFILE_MODULE = "authors.Author"

# HEROKU MADE ME ADD THIS 
import dj_database_url
DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

DEBUG = False

try:
    from .local_settings import *
except ImportError:
    pass