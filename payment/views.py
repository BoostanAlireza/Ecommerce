from django.http import HttpResponse
import requests
import json
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from store.models import Order


def payment_process(request):
    #Get order id from JSON response sent by store/views.py/OrderViewSet
    order_id = request.get('order_id')
    #Get order object
    order = get_object_or_404(Order, id=order_id)

    total_price_in_toman = order.get_total_price()
    total_price_in_rial = total_price_in_toman * 10

    zarinpal_request_url = 'https: // payment.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': total_price_in_rial,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': 'http://127.0.0.1:8000',
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://payment.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_status=payment_status)