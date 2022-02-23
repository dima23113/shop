from django.db.models import F
from .models import OrderItem, Order
from shop.models import ProductSize
from loyalty_program.models import UserBonuses


def update_amount_of_purchases(user):
    """Обновление суммы покупок для покупателя."""
    amount_of_purchases = 0
    for order in Order.objects.filter(customer=user):
        amount_of_purchases += order.get_total_discount_cost()
    user.amount_of_purchases = amount_of_purchases
    user.save()


def order_create(cd, user, cart):
    """Создаем заказ."""
    order = Order.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                 address=user.address, zip_code=user.zip_code, ship_type=cd['ship_type'],
                                 paid=False,
                                 customer=user, pay_type=cd['pay_type'], phone=user.phone)
    order.save()
    create_order_item(cart, order)
    bonus_accrual(user, order)
    update_amount_of_purchases(user)


def create_order_item(cart, order):
    """Связываем товар с заказом и уменьшаем ко-во размеров у купленного товара."""
    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], price=item['price'], qty=item['qty'],
                                 size=item['size'], price_discount=item['discount_price'])
        ProductSize.objects.filter(product_id=item['product'], name=item['size']).update(
            qty=F('qty') - int(item['qty']))


def bonus_accrual(user, order):
    """Начисляем бонусы за покупку товара."""
    bonuses = UserBonuses.objects.get(user=user)
    bonuses.bonuses = bonuses.bonuses + (
            (bonuses.bonuses_program.bonus_percentage / 100) * float(order.get_total_discount_cost()))
    bonuses.save()
