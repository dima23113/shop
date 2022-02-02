from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from shop.models import Product
from account.models import CustomUser


class AddToFavorites(View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['id'])
        user = CustomUser.objects.get(email=request.user)
        user.favorite.add(product)
        return JsonResponse({'status': 'true', 'message': 'Товар добавлен в избранное!'}, status=200)


class RemoveFromFavorites(View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs['id'])
        user = CustomUser.objects.get(email=request.user)
        user.favorite.remoce(product)
        return JsonResponse({'status': 'true', 'message': 'Товар удален из избранного!'}, status=200)
