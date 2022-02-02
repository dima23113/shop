from django.urls import path, include
from .models import *
from .views import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', login_required(ProfileView.as_view(), login_url=reverse_lazy('account:login')), name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",
                                                     success_url=reverse_lazy('account:login')),
         name='password_reset_confirm'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('address/', login_required(AddressesProfileView.as_view(), login_url=reverse_lazy('account:login')),
         name='address'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('favorites/', FavoritesDetailView.as_view(), name='favorites')
]
