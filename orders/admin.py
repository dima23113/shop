from django.contrib import admin
from .models import *


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'email', 'ship_type', 'paid', 'created', 'updated']
    list_editable = ['email', 'paid', 'ship_type']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'qty', 'price']
    list_editable = ['qty', 'price']
