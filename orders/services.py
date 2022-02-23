from .models import Order


def update_amount_of_purchases(user):
    """Обновление суммы покупок для покупателя"""
    amount_of_purchases = 0
    for order in Order.objects.filter(customer=user):
        amount_of_purchases += order.get_total_discount_cost()
    return amount_of_purchases
