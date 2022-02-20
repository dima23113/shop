from django.db import models


class Discount(models.Model):
    amount_of_discount = models.PositiveIntegerField(max_length=80, verbose_name='Размер скидки')
    is_active = models.BooleanField(verbose_name='Акция активна?')
    date_of_completion = models.DateTimeField(verbose_name='Дата завершения Акции')

    class Meta:
        abstract = True


class CategoryDiscount(Discount):
    pass


class SubcategoryDiscount(Discount):
    pass


class SubcategoryTypeDiscount(Discount):
    pass


class BrandDiscount(Discount):
    pass

