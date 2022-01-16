from django.urls import path, include
from .models import *
from .views import *
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls

app_name = 'account'

urlpatterns = [
    path('', login_required(ProfileView.as_view(), login_url=reverse_lazy('account:login')), name='profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",
                                                     success_url=reverse_lazy('account:login')),
         name='password_reset_confirm'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('email/', include(email_urls)),

]
