from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls

urlpatterns = [
    path('account/', include('account.urls', namespace='account')),
    path('', include('shop.urls', namespace='shop')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('email/', include(email_urls)),
]
