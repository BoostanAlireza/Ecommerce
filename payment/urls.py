from django.urls import path
from .views import  payment_callback_sandbox, payment_process_sandbox


app_name = 'payment'


urlpatterns = [
    # path('process/<int:order_id>/', payment_process, name='payment_process'),
    # path('callback/<int:order_id>/', payment_callback, name='payment_callback'),
    path('process/', payment_process_sandbox, name='payment_process_sandbox'),
    path('callback/', payment_callback_sandbox, name='payment_callback_sandbox'),
]

