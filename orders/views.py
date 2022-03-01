from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from .forms import CreateOrderForm
from .services import order_create
from account.models import CustomUser
from cart.cart import Cart


class OrderCreateView(View):

    def post(self, request, *args, **kwargs):
        form = CreateOrderForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUser.objects.get(email=request.user)
            order_create(cd, user, cart)
            cart.clear()
            if cd['ship_type'] == 'Доставка':
                messages.add_message(request, messages.INFO,
                                     'Ожидание оплаты')
                return redirect('shop:index')
            else:
                return redirect('account:orders')

        else:
            messages.add_message(request, messages.INFO,
                                 'Не выбран тип оплаты/способ доставки или не заполнены данные профиля')
            return redirect('cart:cart_detail')
