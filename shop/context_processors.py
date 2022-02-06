from .models import *
from cart.cart import Cart


def category(request):

    return {'categories': Category.objects.all().order_by('id'), 'cart_qty': Cart(request)}
