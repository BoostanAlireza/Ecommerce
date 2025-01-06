from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser



admin.site.site_header = 'Store'
admin.site.index_title = 'Special Access'


class CustomeUser(AbstractUser):
    email = models.EmailField(unique=True)
