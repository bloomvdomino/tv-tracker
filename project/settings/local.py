import dj_database_url

from .base import *  # noqa

SECRET_KEY = 'very-secret-key'

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    'default': dj_database_url.parse('postgres://tt:@127.0.0.1:5432/tt')
}
