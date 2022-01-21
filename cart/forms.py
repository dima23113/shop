from django import forms

PRODUCT_QTY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartUpdateProductForm(forms.Form):
    qty = forms.TypedChoiceField(choices=PRODUCT_QTY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartAddProductForm(forms.Form):
    size = forms.CharField(required=False, initial=False, widget=forms.HiddenInput)
