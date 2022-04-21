from celery import shared_task
from .models import UserBonuses, BonusesProgram
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
    """Обновление суммы покупок для покупателя"""
    order = Order.objects.get(id=order)
    user = order.customer
    user.amount_of_purchases += order.total_discount_cost()
    user.save()


@shared_task
def update_user_loyalty_program(order):
    """Обновление бонусной программы при выполнении условий"""
    user = Order.objects.get(id=order)
    user = user.customer
    for program in BonusesProgram.objects.all():
        if user.amount_of_purchases >= program.required_amount:
            bonuses_program = user.user_bonuses.first()
            bonuses_program.bonuses_program = program
        else:
            pass
    bonuses_program.save()


@shared_task
def remove_user_bonuses():
    """Проверка срока начисления бонусов и их удалении при длительном неиспользовании"""
    pass
