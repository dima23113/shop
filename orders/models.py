from django.db import models
from shop.models import Product
from account.models import CustomUser


class Order(models.Model):
    delivery = 'Доставка'
    self_delivery = 'Самовывоз'
    ship = [
        (delivery, 'Доставка'),
        (self_delivery, 'Самовывоз'),
    ]

    online = 'Онлайн'
    offline = 'При получении'
    pay = [
        (online, 'Онлайн'),
        (offline, 'При получении'),
    ]

    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='email')
    address = models.CharField(max_length=256, verbose_name='Адрес доставки')
    zip_code = models.CharField(max_length=6, verbose_name='Почтовый иднекс')
    ship_type = models.CharField(choices=ship, default=self_delivery, verbose_name='Тип доставки', max_length=50)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления заказа')
    paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Покупатель', related_name='order')
    pay_type = models.CharField(choices=pay, verbose_name='Тип оплаты', default=online, max_length=50)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='Позиция')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return f'Позиция - {self.id}'

    def get_cost(self):
        return self.price * self.qty
