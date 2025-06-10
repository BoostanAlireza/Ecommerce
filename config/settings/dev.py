from .common import *
import environ
import os

env = environ.Env()

if os.environ.get("LIARA_ENV") == "production":
    environ.Env.read_env(".env.production")
else:
    environ.Env.read_env()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
    }
}

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = env.int('EMAIL_PORT')

CELERY_BROKER_URL = env('CELERY_BROKER_URL')
REDIS_CACHE_URL = env('REDIS_CACHE_URL')

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
