from django.urls import path
from .models import *
from .views import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


app_name = 'account'

urlpatterns = [
    path('', login_required(ProfileView.as_view(), login_url=reverse_lazy('account:login')), name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change')

]
