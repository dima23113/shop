from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('brand/', cache_page(60*0)(BrandList.as_view()), name='brand_list'),
    path('brand/<slug:slug>/', cache_page(60*0)(ProductListByBrand.as_view()),
         name='product_list_by_brand'),
    path('category/<slug:slug>/', cache_page(60*0)(ProductListByCategory.as_view()),
         name='product_list_by_category'),
    path('subcategory/<slug:slug>/', cache_page(60*0)(ProductListBySubcategory.as_view()),
         name='product_list_by_subcategory'),
    path('subcategory_type/<slug:slug>/', cache_page(60*0)(ProductListBySubcategoryType.as_view()),
         name='product_list_by_subcategory_type'),
    path('products/<slug:slug>/', cache_page(60*0)(ProductDetail.as_view()), name='product_detail'),
    path('json-filter/', JsonFilterProductView.as_view(), name='json_filter'),
    path('sales/', SaleListView.as_view(), name='products_sale')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
