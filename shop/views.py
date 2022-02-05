from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.template.loader import render_to_string
from cart.forms import CartAddProductForm
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
        lst1 = lst[(len(lst) // 2) + 1:]
        lst = lst[:(len(lst) // 2) + 1]
        context = {
            'brand_cl': lst,
            'brand_cl_1': lst1
        }
        return render(request, 'shop/product/brand_list.html', context=context)


class ProductListByCategory(View):

    def get(self, request, *args, **kwargs):
        category = Category.objects.filter(slug=kwargs['slug'])[0]
        brands = Brand.objects.all().values('name', 'id')
        sizes = ProductSize.objects.filter(product__category=category)
        sizes = list(set([i.name.lower() for i in sizes]))
        products = Product.objects.filter(category=category, available=True)
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'category': category,
            'brands': brands,
            'sizes': sizes
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductListByBrand(View):

    def get(self, request, *args, **kwargs):
        brand = Brand.objects.get(slug=kwargs['slug'])
        products = Product.objects.filter(brand=brand, available=True).values('image', 'brand',
                                                                              'slug', 'name',
                                                                              'price')
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
        product = Product.objects.filter(slug=kwargs['slug']).first()
        spec = ['Характеристики:']
        if product.specifications:
            var = product.specifications.split('\n')
            spec.append(var)
        recommendation = Product.objects.all()[:6].select_related('brand')
        form = CartAddProductForm()
        context = {
            'product': product,
            'spec': spec,
            'recommendation': recommendation,
            'cart_add': form
        }
        return render(request, 'shop/product/product_detail.html', context=context)


class JsonFilterProductView(ListView):

    def get_queryset(self):
        print(self.request.GET.get('category'))
        queryset = Product.objects.filter(
            Q(subcategory_type__in=self.request.GET.getlist('product_type[]', '')) |
            Q(brand__in=self.request.GET.getlist('brand[]', ''), category=self.request.GET.get('category')) |
            Q(product_sizer__name__in=self.request.GET.getlist('size[]', ''))
        ).distinct().select_related('brand').values('name', 'slug', 'brand__name', 'image', 'price')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        print(queryset)
        rendered = render_to_string('shop/product/product_by_filter.html', {'products': queryset})
        return JsonResponse({'products': queryset, 'render': rendered})
