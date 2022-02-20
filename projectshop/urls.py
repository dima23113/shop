from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls

urlpatterns = [
    path('cart/', include('cart.urls', namespace='cart')),
    path('account/', include('account.urls', namespace='account')),
    path('order/', include('orders.urls', namespace='orders')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('search/', include('search.urls', namespace='search')),
    path('loyalty/', include('loyalty_program.urls', namespace='loyalty_program')),
    path('discount/', include('discount_system.urls', namespace='discount_system')),
    path('', include('shop.urls', namespace='shop')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('email/', include(email_urls)),
    path('tinymce/', include('tinymce.urls')),
]
