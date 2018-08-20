import os
from datetime import timedelta

import dj_database_url
from decouple import Csv, config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ENV = config('ENV')  # prod, local or test

SECRET_KEY = config('SECRET_KEY')

DEBUG = ENV == 'local'

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'rest_framework',
    'suit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'project.apps.accounts.apps.AccountsConfig',
    'project.apps.emails.apps.EmailsConfig',
    'project.apps.tmdb.apps.TMDbConfig',
    'project.apps.website.apps.WebsiteConfig',
    'project.core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'project/templates/')],
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

DATABASES = {
    'default': dj_database_url.parse(config('DATABASE_URL'))
}

WSGI_APPLICATION = 'project.wsgi.application'


# Authentication

AUTH_USER_MODEL = 'apps_accounts.User'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Date and time formats

DATE_FORMAT = 'Y/m/d'

DATETIME_FORMAT = 'Y/m/d H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'project/static'),
]


# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# Django CORS Headers

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=Csv())


# Django REST Framework JWT

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_PAYLOAD_HANDLER': 'project.apps.accounts.jwt.payload_handler',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'project.apps.accounts.jwt.payload_username_handler',
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30),
}


# Django Admin

ADMIN_PATH = config('ADMIN_PATH')

SUIT_CONFIG = {
    'ADMIN_NAME': 'TV Tracker',

    'SEARCH_URL': '',

    'MENU': (
        '-',
        {
            'app': 'apps_accounts',
            'models': ('user', 'passwordresettoken'),
        },
        {
            'app': 'apps_emails',
            'models': (
                {
                    'model': 'sendgridemail',
                    'label': 'SendGrid'
                },
            ),
        },
        {
            'app': 'apps_website',
            'models': ('contact',),
        },
    )
}


# Email

DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

SENDGRID_API_KEY = config('SENDGRID_API_KEY')

SENDGRID_SANDBOX_MODE = config('SENDGRID_SANDBOX_MODE', cast=bool)


if ENV == 'test':
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    SENDGRID_SANDBOX_MODE = True
