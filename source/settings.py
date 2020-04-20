import os

import dj_database_url
import sentry_sdk
from decouple import Csv, config
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ENV = config("ENV")  # development, test, qa or production

SECRET_KEY = config("SECRET_KEY")

DEBUG = ENV == "development"

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

ADMIN_PATH = config("ADMIN_PATH")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "source.apps.accounts.apps.AccountsConfig",
    "source.apps.tmdb.apps.TMDbConfig",
    "source.apps.website.apps.WebsiteConfig",
    "source.core.apps.CoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "source.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "source.wsgi.application"


# Database
DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL"))}


# Authentication

AUTH_USER_MODEL = "apps_accounts.User"


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 6},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Password hashers

if ENV == "test":
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Date and time formats

DATE_FORMAT = "Y/m/d"

DATETIME_FORMAT = "Y/m/d H:i:s"


# Login/Logout URLs

LOGIN_REDIRECT_URL = "tmdb:progresses"

LOGIN_URL = "accounts:login"

LOGOUT_REDIRECT_URL = "tmdb:popular_shows"


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [os.path.join(BASE_DIR, "source/core/static")]


# Django Debug Toolbar

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: True}


# TMDb

TMDB_API_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = config("TMDB_API_KEY")

# Email

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

if ENV in ["qa", "production"]:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config("SENDGRID_USERNAME")
    EMAIL_HOST_PASSWORD = config("SENDGRID_PASSWORD")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 25
    EMAIL_USE_TLS = False


# Sentry

sentry_sdk.init(dsn=config("SENTRY_DSN", default=None), integrations=[DjangoIntegration()])
