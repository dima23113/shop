from django.urls import path
from .models import *
from .views import *

app_name = 'account'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
]
