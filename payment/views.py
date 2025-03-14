import requests
import jwt
import json
from rest_framework import status
from decimal import Decimal
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404, reverse
from store.models import Order

from django.core.serializers.json import DjangoJSONEncoder


# This is supposed to be the main implementation
# def payment_process(request, order_id):
#     # Get order id from JSON response sent by store/views.py/OrderViewSet
#     # order_id = request.get('order_id')
#     # Get order object
#     order = get_object_or_404(Order, id=order_id)

#     total_price_in_toman = order.get_total_price()
#     total_price_in_rial = total_price_in_toman * 10

#     zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'

#     request_header = {
#         "accept": "application/json",  #Specifies the format of data that our app is supposed to receive
#         "content-type": "application/json"  #Shows the data format for which we make a post request
#     }

#     request_data = {
#         'merchant_id': 'c39a449c-1a95-403e-9c2a-95fd13632651',
#         'amount': float(total_price_in_rial),
#         'description': f'#{order.id}: {order.customer.user.first_name} {order.customer.user.last_name}',
#         'callback_url': request.build_absolute_uri(reverse('payment:payment_callback', kwargs={'order_id': order_id})),
#     }

#     res = requests.post(
#         url=zarinpal_request_url,
#         data=json.dumps(request_data),
#         headers=request_header,
#         verify=False
#     )

#     data = res.json()['data']
#     authority = data['authority']
#     order.zarinpal_authority = authority
#     order.save()

#     if 'errors' not in data or len(data['errors']) == 0:
#         return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
#     else:
#         return HttpResponse('Error from zarinpal')


# def payment_callback(request, order_id):
#     payment_authority = request.GET.get('Authority')
#     payment_status = request.GET.get('Status')

#     order = get_object_or_404(Order, zarinpal_authority=payment_authority)
#     toman_total_price = Decimal(order.get_total_price())
#     rial_total_price = Decimal(toman_total_price * 10)

#     if payment_status == 'OK':
#         request_header = {
#             "accept": "application/json",
#             "content-type": "application/json"
#         }

#         request_data = {
#             'merchant_id': 'c39a449c-1a95-403e-9c2a-95fd13632651',
#             'amount': rial_total_price,
#             'authority': payment_authority,
#         }

#         res = requests.post(
#             url='https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
#             data=json.dumps(request_data),
#             headers=request_header,
#             verify=False
#         )

#         if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
#             data = res.json()['data']
#             # print(data)
#             payment_code = data['code']

#             if payment_code == 100:
#                 order.is_paid = True
#                 order.re_id = data['ref_id']
#                 order.zarinpal_data = data
#                 order.save()

#                 return HttpResponse('Payment successfully completed.')

#             elif payment_code == 101:
#                 return HttpResponse('This payment has been successfully completed in the past.')

#             else:
#                 error_code = res.json()['errors']['code']
#                 error_message = res.json()['errors']['message']
#                 return HttpResponse(f'Payment unsuccessful. {error_code} {error_message}')

#     else:
#         return HttpResponse(f'Payment unsuccessful.')


#This implementation is solely dedicated to testing
def payment_process_sandbox(request):
    token = request.GET.get('token')

    if not token:
        return HttpResponse('Unauthorized', status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        order_id = payload['order_id']
    except jwt.ExpiredSignatureError:
        return HttpResponse('Token has expired', status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return HttpResponse('Invalid token', status=status.HTTP_401_UNAUTHORIZED)
    
    order = get_object_or_404(Order, id=order_id)

    total_price_in_toman = order.get_total_price()
    total_price_in_rial = total_price_in_toman * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",  #Specifies the format of data that our app is supposed to receive
        "content-type": "application/json"  #Shows the data format for which we make a post request
    }

    request_data = {
        'merchant_id': 'c39a449c-1a95-403e-9c2a-95fd13632651',
        'amount': float(total_price_in_rial),
        'description': f'#{order.id}: {order.customer.user.first_name} {order.customer.user.last_name}',
        'callback_url': request.build_absolute_uri(reverse('payment:payment_callback_sandbox')),
    }

    res = requests.post(
        url=zarinpal_request_url,
        data=json.dumps(request_data),
        headers=request_header,
    )

    data = res.json()['data']
    authority = data['authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}')
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        request_data = {
            'merchant_id': 'c39a449c-1a95-403e-9c2a-95fd13632651',
            'amount': float(rial_total_price),
            'authority': payment_authority,
        }

        print(request_data)
        res = requests.post(
            url='https://sandbox.zarinpal.com/pg/v4/payment/verify.json',
            data=json.dumps(request_data),
            headers=request_header,
        )

        if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.re_id = data['ref_id']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('Payment successfully completed.')

            elif payment_code == 101:
                return HttpResponse('This payment has been successfully completed in the past.')

            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                return HttpResponse(f'Payment unsuccessful. {error_code} {error_message}')

    else:
        return HttpResponse(f'Payment unsuccessful.')
