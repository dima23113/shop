from celery import shared_task
from .models import UserBonuses
from account.models import CustomUser
from orders.models import Order


@shared_task
def bonus_accrual(order):
    """Начисляем бонусы за оплату заказа"""
    order = Order.objects.get(id=order)
    bonuses = UserBonuses.objects.get(user=order.customer)
    bonuses.bonuses = bonuses.bonuses + (
            (bonuses.bonuses_program.bonus_percentage / 100) * float(order.total_discount_cost()))
    bonuses.save()


@shared_task
def update_amount_of_purchases(order):
    order = Order.objects.get(id=order)
    """Обновление суммы покупок для покупателя."""
    user = order.customer
    user.amount_of_purchases += order.total_discount_cost()
    user.save()
