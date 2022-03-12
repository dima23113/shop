from celery import shared_task
from .models import UserBonuses
from account.models import CustomUser


@shared_task
def bonus_accrual(order):
    """Начисляем бонусы за оплату заказа"""
    bonuses = UserBonuses.objects.get(user=order.customer)
    bonuses.bonuses = bonuses.bonuses + (
            (bonuses.bonuses_program.bonus_percentage / 100) * float(order.get_total_discount_cost()))
    bonuses.save()


@shared_task
def update_amount_of_purchases(order):
    """Обновление суммы покупок для покупателя."""
    user = order.customer
    user.amount_of_purchases += order.get_total_discount_cost()
    user.save()
