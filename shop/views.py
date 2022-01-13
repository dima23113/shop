from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import ListView, View
from .models import *


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'shop/base.html')


class BrandList(View):

    def get(self, request, *args, **kwargs):
        lst = []
        brand = Brand.objects.all()
        for i in brand:
            s = {
                'symbol': i.name[0].upper(),
                'name': i.name,
                'slug': i.slug
            }
            if i.image:
                s['img'] = i
            lst.append(s)
        lst1 = lst[(len(lst)//2)+1:]
        lst = lst[:(len(lst)//2)+1]
        context = {
            'brand_cl': lst,
            'brand_cl_1': lst1
        }
        return render(request, 'shop/product/brand_list.html', context=context)


class ProductListByCategory(View):

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs['slug'])
        products = Product.objects.filter(category=category, available=True)
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'category': category
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductListByBrand(View):

    def get(self, request, *args, **kwargs):
        brand = Brand.objects.get(slug=kwargs['slug'])
        products = Product.objects.filter(brand=brand, available=True)
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'brand': brand
        }
        return render(request, 'shop/product/product_by_brand.html', context=context)


class ProductListBySubcategory(View):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(subcategory__slug=kwargs['slug'], available=True)
        context = {
            'products': products
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductDetail(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['slug'])
        spec = ['Характеристики:']
        if product.specifications:
            var = product.specifications.split('\n')
            spec.append(var)
        recommendation = Product.objects.all()[:6]
        context = {
            'product': product,
            'spec': spec,
            'recommendation': recommendation
        }
        return render(request, 'shop/product/product_detail.html', context=context)
