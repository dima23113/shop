import json
from django.db.models import F
from django.conf import settings
from yookassa import Payment
from yookassa.domain.models.currency import Currency

from .models import OrderItem, Order
from shop.models import ProductSize
from loyalty_program.services import bonus_accrual


def update_amount_of_purchases(user):
    """Обновление суммы покупок для покупателя."""
    amount_of_purchases = 0
    for order in Order.objects.filter(customer=user):
        amount_of_purchases += order.get_total_discount_cost()
    user.amount_of_purchases = amount_of_purchases
    user.save()


def order_create(cd, user, cart):
    """Создаем заказ"""
    order = Order.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                 address=user.address, zip_code=user.zip_code, ship_type=cd['ship_type'],
                                 paid=False,
                                 customer=user, pay_type=cd['pay_type'], phone=user.phone)
    order.save()
    cart_items = create_order_item(cart, order)
    bonus_accrual(user, order)
    update_amount_of_purchases(user)
    payment = create_payment(cart_items, order, user)
    return payment['confirmation']['confirmation_url']


def create_order_item(cart, order):
    """Связываем товар с заказом и уменьшаем ко-во размеров у купленного товара."""
    a = {}
    items = [
    ]
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], qty=item['qty'],
                                 size=item['size'], price_discount=item['discount_price'])
        ProductSize.objects.filter(product_id=item['product'], name=item['size']).update(
            qty=F('qty') - int(item['qty']))
        a['description'] = f'{item["product"]}'
        a['quantity'] = item['qty']
        a['amount'] = {
                          'value': item['price'],
                          'currency': Currency.RUB
                      }
        a['vat_code'] = 2
        items.append(a)
        a = {}
    return items


def create_payment(cart_items, order, user):
    """Создание платежа"""
    payment = Payment.create({
        "amount": {
            "value": order.get_total_discount_cost(),
            "currency": "RUB"
        },
        'receipt': {
            'customer': {
                'phone': user.phone,
                'email': user.email
            },
            'items': cart_items
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://6b5e-5-18-218-97.ngrok.io"
        },
        "description": f'Заказ #{order.id}'
    })
    payment = payment.json()
    return json.loads(payment)


def confirm_payment(id, order):
    """Подтверждение платежа"""
    payment_id = id
    res = Payment.capture(payment_id, {
        'amount': {
            'value': order.get_total_discount_cost(),
            'currency': 'RUB'
        }
    })


"""{"amount": {"currency": "RUB", "value": "4409.99"}, "confirmation": {"confirmation_url": 
"https://yoomoney.ru/checkout/payments/v2/contract?orderId=29ba9cbe-000f-5000-9000-110b28453918", "return_url": 
"https://6b5e-5-18-218-97.ngrok.io", "type": "redirect"}, "created_at": "2022-03-09T11:01:18.962Z", "description": 
"Заказ №72", "id": "29ba9cbe-000f-5000-9000-110b28453918", "metadata": {}, "paid": false, "payment_method": {"id": 
"29ba9cbe-000f-5000-9000-110b28453918", "saved": false, "type": "bank_card"}, "recipient": {"account_id": "888013", 
"gateway_id": "1949997"}, "refundable": false, "status": "pending", "test": true} """
