import datetime
from django.utils.timezone import get_current_timezone
from .models import CategoryDiscount, SubcategoryDiscount, SubcategoryTypeDiscount, BrandDiscount, ProductDiscount
from shop.models import Product


def product_discount_by_category_discount(products):
    """Устанавливаем цену со скидкой на товары категории. скидки для категории"""
    for discount in CategoryDiscount.objects.filter(is_active=True):
        if discount.date_of_completion <= datetime.datetime.now(tz=get_current_timezone()):
            for product in products.filter(sale=True, category=discount.category):
                product.price_discount = product.price
            discount.is_active = False
        else:
            for product in products.filter(category=discount.category):
                product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
                product.sale = True
        product.save()


def product_discount_by_subcategory_discount(products):
    """Устанавливаем цену со скидкой на товары подкатегорий. скидки для подкатегории"""
    for discount in SubcategoryDiscount.objects.filter(is_active=True):
        if discount.date_of_completion <= datetime.datetime.now(tz=get_current_timezone()):
            for product in products.filter(sale=True, subcategory=discount.subcategory):
                product.price_discount = product.price
            discount.is_active = False
        else:
            for product in products.filter(subcategory=discount.subcategory):
                product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
                product.sale = True
        product.save()


def product_discount_by_subcategory_type_discount(products):
    """Устанавливаем цену со скидкой на товары типа подкатегории. скидки для типа подкатегории"""
    for discount in SubcategoryTypeDiscount.objects.filter(is_active=True):
        if discount.date_of_completion <= datetime.datetime.now(tz=get_current_timezone()):
            for product in products.filter(sale=True, subcategory_type=discount.subcategory_type):
                product.price_discount = product.price
            discount.is_active = False
        else:
            for product in products.filter(subcategory_type=discount.category):
                product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
                product.sale = True
        product.save()


def product_discount_by_brand_discount(products):
    """Устанавливаем цену со скидкой на бренд. скидки для бренда"""
    for discount in BrandDiscount.objects.filter(is_active=True):
        if discount.date_of_completion <= datetime.datetime.now(tz=get_current_timezone()):
            for product in products.filter(sale=True, brand=discount.brand):
                product.price_discount = product.price
            discount.is_active = False
        else:
            for product in products.filter(subcategory_type=discount.brand):
                product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
                product.sale = True
        product.save()


def product_discount_by_product_discount():
    """Устанавливаем цену со скидкой на товар. Скидка для товара"""
    for discount in ProductDiscount.objects.filter(is_active=True):
        product = Product.objects.get(available=True, product=discount.product)
        if discount.date_of_completion <= datetime.datetime.now(tz=get_current_timezone()):
            product.price_discount = product.price
            product.sale = False
        else:
            product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
            product.sale = True
        product.save()
