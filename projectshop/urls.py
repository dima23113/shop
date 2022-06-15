from django.contrib import admin
from django.urls import path, include, re_path
from django_email_verification import urls as email_urls
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from shop.views import ProductAPIView, BrandAPIView
from tickets.views import TicketAPIView
from orders.views import OrderAPIView

router = routers.DefaultRouter()
router.register('ticket', TicketAPIView, basename='ticket')
router.register('product', ProductAPIView, basename='product')
router.register('brand', BrandAPIView, basename='brand')
router.register('order', OrderAPIView, basename='order')

schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
        description='API интернет магазина',
        terms_of_service='',
        contact=openapi.Contact(email='contact@noyabr.gmail'),
        license=openapi.License(name='BSD Licence')
    ),
    public=True,
    permission_classes=[permissions.DjangoModelPermissions],
)

urlpatterns = [
    path('cart/', include('cart.urls', namespace='cart')),
    path('account/', include('account.urls', namespace='account')),
    path('order/', include('orders.urls', namespace='orders')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('tickets/', include('tickets.urls', namespace='tickets')),
    path('search/', include('search.urls', namespace='search')),
    path('loyalty/', include('loyalty_program.urls', namespace='loyalty_program')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('discount/', include('discount_system.urls', namespace='discount_system')),
    path('', include('shop.urls', namespace='shop')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('email/', include(email_urls)),
    path('tinymce/', include('tinymce.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('api/v1/', include(router.urls)),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
