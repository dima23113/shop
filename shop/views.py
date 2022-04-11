from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.template.loader import render_to_string
from rest_framework.viewsets import mixins, GenericViewSet

from cart.forms import CartAddProductForm
from .models import *
from .serializers import ProductSerializer, BrandSerializer
from .services import sort_brand_list_into_2_columns, get_product_list_by, get_banners_for_index_page, get_new_items, \
    get_sales_items, get_new_articles


class IndexView(View):

    def get(self, request, *args, **kwargs):
        banners, small_banners = get_banners_for_index_page()
        new_items, sale_items = get_new_items()
        articles = get_new_articles()

        context = {
            'banners': banners,
            'small_banners': small_banners,
            'new_items': new_items,
            'sale_items': sale_items,
            'articles': articles
        }
        return render(request, 'shop/base.html', context=context)


class BrandList(View):

    def get(self, request, *args, **kwargs):
        context = sort_brand_list_into_2_columns()
        return render(request, 'shop/product/brand_list.html', context=context)


class ProductListByCategory(View):

    def get(self, request, *args, **kwargs):
        category, sizes, products, subcategory, subcategory_type, brands = get_product_list_by(category=kwargs['slug'])
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
        brand, products, category, subcategory, subcategory_type, sizes = get_product_list_by(brand=kwargs['slug'])
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
        subcategory, products, category, subcategory_type, brands, sizes = get_product_list_by(
            subcategory=kwargs['slug'])
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
        subcategory_type, products, category, subcategory, sizes, brands = get_product_list_by(
            subcategory_type=kwargs['slug'])
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


class ProductDetail(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.select_related('brand'). \
            defer('compound',
                  'gender',
                  'mark',
                  'type_of',
                  'updated',
                  'created').get(slug=kwargs['slug'])
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


class SaleListView(View):

    def get(self, request, *args, **kwargs):
        subcategory, products, category, subcategory_type, brands, sizes = get_sales_items()
        paginator = Paginator(products, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'subcategory': subcategory,
            'products': page_obj,
            'category': category,
            'subcategory_type': subcategory_type,
            'brand': brands,
            'sizes': sizes
        }
        return render(request, 'shop/product/product_list.html', context=context)


class ProductAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                     GenericViewSet):
    """API для получения списка товаров. Можно редактировать товары и добавлять новые"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.select_related('category').select_related('subcategory').select_related(
            'subcategory_type').select_related('brand').prefetch_related('product_img').prefetch_related(
            'product_sizer').all()
        return queryset


class BrandAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
