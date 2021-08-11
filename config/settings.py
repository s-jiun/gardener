"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import json
import environ
from pathlib import Path
import json
from django.core.exceptions import ImproperlyConfigured

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

secret_file = os.path.join(BASE_DIR, 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Email 전송
# 메일을 호스트하는 서버
EMAIL_HOST = 'smtp.gmail.com'

# gmail과의 통신하는 포트
EMAIL_PORT = '587'

# 발신할 이메일
# EMAIL_HOST_USER = '구글아이디@gmail.com'
EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
# get_secret("EMAIL_HOST_PASSWORD")

# TLS 보안 방법
EMAIL_USE_TLS = True

# # 사이트와 관련한 자동응답을 받을 이메일 주소
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# # Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # taggit
    'taggit',

    'user',
    'community',
    'search',
    'QnA',

    # editor
    'ckeditor',
    'ckeditor_uploader',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # image-resize
    'imagekit',
]


SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'config', 'templates'),
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'config', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.GeneralUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# taggit
TAGGIT_CASE_INSENSITIVE = True
TAGGIT_LIMIT = 50
TAGGIT_TAGS_FROM_STRING = 'community.utils.hashtag_splitter'
TAGGIT_STRING_FROM_TAGS = 'community.utils.hashtag_joiner'


# texteditor
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'answer_ckeditor': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Font', 'FontSize'],

            ['BGColor', 'TextColor'],

            ['Bold', 'Italic', 'Strike', 'Superscript',
                'Subscript', 'Underline', 'RemoveFormat'],

            ['BidiLtr', 'BidiRtl'],

            '/',

            ['Image', 'SpecialChar', 'Smiley'],

            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],

            ['Blockquote', 'NumberedList', 'BulletedList'],

            ['Link', 'Unlink'],

            ['Undo', 'Redo']
        ],
        'width': '100%'
    }
}

LOGIN_REDIRECT_URL = '/update'  # 로그인 후 리디렉션
ACCOUNT_LOGOUT_REDIRECT_URL = "/"  # 로그아웃 후 리디렉션

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'FIELDS': [
            'id',
            'name',
            'email'
            'password'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'userid'
ACCOUNT_AUTHENTICATION_METHOD = 'username'
# ACCOUNT_USERNAME_REQUIRED = False


ACCOUNT_FORMS = {'signup': 'user.forms.MyCustomSignupForm'}
