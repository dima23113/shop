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
        sizes = ProductSize.objects.filter(product__category=category).only('name').distinct('name')
        products = Product.objects.filter(category=category, available=True).select_related('brand').only('image',
                                                                                                          'slug',
                                                                                                          'brand',
                                                                                                          'name',
                                                                                                          'price')
        subcategory = Subcategory.objects.filter(subcategory_products__in=products).distinct().only('id', 'name')
        subcategory_type = SubcategoryType.objects.filter(
            subcategory__category=category, product__in=products).distinct().only('id', 'name')
        brands = Brand.objects.filter(product__in=products).values('name', 'id').distinct()
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'category': category,
            'brand': brands,
            'sizes': sizes,
            'subcategory': subcategory,
            'subcategory_type': subcategory_type
        }

        return render(request, 'shop/product/product_list.html', context=context)


class ProductListByBrand(View):

    def get(self, request, *args, **kwargs):
        brand = Brand.objects.get(slug=kwargs['slug'])
        products = Product.objects.filter(brand=brand, available=True)
        category = Category.objects.filter(products__in=products).distinct('name')
        subcategory = Subcategory.objects.filter(subcategory_products__in=products).distinct()
        subcategory_type = SubcategoryType.objects.filter(product__in=products).distinct()
        sizes = ProductSize.objects.filter(product__in=products)
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'brand': brand,
            'sizes': sizes,
            'category': category,
            'subcategory': subcategory,
            'subcategory_type': subcategory_type
        }
        return render(request, 'shop/product/product_by_brand.html', context=context)


class ProductListBySubcategory(View):

    def get(self, request, *args, **kwargs):
        subcategory = Subcategory.objects.get(slug=kwargs['slug'])
        products = Product.objects.filter(
            subcategory=subcategory,
            available=True).only('image', 'slug', 'brand', 'name', 'price')
        category = Category.objects.filter(products__in=products).distinct().only('id', 'name')
        subcategory_type = SubcategoryType.objects.filter(product__in=products).distinct().only('id', 'name')
        brands = Brand.objects.filter(product__in=products).only('name', 'id').distinct()
        sizes = ProductSize.objects.filter(product__in=products).distinct('name')
        paginator = Paginator(products, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'brand': brands,
            'sizes': sizes,
            'category': category,
            'subcategory': subcategory,
            'subcategory_type': subcategory_type
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductListBySubcategoryType(View):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(subcategory_type__slug=kwargs['slug'], available=True).values('image',
                                                                                                        'brand',
                                                                                                        'slug', 'name',
                                                                                                        'price')
        paginator = Paginator(products, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductDetail(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.filter(slug=kwargs['slug']).select_related('brand').first()
        spec = ['Характеристики:']
        if product.specifications:
            var = product.specifications.split('\n')
            spec.append(var)
        recommendation = Product.objects.all()[:6].select_related('brand').only('slug', 'brand', 'name', 'image',
                                                                                'price')
        product_image = ImgProduct.objects.filter(product=product)
        form = CartAddProductForm()
        context = {
            'product': product,
            'spec': spec,
            'recommendation': recommendation,
            'cart_add': form,
            'images': product_image
        }
        return render(request, 'shop/product/product_detail.html', context=context)


class JsonFilterProductView(ListView):

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(product_sizer__name__in=self.request.GET.getlist('size[]', ''),
              brand__in=self.request.GET.getlist('brand[]', ''),
              category__in=self.request.GET.getlist('category[]', ''),
              subcategory__in=self.request.GET.getlist('subcategory[]', ''),
              subcategory_type__in=self.request.GET.getlist('subcategorytype[]', ''))
        ).distinct().select_related('brand').values('name',
                                                    'slug',
                                                    'brand__name',
                                                    'image',
                                                    'price')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        rendered = render_to_string('shop/product/product_by_filter.html', {'products': queryset})
        return JsonResponse({'products': queryset, 'render': rendered})
