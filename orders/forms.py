from django import forms
from .models import Order


class CreateOrderForm(forms.Form):
    ship_type = forms.CharField(required=True, initial=False)
    pay_type = forms.CharField(required=True, initial=False)


