from .models import CategoryDiscount, SubcategoryDiscount, SubcategoryTypeDiscount, BrandDiscount, ProductDiscount
from shop.models import Product


def product_discount_by_category_discount():
    """Устанавливаем цену со скидкой на товары скидки для категории"""
    for discount in CategoryDiscount.objects.filter(is_active=True):
        for product in Product.objects.filter(available=True, category=discount.category):
            product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
            product.save()


def product_discount_by_subcategory_discount():
    """Устанавливаем цену со скидкой на товары скидки для подкатегории"""
    for discount in SubcategoryDiscount.objects.filter(is_active=True):
        for product in Product.objects.filter(available=True, subcategory=discount.subcategory):
            product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
            product.save()


def product_discount_by_subcategory_type_discount():
    """Устанавливаем цену со скидкой на товары скидки для типа подкатегории"""
    for discount in SubcategoryTypeDiscount.objects.filter(is_active=True):
        for product in Product.objects.filter(available=True, subcategory_type=discount.subcategory_type):
            product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
            product.save()


def product_discount_by_brand_discount():
    """Устанавливаем цену со скидкой на бренд скидки для брендов"""
    for discount in BrandDiscount.objects.filter(is_active=True):
        for product in Product.objects.filter(available=True, brand=discount.brand):
            product.price_discount = product.price - (product.price * (discount.amount_of_discount / 100))
            product.save()
