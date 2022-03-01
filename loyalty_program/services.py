from .models import UserBonuses


def bonus_accrual(user, order):
    """Начисляем бонусы за покупку товара."""
    bonuses = UserBonuses.objects.get(user=user)
    bonuses.bonuses = bonuses.bonuses + (
            (bonuses.bonuses_program.bonus_percentage / 100) * float(order.get_total_discount_cost()))
    bonuses.save()
