from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator

from search.forms import SearchProductForm
from shop.models import Product
from shop.services import get_left_filter_submenu


class SearchProductListView(View):

    def get(self, request, *args, **kwargs):
        form = SearchProductForm(request.GET)
        if form.is_valid():
            products = Product.objects.filter(
                Q(name__icontains=request.GET.get('search_field')) |
                Q(brand__name__icontains=request.GET.get('search_field')) |
                Q(category__name__icontains=request.GET.get('search_field')) |
                Q(subcategory__name__icontains=request.GET.get('search_field')) |
                Q(subcategory_type__name__icontains=request.GET.get('search_field'))
            ).distinct()
            paginator = Paginator(products, 50)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            category, subcategory, subcategory_type, sizes, brand = get_left_filter_submenu(products)
            context = {
                'products': page_obj,
                'category': category,
                'brand': brand,
                'sizes': sizes,
                'subcategory': subcategory,
                'subcategory_type': subcategory_type
            }
            return render(request, 'shop/product/product_list.html', context=context)
        else:
            return render(request, 'shop/product/product_list.html')
