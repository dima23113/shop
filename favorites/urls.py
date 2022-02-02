from django.urls import path
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .views import *

app_name = 'favorites'

urlpatterns = [
    path('add/<int:id>/', login_required(AddToFavorites.as_view(), login_url=reverse_lazy('account:login')),
         name='add_to_fav'),
    path('remove/<int:id>/', login_required(RemoveFromFavorites.as_view(), login_url=reverse_lazy('account:login')),
         name='remove_from_fav')
]
