from django.urls import path
from .views import say_hi


urlpatterns = [
    path('hello/', say_hi, name='send_email'),
]
