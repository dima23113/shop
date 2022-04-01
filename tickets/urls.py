from django.urls import path
from .views import CreateTicketView


app_name = 'tickets'


urlpatterns = [
    path('create-ticket/', CreateTicketView.as_view(), name='create_ticket')
]
