import datetime
import json
import uuid

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import get_current_timezone

from celery import shared_task
from yookassa import Payment

from orders.models import Order
from loyalty_program.tasks import bonus_accrual, update_amount_of_purchases, update_user_loyalty_program


@shared_task
def confirm_payment():
    """Подтверждаем платеж
    Вызываем функцию начисления бонусов за заказ, обновления суммы покупок покупателя, обновление бонусной программы и
    отправку письма с информацией о заказе.
    Если заказ не оплачен, то вызываем функцию напоминания о платеже
    """
    for order in Order.objects.filter(pay_type='Онлайн', payment_status='Не оплачен', payment_id__isnull=False):
        if order:
            payment_id = order.payment_id
            payment = Payment.find_one(payment_id)
            payment = json.loads(payment.json())
            if payment['status'] == 'waiting_for_capture' and payment['paid']:
                idempotence_key = str(uuid.uuid4())
                Payment.capture(
                    payment_id,
                    {
                        'amount': {
                            'value': payment['amount']['value'],
                            'currency': payment['amount']['currency']
                        }
                    },
                    idempotence_key
                )
                order.payment_status = 'Оплачен'
                order.save()
                bonus_accrual.apply_async(args=(order.id,))
                update_amount_of_purchases.apply_async(args=(order.id,))
                update_user_loyalty_program.apply_async(args=(order.id,))
                send_order_information.apply_async(args=(order.id,))
            elif payment['status'] == 'pending' and not payment['paid']:
                send_payment_completion_request.apply_async(args=(order.id,))
        else:
            return 'Нечего подтверждать'


@shared_task
def send_order_information(order):
    """Отправляем письмо покупателю с информацией по заказу"""
    order = Order.objects.get(id=order)
    order_items = order.items.all()
    html_template = render_to_string(template_name='orders/mail_order_detail.html',
                                     context={'order': order, 'order_items': order_items})
    html_template = strip_tags(html_template)
    subject = f'Заказ #{order.id} подтвержден!'

    send_mail(subject, html_template, settings.EMAIL_HOST_USER, [order.email], fail_silently=True)


"""@shared_task
def check_payment_completion():
    for order in Order.objects.filter(pay_type='Онлайн', payment_status='Не оплачен', payment_id__isnull=False):
        send_payment_completion_request.apply_async(args=(order.id,))
"""


@shared_task
def send_payment_completion_request(order):
    """Отправляем письмо с информацией по заказу и просьбой завешить платеж"""
    order = Order.objects.get(id=order)
    order_items = order.items.all()

    if order.created + datetime.timedelta(minutes=60) > datetime.datetime.now(tz=get_current_timezone()):
        order_lifetime = (order.created + datetime.timedelta(minutes=60)) - datetime.datetime.now(
            tz=get_current_timezone())
    else:
        order_lifetime = None
        order.confirmation_url = None
        order.payment_status = 'Отменен'
        order.save()
    html_template = render_to_string(template_name='orders/payment_completion_request.html',
                                     context={'order': order, 'order_items': order_items,
                                              'order_lifetime': order_lifetime})
    html_template = strip_tags(html_template)
    subject = f'Заказ #{order.id} подтвержден!'

    send_mail(subject, html_template, settings.EMAIL_HOST_USER, [order.email], fail_silently=True)


@shared_task
def get_order_statistics():
    """Получаем статику заказов за прошедшие сутки"""
    sum_order_prices = 0
    top_of_products = {}
    orders = Order.objects.all()
    pending_orders = orders.filter(payment_status='Не оплачен').count()
    for order in orders.prefetch_related('items').filter(
            created=datetime.datetime.now(get_current_timezone()) - datetime.timedelta(1),
            payment_status='Оплачен'):
        sum_order_prices += order.total_discount_cost()
        for product in order.items.all():
            if top_of_products[product.name]['qty'] > 1:
                top_of_products[product.name]['qty'] = top_of_products[product.name]['qty'] + 1
            else:
                top_of_products = {
                    product.name: {
                        'name': product,
                        'qty': 1,
                        'img': product.image,
                        'available': product.available
                    }
                }

    html_template = render_to_string(template_name='orders/order_statistics.html',
                                     context={'orders_price_sum': sum_order_prices, 'top_products': top_of_products,
                                              'pending_orders': pending_orders, 'orders': orders.filter(
                                             created=datetime.datetime.now(get_current_timezone()) -
                                                     datetime.timedelta(1)).count()})
    html_template = strip_tags(html_template)
    subject = f'Очет статистики заказов за {datetime.date.today() - datetime.timedelta(1)}'
    send_mail(subject, html_template, settings.EMAIL_HOST_USER, ['namedima4@gmail.com'], fail_silently=True)
