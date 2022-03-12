from django.db import models
from django.core.validators import MaxValueValidator

from smart_selects.db_fields import GroupedForeignKey

from shop.models import Category, Subcategory, SubcategoryType, Brand, Product


class Discount(models.Model):
    amount_of_discount = models.DecimalField(validators=[MaxValueValidator(80.00)], max_digits=10, decimal_places=2,
                                             verbose_name='Размер скидки')
    is_active = models.BooleanField(verbose_name='Акция активна?')
    date_of_completion = models.DateTimeField(verbose_name='Дата завершения Акции')

    class Meta:
        abstract = True


class CategoryDiscount(Discount):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_discount',
                                 verbose_name='Скидка для категории товаров')

    class Meta:
        verbose_name = 'Скидки для категорий'
        verbose_name_plural = 'Скидка для категории'

    def __str__(self):
        return f'Скидка {self.amount_of_discount}% на категорию {self.category.name}'


class SubcategoryDiscount(Discount):
    subcategory = GroupedForeignKey(Subcategory, 'category', on_delete=models.CASCADE,
                                    verbose_name='Скидка для подкатегории товаров',
                                    related_name='subcategory_discount')

    class Meta:
        verbose_name = 'Скидки для подкатегорий'
        verbose_name_plural = 'Скидка для подкатегории'

    def __str__(self):
        return f'Скидка {self.amount_of_discount}% на подкатегорию {self.subcategory.name}'


class SubcategoryTypeDiscount(Discount):
    subcategory_type = GroupedForeignKey(SubcategoryType, 'subcategory', on_delete=models.CASCADE,
                                         verbose_name='Скидка для типа подкатегории товаров',
                                         related_name='subcategory_type_discount')

    class Meta:
        verbose_name = 'Скидки для типа подкатегорий'
        verbose_name_plural = 'Скидка для типа подкатегории'

    def __str__(self):
        return f'Скидка {self.amount_of_discount}% на тип подкатегории {self.subcategory_type.name}'


class BrandDiscount(Discount):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_discount',
                              verbose_name='Скидка для товаров бренда')

    class Meta:
        verbose_name = 'Скидка на бренды'
        verbose_name_plural = 'Скидка на бренд'

    def __str__(self):
        return f'Скидка {self.amount_of_discount}% на бренд {self.brand.name}'


class ProductDiscount(Discount):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_discount',
                                verbose_name='Скидка для определенного товара/всех товаров')

    class Meta:
        verbose_name = 'Скидка на товары'
        verbose_name_plural = 'Скидка на товар'

    def __str__(self):
        return f'Скидка {self.amount_of_discount}% на товар {self.product.name}'
