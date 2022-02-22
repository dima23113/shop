from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from shop.models import Product, ProductSize
from .cart import Cart
from .forms import CartUpdateProductForm, CartAddProductForm
from orders.forms import CreateOrderForm


class CartAddView(View):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=kwargs['slug'])
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, qty=1, size=cd['size'], update_qty=False)
        return redirect('cart:cart_detail')


class CartRemoveProductView(View):

    def post(self, request, *args, **kwargs):
        remove_all = request.POST.get('remove_all', None)
        product_id = request.POST.get('product_id', None)
        cart = Cart(request)
        if remove_all:
            cart.clear()
            return JsonResponse({'status': 'true', 'message': 'Корзина удалена'}, status=200)
        else:
            product = get_object_or_404(Product, id=product_id.split('-')[0])
            cart.remove(product_id)
            return JsonResponse({'id': product.id})


class CartDetailView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = CartUpdateProductForm()
        order_form = CreateOrderForm()
        return render(request, 'cart/detail.html', {'cart': cart, 'form': form, 'order_form': order_form})


class CartUpdateView(View):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=kwargs['slug'])
        form = CartUpdateProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, qty=cd['qty'], update_qty=cd['update'])
        return redirect('cart:cart_detail')


class QtyProductSizeView(View):

    def get(self, request, *args, **kwargs):
        product = request.GET.get('product', None)
        size = request.GET.get('size', None)
        if product and size:
            product_size = ProductSize.objects.filter(product__name=product, name=size)[0]
            response = {
                'max_qty': product_size.qty,
                'product': product,
                'size': size
            }
            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'false', 'message': 'Корзина пуста'}, status=404)

    def post(self, request, *args, **kwargs):
        product = request.POST.get('product', None)
        max_qty = request.POST.get('max_qty', None)
        qty = request.POST.get('qty', None)
        size = request.POST.get('size', None)
        if qty and max_qty:
            cart = Cart(request)
            qty = int(qty)
            max_qty = int(max_qty)
            if max_qty >= qty > 0:
                cart.cart[product]['qty'] = qty
                cart.save()
                return JsonResponse({'status': 'true', 'message': 'Изменения внесены!'}, status=200)
            else:
                return JsonResponse(
                    {'status': 'true', 'message': 'Текущее ко-во больше доступного или не может быть 0'}, status=200)
        else:
            return JsonResponse({'status': 'false', 'message': 'Ко-во товара или максимальное ко-во незадано!'},
                                status=404)


class CartPriceView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        response = {'price': cart.get_total_price(), 'price_discount': cart.get_total_discount_price()}
        return JsonResponse(response)


class UpdateQtyCartView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        response = {'cart_qty': len(cart)}
        return JsonResponse(response)
