from django.contrib import admin
from .models import *


class ProductImgInline(admin.StackedInline):
    model = ImgProduct
    max_num = 50
    extra = 0


class ProductSizeInline(admin.StackedInline):
    model = ProductSize
    max_num = 50
    extra = 0


class ProductInline(admin.ModelAdmin):
    inlines = [ProductImgInline, ProductSizeInline]
    list_display = ['name', 'price', 'price_discount', 'available', 'created', 'updated']
    list_filter = ['name', 'slug']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductInline)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']


@admin.register(SubcategoryType)
class SubcategoryTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', 'subcategory']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug', 'description']


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    pass


@admin.register(Banner)
class BannersAdmin(admin.ModelAdmin):
    pass


@admin.register(SmallBanner)
class SmallBannerAdmin(admin.ModelAdmin):
    pass
