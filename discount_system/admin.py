from django.contrib import admin
from .models import CategoryDiscount, SubcategoryDiscount, SubcategoryTypeDiscount, BrandDiscount, ProductDiscount


@admin.register(CategoryDiscount)
class CategoryDiscountAdmin(admin.ModelAdmin):
    list_display = ['category', 'amount_of_discount', 'is_active', 'date_of_completion']
    list_editable = ['amount_of_discount', 'is_active', 'date_of_completion']


@admin.register(SubcategoryDiscount)
class SubcategoryDiscountAdmin(admin.ModelAdmin):
    list_display = ['subcategory', 'amount_of_discount', 'is_active', 'date_of_completion']
    list_editable = ['amount_of_discount', 'is_active', 'date_of_completion']


@admin.register(SubcategoryTypeDiscount)
class SubcategoryTypeDiscountAdmin(admin.ModelAdmin):
    list_display = ['subcategory_type', 'amount_of_discount', 'is_active', 'date_of_completion']
    list_editable = ['amount_of_discount', 'is_active', 'date_of_completion']


@admin.register(BrandDiscount)
class BrandDiscountAdmin(admin.ModelAdmin):
    list_display = ['brand', 'amount_of_discount', 'is_active', 'date_of_completion']
    list_editable = ['amount_of_discount', 'is_active', 'date_of_completion']


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'amount_of_discount', 'is_active', 'date_of_completion']
    list_editable = ['amount_of_discount', 'is_active', 'date_of_completion']
