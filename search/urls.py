from django.urls import path
from .views import *

app_name = 'search'

urlpatterns = [
    path('', SearchProductListView.as_view(), name='product_search'),

]
