from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('brand/', BrandList.as_view(), name='brand_list'),
    path('category/<slug:category>/', ProductListByCategory.as_view(),  name='product_list_by_category'),
    path('brand/<slug:slug>/', ProductListByBrand.as_view(), name='product_list_by_brand'),
    path('subcategory/<slug:slug>/', ProductListBySubcategory.as_view(), name='product_list_by_subcategory'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
