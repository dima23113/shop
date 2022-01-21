from django.urls import path
from django.views.decorators.http import require_POST
from .views import *

app_name = 'cart'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<slug:slug>/', require_POST(CartAddView.as_view()), name='cart_add'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
]
