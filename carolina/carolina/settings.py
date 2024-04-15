"""
Django settings for carolina project.

Generated by 'django-admin startproject' using Django 3.2.19.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.utils.translation import gettext_lazy as _

import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Debug mode
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', os.environ.get('CENTROIA_VM_HOST')]

# Problem with load and dump data encode json Windows
import _locale
_locale._getdefaultlocale = (lambda *args: ['pt_br','utf8'])#['en_US', 'utf8'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'webpage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #added translation
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
] 

ROOT_URLCONF = 'carolina.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'templates/central' , BASE_DIR / 'templates/admin'],
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

WSGI_APPLICATION = 'carolina.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRE_DATABASE'), 
        'USER': os.environ.get('POSTGRE_USER'), 
        'PASSWORD': os.environ.get('POSTGRE_PASSWORD'), 
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

#https://stackoverflow.com/questions/75417464/django-databases-is-improperly-configured-error-after-updating-versions
#https://stackoverflow.com/questions/71337173/django-4-connection-to-postgresql-using-passfile-fe-sendauth-no-password-supp

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

LANGUAGES=[
    ("pt-br", _("Brazilian Portuguese")),
    ("en", _("English")),
]

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# Where to serve in url 
STATIC_URL = '/static/'

# Path of static collected to serve in production (destination)
# Django runserver will not serve staticfiles from here, only from local (static folder inside app) and extra directories in STATIC_DIRS
# One have to create another folder different from STATIC_ROOT in project root and put in STATIC_DIR to use django 'runserver' option. 
STATIC_ROOT = os.path.join(BASE_DIR,'static')

# Path directories to look for collection static files (startpoint)
STATICFILES_DIRS = [ BASE_DIR / 'static_for_django/']

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'