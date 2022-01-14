from django.urls import path
from .models import *
from .views import *


app_name = 'account'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change')

]
