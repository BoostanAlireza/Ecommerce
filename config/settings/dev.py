from django.conf import settings
from django.urls import path, include
from . common import *


SECRET_KEY = env('SECRET_KEY')


DEBUG = True

if 'silk' in INSTALLED_APPS:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']



DATABASES = {
    'default': env.db_url()
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'ecommerce',
#         'HOST': 'localhost',
#         'USER': 'root',
#         'PASSWORD': '09138338774',
#     }
# }

