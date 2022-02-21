from django.urls import path
from .views import *


app_name = 'discount_system'

urlpatterns = [
    path('category_discount/', ChangeDiscountPrice.as_view(), name='category_discount')
]
