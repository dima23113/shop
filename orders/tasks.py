import json
import uuid
from celery import shared_task
from yookassa import Payment
from orders.models import Order
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def confirm_payment():
    for order in Order.objects.filter(pay_type='Онлайн', payment_status='Не оплачен', payment_id__isnull=False):
        print(order)
        payment_id = order.payment_id
        payment = Payment.find_one(payment_id)
        payment = json.loads(payment.json())
        print(payment)
        if payment['status'] == 'waiting_for_capture' and payment['paid']:
            idempotence_key = str(uuid.uuid4())
            response = Payment.capture(
                payment_id,
                {
                    'amount': {
                        'value': payment['amount']['value'],
                        'currency': payment['amount']['currency']
                    }
                },
                idempotence_key
            )
            print(response.json())
            send_order_information(order)


@shared_task
def send_order_information(order):
    order_items = order.items.all()
    html_template = render_to_string(template_name='orders/mail_order_detail.html',
                                     context={'order': order, 'order_items': order_items})
    html_template = strip_tags(html_template)
    subject = f'Заказ #{order.id} подтвержден!'

    send_mail(subject, html_template, settings.EMAIL_HOST_USER, [order.email], fail_silently=True)
