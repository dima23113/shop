import json

from django.db.models import F

from yookassa import Payment
from yookassa.domain.models.currency import Currency

from .models import OrderItem, Order
from shop.models import ProductSize


def order_create(cd, user, cart):
    # todo: Подумать, как обработать увеличение бонусов и сумму покупок для тех, кто платит в магазине
    """Создаем заказ"""
    order = Order.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                 address=user.address, zip_code=user.zip_code, ship_type=cd['ship_type'],
                                 payment_status='Не оплачен',
                                 customer=user, pay_type=cd['pay_type'], phone=user.phone)
    cart_items = create_order_item(cart, order)
    if cd['pay_type'] == 'Онлайн':
        payment = create_payment(cart_items, order, user)
        order.payment_id = payment['id']
        order.confirmation_url = payment['confirmation']['confirmation_url']
        order.save()
        return payment['confirmation']['confirmation_url']
    else:
        order.save()


def create_order_item(cart, order):
    """Связываем товар с заказом и уменьшаем ко-во размеров у купленного товара.
        Формируем чек для юкассы.
    """
    a = {}
    items = [
    ]
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                 qty=item['qty'],
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
    """Создание платежа в юкассе"""
    payment = Payment.create({
        "amount": {
            "value": order.total_discount_cost(),
            "currency": "RUB"
        },
        'receipt': {
            'customer': {
                'phone': user.phone,
                'email': user.email
            },
            'items': cart_items
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://6b5e-5-18-218-97.ngrok.io"
        },
        "description": f'Заказ #{order.id}'
    })
    payment = payment.json()
    return json.loads(payment)
