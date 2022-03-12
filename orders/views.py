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
            if cd['ship_type'] == 'Самовывоз' and cd['pay_type'] == 'При получении':
                user = CustomUser.objects.get(email=request.user)
                order_create(cd, user, cart)
                cart.clear()
                messages.add_message(request, messages.INFO,
                                     'Заказ сформирован, ожидайте доставки в пункт выдачи!')
                return redirect('shop:index')
            elif cd['ship_type'] == 'Доставка' and cd['pay_type'] == 'При получении':
                messages.add_message(request, messages.INFO,
                                     'Доставка возможна только при оплане онлайн!')
                return redirect('cart:cart_detail')
            else:
                user = CustomUser.objects.get(email=request.user)
                pay = order_create(cd, user, cart)
                cart.clear()
                messages.add_message(request, messages.INFO,
                                     'Заказ сформирован и ожидает оплаты!')
                return redirect(pay)
        else:
            messages.add_message(request, messages.INFO,
                                 'Не выбран тип оплаты/способ доставки или не заполнены данные профиля')
            return redirect('cart:cart_detail')
