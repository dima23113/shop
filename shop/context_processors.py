from .models import *
from cart.cart import Cart
from search.forms import SearchProductForm


def category(request):
    search_form = SearchProductForm()

    return {'categories': Category.objects.all().order_by('id'), 'cart_qty': Cart(request), 'search_form': search_form}
