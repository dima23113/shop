from django.views.generic import View
from django.http import JsonResponse

from shop.models import Product
from account.models import CustomUser


class AddToFavorites(View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.POST.get('product'))
        user = CustomUser.objects.get(email=request.user)
        user.favorite.add(product)
        return JsonResponse({'status': 'true', 'message': 'Товар добавлен в избранное!'}, status=200)


class RemoveFromFavorites(View):

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.POST.get('product'))
        user = CustomUser.objects.get(email=request.user)
        user.favorite.remove(product)
        return JsonResponse({'status': 'true', 'message': 'Товар удален из избранного!'}, status=200)
