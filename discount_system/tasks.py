import datetime
from celery import shared_task
from .services import product_discount_by_product_discount, product_discount_by_brand_discount, \
    product_discount_by_category_discount, product_discount_by_subcategory_discount, \
    product_discount_by_subcategory_type_discount
from shop.models import Product


@shared_task
def discount_check():
    """Метод проверяет актуальность акций и обновляет цены в случае их неактуальности"""
    products = Product.objects.filter(available=True)
    product_discount_by_category_discount(products)
    product_discount_by_subcategory_discount(products)
    product_discount_by_subcategory_type_discount(products)
    product_discount_by_brand_discount(products)
    product_discount_by_product_discount()
