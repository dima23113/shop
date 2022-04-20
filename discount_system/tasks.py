from celery import shared_task
from .models import Discount, CategoryDiscount, SubcategoryDiscount, SubcategoryTypeDiscount, BrandDiscount, \
    ProductDiscount

@shared_task
def discount_check():
    pass
