import json
import uuid
from celery import shared_task
from yookassa import Payment
from orders.models import Order


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
