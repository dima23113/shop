from django.shortcuts import render, get_object_or_404
from .models import *
from .services import get_product_list
from django.core.paginator import Paginator


class ProductsObjectMixin:
    model = None
    template = 'shop/product/product_list.html'

    def get(self, request, *args, **kwargs):
        products, brand, category, subcategory, subcategory_type, sizes = get_product_list(
            self.model.__name__.lower(), kwargs['slug'])
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj,
            'category': category,
            'brand': brand,
            'sizes': sizes,
            'subcategory': subcategory,
            'subcategory_type': subcategory_type
        }
        return render(request, self.template, context=context)
