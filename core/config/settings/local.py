import os
from . import base

DEBUG = True
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", '').split(',')

BASE_DIR = base.BASE_DIR
SECRET_KEY = base.SECRET_KEY
INSTALLED_APPS = base.INSTALLED_APPS
MIDDLEWARE = base.MIDDLEWARE
ROOT_URLCONF = base.ROOT_URLCONF
TEMPLATES = base.TEMPLATES
AUTH_USER_MODEL = base.AUTH_USER_MODEL
WSGI_APPLICATION = base.WSGI_APPLICATION
LANGUAGE_CODE = base.LANGUAGE_CODE
TIME_ZONE = base.TIME_ZONE
USE_I18N = base.USE_I18N
USE_TZ = base.USE_TZ
STATIC_URL = base.STATIC_URL
REST_FRAMEWORK = base.REST_FRAMEWORK
SIMPLE_JWT = base.SIMPLE_JWT

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
