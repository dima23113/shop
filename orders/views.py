from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from .forms import CreateOrderForm
from .models import Order, OrderItem
from account.models import CustomUser
from cart.cart import Cart


class OrderCreateView(View):

    def post(self, request, *args, **kwargs):
        form = CreateOrderForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            cd = form.cleaned_data
            ship_type = cd['ship_type']
            pay_type = cd['pay_type']
            user = CustomUser.objects.get(email=request.user)
            order = Order.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                         address=user.address, zip_code=user.zip_code, ship_type=ship_type, paid=False,
                                         customer=user, pay_type=pay_type, phone=user.phone)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], qty=item['qty'],
                                         size=item['size'])
            cart.clear()
            if ship_type == 'Доставка':
                messages.add_message(request, messages.INFO,
                                     'Ожидание оплаты')
                return redirect('shop:index')
            else:
                return redirect('account:orders')

        else:
            messages.add_message(request, messages.INFO,
                                 'Не выбран тип оплаты/способ доставки или не заполнены данные профиля')
            return redirect('cart:cart_detail')
