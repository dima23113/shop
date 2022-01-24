from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from shop.models import Product, ProductSize
from .cart import Cart
from .forms import CartUpdateProductForm, CartAddProductForm


class CartAddView(View):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=kwargs['slug'])
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, qty=1, size=cd['size'], update_qty=False)
        return redirect('cart:cart_detail')


class CartRemoveView(View):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart.remove(product)
        return redirect('cart:cart_detail')


class CartDetailView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        form = CartUpdateProductForm()
        for item in cart:
            item['update_qty_form'] = CartUpdateProductForm(initial={'qty': item['qty'], 'update': True})
        return render(request, 'cart/detail.html', {'cart': cart, 'form': form})


class CartUpdateView(View):

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=kwargs['slug'])
        form = CartUpdateProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, qty=cd['qty'], update_qty=cd['update'])
        return redirect('cart:cart_detail')


class CheckQtyProductView(View):

    def get(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id', None)
        size = request.GET.get('size', None)
        s = ProductSize.objects.filter(product__id=product_id, name=size).select_related('product')[0]
        response = {
            'product_id': product_id,
            'size': size,
            'qty': s.qty,
            'product_name': s.product.name
        }
        return JsonResponse(response)

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id', None)
        size = request.POST.get('size', None)
        sign = request.POST.get('sign', None)
        qty_now = request.POST.get('qty_now', None)
        max_qty = request.POST.get('max_qty', None)
        print(product_id)
        print(sign)
        print(qty_now)
        print(max_qty)
        cart = Cart(request)
        if product_id in cart.cart.keys():
            if int(qty_now) <= int(max_qty):
                if sign == "+":
                    cart.cart[product_id]['qty'] += 1
                    response = {
                        'qty_now': cart.cart[product_id]['qty']
                    }
                    return JsonResponse(response, safe=False)
                else:
                    cart.cart[product_id]['qty'] -= 1
                    response = {
                        'qty_now': cart.cart[product_id]['qty']
                    }
                    return JsonResponse(response, safe=False)
            elif qty_now == '0':
                cart.cart[product_id]['qty'] = 1
                response = {
                    'qty_now': cart.cart[product_id]['qty']
                }
                return JsonResponse(response, safe=False)
            else:
                response = {
                    'qty_now': cart.cart[product_id]['qty']
                }
                return JsonResponse(response, safe=False)
