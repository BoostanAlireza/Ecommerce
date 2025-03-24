from django.conf import settings
from django.urls import path, include
from . common import *


SECRET_KEY = 'django-insecure-!_d2wsl % 2br_u8veu3oq768+^bx!s@ywsb3uva8j-  # !@kb*t=h'


DEBUG = True

if 'silk' in INSTALLED_APPS:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '09138338774',
    }
}

