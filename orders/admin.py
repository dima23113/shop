from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'email', 'ship_type', 'payment_status', 'created', 'updated']
    list_editable = ['email', 'payment_status', 'ship_type']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'qty', 'price']
    list_editable = ['qty', 'price']
