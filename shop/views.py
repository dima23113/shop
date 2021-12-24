from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from .models import *


class IndexView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        brand = Brand.objects.all()
        context = {
            'brand': brand,
            'categories': categories,
        }
        return render(request, 'shop/base.html', context=context)


class ProductListByCategory(View):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(category__slug=kwargs['slug'], available=True)
        context = {
            'products': products
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductListByBrand(View):

    def get(self, request, *args, **kwargs):
        brand = Product.objects.get(slug=kwargs['slug'])
        products = Product.objects.filter(brand__slug=kwargs['slug'], available=True)
        context = {
            'products': products,
            'brand': brand
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductListBySubcategory(View):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(subcategory__slug=kwargs['slug'], available=True)
        context = {
            'products': products
        }
        return render(request, 'shop/product/product_list.html', context=context)

