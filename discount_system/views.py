from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from .services import product_discount_by_category_discount


class ChangeDiscountPrice(View):

    def get(self, *args, **kwargs):
        product_discount_by_category_discount()
        return HttpResponse('ok')

