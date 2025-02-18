from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from django.http import HttpResponse
from .tasks import notify_customers


def say_hi(request):
    # try:
    #     message = BaseEmailMessage(
    #         template_name='emails/hello.html',
    #         context={'name': 'Boostan'}
    #         )
    #     message.send(['ali@boostanbuy.com'])
        
        # message = EmailMessage('subject', 'message', 'from@boostanbuy.com', ['alireza@boostanbuy.com'])
        # message.attach_file('emailbackend/static/images/pic.png')
        # message.send()
       
        # mail_admins('Hello Admins', 'How are you guys.', html_message='message')
       
        # send_mail('Hello World', 'Hello there. This is a test Email!',
                # 'from@boostanbuy.com', ['alireza@boostanbuy.com'])
    # except BadHeaderError:
    #     pass

    notify_customers.delay('hello')
    return HttpResponse('Email was sent successfully.')