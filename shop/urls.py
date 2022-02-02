from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('brand/', BrandList.as_view(), name='brand_list'),
    path('brand/<slug:slug>/', ProductListByBrand.as_view(), name='product_list_by_brand'),
    path('category/<slug:slug>/', ProductListByCategory.as_view(),  name='product_list_by_category'),
    path('subcategory/<slug:slug>/', ProductListBySubcategory.as_view(), name='product_list_by_subcategory'),
    path('products/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
