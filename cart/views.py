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


"""class CartRemoveView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        cart.remove(product)
        return redirect('cart:cart_detail')"""


class CartRemoveView(View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return JsonResponse({'id': product.id})


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
