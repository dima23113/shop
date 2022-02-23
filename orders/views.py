from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from django.db.models import F
from .forms import CreateOrderForm
from .models import Order, OrderItem
from .services import update_amount_of_purchases
from account.models import CustomUser
from cart.cart import Cart
from shop.models import ProductSize
from loyalty_program.models import UserBonuses


class OrderCreateView(View):

    def post(self, request, *args, **kwargs):
        form = CreateOrderForm(request.POST)
        cart = Cart(request)
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUser.objects.get(email=request.user)
            order = Order.objects.create(first_name=user.first_name, last_name=user.last_name, email=user.email,
                                         address=user.address, zip_code=user.zip_code, ship_type=cd['ship_type'],
                                         paid=False,
                                         customer=user, pay_type=cd['pay_type'], phone=user.phone)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], qty=item['qty'],
                                         size=item['size'], price_discount=item['discount_price'])
                ProductSize.objects.filter(product_id=item['product'], name=item['size']).update(
                    qty=F('qty') - int(item['qty']))
            bonuses = UserBonuses.objects.get(user=user)
            bonuses.bonuses = bonuses.bonuses + (
                        (bonuses.bonuses_program.bonus_percentage / 100) * float(order.get_total_discount_cost()))
            bonuses.save()
            user.amount_of_purchases = update_amount_of_purchases(user)
            user.save()
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
