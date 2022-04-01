from django.forms import ModelForm
from .models import Ticket


class CreateTicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'order_number', 'text']
